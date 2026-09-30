#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fastfix.py —— FixCover 的「增量 / 差异」重写（基准里的 C 方案，可丢进 KUAL）

原版每一步都在做全量工作：
  ① 对 cc.db 里**每一本**书 `open(path,'rb').read()` 整本读入内存（Sectionizer.__init__）；
  ② 再对每一个资源段跑 `imghdr.what()` 找封面；
  ③ 读完之后才判断"这本要不要修"（FixCover.py:154 → 166）。
⇒ 每次运行的工作量是 O(整库字节数)，而真正需要的只是"坏掉的那几张"。

本脚本的三层改进（可分别独立生效）：

  【1】工作清单先行（等价 git 的 index）
      cc.db 的 `p_thumbnail` + 缩略图文件大小本身就是索引：
      `p_thumbnail IS NULL` 或 文件缺失或 <2000 字节 ⇒ 才需要动手。
      健康书一次 stat 都不做，更不读文件。

  【2】定位式取封面（等价"只读需要的那个对象"）
      ★ 原版那圈 imghdr 扫描对结果**没有任何影响**：`imgnames` 无论是不是图片
        都只 append 一个元素，所以 `len(imgnames)-1 == coverid` 恒等于
        「迭代次数 == coverid」，函数返回的永远是 `sections[firstresource + CoverOffset]`。
      ⇒ 封面位置 = PDB 段号 `firstresource + EXTH(201)`，**不需要扫描、不需要整本读**。
      只读：78 字节 PDB 头 + 8n 字节记录表 + record 0（含 EXTH）+ 封面那一段。
      一本 10MB 的书从"读 10MB"变成"读 ~50KB"。

  【3】内容寻址封面仓 + stat 差异（等价 git 的 object store + racy-git 之外的 stat 快路径）
      covers/<sha1[:2]>/<sha1>.jpg 存提取出来的封面字节（内容寻址、天然去重）；
      索引 `fixcover-index.json` 记 p_location → (size, mtime_ns, asin, cde, sha1)。
      书的 (size, mtime) 没变 且 blob 还在 ⇒ **一个字节都不用从书里读**，
      直接把封面从仓里写回缩略图。适用于"缩略图被同步/清理弄丢了要重建"。

用法（Kindle 上）：
    python3 fastfix.py /mnt/us --status     # 只看差异，什么都不改（像 git status）
    python3 fastfix.py /mnt/us --fix        # 增量修复
    python3 fastfix.py /mnt/us --rebuild    # 忽略索引，全部重读（等价原版工作量但仍是定位式）
"""
from __future__ import print_function

import argparse
import hashlib
import json
import os
import sqlite3
import struct
import sys
import tempfile
import time

DAMAGED_SIZE = 2000          # 与原版 is_damaged_thumbnail 一致
THUMB_DIR = os.path.join('system', 'thumbnails')
DOC_DIR = 'documents'
DEFAULT_DB = '/var/local/cc.db'

EXTH_COVER_OFFSET = 201
EXTH_ASIN = 113
EXTH_DOC_TYPE = 501


# ────────────────────────────────────────────────────────────────
# 最小 I/O：只读 PDB 表 + record 0 + 封面那一段
# ────────────────────────────────────────────────────────────────
class Counter(object):
    def __init__(self):
        self.bytes_read = 0
        self.books_read = 0

    def read(self, f, n):
        b = f.read(n)
        self.bytes_read += len(b)
        return b


def read_pdb_table(f, ctr):
    f.seek(0)
    hdr = ctr.read(f, 78)
    if len(hdr) < 78:
        raise ValueError('not a PDB')
    n = struct.unpack_from('>H', hdr, 76)[0]
    table = ctr.read(f, 8 * n)
    if len(table) < 8 * n:
        raise ValueError('truncated record table')
    offs = [struct.unpack_from('>L', table, i * 8)[0] for i in range(n)]
    return n, offs


def parse_exth(rec0):
    """返回 {exth_id: payload_bytes}。EXTH flags 在 record 0 的**偏移 128**（MOBI 头相对 0x70）。"""
    if len(rec0) < 132:
        return {}
    flags = struct.unpack_from('>L', rec0, 128)[0]
    if not (flags & 0x40):
        return {}
    mh_len = struct.unpack_from('>L', rec0, 20)[0]
    start = 16 + mh_len
    if rec0[start:start + 4] != b'EXTH':
        return {}
    count = struct.unpack_from('>L', rec0, start + 8)[0]
    pos = start + 12
    out = {}
    for _ in range(count):
        if pos + 8 > len(rec0):
            break
        tid, size = struct.unpack_from('>LL', rec0, pos)
        if size < 8 or pos + size > len(rec0):
            break
        out[tid] = rec0[pos + 8:pos + size]
        pos += size
    return out


def _exth_int(payload):
    """EXTH 无类型系统，按 payload 长度推断整数（4→>L，2→>H，1→B）。"""
    if payload is None:
        return None
    if len(payload) == 4:
        return struct.unpack('>L', payload)[0]
    if len(payload) == 2:
        return struct.unpack('>H', payload)[0]
    if len(payload) == 1:
        return struct.unpack('B', payload)[0]
    return None


def _exth_str(payload):
    if not payload:
        return None
    try:
        return payload.decode('utf-8')
    except UnicodeDecodeError:
        return payload.decode('latin-1')


def read_cover(path, ctr):
    """定位式提取封面。返回 (cover_bytes|None, meta_dict, coverid)。"""
    meta = {'asin': None, 'cde': None, 'coverid': None, 'drm': None}
    size = os.path.getsize(path)
    with open(path, 'rb') as f:
        n, offs = read_pdb_table(f, ctr)
        if n < 2:
            return None, meta, None
        rec0_len = offs[1] - offs[0]
        f.seek(offs[0])
        rec0 = ctr.read(f, rec0_len)

        e = parse_exth(rec0)
        meta['asin'] = _exth_str(e.get(EXTH_ASIN))
        meta['cde'] = _exth_str(e.get(EXTH_DOC_TYPE))
        coverid = _exth_int(e.get(EXTH_COVER_OFFSET))
        meta['coverid'] = coverid
        if coverid is None:
            return None, meta, None

        # firstresource（MOBI 头相对 0x50 ⇒ record 0 内 0x60? 不 —— 见下）
        # KindleUnpack 用 header[0x6C]：即 record 0 内绝对偏移 0x6C = 108
        first_res = struct.unpack_from('>L', rec0, 0x6C)[0]
        if first_res == 0xFFFFFFFF:
            records = struct.unpack_from('>H', rec0, 8)[0]
            first_res = records + 1                      # KindleUnpack 的默认值

        idx = first_res + coverid
        if idx < 0 or idx >= n:
            return None, meta, coverid
        start = offs[idx]
        end = offs[idx + 1] if idx + 1 < n else size
        f.seek(start)
        cover = ctr.read(f, end - start)
    return cover, meta, coverid


# ────────────────────────────────────────────────────────────────
# 内容寻址封面仓 + stat 差异索引
# ────────────────────────────────────────────────────────────────
class Store(object):
    def __init__(self, base):
        self.base = base
        self.covers = os.path.join(base, 'covers')
        self.index_path = os.path.join(base, 'fixcover-index.json')
        self.index = {'version': 1, 'entries': {}}
        try:
            # 显式 utf-8：Windows 上 open() 默认走本地代码页（cp936），
            # 会把 UTF-8 的索引读炸（UnicodeDecodeError 是 ValueError 子类 ⇒ 被下面吞掉 ⇒ 静默退化全量）。
            with open(self.index_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, dict) and 'entries' in data:
                self.index = data
        except (IOError, ValueError):
            # 索引存在但读不回来 ⇒ 会退化成全量重读。这必须说出来，不能静默。
            if os.path.exists(self.index_path):
                sys.stderr.write('[warn] index unreadable, falling back to full re-read: %s\n'
                                 % self.index_path)

    def blob_path(self, digest):
        return os.path.join(self.covers, digest[:2], digest + '.jpg')

    def has(self, digest):
        return os.path.exists(self.blob_path(digest))

    def get(self, digest):
        with open(self.blob_path(digest), 'rb') as f:
            return f.read()

    def put(self, data):
        digest = hashlib.sha1(data).hexdigest()
        p = self.blob_path(digest)
        if not os.path.exists(p):
            d = os.path.dirname(p)
            if not os.path.isdir(d):
                os.makedirs(d)
            _atomic_write(p, data)
        return digest

    def lookup(self, p_location, size, mtime_ns):
        ent = self.index['entries'].get(p_location)
        if not ent:
            return None
        if ent.get('size') != size or ent.get('mtime_ns') != mtime_ns:
            return None
        if not self.has(ent.get('sha1', '')):
            return None
        return ent

    def record(self, p_location, size, mtime_ns, digest, meta, thumb):
        self.index['entries'][p_location] = {
            'size': size, 'mtime_ns': mtime_ns, 'sha1': digest,
            'asin': meta.get('asin'), 'cde': meta.get('cde'),
            'coverid': meta.get('coverid'), 'thumb': thumb,
            'indexed_at': int(time.time()),
        }

    def save(self):
        if not os.path.isdir(self.base):
            os.makedirs(self.base)
        # ensure_ascii=True：索引里全是路径，转义成纯 ASCII 后可跨任意 locale 读回
        _atomic_write(self.index_path,
                      json.dumps(self.index, ensure_ascii=True, sort_keys=True).encode('utf-8'))


def _atomic_write(path, data):
    """先写临时文件再 rename —— 避免断电/被杀留下 0 字节文件（那正好会被判成"损坏"）。"""
    d = os.path.dirname(path) or '.'
    fd, tmp = tempfile.mkstemp(dir=d, prefix='.tmp-')
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(data)
        if os.path.exists(path):
            os.remove(path)
        os.rename(tmp, path)
    except Exception:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise


# ────────────────────────────────────────────────────────────────
# 主流程
# ────────────────────────────────────────────────────────────────
def is_damaged(path):
    try:
        return os.path.getsize(path) < DAMAGED_SIZE
    except OSError:
        return True


def thumbnail_name(asin, cde):
    return 'thumbnail_%s_%s_portrait.jpg' % (asin, cde)


def run(root, mode, db_path, cache_dir, quiet):
    docs = os.path.join(root, DOC_DIR)
    thumbs = os.path.join(root, THUMB_DIR)
    if not os.path.isdir(thumbs):
        print('[NG] no thumbnail dir: %s' % thumbs)
        return 2

    # --status 只读，不锁库、不写库
    uri = 'file:%s%s' % (db_path, '?mode=ro' if mode == 'status' else '')
    try:
        con = sqlite3.connect(uri, uri=True, check_same_thread=False,
                              timeout=10) if mode == 'status' else \
            sqlite3.connect(db_path, check_same_thread=False, timeout=10)
    except TypeError:                                   # 老 python 不支持 uri
        con = sqlite3.connect(db_path, check_same_thread=False, timeout=10)

    rows = con.execute(
        "SELECT p_uuid, p_location, p_thumbnail, p_cdeType FROM Entries "
        "WHERE p_cdeType IN ('EBOK','PDOC') AND p_location IS NOT NULL").fetchall()

    store = Store(cache_dir)
    ctr = Counter()
    st = {'rows': len(rows), 'need': 0, 'skip_healthy': 0, 'skip_notebook': 0,
          'skip_missing': 0, 'from_store': 0, 'from_book': 0, 'no_cover': 0,
          'fixed': 0, 'generated': 0, 't0': time.time()}

    valid_ext = ('.mobi', '.azw', '.azw3', 'azw4')
    pending = []

    for p_uuid, p_location, p_thumbnail, p_cde in rows:
        # ──【1】工作清单：要不要修？（零文件读，最多一次 stat） ──────────
        if p_thumbnail is None:
            need = p_cde in ('EBOK', 'PDOC')
        elif not os.path.exists(p_thumbnail) or is_damaged(p_thumbnail):
            need = True
        else:
            need = False

        if not need:
            st['skip_healthy'] += 1
            continue
        st['need'] += 1

        is_kual = p_location.endswith('KUAL.kual')
        if not (is_kual or p_location.endswith(valid_ext)):
            st['skip_notebook'] += 1
            continue
        if not os.path.exists(p_location):
            st['skip_missing'] += 1
            continue

        if mode == 'status':
            # status 模式只报告：连书的 stat 都不做，只把"哪几本要修"记下来
            if p_thumbnail is None:
                state = 'no thumbnail registered'
            elif not os.path.exists(p_thumbnail):
                state = 'thumbnail file missing'
            else:
                state = 'thumbnail damaged (%d bytes)' % os.path.getsize(p_thumbnail)
            pending.append((os.path.basename(p_location), p_cde, state))
            continue

        # ──【3】先问索引：这本书没变过吗？ ─────────────────────────────
        sb = os.stat(p_location)
        size, mtime_ns = sb.st_size, getattr(sb, 'st_mtime_ns', int(sb.st_mtime * 1e9))
        ent = None if mode == 'rebuild' else store.lookup(p_location, size, mtime_ns)

        if ent is not None:
            cover = store.get(ent['sha1'])
            meta = {'asin': ent.get('asin'), 'cde': ent.get('cde'), 'coverid': ent.get('coverid')}
            st['from_store'] += 1
        else:
            # ──【2】定位式取封面（不扫描、不整本读） ────────────────────
            try:
                cover, meta, _ = read_cover(p_location, ctr)
            except (IOError, OSError, ValueError, struct.error):
                cover, meta = None, {}
            ctr.books_read += 1
            st['from_book'] += 1

        if is_kual:
            try:
                cover = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kual.jpg'), 'rb').read()
            except IOError:
                pass

        if not cover:
            st['no_cover'] += 1
            continue

        if ent is None:
            digest = store.put(cover)
            store.record(p_location, size, mtime_ns, digest, meta, p_thumbnail)

        if p_thumbnail is None:
            asin = meta.get('asin') or p_uuid
            cde = meta.get('cde') or p_cde
            p_thumbnail = os.path.join(thumbs, thumbnail_name(asin, cde))
            _atomic_write(p_thumbnail, cover)
            con.execute('UPDATE Entries SET p_thumbnail = ? WHERE p_location = ?',
                        (p_thumbnail, p_location))
            st['generated'] += 1
        else:
            _atomic_write(p_thumbnail, cover)
            st['fixed'] += 1

        if not quiet:
            print('  + %s' % os.path.basename(p_thumbnail))

    if mode != 'status':
        con.commit()
        store.save()
    con.close()

    dt = time.time() - st['t0']
    print('')
    print('[i] mode            : %s' % mode)
    print('[i] cc.db rows      : %d' % st['rows'])
    print('[i] need fix        : %d   (healthy skipped: %d / not-ebook: %d / missing file: %d)'
          % (st['need'], st['skip_healthy'], st['skip_notebook'], st['skip_missing']))
    print('[i] cover from      : book=%d  store=%d' % (st['from_book'], st['from_store']))
    print('[i] fixed/generated : %d / %d   (no cover found: %d)' % (st['fixed'], st['generated'], st['no_cover']))
    print('[i] BOOK BYTES READ : %d  (= %.2f MB)  over %d file(s)'
          % (ctr.bytes_read, ctr.bytes_read / 1048576.0, ctr.books_read))
    print('[i] elapsed         : %.2fs' % dt)
    print('[i] index entries   : %d' % len(store.index['entries']))
    if mode == 'status':
        if pending:
            print('')
            print('[i] --- books that need fixing (%d) ---' % len(pending))
            for name, cde, state in pending[:60]:
                print('    - %s  [%s]  %s' % (name, cde, state))
            if len(pending) > 60:
                print('    ... and %d more' % (len(pending) - 60))
        else:
            print('[i] nothing to fix -- every registered thumbnail looks healthy')
    return 0


def main():
    ap = argparse.ArgumentParser(description='Incremental Kindle ebook cover fixer')
    ap.add_argument('root', nargs='?', default='/mnt/us', help='Kindle root (default /mnt/us)')
    g = ap.add_mutually_exclusive_group()
    g.add_argument('--status', action='store_true', help='只报告差异，不修改（默认）')
    g.add_argument('--fix', action='store_true', help='增量修复')
    g.add_argument('--rebuild', action='store_true', help='忽略索引，全部重新提取')
    ap.add_argument('--db', default=DEFAULT_DB, help='cc.db 路径')
    ap.add_argument('--cache', default=None, help='索引与封面仓目录')
    ap.add_argument('-q', '--quiet', action='store_true')
    args = ap.parse_args()

    mode = 'rebuild' if args.rebuild else ('fix' if args.fix else 'status')
    cache = args.cache or os.path.join(os.path.dirname(os.path.abspath(__file__)), '.fixcover')
    return run(args.root, mode, args.db, cache, args.quiet)


if __name__ == '__main__':
    sys.exit(main())

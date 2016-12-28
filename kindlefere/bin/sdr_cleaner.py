#!/usr/bin/python
# -*- coding:utf-8 -*-

import datetime
import glob
import os
import shutil
import sys

# fix ''ascii' codec can't decode byte 0xe8 in position ...'
# reload(sys)
# sys.setdefaultencoding('utf-8')

# define flag
clean_screenshot = False
generate_log = True


def do_clean_screenshot(kindle_path):
    screenshot_list = []
    for screenshot_file in glob.glob1(kindle_path, 'screenshot*.png'):
        os.remove(os.path.join(kindle_path, screenshot_file))
        screenshot_list.append(screenshot_file)
    for screenshot_file in glob.glob1(kindle_path, 'wininfo_screenshot*.txt'):
        os.remove(os.path.join(kindle_path, screenshot_file))
    return screenshot_list


def do_clean_sdr(documents_path):
    book_suffixs = [
        '.azw',
        '.azw3',
        '.pdf',
        '.txt',
        '.prc',
        '.mobi',
        '.pobi',
        '.epub',
        '.azw4',
        '.kfx',
    ]
    sdr_suffixs = [
        '.sdr',
        '.dir'
    ]
    book_names = set()
    for book_suffix in book_suffixs:
        book_names |= set([os.path.splitext(name)[0] for name in glob.glob1(documents_path, '*' + book_suffix)])
    sdr_names = set()
    for sdr_suffix in sdr_suffixs:
        sdr_names |= set([os.path.splitext(name)[0] for name in glob.glob1(documents_path, '*' + sdr_suffix)])
    # 差集为需要删除的文件夹
    sdr_fail_list = []
    sdr_success_list = []
    for unused_sdr_name in sdr_names - book_names:
        for sdr_suffix in sdr_suffixs:
            sdr_path = os.path.join(documents_path, unused_sdr_name + sdr_suffix)
            if os.path.exists(sdr_path):
                try:
                    shutil.rmtree(sdr_path)
                except OSError:
                    sdr_fail_list.append(sdr_path)
                else:
                    sdr_success_list.append(sdr_path)
    return sdr_success_list, sdr_fail_list


def do_log_success(log_file, name, file_list):
    log_file.write('成功删除 ' + str(len(file_list)) + ' 个' + name)
    log_file.write(': \n---------------------------------\n')
    for file_path in file_list:
        log_file.write(file_path + '\n')
    log_file.write('=================================\n')


def do_log_fail(log_file, name, file_list):
    if file_list:
        log_file.write('有 ' + str(len(file_list)) + ' 个' + name + '删除失败')
        log_file.write(': \n---------------------------------\n')
        for file_path in file_list:
            log_file.write(file_path + '\n')
        log_file.write('=================================\n')


def do_generate_log(log_path, sdr_success_list, sdr_fail_list, screenshot_list):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_path, 'w') as new_log:
        new_log.write('清理时间 ' + current_time)
        new_log.write('\n=================================\n')
        do_log_success(new_log, '无用 SDR 文件夹', sdr_success_list)
        do_log_fail(new_log, '无用 SDR 文件夹', sdr_fail_list)
        if sdr_fail_list:
            new_log.write('* 删除失败是因为该文件名中含有特殊字符无法被删除，目前还没找到好的办法解决，请暂时手动删除。\n')
            new_log.write('---------------------------------\n')
        do_log_success(new_log, '截图', screenshot_list)
        new_log.write('Kindle 伴侣 - 为精心阅读而生\nhttp://kindlefere.com\n')


# Process
def process_clean(kindle_path):
    documents_path = os.path.join(kindle_path, 'documents')
    if not os.path.exists(documents_path):
        sys.exit(-1)
    log_path = os.path.join(documents_path, 'sdr_cleaner.log')
    if os.path.exists(log_path):
        os.remove(log_path)

    # Clean Screen Shot
    screenshot_list = []
    if clean_screenshot:
        screenshot_list = do_clean_screenshot(kindle_path)
    # Clean SDR Folder
    sdr_success_list, sdr_fail_list = do_clean_sdr(documents_path)
    # Generate Clean Log
    if generate_log:
        do_generate_log(log_path, sdr_success_list, sdr_fail_list, screenshot_list)


if __name__ == '__main__':
    # Execute
    process_clean('/path/to/kindle')

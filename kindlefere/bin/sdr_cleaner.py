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


def do_clean_dir(documents_path, book_names, dir_names, dir_suffixs):
    fail_list = []
    success_list = []
    # 差集为需要删除的文件夹
    for unused_name in dir_names - book_names:
        for dir_suffix in dir_suffixs:
            dir_path = os.path.join(documents_path, unused_name + dir_suffix)
            if os.path.exists(dir_path):
                try:
                    shutil.rmtree(dir_path)
                except OSError:
                    fail_list.append(dir_path)
                else:
                    success_list.append(dir_path)
    return success_list, fail_list


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


def get_names(path, patterns):
    names = set()
    for pattern in patterns:
        names |= set([os.path.splitext(name)[0] for name in glob.glob1(path, pattern)])
    return names


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
    book_patterns = [
        '*.azw',
        '*.azw3',
        '*.pdf',
        '*.txt',
        '*.prc',
        '*.mobi',
        '*.pobi',
        '*.epub',
        '*.azw4',
        '*.kfx',
    ]
    sdr_suffixs = [
        '.sdr',
    ]
    dir_suffixs = [
        '.dir'
    ]
    book_names = get_names(documents_path, book_patterns)
    sdr_names = get_names(documents_path, ['*'+suffix for suffix in sdr_suffixs])
    dir_names = get_names(documents_path, ['*'+suffix for suffix in dir_suffixs])
    # Clean SDR Folder
    sdr_success_list, sdr_fail_list = do_clean_dir(documents_path, book_names, sdr_names, sdr_suffixs)
    # Clean DIR Folder
    dir_success_list, dir_fail_list = do_clean_dir(documents_path, book_names, dir_names, dir_suffixs)
    # Generate Clean Log
    if generate_log:
        with open(log_path, 'w') as new_log:
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_log.write('清理时间 ' + current_time)
            new_log.write('\n=================================\n')
            do_log_success(new_log, '无用 SDR 文件夹', sdr_success_list)
            do_log_fail(new_log, '无用 SDR 文件夹', sdr_fail_list)
            do_log_success(new_log, '无用 DIR 文件夹', dir_success_list)
            do_log_fail(new_log, '无用 DIR 文件夹', dir_fail_list)
            do_log_success(new_log, '截图', screenshot_list)
            new_log.write('Kindle 伴侣 - 为精心阅读而生\nhttp://kindlefere.com\n')


if __name__ == '__main__':
    process_clean(sys.argv[1])

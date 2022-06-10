#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import glob
import imghdr
import string
import tempfile

from File import MOBIFile


class FixCover:
    version = '1.0'
    description = 'A script to fix damaged cover of Kindle ebook.\n\
Detail: https://bookfere.com/post/986.html'


    def __init__(self, logger=None, progress=None):
        self.logger = logger
        self.progress = progress

        self.print_log('Version: %s' % self.version)
        self.print_log(self.description, True)


    def print_log(self, text, sep=False):
        if self.logger is not None:
            divider = '-------------------------------------------'
            text =  '%s\n%s\n%s' % (divider, text, divider) \
                if sep is True else text
            self.logger(text)


    def print_progress(self, factor):
        if self.progress is not None:
            self.progress(factor)


    def get_filepath_list(self, path):
        return glob.glob('%s%s**' % (path, os.sep), recursive=True)


    def get_filename(self, path):
        return path.split('/')[-1];


    def get_damaged_thumbnails(self, path):
        thumbnails = dict()
        for thumbnail in self.get_filepath_list(path):
            asin = re.match(rf'.*{re.escape(os.sep)}thumbnail_(.+)_EBOK.+', thumbnail)
            if asin is not None and os.path.getsize(thumbnail) < 2000:
                thumbnails[asin.group(1)] = thumbnail
                self.print_log('- %s' % self.get_filename(thumbnail))
        return thumbnails


    def is_valid_ebook_file(self, filename):
        for ext in ['.mobi', '.azw', '.azw3', 'azw4']:
            if filename.endswith(ext):
                return True
        return False


    def get_ebook_list(self, path):
        ebook_list = []
        for filename in self.get_filepath_list(path):
            if not self.is_valid_ebook_file(filename):
                continue
            ebook_list.append(filename)
        return ebook_list


    def fix_damaged_thumbnails(self, path, thumbnails):
        ebook_list = self.get_ebook_list(path)
        failure_jobs = {
            'cover_errors': [],
            'ebook_errors': [],
        }
        for filepath in ebook_list:
            self.print_progress(len(ebook_list))

            try:
                mobi_file = MOBIFile(filepath)
            except:
                continue

            ebook_asin = mobi_file.get_metadata('ASIN')
            # ebook_type = mobi_file.get_metadata('Document Type')

            if ebook_asin in thumbnails.keys():
                # self.print_log('- %s' % filepath)
                store_path = thumbnails[ebook_asin]
                filename = self.get_filename(store_path)
                try:
                    cover_data = mobi_file.get_cover_image()
                    img_format = imghdr.what(None, h=cover_data)
                    with open(store_path, 'wb') as file:
                        file.write(cover_data)
                    self.print_log('✓ %s' % filename)
                except:
                    failure_jobs['ebook_errors'].append(
                        self.get_filename(store_path) +
                        '\n  └ %s' % self.get_filename(filepath)
                    )
                finally:
                    del thumbnails[ebook_asin]

        failure_jobs['cover_errors'] = [
            self.get_filename(thumbnail) for thumbnail in thumbnails.values()
        ]

        self.print_progress(0);

        return failure_jobs


    def get_kindle_path(self, path):
        return (
            os.path.join(path, 'documents'),
            os.path.join(path, 'system', 'thumbnails')
        )


    def is_kindle_root(self, path):
        for path in self.get_kindle_path(path):
            if os.path.exists(path) is False:
                return False
        return True


    def get_kindle_root_manually(self, args):
        roots = []
        for path in args:
            path = os.path.join(path)
            if self.is_kindle_root(path):
                roots.append(path)
            else:
                message = '%s is not a kindle root directory.' % path \
                    if path != '' else 'You need choose a Kindle root directory.'
                self.print_log(message)
        return roots


    def get_kindle_root_automatically(self):
        drives = []
        roots = []

        if sys.platform.startswith('win'):
            drives = ['%s:\\' % s.upper() for s in string.ascii_lowercase[:26]]
            drives.reverse()
        elif sys.platform.startswith('darwin'):
            drives = glob.glob('/Volumes/*')

        for drive in drives:
            path = os.path.join('%s' % drive)
            if self.is_kindle_root(path):
                roots.append(path)

        return roots


    def get_kindle_root(self, roots):
        if len(roots) > 0:
            return self.get_kindle_root_manually(roots)
        return self.get_kindle_root_automatically()


    def handle(self, path = []):
        if not sys.version_info >= (3, 5):
            self.print_log(
                'Rquired Python version >= 3.5\n' +
                'You can download here: https://www.python.org/downloads/'
            )
            return

        path = [path] if type(path) != list else path
        kindle_roots = self.get_kindle_root(path)

        if len(kindle_roots) < 1:
            self.print_log('No Kindle root directory detected.')
            return

        for kindle_root in kindle_roots:
            self.print_log('Processing Kindle device: %s' % kindle_root)
            documents_path, thumbnails_path = self.get_kindle_path(kindle_root)

            self.print_log('Checking damaged ebook covers:', True)
            thumbnails = self.get_damaged_thumbnails(thumbnails_path)

            if not any(thumbnails):
                self.print_log('- No ebook covers need to fix.')
                return

            self.print_log('Fixing damaged ebook covers:', True)
            self.print_log('Working ...')
            failure_jobs = self.fix_damaged_thumbnails(documents_path, thumbnails)

            if any(len(job) > 0 for job in failure_jobs.values()):
                if len(failure_jobs['cover_errors']) > 0:
                    self.print_log(
                        '- These covers have no corresponding ebook'
                    )
                    for job in failure_jobs['cover_errors']:
                        self.print_log('* %s' % job)


                if len(failure_jobs['ebook_errors']) > 0:
                    self.print_log(
                        '- These covers corresponding ebook has no cover'
                    )
                    for job in failure_jobs['ebook_errors']:
                        self.print_log('! %s' % job)
            else:
                self.print_log('✓ All ebook covers fixed.')

            self.print_log('All jobs done.', True)

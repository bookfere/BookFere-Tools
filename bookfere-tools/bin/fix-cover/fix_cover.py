#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import argparse

from FixCover import FixCover

def main():
    parser = argparse.ArgumentParser(description=FixCover.description,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('path', nargs='?', default=None,
        help='Kindle root directories (optional)')
    parser.add_argument('-a', '--action', dest='action',
        default='fix', choices=['fix', 'clean'],
        help='Specify an action to process ebook cover (default: fix)')
    parser.add_argument('-l', '--log', dest='log', default=False,
        action='store_true', help='Enable log.')

    args = parser.parse_args()

    def get_logger():
        def logger(text):
            log_path = os.path.join(args.path, 'documents/fixcover_log.txt')
            with open(log_path, 'a') as log:
                log.write('%s\n' % text)
        return logger if args.log else None

    fix_cover = FixCover(logger=get_logger())
    fix_cover.handle(args.action, args.path)

if __name__ == '__main__':
    main()


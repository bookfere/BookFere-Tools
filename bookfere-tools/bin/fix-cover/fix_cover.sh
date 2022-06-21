#!/bin/sh

#------------------------
# bookfere.com
#------------------------

. ./bin/config.sh

if [ ! -f "$PYTHON3" ]; then
    print_log 3 'Need to install Python3 (>=3.5) on the Kindle.'
    exit 0
fi

print_log 3 'Working...'

if [ "$1" = '-c' ]; then
    $PYTHON3 $FIX_SCRIPT $KINDLE_PATH -a clean
    if [ $? = 0 ]; then
        print_log 4 'All orphan ebook cover was deleted.'
    fi
else
    $PYTHON3 $FIX_SCRIPT $KINDLE_PATH
    if [ $? = 0 ]; then
        print_log 4 'All damaged ebook cover was fixed.'
    fi
fi

if [ $? != 0 ]; then
    print_log 4 'Unexpected error occurs.'
fi
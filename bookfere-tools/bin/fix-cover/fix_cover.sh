#!/bin/sh

#------------------------
# bookfere.com
#------------------------

. ./bin/config.sh

eips 1 2 'Working...'

if [ -f $PYTHON3 ]; then
    $PYTHON $FIX_SCRIPT
else
    eips 1 2 'Need to install Python3 (>=3.5) on the Kindle.'
fi

if [ $? = 0 ]; then
    eips 1 2 'All damaged ebook cover was fixed.'
else
    eips 1 2 'Unexpected error occurs.'
fi
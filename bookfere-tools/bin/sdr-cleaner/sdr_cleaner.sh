#!/bin/sh

#------------------------
# bookfere.com
#------------------------

. ./bin/config.sh

eips 1 2 'Working...'

if [ -f $PYTHON2 ]; then
    $PYTHON2 $SDR_SCRIPT
elif [ -f $PYTHON3 ]; then
    $PYTHON3 $SDR_SCRIPT
else
    eips 1 2 'Need to install a Python on the Kindle.'
    exit 0
fi

if [ $? = 0 ]; then
    eips 1 2 'All unused SDR folders was cleared.'
else
    eips 1 2 'Unexpected error occurs.'
fi

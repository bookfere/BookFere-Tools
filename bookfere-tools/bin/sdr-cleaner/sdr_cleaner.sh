#!/bin/sh

#------------------------
# bookfere.com
#------------------------

. ./bin/config.sh

print_log 3 'Working...'

if [ -f "$PYTHON2" ]; then
    $PYTHON2 $SDR_SCRIPT
elif [ -f "$PYTHON3" ]; then
    $PYTHON3 $SDR_SCRIPT
else
    print_log 4 'Need to install a Python on the Kindle.'
    exit 0
fi

if [ $? = 0 ]; then
    print_log 4 'All unused SDR folders was cleared.'
else
    print_log 4 'Unexpected error occurs.'
fi

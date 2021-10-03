#!/bin/sh

#------------------------
# bookfere.com
#------------------------

. ./bin/config.sh

PYTHON=/usr/bin/python
PYTHON3=/usr/bin/python3

# Check if python installed.
if [ -f $PYTHON3 ]; then
    $PYTHON3 $SDR_SCRIPT $KINDLE_PATH
elif [ -f $PYTHON ]; then
    $PYTHON2 $SDR_SCRIPT $KINDLE_PATH
else
    $MSG_VIEWER 'Need install python to Kindle.' string
    exit 0
fi

if [ $? = 0 ]; then
    $MSG_VIEWER 'SDR folder clear completed.' string
else
    $MSG_VIEWER 'Unexpected error.' string
fi

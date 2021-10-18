#!/bin/sh

#------------------------
# bookfere.com
#------------------------

. ./bin/config.sh

SUCCESS=0
PATH1=/usr/bin/python3
PATH2=/mnt/us/python3/bin/python3.8
PATH3=/mnt/us/python3/bin/python3.9
PATH4=/usr/bin/python
PATH5=/mnt/us/python2/bin/python2.7

for PYTHON in $PATH1 $PATH2 $PATH3 $PATH4 $PATH5; do
    if [ -f $PYTHON ]; then
        $PYTHON $SDR_SCRIPT
        SUCCESS=1
        break
    fi
done

if [ $? = 0 ]; then
    $MSG_VIEWER 'All unused SDR folders are cleared.' string
elif [ $SUCCESS = 0 ]; then
    $MSG_VIEWER 'Need to install python on Kindle.' string
else
    $MSG_VIEWER 'Unexpected error occurs.' string
fi

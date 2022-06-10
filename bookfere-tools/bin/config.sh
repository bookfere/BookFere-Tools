#!/bin/sh

#------------------------
# bookfere.com
#------------------------

KINDLE_PATH=/mnt/us

SDR_SCRIPT=./bin/sdr-cleaner/sdr_cleaner.py
FIX_SCRIPT=./bin/fix-cover/fix_cover.py

get_python() {
    for PYTHON_PATH in $1; do
        if [ -f $PYTHON ]; then
            echo $PYTHON_PATH
            break
        fi
    done
    echo ''
}

PYTHON2=$(get_python '/usr/bin/python /mnt/us/python2/bin/python2.7')
PYTHON3=$(get_python '/usr/bin/python3 /mnt/us/python3/bin/python3.8 /mnt/us/python3/bin/python3.9')
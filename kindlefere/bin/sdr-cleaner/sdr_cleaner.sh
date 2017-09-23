#!/bin/sh

#------------------------
# kindlefere.com
#------------------------

KINDLE_PATH=/chroot/mnt/us
if [[ $PATH != *"/mnt/us/python/bin"* ]]
    then
        export PATH=$PATH:/mnt/us/python/bin
fi
alias python="python2.7"

# sdr_cleaner
cd ${KINDLE_PATH}/extensions/kindlefere/bin/sdr-cleaner
python sdr_cleaner.py ${KINDLE_PATH}

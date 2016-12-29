#!/bin/sh

#------------------------
# kindlefere.com
#------------------------

KINDLE_PATH=/chroot/mnt/us

# Enable generate log file
cd ${KINDLE_PATH}/extensions/kindlefere/bin/sdr-cleaner
sed -i "s/^cleanlog  = .*/cleanlog  = True/g" ./sdr_cleaner.py
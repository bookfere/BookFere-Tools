#!/bin/sh

#------------------------
# kindlefere.com
#------------------------

KINDLE_PATH=/chroot/mnt/us

# Disable generate log file
cd ${KINDLE_PATH}/extensions/kindlefere/bin/sdr-cleaner
sed -i "s/^cleanlog  = .*/cleanlog  = False/g" ./sdr_cleaner.py
#!/bin/sh

#------------------------
# kindlefere.com
#------------------------

KINDLE_PATH=/chroot/mnt/us

# Disable screenshot file
cd ${KINDLE_PATH}/extensions/kindlefere/bin/sdr-cleaner
sed -i "s/^cleanshot = .*/cleanshot = True/g" ./sdr_cleaner.py
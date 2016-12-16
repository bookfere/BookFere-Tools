#!/bin/sh

#------------------------
# kindlefere.com
#------------------------

# Update KindleFere Tools
cd /chroot/mnt/us/extensions/
wget http://soft.kindlefere.com/kindlefere.zip
if [ -f "kindlefere.zip" ] ; then
    rm -rf kindlefere
    unzip kindlefere.zip
    rm kindlefere.zip
fi
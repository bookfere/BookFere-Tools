#!/bin/sh

#------------------------
# kindlefere.com
#------------------------

# Update KindleFere Tools



cd /chroot/mnt/us/extensions/

if [ -f "KIDNLEFERE_VERSION" ]; then
    rm KIDNLEFERE_VERSION
fi
wget http://soft.kindlefere.com/kindlefere/VERSION -O KIDNLEFERE_VERSION
server=$(sed -n "s/^KindleFere Tools - v\(.*\)/\1/p" ./KIDNLEFERE_VERSION)
current=$(sed -n "s/^KindleFere Tools - v\(.*\)/\1/p" ./kindlefere/VERSION)
if [ ! $server = $current ]; then
    wget http://soft.kindlefere.com/kindlefere/kindlefere.zip
    if [ -f "kindlefere.zip" ]; then
        rm -rf kindlefere
        unzip kindlefere.zip
        rm kindlefere.zip
    fi
fi
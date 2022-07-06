#!/bin/sh

#------------------------
# bookfere.com
#------------------------

. ./bin/config.sh

# Disable screenshot file
sed -i "s/^cleanshot = .*/cleanshot = False/g" $SDR_SCRIPT

#!/bin/sh

#------------------------
# bookfere.com
#------------------------

. ./bin/config.sh

# Disable screenshot file
/bin/sed -i "s/^cleanshot = .*/cleanshot = True/g" $SDR_SCRIPT
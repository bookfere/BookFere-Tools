#!/bin/sh

#------------------------
# bookfere.com
#------------------------

. ./bin/config.sh

# Disable generate log file
sed -i "s/^cleanlog  = .*/cleanlog  = False/g" $SDR_SCRIPT

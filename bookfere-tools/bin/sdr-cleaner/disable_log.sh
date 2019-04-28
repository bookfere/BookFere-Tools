#!/bin/sh

#------------------------
# bookfere.com
#------------------------

. ./bin/config.sh

# Disable generate log file
sed -i "s/^cleanlog  = .*/cleanlog  = False/g" ./bin/sdr-cleaner/sdr_cleaner.py
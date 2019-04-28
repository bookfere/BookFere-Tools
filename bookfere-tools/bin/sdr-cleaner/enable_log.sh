#!/bin/sh

#------------------------
# bookfere.com
#------------------------

. ./bin/config.sh

# Enable generate log file
sed -i "s/^cleanlog  = .*/cleanlog  = True/g" ./bin/sdr-cleaner/sdr_cleaner.py
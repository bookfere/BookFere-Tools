#!/bin/sh

#------------------------
# bookfere.com
#------------------------

. ./bin/config.sh

# Run sdr_cleaner
if [ ! -f /usr/bin/python ]; then
    /usr/bin/WebReaderViewer 'Need install python to Kindle.' string
else
    /usr/bin/python ./bin/sdr-cleaner/sdr_cleaner.py ${KINDLE_PATH}
    /usr/bin/WebReaderViewer 'SDR folder clear completed.' string
fi
#!/bin/sh

#------------------------
# bookfere.com
#------------------------

. ./bin/change-margins/config.sh

# Unzip config file to Kindle root path
if [ -f ${SYSTEM_CONFIG_PATH} ]; then
    /bin/mkdir -p ${TEMP_CONFIG_PATH}
    /usr/bin/unzip -o ${SYSTEM_CONFIG_PATH} -d ${TEMP_CONFIG_PATH}
    /usr/bin/WebReaderViewer 'Margin config file was extracted to temp path.' string
else
    /usr/bin/WebReaderViewer "There is no margin config file named as ${CONFIG_FILE}." string
fi
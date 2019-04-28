#!/bin/sh

#------------------------
# bookfere.com
#------------------------

. ./bin/config.sh

# Language of config file
LANGUAGE=./bin/change-margins/LANGUAGE
if [ -f $LANGUAGE ]; then
    # Use set language
    CONFIG_LANG=$(cat $LANGUAGE)
else
    # Use default language if not set
    LOCAL_LANG=/var/local/system/locale
    CONFIG_LANG=$(/bin/cat ${LOCAL_LANG} | /bin/grep LANG | /bin/sed -r 's/LANG=([a-z]+).*/\1/')
    if [ $LANG = 'en' ]; then
        CONFIG_LANG=$LANG'_GB'
    fi
fi

# Config file path
CONFIG_FILE=ReaderSDK-impl-${CONFIG_LANG}.jar
SYSTEM_CONFIG_PATH=/opt/amazon/ebook/lib/${CONFIG_FILE}
BACKUP_CONFIG_PATH=/opt/amazon/ebook/lib/${CONFIG_FILE}_default
TEMP_CONFIG_PATH=${KINDLE_PATH}/margins-config-temp-${CONFIG_LANG}
COPY_CONFIG_PATH=${TEMP_CONFIG_PATH}/${CONFIG_FILE}

# Test path
# echo $CONFIG_LANG
# echo $KINDLE_PATH
# echo $CONFIG_PATH
# echo $EXTENSION_PATH
# echo $CONFIG_FILE
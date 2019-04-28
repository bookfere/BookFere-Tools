#!/bin/sh

#------------------------
# bookfere.com
#------------------------

. ./bin/change-margins/config.sh

# Rename .zip to .jar
if [ -f ${TEMP_CONFIG_PATH}/a.zip ]; then
    mv ${TEMP_CONFIG_PATH}/a.zip ${COPY_CONFIG_PATH}
fi

# Repalece modified config file if exist
if [ -f ${COPY_CONFIG_PATH} ]; then
    /usr/sbin/mntroot rw
    # Backup default config file if not exist
    if [ ! -f ${BACKUP_CONFIG_PATH} ]; then
        /bin/mv ${SYSTEM_CONFIG_PATH} ${BACKUP_CONFIG_PATH}
    fi
    # Copy config file to system (Overwrite) and reboot
    /bin/cp -f ${COPY_CONFIG_PATH} ${SYSTEM_CONFIG_PATH}
    /usr/sbin/mntroot ro
    /sbin/reboot
else
    /usr/bin/WebReaderViewer 'There is no margin config file in temp path.' string
fi
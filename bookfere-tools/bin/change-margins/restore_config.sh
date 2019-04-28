#!/bin/sh

#------------------------
# bookfere.com
#------------------------

. ./bin/change-margins/config.sh

# Restore the default config file to system
if [ -f ${BACKUP_CONFIG_PATH} ]; then
    /usr/sbin/mntroot rw
    # Delete modified config file
    if [ -f ${SYSTEM_CONFIG_PATH} ]; then
        /bin/rm ${SYSTEM_CONFIG_PATH}.jar
    fi
    # Restore default config file
    /bin/mv ${BACKUP_CONFIG_PATH} ${SYSTEM_CONFIG_PATH}
    /usr/sbin/mntroot ro
    /sbin/reboot
else
    /usr/bin/WebReaderViewer 'There is no backup margin config file needs to be restored.' string
fi
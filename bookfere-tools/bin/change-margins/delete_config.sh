#!/bin/sh

#------------------------
# bookfere.com
#------------------------

. ./bin/change-margins/config.sh

# Delete config path
COUNT=$(/usr/bin/find ${KINDLE_PATH} -maxdepth 1 -type d | grep -e 'margins-config-temp-.*' | wc -l)
if [ $COUNT -gt 0 ]; then
    /bin/rm -rf echo $(echo ${TEMP_CONFIG_PATH} | sed -r 's/(.*-).*$/\1\*/')
    /usr/bin/WebReaderViewer "$COUNT margin config files was deleted." string
else
    /usr/bin/WebReaderViewer "No margin config file needs to be deleted." string
fi
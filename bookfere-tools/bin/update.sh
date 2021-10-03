#!/bin/sh

#------------------------
# bookfere.com
#------------------------

. ./bin/config.sh

# Update BookFere Tools
URL=http://soft.bookfere.com/bookfere-tools
EXTENSION_PATH=bookfere-tools
EXTENSION_FILE=${EXTENSION_PATH}.zip
REMOTE_VERSION_FILE=BOOKFERE_VERSION
LOCAL_VERSION_FILE=VERSION

cd ${KINDLE_PATH}/extensions/
# Download remote version infomation
/usr/bin/wget ${URL}/VERSION -O ${REMOTE_VERSION_FILE}
sleep 10
if [ -f ${REMOTE_VERSION_FILE} ]; then
    # Parse version
    REMOTE_VERSION=$(/bin/sed -n "s/^BookFere Tools - v\(.*\)/\1/p" ./${REMOTE_VERSION_FILE})
    LOCAL_VERSION=$(/bin/sed -n "s/^BookFere Tools - v\(.*\)/\1/p" ./${EXTENSION_PATH}/${LOCAL_VERSION_FILE})
    # Update extension if server version not equal local version
    if [ ${REMOTE_VERSION} != ${LOCAL_VERSION} ]; then
        /usr/bin/wget ${URL}/${EXTENSION_FILE}
        if [ -f ${EXTENSION_FILE} ]; then
            /bin/rm -rf ${EXTENSION_PATH}
            /usr/bin/unzip ${EXTENSION_FILE}
            /bin/rm -f ${EXTENSION_FILE}
        fi
        $MSG_VIEWER 'Updated latest version.' string
    else
        $MSG_VIEWER 'No Update available.' string
    fi
else
    $MSG_VIEWER 'Update server error.' string
fi
/bin/rm -f ${REMOTE_VERSION_FILE}
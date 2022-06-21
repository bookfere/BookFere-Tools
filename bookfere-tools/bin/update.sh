#!/bin/sh

#------------------------
# bookfere.com
#------------------------

. ./bin/config.sh

EXTENSION_PATH=${KINDLE_PATH}/extensions
PLUGIN_PATH=${EXTENSION_PATH}/bookfere-tools
REMOTE_URL=http://soft.bookfere.com/bookfere-tools
REMOTE_VERSION=BOOKFERE_VERSION
REMOTE_PACKAGE=bookfere-tools.zip

print_log 3 'Working...'

DOWNLOADED_VERSION=${EXTENSION_PATH}/${REMOTE_VERSION}
/usr/bin/wget -O $DOWNLOADED_VERSION ${REMOTE_URL}/VERSION

get_version() {
    echo $(/bin/sed -n "s/^BookFere Tools - v\(.*\)/\1/p" $1)
}

if [ -f "$DOWNLOADED_VERSION" ]; then
    REMOTE_VERSION=$(get_version $DOWNLOADED_VERSION)
    LOCAL_VERSION=$(get_version $PLUGIN_PATH/VERSION)
    /bin/rm -f $DOWNLOADED_VERSION

    if [ "$REMOTE_VERSION" != "$LOCAL_VERSION" ]; then
        DOWNLOADED_PACKAGE=${EXTENSION_PATH}/${REMOTE_PACKAGE}
        /usr/bin/wget -O $DOWNLOADED_PACKAGE ${REMOTE_URL}/${REMOTE_PACKAGE}
        if [ -f "$DOWNLOADED_PACKAGE" ]; then
            /bin/rm -rf $PLUGIN_PATH
            /usr/bin/unzip -oq $DOWNLOADED_PACKAGE -d $EXTENSION_PATH
            /bin/rm -f $DOWNLOADED_PACKAGE
            print_log 4 "$LOCAL_VERSION -> $REMOTE_VERSION"
            print_log 5 'Updated latest version.'
        else
            print_log 4 'Update failed.'
        fi
    else
        print_log 4 'No Update available.'
    fi
else
    print_log 4 'Update server error.'
fi
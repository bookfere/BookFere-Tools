#!/bin/bash

# Copyright (c)2022 https://bookfere.com
# This is a batch script for fixing Google Translate and making it available
# in the Chinese mainland. If you experience any problem, visit the page below:
# https://bookfere.com/post/553.html

. ./bin/config.sh

SOURCE_DOMAIN=google.cn
TARGET_DOMAIN=translate.googleapis.com
HOSTS_FILE=/etc/hosts
COMMENT="# Fix Google Translate CN"

HOST_CMD=/usr/bin/nslookup
AWK_CMD=/usr/bin/awk
SED_CMD=/bin/sed

IP="$(echo "$($HOST_CMD google.cn)" | $AWK_CMD 'NR==5, FS=": " {print $2}')"
OLD_RULE=$(cat $HOSTS_FILE | grep $TARGET_DOMAIN)
NEW_RULE="$IP $TARGET_DOMAIN"

if [ "$1" == "-d" ]; then
    if [ -n "$OLD_RULE" ]; then
        print_log 3 "Deleting the rule \"$OLD_RULE\""
        PATTERN=':a;N;$!ba;s/\n\{0,\}'${COMMENT}'\n.*'${TARGET_DOMAIN}'//'
        $SED_CMD -i "$PATTERN" $HOSTS_FILE
    else
        print_log 3 "No rule exists, nothing to do."
    fi
    print_log 4 "Done."
    exit 0
fi

if [ -n "$OLD_RULE" ]; then
    if [ "$OLD_RULE" != "$NEW_RULE" ]; then
        print_log 3 "Deleting the rule \"$OLD_RULE\""
        print_log 4 "Adding the rule \"$NEW_RULE\""
        $SED_CMD -i "s/.*${TARGET_DOMAIN}/${NEW_RULE}/" $HOSTS_FILE
    else
        print_log 3 'The rule already exists, nothing to do.'
    fi
else
    print_log 3 "Adding the rule \"$NEW_RULE\""
    echo -ne "\n$COMMENT\n$NEW_RULE" >> $HOSTS_FILE
fi

print_log 4 'Done.'

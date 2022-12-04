#!/bin/bash

# Copyright (c)2022 https://bookfere.com
# This is a batch script for fixing Google Translate and making it available
# in the Chinese mainland. If you experience any problem, visit the page below:
# https://bookfere.com/post/553.html

. ./bin/config.sh

IPS='74.125.137.90
74.125.193.186
74.125.196.113
108.177.97.100
108.177.111.90
108.177.122.90
108.177.125.186
108.177.126.90
108.177.127.90
142.250.0.90
142.250.1.90
142.250.4.90
142.250.8.90
142.250.9.90
142.250.10.90
142.250.11.90
142.250.12.90
142.250.13.90
142.250.27.90
142.250.28.90
142.250.30.90
142.250.31.90
142.250.96.90
142.250.97.90
142.250.98.90
142.250.99.90
142.250.100.90
142.250.101.90
142.250.102.90
142.250.103.90
142.250.105.90
142.250.107.90
142.250.111.90
142.250.112.90
142.250.113.90
142.250.114.90
142.250.115.90
142.250.123.90
142.250.125.90
142.250.126.90
142.250.128.90
142.250.138.90
142.250.141.90
142.250.142.90
142.250.145.90
142.250.152.90
142.250.153.90
142.250.157.90
142.250.157.183
142.250.157.184
142.250.157.186
142.250.158.90
142.250.159.90
142.251.1.90
142.251.2.90
142.251.4.90
142.251.5.90
142.251.6.90
142.251.8.90
142.251.9.90
142.251.10.90
142.251.12.90
142.251.15.90
142.251.16.90
142.251.18.90
142.251.107.90
142.251.111.90
142.251.112.90
142.251.116.90
142.251.117.90
142.251.120.90
142.251.160.90
142.251.161.90
142.251.162.90
142.251.163.90
142.251.166.90
172.217.192.90
172.217.195.90
172.217.203.90
172.217.204.90
172.217.214.90
172.217.215.90
172.253.58.90
172.253.62.90
172.253.63.90
172.253.112.90
172.253.113.90
172.253.114.90
172.253.115.90
172.253.116.90
172.253.117.90
172.253.118.90
172.253.119.90
172.253.123.90
172.253.124.90
172.253.125.90
172.253.126.90
172.253.127.90
216.58.227.65
216.58.227.66
216.58.227.67'

API='https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=fr&dt=t&dj=1&q=hello'
TARGET_DOMAIN=translate.googleapis.com
HOSTS_FILE=/etc/hosts
COMMENT="# Fix Google Translate CN"

SED_CMD=/bin/sed
GREP_CMD=/bin/grep
CURL_CMD=/usr/bin/curl

for i in $IPS; do
    TRANS=$($CURL_CMD -sk $API --resolve $TARGET_DOMAIN:443:$i \
    | $GREP_CMD '"trans":"bonjour"')
    if [ -n "$TRANS" ]; then IP=$i; break; fi
done

if [ ! -n "$IP" ]; then
    print_log 3 "No IP available!"
    exit 0
fi

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

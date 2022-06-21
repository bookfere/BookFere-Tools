#!/bin/sh

. ./bin/config.sh

get_size() {
    echo $(df -k 2>/dev/null | awk '{ if($6=="/chroot/mnt/us") print $4 }')
}

PLACEHOLDER="${KINDLE_PATH}/disable_update_placeholder"

if [ "$1" = '-d' ]; then
    rm -f "$PLACEHOLDER"* &&
    print_log 3 "Placeholder file was deleted."
    print_log 3 "Total available space: $(get_size)."
    exit
fi

AVAILABLE=$(get_size)
FILLING=$(($AVAILABLE - 150000))

if [ $FILLING -gt 0 ]; then
    print_log 3 "Total: ${AVAILABLE}KB, Fill: ${FILLING}KB, Left: 150000KB"
    print_log 4 'Writing placeholder file, please wait ...'
    dd if=/dev/zero count=$FILLING bs=1024 2>/dev/null |
    split -b 3500000k -a 1 - $PLACEHOLDER. &&
    print_log 5 'Placeholder file was created.'
else
    print_log 3 "Total: ${AVAILABLE}KB, No need to fill out placeholder file."
fi
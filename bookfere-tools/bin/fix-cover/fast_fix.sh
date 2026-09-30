#!/bin/sh
# fast_fix.sh -- incremental cover fixer (fastfix.py) as a KUAL action
#
#   ./bin/fix-cover/fast_fix.sh --status   report only, changes nothing
#   ./bin/fix-cover/fast_fix.sh --fix      incremental repair (default)
#   ./bin/fix-cover/fast_fix.sh --rebuild  ignore the index, re-extract everything
#
# LF line endings only. ASCII only.

. ./bin/config.sh

FAST_SCRIPT=./bin/fix-cover/fastfix.py
FAST_LOG=./bin/fix-cover/fastfix-last.log

if [ ! -f "$FAST_SCRIPT" ]; then
    print_log 3 'fastfix.py is missing.'
    exit 0
fi
if [ ! -f "$PYTHON3" ]; then
    print_log 3 'Need Python3 (>=3.5) on the Kindle.'
    exit 0
fi

case "$1" in
    --status)  ARG=--status ;;
    --rebuild) ARG=--rebuild ;;
    *)         ARG=--fix ;;
esac

print_log 3 "Working ($ARG) ..."

OUT=$($PYTHON3 $FAST_SCRIPT $KINDLE_PATH $ARG 2>&1)
RC=$?
printf '%s\n' "$OUT" > $FAST_LOG

NEED=$(printf '%s\n' "$OUT" | sed -n 's/^\[i\] need fix *: \([0-9]*\).*/\1/p' | head -n 1)
DONE=$(printf '%s\n' "$OUT" | sed -n 's/^\[i\] fixed\/generated *: \([0-9]*\) \/ \([0-9]*\).*/\1+\2/p' | head -n 1)
READ=$(printf '%s\n' "$OUT" | sed -n 's/^\[i\] BOOK BYTES READ *: \([0-9]*\).*/\1/p' | head -n 1)

eips 2 3 "need fix: ${NEED:-?}   done: ${DONE:-?}"
eips 2 4 "book bytes read: ${READ:-?}"
if [ "$RC" = "0" ]; then
    eips 2 5 "OK  (log: bin/fix-cover/fastfix-last.log)"
else
    eips 2 5 "FAILED rc=$RC  (see fastfix-last.log)"
fi

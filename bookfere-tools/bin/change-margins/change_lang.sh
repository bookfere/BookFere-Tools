#!/bin/sh

#------------------------
# bookfere.com
#------------------------

# ReaderSDK-impl-de (Germany) 
# ReaderSDK-impl-en_GB (English)
# ReaderSDK-impl-es (Spain)
# ReaderSDK-impl-fr (France)
# ReaderSDK-impl-it (Italy)
# ReaderSDK-impl-ja (Japan)
# ReaderSDK-impl-nl (Netherlands)
# ReaderSDK-impl-pt (Portugal)
# ReaderSDK-impl-ru (Russian Federation)
# ReaderSDK-impl-sq (Albanian)
# ReaderSDK-impl-zh (Chinese)

. ./bin/config.sh

LANGUAGE=./bin/change-margins/LANGUAGE
if [ ! $1 ]; then
    /bin/rm ${LANGUAGE}
else
    /bin/echo $1 > ${LANGUAGE}
fi
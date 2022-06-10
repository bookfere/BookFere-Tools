#!/bin/sh

#------------------------
# bookfere.com
#------------------------

. ./bin/config.sh

# Show Current Version
CURRENT_VERSION=$(/bin/cat ./VERSION)
eips 1 2 "${CURRENT_VERSION}"
#!/bin/sh

#------------------------
# bookfere.com
#------------------------

. ./bin/config.sh

# Show Current Version
CURRENT_VERSION=$(/bin/cat ./VERSION)
print_log 3 "${CURRENT_VERSION}"
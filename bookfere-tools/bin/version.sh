#!/bin/sh

#------------------------
# bookfere.com
#------------------------

. ./bin/config.sh

# Show Current Version
CURRENT_VERSION=$(/bin/cat ./VERSION)
$MSG_VIEWER "Current version is ${CURRENT_VERSION}." string
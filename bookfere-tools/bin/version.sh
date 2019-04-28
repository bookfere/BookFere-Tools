#!/bin/sh

#------------------------
# bookfere.com
#------------------------

# Show Current Version
CURRENT_VERSION=$(/bin/cat ./VERSION)
/usr/bin/WebReaderViewer "Current version is ${CURRENT_VERSION}." string
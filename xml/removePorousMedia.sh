#!/usr/bin/env bash

set -x

# delete fluid
xmlstarlet ed --delete "//OpenGeoSysProject/processes/process/porous_medium" $1 > /tmp/removedPorousMedia.prj
# format the result file
xmlstarlet fo -s 4 /tmp/removedPorousMedia.prj > ${1}

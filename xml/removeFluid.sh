#!/usr/bin/env bash

set -x

# delete fluid
xmlstarlet ed --delete "//OpenGeoSysProject/processes/process/fluid" $1 > /tmp/removedFluid.prj
# format the result file
xmlstarlet fo -s 4 /tmp/removedFluid.prj > ${1}

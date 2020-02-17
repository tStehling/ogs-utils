#!/usr/bin/env bash

set -x

# delete fluid
xmlstarlet ed --delete "//OpenGeoSysProject/processes/process/material_property" $1 > /tmp/removedMaterialProperty.prj
# format the result file
xmlstarlet fo -s 4 /tmp/removedMaterialProperty.prj > ${1}

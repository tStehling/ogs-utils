#!/usr/bin/env bash

#set -x

zero=0.0
pzero=.0
szero=0

number_of_medium_tags=`xmlstarlet sel -t -v "count(///*/medium)" $1`
number_of_medium_tags=$(($number_of_medium_tags - 1))

storage_value=`xmlstarlet sel -t -m "//*/media/medium/phases/phase/properties/property[name='storage']" -v "./value" $1`

solid_density_type=`xmlstarlet sel -t -m "//*/media/medium/phases/phase[type='Solid']/properties/property[name='density']" -v "./type" $1`
solid_density_value=`xmlstarlet sel -t -m "//*/media/medium/phases/phase[type='Solid']/properties/property[name='density']" -v "./value" $1`
if [ "$storage_value" == "$zero" ] || [ "$storage_value" == "$pzero" ] || [ "$storage_value" == "$szero" ]; then
    if [ "$solid_density_type" == "Constant" ] && [ "$solid_density_value" == "$zero" ] || [ "$solid_density_value" == "$pzero" ] || [ "$solid_density_value" == "$szero" ]; then
        xmlstarlet ed --delete "//media/medium/phases/phase[type='Solid']/properties/property[name='storage']" $1 > /tmp/removedStorage.prj
        echo "$1: removing storage"
    fi
fi

# format the result file
xmlstarlet fo -s 4 /tmp/removedStorage.prj > ${1}

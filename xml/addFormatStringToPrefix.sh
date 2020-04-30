#!/usr/bin/env bash

sub_path=//OpenGeoSysProject/time_loop/output/prefix
prefix_value=`xmlstarlet sel -t -v $sub_path $1`
prefix_format_string=${prefix_value}_pcs_{:process}_ts_{:timestep}_t_{:time}

xmlstarlet ed -u $sub_path -v $prefix_format_string $1 > /tmp/prefix.prj

#format the result file
xmlstarlet fo -s 4 /tmp/prefix.prj > ${1}

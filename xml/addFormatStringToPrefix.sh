#!/usr/bin/env bash

base_path=//OpenGeoSysProject/time_loop/output
sub_path=${base_path}/prefix
prefix_value=`xmlstarlet sel -t -v $sub_path $1`
prefix_format_string=${prefix_value}_pcs_{:process_id}
suffix_format_string=_ts_{:timestep}_t_{:time}

xmlstarlet ed -u $sub_path -v $prefix_format_string $1 > /tmp/prefix.prj
xmlstarlet ed -s ${base_path} --type elem -n suffix -v $suffix_format_string /tmp/prefix.prj > /tmp/suffix.prj

#format the result file
xmlstarlet fo -s 4 /tmp/suffix.prj > ${1}

#!/usr/bin/env bash

#set -x

number_of_medium_tags=`xmlstarlet sel -t -v "count(///*/medium)" $1`
number_of_medium_tags=$(($number_of_medium_tags - 1))

path="//OpenGeoSysProject/media/medium[@id="0"]"
xmlstarlet ed --move "$path/properties/property[name='porosity']" "$path/phases/phase[type='Solid']/properties" $1 > /tmp/t0.prj

for i in `seq 1 ${number_of_medium_tags}`;
do
    i_m_e=$(($i-1))
    path="//OpenGeoSysProject/media/medium[@id="${i}"]"
    xmlstarlet ed --move "$path/properties/property[name='porosity']" "$path/phases/phase[type='Solid']/properties" /tmp/t$i_m_e.prj > /tmp/t${i}.prj
done

#format the result file
xmlstarlet fo -s 4 /tmp/t${number_of_medium_tags}.prj > ${1}

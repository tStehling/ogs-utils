#!/usr/bin/env bash

set -x

### add reference_temperature property
sub_path=//OpenGeoSysProject/media/medium/properties
xmlstarlet ed --subnode $sub_path --type elem -n "property_reference_temperature" $1 > /tmp/t_property.prj
# add property name
xmlstarlet ed --subnode $sub_path/property_reference_temperature --type elem -n name -v reference_temperature /tmp/t_property.prj > /tmp/t_name.prj
# add property type
xmlstarlet ed --subnode $sub_path/property_reference_temperature --type elem -n type -v Constant /tmp/t_name.prj > /tmp/t_type.prj
# add property value
xmlstarlet ed --subnode $sub_path/property_reference_temperature --type elem -n value -v 293.15 /tmp/t_type.prj > /tmp/t_entry.prj
# rename property_storage to property
xmlstarlet ed --rename "//OpenGeoSysProject/media/medium/properties/property_reference_temperature" -v "property" /tmp/t_entry.prj > /tmp/with_reference_temperature.prj

#format the result file
xmlstarlet fo -s 4 /tmp/with_reference_temperature.prj > ${1}

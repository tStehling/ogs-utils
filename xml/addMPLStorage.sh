#!/usr/bin/env bash

set -x

storage_value=`xmlstarlet sel -t -v "//OpenGeoSysProject/processes/process/porous_medium/porous_medium/storage/value" $1`
storage_type=`xmlstarlet sel -t -v "//OpenGeoSysProject/processes/process/porous_medium/porous_medium/storage/type" $1`

### rename the solid phase for unique insertion
xmlstarlet ed -r "//*/phase/type[text()='Solid']/.." -v solid_phase $1 > /tmp/solid_phase_properties.prj

### add storage property
sub_path=//OpenGeoSysProject/media/medium/phases/solid_phase/properties
xmlstarlet ed --subnode $sub_path --type elem -n "property_storage" /tmp/solid_phase_properties.prj > /tmp/solid_phase_properties_property_storage.prj
# add property name
xmlstarlet ed --subnode $sub_path/property_storage --type elem -n name -v storage /tmp/solid_phase_properties_property_storage.prj > /tmp/solid_phase_properties_property_storage_name.prj
# add property type
xmlstarlet ed --subnode $sub_path/property_storage --type elem -n type -v $storage_type /tmp/solid_phase_properties_property_storage_name.prj > /tmp/solid_phase_properties_property_storage_type.prj
# add property value
xmlstarlet ed --subnode $sub_path/property_storage --type elem -n value -v "$storage_value" /tmp/solid_phase_properties_property_storage_type.prj > /tmp/solid_phase_properties_property_storage_entries.prj
# rename property_storage to property
xmlstarlet ed --rename "//OpenGeoSysProject/media/medium/phases/solid_phase/properties/property_storage" -v "property" /tmp/solid_phase_properties_property_storage_entries.prj > /tmp/with_storage.prj

### rename solid_phase tag to phase
xmlstarlet ed --rename "//OpenGeoSysProject/media/medium/phases/solid_phase" -v "phase" /tmp/with_storage.prj > /tmp/with_solid_phase.prj

#format the result file
xmlstarlet fo -s 4 /tmp/with_solid_phase.prj > ${1}

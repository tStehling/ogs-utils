#!/usr/bin/env bash

set -x

porosity_parameter_name=`xmlstarlet sel -t -m "//*/porosity" -v "./porosity_parameter" $1`
echo $porosity_parameter_name

porosity_type=`xmlstarlet sel -t -m "//*/parameter[name='$porosity_parameter_name']" -v "./type" $1`
echo $porosity_type
porosity_entries=`xmlstarlet sel -t -m "//*/parameter[name='$porosity_parameter_name']" -v "./value|values" $1`
echo $porosity_entries

### rename the solid phase for unique insertion
xmlstarlet ed -r "//*/phase/type[text()='Solid']/.." -v solid_phase $1 > /tmp/solid_phase_properties.prj

### add porosity property
sub_path=//OpenGeoSysProject/media/medium/phases/solid_phase/properties
xmlstarlet ed --subnode $sub_path --type elem -n "property_porosity" /tmp/solid_phase_properties.prj > /tmp/solid_phase_properties_property_porosity.prj
# add property name
xmlstarlet ed --subnode $sub_path/property_porosity --type elem -n name -v porosity /tmp/solid_phase_properties_property_porosity.prj > /tmp/solid_phase_properties_property_porosity_name.prj
# add property type
xmlstarlet ed --subnode $sub_path/property_porosity --type elem -n type -v $porosity_type /tmp/solid_phase_properties_property_porosity_name.prj > /tmp/solid_phase_properties_property_porosity_type.prj
# add property value
xmlstarlet ed --subnode $sub_path/property_porosity --type elem -n value -v "$porosity_entries" /tmp/solid_phase_properties_property_porosity_type.prj > /tmp/solid_phase_properties_property_porosity_entries.prj
# rename property_porosity to property
xmlstarlet ed --rename "//OpenGeoSysProject/media/medium/phases/solid_phase/properties/property_porosity" -v "property" /tmp/solid_phase_properties_property_porosity_entries.prj > /tmp/with_porosity.prj

### rename solid_phase tag to phase
xmlstarlet ed --rename "//OpenGeoSysProject/media/medium/phases/solid_phase" -v "phase" /tmp/with_porosity.prj > /tmp/with_solid_phase.prj

#format the result file
xmlstarlet fo -s 4 /tmp/with_solid_phase.prj > ${1}

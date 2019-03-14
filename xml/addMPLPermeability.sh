#!/usr/bin/env bash

set -x

permeability_parameter_name=`xmlstarlet sel -t -m "//*/permeability" -v "./permeability_tensor_entries" $1`
echo $permeability_parameter_name

permeability_tensor_type=`xmlstarlet sel -t -m "//*/parameter[name='$permeability_parameter_name']" -v "./type" $1`
echo $permeability_tensor_type
permeability_tensor_entries=`xmlstarlet sel -t -m "//*/parameter[name='$permeability_parameter_name']" -v "./value|values" $1`
echo $permeability_tensor_entries

### add solid phase in phases
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases" --type elem -n "solid_phase" $1 > /tmp/solid_phase.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/solid_phase" --type elem -n "type" -v "Solid" /tmp/solid_phase.prj > /tmp/solid_phase_type.prj
### add properties tag in solid_phase
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/solid_phase" --type elem -n "properties" /tmp/solid_phase_type.prj > /tmp/solid_phase_properties.prj

### add permeability property
sub_path=//OpenGeoSysProject/media/medium/phases/solid_phase/properties
xmlstarlet ed --subnode $sub_path --type elem -n "property_permeability" /tmp/solid_phase_properties.prj > /tmp/solid_phase_properties_property_permeability.prj
# add property name
xmlstarlet ed --subnode $sub_path/property_permeability --type elem -n name -v permeability /tmp/solid_phase_properties_property_permeability.prj > /tmp/solid_phase_properties_property_permeability_name.prj
# add property type
xmlstarlet ed --subnode $sub_path/property_permeability --type elem -n type -v $permeability_tensor_type /tmp/solid_phase_properties_property_permeability_name.prj > /tmp/solid_phase_properties_property_permeability_type.prj
# add property value
xmlstarlet ed --subnode $sub_path/property_permeability --type elem -n value -v "$permeability_tensor_entries" /tmp/solid_phase_properties_property_permeability_type.prj > /tmp/solid_phase_properties_property_permeability_entries.prj
# rename property_permeability to property
xmlstarlet ed --rename "//OpenGeoSysProject/media/medium/phases/solid_phase/properties/property_permeability" -v "property" /tmp/solid_phase_properties_property_permeability_entries.prj > /tmp/with_permeability.prj

### rename solid_phase tag to phase
xmlstarlet ed --rename "//OpenGeoSysProject/media/medium/phases/solid_phase" -v "phase" /tmp/with_permeability.prj > /tmp/with_solid_phase.prj

#format the result file
xmlstarlet fo -s 4 /tmp/with_solid_phase.prj > ${1}

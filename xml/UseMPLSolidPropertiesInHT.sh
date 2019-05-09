#!/usr/bin/env bash

set -x

old_density_path="//OpenGeoSysProject/processes/process/density_solid"
density_parameter_name=`xmlstarlet sel -T -t -v "${old_density_path}" ${1}`
density_parameter_value=`xmlstarlet sel -t -m "//*/parameter[name='${density_parameter_name}']" -v "./value" ${1}`
echo "${density_parameter_name}: ${density_parameter_value}"

old_specific_heat_capacity_solid_path="//OpenGeoSysProject/processes/process/specific_heat_capacity_solid"
specific_heat_capacity_solid_parameter_name=`xmlstarlet sel -T -t -v "${old_specific_heat_capacity_solid_path}" ${1}`
specific_heat_capacity_solid_parameter_value=`xmlstarlet sel -t -m "//*/parameter[name='${specific_heat_capacity_solid_parameter_name}']" -v "./value" ${1}`
echo "${specific_heat_capacity_solid_parameter_name}: ${specific_heat_capacity_solid_parameter_value}"

old_thermal_conductivity_solid_path="//OpenGeoSysProject/processes/process/thermal_conductivity_solid"
thermal_conductivity_solid_parameter_name=`xmlstarlet sel -T -t -v "${old_thermal_conductivity_solid_path}" ${1}`
thermal_conductivity_solid_parameter_value=`xmlstarlet sel -t -m "//*/parameter[name='${thermal_conductivity_solid_parameter_name}' and type='Constant']" -v "./value" ${1}`
echo "${thermal_conductivity_solid_parameter_name}: ${thermal_conductivity_solid_parameter_value}"

# solid density
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase[type='Solid']/properties" --type elem -n "property_density" ${1} > /tmp/2.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase[type='Solid']/properties/property_density" --type elem -n "name" -v "density" /tmp/2.prj > /tmp/3.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase[type='Solid']/properties/property_density" --type elem -n "type" -v "Constant" /tmp/3.prj > /tmp/4.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase[type='Solid']/properties/property_density" --type elem -n "value" -v "${density_parameter_value}" /tmp/4.prj > /tmp/5.prj
xmlstarlet ed --rename "//OpenGeoSysProject/media/medium/phases/phase[type='Solid']/properties/property_density" -v "property" /tmp/5.prj > /tmp/1.prj

# solid thermal_conductivity
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase[type='Solid']/properties" --type elem -n "property_thermal_conductivity" /tmp/1.prj > /tmp/2.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase[type='Solid']/properties/property_thermal_conductivity" --type elem -n "name" -v "thermal_conductivity" /tmp/2.prj > /tmp/3.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase[type='Solid']/properties/property_thermal_conductivity" --type elem -n "type" -v "Constant" /tmp/3.prj > /tmp/4.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase[type='Solid']/properties/property_thermal_conductivity" --type elem -n "value" -v "${thermal_conductivity_solid_parameter_value}" /tmp/4.prj > /tmp/5.prj
xmlstarlet ed --rename "//OpenGeoSysProject/media/medium/phases/phase[type='Solid']/properties/property_thermal_conductivity" -v "property" /tmp/5.prj > /tmp/1.prj

# solid specific_heat_capacity
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase[type='Solid']/properties" --type elem -n "property_specific_heat_capacity" /tmp/1.prj > /tmp/2.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase[type='Solid']/properties/property_specific_heat_capacity" --type elem -n "name" -v "specific_heat_capacity" /tmp/2.prj > /tmp/3.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase[type='Solid']/properties/property_specific_heat_capacity" --type elem -n "type" -v "Constant" /tmp/3.prj > /tmp/4.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase[type='Solid']/properties/property_specific_heat_capacity" --type elem -n "value" -v "${specific_heat_capacity_solid_parameter_value}" /tmp/4.prj > /tmp/5.prj
xmlstarlet ed --rename "//OpenGeoSysProject/media/medium/phases/phase[type='Solid']/properties/property_specific_heat_capacity" -v "property" /tmp/5.prj > /tmp/1.prj


# delete old tags
xmlstarlet ed --delete "${old_density_path}" /tmp/1.prj > /tmp/2.prj
xmlstarlet ed --delete "${old_specific_heat_capacity_solid_path}" /tmp/2.prj > /tmp/3.prj
xmlstarlet ed --delete "${old_thermal_conductivity_solid_path}" /tmp/3.prj > /tmp/1.prj

# delete old parameters
xmlstarlet ed --delete "//OpenGeoSysProject/parameters/parameter[name='${density_parameter_name}']" /tmp/1.prj > /tmp/2.prj
xmlstarlet ed --delete "//OpenGeoSysProject/parameters/parameter[name='${specific_heat_capacity_solid_parameter_name}']" /tmp/2.prj > /tmp/3.prj
xmlstarlet ed --delete "//OpenGeoSysProject/parameters/parameter[name='${thermal_conductivity_solid_parameter_name}']" /tmp/3.prj > /tmp/1.prj

# format the result file
xmlstarlet fo -s 4 /tmp/1.prj > ${1}

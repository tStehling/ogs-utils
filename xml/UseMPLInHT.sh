#!/usr/bin/env bash

set -x

density=`xmlstarlet sel -T -t -v "//OpenGeoSysProject/processes/process/fluid/density/value" ${1}`
echo ${density}
viscosity=`xmlstarlet sel -T -t -v "//OpenGeoSysProject/processes/process/fluid/viscosity/value" ${1}`
echo ${viscosity}
exit
# add media tag before //OpenGeoSysProject/time_loop
xmlstarlet ed --insert "//OpenGeoSysProject/time_loop" --type elem -n "media" ${1} > /tmp/a.prj

# add subnode medium into //OpenGeoSysProject/media
xmlstarlet ed --subnode "//OpenGeoSysProject/media" --type elem -n "medium" /tmp/a.prj > /tmp/b.prj

xmlstarlet ed --insert "//OpenGeoSysProject/media/medium" --type attr -n "id" -v "0" /tmp/b.prj > /tmp/c.prj

# add subnode phases into //OpenGeoSysProject/media/medium
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium" --type elem -n "phases" /tmp/c.prj > /tmp/d.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases" --type elem -n "phase" /tmp/d.prj > /tmp/e.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase" --type elem -n "type" -v "AqueousLiquid" /tmp/e.prj > /tmp/f.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase" --type elem -n "properties" /tmp/f.prj > /tmp/1.prj

# density
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase/properties" --type elem -n "property_density" /tmp/1.prj > /tmp/2.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase/properties/property_density" --type elem -n "name" -v "density" /tmp/2.prj > /tmp/3.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase/properties/property_density" --type elem -n "type" -v "Constant" /tmp/3.prj > /tmp/4.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase/properties/property_density" --type elem -n "value" -v "1000" /tmp/4.prj > /tmp/5.prj
xmlstarlet ed --rename "//OpenGeoSysProject/media/medium/phases/phase/properties/property_density" -v "property" /tmp/5.prj > /tmp/1.prj

# viscosity
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase/properties" --type elem -n "property_viscosity" /tmp/1.prj > /tmp/2.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase/properties/property_viscosity" --type elem -n "name" -v "viscosity" /tmp/2.prj > /tmp/3.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase/properties/property_viscosity" --type elem -n "type" -v "Constant" /tmp/3.prj > /tmp/4.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase/properties/property_viscosity" --type elem -n "value" -v "1e-3" /tmp/4.prj > /tmp/5.prj
xmlstarlet ed --rename "//OpenGeoSysProject/media/medium/phases/phase/properties/property_viscosity" -v "property" /tmp/5.prj > /tmp/1.prj

# thermal_conductivity
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase/properties" --type elem -n "property_thermal_conductivity" /tmp/1.prj > /tmp/2.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase/properties/property_thermal_conductivity" --type elem -n "name" -v "thermal_conductivity" /tmp/2.prj > /tmp/3.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase/properties/property_thermal_conductivity" --type elem -n "type" -v "Constant" /tmp/3.prj > /tmp/4.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/phases/phase/properties/property_thermal_conductivity" --type elem -n "value" -v "0.65" /tmp/4.prj > /tmp/5.prj
xmlstarlet ed --rename "//OpenGeoSysProject/media/medium/phases/phase/properties/property_thermal_conductivity" -v "property" /tmp/5.prj > /tmp/1.prj

# add general medium properties
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium" --type elem -n "properties" /tmp/1.prj > /tmp/A.prj

# add thermal_longitudinal_dispersivity
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/properties" --type elem -n "property_thermal_longitudinal_dispersivity" /tmp/A.prj > /tmp/2.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/properties/property_thermal_longitudinal_dispersivity" --type elem -n "name" -v "thermal_longitudinal_dispersivity" /tmp/2.prj > /tmp/3.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/properties/property_thermal_longitudinal_dispersivity" --type elem -n "type" -v "Constant" /tmp/3.prj > /tmp/4.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/properties/property_thermal_longitudinal_dispersivity" --type elem -n "value" -v "0" /tmp/4.prj > /tmp/5.prj
xmlstarlet ed --rename "//OpenGeoSysProject/media/medium/properties/property_thermal_longitudinal_dispersivity" -v "property" /tmp/5.prj > /tmp/A.prj

# add thermal_transversal_dispersivity
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/properties" --type elem -n "property_thermal_transversal_dispersivity" /tmp/A.prj > /tmp/2.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/properties/property_thermal_transversal_dispersivity" --type elem -n "name" -v "thermal_transversal_dispersivity" /tmp/2.prj > /tmp/3.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/properties/property_thermal_transversal_dispersivity" --type elem -n "type" -v "Constant" /tmp/3.prj > /tmp/4.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/properties/property_thermal_transversal_dispersivity" --type elem -n "value" -v "0" /tmp/4.prj > /tmp/5.prj
xmlstarlet ed --rename "//OpenGeoSysProject/media/medium/properties/property_thermal_transversal_dispersivity" -v "property" /tmp/5.prj > /tmp/A.prj

# add specific_heat_capacity
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/properties" --type elem -n "property_specific_heat_capacity" /tmp/A.prj > /tmp/2.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/properties/property_specific_heat_capacity" --type elem -n "name" -v "specific_heat_capacity" /tmp/2.prj > /tmp/3.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/properties/property_specific_heat_capacity" --type elem -n "type" -v "Constant" /tmp/3.prj > /tmp/4.prj
xmlstarlet ed --subnode "//OpenGeoSysProject/media/medium/properties/property_specific_heat_capacity" --type elem -n "value" -v "0" /tmp/4.prj > /tmp/5.prj
xmlstarlet ed --rename "//OpenGeoSysProject/media/medium/properties/property_specific_heat_capacity" -v "property" /tmp/5.prj > /tmp/A.prj

# delete thermal_conductivity_fluid
xmlstarlet ed --delete "//OpenGeoSysProject/processes/process/thermal_conductivity_fluid" /tmp/A.prj > /tmp/2.prj
xmlstarlet ed --delete "//OpenGeoSysProject/processes/process/thermal_dispersivity" /tmp/2.prj > /tmp/A.prj

# xmlstarlet ed --delete "//OpenGeoSysProject/parameters/parameter/"

# format the result file
xmlstarlet fo -s 4 /tmp/A.prj > ${1}

#!/bin/python

import sys
import subprocess

class ConstantProperty:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.xml_path = "//OpenGeoSysProject/media/medium/phases/phase/properties"

    def writeAsMediumPropertyToFile(self, file_name):
        ex = "xmlstarlet ed "
        path = self.xml_path
        node = "property_density"
        node_cmd = ex + " --subnode \"" + path + "\" --type elem -n \"node\"" + file_name + " > /tmp/2.prj"
        process = subprocess.Popen(node_cmd.split(), stdout=subprocess.PIPE)
        ppath = path + "/" + node
        subnode_cmd = ex + " --subnode \"" + ppath + "\" --type elem"
        name_cmd = subnode_cmd + " -n \"name\" -v \"density\"" + "/tmp/2.prj  > /tmp/3.prj"
        process = subprocess.Popen(name_cmd.split(), stdout=subprocess.PIPE)
        type_cmd = subnode_cmd + " -n \"type\" -v \"Constant\" /tmp/3.prj  > /tmp/4.prj"
        process = subprocess.Popen(type_cmd.split(), stdout=subprocess.PIPE)
        value_cmd = subnode_cmd + " -n \"value\" -v \"" + str(value) + "\" /tmp/4.prj  > /tmp/5.prj"
        process = subprocess.Popen(value_cmd.split(), stdout=subprocess.PIPE)
        rename_cmd = ex + " --rename \"" + ppath + "\" -v \"property\" /tmp/5.prj  > " + file_name
        process = subprocess.Popen(rename_cmd.split(), stdout=subprocess.PIPE)

class LinearProperty:
    def __init__(self, name, ref_value, variable_name, slope, ref_condition):
        self.name = name
        self.ref_value = ref_value
        self.variable_name = variable_name
        self.slope = slope
        self.ref_condition = ref_condition
        self.xml_path = "//OpenGeoSysProject/media/medium/phases/phase/properties"

### read the density
# read property type: ConstantProperty or LinearProperty
density_type_command = "xmlstarlet sel -T -t -v //OpenGeoSysProject/processes/process/fluid/density/type " + sys.argv[1]
process = subprocess.Popen(density_type_command.split(), stdout=subprocess.PIPE)
density_type_byte_stream, error = process.communicate()

density_type = density_type_byte_stream.decode()
if (density_type == 'Constant'):
    density_value_cmd = "xmlstarlet sel -T -t -v //OpenGeoSysProject/processes/process/fluid/density/value " + sys.argv[1]
    process = subprocess.Popen(density_value_cmd.split(), stdout=subprocess.PIPE)
    density_value_stream, error = process.communicate()
    density_value = density_value_stream.decode()
    constant_density = ConstantDensity(density_type, density_value)

if (density_type == 'TemperatureDependent'):
    print('primary variable is temperature.')

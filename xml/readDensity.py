#!/bin/python

import sys
import subprocess

class ConstantProperty:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.xml_path = "//OpenGeoSysProject/media/medium/phases/phase/properties"

    def writeAsMediumPropertyToFile(self, file_name):
        print("writeAsMediumPropertyToFile ...")
        ex = "xmlstarlet ed "
        path = self.xml_path
        node = "property_density"
        node_cmd = ex + " --subnode \"" + path + "\" --type elem -n \"node\"" + file_name
        process = subprocess.Popen(node_cmd.split(), stdout=subprocess.PIPE)
        output_stream, errors = process.communicate()
        output = output_stream.decode()
        outfile = open('/tmp/2.prj', 'w')
        outfile.write(output)
        exit()

        ppath = path + "/" + node
        subnode_cmd = ex + " --subnode \"" + ppath + "\" --type elem"
        name_cmd = subnode_cmd + " -n \"name\" -v \"density\"" + "/tmp/2.prj"
        process = subprocess.Popen(name_cmd.split(), stdout=subprocess.PIPE)
        process = subprocess.Popen(node_cmd.split(), stdout=subprocess.PIPE)
        output_stream, errors = process.communicate()
        output = output_stream.decode()
        outfile = open('/tmp/3.prj', 'w')
        outfile.write(output)

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

    def writeAsMediumPropertyToFile(self, file_name):
        print("LinearProperty: writeAsMediumPropertyToFile ...")
        ex = "xmlstarlet ed "
        path = self.xml_path
        node = "property_density"
        node_cmd = ex + " --subnode " + path + " --type elem -n " + node + " " + file_name
        process = subprocess.Popen(node_cmd.split(), stdout=subprocess.PIPE)
        output_stream, errors = process.communicate()
        output = output_stream.decode()
        outfile = open('/tmp/2.prj', 'w')
        outfile.write(output)

        ppath = path + "/" + node
        subnode_cmd = ex + " --subnode " + ppath + " --type elem"
        name_cmd = subnode_cmd + " -n name -v density /tmp/2.prj"
        process = subprocess.Popen(name_cmd.split(), stdout=subprocess.PIPE)
        output_stream, errors = process.communicate()
        output = output_stream.decode()
        outfile = open('/tmp/3.prj', 'w')
        outfile.write(output)

        type_cmd = subnode_cmd + " -n type -v Linear /tmp/3.prj"
        process = subprocess.Popen(type_cmd.split(), stdout=subprocess.PIPE)
        output_stream, errors = process.communicate()
        output = output_stream.decode()
        outfile = open('/tmp/4.prj', 'w')
        outfile.write(output)

        value_cmd = subnode_cmd + " -n reference_value -v " + str(self.ref_value) + " /tmp/4.prj"
        process = subprocess.Popen(value_cmd.split(), stdout=subprocess.PIPE)
        output_stream, errors = process.communicate()
        output = output_stream.decode()
        outfile = open('/tmp/5.prj', 'w')
        outfile.write(output)

        # independent_variable
        iv_cmd = subnode_cmd + " -n independent_variable /tmp/5.prj"
        process = subprocess.Popen(iv_cmd.split(), stdout=subprocess.PIPE)
        output_stream, errors = process.communicate()
        output = output_stream.decode()
        outfile = open('/tmp/6.prj', 'w')
        outfile.write(output)

        #   variable_name
        iv_path = ppath + "/independent_variable"
        iv_name_cmd = ex + " --subnode " + iv_path + " --type elem -n variable_name -v " + str(self.variable_name) + " /tmp/6.prj"
        process = subprocess.Popen(iv_name_cmd.split(), stdout=subprocess.PIPE)
        output_stream, errors = process.communicate()
        output = output_stream.decode()
        outfile = open('/tmp/7.prj', 'w')
        outfile.write(output)

        #   reference_condition
        iv_reference_condition_cmd = ex + " --subnode " + iv_path + " --type elem -n reference_condition -v " + str(self.ref_condition) + " /tmp/7.prj"
        process = subprocess.Popen(iv_reference_condition_cmd.split(), stdout=subprocess.PIPE)
        output_stream, errors = process.communicate()
        output = output_stream.decode()
        outfile = open('/tmp/8.prj', 'w')
        outfile.write(output)

        #   slope
        iv_slope_cmd = ex + " --subnode " + iv_path + " --type elem -n slope -v " + str(self.slope) + " /tmp/8.prj"
        process = subprocess.Popen(iv_slope_cmd.split(), stdout=subprocess.PIPE)
        output_stream, errors = process.communicate()
        output = output_stream.decode()
        outfile = open('/tmp/9.prj', 'w')
        outfile.write(output)

        rename_cmd = ex + " --rename " + ppath + " -v property /tmp/9.prj"
        process = subprocess.Popen(rename_cmd.split(), stdout=subprocess.PIPE)
        output_stream, errors = process.communicate()
        output = output_stream.decode()
        outfile = open(file_name, 'w')
        outfile.write(output)

def addMedia(input, out):
    xml_path = "//OpenGeoSysProject/time_loop"
    ex = "xmlstarlet ed --insert " + xml_path + " --type elem -n media " + input
    process = subprocess.Popen(ex.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open(out, 'w')
    outfile.write(output)

def addMedium(input, out, medium_id):
    xml_path = "//OpenGeoSysProject/media"
    ex = "xmlstarlet ed --subnode " + xml_path + " --type elem -n medium " + input
    process = subprocess.Popen(ex.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open('/tmp/temp_medium_out.prj', 'w')
    outfile.write(output)

    xml_path = xml_path + "/medium"
    ex = "xmlstarlet ed --subnode " + xml_path + " --type attr -n id -v " + str(medium_id) + " /tmp/temp_medium_out.prj"
    process = subprocess.Popen(ex.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open(out, 'w')
    outfile.write(output)


def addPhases(input, out):
    xml_path = "//OpenGeoSysProject/media/medium"
    ex = "xmlstarlet ed --subnode " + xml_path + " --type elem -n phases " + input
    process = subprocess.Popen(ex.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open(out, 'w')
    outfile.write(output)

def addPhase(input, out, phase):
    xml_path = "//OpenGeoSysProject/media/medium/phases"
    ex = "xmlstarlet ed --subnode " + xml_path + " --type elem -n phase " + input
    process = subprocess.Popen(ex.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open(out, 'w')
    outfile.write(output)

    # phase
    xml_path = "//OpenGeoSysProject/media/medium/phases/phase"
    ex = "xmlstarlet ed --subnode " + xml_path + " --type elem -n type -v " + phase + " " + out
    process = subprocess.Popen(ex.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open(out, 'w')
    outfile.write(output)

def addProperties(input, out, phase):
    xml_path = "//OpenGeoSysProject/media/medium/phases/phase"
    ex = "xmlstarlet ed --subnode " + xml_path + " --type elem -n properties " + input
    process = subprocess.Popen(ex.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open(out, 'w')
    outfile.write(output)

def addMediumProperties(input, out):
    xml_path = "//OpenGeoSysProject/media/medium"
    ex = "xmlstarlet ed --subnode " + xml_path + " --type elem -n properties " + input
    process = subprocess.Popen(ex.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open(out, 'w')
    outfile.write(output)

# add thermal longitudinal dispersivity as phase independent property
def addThermalLongitudinalDispersivity(input, out, medium_id):
    xml_path = "//OpenGeoSysProject/media/medium/properties"
    ex = "xmlstarlet ed --subnode " + xml_path + " --type elem -n longitudinal_dispersivity_property " + input
    process = subprocess.Popen(ex.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open('/tmp/longitudinal_dispersivity.prj', 'w')
    outfile.write(output)

    xml_path_name = xml_path + "/longitudinal_dispersivity_property"
    ex = "xmlstarlet ed --subnode " + xml_path_name + " --type elem -n name -v thermal_longitudinal_dispersivity /tmp/longitudinal_dispersivity.prj"
    process = subprocess.Popen(ex.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open('/tmp/name_longitudinal_dispersivity.prj', 'w')
    outfile.write(output)

    xml_path_type = xml_path + "/longitudinal_dispersivity_property"
    ex = "xmlstarlet ed --subnode " + xml_path_type + " --type elem -n type -v Constant /tmp/name_longitudinal_dispersivity.prj"
    process = subprocess.Popen(ex.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open('/tmp/type_longitudinal_dispersivity.prj', 'w')
    outfile.write(output)

    xml_path_value = xml_path + "/longitudinal_dispersivity_property"
    ex = "xmlstarlet ed --subnode " + xml_path_value + " --type elem -n value -v 0.0 /tmp/type_longitudinal_dispersivity.prj"
    process = subprocess.Popen(ex.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open('/tmp/value_longitudinal_dispersivity.prj', 'w')
    outfile.write(output)

    # rename from longitudinal_dispersivity_property to property
    rename_cmd = "xmlstarlet ed --rename " + xml_path_name + " -v property /tmp/value_longitudinal_dispersivity.prj"
    process = subprocess.Popen(rename_cmd.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open(out, 'w')
    outfile.write(output)

# add thermal transversal dispersivity as phase independent property
def addThermalTransversalDispersivity(input, out, medium_id):
    xml_path = "//OpenGeoSysProject/media/medium/properties"
    ex = "xmlstarlet ed --subnode " + xml_path + " --type elem -n transversal_dispersivity_property " + input
    process = subprocess.Popen(ex.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open('/tmp/transversal_dispersivity.prj', 'w')
    outfile.write(output)

    xml_path_name = xml_path + "/transversal_dispersivity_property"
    ex = "xmlstarlet ed --subnode " + xml_path_name + " --type elem -n name -v thermal_transversal_dispersivity /tmp/transversal_dispersivity.prj"
    process = subprocess.Popen(ex.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open('/tmp/name_transversal_dispersivity.prj', 'w')
    outfile.write(output)

    xml_path_type = xml_path + "/transversal_dispersivity_property"
    ex = "xmlstarlet ed --subnode " + xml_path_type + " --type elem -n type -v Constant /tmp/name_transversal_dispersivity.prj"
    process = subprocess.Popen(ex.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open('/tmp/type_transversal_dispersivity.prj', 'w')
    outfile.write(output)

    xml_path_value = xml_path + "/transversal_dispersivity_property"
    ex = "xmlstarlet ed --subnode " + xml_path_value + " --type elem -n value -v 0.0 /tmp/type_transversal_dispersivity.prj"
    process = subprocess.Popen(ex.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open('/tmp/value_transversal_dispersivity.prj', 'w')
    outfile.write(output)

    # rename from transversal_dispersivity_property to property
    rename_cmd = "xmlstarlet ed --rename " + xml_path_name + " -v property /tmp/value_transversal_dispersivity.prj"
    process = subprocess.Popen(rename_cmd.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open(out, 'w')
    outfile.write(output)

# add specific heat capacity as phase independent property
def addSpecificHeatCapacity(input, out, medium_id):
    xml_path = "//OpenGeoSysProject/media/medium/properties"
    ex = "xmlstarlet ed --subnode " + xml_path + " --type elem -n specific_heat_capacity_property " + input
    process = subprocess.Popen(ex.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open('/tmp/specific_heat_capacity.prj', 'w')
    outfile.write(output)

    xml_path_name = xml_path + "/specific_heat_capacity_property"
    ex = "xmlstarlet ed --subnode " + xml_path_name + " --type elem -n name -v specific_heat_capacity /tmp/specific_heat_capacity.prj"
    process = subprocess.Popen(ex.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open('/tmp/name_specific_heat_capacity.prj', 'w')
    outfile.write(output)

    xml_path_type = xml_path + "/specific_heat_capacity_property"
    ex = "xmlstarlet ed --subnode " + xml_path_type + " --type elem -n type -v Constant /tmp/name_specific_heat_capacity.prj"
    process = subprocess.Popen(ex.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open('/tmp/type_specific_heat_capacity.prj', 'w')
    outfile.write(output)

    xml_path_value = xml_path + "/specific_heat_capacity_property"
    ex = "xmlstarlet ed --subnode " + xml_path_value + " --type elem -n value -v 4200 /tmp/type_specific_heat_capacity.prj"
    process = subprocess.Popen(ex.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open('/tmp/value_specific_heat_capacity.prj', 'w')
    outfile.write(output)

    # rename from specific_heat_capacity_property to property
    rename_cmd = "xmlstarlet ed --rename " + xml_path_name + " -v property /tmp/value_specific_heat_capacity.prj"
    process = subprocess.Popen(rename_cmd.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open(out, 'w')
    outfile.write(output)

### create media xml tree
addMedia(sys.argv[1], '/tmp/media.prj')
addMedium('/tmp/media.prj', '/tmp/medium.prj', 0)
addPhases('/tmp/medium.prj', '/tmp/phases.prj')
addPhase('/tmp/phases.prj', '/tmp/phase.prj', 'AqueousLiquid')
addProperties('/tmp/phase.prj', '/tmp/properties.prj', 'AqueousLiquid')
# rename
rename='cp /tmp/properties.prj ' + sys.argv[1]
rename_process = subprocess.Popen(rename.split(), stdout=subprocess.PIPE)

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
    constant_density.writeAsMediumPropertyToFile(sys.argv[1])

if (density_type == 'TemperatureDependent'):
    density_reference_cmd = "xmlstarlet sel -T -t -v //OpenGeoSysProject/processes/process/fluid/density/rho0 " + sys.argv[1]
    process = subprocess.Popen(density_reference_cmd.split(), stdout=subprocess.PIPE)
    density_reference_stream, error = process.communicate()
    density_reference = density_reference_stream.decode()

    temperature_reference_cmd = "xmlstarlet sel -T -t -v //OpenGeoSysProject/processes/process/fluid/density/temperature0 " + sys.argv[1]
    process = subprocess.Popen(temperature_reference_cmd.split(), stdout=subprocess.PIPE)
    temperature_reference_stream, error = process.communicate()
    temperature_reference = temperature_reference_stream.decode()

    slope_cmd = "xmlstarlet sel -T -t -v //OpenGeoSysProject/processes/process/fluid/density/beta " + sys.argv[1]
    process = subprocess.Popen(slope_cmd.split(), stdout=subprocess.PIPE)
    slope_stream, error = process.communicate()
    slope = slope_stream.decode()

    temperature_density = LinearProperty('density', density_reference, 'temperature', slope, temperature_reference)
    temperature_density.writeAsMediumPropertyToFile(sys.argv[1])


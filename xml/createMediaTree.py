#!/bin/python

import sys
import subprocess

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
    xml_medium_node = "medium_" + str(medium_id)
    ex = "xmlstarlet ed --subnode " + xml_path + " --type elem -n " + xml_medium_node + " " + input
    process = subprocess.Popen(ex.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open('/tmp/' + xml_medium_node + '_t1.prj', 'w')
    outfile.write(output)

    xml_medium = xml_path + "/" + xml_medium_node
    ex = "xmlstarlet ed --subnode " + xml_medium + " --type attr -n id -v " + str(medium_id) + " /tmp/" + xml_medium_node + "_t1.prj"
    process = subprocess.Popen(ex.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open('/tmp/' + xml_medium_node + '_t2.prj', 'w')
    outfile.write(output)

    addPhases('/tmp/' + xml_medium_node + '_t2.prj', '/tmp/' + xml_medium_node + '_t2_phases.prj', xml_medium)

    rename_cmd = "xmlstarlet ed --rename " + xml_medium + " -v medium /tmp/" + xml_medium_node + "_t2_phases.prj"
    process = subprocess.Popen(rename_cmd.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    outfile = open(out, 'w')
    outfile.write(output)

def addPhases(input, out, xml_path):
    ex = "xmlstarlet ed --subnode " + xml_path + " --type elem -n phases " + input
    process = subprocess.Popen(ex.split(), stdout=subprocess.PIPE)
    output_stream, errors = process.communicate()
    output = output_stream.decode()
    file_name = '/tmp/media_medium_phases.prj'
    outfile = open(file_name, 'w')
    outfile.write(output)

    addPhase(file_name, out, 'AqueousLiquid', "//OpenGeoSysProject/media/medium/phases")

def addPhase(input, out, phase, xml_path):
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

### create media xml tree
addMedia(sys.argv[1], '/tmp/media.prj')
addMedium('/tmp/media.prj', '/tmp/medium_0.prj', 0)
addMedium('/tmp/medium_0.prj', '/tmp/medium_1.prj', 1)
exit()
addPhase('/tmp/phases.prj', '/tmp/phase.prj', 'AqueousLiquid')
addProperties('/tmp/phase.prj', '/tmp/aqueous_properties.prj', 'AqueousLiquid')
addMediumProperties('/tmp/aqueous_properties.prj', '/tmp/medium_properties.prj')


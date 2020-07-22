#!/usr/bin/env python

import sys
from vtk import *
from pathlib import Path
from lxml import etree as ET

def readPVD(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    ts_files = {}
    ts_files['ts'] = []
    ts_files['filename'] = []
    for dataset in root.xpath('//DataSet'):
        ts_files['ts'].append(dataset.attrib['timestep'])
        ts_files['filename'].append(dataset.attrib['file'])
    return ts_files

def readPVTU(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    pvtu_files = {}
    pvtu_files['filename'] = []
    for piece in root.xpath('//Piece'):
        pvtu_files['filename'].append(piece.attrib['Source'])
    return pvtu_files

def readVTU(filename):
    reader = vtkXMLUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()
    return reader.GetOutput()

def extractBulkPointData(bulk_vtu, bulk_node_id, array_name):
    point_data = bulk_vtu.GetPointData()
    data_array = point_data.GetArray(array_name)
    return data_array.GetTuple1(bulk_node_id)

def extractBulkNodeIDFromPointVTU(point_vtu):
    point_data = point_vtu.GetPointData()
    bulk_node_ids = point_data.GetArray('bulk_node_ids')
    return bulk_node_ids.GetTuple1(0)

def extractBulkNodeCoordinatesFromPointVTU(point_vtu):
    return point_vtu.GetPoint(0)

def extractPartitionNumberFromFileName(filename):
    file_name = Path(filename).stem
    partition = int(file_name.rpartition('_')[2])
    return partition

def extractFileNameWithoutPartitionNumber(filename):
    file_name = Path(filename).stem
    return file_name.rpartition('_')[0]

def extractStationNameFromFileName(filename):
    file_name = (Path(filename).stem).rpartition('_ts_')[0]
    return file_name.partition('20a_')[2]

def extractPartitionAndNodeIDAndStationName(point_mesh_pvtu_filename):
    point_vtu_filenames = readPVTU(point_mesh_pvtu_filename)
    point_vtu_filename = point_vtu_filenames['filename'][0]
    station_name = extractStationNameFromFileName(point_vtu_filename)
    point_partition = extractPartitionNumberFromFileName(point_vtu_filename)
    bulk_node_id = int(extractBulkNodeIDFromPointVTU(readVTU(point_vtu_filename)))
    return point_partition, bulk_node_id, station_name

def readPointMeshInformation(argv):
    point_mesh_information = {}
    point_mesh_information['partition'] = []
    point_mesh_information['bulk_node_id'] = []
    point_mesh_information['station_name'] = []
    for i in range(2, len(argv)):
        point_partition, bulk_node_id, station_name = extractPartitionAndNodeIDAndStationName(sys.argv[i])
        point_mesh_information['partition'].append(point_partition)
        point_mesh_information['bulk_node_id'].append(bulk_node_id)
        point_mesh_information['station_name'].append(station_name)
    return point_mesh_information

# read pvd of the subsurface mesh
timestep_filenames = readPVD(sys.argv[1])

# read the point mesh information (partition number, bulk_node_id, and station
# name)
point_mesh_information = readPointMeshInformation(sys.argv)

# loop over the subsurface pvtu files
for k in range(1, len(timestep_filenames['filename'])):
    subsurface_mesh_pvtu_filename = timestep_filenames['filename'][k]
    bulk_vtu_filenames = readPVTU(subsurface_mesh_pvtu_filename)

    for i in range(0, len(point_mesh_information['station_name'])):
        partition = int(point_mesh_information['partition'][i])
        subsurface_vtu_file_name = extractFileNameWithoutPartitionNumber(bulk_vtu_filenames['filename'][0]) + '_' + str(partition) + '.vtu'
        subsurface_vtu = readVTU(subsurface_vtu_file_name)

        print(point_mesh_information['station_name'][i] + ',' + timestep_filenames['ts'][k] + ',' + str(extractBulkPointData(subsurface_vtu, point_mesh_information['bulk_node_id'][i], 'T')))


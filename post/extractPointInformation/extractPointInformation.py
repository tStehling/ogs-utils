#!/usr/bin/env python

import sys
from vtk import *
from pathlib import Path

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

bulk_vtu = readVTU(sys.argv[1])

bulk_node_ids = {}
bulk_node_ids['filename'] = []
bulk_node_ids['id'] = []

for i in range(2, len(sys.argv)):
    bulk_node_ids['filename'].append(sys.argv[i])
    point_vtu = readVTU(sys.argv[i])
    bulk_node_ids['id'].append(int(extractBulkNodeIDFromPointVTU(point_vtu)))

for i in range(0, len(bulk_node_ids['id'])):
    array_name = 'T'
    print(Path(bulk_node_ids['filename'][i]).stem + ' ' + str(extractBulkPointData(bulk_vtu, bulk_node_ids['id'][i], 'T')))



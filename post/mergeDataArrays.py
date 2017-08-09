#!/usr/bin/env python2

from vtk import *
from sys import argv, exit

if len(argv) < 6:
    print "Usage:", argv[0], "input.vtu scalar1 scalar2 vector_2d output.vtu"
    exit(1)

input_file = argv[1]
output_file = argv[5]
print("Reading from", input_file)
print("Writing to", output_file)

r = vtkXMLUnstructuredGridReader()
r.SetFileName(input_file)
r.Update()

m = r.GetOutput()
point_data = m.GetPointData()
scalar_array_1 = point_data.GetArray(argv[2])
scalar_array_2 = point_data.GetArray(argv[3])
new_array = vtkDoubleArray()
new_array.SetNumberOfComponents(2)
new_array.SetNumberOfTuples(scalar_array_1.GetNumberOfTuples())
new_array.SetName(argv[4])
new_array.CopyComponent(0, scalar_array_1, 0)
new_array.CopyComponent(1, scalar_array_2, 0)
point_data.AddArray(new_array)
point_data.RemoveArray(argv[2])
point_data.RemoveArray(argv[3])

w = vtkXMLUnstructuredGridWriter()
w.SetFileName(output_file)
w.SetInputData(m)
w.SetDataModeToAscii()
w.SetCompressorTypeToNone()
w.Update()

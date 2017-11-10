#
# \copyright
# Copyright (c) 2012-2017, OpenGeoSys Community (http://www.opengeosys.org)
#            Distributed under a Modified BSD License.
#              See accompanying file LICENSE.txt or
#              http://www.opengeosys.org/project/license
#

#!/usr/bin/env python2

from vtk import *
from sys import argv, exit

if len(argv) < 5:
    print "Usage:", argv[0], "input.vtu scalar_array1 ... name_for_new_array output.vtu"
    exit(1)

input_file = argv[1]
output_file = argv[len(argv)-1]
print("Reading from", input_file)
print("Writing to", output_file)

r = vtkXMLUnstructuredGridReader()
r.SetFileName(input_file)
r.Update()
m = r.GetOutput()

cell_data = m.GetCellData()
tensor_arrays = []

number_of_components = len(argv) - 4
number_of_tuples = cell_data.GetArray(argv[(2)]).GetNumberOfTuples()

for i in range(0, number_of_components):
    tensor_arrays.append(cell_data.GetArray(argv[(i)+2]))

new_array = vtkDoubleArray()
new_array.SetNumberOfComponents(number_of_components)
new_array.SetNumberOfTuples((number_of_tuples))
new_array.SetName(argv[len(argv)-2])

print "copy the particular cell data arrays to the cell data array ", argv[(len(argv)-2)]
for i in range(0, number_of_components):
    new_array.CopyComponent(i, tensor_arrays[i], 0)

print "add ", argv[(len(argv)-2)], " to the data arrays"
cell_data.AddArray(new_array)

print "remove the not needed cell data arrays"

for i in range(0, number_of_components):
    print "remove the not needed cell data array", argv[(i)+2]
    cell_data.RemoveArray(argv[(i)+2])

print "write result to file"

w = vtkXMLUnstructuredGridWriter()
w.SetFileName(output_file)
w.SetInputData(m)
w.SetDataModeToAscii()
w.SetCompressorTypeToNone()
w.Update()

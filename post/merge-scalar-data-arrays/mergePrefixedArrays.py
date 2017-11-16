#!/usr/bin/env python2

from vtk import *
from sys import argv, exit

if len(argv) != 5:
    print("errorneous number of args.")
    exit(1)

dimension = int(argv[1])
if dimension != 2 and dimension != 3:
    print("wrong dimension", dimension)
    exit(1)

field_name = argv[2]

input_filename = argv[3]
output_filename = argv[4]

r = vtkXMLUnstructuredGridReader()
r.SetFileName(input_filename)
r.Update()

m = r.GetOutput()
pd = m.GetPointData()

tensor = vtkDoubleArray()
tensor.SetName(field_name)
tensor.SetNumberOfComponents({2 : 4, 3 : 6}[dimension])
tensor.SetNumberOfTuples(m.GetNumberOfPoints())

for i in range(m.GetNumberOfPoints()):
    xx = pd.GetArray(field_name + '_xx').GetValue(i)
    yy = pd.GetArray(field_name + '_yy').GetValue(i)
    zz_array = pd.GetArray(field_name + '_zz')
    zz = 0 if zz_array is None else zz_array.GetValue(i)
    xy = pd.GetArray(field_name + '_xy').GetValue(i)

    if dimension == 2:
        tensor.SetTuple4(i, xx, yy, zz, xy)
    elif dimension == 3:
        xz_array = pd.GetArray(field_name + '_xz')
        xz = 0 if xz_array is None else xz_array.GetValue(i)
        yz_array = pd.GetArray(field_name + '_yz')
        yz = 0 if yz_array is None else yz_array.GetValue(i)

        tensor.SetTuple6(i, xx, yy, zz, xy, xz, yz)

pd.RemoveArray(field_name + '_xx')
pd.RemoveArray(field_name + '_yy')
pd.RemoveArray(field_name + '_zz')
pd.RemoveArray(field_name + '_xy')
pd.RemoveArray(field_name + '_xz')
pd.RemoveArray(field_name + '_yz')
pd.AddArray(tensor)

w = vtkXMLUnstructuredGridWriter()
w.SetFileName(output_filename)
w.SetInputData(m)
w.Update()
# Copyright (c) Alireza Hassanzadegan <alireza.hassanzadegan@bge.de>
# This program is free ; you can redistribute it and/or modify it
#
# Refactored as ParaView VTKPythonAlgorithm by Lars Bilke <lars.bilke@ufz.de>.

# Assigning material parameters
#
# To use this filter:
#
# 1. Convert the model to VTK format (e.g. using meshio) and load your Mesh.vtu
#    in Paraview.
# 2. Load this filter as a Plugin (Tools / Manage Plugins / Load New)
# 3. Apply this filter (AssignMaterialParameter) to the mesh
# 4. In the filter properties set the property "Data File" to your input csv
#    file. Pay attention to file paths, input file format(CSV) and separators
#    (delimiter must be;)
# 4. Material parameters are assigned based on the materialIDs (MID in Table)
#    as a keyword.

import os
from paraview.util.vtkAlgorithm import *

@smproxy.filter()
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkUnstructuredGrid"], composite_data_supported=False)
class AssignMaterialParameter(VTKPythonAlgorithmBase):
  def __init__(self):
      VTKPythonAlgorithmBase.__init__(self, nInputPorts=1, nOutputPorts=1, outputType="vtkUnstructuredGrid")
      self._csv_file = ""

  def FillInputPortInformation(self, port, info):
    if port == 0:
      info.Set(self.INPUT_REQUIRED_DATA_TYPE(), "vtkUnstructuredGrid")
    return 1

  def RequestData(self, request, inInfoVec, outInfoVec):
    from paraview import vtk
    import time
    startTime = time.time()
    pdi = vtk.vtkUnstructuredGrid.GetData(inInfoVec[0], 0)
    pdo = vtk.vtkUnstructuredGrid.GetData(outInfoVec, 0)
    pdo.ShallowCopy(pdi)

    # Assign MaterialIDs
    numcells = pdi.GetNumberOfCells()
    celldata = pdi.GetCellData()
    cellmid = celldata.GetArray("MaterialIDs")
    matIdsRange = cellmid.GetRange()
    numlines = int(matIdsRange[1])+1

    # Load data
    firstline =True
    FileName=os.path.normcase(self._csv_file)
    f = open(FileName)
    # Read header
    if firstline:
      firstline = False
      header=f.readline().split(";")

    # How many materialparameter
    numparam=int(len(header))

    # Restore data as List in List
    datalist = []
    for line in f:
      data = line.split(";")
      datalist.append(data)

    # Assign properties to CellData
    for j in range(1, numparam): # skip first column (MID)
      dataArray = vtk.vtkDoubleArray()
      dataArray.SetNumberOfComponents(1)
      dataArray.SetName(header[j])
      for i in range(numlines):
        for k in range(numcells):
          t = int(cellmid.GetTuple1(k))
          dataArray.InsertNextValue(float(datalist[t][j]))
      pdo.GetCellData().AddArray(dataArray)

    print('Material parameters were assigned. It took %8.2f seconds.' %(time.time() - startTime))
    return 1

  @smproperty.stringvector(name="Data File", number_of_elements="1")
  def SetCSV(self, value):
    if os.path.isfile(value) and os.access(value, os.R_OK):
      self._csv_file = value
      self.Modified()
    else:
      print("File does not exist: ", value)

#!/usr/bin/env pvpython

import inspect

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input", type=str, required=True)
parser.add_argument("--output", type=str, required=True)
args = parser.parse_args()

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'XML Unstructured Grid Reader'
xMLUnstructuredGridReader1 = XMLUnstructuredGridReader(FileName=[args.input])


def do_enumerate_points():
    data = self.GetInputDataObject(0, 0)

    # point_ids = vtk.vtkIdTypeArray()  ## TODO why does that not work?
    # point_ids = vtk.vtkLongArray()
    point_ids = vtk.vtkUnsignedLongArray()
    point_ids.SetName("OriginalSubsurfaceNodeIDs")
    point_ids.SetNumberOfComponents(1)
    N = data.GetPoints().GetNumberOfPoints()
    point_ids.SetNumberOfTuples(N)

    for i in range(N):
        point_ids.SetComponent(i, 0, i)

    self.GetOutputDataObject(0).GetPointData().AddArray(point_ids)

    ### Cell ids do not work like that:
    # cell_ids = vtk.vtkDoubleArray()
    # cell_ids.SetName("bulk_mesh_element_ids")
    # cell_ids.SetNumberOfComponents(1)
    # C = data.GetCellData().GetNumberOfTuples()
    # cell_ids.SetNumberOfTuples(N)

    # for i in range(C):
    #     cell_ids.SetComponent(i, 0, i)

    # self.GetOutputDataObject(0).GetCellData().AddArray(cell_ids)


enumerate_points = ProgrammableFilter(Input=xMLUnstructuredGridReader1)
enumerate_points.Script = inspect.getsource(do_enumerate_points) + "\n\ndo_enumerate_points()"
enumerate_points.RequestInformationScript = ''
enumerate_points.RequestUpdateExtentScript = ''
enumerate_points.PythonPath = ''
enumerate_points.CopyArrays = 0


# create a new 'Slice'
slice1 = Slice(Input=enumerate_points)
slice1.SliceType = 'Plane'
slice1.Triangulatetheslice = 0
slice1.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [0.0044, 0.03, 0.0]
slice1.SliceType.Normal = [0.0, 1.0, 0.0]


# Trick from http://www.vtk.org/Wiki/VTK/Examples/Cxx/PolyData/PolyDataToUnstructuredGrid
# for converting slice's polydata to an unstructured grid
appendDatasets1 = AppendDatasets(Input=slice1)


def do_compute_mass_flux():
    import numpy as np
    from scipy.interpolate import interp1d
    data = self.GetInputDataObject(0, 0)

    ### compute predefined mass flux

    mu  = 21.90e-6 # Pa s
    rho = 0.9333 # kg/m³

    csv = "smooth_velocity_profile.csv"
    rs, velocities = np.loadtxt(csv, unpack=True, usecols=(0,1))
    velocity_fct = interp1d(rs, velocities)

    points = data.GetPoints()

    mass_flux = vtk.vtkDoubleArray()
    mass_flux.SetName("mass_flux")
    mass_flux.SetNumberOfComponents(1)
    N = points.GetNumberOfPoints()
    mass_flux.SetNumberOfTuples(N)

    for i in range(N):
        r, z, phi = points.GetPoint(i)
        mass_flux.SetComponent(i, 0, velocity_fct(r) * rho)

    self.GetOutputDataObject(0).GetPointData().AddArray(mass_flux)


mass_flux = ProgrammableFilter(Input=appendDatasets1)
mass_flux.Script = inspect.getsource(do_compute_mass_flux) + "\n\ndo_compute_mass_flux()"
mass_flux.RequestInformationScript = ''
mass_flux.RequestUpdateExtentScript = ''
mass_flux.PythonPath = ''
mass_flux.CopyArrays = 1

# ----------------------------------------------------------------
# finally, restore active source
SetActiveSource(mass_flux)
# ----------------------------------------------------------------

# save data
SaveData(args.output, proxy=mass_flux, DataMode='Binary',
    EncodeAppendedData=1,
    CompressorType='ZLib')


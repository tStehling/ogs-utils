#!/usr/bin/env pvpython
# -*- coding: utf-8 -*-

import inspect

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input", type=str, required=True)
parser.add_argument("--output", type=str, required=True)
args = parser.parse_args()


# state file generated using paraview version 5.3.0

# ----------------------------------------------------------------
# setup views used in the visualization
# ----------------------------------------------------------------

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'XML Unstructured Grid Reader'
xMLUnstructuredGridReader1 = XMLUnstructuredGridReader(FileName=[args.input])

# create a new 'Calculator'
coords_to_property = Calculator(Input=xMLUnstructuredGridReader1)
coords_to_property.ResultArrayName = 'cell_centers'
coords_to_property.Function = 'coords'

# create a new 'Point Data to Cell Data'
pointDatatoCellData2 = PointDatatoCellData(Input=coords_to_property)

def compute_perm():
    import os
    import numpy as np
    from scipy.interpolate import interp1d

    csv = "smooth_permeability_profile.csv"
    rs, perms = np.loadtxt(csv, unpack=True, usecols=(0,1))
    perm_fct = interp1d(rs, perms)

    data = self.GetInputDataObject(0, 0)
    cell_centers = data.GetCellData().GetArray("cell_centers")

    perm_cell = vtk.vtkDoubleArray()
    perm_cell.SetName("K_rho_over_mu__eff")
    perm_cell.SetNumberOfComponents(1)
    N = cell_centers.GetNumberOfTuples()
    perm_cell.SetNumberOfTuples(N)

    mu  = 21.90e-6 # Pa s
    rho = 0.9333 # kg/m³

    for i in range(N):
        r, z, _ = cell_centers.GetTuple(i)
        K = perm_fct(r)
        perm_cell.SetComponent(i, 0, K * rho / mu)

    self.GetOutputDataObject(0).GetCellData().AddArray(perm_cell)


    if True:
        # mass flux

        csv = "smooth_velocity_profile.csv"
        rs, velocities = np.loadtxt(csv, unpack=True, usecols=(0,1))
        velocity_fct = interp1d(rs, velocities)

        points = data.GetPoints()

        mass_flux = vtk.vtkDoubleArray()
        mass_flux.SetName("mass_flux_ref")
        mass_flux.SetNumberOfComponents(2)
        N = points.GetNumberOfPoints()
        mass_flux.SetNumberOfTuples(N)

        for i in range(N):
            r, z, phi = points.GetPoint(i)
            mass_flux.SetComponent(i, 0, 0)
            mass_flux.SetComponent(i, 1, -velocity_fct(r) * rho)

        self.GetOutputDataObject(0).GetPointData().AddArray(mass_flux)

    self.GetOutputDataObject(0).GetCellData().RemoveArray("cell_centers")


perm = ProgrammableFilter(Input=pointDatatoCellData2)
perm.Script = inspect.getsource(compute_perm) + "\n\ncompute_perm()"
perm.RequestInformationScript = ''
perm.RequestUpdateExtentScript = ''
perm.PythonPath = ''
perm.CopyArrays = 0

# ----------------------------------------------------------------
# finally, restore active source
SetActiveSource(perm)
# ----------------------------------------------------------------

# save data
SaveData(args.output, proxy=perm, DataMode='Binary',
    EncodeAppendedData=1,
    CompressorType='ZLib')

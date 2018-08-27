#!/usr/bin/env pvpython

import inspect

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--bulk", type=str, required=True)
parser.add_argument("--boundary", type=str, required=True)
parser.add_argument("--output", type=str, required=True)
args = parser.parse_args()

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'XML Unstructured Grid Reader'
reader_bulk = XMLUnstructuredGridReader(FileName=[args.bulk])
reader_boundary = XMLUnstructuredGridReader(FileName=[args.boundary])


def do_mapping():
    bulk = self.GetInputDataObject(0, 1)
    boundary = self.GetInputDataObject(0, 0)

    points_bulk = bulk.GetPoints()
    points_boundary = boundary.GetPoints()

    N_boundary = points_boundary.GetNumberOfPoints()
    N_bulk = points_bulk.GetNumberOfPoints()

    # point_ids = vtk.vtkIdTypeArray()  ## TODO why does that not work?
    # point_ids = vtk.vtkLongArray()
    point_ids = vtk.vtkUnsignedLongArray()
    point_ids.SetName("bulk_node_ids")
    point_ids.SetNumberOfComponents(1)
    point_ids.SetNumberOfTuples(N_boundary)

    i_bulk = 0
    map_coords_to_bulk_point_ids = {}

    for i_boundary in range(N_boundary):
        coords_boundary = points_boundary.GetPoint(i_boundary)

        try:
            point_id_bulk = map_coords_to_bulk_point_ids[coords_boundary]
        except KeyError:
            # If point has not been mapped yet, search for it
            # Note: This approach is not very efficient, and in the worst case
            # it copies all bulk mesh nodes.
            for i_bulk in range(i_bulk, N_bulk):
                coords_bulk = points_bulk.GetPoint(i_bulk)

                if coords_bulk == coords_boundary:
                    point_id_bulk = i_bulk
                    # Breaking here makes sure that duplicate nodes are not
                    # found and an error message will be generated
                    break

                map_coords_to_bulk_point_ids[coords_bulk] = i_bulk
            else:
                raise ValueError("The boundary coordinates " + str(coords_boundary)
                        + " have not been found in the bulk mesh. Reasons might be"
                        + " (i) those coordinates do not match any in the bulk mesh, or"
                        + " (ii) those coordinates are duplicate in the boundary mesh")

        point_ids.SetComponent(i_boundary, 0, point_id_bulk)


    self.GetOutputDataObject(0).GetPointData().AddArray(point_ids)

    # TODO map cells


boundary_bulk_mapping = ProgrammableFilter(Input=[reader_boundary, reader_bulk])
boundary_bulk_mapping.Script = inspect.getsource(do_mapping) + "\n\ndo_mapping()"
boundary_bulk_mapping.RequestInformationScript = ''
boundary_bulk_mapping.RequestUpdateExtentScript = ''
boundary_bulk_mapping.PythonPath = ''
boundary_bulk_mapping.CopyArrays = 1


# save data
SaveData(args.output, proxy=boundary_bulk_mapping, DataMode='Binary',
    EncodeAppendedData=1,
    CompressorType='ZLib')


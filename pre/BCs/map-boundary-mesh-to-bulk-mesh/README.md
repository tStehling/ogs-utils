# Map the nodes of a boundary mesh to the corresponding nodes of the given bulk mesh

## Requirements

* Both meshes have to be conforming, i.e., the coordinates of the boundary mesh
  must exactly coincide with the coordinates of some bulk mesh nodes
* Put more explicitly: The coordinates in bulk and boundary must exactly match,
  i.e., bit-wise, because this script does not apply any tolerances.


## What is output?

* A nodal field `bulk_node_ids` is added to the given `--boundary` mesh.
  This nodal field maps the nodes of the boundary mesh to the corresponding
  nodes of the `--bulk` mesh.
* The generated `--output` mesh can be used with OGS to specify (inhomogeneous)
  Boundary conditions along arbitrary surfaces.


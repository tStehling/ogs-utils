# Prepare an inhomogeneous node-based mass flux field along a slice through a mesh

The superficial velocity is given as a profile in radial (i.e., x) direction in the file `smooth_velocity_profile.csv`.

A slice (hard-coded) through the `--input` mesh is taken. The mass flux field is
evaluated at every node of the slice. The slice with the mass flux field is
written to a VTU file in `--output`.

Additionally to the `mass_flux` field, there will be a field `bulk_mesh_node_ids` which is used by OGS to map the mass flux values to the right mesh nodes if used as a Neumann BC.


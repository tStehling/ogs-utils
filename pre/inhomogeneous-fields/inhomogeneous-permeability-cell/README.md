# Prepare an inhomogeneous cell-based permeability field

The permeability is given as a profile in radial (i.e., x) direction in the file `smooth_permeability_profile.csv`.
The permeability value is evaluated at the center coordinate of each cell of the mesh read from `--input`.
The resulting field and mesh is written to `--output`.

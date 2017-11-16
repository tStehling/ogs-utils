# Merge two scalar data arrays

The script 'mergeDataArrays' takes two scalar nodal fields from a vtu file and combines them to a
two-component vector field.

The script 'mergeDataArraysIntoOne' takes arbitrary number of scalar fields from
a vtu file and uses them as the components of a vector field that will be
created.

# Merge prefixed scalar fields (mechanics)

All fields starting with a given prefix and ending with `_xx`, `_yy`, `_zz`,
`_xy`, `_yz`, and `_xz` will be merged into a single vectorial array with four
or six components depending on the given dimension.
This is useful to combine arrays like `sigma_xx`, _etc._ to single `sigma`
array.

Example usage:
```sh
mergePrefixedArrays.py 2 sigma input.vtu output.vtu
mergePrefixedArrays.py 3 epsilon input.vtu output.vtu
```

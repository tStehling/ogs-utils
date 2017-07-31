Measured compilation time after changing a single file of the OGS sources.
This should resemble the usual process development work.

# Summary

Compiling with fixed-size Eigen matrices takes significantly longer than with
dynamic-sized Eigen matrices.

# Used script

```{sh}
#!/bin/sh

set -e

export MAKEFLAGS="-j3"

(
    cd ../src
    if [ "`git status --porcelain | wc -l`" -ne 0 ]; then
        echo "Source directory contains untracked/uncommitted changes. Aborting" >&2
        exit 1
    fi
) || exit 1


if ! mkdir "build" &>/dev/null; then
    echo "WARNING: reusing existing build directory!" >&2
    read -r -p "Hit enter to continue "
fi

cd build

# set some cmake option I usually use
if ! cmake ../../src \
    -DCMAKE_BUILD_TYPE=Release \
    -DOGS_EIGEN_DYNAMIC_SHAPE_MATRICES=ON \
    -DOGS_USE_LIS=ON;
then
    # workaround for second git worktree
    (
        cd CMakeFiles/git-data
        ln -s HEAD head-ref
    )
    cmake .
fi

# initial build in fresh build directory
time make ogs

# make a non-trivial change to the code
echo "inline void unused_dummy_function() {}" >> ../../src/ProcessLib/TES/TESLocalAssemblerInner.h

# supposedly faster second build
time make ogs
```

# Some results

Summary: Initial compile time: ~ 10 minutes, compilation of changes only: ~ 16 seconds.
Changing only ProcessLib/SmallDeformation/SmallDeformationFEM.h took ~20 seconds in the second build.

```
[...]
Scanning dependencies of target ogs
[100%] Building CXX object Applications/CLI/CMakeFiles/ogs.dir/ogs.cpp.o
[100%] Linking CXX executable ../../bin/ogs
[100%] Built target ogs

real	9m47,808s
user	24m2,080s
sys	1m25,050s
[  5%] Built target logog
[ 10%] Built target BaseLib
[ 19%] Built target MathLib
[ 28%] Built target GeoLib
[ 47%] Built target MeshLib
[ 52%] Built target MeshGeoToolsLib
[ 61%] Built target NumLib
[ 75%] Built target MaterialLib
Scanning dependencies of target ProcessLib
[ 75%] Building CXX object ProcessLib/CMakeFiles/ProcessLib.dir/TES/CreateTESProcess.cpp.o
[ 75%] Building CXX object ProcessLib/CMakeFiles/ProcessLib.dir/TES/TESLocalAssemblerInner.cpp.o
[ 77%] Building CXX object ProcessLib/CMakeFiles/ProcessLib.dir/TES/TESProcess.cpp.o
[ 77%] Building CXX object ProcessLib/CMakeFiles/ProcessLib.dir/TES/TESReactionAdaptor.cpp.o
[ 78%] Linking CXX static library ../lib/libProcessLib.a
[100%] Built target ProcessLib
[100%] Built target ApplicationsLib
[100%] Linking CXX executable ../../bin/ogs
[100%] Built target ogs

real	0m15,544s
user	0m26,212s
sys	0m1,759s
```

## For reference: fixed-size Eigen matrices, three threads, ccache not disabled (but maybe not effective)

initial build:
```
real	55m52,166s
user	63m0,470s
sys	7m32,749s
```

build after change:
```
real	2m6,759s
user	2m11,119s
sys	0m2,841s
```

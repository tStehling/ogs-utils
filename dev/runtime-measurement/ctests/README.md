# Runtime measurements for OGS's ctests

The run time for OGS's ctests for fixed-size Eigen matrices and dynamic-size
Eigen matrices is measured and compared.

The final results are given in the Libreoffice spreadsheet.

## Shell commands

```{sh}
export OMP_NUM_THREADS=1

for d in build*/; do ( cd "$d"; ctest; ); done

find build/Tests/Data/ build-fixed/Tests/Data/ -type f -name '*.log' -exec ../compute-time-shares.py --quiet --json-out {} \;

../aggregate_timings.py build-fixed/Tests/Data/ - | sort >timings_fixed.csv
../aggregate_timings.py build/Tests/Data/ - | sort >timings_dynamic.csv


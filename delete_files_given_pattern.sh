#!/bin/bash
#
sessionID=${1}
nifti_id=$(python3 - <<EOF
from utilities_using_xnat_python import get_id_from_nifti_location_csv

val = get_id_from_nifti_location_csv("${sessionID}")

if val is not None:
    print(val)
EOF
)

echo "NIFTI_ID = $nifti_id"
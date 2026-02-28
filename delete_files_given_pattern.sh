#!/bin/bash
#
sessionID=${1}
scanID=$(python3 - <<EOF
from utilities_using_xnat_python import get_id_from_nifti_location_csv

val = get_id_from_nifti_location_csv("${sessionID}")

if val is not None:
    print(val)
EOF
)
resourceName="MASKS"
pattern='ventricle.nii'
patternType='regex'
echo "NIFTI_ID = $scanID"
python3 - <<EOF
from utilities_using_xnat_python import xnat_delete_files_in_scan_resource_by_pattern

summary = xnat_delete_files_in_scan_resource_by_pattern(
    session_id="${sessionID}",
    scan_id="${scanID}",
    resource_name="${resourceName}",
    pattern=r"${pattern}",
    pattern_type="${patternType}",   # "regex" or "glob"
    dry_run=False
)

print(summary)
EOF
pattern='total.nii'
python3 - <<EOF
from utilities_using_xnat_python import xnat_delete_files_in_scan_resource_by_pattern

summary = xnat_delete_files_in_scan_resource_by_pattern(
    session_id="${sessionID}",
    scan_id="${scanID}",
    resource_name="${resourceName}",
    pattern=r"${pattern}",
    pattern_type="${patternType}",   # "regex" or "glob"
    dry_run=False
)

print(summary)
EOF
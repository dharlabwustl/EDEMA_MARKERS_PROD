#!/usr/bin/env bash
#set -euo pipefail

SESSION_ID="$1"

ID_VALUE=$(
python3 - <<EOF
import sys
from utilities_using_xnat_python import get_id_from_nifti_location_csv

session_id = "${SESSION_ID}"
val = get_id_from_nifti_location_csv(session_id)

if val is None:
    sys.exit(1)

print(val)
EOF
)

echo "NIFTI_LOCATION ID = ${ID_VALUE}"

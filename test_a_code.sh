#!/usr/bin/env bash
#set -euo pipefail

SESSION_ID="$1"

ID_VALUE=$(
python3 - <<EOF
import sys
from datetime import datetime

try:
    from utilities_using_xnat_python import get_id_from_nifti_location_csv
except Exception as e:
    with open("./error.txt", "a") as f:
        f.write(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"ImportError in bash wrapper\n"
            f"Error: {e}\n"
            f"{'-'*80}\n"
        )
    sys.exit(1)

session_id = "${SESSION_ID}"

try:
    val = get_id_from_nifti_location_csv(session_id)
    if val is None:
        with open("./error.txt", "a") as f:
            f.write(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                f"get_id_from_nifti_location_csv returned None\n"
                f"Session ID: {session_id}\n"
                f"{'-'*80}\n"
            )
        sys.exit(1)

    print(val)

except Exception as e:
    with open("./error.txt", "a") as f:
        f.write(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"Unhandled exception in bash wrapper\n"
            f"Session ID: {session_id}\n"
            f"Error: {e}\n"
            f"{'-'*80}\n"
        )
    sys.exit(1)
EOF
)


echo "NIFTI_LOCATION ID = ${ID_VALUE}"

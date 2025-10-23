#!/bin/bash

# ==============================
# Usage: ./get_selected_scan.sh XNAT_SESSION_ID
# ==============================

# 1. Take session ID from command line
SESSION_ID="$1"

# 2. Run the Python function and capture its output
SCAN_INFO=$(python3 - <<EOF
from download_with_session_ID import find_selected_scan_id
scan_id, scan_name = find_selected_scan_id("${SESSION_ID}")
print(f"{scan_id},{scan_name}")
EOF
)

# 3. Split into variables
SCAN_ID=$(echo "$SCAN_INFO" | cut -d',' -f1)
SCAN_NAME=$(echo "$SCAN_INFO" | cut -d',' -f2)

# 4. Print nicely or use them downstream
echo "Selected scan ID:   $SCAN_ID"
echo "Selected scan name: $SCAN_NAME"

#!/bin/bash
# save as: fetch_best_csv.sh
# Usage: ./fetch_best_csv.sh XNAT_SESSION_ID SCAN_ID /path/to/save.csv

# SESSION_ID="$1"
# SCAN_ID="$2"
OUTPATH="/workingoutput"

python3 - <<'PY'
import sys, json, os
from download_with_session_ID import get_largest_newest_csv_for_scan, download_xnat_file_to_path

session_id, scan_id, out_path = "${SESSION_ID}", "${SCAN_ID}", "${OUTPATH}"
info = get_largest_newest_csv_for_scan(session_id, scan_id)
download_xnat_file_to_path(info["uri"], out_path)
print(json.dumps({"saved": out_path, "name": info["name"], "size": info["size"], "created": str(info["created"])}, ensure_ascii=False))
PY


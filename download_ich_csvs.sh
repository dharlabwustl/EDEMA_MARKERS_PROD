#!/bin/bash
# Usage: ./get_first_ct_session.sh SUBJECT_ID [PROJECT_ID]
# Example: ./get_first_ct_session.sh SNIPR02_S12345 BJH_ICH

set -euo pipefail

SUBJECT_ID="${1:?subject id required}"
PROJECT_ID="${2:-ICH}"         # default if not provided
OUTPATH="/workingoutput"

# 1) Earliest CT session for subject (prints: "SESSION_ID"::<id>::"LABEL"::<label>::"DATE"::<date>)
RAW_SESSION=$(
python3 - <<EOF
from download_with_session_ID import get_first_ct_session_for_subject
# Function must accept (project_id, subject_id) and internally call:
#   /data/projects/{project_id}/subjects/{subject_id}/experiments?format=json
get_first_ct_session_for_subject("${PROJECT_ID}", "${SUBJECT_ID}")
EOF
)

# Parse session line
SESSION_ID=$(awk -F'::' '{gsub(/"/,"",$2); print $2}' <<< "$RAW_SESSION" | tr -d '[:space:]')
SESSION_LABEL=$(awk -F'::' '{gsub(/"/,"",$4); print $4}' <<< "$RAW_SESSION" | sed 's/[[:space:]]\+$//' )
SESSION_DATE=$(awk -F'::' '{gsub(/"/,"",$6); print $6}' <<< "$RAW_SESSION" | tr -d '[:space:]')

echo "Earliest CT session ID:     $SESSION_ID"
echo "Earliest CT session label:  $SESSION_LABEL"
echo "Session date:               $SESSION_DATE"

# 2) Find selected scan within that session (prints: "SCAN_ID"::<id>::"SCAN_NAME"::<name>)
RAW_SCAN=$(
python3 - <<EOF
from download_with_session_ID import find_selected_scan_id
#print(find_selected_scan_id("${SESSION_ID}"))
find_selected_scan_id("${SESSION_ID}")
EOF
)

# Parse scan line
SCAN_ID=$(awk -F'::' '{gsub(/"/,"",$2); print $2}' <<< "$RAW_SCAN" | tr -d '[:space:]')
SCAN_NAME=$(awk -F'::' '{gsub(/^"/,"",$4); gsub(/"$/,"",$4); print $4}' <<< "$RAW_SCAN" | sed 's/[[:space:]]\+$//')

echo "Selected scan ID:           $SCAN_ID"
echo "Selected scan name:         $SCAN_NAME"

# 3) Get largest-newest CSV for that scan (no exports; pass as argv)
python3 - "$SESSION_ID" "$SCAN_ID" "$OUTPATH" <<'PY'
import sys, json, os
from download_with_session_ID import get_largest_newest_csv_for_scan, download_xnat_file_to_path

session_id, scan_id, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]

info = get_largest_newest_csv_for_scan(session_id, scan_id)
# If your downloader expects a filepath, save under original filename in out_dir:
filename = info["name"] if info.get("name") else os.path.basename(info["uri"])
out_path = os.path.join(out_dir, filename)

download_xnat_file_to_path(info["uri"], out_path)
print(json.dumps({"saved": out_path, **{k:v for k,v in info.items() if k!="uri"}}, indent=2, ensure_ascii=False))
PY

# 4) Get largest-newest PDF for that scan
python3 - "$SESSION_ID" "$SCAN_ID" "$OUTPATH" <<'PY'
import sys, json, os
from download_with_session_ID import get_largest_newest_pdf_for_scan, download_xnat_file_to_path

session_id, scan_id, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]

info = get_largest_newest_pdf_for_scan(session_id, scan_id)
filename = info["name"] if info.get("name") else os.path.basename(info["uri"])
out_path = os.path.join(out_dir, filename)

download_xnat_file_to_path(info["uri"], out_path)
print(json.dumps({"saved": out_path, **{k:v for k,v in info.items() if k!="uri"}}, indent=2, ensure_ascii=False))
PY

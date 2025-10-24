#!/bin/bash
# Usage: ./get_first_ct_session.sh SUBJECT_ID

SUBJECT_ID="$1"
project_id='ICH'
RAW=$(python3 - <<EOF
from download_with_session_ID import get_first_ct_session_for_subject
get_first_ct_session_for_subject("${project_id}","${SUBJECT_ID}")
EOF
)

# Parse output string: "SESSION_ID"::<id>::"LABEL"::<label>::"DATE"::<date>
SESSION_ID=$(awk -F'::' '{gsub(/"/,"",$2); print $2}' <<< "$RAW" | tr -d '[:space:]')
SESSION_LABEL=$(awk -F'::' '{gsub(/"/,"",$4); print $4}' <<< "$RAW" | tr -d '[:space:]')
SESSION_DATE=$(awk -F'::' '{gsub(/"/,"",$6); print $6}' <<< "$RAW" | tr -d '[:space:]')

echo "Earliest CT session ID:     $SESSION_ID"
echo "Earliest CT session label:  $SESSION_LABEL"
echo "Session date:               $SESSION_DATE"

##!/bin/bash
#
## ==============================
## Usage: ./get_selected_scan.sh XNAT_SESSION_ID
## ==============================
#
# 1️⃣ Take session ID from command line
#SESSION_ID="$1"
OUTPATH="/workingoutput"

# 2️⃣ Call Python function to get selected scan (returns one string)
RAW=$(
python3 - <<EOF
from download_with_session_ID import find_selected_scan_id
#print(find_selected_scan_id("${SESSION_ID}"))
find_selected_scan_id("${SESSION_ID}")
EOF
)
echo $RAW

# 3️⃣ Parse "SCAN_ID"::<id>::"SCAN_NAME"::<name>
#SCAN_ID=$(awk -F'::' '{gsub(/"/,"",$2); print $2}' <<< "$RAW")
#SCAN_NAME=$(awk -F'::' '{gsub(/^"/,"",$4); gsub(/"$/,"",$4); print $4}' <<< "$RAW")

# 3️⃣ Parse "SCAN_ID"::<id>::"SCAN_NAME"::<name>
SCAN_ID=$(awk -F'::' '{gsub(/"/,"",$2); print $2}' <<< "$RAW" | tr -d '[:space:]')
SCAN_NAME=$(awk -F'::' '{gsub(/^"/,"",$4); gsub(/"$/,"",$4); print $4}' <<< "$RAW" | tr -d '[:space:]')

echo "Selected scan ID:   $SCAN_ID"
echo "Selected scan name: $SCAN_NAME"


echo "Selected scan ID:   $SCAN_ID"
echo "Selected scan name: $SCAN_NAME"

# 4️⃣ Export variables so Python can read them safely via environment
#export SESSION_ID SCAN_ID OUTPATH
#
## 5️⃣ Run Python to get largest & newest CSV from ICH_PHE_QUANTIFICATION
#python3 - <<'PY'
#import os, json
#from download_with_session_ID import get_largest_newest_csv_for_scan, download_xnat_file_to_path
#
#session_id = os.environ["SESSION_ID"]
#scan_id = os.environ["SCAN_ID"]
#out_path = os.environ["OUTPATH"]
# Run Python inline and pass variables as arguments
python3 - "$SESSION_ID" "$SCAN_ID" "$OUTPATH" <<'PY'
import sys, json
from download_with_session_ID import get_largest_newest_csv_for_scan, download_xnat_file_to_path

# Read arguments passed from bash
session_id, scan_id, out_path = sys.argv[1], sys.argv[2], sys.argv[3]

info = get_largest_newest_csv_for_scan(session_id, scan_id)
download_xnat_file_to_path(info["uri"], out_path)

print(json.dumps({
    "saved": out_path,
    "name": info["name"],
    "size": info["size"],
    "created": str(info["created"])
}, indent=2, ensure_ascii=False))
PY

#info = get_largest_newest_csv_for_scan (session_id, scan_id)
#download_xnat_file_to_path(info["uri"], out_path)
#
#print(json.dumps({
#    "saved": out_path,
#    "name": info["name"],
#    "size": info["size"],
#    "created": str(info["created"])
#}, indent=2, ensure_ascii=False))
#PY

python3 - "$SESSION_ID" "$SCAN_ID" "$OUTPATH" <<'PY'
import sys, json
from download_with_session_ID import get_largest_newest_pdf_for_scan, download_xnat_file_to_path

# Read arguments passed from bash
session_id, scan_id, out_path = sys.argv[1], sys.argv[2], sys.argv[3]

info = get_largest_newest_pdf_for_scan(session_id, scan_id)
download_xnat_file_to_path(info["uri"], out_path)

print(json.dumps({
    "saved": out_path,
    "name": info["name"],
    "size": info["size"],
    "created": str(info["created"])
}, indent=2, ensure_ascii=False))
PY

#info=get_largest_newest_csv_for_scan(session_id, scan_id)
#download_xnat_file_to_path(info["uri"], out_path)
#
#print(json.dumps({
#    "saved": out_path,
#    "name": info["name"],
#    "size": info["size"],
#    "created": str(info["created"])
#}, indent=2, ensure_ascii=False))
#PY

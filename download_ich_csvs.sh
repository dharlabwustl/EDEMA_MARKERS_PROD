#!/bin/bash

# ==============================
# Usage: ./get_selected_scan.sh XNAT_SESSION_ID
# ==============================

# 1️⃣ Take session ID from command line
SESSION_ID="$1"
OUTPATH="/workingoutput"

# 2️⃣ Call Python function to get selected scan (returns one string)
RAW=$(
python3 - <<EOF
from download_with_session_ID import find_selected_scan_id
print(find_selected_scan_id("${SESSION_ID}"))
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
export SESSION_ID SCAN_ID OUTPATH

# 5️⃣ Run Python to get largest & newest CSV from ICH_PHE_QUANTIFICATION
python3 - <<'PY'
import os, json
from download_with_session_ID import get_largest_newest_csv_for_scan, download_xnat_file_to_path

session_id = os.environ["SESSION_ID"]
scan_id = os.environ["SCAN_ID"]
out_path = os.environ["OUTPATH"]

info = get_largest_newest_csv_for_scan(session_id, scan_id)
download_xnat_file_to_path(info["uri"], out_path)

print(json.dumps({
    "saved": out_path,
    "name": info["name"],
    "size": info["size"],
    "created": str(info["created"])
}, indent=2, ensure_ascii=False))
PY
##########################


##!/bin/bash
#
## ==============================
## Usage: ./get_selected_scan.sh XNAT_SESSION_ID
## ==============================
#
## 1. Take session ID from command line
#SESSION_ID="$1"
#
## 2. Run the Python function and capture its output
##SESSION_ID="$1"
#
## 1) Call the Python function (returns one string)
#RAW=$(
#python3 - <<EOF
#from download_with_session_ID import find_selected_scan_id
#print(find_selected_scan_id("${SESSION_ID}"))
#EOF
#)
#
## 2) Parse the string -> SCAN_ID and SCAN_NAME
##    Format: "SCAN_ID"::<id>::"SCAN_NAME"::<name>
#SCAN_ID=$(awk -F'::' '{gsub(/"/,"",$2); print $2}' <<< "$RAW")
#SCAN_NAME=$(awk -F'::' '{gsub(/^"/,"",$4); gsub(/"$/,"",$4); print $4}' <<< "$RAW")
#
## 3) Use them
#echo "Selected scan ID:   $SCAN_ID"
#echo "Selected scan name: $SCAN_NAME"
#
## 4. Print nicely or use them downstream
#echo "Selected scan ID:   $SCAN_ID"
#echo "Selected scan name: $SCAN_NAME"
#
##!/bin/bash
## save as: fetch_best_csv.sh
## Usage: ./fetch_best_csv.sh XNAT_SESSION_ID SCAN_ID /path/to/save.csv
#
## SESSION_ID="$1"
## SCAN_ID="$2"
#OUTPATH="/workingoutput"
#
## 2. Run Python to get largest & newest CSV from ICH_PHE_QUANTIFICATION
#python3 - <<EOF
#import json
#from download_with_session_ID import get_largest_newest_csv_for_scan, download_xnat_file_to_path
#
#session_id, scan_id, out_path = "${SESSION_ID}", "${SCAN_ID}", "${OUTPATH}"
#info = get_largest_newest_csv_for_scan(session_id, scan_id)
#download_xnat_file_to_path(info["uri"], out_path)
#print(json.dumps({
#    "saved": out_path,
#    "name": info["name"],
#    "size": info["size"],
#    "created": str(info["created"])
#}, ensure_ascii=False, indent=2))
#EOF
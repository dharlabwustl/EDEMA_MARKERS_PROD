#!/bin/bash
# =====================================================
# Usage:
#   ./audit_project_cleanup.sh PROJECT_ID
#
# Example:
#   ./audit_project_cleanup.sh BJH_ICH
#
# This script:
#   1️⃣ Gets project size before cleanup
#   2️⃣ Exports experiment list to CSV
#   3️⃣ Runs batch cleanup
#   4️⃣ Gets project size after cleanup
#   5️⃣ Writes an audit CSV (with before/after sizes)
#   6️⃣ Uploads the audit CSV to XNAT project resource "AUDIT_REPORTS"
# =====================================================

set -euo pipefail

PROJECT_ID="$1"
TODAY=$(date +%Y%m%d_%H%M%S)
WORKDIR="/workingoutput"

EXPERIMENT_CSV="${WORKDIR}/${PROJECT_ID}_experiments.csv"
CLEANUP_REPORT="${WORKDIR}/${PROJECT_ID}_cleanup_report.csv"
AUDIT_FILE="${WORKDIR}/audit_${TODAY}.csv"

echo "[INFO] Starting cleanup audit for project: ${PROJECT_ID}"
echo "[INFO] Working directory: ${WORKDIR}"
echo "[INFO] Audit file will be: ${AUDIT_FILE}"

# -----------------------------------------------------
# 1️⃣ Measure project size BEFORE cleanup
# -----------------------------------------------------
echo "[STEP] Measuring project size (before cleanup)..."
# Measure project size (before cleanup)
BEFORE=$(python3 - <<EOF
import warnings, json
warnings.filterwarnings("ignore")
from download_with_session_ID import get_project_storage_size
print(json.dumps(get_project_storage_size("${PROJECT_ID}")))
EOF
)
BEFORE_SIZE=$(echo "$BEFORE" | grep -o '{.*}' | python3 -c 'import sys,json; print(json.load(sys.stdin)["size_gb"])')
echo ${BEFORE_SIZE}

# -----------------------------------------------------
# 2️⃣ Export experiments for the project
# -----------------------------------------------------
echo "[STEP] Exporting experiment list to: ${EXPERIMENT_CSV}"
python3 - <<EOF
from download_with_session_ID import export_project_experiments_to_csv
export_project_experiments_to_csv("${PROJECT_ID}", "${EXPERIMENT_CSV}")
EOF

# -----------------------------------------------------
# 3️⃣ Run batch cleanup
# -----------------------------------------------------
echo "[STEP] Running batch cleanup..."
python3 - "$EXPERIMENT_CSV" "$CLEANUP_REPORT" <<'PY'
import sys
from download_with_session_ID import batch_cleanup_from_experiment_csv
csv_path, report_path = sys.argv[1], sys.argv[2]
batch_cleanup_from_experiment_csv(csv_path, report_path)
PY

# -----------------------------------------------------
# 4️⃣ Measure project size AFTER cleanup
# -----------------------------------------------------
echo "[STEP] Measuring project size (after cleanup)..."
# Measure project size (after cleanup)
AFTER=$(python3 - <<EOF
import warnings, json
warnings.filterwarnings("ignore")
from download_with_session_ID import get_project_storage_size
print(json.dumps(get_project_storage_size("${PROJECT_ID}")))
EOF
)
AFTER_SIZE=$(echo "$AFTER" | grep -o '{.*}' | python3 -c 'import sys,json; print(json.load(sys.stdin)["size_gb"])')


# -----------------------------------------------------
# 5️⃣ Compute difference and write audit CSV
# -----------------------------------------------------
FREED=$(python3 -c "print(round(${BEFORE_SIZE} - ${AFTER_SIZE}, 2))")
echo "Project_ID,Date,Size_Before_GB,Size_After_GB,Freed_GB" > "$AUDIT_FILE"
echo "${PROJECT_ID},${TODAY},${BEFORE_SIZE},${AFTER_SIZE},${FREED}" >> "$AUDIT_FILE"

echo "[INFO] Audit CSV written to: ${AUDIT_FILE}"
cat "$AUDIT_FILE"

# -----------------------------------------------------
# 6️⃣ Upload audit file to XNAT project resources
# -----------------------------------------------------
echo "[STEP] Uploading audit CSV to XNAT project resources..."
#PROJECT_ID="$1"
FILE_PATH="$AUDIT_FILE"

python3 - <<EOF
from download_with_session_ID import upload_project_file_to_xnat
upload_project_file_to_xnat("${PROJECT_ID}", "${FILE_PATH}", resource_name="AUDIT_REPORTS")
EOF
echo "[✅] Audit complete and uploaded to XNAT project ${PROJECT_ID}."

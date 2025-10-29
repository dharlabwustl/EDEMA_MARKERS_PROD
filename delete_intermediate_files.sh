#!/bin/bash
PROJECT="$1"

echo "Checking project size before cleanup..."
BEFORE=$(python3 - <<EOF
from download_with_session_ID import get_project_storage_size
import json
print(json.dumps(get_project_storage_size("${PROJECT}")))
EOF
)

echo "Size before cleanup: $BEFORE"

## --- Run your cleanup ---
#./batch_cleanup_from_csv.sh /workingoutput/${PROJECT}_experiments.csv /workingoutput/${PROJECT}_cleanup_report.csv
#
#echo "Checking project size after cleanup..."
#AFTER=$(python3 - <<EOF
#from download_with_session_ID import get_project_storage_size
#import json
#print(json.dumps(get_project_storage_size("${PROJECT}")))
#EOF
#)
#
#echo "Size after cleanup: $AFTER"


#echo ${1}
##!/bin/bash
## Usage: ./export_experiments.sh PROJECT_NAME OUTPUT_CSV
#output_dir=/workingoutput
#PROJECT="$1"
#OUTCSV="${output_dir}/${1}_experiments.csv"
#
#python3 - <<EOF
#from download_with_session_ID import export_project_experiments_to_csv
#export_project_experiments_to_csv("${PROJECT}", "${OUTCSV}")
#EOF
#
#
#
#set -euo pipefail
#
#CSV_PATH="${OUTCSV}"
#REPORT_PATH="${PROJECT}_cleanup_report.csv"   # default name if not given
#
#echo "[INFO] Running batch cleanup on: $CSV_PATH"
#echo "[INFO] Report will be saved as:  $REPORT_PATH"
#
#python3 - "$CSV_PATH" "$REPORT_PATH" <<'PY'
#import sys
#from download_with_session_ID import batch_cleanup_from_experiment_csv
#
#csv_path, report_path = sys.argv[1], sys.argv[2]
#batch_cleanup_from_experiment_csv(csv_path, report_path)
#PY
#
#

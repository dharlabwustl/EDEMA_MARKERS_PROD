echo ${1}
#!/bin/bash
# Usage: ./export_experiments.sh PROJECT_NAME OUTPUT_CSV

PROJECT="$1"
OUTCSV="${1}_experiments.csv"

python3 - <<EOF
from download_with_session_ID import export_project_experiments_to_csv
export_project_experiments_to_csv("${PROJECT}", "${OUTCSV}")
EOF

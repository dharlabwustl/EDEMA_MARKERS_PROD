PROJECT_ID="COLI"
OUTPUT_CSV="/output/${PROJECT_ID}_sessions.csv"

python3 -c '
import sys
from download_with_session_ID_xnat import get_metadata_project_sessionlist

get_metadata_project_sessionlist(
    project_ID=sys.argv[1],
    outputfile=sys.argv[2]
)
' "$PROJECT_ID" "$OUTPUT_CSV"
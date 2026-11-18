#!/bin/bash
set -euo pipefail

if [[ $# -ne 4 ]]; then
    echo "Usage: $0 PROJECT_ID XNAT_USER XNAT_PASS XNAT_HOST" >&2
    exit 2
fi

export XNAT_USER="$2" XNAT_PASS="$3" XNAT_HOST="$4"
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$script_dir/SNIPR_ANALYTICS_STEP1_noxml.py" "$1"

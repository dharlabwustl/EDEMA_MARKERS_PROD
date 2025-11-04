#!/bin/bash

# Usage: ./run_function.sh <function_name> <arg1>

# Example:
# ./run_function.sh given_project_download_experimentslist PROJ123

FUNC_NAME='given_project_download_experimentslist'
ARG1=ICH

if [ -z "$FUNC_NAME" ] || [ -z "$ARG1" ]; then
  echo "Usage: $0 <function_name> <argument>"
  exit 1
fi

python3 - <<EOF
import sys
from download_files_with_given_proj_partialsessionlabel_ext_1 import *

func_name = "$FUNC_NAME"
arg1 = "$ARG1"

if func_name in globals():
    result = globals()[func_name](arg1)
    print(f"✅ Function '{func_name}' returned:", result)
else:
    print(f"❌ Function '{func_name}' not found.")
EOF

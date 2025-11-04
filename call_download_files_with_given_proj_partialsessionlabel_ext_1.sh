#!/bin/bash

# Usage: ./run_function.sh <function_name> <arg1>

# Example:
# ./run_function.sh given_project_download_experimentslist PROJ123

FUNC_NAME='given_session_id_download_file_with_extension' #'given_experiment_find_selected_scan'
#ARGS="SNIPR12_E00443::ICH_PHE_QUANTIFICATION::pdf"
#ARG1=SNIPR12_E00443 #ICH
#ARG2=ICH_PHE_QUANTIFICATION
#ARG3=pdf
ARGS="SNIPR12_E00443::ICH_PHE_QUANTIFICATION::pdf"

# Split by '::' into array
IFS='::' read -r ARG1 ARG2 ARG3 <<< "$ARGS"
if [ -z "$FUNC_NAME" ] || [ -z "$ARG1" ]; then
  echo "Usage: $0 <function_name> <argument>"
  exit 1
fi

python3 - <<EOF
import sys
from download_files_with_given_proj_partialsessionlabel_ext_1 import *

func_name = "$FUNC_NAME"
arg1 = "$ARG1"
arg2= "$ARG2"
arg3= "$ARG3"

if func_name in globals():
    result = globals()[func_name](arg1,arg2,arg3)
    print(f"✅ Function '{func_name}' returned:", result)
else:
    print(f"❌ Function '{func_name}' not found.")
EOF

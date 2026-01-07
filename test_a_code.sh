#!/usr/bin/env bash
ID_VALUE=$(
python3 -c "from utilities_using_xnat_python import log_error; print(log_error('${SESSION_ID}'))"
)


echo "NIFTI_LOCATION ID = ${ID_VALUE}"

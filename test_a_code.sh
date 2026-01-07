#!/usr/bin/env bash
SESSION_ID=${1}
#ID_VALUE=$(
#python3 -c "from utilities_using_xnat_python import log_error; print(log_error('${SESSION_ID}'))"
#)

python3 -c "from utilities_using_xnat_python import log_error; log_error('TEST MESSAGE'); print('done')"
ls -l error.txt
cat error.txt

echo "NIFTI_LOCATION ID = ${ID_VALUE}"

#!/usr/bin/env bash
SESSION_ID=${1}
#ID_VALUE=$(
#python3 -c "from utilities_using_xnat_python import log_error; print(log_error('${SESSION_ID}'))"
#)

#python3 -c "from utilities_using_xnat_python import log_error; log_error('TEST MESSAGE','NO_FUNC'); print('done')"
#python3 -c "from utilities_using_xnat_python import get_id_from_nifti_location_csv; get_id_from_nifti_location_csv('${SESSION_ID}'); print('done')"
ID_VALUE=$(
python3 -c "from utilities_using_xnat_python import get_id_from_nifti_location_csv; print(get_id_from_nifti_location_csv('${SESSION_ID}'))"
)

RESOURCE_DIR="EDEMA_BIOMARKER"
EXT='.pdf'
LATEST_URI=$(
python3 -c "from utilities_using_xnat_python import get_latest_file_uri_from_scan_resource; \
print(get_latest_file_uri_from_scan_resource('${SESSION_ID}','${ID_VALUE}','${RESOURCE_DIR}','${EXT}'))"
)
echo "$LATEST_URI"


ls -l error.txt
realpath error.txt
cat error.txt

echo "NIFTI_LOCATION ID = ${ID_VALUE}"

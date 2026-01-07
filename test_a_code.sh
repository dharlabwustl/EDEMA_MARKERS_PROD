#!/usr/bin/env bash
ID_VALUE=$(
python3 -c "from utilities_using_xnat_python import get_id_from_nifti_location_csv; print(get_id_from_nifti_location_csv('${SESSION_ID}'))"
)


echo "NIFTI_LOCATION ID = ${ID_VALUE}"

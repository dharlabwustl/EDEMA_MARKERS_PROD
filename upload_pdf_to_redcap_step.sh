#!/usr/bin/env bash
SESSION_ID=${1}
echo "REDCAP_API::REDCAP_API::${REDCAP_API}::${SESSION_ID}"
#exit
#ID_VALUE=$(
#python3 -c "from utilities_using_xnat_python import log_error; print(log_error('${SESSION_ID}'))"
#)

#python3 -c "from utilities_using_xnat_python import log_error; log_error('TEST MESSAGE','NO_FUNC'); print('done')"
#python3 -c "from utilities_using_xnat_python import get_id_from_nifti_location_csv; get_id_from_nifti_location_csv('${SESSION_ID}'); print('done')"
ID_VALUE=${2}

#$(
#python3 -c "from utilities_using_xnat_python import get_id_from_nifti_location_csv; print(get_id_from_nifti_location_csv('${SESSION_ID}'))"
#)

#RESOURCE_DIR="EDEMA_BIOMARKER"
#EXT='.pdf'
#LATEST_URI=$(
#python3 -c "from utilities_using_xnat_python import get_latest_file_uri_from_scan_resource; \
#print(get_latest_file_uri_from_scan_resource('${SESSION_ID}','${ID_VALUE}','${RESOURCE_DIR}','${EXT}'))"
#)
#echo "$LATEST_URI"
#filename=$(basename ${LATEST_URI})

ls -l error.txt
realpath error.txt
cat error.txt

echo "NIFTI_LOCATION ID = ${ID_VALUE}"
#OUT_PATH=$(
#python3 -c "from utilities_using_xnat_python import download_file_from_xnat_uri; \
#print(download_file_from_xnat_uri('$LATEST_URI','/workingoutput/${filename}'))"
#)
OUT_PATH=${3}
echo "$OUT_PATH"
read PROJECT_ID SUBJECT_ID <<< $(
python3 -c "
from utilities_using_xnat_python import given_sessionid_get_project_n_subjectids
p, s = given_sessionid_get_project_n_subjectids('${SESSION_ID}')
if p is not None and s is not None:
    print(p, s)
"
)

echo "PROJECT_ID::$PROJECT_ID"
echo "SUBJECT_LABEL::$SUBJECT_ID"
SUBJECT_LABEL=$SUBJECT_ID
SESSION_LABEL=$(
python3 -c "from utilities_using_xnat_python import get_session_label_from_session_id; \
print(get_session_label_from_session_id('${SESSION_ID}'))"
)
echo "PROJECT_ID::$PROJECT_ID"
echo "SUBJECT_LABEL::${SUBJECT_LABEL}"
echo "SESSION_LABEL::${SESSION_LABEL}"
echo "OUT_PATH::${OUT_PATH}"
#fill_redcap_for_selected_scan_arguments=('fill_redcap_for_pdffile_given_subject_label' ${xml_filename} ${pdffilename}) #${subj_listfile})
#outputfiles_present=$(python3 download_with_session_ID.py "${fill_redcap_for_selected_scan_arguments[@]}")
#subject_name,session_label,project_name,file_name
SUCCESS_VALUE_0_FAIL_1=$(
python3 -c "from download_with_session_ID import fill_redcap_for_pdffile_given_subject_label; print(fill_redcap_for_pdffile_given_subject_label('${SUBJECT_LABEL}','${SESSION_LABEL}','${PROJECT_ID}','${OUT_PATH}'))"
)

echo SUCCESS_VALUE_0_FAIL_1="${SUCCESS_VALUE_0_FAIL_1}"
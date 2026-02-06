#!/usr/bin/env bash
export XNAT_USER=${2} 
export XNAT_PASS=${3} 
export XNAT_HOST=${4} #"https://snipr-dev-test1.nrg.wustl.edu"
python3 /software/dicom2nifiti_sessionlevel_selected.py  ${1}

python3 -c "from utilities_using_xnat_python import create_new_sessionlist_table_in_railway_with_session_id; create_new_sessionlist_table_in_railway_with_session_id('${1}')"
python3 -c "from utilities_using_xnat_python import fill_after_dicom2nifti; fill_after_dicom2nifti('${1}')"



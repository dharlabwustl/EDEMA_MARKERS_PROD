#!/usr/bin/env bash
export XNAT_USER=${2}
export XNAT_PASS=${3}
export XNAT_HOST=${4} #"https://snipr-dev-test1.nrg.wustl.edu"
#export REDCAP_HOST=${5}  #'https://redcap.wustl.edu/redcap/api/' #
#export REDCAP_API=${5} #'EC6A2206FF8C1D87D4035E61C99290FF' #
sessionID=${1}
python3 -c "from dicom2nifti_20260206 import run_dicom2nifti_for_session; run_dicom2nifti_for_session('${1}')"
python3 -c "from utilities_using_xnat_python import fill_after_dicom2nifti; fill_after_dicom2nifti('${1}')"
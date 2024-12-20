#!/usr/bin/env bash
export XNAT_USER=${2} 
export XNAT_PASS=${3} 
export XNAT_HOST=${4} #"https://snipr-dev-test1.nrg.wustl.edu"
python3 /software/dicom2niftiDec202024.py  ${1}



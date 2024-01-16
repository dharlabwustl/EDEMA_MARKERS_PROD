#!/bin/bash
PROJECT_ID=${1}
XNAT_USER=${2}
XNAT_PASS=${3}
XNAT_HOST=${4}
redcap_token=${REDCAP_API_TOKEN}
redcap_url='https://redcap.wustl.edu/redcap/api/'
python3 redcapapi.py ${redcap_token} ${redcap_url}
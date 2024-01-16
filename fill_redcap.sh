#!/bin/bash
PROJECT_ID=${1}
XNAT_USER=${2}
XNAT_PASS=${3}
XNAT_HOST_TOKEN='https://snipr.wustl.edu/'"::::"'https://redcap.wustl.edu/redcap/api/'"::::EC6A2206FF8C1D87D4035E61C99290FF" ###${4}
IFS='::::' read -ra ADDR <<< "${XNAT_HOST_TOKEN}"
XNAT_HOST=${ADDR[0]}
redcap_token=${ADDR[2]}
redcap_url=${ADDR[1]} #'https://redcap.wustl.edu/redcap/api/'
python3 redcapapi.py ${redcap_token} ${redcap_url}
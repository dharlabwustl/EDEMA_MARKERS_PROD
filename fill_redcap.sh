#!/bin/bash
PROJECT_ID=${1}
export XNAT_USER=${2}
export XNAT_PASS=${3}
export XNAT_HOST=${4}
XNAT_HOST_TOKEN='https://snipr.wustl.edu/::::https://redcap.wustl.edu/redcap/api/::::EC6A2206FF8C1D87D4035E61C99290FF' ###${4}
IFS='::::' read -ra ADDR <<< "${XNAT_HOST_TOKEN}"
redcap_token='EC6A2206FF8C1D87D4035E61C99290FF' #${ADDR[2]}
redcap_url='https://redcap.wustl.edu/redcap/api/' #${ADDR[1]} #'https://redcap.wustl.edu/redcap/api/'
echo '${redcap_token} ${redcap_url}'::"${redcap_token} ${redcap_url}"
#python3 /software/redcapapi.py ${redcap_token} ${redcap_url} ${PROJECT_ID}
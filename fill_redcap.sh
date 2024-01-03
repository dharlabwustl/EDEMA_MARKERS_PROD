#!/bin/bash
redcap_token=${REDCAP_API_TOKEN}
redcap_url='https://redcap.wustl.edu/redcap/api/'
python3 redcapapi.py ${redcap_token} ${redcap_url}
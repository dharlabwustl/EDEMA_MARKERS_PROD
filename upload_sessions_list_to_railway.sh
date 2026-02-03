#!/bin/bash

project_id="COLI"
python3 -c "from utilities_using_xnat_python import create_new_sessionlist_table_in_railway; create_new_sessionlist_table_in_railway('${project_id}')"

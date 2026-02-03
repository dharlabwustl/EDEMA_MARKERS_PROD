#!/bin/bash

for x in "COLI","BM" ; ##,"SAH","ICH","Krakow","BJH","WashU")
do
project_id=$x ##"SAH"
python3 -c "from utilities_using_xnat_python import create_new_sessionlist_table_in_railway; create_new_sessionlist_table_in_railway('${project_id}')"
echo "TABLE SEARCH DONE"
done
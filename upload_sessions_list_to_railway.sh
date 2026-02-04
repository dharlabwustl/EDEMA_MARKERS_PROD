#!/bin/bash

for x in SNIPR12_E00664 ;  #"COLI" "BM" ; ##,"SAH","ICH","Krakow","BJH","WashU")
do
project_id=$x ##"SAH"
python3 -c "from utilities_using_xnat_python import count_z_axial_scans_in_session; count_z_axial_scans_in_session('${project_id}')"
#python3 -c "from utilities_using_xnat_python import create_new_sessionlist_table_in_railway; create_new_sessionlist_table_in_railway('${project_id}')"
#count_z_axial_scans_in_session
echo "TABLE SEARCH DONE"
done
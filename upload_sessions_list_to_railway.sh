#!/bin/bash

for x in SNIPR01_E00001; #SNIPR02_E01687 SNIPR02_E02550 ;  #"COLI" "BM" ; ##,"SAH","ICH","Krakow","BJH","WashU")
do
project_id=$x ##"SAH"
python3 -c "from utilities_using_xnat_python import fill_after_dicom2nifti; fill_after_dicom2nifti('${project_id}')"
#python3 -c "from utilities_using_xnat_python import create_new_sessionlist_table_in_railway; create_new_sessionlist_table_in_railway('${project_id}')"
#count_z_axial_scans_in_session
echo "TABLE SEARCH DONE"
done
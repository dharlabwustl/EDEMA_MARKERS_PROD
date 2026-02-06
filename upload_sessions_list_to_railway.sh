#!/bin/bash

railway_fill='fill_after_dicom2nifti'
for x in "COLI" "BM"  "WashU"; ##,"SAH","ICH","Krakow","BJH","WashU") SNIPR02_E01687; ##SNIPR01_E00001; #SNIPR02_E01687 SNIPR02_E02550 ;  #
do
project_id=$x ##"SAH"
if [[ ${railway_fill} == 'fill_after_dicom2nifti' ]] ; then
#python3 -c "from utilities_using_xnat_python import fill_after_dicom2nifti; fill_after_dicom2nifti('${project_id}')"
python3 -c "from utilities_using_xnat_python import create_new_sessionlist_table_in_railway; create_new_sessionlist_table_in_railway('${project_id}')"
#count_z_axial_scans_in_session
echo "TABLE SEARCH DONE"
fi
done
XNAT_USER="atulkumar"
XNAT_PASS='Mrityor1!'
XNAT_HOST='https://snipr.wustl.edu'
SESSION_IDS=(SNIPR01_E00147 SNIPR01_E00146 SNIPR01_E00193 SNIPR02_E02970 SNIPR02_E09071 SNIPR01_E00231 )
resource_dir='PREPROCESS_SEGM_4'  ###NIFTI'
file_extension='_fixed_COLIHM620406202215542_lin1_BET.nii.gz' #'_brain_f.nii.gz'
for session_id in "${SESSION_IDS[@]}" ; do

#session_count=113 #'mgb_test.csv' #Missing_PDFs_for_RIS_Atul_1.csv' #test1.csv' ## 'Missing_PDF_MGBBMC.csv' ##must have session name column as 'name'. No space in file name.
./download_singlefile_with_session_id.sh $XNAT_USER $XNAT_PASS ${XNAT_HOST} ${session_id}   ${resource_dir} ${file_extension}
done

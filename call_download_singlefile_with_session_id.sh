session_id=${1}
resource_dir=${2} #'PREPROCESS_SEGM_4'  ###NIFTI'
file_extension=${3} ##'_fixed_COLIHM620406202215542_lin1_BET.nii.gz' #'_brain_f.nii.gz'
echo "./download_singlefile_with_session_id.sh $XNAT_USER $XNAT_PASS ${XNAT_HOST} ${session_id}   ${resource_dir} ${file_extension}"

/software/download_singlefile_with_session_id.sh $XNAT_USER $XNAT_PASS ${XNAT_HOST} ${session_id}   ${resource_dir} ${file_extension}

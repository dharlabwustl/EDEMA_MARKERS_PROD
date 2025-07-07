source ./bash_utilities.sh
sessionID=${1}
echo ${sessionID}
##get the selected scan id
scanID=$(get_scan_id ${sessionID})
echo ${scanID}
echo ${sessionID}::${scanID}
snipr_output_foldername='MASKS'
file_extension='.nii.gz'
outputdir='/workingoutput/'
echo "${sessionID} ${scanID} ${snipr_output_foldername} ${file_extension} ${outputdir} "
function_with_arguments=('call_download_a_file_with_ext' ${sessionID} ${scanID} ${snipr_output_foldername} ${file_extension} ${outputdir} ) ##'warped_1_mov_mri_region_' )
echo "outputfiles_present="'$(python3 download_with_session_ID.py' "${function_with_arguments[@]}"
outputfiles_present=$(python3 download_with_session_ID.py "${function_with_arguments[@]}")
#session_id=${1}
#resource_dir=${2} ####''  ###NIFTI'
#file_extension=${3} ##'_fixed_COLIHM620406202215542_lin1_BET.nii.gz' #'_brain_f.nii.gz'
#echo "./download_singlefile_with_session_id.sh $XNAT_USER $XNAT_PASS ${XNAT_HOST} ${session_id}   ${resource_dir} ${file_extension}"
#/software/download_singlefile_with_session_id.sh $XNAT_USER $XNAT_PASS ${XNAT_HOST} ${session_id}   ${resource_dir} ${file_extension}

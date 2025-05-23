# Session ID given
source ./bash_utilities.sh
working_dir=/workinginput
working_dir_1=/input1
output_directory=/workingoutput
sessionID=${1}
#get the selected scan id
scanID=$(get_scan_id ${sessionID})
echo ${sessionID}::${scanID}
# donwload respective nifti and relevant masks
resource_dir='NIFTI'
download_resource_dir ${sessionID}  ${scanID} ${resource_dir}
resource_dir='MASKS'
download_resource_dir ${sessionID}  ${scanID} ${resource_dir}
# bring masks from yasheng's work to the original nifti reference frame
scan_file_basename=$(basename $(ls ${working_dir}/NIFTI/*.nii))
scan_file_basename_no_ext=${scan_file_basename%.nii*}

original_ct_file=$(ls ${working_dir}/NIFTI/${scan_file_basename_no_ext}.nii)
# brain_half mask
levelset_mask_file=$(ls ${working_dir}/MASKS/left_half_brain_nib_img.nii.gz)
to_original_nifti_rf ${original_ct_file} ${levelset_mask_file} ${output_directory}
mv ${output_directory}/left_half_brain_nib_img.nii.gz ${output_directory}/${scan_file_basename_no_ext}_left_half_brain_nib_img.nii.gz
half_brain_mask=${output_directory}/${scan_file_basename_no_ext}_left_half_brain_nib_img.nii.gz
levelset_mask_file=$(ls ${working_dir}/MASKS/${scan_file_basename_no_ext}_resaved_levelset_bet.nii.gz)
to_original_nifti_rf ${original_ct_file} ${levelset_mask_file} ${output_directory}
bet_mask=${output_directory}/${scan_file_basename_no_ext}_resaved_levelset_bet.nii.gz

## download as zip, then unzip and arrange the directory like that in the SNIPR
#call_download_files_in_a_resource_in_a_session_arguments=('call_dowload_a_folder_as_zip' ${sessionID} ${scanID}  ${resource_dir})
#outputfiles_present=$(python3 download_with_session_ID.py "${call_download_files_in_a_resource_in_a_session_arguments[@]}")
#curl -u "$XNAT_USER:$XNAT_PASS" -X GET \
#  "${XNAT_HOST}/data/experiments/${sessionID}/scans/${scanID}/resources/${resource_dir}/files?format=zip" \
#  -o "${working_dir}/${sessionID}_${scanID}_${resource_dir}.zip"
#
#echo "curl -u $XNAT_USER:$XNAT_PASS -X GET $XNAT_HOST/data/experiments/${sessionID}/scans/${scanID}/resources/${resource_dir}/files?format=zip > ${sessionID}_${scanID}_${resource_dir}.zip"
# resample the masks to the original nifti

# use transformation matrix to register all of them to the template (rigid registration)
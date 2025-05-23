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
resource_dir='EDEMA_BIOMARKER'
download_resource_dir ${sessionID}  ${scanID} ${resource_dir}
# bring masks from yasheng's work to the original nifti reference frame
scan_file_basename=$(basename $(ls ${working_dir}/NIFTI/*.nii))
scan_file_basename_no_ext=${scan_file_basename%.nii*}

original_ct_file=$(ls ${working_dir}/NIFTI/${scan_file_basename_no_ext}.nii)
# brain_half mask
levelset_mask_file=$(ls ${working_dir}/MASKS/left_half_brain_nib_img.nii.gz)
full_string=$(to_original_nifti_rf ${original_ct_file} ${levelset_mask_file} ${output_directory})
half_brain_mask=$(echo "$full_string" | awk -F'_parsehere_' '{print $2}' | xargs)
echo half_brain_mask::${half_brain_mask}
mv ${half_brain_mask} ${output_directory}/${scan_file_basename_no_ext}_left_half_brain_nib_img.nii.gz
half_brain_mask=${output_directory}/${scan_file_basename_no_ext}_left_half_brain_nib_img.nii.gz
#
levelset_mask_file=$(ls ${working_dir}/MASKS/${scan_file_basename_no_ext}_resaved_levelset_bet.nii.gz)
full_string=$(to_original_nifti_rf ${original_ct_file} ${levelset_mask_file} ${output_directory})
bet_mask=$(echo "$full_string" | awk -F'_parsehere_' '{print $2}' | xargs)
echo bet_mask::${bet_mask}

## make bet of the gray image:
#levelset_mask_file=$(ls ${working_dir}/MASKS/${scan_file_basename_no_ext}_resaved_levelset_bet.nii.gz)
full_string=$(to_betgray_given_gray_n_binary ${original_ct_file} ${bet_mask} ${output_directory})
bet_gray=$(echo "$full_string" | awk -F'_parsehere_' '{print $2}' | xargs)
echo bet_gray::${bet_gray}
### apply transform matrix to align to the template image:
transform_mat_file=$(ls ${working_dir}/EDEMA_BIOMARKER/${scan_file_basename_no_ext}_resaved_levelset_brain_f_scct_strippedResampled1lin1.mat)
echo "transform_files_with_given_mat_wrt_sccttemplate ${bet_gray} ${bet_gray%.nii*}_RF_scct.nii.gz ${transform_mat_file}"
transform_files_with_given_mat_wrt_sccttemplate ${bet_gray} ${bet_gray%.nii*}_RF_scct.nii.gz ${transform_mat_file}
transform_files_with_given_mat_wrt_sccttemplate ${half_brain_mask} ${half_brain_mask%.nii*}_RF_scct.nii.gz ${transform_mat_file}
snipr_output_foldername='HEMISPHERE_MASK'
substring='nii'
delete_a_file ${sessionID}  ${scanID} ${snipr_output_foldername} ${substring}
uploadsinglefile ${sessionID} ${scanID} $(dirname ${bet_gray%.nii*}_RF_scct.nii.gz) ${snipr_output_foldername} $(basename  ${bet_gray%.nii*}_RF_scct.nii.gz)
uploadsinglefile ${sessionID} ${scanID} $(dirname ${half_brain_mask%.nii*}_RF_scct.nii.gz) ${snipr_output_foldername} $(basename  ${half_brain_mask%.nii*}_RF_scct.nii.gz)


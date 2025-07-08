source ./bash_utilities.sh
sessionID=${1}
#echo ${sessionID}
##get the selected scan id
scanID=$(get_scan_id ${sessionID})
#echo ${scanID}
#echo ${sessionID}::${scanID}
# download nifti original
snipr_output_foldername='NIFTI'
file_extension='.nii'
outputdir='/workinginput/'
echo "download_a_single_file_with_ext sessionID::${sessionID} scanID::${scanID} snipr_output_foldername::${snipr_output_foldername} file_extension::${file_extension} outputdir::${outputdir}  "
download_a_single_file_with_ext "${sessionID} ${scanID} ${snipr_output_foldername} ${file_extension} ${outputdir} "
echo sessionID::${sessionID}
original_ct_file=$(find ${outputdir} -name "*${file_extension}" )
echo ${original_ct_file}
### download ventricle mask
snipr_output_foldername='MASKS'
file_extension='_ventricle_total.nii.gz'
outputdir='/workinginput/'
echo "download_a_single_file_with_ext sessionID::${sessionID} scanID::${scanID} snipr_output_foldername::${snipr_output_foldername} file_extension::${file_extension} outputdir::${outputdir}  "
download_a_single_file_with_ext "${sessionID} ${scanID} ${snipr_output_foldername} ${file_extension} ${outputdir} "
levelset_ventricle_mask_file=$(find ${outputdir} -name *${file_extension})


output_directory='/workingoutput/'
to_original_nifti_rf ${original_ct_file} ${levelset_ventricle_mask_file} ${output_directory}
levelset_ventricle_mask_file_orf=${output_directory}$(basename ${levelset_ventricle_mask_file})

snipr_output_foldername='PREPROCESS_SEGM_3'
file_extension='_brain_f.nii.gz'
outputdir='/workinginput/'
echo "download_a_single_file_with_ext sessionID::${sessionID} scanID::${scanID} snipr_output_foldername::${snipr_output_foldername} file_extension::${file_extension} outputdir::${outputdir}  "
download_a_single_file_with_ext "${sessionID} ${scanID} ${snipr_output_foldername} ${file_extension} ${outputdir} "
bet_gray_file=$(find ${outputdir} -name *${file_extension})

snipr_output_foldername='EDEMA_BIOMARKER'
file_extension='_resaved_levelset_brain_f_scct_strippedResampled1lin1.mat'
outputdir='/workinginput/'
echo "download_a_single_file_with_ext sessionID::${sessionID} scanID::${scanID} snipr_output_foldername::${snipr_output_foldername} file_extension::${file_extension} outputdir::${outputdir}  "
download_a_single_file_with_ext "${sessionID} ${scanID} ${snipr_output_foldername} ${file_extension} ${outputdir} "
mat_file_session_ct_is_moving=$(find ${outputdir} -name *${file_extension})
## transform gray_bet to scct template
transformed_output_file=/workingoutput/mov_$(basename ${bet_gray_file})
echo "original_ct_file::${original_ct_file}  levelset_ventricle_mask_file_orf::${levelset_ventricle_mask_file_orf}" bet_gray_file::${bet_gray_file} mat_file_session_ct_is_moving::${mat_file_session_ct_is_moving} transformed_output_file::${transformed_output_file}


#transform_mat_file=/workinginput/$(basename ${original_ct_file%.nii*})_resaved_levelset_brain_f_scct_strippedResampled1lin1.mat
transform_files_with_given_mat_wrt_sccttemplate ${bet_gray_file} ${transformed_output_file} ${mat_file_session_ct_is_moving}
#  local moving_img=${1}
#  local transformed_output_file=${2}
#  local transform_mat_file=${3}

## download BET gray file:
#  local original_ct_file=${1}
#  local levelset_infarct_mask_file=${2}
#  local output_directory=${3}

#function_with_arguments=('call_download_a_file_with_ext' ${sessionID} ${scanID} ${snipr_output_foldername} ${file_extension} ${outputdir} ) ##'warped_1_mov_mri_region_' )
#echo "outputfiles_present="'$(python3 download_with_session_ID.py' "${function_with_arguments[@]}"
#outputfiles_present=$(python3 download_with_session_ID.py "${function_with_arguments[@]}")
#session_id=${1}
#resource_dir=${2} ####''  ###NIFTI'
#file_extension=${3} ##'_fixed_COLIHM620406202215542_lin1_BET.nii.gz' #'_brain_f.nii.gz'
#echo "./download_singlefile_with_session_id.sh $XNAT_USER $XNAT_PASS ${XNAT_HOST} ${session_id}   ${resource_dir} ${file_extension}"
#/software/download_singlefile_with_session_id.sh $XNAT_USER $XNAT_PASS ${XNAT_HOST} ${session_id}   ${resource_dir} ${file_extension}

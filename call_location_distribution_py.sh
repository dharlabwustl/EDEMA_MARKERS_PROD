#!/bin/bash
export XNAT_USER=${2}
export XNAT_PASS=${3}
export XNAT_HOST=${4}
sessionID=${1}
working_dir=/workinginput
working_dir_1=/input
output_directory=/workingoutput

final_output_directory=/outputinsidedocker


## get the scan used in this session



call_download_files_in_a_resource_in_a_session_arguments=('call_download_files_in_a_resource_in_a_session' ${sessionID} "NIFTI_LOCATION" ${working_dir})
outputfiles_present=$(python3 download_with_session_ID.py "${call_download_files_in_a_resource_in_a_session_arguments[@]}")
echo '$outputfiles_present'::$outputfiles_present
########################################
## donwload the relevant nifti file and masks
for niftifile_csvfilename in ${working_dir}/*NIFTILOCATION.csv; do
whie IFS=',' read -ra array; do
  echo ${array[0]}
  done < <(tail -n +2 "${niftifile_csvfilename}")
done

#rm ${final_output_directory}/*.*
#rm ${output_directory}/*.*
#outputfiles_present=0
#echo $niftifile_csvfilename
#while IFS=',' read -ra array; do
#scanID=${array[2]}
#echo sessionId::${sessionID}
#echo scanId::${scanID}
#snipr_output_foldername="PREPROCESS_SEGM_2"
#function_with_arguments=('call_delete_file_with_ext' ${sessionID} ${scanID} ${snipr_output_foldername} 'cistern_area' ) ##'warped_1_mov_mri_region_' )
#echo "outputfiles_present="'$(python3 utilities_simple_trimmed.py' "${function_with_arguments[@]}"
#outputfiles_present=$(python3 download_with_session_ID.py "${function_with_arguments[@]}")
#snipr_output_foldername="PREPROCESS_SEGM_2"
#### check if the file exists:
#call_check_if_a_file_exist_in_snipr_arguments=('call_check_if_a_file_exist_in_snipr' ${sessionID} ${scanID} ${snipr_output_foldername} .pdf .csv)
#outputfiles_present=$(python3 download_with_session_ID.py "${call_check_if_a_file_exist_in_snipr_arguments[@]}")
#
#################################################
##    outputfiles_present=0
#echo "outputfiles_present:: "${outputfiles_present: -1}"::outputfiles_present"
##echo "outputfiles_present::ATUL${outputfiles_present}::outputfiles_present"
#if [[ "${outputfiles_present: -1}" -eq 1 ]]; then
#echo " I AM THE ONE"
#fi
#if  [[ "${outputfiles_present: -1}" -eq 0 ]]; then ## [[ 1 -gt 0 ]]  ; then #
#
#echo "outputfiles_present:: "${outputfiles_present: -1}"::outputfiles_present"
### GET THE SESSION CT image
#copy_scan_data ${niftifile_csvfilename} ${working_dir_1} #${working_dir}
#nifti_file_without_ext=$(basename $(ls ${working_dir_1}/*.nii))
#nifti_file_without_ext=${nifti_file_without_ext%.nii*}
###############################################################################################################
#
### GET THE RESPECTIVS MASKS NIFTI FILE NAME AND COPY IT TO THE WORKING_DIR
#
######################################################################################
#resource_dirname='MASKS'
#output_dirname=${working_dir}
#while IFS=',' read -ra array; do
#scanID=${array[2]}
#echo sessionId::${sessionID}
#echo scanId::${scanID}
#done < <(tail -n +2 "${niftifile_csvfilename}")
#echo working_dir::${working_dir}
#echo output_dirname::${output_dirname}
#copy_masks_data ${sessionID} ${scanID} ${resource_dirname} ${output_dirname}
#resource_dirname='PREPROCESS_SEGM_2'
#copy_masks_data ${sessionID} ${scanID} ${resource_dirname} ${output_dirname}
#resource_dirname='EDEMA_BIOMARKER'
#copy_masks_data ${sessionID} ${scanID} ${resource_dirname} ${output_dirname}
#
####################### BY NOW WE HAVE EVERYTHIN WE NEED #############
### RELEVANT FILES ARE : SESSION CT, TEMPLATE CT, TEMPLATE MASKS, BET MASK FROM YASHENG to  MAKE BET GRAY OF SESSION CT
### and the mat files especially the Inv.mat file let us keep the sensible names from here:
#session_ct=$( ls ${working_dir_1}/*'.nii' )
#session_ct_bname_noext=$(basename ${session_ct})
#session_ct_bname_noext=${session_ct_bname_noext%.nii*}
##fixed_image_filename='/software/COLIHM620406202215542.nii.gz'  ####${template_prefix}.nii.gz'
##infarct_mask_from_yasheng=$(ls ${working_dir}/${nifti_file_without_ext}*_resaved_infarct_auto_removesmall.nii.gz)
##      template_masks_dir='/software/mritemplate/NONLINREGTOCT/' 	COLI_HM62_04062022_1554_2_resaved_csf_unet.nii.gz
#bet_mask_from_yasheng=$(ls ${working_dir}/${nifti_file_without_ext}*_resaved_levelset_bet.nii.gz)
##csf_mask_from_yasheng=$(ls ${working_dir}/${nifti_file_without_ext}*_resaved_csf_unet.nii.gz)
##echo "levelset_bet_mask_file:${levelset_bet_mask_file}"
##python3 -c "
##
##import sys ;
##sys.path.append('/software/') ;
##from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${session_ct}" "${infarct_mask_from_yasheng}" "${output_directory}"
#
#python3 -c "
#
#import sys ;
#sys.path.append('/software/') ;
#from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${session_ct}" "${bet_mask_from_yasheng}" "${output_directory}"
#
##python3 -c "
##
##import sys ;
##sys.path.append('/software/') ;
##from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${session_ct}" "${csf_mask_from_yasheng}" "${output_directory}"
#
#
## now let us make bet gray for session ct:
#/software/bet_withlevelset.sh ${session_ct} ${output_directory}/$(basename ${bet_mask_from_yasheng})
#
#
#moving_image_filename=/software/scct_strippedResampled1.nii.gz ###COLIHM620406202215542.nii.gz ##'  ####${template_prefix}.nii.gz ##${session_ct_bet_gray}
###'COLIHM620406202215542'
#fixed_image_filename=${output_directory}/${session_ct_bname_noext}_brain_f.nii.gz
#template_prefix=$(basename ${fixed_image_filename%.nii*})
##/software/linear_rigid_registration_v10162024.sh ${moving_image_filename}  ${fixed_image_filename} ${output_directory}
##session_ct_bet_gray_lin_reg_output=${output_directory}/'mov_'$(basename ${moving_image_filename%.nii*})_fixed_$(basename  ${fixed_image_filename%.nii*})_lin1.nii.gz
##movingimage_gray_registered=${output_directory}/'mov_'$(basename ${moving_image_filename%.nii*})_fixed_$(basename  ${fixed_image_filename%.nii*})_lin1.nii.gz
#
#moving_image_filename=$(basename ${moving_image_filename})
#registration_mat_file=${working_dir}/'mov_'$(basename ${moving_image_filename%.nii*})_fixed_$(basename  ${fixed_image_filename%.nii*})_lin1.mat
#
#registration_nii_file=${working_dir}/'mov_'$(basename ${moving_image_filename%.nii*})_fixed_$(basename  ${fixed_image_filename%.nii*})_lin1.nii.gz
##################################################################################################
#moving_image_filename=/software/scct_strippedResampled1_onlyventricle.nii.gz #${output_directory}/${moving_image_filename} ##%.nii*}resampled_mov.nii.gz
#mask_binary_output_dir='/input'
#snipr_output_foldername="PREPROCESS_SEGM_2"
#
#/software/linear_rigid_registration_onlytrasnformwith_matfile10162024.sh  ${moving_image_filename} ${fixed_image_filename} ${registration_mat_file} ${mask_binary_output_dir}
#mask_binary_output_filename=mov_$(basename ${moving_image_filename%.nii*})_fixed_${template_prefix}_lin1.nii.gz
#threshold=0
#function_with_arguments=('call_gray2binary' ${mask_binary_output_dir}/${mask_binary_output_filename}  ${mask_binary_output_dir} ${threshold})
#echo "outputfiles_present="'$(python3 utilities_simple_trimmed.py' "${function_with_arguments[@]}"
#outputfiles_present=$(python3 utilities_simple_trimmed.py "${function_with_arguments[@]}")
#infarct_mask_binary_output_filename=${mask_binary_output_dir}/${mask_binary_output_filename%.nii*}_BET.nii.gz
#uploadsinglefile ${sessionID} ${scanID} $(dirname ${infarct_mask_binary_output_filename}) ${snipr_output_foldername} $(basename  ${infarct_mask_binary_output_filename})
########################################################################################################
##################################################################################################
#moving_image_filename=/software/midlinecssfResampled1.nii.gz #${output_directory}/${moving_image_filename} ##%.nii*}resampled_mov.nii.gz
#mask_binary_output_dir='/input'
#snipr_output_foldername="PREPROCESS_SEGM_2"
#/software/linear_rigid_registration_onlytrasnformwith_matfile10162024.sh  ${moving_image_filename} ${fixed_image_filename} ${registration_mat_file} ${mask_binary_output_dir}
#mask_binary_output_filename=mov_$(basename ${moving_image_filename%.nii*})_fixed_${template_prefix}_lin1.nii.gz
#threshold=0
#function_with_arguments=('call_gray2binary' ${mask_binary_output_dir}/${mask_binary_output_filename}  ${mask_binary_output_dir} ${threshold})
#echo "outputfiles_present="'$(python3 utilities_simple_trimmed.py' "${function_with_arguments[@]}"
#outputfiles_present=$(python3 utilities_simple_trimmed.py "${function_with_arguments[@]}")
#infarct_mask_binary_output_filename=${mask_binary_output_dir}/${mask_binary_output_filename%.nii*}_BET.nii.gz
#uploadsinglefile ${sessionID} ${scanID} $(dirname ${infarct_mask_binary_output_filename}) ${snipr_output_foldername} $(basename  ${infarct_mask_binary_output_filename})
########################################################################################################
##################################################################################################
#moving_image_filename=/software/cistern_area.nii.gz #${output_directory}/${moving_image_filename} ##%.nii*}resampled_mov.nii.gz
#mask_binary_output_dir='/input'
#snipr_output_foldername="PREPROCESS_SEGM_2"
#function_with_arguments=('call_delete_file_with_ext' ${sessionID} ${scanID} ${snipr_output_foldername} 'cistern_area' ) ##'warped_1_mov_mri_region_' )
#echo "outputfiles_present="'$(python3 utilities_simple_trimmed.py' "${function_with_arguments[@]}"
#outputfiles_present=$(python3 download_with_session_ID.py "${function_with_arguments[@]}")
#
#/software/linear_rigid_registration_onlytrasnformwith_matfile10162024.sh  ${moving_image_filename} ${fixed_image_filename} ${registration_mat_file} ${mask_binary_output_dir}
#mask_binary_output_filename=mov_$(basename ${moving_image_filename%.nii*})_fixed_${template_prefix}_lin1.nii.gz
#threshold=0
#function_with_arguments=('call_gray2binary' ${mask_binary_output_dir}/${mask_binary_output_filename}  ${mask_binary_output_dir} ${threshold})
#echo "outputfiles_present="'$(python3 utilities_simple_trimmed.py' "${function_with_arguments[@]}"
#outputfiles_present=$(python3 utilities_simple_trimmed.py "${function_with_arguments[@]}")
#infarct_mask_binary_output_filename=${mask_binary_output_dir}/${mask_binary_output_filename%.nii*}_BET.nii.gz
#uploadsinglefile ${sessionID} ${scanID} $(dirname ${infarct_mask_binary_output_filename}) ${snipr_output_foldername} $(basename  ${infarct_mask_binary_output_filename})
########################################################################################################
###########################################
##snipr_output_foldername="PREPROCESS_SEGM_2"
###snipr_output_foldername='PREPROCESS_SEGM'
##function_with_arguments=('call_delete_file_with_ext' ${sessionID} ${scanID} ${snipr_output_foldername} '.nii.gz' ) ##'warped_1_mov_mri_region_' )
##echo "outputfiles_present="'$(python3 utilities_simple_trimmed.py' "${function_with_arguments[@]}"
###outputfiles_present=$(python3 download_with_session_ID.py "${function_with_arguments[@]}")
##function_with_arguments=('call_delete_file_with_ext' ${sessionID} ${scanID} ${snipr_output_foldername} '.mat' ) ##'warped_1_mov_mri_region_' )
##echo "outputfiles_present="'$(python3 utilities_simple_trimmed.py' "${function_with_arguments[@]}"
###outputfiles_present=$(python3 download_with_session_ID.py "${function_with_arguments[@]}")
##uploadsinglefile ${sessionID} ${scanID} $(dirname ${registration_mat_file}) ${snipr_output_foldername} $(basename  ${registration_mat_file})
##uploadsinglefile ${sessionID} ${scanID} $(dirname ${registration_nii_file}) ${snipr_output_foldername} $(basename  ${registration_nii_file})
##uploadsinglefile ${sessionID} ${scanID} $(dirname ${mask_binary_output_dir}/${mask_binary_output_filename}) ${snipr_output_foldername} $(basename  ${mask_binary_output_dir}/${mask_binary_output_filename})
##uploadsinglefile ${sessionID} ${scanID} $(dirname ${infarct_mask_binary_output_filename}) ${snipr_output_foldername} $(basename  ${infarct_mask_binary_output_filename})
##
##uploadsinglefile ${sessionID} ${scanID} $(dirname ${fixed_image_filename}) ${snipr_output_foldername} $(basename  ${fixed_image_filename})
#
##registration_mat_file,registration_nii_file,${mask_binary_output_dir}/${mask_binary_output_filename},infarct_mask_binary_output_filename
#echo " FILES NOT PRESENT I AM WORKING ON IT"
#else
#echo " FILES ARE PRESENT "
########################################################################################################################
#fi
###
#
#done < <(tail -n +2 "${niftifile_csvfilename}")
#done

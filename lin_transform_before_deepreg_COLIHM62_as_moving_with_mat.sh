#!/bin/bash
set -euo pipefail

export XNAT_USER=${2}
export XNAT_PASS=${3}
export XNAT_HOST=${4}

sessionID=${1}

working_dir=/workinginput
working_dir_1=/input1
output_directory=/workingoutput
final_output_directory=/outputinsidedocker

copy_masks_data() {
  sessionID_=${1}
  scanID_=${2}
  resource_dirname_=${3}
  output_dirname_=${4}

  python3 -c "
import sys
sys.path.append('/software')
from download_with_session_ID import *
downloadfiletolocaldir()
" "${sessionID_}" "${scanID_}" "${resource_dirname_}" "${output_dirname_}"
}

copy_scan_data() {
  csvfilename_=${1}
  dir_to_save_=${2}

  python3 -c "
import sys
sys.path.append('/software')
from download_with_session_ID import *
downloadniftiwithuri_withcsv()
" "${csvfilename_}" "${dir_to_save_}"
}

uploadsinglefile() {
  sessionID_=${1}
  scanID_=${2}
  local_dir_=${3}
  snipr_output_foldername_=${4}
  filename_=${5}

  python3 -c "
import sys
sys.path.append('/software')
from download_with_session_ID import *
uploadsinglefile()
" "${sessionID_}" "${scanID_}" "${local_dir_}" "${snipr_output_foldername_}" "${filename_}"
}

midlineonly_each_scan() {
  for eachfile in ${working_dir_1}/*.nii*; do
    if [[ "${eachfile}" == *"levelset"* ]]; then
      continue
    fi

    original_ct_file=${eachfile}
    eachfile_basename=$(basename ${eachfile})
    eachfile_basename_noext=${eachfile_basename%.nii*}

    grayfilename=${eachfile_basename_noext}_resaved_levelset.nii
    if [[ "${eachfile_basename}" == *".nii.gz"* ]]; then
      grayfilename=${eachfile_basename_noext}_resaved_levelset.nii.gz
    fi

    betfilename=${eachfile_basename_noext}_resaved_levelset_bet.nii.gz

    cp ${working_dir}/${betfilename} ${output_directory}/
    cp ${original_ct_file} ${output_directory}/${grayfilename}

    python3 -c "
import sys
sys.path.append('/software')
from utilities_simple_trimmed import *
levelset2originalRF_new_flip()
" "${original_ct_file}" "${output_directory}/${betfilename}" "${output_directory}"

    /software/bet_withlevelset.sh ${output_directory}/${grayfilename} ${output_directory}/${betfilename}
    /software/ideal_midline_fslpart.sh ${output_directory}/${grayfilename}
    /software/ideal_midline_pythonpart.sh ${output_directory}/${grayfilename}
    /software/ideal_midline_pythonpart_V2.sh ${output_directory}/${grayfilename}
  done
}

python3 /software/download_with_session_ID.py call_download_files_in_a_resource_in_a_session ${sessionID} NIFTI_LOCATION ${working_dir}

for niftifile_csvfilename in ${working_dir}/*NIFTILOCATION.csv; do
  rm -f ${final_output_directory}/* 2>/dev/null || true
  rm -f ${output_directory}/* 2>/dev/null || true
  rm -f ${working_dir_1}/* 2>/dev/null || true

  while IFS=',' read -ra array; do
    scanID=${array[2]}
    snipr_output_foldername="PREPROCESS_SEGM_3"

#    outputfiles_present=$(python3 /software/download_with_session_ID.py call_check_if_a_file_exist_in_snipr ${sessionID} ${scanID} ${snipr_output_foldername} .pdf .csv)
#    if [[ "${outputfiles_present: -1}" -ne 0 ]]; then
#      continue
#    fi

    copy_scan_data ${niftifile_csvfilename} ${working_dir_1}

    nifti_file_without_ext=$(basename $(ls ${working_dir_1}/*.nii* | head -n 1))
    nifti_file_without_ext=${nifti_file_without_ext%.nii*}

    copy_masks_data ${sessionID} ${scanID} MASKS ${working_dir}
    copy_masks_data ${sessionID} ${scanID} PREPROCESS_SEGM_3 ${working_dir}
    copy_masks_data ${sessionID} ${scanID} EDEMA_BIOMARKER ${working_dir}

    session_ct=$(ls ${working_dir_1}/*.nii* | head -n 1)
    session_ct_bname_noext=$(basename ${session_ct})
    session_ct_bname_noext=${session_ct_bname_noext%.nii*}

    bet_mask_from_yasheng=$(ls ${working_dir}/${nifti_file_without_ext}*_resaved_levelset_bet.nii.gz | head -n 1)

    python3 -c "
import sys
sys.path.append('/software')
from utilities_simple_trimmed import *
levelset2originalRF_new_flip()
" "${session_ct}" "${bet_mask_from_yasheng}" "${output_directory}"

    /software/bet_withlevelset.sh ${session_ct} ${output_directory}/$(basename ${bet_mask_from_yasheng})

    fixed_image_filename=${output_directory}/${session_ct_bname_noext}_brain_f.nii.gz
    template_prefix=$(basename ${fixed_image_filename%.nii*})

    moving_image_filename=/software/COLIHM620406202215542.nii.gz
    /software/linear_rigid_registration_v10162024.sh ${moving_image_filename} ${fixed_image_filename} ${output_directory}

    registration_mat_file=${output_directory}/mov_COLIHM620406202215542_fixed_${template_prefix}_lin1.mat
    registration_nii_file=${output_directory}/mov_COLIHM620406202215542_fixed_${template_prefix}_lin1.nii.gz

    mask_binary_output_dir=${working_dir_1}
    threshold=0

    for moving_mask in \
      /software/VENTRICLE_COLIHM62.nii.gz \
      /software/midlinecssfResampled1.nii.gz \
      /software/VENTRICLE_COLIHM62_gray.nii.gz \
      /software/CISTERN_COLIHM62.nii.gz
    do
      /software/linear_rigid_registration_onlytrasnformwith_matfile10162024.sh \
        ${moving_mask} ${fixed_image_filename} ${registration_mat_file} ${mask_binary_output_dir}

      mask_binary_output_filename=mov_$(basename ${moving_mask%.nii*})_fixed_${template_prefix}_lin1.nii.gz

      python3 /software/utilities_simple_trimmed.py call_gray2binary \
        ${mask_binary_output_dir}/${mask_binary_output_filename} ${mask_binary_output_dir} ${threshold}

      bet_out=${mask_binary_output_dir}/${mask_binary_output_filename%.nii*}_BET.nii.gz
      uploadsinglefile ${sessionID} ${scanID} $(dirname ${bet_out}) ${snipr_output_foldername} $(basename ${bet_out})
    done

    uploadsinglefile ${sessionID} ${scanID} $(dirname ${fixed_image_filename}) ${snipr_output_foldername} $(basename ${fixed_image_filename})
    uploadsinglefile ${sessionID} ${scanID} $(dirname ${registration_mat_file}) ${snipr_output_foldername} $(basename ${registration_mat_file})
    uploadsinglefile ${sessionID} ${scanID} $(dirname ${registration_nii_file}) ${snipr_output_foldername} $(basename ${registration_nii_file})

    midlineonly_each_scan

    snipr_midline_folder="MIDLINE_NPY"
    for npyfile in ${working_dir_1}/*.npy ${output_directory}/*.npy; do
      if [[ -f "${npyfile}" ]]; then
        uploadsinglefile ${sessionID} ${scanID} $(dirname ${npyfile}) ${snipr_midline_folder} $(basename ${npyfile})
      fi
    done

    /software/run_ssh_for_compartment_and_nwu.sh ${sessionID}

  done < <(tail -n +2 "${niftifile_csvfilename}")
done

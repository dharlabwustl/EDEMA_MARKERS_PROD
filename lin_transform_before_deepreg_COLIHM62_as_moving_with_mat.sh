#!/bin/bash
set -euo pipefail

# Usage:
#   ./combined_lin_transform_before_deepreg.sh <SESSION_ID> <XNAT_USER> <XNAT_PASS> <XNAT_HOST>
#
# Notes:
# - Combines logic from:
#   1) lin_transform_before_deepreg_COLIHM62_as_moving.sh
#   2) lin_transform_before_deepreg_COLIHM62_as_moving_mat_on_mask_ris_deepreg_then_to_snipr.sh
# - If a registration .mat is already present (downloaded from SNIPR PREPROCESS_SEGM_3), it will reuse it.
#   Otherwise it will compute it using linear_rigid_registration_v10162024.sh.

export XNAT_USER="${2}"
export XNAT_PASS="${3}"
export XNAT_HOST="${4}"

sessionID="${1}"

working_dir="/workinginput"
working_dir_1="/input1"
output_directory="/workingoutput"
final_output_directory="/outputinsidedocker"

###############################################################################
# SNIPR helper functions
###############################################################################
copy_masks_data() {
  echo " I AM IN copy_masks_data "
  local sessionID="${1}"
  local scanID="${2}"
  local resource_dirname="${3}"
  local output_dirname="${4}"
  echo "output_dirname::${output_dirname}"
  python3 -c "
import sys
sys.path.append('/software');
from download_with_session_ID import *;
downloadfiletolocaldir()" "${sessionID}" "${scanID}" "${resource_dirname}" "${output_dirname}"
}

copy_scan_data_from_csv() {
  local csvfilename="${1}"
  local dir_to_save="${2}"
  python3 -c "
import sys
sys.path.append('/software');
from download_with_session_ID import *;
downloadniftiwithuri_withcsv()" "${csvfilename}" "${dir_to_save}"
}

uploadsinglefile() {
  local sessionID="${1}"
  local scanID="${2}"
  local local_dir="${3}"
  local snipr_output_foldername="${4}"
  local filename="${5}"

  echo "${local_dir}/${filename}"
  python3 -c "
import sys
sys.path.append('/software');
from download_with_session_ID import *;
uploadsinglefile()" "${sessionID}" "${scanID}" "${local_dir}" "${snipr_output_foldername}" "${filename}"
}

###############################################################################
# Midline (IML) logic from *_mat_on_mask_* script
###############################################################################
run_IML() {
  local this_filename="${1}"
  local this_betfilename="${2}"

  echo "BET USING LEVELSET MASK"
  /software/bet_withlevelset.sh "${this_filename}" "${this_betfilename}"

  echo "bet_withlevelset successful" > "${output_directory}/success.txt"

  local this_filename_brain="${this_filename%.nii*}_brain_f.nii.gz"

  echo "LINEAR REGISTRATION TO TEMPLATE"
  local mat_file_num
  mat_file_num=$(ls "${output_directory}"/*.mat 2>/dev/null | wc -l || true)

  if [[ "${mat_file_num}" -gt 1 ]]; then
    echo "MAT FILES PRESENT"
    /software/linear_rigid_registration_onlytrasnformwith_matfile.sh "${this_filename_brain}"
  else
    /software/linear_rigid_registration.sh "${this_filename_brain}"
    /software/linear_rigid_registration_onlytrasnformwith_matfile.sh "${this_filename_brain}"
    echo "linear_rigid_registration successful" >> "${output_directory}/success.txt"
  fi

  echo "RUNNING IML FSL PART"
  /software/ideal_midline_fslpart.sh "${this_filename}"
  echo "ideal_midline_fslpart successful" >> "${output_directory}/success.txt"

  echo "RUNNING IML PYTHON PART"
  /software/ideal_midline_pythonpart.sh "${this_filename}"
  echo "ideal_midline_pythonpart successful" >> "${output_directory}/success.txt"

  /software/ideal_midline_pythonpart_V2.sh "${this_filename}"
}

midlineonly_each_scan() {
  local original_ct_file=""
  local eachfile_basename=""
  local eachfile_basename_noext=""
  local grayfilename=""
  local betfilename=""
  local grayimage=""
  local bet_mask_filename=""

  for eachfile in "${working_dir_1}"/*.nii*; do
    if [[ "${eachfile}" != *"levelset"* ]]; then
      original_ct_file="${eachfile}"
      eachfile_basename="$(basename "${eachfile}")"
      eachfile_basename_noext="${eachfile_basename%.nii*}"

      grayfilename="${eachfile_basename_noext}_resaved_levelset.nii"
      if [[ "${eachfile_basename}" == *".nii.gz"* ]]; then
        grayfilename="${eachfile_basename_noext}_resaved_levelset.nii.gz"
      fi

      betfilename="${eachfile_basename_noext}_resaved_levelset_bet.nii.gz"

      # Copy levelset-bet from working_dir (downloaded masks) to output_directory
      if [[ -f "${working_dir}/${betfilename}" ]]; then
        cp "${working_dir}/${betfilename}" "${output_directory}/"
      fi

      source /software/bash_functions_forhost.sh

      # Put grayscale CT into output_directory with expected name
      cp "${original_ct_file}" "${output_directory}/${grayfilename}"
      grayimage="${output_directory}/${grayfilename}"

      # Preprocess bet mask to original RF
      bet_mask_filename="${output_directory}/${betfilename}"
      echo "levelset_bet_mask_file:${bet_mask_filename}"
      python3 -c "
import sys
sys.path.append('/software/')
from utilities_simple_trimmed import *
levelset2originalRF_new_flip()" "${original_ct_file}" "${bet_mask_filename}" "${output_directory}"

      run_IML "${grayimage}" "${bet_mask_filename}"
    fi
  done
}

###############################################################################
# Main pipeline
###############################################################################

# Download NIFTI_LOCATION CSV(s) into working_dir
call_download_files_in_a_resource_in_a_session_arguments=('call_download_files_in_a_resource_in_a_session' "${sessionID}" "NIFTI_LOCATION" "${working_dir}")
outputfiles_present=$(python3 /software/download_with_session_ID.py "${call_download_files_in_a_resource_in_a_session_arguments[@]}")
echo "outputfiles_present::${outputfiles_present}"

for niftifile_csvfilename in "${working_dir}"/*NIFTILOCATION.csv; do
  rm -f "${final_output_directory}"/*.* 2>/dev/null || true
  rm -f "${output_directory}"/*.* 2>/dev/null || true
  rm -f "${working_dir_1}"/*.* 2>/dev/null || true

  echo "Processing CSV: ${niftifile_csvfilename}"

  # Skip header, loop rows
  while IFS=',' read -ra array; do
    scanID="${array[2]}"

    echo "sessionId::${sessionID}"
    echo "scanId::${scanID}"

    snipr_output_foldername="PREPROCESS_SEGM_3"

    # Check if outputs already present
#    call_check_if_a_file_exist_in_snipr_arguments=('call_check_if_a_file_exist_in_snipr' "${sessionID}" "${scanID}" "${snipr_output_foldername}" .pdf .csv)
#    outputfiles_present=$(python3 /software/download_with_session_ID.py "${call_check_if_a_file_exist_in_snipr_arguments[@]}")
#    echo "outputfiles_present::${outputfiles_present: -1}"
#
#    if [[ "${outputfiles_present: -1}" -ne 0 ]]; then
#      echo "FILES ARE PRESENT - skipping."
#      continue
#    fi
#
#    echo "FILES NOT PRESENT - running pipeline."

    ###########################################################################
    # 1) Download session CT into /input1
    ###########################################################################
    copy_scan_data_from_csv "${niftifile_csvfilename}" "${working_dir_1}"

    session_ct="$(ls "${working_dir_1}"/*.nii* | head -n 1)"
    session_ct_bname_noext="$(basename "${session_ct}")"
    session_ct_bname_noext="${session_ct_bname_noext%.nii*}"

    nifti_file_without_ext="$(basename "${session_ct}")"
    nifti_file_without_ext="${nifti_file_without_ext%.nii*}"

    ###########################################################################
    # 2) Download relevant resources into /workinginput
    ###########################################################################
    copy_masks_data "${sessionID}" "${scanID}" "MASKS" "${working_dir}"
    copy_masks_data "${sessionID}" "${scanID}" "PREPROCESS_SEGM_3" "${working_dir}"
    copy_masks_data "${sessionID}" "${scanID}" "EDEMA_BIOMARKER" "${working_dir}"

    ###########################################################################
    # 3) Make BET gray for session CT (uses bet mask from Yasheng)
    ###########################################################################
    bet_mask_from_yasheng="$(ls "${working_dir}/${nifti_file_without_ext}"*_resaved_levelset_bet.nii.gz | head -n 1)"

    # Convert bet mask to original RF into output_directory
    python3 -c "
import sys
sys.path.append('/software/')
from utilities_simple_trimmed import *
levelset2originalRF_new_flip()" "${session_ct}" "${bet_mask_from_yasheng}" "${output_directory}"

    # Create brain-extracted fixed image
    /software/bet_withlevelset.sh "${session_ct}" "${output_directory}/$(basename "${bet_mask_from_yasheng}")"
    fixed_image_filename="${output_directory}/${session_ct_bname_noext}_brain_f.nii.gz"
    template_prefix="$(basename "${fixed_image_filename%.nii*}")"

    ###########################################################################
    # 4) Get or compute registration mat/nii for COLIHM62 -> session brain
    ###########################################################################
    moving_gray_template="/software/COLIHM620406202215542.nii.gz"
    moving_gray_template_b="$(basename "${moving_gray_template}")"

    # Preferred: reuse .mat if it exists in working_dir (downloaded from SNIPR)
    registration_mat_file_candidate_1="${working_dir}/mov_${moving_gray_template_b%.nii*}_fixed_${template_prefix}_lin1.mat"
    registration_mat_file_candidate_2="${output_directory}/mov_${moving_gray_template_b%.nii*}_fixed_${template_prefix}_lin1.mat"

    if [[ -f "${registration_mat_file_candidate_1}" ]]; then
      registration_mat_file="${registration_mat_file_candidate_1}"
      registration_nii_file="${working_dir}/mov_${moving_gray_template_b%.nii*}_fixed_${template_prefix}_lin1.nii.gz"
      echo "Reusing existing registration mat: ${registration_mat_file}"
    elif [[ -f "${registration_mat_file_candidate_2}" ]]; then
      registration_mat_file="${registration_mat_file_candidate_2}"
      registration_nii_file="${output_directory}/mov_${moving_gray_template_b%.nii*}_fixed_${template_prefix}_lin1.nii.gz"
      echo "Reusing existing registration mat: ${registration_mat_file}"
    else
      echo "No existing registration mat found. Computing rigid registration..."
      /software/linear_rigid_registration_v10162024.sh "${moving_gray_template}" "${fixed_image_filename}" "${output_directory}"
      registration_mat_file="${output_directory}/mov_${moving_gray_template_b%.nii*}_fixed_${template_prefix}_lin1.mat"
      registration_nii_file="${output_directory}/mov_${moving_gray_template_b%.nii*}_fixed_${template_prefix}_lin1.nii.gz"
    fi

    ###########################################################################
    # 5) Apply registration mat to multiple masks/templates -> binarize -> upload
    ###########################################################################
    mask_binary_output_dir="/input1"
    threshold=0

    declare -a MOVING_MASKS=(
      "/software/VENTRICLE_COLIHM62.nii.gz"
      "/software/midlinecssfResampled1.nii.gz"
      "/software/scct_strippedResampled1_left_half.nii.gz"
      "/software/VENTRICLE_COLIHM62_gray.nii.gz"
      "/software/CISTERN_COLIHM62.nii.gz"
    )

    produced_bet_masks=()

    for moving_image_filename in "${MOVING_MASKS[@]}"; do
      /software/linear_rigid_registration_onlytrasnformwith_matfile10162024.sh \
        "${moving_image_filename}" \
        "${fixed_image_filename}" \
        "${registration_mat_file}" \
        "${mask_binary_output_dir}"

      mask_binary_output_filename="mov_$(basename "${moving_image_filename%.nii*}")_fixed_${template_prefix}_lin1.nii.gz"

      function_with_arguments=('call_gray2binary' "${mask_binary_output_dir}/${mask_binary_output_filename}" "${mask_binary_output_dir}" "${threshold}")
      outputfiles_present=$(python3 /software/utilities_simple_trimmed.py "${function_with_arguments[@]}")

      bet_out="${mask_binary_output_dir}/${mask_binary_output_filename%.nii*}_BET.nii.gz"
      produced_bet_masks+=("${bet_out}")

      uploadsinglefile "${sessionID}" "${scanID}" "$(dirname "${bet_out}")" "${snipr_output_foldername}" "$(basename "${bet_out}")"
    done

    ###########################################################################
    # 6) Upload core registration products (mat/nii/fixed brain)
    ###########################################################################
    if [[ -f "${registration_mat_file}" ]]; then
      uploadsinglefile "${sessionID}" "${scanID}" "$(dirname "${registration_mat_file}")" "${snipr_output_foldername}" "$(basename "${registration_mat_file}")"
    fi
    if [[ -f "${registration_nii_file}" ]]; then
      uploadsinglefile "${sessionID}" "${scanID}" "$(dirname "${registration_nii_file}")" "${snipr_output_foldername}" "$(basename "${registration_nii_file}")"
    fi
    if [[ -f "${fixed_image_filename}" ]]; then
      uploadsinglefile "${sessionID}" "${scanID}" "$(dirname "${fixed_image_filename}")" "${snipr_output_foldername}" "$(basename "${fixed_image_filename}")"
    fi

    ###########################################################################
    # 7) Run midline-only pipeline & upload NPYs
    ###########################################################################
    midlineonly_each_scan "${session_ct}"

    snipr_midline_folder="MIDLINE_NPY"
    for npyfilename in "${working_dir_1}"/*.npy; do
      [[ -f "${npyfilename}" ]] || continue
      uploadsinglefile "${sessionID}" "${scanID}" "$(dirname "${npyfilename}")" "${snipr_midline_folder}" "$(basename "${npyfilename}")"
    done
    for npyfilename in "${output_directory}"/*.npy; do
      [[ -f "${npyfilename}" ]] || continue
      uploadsinglefile "${sessionID}" "${scanID}" "$(dirname "${npyfilename}")" "${snipr_midline_folder}" "$(basename "${npyfilename}")"
    done

    ###########################################################################
    # 8) Update DB status + trigger downstream (ssh) step
    ###########################################################################
    call_get_session_label_arguments=('call_get_session_project' "${sessionID}" "${output_directory}/${session_ct_bname_noext}_SESSION_PROJECT.csv")
    outputfiles_present=$(python3 /software/download_with_session_ID.py "${call_get_session_label_arguments[@]}")

    csv_file="${output_directory}/${session_ct_bname_noext}_SESSION_PROJECT.csv"
    column_name="SESSION_PROJECT"
    col_index=$(awk -F, -v col="${column_name}" 'NR==1 { for (i=1; i<=NF; i++) if ($i == col) { print i; exit } }' "${csv_file}")
    first_value=$(awk -F, -v idx="${col_index}" 'NR==2 { print $idx }' "${csv_file}")
    database_table_name="${first_value}"
    echo "database_table_name::${database_table_name}"

    # Record completion (include a few key filenames; keep it robust)
    function_with_arguments=('call_pipeline_step_completed'
      "${database_table_name}" "${sessionID}" "${scanID}"
      "RIGID_REGIS_AND_MIDLINE_WITH_COLIHM62_COMPLETE" 0
      "${snipr_output_foldername}"
      "$(basename "${fixed_image_filename}")"
      "$(basename "${registration_mat_file}")"
      "$(basename "${registration_nii_file}")"
    )
    outputfiles_present=$(python3 /software/download_with_session_ID.py "${function_with_arguments[@]}")

    # Trigger downstream compartment/NWU step (as in your mat_on_mask script)
    /software/run_ssh_for_compartment_and_nwu.sh "${sessionID}"

    echo "DONE for scanID=${scanID}"

  done < <(tail -n +2 "${niftifile_csvfilename}")

done

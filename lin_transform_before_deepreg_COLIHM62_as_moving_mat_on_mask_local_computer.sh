#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

###############################################################################
# CONFIGURATION – adjust paths if needed
###############################################################################
# CT NIfTI directory
WORKING_DIR_CT="/input1"

# Directory containing precomputed masks from Yasheng pipeline
WORKING_DIR_MASKS="/workinginput"

# Directory for outputs (bet gray, mats, midline outputs, etc.)
OUTPUT_DIR="/workingoutput"

# Software directory
SOFTWARE_DIR="/software"
cp /input/SCANS/2/NIFTI/* ${WORKING_DIR_CT}/
# Directory containing masks from prior pipeline (Yasheng outputs etc.)
WORKING_DIR_MASKS="/workinginput"
cp /input/SCANS/2/PREPROCESS_SEGM/* ${WORKING_DIR_MASKS}/
cp /input/SCANS/2/PREPROCESS_SEGM_3/* ${WORKING_DIR_MASKS}/
# Templates for rigid registration and masks
TEMPLATE_CT="${SOFTWARE_DIR}/COLIHM620406202215542.nii.gz"
VENTRICLE_TEMPLATE="${SOFTWARE_DIR}/VENTRICLE_COLIHM62.nii.gz"
VENTRICLE_TEMPLATE_GRAY="${SOFTWARE_DIR}/VENTRICLE_COLIHM62_gray.nii.gz"
MIDLINE_TEMPLATE="${SOFTWARE_DIR}/midlinecssfResampled1.nii.gz"
SCCT_LEFT_HALF_TEMPLATE="${SOFTWARE_DIR}/scct_strippedResampled1_left_half.nii.gz"
CISTERN_TEMPLATE="${SOFTWARE_DIR}/CISTERN_COLIHM62.nii.gz"

###############################################################################
# Helper: simple logger
###############################################################################
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

###############################################################################
# run_IML: full midline pipeline for a single gray CT + BET mask
###############################################################################
run_IML() {
  local this_filename="$1"      # gray CT image (levelset-resaved)
  local this_betfilename="$2"   # BET mask filename (in OUTPUT_DIR)

  log "RUN_IML: BET using levelset mask"
  "${SOFTWARE_DIR}/bet_withlevelset.sh" "${this_filename}" "${this_betfilename}"

  echo "bet_withlevelset successful" > "${OUTPUT_DIR}/success.txt"

  # Brain-extracted version created by bet_withlevelset.sh
  local this_filename_brain="${this_filename%.nii*}_brain_f.nii.gz"

  log "RUN_IML: LINEAR REGISTRATION TO TEMPLATE (for IML)"
  local mat_file_num
  mat_file_num=$(ls "${OUTPUT_DIR}"/*.mat 2>/dev/null | wc -l || echo 0)

  if [[ "${mat_file_num}" -gt 1 ]]; then
    log "RUN_IML: MAT files already present, applying transform only"
    "${SOFTWARE_DIR}/linear_rigid_registration_onlytrasnformwith_matfile.sh" "${this_filename_brain}"
  else
    "${SOFTWARE_DIR}/linear_rigid_registration.sh" "${this_filename_brain}"
    "${SOFTWARE_DIR}/linear_rigid_registration_onlytrasnformwith_matfile.sh" "${this_filename_brain}"
    echo "linear_rigid_registration successful" >> "${OUTPUT_DIR}/success.txt"
  fi

  log "RUN_IML: Running IML FSL part"
  "${SOFTWARE_DIR}/ideal_midline_fslpart.sh" "${this_filename}"
  echo "ideal_midline_fslpart successful" >> "${OUTPUT_DIR}/success.txt"

  log "RUN_IML: Running IML Python part (V1)"
  "${SOFTWARE_DIR}/ideal_midline_pythonpart.sh" "${this_filename}"
  echo "ideal_midline_pythonpart successful" >> "${OUTPUT_DIR}/success.txt"

  log "RUN_IML: Running IML Python part (V2)"
  "${SOFTWARE_DIR}/ideal_midline_pythonpart_V2.sh" "${this_filename}"

  log "RUN_IML: Finished midline processing for ${this_filename}"
}

###############################################################################
# Midline for a single CT: copy masks, align, call run_IML
###############################################################################
midline_for_ct() {
  local session_ct="$1"

  log "------------------------------------------------------------"
  log "Midline-only pipeline for CT: ${session_ct}"

  local ct_basename
  ct_basename="$(basename "${session_ct}")"
  local ct_noext="${ct_basename%.nii*}"

  # Levelset gray and BET mask names
  local grayfilename
  if [[ "${ct_basename}" == *".nii.gz" ]]; then
    grayfilename="${ct_noext}_resaved_levelset.nii.gz"
  else
    grayfilename="${ct_noext}_resaved_levelset.nii"
  fi

  local betfilename="${ct_noext}_resaved_levelset_bet.nii.gz"

  # Copy BET mask and CT into OUTPUT_DIR
  local bet_mask_from_yasheng
  bet_mask_from_yasheng="$(ls "${WORKING_DIR_MASKS}/${ct_noext}"*_resaved_levelset_bet.nii.gz)"

  log "Midline: using BET mask from ${bet_mask_from_yasheng}"

  cp "${bet_mask_from_yasheng}" "${OUTPUT_DIR}/${betfilename}"

  # Make sure host bash functions are present if needed
  if [[ -f "${SOFTWARE_DIR}/bash_functions_forhost.sh" ]]; then
    # shellcheck source=/dev/null
    source "${SOFTWARE_DIR}/bash_functions_forhost.sh"
  fi

  cp "${session_ct}" "${OUTPUT_DIR}/${grayfilename}"
  local grayimage="${OUTPUT_DIR}/${grayfilename}"

  log "Midline: grayimage = ${grayimage}"

  # Align BET mask to original CT orientation
  local levelset_bet_mask_file="${OUTPUT_DIR}/${betfilename}"
  log "Midline: aligning BET mask with levelset2originalRF_new_flip"
  python3 -c "
import sys
sys.path.append('${SOFTWARE_DIR}')
from utilities_simple_trimmed import levelset2originalRF_new_flip
levelset2originalRF_new_flip()
" "${session_ct}" "${levelset_bet_mask_file}" "${OUTPUT_DIR}"

  # Run full IML pipeline
  run_IML "${grayimage}" "${levelset_bet_mask_file}"
}

###############################################################################
# Warp template → CT using precomputed registration and binarize
###############################################################################
warp_and_binarize_template() {
  local template_path="$1"          # e.g. VENTRICLE_TEMPLATE
  local fixed_image_filename="$2"   # brain-extracted CT
  local registration_mat_file="$3"  # mat from TEMPLATE_CT → fixed
  local mask_output_dir="$4"        # where warped & binary masks will be saved

  local template_basename
  template_basename="$(basename "${template_path}")"
  local template_prefix_fixed
  template_prefix_fixed="$(basename "${fixed_image_filename%.nii*}")"

  log "Warping template ${template_basename} → CT space"

  "${SOFTWARE_DIR}/linear_rigid_registration_onlytrasnformwith_matfile10162024.sh" \
    "${template_path}" \
    "${fixed_image_filename}" \
    "${registration_mat_file}" \
    "${mask_output_dir}"

  local warped_filename="mov_${template_basename%.nii*}_fixed_${template_prefix_fixed}_lin1.nii.gz"
  local warped_path="${mask_output_dir}/${warped_filename}"

  log "Warped template written to: ${warped_path}"

  log "Binarizing warped template (call_gray2binary, threshold=0)"
  python3 "${SOFTWARE_DIR}/utilities_simple_trimmed.py" \
    "call_gray2binary" \
    "${warped_path}" \
    "${mask_output_dir}" \
    0

  local binary_path="${mask_output_dir}/${warped_filename%.nii*}_BET.nii.gz"
  log "Binary mask written to: ${binary_path}"

  # Return path (echo so caller can capture if needed)
  echo "${binary_path}"
}

###############################################################################
# Full processing for a single CT: registration + warp templates + midline
###############################################################################
process_ct() {
  local session_ct="$1"

  log "============================================================"
  log "Processing CT (full pipeline): ${session_ct}"

  local ct_basename
  ct_basename="$(basename "${session_ct}")"
  local ct_noext="${ct_basename%.nii*}"

  # 1) Get Yasheng BET mask
  local bet_mask_from_yasheng
  bet_mask_from_yasheng="$(ls "${WORKING_DIR_MASKS}/${ct_noext}"*_resaved_levelset_bet.nii.gz)"

  log "Using Yasheng BET mask: ${bet_mask_from_yasheng}"

  # 2) Align BET mask to CT and compute brain-extracted CT
  #    (same steps as in midline, but we want the _brain_f image for registration)
  local grayfilename
  if [[ "${ct_basename}" == *".nii.gz" ]]; then
    grayfilename="${ct_noext}_resaved_levelset.nii.gz"
  else
    grayfilename="${ct_noext}_resaved_levelset.nii"
  fi

  local betfilename="${ct_noext}_resaved_levelset_bet.nii.gz"

  cp "${bet_mask_from_yasheng}" "${OUTPUT_DIR}/${betfilename}"
  cp "${session_ct}"           "${OUTPUT_DIR}/${grayfilename}"

  local grayimage="${OUTPUT_DIR}/${grayfilename}"

  log "Aligning BET mask to original CT"
  python3 -c "
import sys
sys.path.append('${SOFTWARE_DIR}')
from utilities_simple_trimmed import levelset2originalRF_new_flip
levelset2originalRF_new_flip()
" "${session_ct}" "${OUTPUT_DIR}/${betfilename}" "${OUTPUT_DIR}"

  log "Running bet_withlevelset.sh to get brain-extracted CT"
  "${SOFTWARE_DIR}/bet_withlevelset.sh" "${session_ct}" "${OUTPUT_DIR}/$(basename "${bet_mask_from_yasheng}")"

  local fixed_image_filename="${OUTPUT_DIR}/${ct_noext}_brain_f.nii.gz"
  local template_prefix
  template_prefix="$(basename "${fixed_image_filename%.nii*}")"

  log "Brain-extracted CT for registration: ${fixed_image_filename}"

  # 3) Rigid registration: TEMPLATE_CT → fixed_image (brain CT)
  log "Rigid registration: ${TEMPLATE_CT} → ${fixed_image_filename}"
  "${SOFTWARE_DIR}/linear_rigid_registration_v10162024.sh" \
    "${TEMPLATE_CT}" \
    "${fixed_image_filename}" \
    "${OUTPUT_DIR}"

  local template_ct_basename
  template_ct_basename="$(basename "${TEMPLATE_CT}")"

  local registration_mat_file="${OUTPUT_DIR}/mov_${template_ct_basename%.nii*}_fixed_${template_prefix}_lin1.mat"
  local registration_nii_file="${OUTPUT_DIR}/mov_${template_ct_basename%.nii*}_fixed_${template_prefix}_lin1.nii.gz"

  log "Registration matrix: ${registration_mat_file}"
  log "Registered template CT: ${registration_nii_file}"

  # 4) Warp various templates and binarize (all into CT directory)
  log "Warping ventricle template (binary mask)"
  local ventricle_mask
  ventricle_mask="$(warp_and_binarize_template "${VENTRICLE_TEMPLATE}" "${fixed_image_filename}" "${registration_mat_file}" "${WORKING_DIR_CT}")"

  log "Warping midline template (binary mask)"
  local midline_mask
  midline_mask="$(warp_and_binarize_template "${MIDLINE_TEMPLATE}" "${fixed_image_filename}" "${registration_mat_file}" "${WORKING_DIR_CT}")"

  log "Warping left-half SCCT template (binary mask)"
  local scct_left_mask
  scct_left_mask="$(warp_and_binarize_template "${SCCT_LEFT_HALF_TEMPLATE}" "${fixed_image_filename}" "${registration_mat_file}" "${WORKING_DIR_CT}")"

  log "Warping ventricle gray template (binary mask)"
  local ventricle_gray_mask
  ventricle_gray_mask="$(warp_and_binarize_template "${VENTRICLE_TEMPLATE_GRAY}" "${fixed_image_filename}" "${registration_mat_file}" "${WORKING_DIR_CT}")"

  log "Warping cistern template (binary mask)"
  local cistern_mask
  cistern_mask="$(warp_and_binarize_template "${CISTERN_TEMPLATE}" "${fixed_image_filename}" "${registration_mat_file}" "${WORKING_DIR_CT}")"

  log "Warped/Binary mask outputs:"
  log "  - Ventricle mask:       ${ventricle_mask}"
  log "  - Midline mask:         ${midline_mask}"
  log "  - SCCT left-half mask:  ${scct_left_mask}"
  log "  - Ventricle gray mask:  ${ventricle_gray_mask}"
  log "  - Cistern mask:         ${cistern_mask}"

  # 5) Run midline-only IML pipeline (produces .npy midline outputs)
  midline_for_ct "${session_ct}"

  log "Finished full pipeline for CT: ${session_ct}"
}

###############################################################################
# Main: process all CTs in WORKING_DIR_CT
###############################################################################
main() {
  log "Starting local midline + template-warp pipeline"
  log "CT directory:           ${WORKING_DIR_CT}"
  log "Mask directory:         ${WORKING_DIR_MASKS}"
  log "Output directory:       ${OUTPUT_DIR}"
  log "Template CT:            ${TEMPLATE_CT}"
  log "Ventricle template:     ${VENTRICLE_TEMPLATE}"
  log "Midline template:       ${MIDLINE_TEMPLATE}"
  log "SCCT left-half template:${SCCT_LEFT_HALF_TEMPLATE}"
  log "Cistern template:       ${CISTERN_TEMPLATE}"

  mkdir -p "${WORKING_DIR_CT}" "${WORKING_DIR_MASKS}" "${OUTPUT_DIR}"

  shopt -s nullglob
  local ct_files=("${WORKING_DIR_CT}"/*.nii*)

  if (( ${#ct_files[@]} == 0 )); then
    log "No CT files (*.nii*) found in ${WORKING_DIR_CT}. Nothing to do."
    exit 0
  fi

  for ct_file in "${ct_files[@]}"; do
    process_ct "${ct_file}"
  done
cp ${WORKING_DIR_CT}/*.* /input/SCANS/2/PREPROCESS_SEGM_3/
cp ${OUTPUT_DIR}/*.* /input/SCANS/2/PREPROCESS_SEGM_3/
  log "All CTs processed successfully."
}

main "$@"

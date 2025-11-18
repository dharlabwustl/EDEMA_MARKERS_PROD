#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

###############################################################################
# CONFIGURATION – ADJUST THESE IF NEEDED
###############################################################################
# Directory containing original CT NIfTI files

WORKING_DIR_CT="/input1"
cp /input/SCANS/2/NIFTI/* ${WORKING_DIR_CT}/
# Directory containing masks from prior pipeline (Yasheng outputs etc.)
WORKING_DIR_MASKS="/workinginput"
cp /input/SCANS/2/PREPROCESS_SEGM/* ${WORKING_DIR_MASKS}/
# Directory where we will write intermediate and final outputs for this script
OUTPUT_DIR="/workingoutput"
OUTPUT_DIR_FOR_SNIPR="/outputinsidedocker"

# Software directory with scripts and templates
SOFTWARE_DIR="/software"

# Template CT and ventricle template
TEMPLATE_CT="${SOFTWARE_DIR}/COLIHM620406202215542.nii.gz"
VENTRICLE_TEMPLATE="${SOFTWARE_DIR}/VENTRICLE_COLIHM62.nii.gz"

###############################################################################
# Helper: simple logger
###############################################################################
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

###############################################################################
# Main per-CT processing function
###############################################################################
process_ct() {
  local session_ct="$1"

  log "------------------------------------------------------------"
  log "Processing CT: ${session_ct}"

  # Get base name without extension
  local ct_basename
  ct_basename="$(basename "${session_ct}")"
  local ct_noext="${ct_basename%.nii*}"

  # Find BET mask from Yasheng / previous pipeline
  # Expected pattern: <ct_noext>*_resaved_levelset_bet.nii.gz in WORKING_DIR_MASKS
  local bet_mask_from_yasheng
  bet_mask_from_yasheng="$(ls "${WORKING_DIR_MASKS}/${ct_noext}"*_resaved_levelset_bet.nii.gz)"

  log "Found BET mask from previous pipeline: ${bet_mask_from_yasheng}"

  ###########################################################################
  # 1) Transform BET mask to original CT space (if needed)
  ###########################################################################
  log "Transforming BET mask to original CT space using levelset2originalRF_new_flip"
  python3 -c "
import sys
sys.path.append('${SOFTWARE_DIR}')
from utilities_simple_trimmed import levelset2originalRF_new_flip
levelset2originalRF_new_flip()
" "${session_ct}" "${bet_mask_from_yasheng}" "${OUTPUT_DIR}"

  ###########################################################################
  # 2) Run BET with levelset mask to get brain-extracted CT
  ###########################################################################
  local bet_mask_name
  bet_mask_name="$(basename "${bet_mask_from_yasheng}")"

  log "Running bet_withlevelset.sh on CT with mask: ${bet_mask_name}"
  "${SOFTWARE_DIR}/bet_withlevelset.sh" "${session_ct}" "${OUTPUT_DIR}/${bet_mask_name}"

  local fixed_image_filename="${OUTPUT_DIR}/${ct_noext}_brain_f.nii.gz"
  local template_prefix
  template_prefix="$(basename "${fixed_image_filename%.nii*}")"

  log "Brain-extracted CT (fixed image) is: ${fixed_image_filename}"

  ###########################################################################
  # 3) Rigid registration: TEMPLATE_CT (moving) → brain-extracted CT (fixed)
  ###########################################################################
  log "Running rigid registration: TEMPLATE_CT → brain-extracted CT"
  "${SOFTWARE_DIR}/linear_rigid_registration_v10162024.sh" \
    "${TEMPLATE_CT}" "${fixed_image_filename}" "${OUTPUT_DIR}"

  local template_ct_basename
  template_ct_basename="$(basename "${TEMPLATE_CT}")"

  local registration_mat_file="${OUTPUT_DIR}/mov_${template_ct_basename%.nii*}_fixed_${template_prefix}_lin1.mat"
  local registration_nii_file="${OUTPUT_DIR}/mov_${template_ct_basename%.nii*}_fixed_${template_prefix}_lin1.nii.gz"

  log "Registration matrix: ${registration_mat_file}"
  log "Registered TEMPLATE_CT: ${registration_nii_file}"

  ###########################################################################
  # 4) Apply transform to ventricle template
  ###########################################################################
  log "Applying rigid transform to ventricle template: ${VENTRICLE_TEMPLATE}"
  local mask_binary_output_dir="${WORKING_DIR_CT}"

  "${SOFTWARE_DIR}/linear_rigid_registration_onlytrasnformwith_matfile10162024.sh" \
    "${VENTRICLE_TEMPLATE}" \
    "${fixed_image_filename}" \
    "${registration_mat_file}" \
    "${mask_binary_output_dir}"

  local ventricle_template_basename
  ventricle_template_basename="$(basename "${VENTRICLE_TEMPLATE}")"

  local mask_binary_output_filename="mov_${ventricle_template_basename%.nii*}_fixed_${template_prefix}_lin1.nii.gz"
  local warped_ventricle_path="${mask_binary_output_dir}/${mask_binary_output_filename}"

  log "Warped ventricle image written to: ${warped_ventricle_path}"

  ###########################################################################
  # 5) Binarize warped ventricle image
  ###########################################################################
  log "Binarizing warped ventricle image using call_gray2binary (threshold=0)"
  python3 "${SOFTWARE_DIR}/utilities_simple_trimmed.py" \
    "call_gray2binary" \
    "${warped_ventricle_path}" \
    "${mask_binary_output_dir}" \
    0

  local ventricle_binary_path="${mask_binary_output_dir}/${mask_binary_output_filename%.nii*}_BET.nii.gz"
  log "Binary ventricle mask written to: ${ventricle_binary_path}"

  log "Done with CT: ${session_ct}"
  log "Outputs:"
  log "  - Brain-extracted CT (fixed):      ${fixed_image_filename}"
  log "  - Registration matrix (.mat):      ${registration_mat_file}"
  log "  - Registered TEMPLATE_CT (.nii):   ${registration_nii_file}"
  log "  - Warped ventricle image:          ${warped_ventricle_path}"
  log "  - Binary ventricle mask:           ${ventricle_binary_path}"
}

###############################################################################
# Main loop: process all CTs in WORKING_DIR_CT
###############################################################################
main() {
  echo argument1::${1}
#  exit
  log "Starting local rigid-registration + ventricle-mask pipeline"
  log "CT directory:        ${WORKING_DIR_CT}"
  log "Mask directory:      ${WORKING_DIR_MASKS}"
  log "Output directory:    ${OUTPUT_DIR}"
  log "Template CT:         ${TEMPLATE_CT}"
  log "Ventricle template:  ${VENTRICLE_TEMPLATE}"

  # Ensure directories exist
#  mkdir -p "${WORKING_DIR_CT}" "${WORKING_DIR_MASKS}" "${OUTPUT_DIR}"

  shopt -s nullglob
  local ct_files=("${WORKING_DIR_CT}"/*.nii*)

  if (( ${#ct_files[@]} == 0 )); then
    log "No CT files (*.nii*) found in ${WORKING_DIR_CT}. Nothing to do."
    exit 0
  fi

  for ct_file in "${ct_files[@]}"; do
    process_ct "${ct_file}"
  done
  cp ${OUTPUT_DIR}/* ${OUTPUT_DIR_FOR_SNIPR}/
  cp ${OUTPUT_DIR}/* /input/SCANS/2/PREPROCESS_SEGM_3
  log "All CTs processed successfully."
}

main "$@"

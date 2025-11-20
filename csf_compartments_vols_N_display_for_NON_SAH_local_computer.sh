#!/bin/bash
set -euo pipefail

########################################
# Usage:
#   ./csf_local_simple.sh <CT_DIR> <MASK_DIR> <OUTPUT_DIR>
#
#   CT_DIR    : folder with original NCCT NIfTI(s)
#   MASK_DIR  : folder with *_resaved_levelset_bet.nii.gz,
#               *_resaved_csf_unet.nii.gz,
#               *_resaved_infarct_auto_removesmall.nii.gz, etc.
#   OUTPUT_DIR: where all outputs (registered NIfTI, CSV, PDF, etc.) go
########################################

if [ "$#" -lt 3 ]; then
  echo "Usage: $0 <CT_DIR> <MASK_DIR> <OUTPUT_DIR>"
  exit 1
fi

CT_DIR="/input1"            # original CT
MASK_DIR="/workinginput"          # masks
OUTPUT_DIR="/workingoutput"        # processing + final outputs
FINAL_OUTPUT_DIR="$OUTPUT_DIR"
cp /input/SCANS/2/NIFTI/* ${CT_DIR}/
# Directory containing masks from prior pipeline (Yasheng outputs etc.)
WORKING_DIR_MASKS="/workinginput"
cp /input/SCANS/2/MASKS/* ${MASK_DIR}/
#cp /input/SCANS/2/PREPROCESS_SEGM_3/* ${WORKING_DIR_MASKS}/
#mkdir -p "${CT_DIR}" "${MASK_DIR}" "${OUTPUT_DIR}" "${FINAL_OUTPUT_DIR}"

echo "Running LOCAL NWU + CSF pipeline (no XNAT, no DB)"
echo "  CT_DIR      : ${CT_DIR}"
echo "  MASK_DIR    : ${MASK_DIR}"
echo "  OUTPUT_DIR  : ${OUTPUT_DIR}"
echo

########################################
# Helper: IML + NWU + CSF volume calc
########################################
run_IML_NWU_CSF_CALC() {
  local this_filename=${1}
  local this_betfilename=${2}
  local this_csfmaskfilename=${3}
  local this_infarctmaskfilename=${4}
  local lower_threshold=${5}
  local upper_threshold=${6}

  echo "=== IML + NWU + CSF CALC ==="
  echo "CT          : ${this_filename}"
  echo "BET mask    : ${this_betfilename}"
  echo "CSF mask    : ${this_csfmaskfilename}"
  echo "Infarct mask: ${this_infarctmaskfilename}"
  echo "Thresholds  : ${lower_threshold}–${upper_threshold}"
  echo "==================================="

  echo "BET USING LEVELSET MASK"
  /software/bet_withlevelset.sh "${this_filename}" "${this_betfilename}"

  echo "bet_withlevelset successful" >"${OUTPUT_DIR}/success.txt"

  local this_filename_brain=${this_filename%.nii*}_brain_f.nii.gz
  echo "LINEAR REGISTRATION TO TEMPLATE"
  /software/linear_rigid_registration.sh "${this_filename_brain}"
  echo "linear_rigid_registration successful" >>"${OUTPUT_DIR}/success.txt"

  echo "RUNNING IML FSL PART"
  /software/ideal_midline_fslpart.sh "${this_filename}"
  echo "ideal_midline_fslpart successful" >>"${OUTPUT_DIR}/success.txt"

  echo "RUNNING IML PYTHON PART"
  /software/ideal_midline_pythonpart.sh "${this_filename}"
  echo "ideal_midline_pythonpart successful" >>"${OUTPUT_DIR}/success.txt"

  echo "RUNNING NWU AND CSF VOLUME CALCULATION"
  /software/nwu_csf_volume.sh \
    "${this_filename}" \
    "${this_betfilename}" \
    "${this_csfmaskfilename}" \
    "${this_infarctmaskfilename}" \
    "${lower_threshold}" \
    "${upper_threshold}"

  echo "nwu_csf_volume successful" >>"${OUTPUT_DIR}/success.txt"

  # Build PDFs from LaTeX, if any
  for texfile in "${OUTPUT_DIR}"/*.tex; do
    [ -e "${texfile}" ] || continue
    echo "Compiling LaTeX: ${texfile}"
    pdflatex -halt-on-error -interaction=nonstopmode -output-directory="${OUTPUT_DIR}" "${texfile}"
    rm -f "${OUTPUT_DIR}"/*.aux "${OUTPUT_DIR}"/*.log
  done

  # Copy key outputs to FINAL_OUTPUT_DIR
  for f in "${OUTPUT_DIR}"/*_brain_f.nii.gz; do
    [ -e "${f}" ] || continue
    cp "${f}" "${FINAL_OUTPUT_DIR}/"
  done

  for f in "${OUTPUT_DIR}"/*.mat; do
    [ -e "${f}" ] || continue
    cp "${f}" "${FINAL_OUTPUT_DIR}/"
  done

  for f in "${OUTPUT_DIR}"/*.pdf; do
    [ -e "${f}" ] || continue
    cp "${f}" "${FINAL_OUTPUT_DIR}/"
  done

  for f in "${OUTPUT_DIR}"/*.csv; do
    [ -e "${f}" ] || continue
    cp "${f}" "${FINAL_OUTPUT_DIR}/"
  done
}

########################################
# MAIN LOOP: for each CT in CT_DIR
########################################

# global thresholds (can edit here)
LOWER_THRESHOLD=0
UPPER_THRESHOLD=20

for eachfile in "${CT_DIR}"/*.nii*; do
  [ -e "${eachfile}" ] || continue   # skip if none

  original_ct_file="${eachfile}"
  eachfile_basename=$(basename "${eachfile}")
  eachfile_basename_noext=${eachfile_basename%.nii*}

  echo
  echo "#####################################################"
  echo "Processing CT file: ${eachfile_basename}"
  echo "#####################################################"

  # Levelset gray filename
  grayfilename="${eachfile_basename_noext}_resaved_levelset.nii"
  if [[ "${eachfile_basename}" == *".nii.gz"* ]]; then
    grayfilename="${eachfile_basename_noext}_resaved_levelset.nii.gz"
  fi

  betfilename="${eachfile_basename_noext}_resaved_levelset_bet.nii.gz"
  csffilename="${eachfile_basename_noext}_resaved_csf_unet.nii.gz"
  infarctfilename="${eachfile_basename_noext}_resaved_infarct_auto_removesmall.nii.gz"

  # Check that required masks exist in MASK_DIR
  for f in "${betfilename}" "${csffilename}" "${infarctfilename}"; do
    if [ ! -f "${MASK_DIR}/${f}" ]; then
      echo "WARNING: Missing mask ${MASK_DIR}/${f} – skipping this CT."
      continue 2
    fi
  done

  # Copy masks from MASK_DIR to OUTPUT_DIR
  cp "${MASK_DIR}/${betfilename}"     "${OUTPUT_DIR}/"
  cp "${MASK_DIR}/${csffilename}"     "${OUTPUT_DIR}/"
  cp "${MASK_DIR}/${infarctfilename}" "${OUTPUT_DIR}/"

  # Prepare gray image in OUTPUT_DIR
  cp "${original_ct_file}" "${OUTPUT_DIR}/${grayfilename}"
  grayimage="${OUTPUT_DIR}/${grayfilename}"

  # Map masks from levelset RF to original RF
  echo "Mapping masks to original RF using utilities_simple_trimmed.levelset2originalRF_new_flip"

  levelset_infarct_mask_file="${OUTPUT_DIR}/${infarctfilename}"
  python3 -c "
import sys
sys.path.append('/software/')
from utilities_simple_trimmed import *
levelset2originalRF_new_flip()" \
    "${original_ct_file}" "${levelset_infarct_mask_file}" "${OUTPUT_DIR}"

  levelset_bet_mask_file="${OUTPUT_DIR}/${betfilename}"
  python3 -c "
import sys
sys.path.append('/software/')
from utilities_simple_trimmed import *
levelset2originalRF_new_flip()" \
    "${original_ct_file}" "${levelset_bet_mask_file}" "${OUTPUT_DIR}"

  levelset_csf_mask_file="${OUTPUT_DIR}/${csffilename}"
  python3 -c "
import sys
sys.path.append('/software/')
from utilities_simple_trimmed import *
levelset2originalRF_new_flip()" \
    "${original_ct_file}" "${levelset_csf_mask_file}" "${OUTPUT_DIR}"

  x="${grayimage}"
  bet_mask_filename="${OUTPUT_DIR}/${betfilename}"
  infarct_mask_filename="${OUTPUT_DIR}/${infarctfilename}"
  csf_mask_filename="${OUTPUT_DIR}/${csffilename}"

  run_IML_NWU_CSF_CALC \
    "${x}" \
    "${bet_mask_filename}" \
    "${csf_mask_filename}" \
    "${infarct_mask_filename}" \
    "${LOWER_THRESHOLD}" \
    "${UPPER_THRESHOLD}"

done

echo
echo "All done (local-only NWU + CSF pipeline). Outputs in: ${OUTPUT_DIR} and ${FINAL_OUTPUT_DIR}"

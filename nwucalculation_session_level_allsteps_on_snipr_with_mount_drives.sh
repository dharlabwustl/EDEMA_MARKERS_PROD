#!/bin/bash
#
# local_edema_nwu_csf_pipeline.sh
#
# Run IML + NWU + CSF volume calculation **locally** on CT + mask files.
# All XNAT / SNIPR download/upload logic has been removed.
#
# Usage:
#   ./local_edema_nwu_csf_pipeline.sh \
#       /path/to/ct_dir \
#       /path/to/mask_dir \
#       [/workingoutput] \
#       [/outputinsidedocker]
#
# Defaults (if not provided):
#   output_directory     = /workingoutput
#   final_output_dir     = /outputinsidedocker
#

set -euo pipefail

# ----------------- Parse arguments -------------------------------------------

#if [[ $# -lt 2 ]]; then
#  echo "Usage: $0 /path/to/ct_dir /path/to/mask_dir [/workingoutput] [/outputinsidedocker]"
#  exit 1
#fi

# Directory with original CT NIfTI files (e.g. /input1)
sessionID=${1}
working_dir_1="/input"

# Directory with mask files (bet, csf, infarct) (e.g. /workinginput)
working_dir="/workinginput"
output_directory=/workingoutput #"${3:-/workingoutput}"
final_output_directory=/outputinsidedocker ##"${4:-/outputinsidedocker}"
cp /input/RESOURCES/NIFTI_LOCATION/*_NIFTILOCATION.csv ${working_dir}/
niftilocation_file=$(ls ${working_dir}/*_NIFTILOCATION.csv | head -n 1)
scanID=$(python3 -c "from utilities_simple_trimmed import get_csv_column_value; print(get_csv_column_value('${niftilocation_file}', 'ID'))")
cp /input/SCANS/${scanID}/NIFTI/*.* "${working_dir_1}/"
cp /input/SCANS/${scanID}/PREPROCESS_SEGM/*.* "${working_dir}/"
cp /input/SCANS/${scanID}/MASKS/*.*   "${working_dir}/"
cp /input/SCANS/${scanID}/PREPROCESS_SEGM_3/*.*  ${output_directory}/
#cp /input/SCANS/2/PREPROCESS_SEGM/*.*  ${output_directory}/
# Output dirs


echo ">>> CT input directory:          ${working_dir_1}"
echo ">>> Mask input directory:        ${working_dir}"
echo ">>> Output directory:            ${output_directory}"
echo ">>> Final output directory:      ${final_output_directory}"

#mkdir -p "${output_directory}"
#mkdir -p "${final_output_directory}"

# Optional clean up of previous results
#echo ">>> Cleaning old contents in output and final directories..."
#rm -rf "${output_directory:?}/"* || true
#rm -rf "${final_output_directory:?}/"* || true

# ----------------- Functions (LOCAL ONLY) ------------------------------------

run_IML_NWU_CSF_CALC() {
  this_filename=${1}
  this_betfilename=${2}
  this_csfmaskfilename=${3}
  this_infarctmaskfilename=${4}

  echo "========================================================="
  echo "RUN_IML_NWU_CSF_CALC for: ${this_filename}"
  echo "BET mask:    ${this_betfilename}"
  echo "CSF mask:    ${this_csfmaskfilename}"
  echo "Infarct mask:${this_infarctmaskfilename}"
  echo "========================================================="

  echo "BET USING LEVELSET MASK"
  /software/bet_withlevelset.sh "${this_filename}" "${this_betfilename}"

  echo "bet_withlevelset successful" > "${output_directory}/success.txt"

  this_filename_brain=${this_filename%.nii*}_brain_f.nii.gz

  echo "LINEAR REGISTRATION TO TEMPLATE 1"
  mat_file_num=$(ls ${output_directory}/*.mat | wc -l)
  if [[ ${mat_file_num} -gt 1 ]]; then
    echo "MAT FILES PRESENT"
    /software/linear_rigid_registration_onlytrasnformwith_matfile.sh ${this_filename_brain}
  else
    /software/linear_rigid_registration.sh ${this_filename_brain} #${templatefilename} #$3 ${6} WUSTL_233_11122015_0840__levelset_brain_f.nii.gz
    /software/linear_rigid_registration_onlytrasnformwith_matfile.sh ${this_filename_brain}
    echo "linear_rigid_registration successful" >>${output_directory}/success.txt
  fi

#  /software/linear_rigid_registration.sh "${this_filename_brain}"



#  echo "linear_rigid_registration successful" >> "${output_directory}/success.txt"

  echo "RUNNING IML FSL PART"
  /software/ideal_midline_fslpart.sh "${this_filename}"
  echo "ideal_midline_fslpart successful" >> "${output_directory}/success.txt"

  echo "RUNNING IML PYTHON PART"
  /software/ideal_midline_pythonpart.sh "${this_filename}"
  echo "ideal_midline_pythonpart successful" >> "${output_directory}/success.txt"

  echo "RUNNING NWU AND CSF VOLUME CALCULATION"
  /software/nwu_csf_volume.sh \
    "${this_filename}" \
    "${this_betfilename}" \
    "${this_csfmaskfilename}" \
    "${this_infarctmaskfilename}" \
    "${lower_threshold}" \
    "${upper_threshold}"

  echo "nwu_csf_volume successful" >> "${output_directory}/success.txt"

  thisfile_basename=$(basename "${this_filename}")

  # Compile LaTeX reports (all .tex in output_directory)
  for texfile in "${output_directory}"/*.tex; do
    [ -e "$texfile" ] || continue
    pdflatex -halt-on-error -interaction=nonstopmode \
      -output-directory="${output_directory}" "$texfile"
    rm -f "${output_directory}"/*.aux
    rm -f "${output_directory}"/*.log
  done

  # Copy brain images
  for filetocopy in $(/usr/lib/fsl/5.0/remove_ext "${output_directory}/${thisfile_basename}")*_brain_f.nii.gz; do
    [ -e "$filetocopy" ] || continue
    cp "${filetocopy}" "${final_output_directory}/"
  done

  # Copy .mat transform files
  for filetocopy in $(/usr/lib/fsl/5.0/remove_ext "${output_directory}/${thisfile_basename}")*.mat; do
    [ -e "$filetocopy" ] || continue
    cp "${filetocopy}" "${final_output_directory}/"
  done

  # Copy PDFs and CSVs
  for filetocopy in "${output_directory}"/*.pdf; do
    [ -e "$filetocopy" ] || continue
    cp "${filetocopy}" "${final_output_directory}/"
  done

  for filetocopy in "${output_directory}"/*.csv; do
    [ -e "$filetocopy" ] || continue
    cp "${filetocopy}" "${final_output_directory}/"
  done

  echo ">>> Finished RUN_IML_NWU_CSF_CALC for: ${this_filename}"
}

nwucalculation_each_scan() {
  eachfile_basename_noext=''
  original_ct_file=''

  # Process each CT file in working_dir_1
  for eachfile in "${working_dir_1}"/*.nii*; do
    [ -e "$eachfile" ] || continue

    original_ct_file="${eachfile}"
    eachfile_basename=$(basename "${eachfile}")
    eachfile_basename_noext=${eachfile_basename%.nii*}

    echo "========================================================="
    echo "Processing CT file: ${original_ct_file}"
    echo "Base name:          ${eachfile_basename_noext}"
    echo "========================================================="

    # Filenames for masks (must exist in ${working_dir})
    grayfilename=${eachfile_basename_noext}_resaved_levelset.nii
    if [[ "$eachfile_basename" == *".nii.gz"* ]]; then
      grayfilename=${eachfile_basename_noext}_resaved_levelset.nii.gz
    fi

    betfilename=${eachfile_basename_noext}_resaved_levelset_bet.nii.gz
    csffilename=${eachfile_basename_noext}_resaved_csf_unet.nii.gz
    infarctfilename=${eachfile_basename_noext}_resaved_infarct_auto_removesmall.nii.gz

    echo "Expected mask files (in mask dir):"
    echo "  BET:     ${working_dir}/${betfilename}"
    echo "  CSF:     ${working_dir}/${csffilename}"
    echo "  Infarct: ${working_dir}/${infarctfilename}"

    # Copy masks into output_directory
    cp "${working_dir}/${betfilename}"     "${output_directory}/"
    cp "${working_dir}/${csffilename}"     "${output_directory}/"
    cp "${working_dir}/${infarctfilename}" "${output_directory}/"

    # Source any host bash functions if needed
    source /software/bash_functions_forhost.sh

    # Copy original CT into output_directory with grayfilename
    cp "${original_ct_file}" "${output_directory}/${grayfilename}"
    grayimage="${output_directory}/${grayfilename}"

    levelset_infarct_mask_file="${output_directory}/${infarctfilename}"
    echo "levelset_infarct_mask_file: ${levelset_infarct_mask_file}"

    # Preprocess infarct mask
    python3 -c "
import sys
sys.path.append('/software/')
from utilities_simple_trimmed import *  # noqa
levelset2originalRF_new_flip()" \
      "${original_ct_file}" "${levelset_infarct_mask_file}" "${output_directory}"

    # Preprocess BET mask
    levelset_bet_mask_file="${output_directory}/${betfilename}"
    echo "levelset_bet_mask_file: ${levelset_bet_mask_file}"

    python3 -c "
import sys
sys.path.append('/software/')
from utilities_simple_trimmed import *  # noqa
levelset2originalRF_new_flip()" \
      "${original_ct_file}" "${levelset_bet_mask_file}" "${output_directory}"

    # Preprocess CSF mask
    levelset_csf_mask_file="${output_directory}/${csffilename}"
    echo "levelset_csf_mask_file: ${levelset_csf_mask_file}"

    python3 -c "
import sys
sys.path.append('/software/')
from utilities_simple_trimmed import *  # noqa
levelset2originalRF_new_flip()" \
      "${original_ct_file}" "${levelset_csf_mask_file}" "${output_directory}"

    # Thresholds + template info (used inside run_IML_NWU_CSF_CALC via globals)
    lower_threshold=0
    upper_threshold=20
    templatefilename=scct_strippedResampled1.nii.gz
    mask_on_template=midlinecssfResampled1.nii.gz

    x="${grayimage}"
    bet_mask_filename="${output_directory}/${betfilename}"
    infarct_mask_filename="${output_directory}/${infarctfilename}"
    csf_mask_filename="${output_directory}/${csffilename}"

    run_IML_NWU_CSF_CALC "${x}" "${bet_mask_filename}" "${csf_mask_filename}" "${infarct_mask_filename}"

    echo ">>> Completed edema biomarker calculation for: ${original_ct_file}"
    echo
  done
}

# ----------------- Main ------------------------------------------------------

echo ">>> Starting local NWU + CSF volume pipeline..."
nwucalculation_each_scan
#uploadsinglefile(){
#local sessionID=${1}
#local scanID=${2}
#local mask_binary_output_dir=${3}
#local snipr_output_foldername=${4}
#local mask_binary_output_filename=${5}
#
#echo ${mask_binary_output_dir}/${mask_binary_output_filename}
#python3 -c "
#import sys
#sys.path.append('/software');
#from download_with_session_ID import *;
#uploadsinglefile()" ${sessionID} ${scanID} ${mask_binary_output_dir} ${snipr_output_foldername} ${mask_binary_output_filename}
#}
#snipr_output_foldername="EDEMA_BIOMARKER"
##file_to_upload=$(ls ${workingoutput}/*columndropped.csv ) ##| head -n 1)
##uploadsinglefile ${sessionID} ${scanID} $(dirname "${file_to_upload}")  ${snipr_output_foldername} $(basename "${file_to_upload}")
#for file_to_upload in "${workingoutput}"/*columndropped.csv; do
#    # Skip if no files match
#    [ -e "$file_to_upload" ] || continue
#
#    uploadsinglefile \
#        "${sessionID}" \
#        "${scanID}" \
#        "$(dirname "$file_to_upload")" \
#        "${snipr_output_foldername}" \
#        "$(basename "$file_to_upload")"
#done
#for file_to_upload in "${workingoutput}"/*.mat; do
#    # Skip if no files match
#    [ -e "$file_to_upload" ] || continue
#
#    uploadsinglefile \
#        "${sessionID}" \
#        "${scanID}" \
#        "$(dirname "$file_to_upload")" \
#        "${snipr_output_foldername}" \
#        "$(basename "$file_to_upload")"
#done
#
##copyoutput_to_snipr() {
##  sessionID=$1
##  scanID=$2
##  resource_dirname=$4 #"MASKS" #sys.argv[4]
##  file_suffix=$5
##  output_dir=$3
##  echo " I AM IN copyoutput_to_snipr "
##  python3 -c "
##import sys
##sys.path.append('/software');
##from download_with_session_ID import *;
##uploadfile()" ${sessionID} ${scanID} ${output_dir} ${resource_dirname} ${file_suffix} # ${infarctfile_present}  ##$static_template_image $new_image $backslicenumber #$single_slice_filename
##
##}
##echo ">>> All done. Final outputs are in: ${final_output_directory}"
###cp ${final_output_directory}/*.*  /input/SCANS/2/EDEMA_BIOMARKER/
##snipr_output_foldername="EDEMA_BIOMARKER"
##file_suffixes=(.pdf .mat .csv) #sys.argv[5]
##for file_suffix in "${file_suffixes[@]}"; do
##  copyoutput_to_snipr ${sessionID} ${scanID} "${final_output_directory}" ${snipr_output_foldername} ${file_suffix}
##done
#!/usr/bin/env bash
set -euo pipefail
echo " IAM HERE"
#exit
VERSION='TEST'
time_now=$(date +%m_%d_%Y)
outputfiles_suffix="${VERSION}_${time_now}"

grayscale_filename_1="/media/atul/WDJan2022/WASHU_WORKS/PROJECTS/GUI_SOFTWARE/SNIPR_PIPELINE/workinginput/COLI_HSP56_08242020_1502_201_resaved_levelset.nii.gz"
grayscale_filename_basename_noext="$(basename "${grayscale_filename_1%.nii*}")"
echo $grayscale_filename_1
ls ${grayscale_filename_1}
latexfilename_prefix="${grayscale_filename_1%.nii*}"
latexfilename="${latexfilename_prefix}_${outputfiles_suffix}.tex"

# ---- LaTeX start ----
call_latex_start_arguments=( "call_latex_start" "${latexfilename}" )
outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_latex_start_arguments[@]}")

contrast_limits="1000_1200"

# Use a single, consistent output directory variable
output_directory="/workingoutput"
outputfile_dir="${output_directory}"

outputfile_suffix="MIDLINE"
color_list="orange_orange"
midline_mask="/media/atul/WDJan2022/WASHU_WORKS/PROJECTS/GUI_SOFTWARE/SNIPR_PIPELINE/workinginput/warped_1_mov_midlinecssfResampled1_fixed_COLI_HSP56_08242020_1502_201_brain_f_lin1_BET.nii.gz"
echo ${midline_mask}
ls ${midline_mask}
npyfiledirectory="/workinginput"
# Use a consistent working_dir name
working_dir="/workinginput"
working_dir_1="input1"
#    outputfile_suffix="MIDLINE"
    color_list='red_green'
    call_masks_on_grayscale_colored_arguments=('call_masks_on_grayscale_colored' ${grayscale_filename_1} ${contrast_limits} ${outputfile_dir} ${outputfile_suffix} ${color_list} ${working_dir_1} ${midline_mask} ${midline_mask})
   echo "${call_masks_on_grayscale_colored_arguments[@]}"
#python3 -c "from utilities_simple_trimmed import create_color_legend_from_names; create_color_legend_from_names(['green','red','None'], ['RIGHT_CSF_VOLUME ${RIGHT_CSF_VOLUME}','LEFT_CSF_VOLUME ${LEFT_CSF_VOLUME}','CSF_RATIO ${CSF_RATIO}'], 'legend_CSF.png')"
#    outputfiles_present=$(python3 dividemasks_into_left_right_Nov20_2025.py "${call_masks_on_grayscale_colored_arguments[@]}")
#python3 - <<EOF
#from dividemasks_into_left_right_Nov20_2025 import masks_on_grayscale_colored
#
#result = masks_on_grayscale_colored(
#    "${grayscale_filename}",
#    "${contrast_limits}",
#    "${mask_filename_list}",
#    "${mask_color_list}",
#    "${outputfile_dir}",
#    "${outputfile_suffix}",
#    "${npyfiledirectory}"
#)
#
#print(result)
#EOF

#
#call_masks_on_grayscale_colored_arguments=(
#  "call_masks_on_grayscale_colored"
#  "${grayscale_filename_1}"
#  "${contrast_limits}"
#  "${outputfile_dir}"
#  "${outputfile_suffix}"
#  "${color_list}"
#  "${working_dir}"
#  "${midline_mask}"
#  "${midline_mask}"
#)
outputfiles_present=$(python3 dividemasks_into_left_right_Nov20_2025.py "${call_masks_on_grayscale_colored_arguments[@]}")
#
## ---- Loop over JPGs ----
#for x in "${working_dir}/${grayscale_filename_basename_noext}"*.jpg; do
#  # If the glob doesn't match anything, skip
#  [ -e "$x" ] || continue
#
#  imagescale='0.18'
#  angle='90'
#  space='1'
#
#  # Re-initialize array for each image
#  images=()
#  images+=( "call_latex_insertimage_tableNc" )
#  images+=( "${latexfilename}" )
#  images+=( "${imagescale}" )
#  images+=( "${angle}" )
#  images+=( "${space}" )
#
#  y="${x%.*}"
#  echo "${y}"
#  echo "DEBUGGING STARTS"
#
#  # Get numeric suffix after last underscore
#  suffix="${y##*_}"
#
#  # Ensure suffix is numeric before integer comparison
#  if [[ "${suffix}" =~ ^[0-9]+$ ]] \
#     && (( suffix > 0 )) \
#     && [ -f "${x}" ] \
#     && [ -f "${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_MIDLINE_${suffix}.jpg" ]; then
#
#    echo "suffix::${suffix}"
#
#    images+=( "${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_MIDLINE_${suffix}.jpg" )
#
#    outputfiles_present=$(python3 utilities_simple_trimmed.py "${images[@]}")
#    echo "outputfiles_present::${outputfiles_present}"
#  fi
#done
#
## ---- LaTeX end + PDF ----
#call_latex_end_arguments=( "call_latex_end" "${latexfilename}" )
#outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_latex_end_arguments[@]}")
#
#pdflatex -halt-on-error -interaction=nonstopmode \
#  -output-directory="${output_directory}" \
#  "${latexfilename}"

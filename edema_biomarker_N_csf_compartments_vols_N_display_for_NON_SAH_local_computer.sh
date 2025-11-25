VERSION='V_08162023'
time_now=$(date -dnow +%m_%d_%Y)
outputfiles_suffix=${VERSION}_${time_now}
export XNAT_USER=${2}
export XNAT_PASS=${3}
export XNAT_HOST=${4}
sessionID=${1}
working_dir=/workinginput
working_dir_1=/input1
output_directory=/workingoutput
cp /input/SCANS/2/NIFTI/* ${working_dir_1}/
# Directory containing masks from prior pipeline (Yasheng outputs etc.)
WORKING_DIR_MASKS="/workinginput"
cp /input/SCANS/2/MASKS/* ${working_dir}/
#cp /input/SCANS/2/NIFTI/* ${WORKING_DIR_CT}/
# Directory containing masks from prior pipeline (Yasheng outputs etc.)
#WORKING_DIR_MASKS="/workinginput"

cp /input/SCANS/2/PREPROCESS_SEGM_3/* ${working_dir}/
cp /input/SCANS/2/PREPROCESS_SEGM/* ${working_dir}/
final_output_directory=/outputinsidedocker
call_combine_csv_horizontally() {
  local grayscale_filename_basename_noext=${1}
  local csvfilename=${2}
  local file_to_append_horizontally=${3}
  local call_combine_csv_horizontally_arguments=('call_combine_csv_horizontally' ${grayscale_filename_basename_noext} ${csvfilename} ${csvfilename} ${file_to_append_horizontally})
  local outputfiles_present=$(python3 dividemasks_into_left_right_Nov20_2025.py "${call_combine_csv_horizontally_arguments[@]}")

}
run_Registration() {
  this_filename=${1}
  this_betfilename=${2}
  echo "BET USING LEVELSET MASK"

  /software/bet_withlevelset.sh $this_filename ${this_betfilename} #${output_directory} #Helsinki2000_1019_10132014_1048_Head_2.0_ax_Tilt_1_levelset # ${3} # Helsinki2000_702_12172013_2318_Head_2.0_ax_levelset.nii.gz #${3} # $6 $7 $8 $9 ${10}

  echo "bet_withlevelset successful" >${output_directory}/success.txt
  this_filename_brain=${this_filename%.nii*}_brain_f.nii.gz
  echo "LINEAR REGISTRATION TO TEMPLATE 1"
  /software/linear_rigid_registration.sh ${this_filename_brain} #${templatefilename} #$3 ${6} WUSTL_233_11122015_0840__levelset_brain_f.nii.gz



}

run_IML() {
  this_filename=${1}
  this_betfilename=${2}
  echo "BET USING LEVELSET MASK"

  /software/bet_withlevelset.sh $this_filename ${this_betfilename} #${output_directory} #Helsinki2000_1019_10132014_1048_Head_2.0_ax_Tilt_1_levelset # ${3} # Helsinki2000_702_12172013_2318_Head_2.0_ax_levelset.nii.gz #${3} # $6 $7 $8 $9 ${10}

  echo "bet_withlevelset successful" >${output_directory}/success.txt
  this_filename_brain=${this_filename%.nii*}_brain_f.nii.gz
  echo "LINEAR REGISTRATION TO TEMPLATE 2"
  mat_file_num=$(ls ${output_directory}/*.mat | wc -l)
  if [[ ${mat_file_num} -gt 1 ]]; then
    echo "MAT FILES PRESENT"
    /software/linear_rigid_registration_onlytrasnformwith_matfile.sh ${this_filename_brain}
  else
    /software/linear_rigid_registration.sh ${this_filename_brain} #${templatefilename} #$3 ${6} WUSTL_233_11122015_0840__levelset_brain_f.nii.gz
    /software/linear_rigid_registration_onlytrasnformwith_matfile.sh ${this_filename_brain}
    echo "linear_rigid_registration successful" >>${output_directory}/success.txt
  fi

  echo "RUNNING IML FSL PART"
  /software/ideal_midline_fslpart.sh ${this_filename} # ${templatefilename} ${mask_on_template}  #$9 #${10} #$8
  echo "ideal_midline_fslpart successful" >>${output_directory}/success.txt

  echo "RUNNING IML PYTHON PART"

  /software/ideal_midline_pythonpart.sh ${this_filename} #${templatefilename}  #$3 #$8 $9 ${10}
  echo "ideal_midline_pythonpart successful" >>${output_directory}/success.txt
  /software/ideal_midline_pythonpart_V2.sh ${this_filename} #${templatefilename}  #$3 #$8 $9 ${10}


}



run_divide_mask_into_left_right() {
  local grayimage=${1}
  local csf_mask_filename=${2}
  local output_directory=${3}
  local working_dir=${4}
  call_divide_a_mask_into_left_right_submasks_arguments=('call_divide_a_mask_into_left_right_submasks' ${grayimage} ${csf_mask_filename} ${output_directory} ${working_dir})
  outputfiles_present=$(python3 dividemasks_into_left_right_Nov20_2025.py  "${call_divide_a_mask_into_left_right_submasks_arguments[@]}")
}

run_CSF_COMPARTMENTS_CALC() {
  this_filename=${1}
  this_betfilename=${2}
  this_csfmaskfilename=${3}
  this_infarctmaskfilename=${4}

  echo "RUNNING NWU AND CSF VOLUME CALCULATION "

  /software/nwu_csf_volume.sh ${this_filename} ${this_betfilename} ${this_csfmaskfilename} ${this_infarctmaskfilename} 0 1000 #${lower_threshold} ${upper_threshold}
  echo "nwu_csf_volume successful" >>${output_directory}/success.txt
  thisfile_basename=$(basename $this_filename)

}

run_IML_NWU_CSF_CALC() {
  this_filename=${1}
  this_betfilename=${2}
  this_csfmaskfilename=${3}
  this_infarctmaskfilename=${4}
  echo "BET USING LEVELSET MASK"

  /software/bet_withlevelset.sh $this_filename ${this_betfilename} #${output_directory} #Helsinki2000_1019_10132014_1048_Head_2.0_ax_Tilt_1_levelset # ${3} # Helsinki2000_702_12172013_2318_Head_2.0_ax_levelset.nii.gz #${3} # $6 $7 $8 $9 ${10}

  echo "bet_withlevelset successful" >${output_directory}/success.txt
  this_filename_brain=${this_filename%.nii*}_brain_f.nii.gz
  echo "LINEAR REGISTRATION TO TEMPLATE 3"
  /software/linear_rigid_registration.sh ${this_filename_brain} #${templatefilename} #$3 ${6} WUSTL_233_11122015_0840__levelset_brain_f.nii.gz
  echo "linear_rigid_registration successful" >>${output_directory}/success.txt
  echo "RUNNING IML FSL PART"
  /software/ideal_midline_fslpart.sh ${this_filename} # ${templatefilename} ${mask_on_template}  #$9 #${10} #$8
  echo "ideal_midline_fslpart successful" >>${output_directory}/success.txt
  echo "RUNNING IML PYTHON PART"

  /software/ideal_midline_pythonpart.sh ${this_filename} #${templatefilename}  #$3 #$8 $9 ${10}
  echo "ideal_midline_pythonpart successful" >>${output_directory}/success.txt

  echo "RUNNING NWU AND CSF VOLUME CALCULATION "

  /software/nwu_csf_volume.sh ${this_filename} ${this_betfilename} ${this_csfmaskfilename} ${this_infarctmaskfilename} ${lower_threshold} ${upper_threshold}
  echo "nwu_csf_volume successful" >>${output_directory}/success.txt
  thisfile_basename=$(basename $this_filename)
  for texfile in ${output_directory}/*.tex; do
    pdflatex -halt-on-error -interaction=nonstopmode -output-directory=${output_directory} $texfile ##${output_directory}/$(/usr/lib/fsl/5.0/remove_ext $this_filename)*.tex
    rm ${output_directory}/*.aux
    rm ${output_directory}/*.log
  done

  for filetocopy in $(/usr/lib/fsl/5.0/remove_ext ${output_directory}/$thisfile_basename)*_brain_f.nii.gz; do
    cp ${filetocopy} ${final_output_directory}/
  done

  for filetocopy in $(/usr/lib/fsl/5.0/remove_ext ${output_directory}/$thisfile_basename)*.mat; do
    cp ${filetocopy} ${final_output_directory}/
  done

  for filetocopy in ${output_directory}/*.pdf; do
    cp ${filetocopy} ${final_output_directory}/
  done
  for filetocopy in ${output_directory}/*.csv; do
    cp ${filetocopy} ${final_output_directory}/
  done

}
registrationonly_each_scan() {
  local niftifilename_ext=${1}

  eachfile_basename_noext=''
  originalfile_basename=''
  original_ct_file=''
  for eachfile in ${working_dir_1}/*.nii*; do
    original_ct_file=${eachfile}
    eachfile_basename=$(basename ${eachfile})
    originalfile_basename=${eachfile_basename}
    eachfile_basename_noext=${eachfile_basename%.nii*}

    grayfilename=${eachfile_basename_noext}_resaved_levelset.nii
    if [[ "$eachfile_basename" == *".nii.gz"* ]]; then #"$STR" == *"$SUB"*
      grayfilename=${eachfile_basename_noext}_resaved_levelset.nii.gz
    fi
    betfilename=${eachfile_basename_noext}_resaved_levelset_bet.nii.gz
    cp ${working_dir}/${betfilename} ${output_directory}/
    source /software/bash_functions_forhost.sh

    cp ${original_ct_file} ${output_directory}/${grayfilename}
    grayimage=${output_directory}/${grayfilename} #${gray_output_subdir}/${eachfile_basename_noext}_resaved_levelset.nii


    levelset_bet_mask_file=${output_directory}/${betfilename}
    echo "levelset_bet_mask_file:${levelset_bet_mask_file}"
    python3 -c "

import sys ;
sys.path.append('/software/') ;
from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${original_ct_file}" "${levelset_bet_mask_file}" "${output_directory}"



    x=$grayimage
    bet_mask_filename=${output_directory}/${betfilename}
    run_Registration $x ${bet_mask_filename} #${csf_mask_filename} ${infarct_mask_filename}

  done


}

midlineonly_each_scan() {
  local niftifilename_ext=${1}

  eachfile_basename_noext=''
  originalfile_basename=''
  original_ct_file=''
  for eachfile in ${working_dir_1}/*.nii*; do
    if [[ ${eachfile} != *"levelset"* ]]; then

      original_ct_file=${eachfile}
      eachfile_basename=$(basename ${eachfile})
      originalfile_basename=${eachfile_basename}
      eachfile_basename_noext=${eachfile_basename%.nii*}

      grayfilename=${eachfile_basename_noext}_resaved_levelset.nii
      if [[ "$eachfile_basename" == *".nii.gz"* ]]; then #"$STR" == *"$SUB"*
        grayfilename=${eachfile_basename_noext}_resaved_levelset.nii.gz
      fi
      betfilename=${eachfile_basename_noext}_resaved_levelset_bet.nii.gz
      cp ${working_dir}/${betfilename} ${output_directory}/
      source /software/bash_functions_forhost.sh

      cp ${original_ct_file} ${output_directory}/${grayfilename}
      grayimage=${output_directory}/${grayfilename} #${gray_output_subdir}/${eachfile_basename_noext}_resaved_levelset.nii


      levelset_bet_mask_file=${output_directory}/${betfilename}
      echo "levelset_bet_mask_file:${levelset_bet_mask_file}"
      python3 -c "

import sys ;
sys.path.append('/software/') ;
from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${original_ct_file}" "${levelset_bet_mask_file}" "${output_directory}"



      x=$grayimage
      bet_mask_filename=${output_directory}/${betfilename}
      run_IML $x ${bet_mask_filename} #${csf_mask_filename} ${infarct_mask_filename}
    fi
  done


}
split_masks_into_two_halves() {

  eachfile_basename_noext=''
  originalfile_basename=''
  original_ct_file=''
  maskfile_extension=${1}
  for eachfile in ${working_dir_1}/*.nii*; do
    if  [[ ${eachfile} != *"levelset"* ]] ; then
    original_ct_file=${eachfile}
    eachfile_basename=$(basename ${eachfile})
    originalfile_basename=${eachfile_basename}
    eachfile_basename_noext=${eachfile_basename%.nii*}
    grayfilename=${eachfile_basename_noext}_resaved_levelset.nii
    if [[ "$eachfile_basename" == *".nii.gz"* ]]; then #"$STR" == *"$SUB"*
      grayfilename=${eachfile_basename_noext}_resaved_levelset.nii.gz
    fi
    csffilename=${eachfile_basename_noext}${maskfile_extension} #_resaved_csf_unet.nii.gz
    cp ${working_dir}/${csffilename} ${output_directory}/
    source /software/bash_functions_forhost.sh

    cp ${original_ct_file} ${output_directory}/${grayfilename}
    grayimage=${output_directory}/${grayfilename} #${gray_output_subdir}/${eachfile_basename_noext}_resaved_levelset.nii
    levelset_csf_mask_file=${output_directory}/${csffilename}
    echo "levelset_csf_mask_file:${levelset_csf_mask_file}"
    python3 -c "
import sys ;
sys.path.append('/software/') ;
from utilities_simple_trimmed import * ;   levelset2originalRF_new_flip()" "${original_ct_file}" "${levelset_csf_mask_file}" "${output_directory}"
    templatefilename=scct_strippedResampled1.nii.gz
    mask_on_template=midlinecssfResampled1.nii.gz
    csf_mask_filename=${output_directory}/${csffilename}
    echo  " I AM HERE run_divide_mask_into_left_right ${grayimage} ${csf_mask_filename} ${output_directory} ${working_dir} "
    run_divide_mask_into_left_right ${grayimage} ${csf_mask_filename} ${output_directory} ${working_dir}
    fi
  done

}
nwucalculation_each_scan() {

  eachfile_basename_noext=''
  originalfile_basename=''
  original_ct_file=''
  for eachfile in ${working_dir_1}/*.nii*; do
    original_ct_file=${eachfile}
    eachfile_basename=$(basename ${eachfile})
    originalfile_basename=${eachfile_basename}
    eachfile_basename_noext=${eachfile_basename%.nii*}

    grayfilename=${eachfile_basename_noext}_resaved_levelset.nii
    if [[ "$eachfile_basename" == *".nii.gz"* ]]; then #"$STR" == *"$SUB"*
      grayfilename=${eachfile_basename_noext}_resaved_levelset.nii.gz
    fi
    betfilename=${eachfile_basename_noext}_resaved_levelset_bet.nii.gz
    csffilename=${eachfile_basename_noext}_resaved_csf_unet.nii.gz

    infarctfilename=${eachfile_basename_noext}_resaved_infarct_auto_removesmall.nii.gz
    cp ${working_dir}/${betfilename} ${output_directory}/
    cp ${working_dir}/${csffilename} ${output_directory}/
    cp ${working_dir}/${infarctfilename} ${output_directory}/
    source /software/bash_functions_forhost.sh

    cp ${original_ct_file} ${output_directory}/${grayfilename}
    grayimage=${output_directory}/${grayfilename} #${gray_output_subdir}/${eachfile_basename_noext}_resaved_levelset.nii


    levelset_infarct_mask_file=${output_directory}/${infarctfilename}
    echo "levelset_infarct_mask_file:${levelset_infarct_mask_file}"
    python3 -c "
import sys ;
sys.path.append('/software/') ;
from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${original_ct_file}" "${levelset_infarct_mask_file}" "${output_directory}"

    levelset_bet_mask_file=${output_directory}/${betfilename}
    echo "levelset_bet_mask_file:${levelset_bet_mask_file}"
    python3 -c "

import sys ;
sys.path.append('/software/') ;
from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${original_ct_file}" "${levelset_bet_mask_file}" "${output_directory}"

    levelset_csf_mask_file=${output_directory}/${csffilename}
    echo "levelset_csf_mask_file:${levelset_csf_mask_file}"
    python3 -c "
import sys ;
sys.path.append('/software/') ;
from utilities_simple_trimmed import * ;   levelset2originalRF_new_flip()" "${original_ct_file}" "${levelset_csf_mask_file}" "${output_directory}"

    lower_threshold=0
    upper_threshold=20
    templatefilename=scct_strippedResampled1.nii.gz
    mask_on_template=midlinecssfResampled1.nii.gz

    x=$grayimage
    bet_mask_filename=${output_directory}/${betfilename}
    infarct_mask_filename=${output_directory}/${infarctfilename}
    csf_mask_filename=${output_directory}/${csffilename}
    run_IML_NWU_CSF_CALC $x ${bet_mask_filename} ${csf_mask_filename} ${infarct_mask_filename}

  done


}



calculate_left_right_ratio() {
  local lefthalf_file=${1}
  local righthalf_file=${2}
  local grayscale_filename_basename_noext=${3}
  local column_name_this=$(basename ${lefthalf_file})
  local column_name_this=${column_name_this##*${grayscale_filename_basename_noext}_resaved_}
  local column_name_this=${column_name_this%_half_originalRF*}
  local column_name_this=${column_name_this%_left*}_RATIO
  local filename_to_write=${output_directory}/$(basename ${lefthalf_file%.nii*})_RATIO.csv
  local call_ratio_left_right_arguments=('call_ratio_left_right' ${lefthalf_file} ${righthalf_file} ${column_name_this} ${filename_to_write})
  local outputfiles_present=$(python3 dividemasks_into_left_right_Nov20_2025.py "${call_ratio_left_right_arguments[@]}")
  echo outputfiles_present::${outputfiles_present}
}

calculate_volume() {
  local column_name=${2}

  local mask_file=${1} ##$(ls ${working_dir}/*${maskfile_extension_no_nii}_${2}_half_originalRF.nii.gz)
  local mask_file_basename=$(basename ${mask_file})
  local mask_file_basename=${mask_file_basename%.nii*}
  local filename_to_write=${output_directory}/${mask_file_basename}.csv
  local call_calculate_volume_arguments=('call_calculate_volume' ${mask_file} ${column_name} ${filename_to_write})
  local outputfiles_present=$(python3 dividemasks_into_left_right_Nov20_2025.py "${call_calculate_volume_arguments[@]}")
  echo outputfiles_present::${outputfiles_present}
}
call_calculate_volume() {
  local mask_filename=${1}
  local grayscale_filename_basename_noext=${2}
  local column_name_this=$(basename ${mask_filename})
  local column_name_this=${column_name_this##*${grayscale_filename_basename_noext}_resaved_}
  local column_name_this=${column_name_this%_half_originalRF*}
  calculate_volume ${mask_filename} ${column_name_this}
}
call_calculate_volume_mask_from_yasheng() {
  local mask_filename=${1}
  local original_nifti_file=${2}
  local grayscale_filename_basename_noext=$(basename ${original_nifti_file%.nii*})
  local mask_file_basename=$(basename ${mask_filename})
  local mask_file_basename=${mask_file_basename%.nii*}
  local filename_to_write=${output_directory}/${mask_file_basename}.csv
  local column_name_this=$(basename ${mask_filename%.nii*})
  local column_name_this=${column_name_this##*${grayscale_filename_basename_noext}_resaved_} #_TOTAL
  local call_calculate_volume_mask_from_yasheng_arguments=('call_calculate_volume_mask_from_yasheng' ${mask_filename} ${original_nifti_file} ${column_name_this} ${filename_to_write})
  local outputfiles_present=$(python3 dividemasks_into_left_right_Nov20_2025.py "${call_calculate_volume_mask_from_yasheng_arguments[@]}")
  echo outputfiles_present::${outputfiles_present}

}
mask_subtraction() {
  local mask_donor=${1}
  local mask_tobe_subtracted=${2}
  local output_mask_dir=${3}
  local mask_donor_basename=$(basename ${mask_donor})
  local mask_donor_basename=${mask_donor_basename%.nii*}
  local mask_tobe_subtracted_extension=${mask_tobe_subtracted##*.}
  local mask_tobe_subtracted_basename=$(basename ${mask_tobe_subtracted})
  local mask_tobe_subtracted_basename=${mask_tobe_subtracted_basename%.nii*}
  local output_mask_file=${output_mask_dir}/${mask_donor_basename}_WITHOUT_${mask_tobe_subtracted_basename}.nii.gz
  call_masks_subtraction_arguments=('call_masks_subtraction' ${mask_donor} ${mask_tobe_subtracted} ${output_mask_file})
  outputfiles_present=$(python3 dividemasks_into_left_right_Nov20_2025.py "${call_masks_subtraction_arguments[@]}")
  echo outputfiles_present::${outputfiles_present}
}
overlapped_mask_on_otherimage() {
  local grayscale_filename_1=${1}
  local contrast_limits=${2}
  local outputfile_dir=${3}
  local outputfile_suffix=${4}
  local color_list=${5}
  local working_dir_1=${6}
  local -n mask_filename=${7}
  local call_masks_on_grayscale_colored_arguments=('call_masks_on_grayscale_colored' ${grayscale_filename_1} ${contrast_limits} ${outputfile_dir} ${outputfile_suffix} ${color_list} ${working_dir_1} ${mask_filename[@]})
  local outputfiles_present=$(python3 dividemasks_into_left_right_Nov20_2025.py "${call_masks_on_grayscale_colored_arguments[@]}")
  echo outputfiles_present::${outputfiles_present}

}

echo " I AM RUNNING "


#function get_scanID_from_sessionID() {
#  local sessionID=$1
#  local working_dir=$2
#  local URI="/data/experiments/${sessionID}"
#  local resource_dir="NIFTI_LOCATION"
#  local output_csvfile="${sessionID}_SCANSELECTION_METADATA.csv"
#
#  call_get_resourcefiles_metadata_saveascsv_args ${URI} ${resource_dir} ${working_dir} ${output_csvfile}
#
#  local niftifile_csvfilename=$(ls ${working_dir}/*NIFTILOCATION.csv)
#  scanID=$(tail -n +2 "${niftifile_csvfilename}" | cut -d',' -f3 | head -n 1)
#  echo ${scanID}
#}

#URI="/data/experiments/${sessionID}"
#resource_dir="NIFTI_LOCATION"
#output_csvfile="${sessionID}_SCANSELECTION_METADATA.csv"
#call_get_resourcefiles_metadata_saveascsv_args ${URI} ${resource_dir} ${working_dir} ${output_csvfile}


#URI=/data/experiments/${sessionID}

#resource_dir="NIFTI_LOCATION"
#output_csvfile=${sessionID}_SCANSELECTION_METADATA.csv
#call_get_resourcefiles_metadata_saveascsv_args ${URI} ${resource_dir} ${working_dir} ${output_csvfile}
dir_to_save=${working_dir}

greyfile="NONE" ##'/media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/CSFSEPERATION/TESTING_CSF_SEPERATION/Krak_003_09042014_0949_MOZG_6.0_H31s_levelset.nii.gz'
betfile="NONE"  ##'/media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/CSFSEPERATION/TESTING_CSF_SEPERATION/Krak_003_09042014_0949_MOZG_6.0_H31s_levelset_bet.nii.gz'
csffile="NONE"  ##'/media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/CSFSEPERATION/TESTING_CSF_SEPERATION/Krak_003_09042014_0949_MOZG_6.0_H31s_final_seg.nii.gz'
NIFTI_SCAN_URI=''

cp /EDEMABIOMARKEROUTPUT/*_infarct.png ${output_directory}/
cp /EDEMABIOMARKEROUTPUT/*columndropped.csv ${output_directory}/
for each_npy in  $(find /input/SCANS/2/PREPROCESS_SEGM_3/ -name '*.npy') ;  do  if [[ $each_npy  == *'V2'* ]] ; then  cp $each_npy ${working_dir_1} ; fi ; done
 for each_npy in  $(find /input/SCANS/2/PREPROCESS_SEGM_3/ -name '*.npy') ;  do  if [[ $each_npy  == *'.npy'* ]] ; then  cp $each_npy ${output_directory} ; fi ; done
    split_masks_into_two_halves "_resaved_levelset_sulci_total.nii.gz"
    split_masks_into_two_halves "_resaved_levelset_sulci_above_ventricle.nii.gz"
    split_masks_into_two_halves "_resaved_levelset_sulci_at_ventricle.nii.gz"
    split_masks_into_two_halves "_resaved_levelset_sulci_below_ventricle.nii.gz"
    split_masks_into_two_halves "_resaved_levelset_ventricle_total.nii.gz"
    split_masks_into_two_halves "_resaved_levelset_bet.nii.gz"
    split_masks_into_two_halves "_resaved_levelset_ventricle_cistern.nii.gz"

filename_nifti=$(basename $(ls ${working_dir_1}/*.nii))
    split_masks_into_two_halves "_resaved_csf_unet.nii.gz"
    split_masks_into_two_halves "_resaved_infarct_auto_removesmall.nii.gz"
    grayscale_filename=${working_dir_1}/${filename_nifti}

    grayscale_filename_basename=$(basename ${grayscale_filename})
    grayscale_filename_basename_noext=${grayscale_filename_basename%.nii*}
    echo ${grayscale_filename_basename_noext}
    grayscale_filename_basename_ext=${grayscale_filename_basename##*.}
    call_slice_num_to_csv_arguments=('call_slice_num_to_csv' ${grayscale_filename} SLICE_NUM ${output_directory}/${grayscale_filename_basename_noext}_SLICE_NUM.csv)
    outputfiles_present=$(python3 dividemasks_into_left_right_Nov20_2025.py "${call_slice_num_to_csv_arguments[@]}")
    grayscale_filename_1=${working_dir_1}/${grayscale_filename_basename_noext}_resaved_levelset.${grayscale_filename_basename_ext}
    cp ${grayscale_filename} ${grayscale_filename_1}
    latexfilename_prefix=${grayscale_filename%.nii*}
    latexfilename=${latexfilename_prefix}_${outputfiles_suffix}.tex
    csvfilename=${latexfilename_prefix}_${outputfiles_suffix}.csv
    call_latex_start_arguments=('call_latex_start' ${latexfilename})
    outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_latex_start_arguments[@]}")
    contrast_limits=0_200 ##(args.stuff[2].split('_')[0],args.stuff[2].split('_')[1])
    outputfile_dir=${output_directory}
    grayscale_left_half=${working_dir}/${grayscale_filename_basename_noext}_resaved_levelset_left_half_originalRF.nii.gz
    grayscale_right_half=${working_dir}/${grayscale_filename_basename_noext}_resaved_levelset_right_half_originalRF.nii.gz
    mask_filename1=${working_dir}/${grayscale_filename_basename_noext}_resaved_levelset_bet_left_half_originalRF.nii.gz
    mask_filename2=${working_dir}/${grayscale_filename_basename_noext}_resaved_levelset_bet_right_half_originalRF.nii.gz
    mask_filename3=${working_dir}/${grayscale_filename_basename_noext}_resaved_csf_unet_left_half_originalRF.nii.gz
    mask_filename4=${working_dir}/${grayscale_filename_basename_noext}_resaved_csf_unet_right_half_originalRF.nii.gz


    mask_filename3_1=${working_dir}/${grayscale_filename_basename_noext}_resaved_levelset_ventricle_total_left_half_originalRF.nii.gz
    mask_filename4_1=${working_dir}/${grayscale_filename_basename_noext}_resaved_levelset_ventricle_total_right_half_originalRF.nii.gz
    mask_filename5=${working_dir}/${grayscale_filename_basename_noext}_resaved_levelset_sulci_above_ventricle_left_half_originalRF.nii.gz
    mask_filename6=${working_dir}/${grayscale_filename_basename_noext}_resaved_levelset_sulci_above_ventricle_right_half_originalRF.nii.gz
    mask_filename7=${working_dir}/${grayscale_filename_basename_noext}_resaved_levelset_sulci_at_ventricle_left_half_originalRF.nii.gz
    mask_filename8=${working_dir}/${grayscale_filename_basename_noext}_resaved_levelset_sulci_at_ventricle_right_half_originalRF.nii.gz
    mask_filename9=${working_dir}/${grayscale_filename_basename_noext}_resaved_levelset_sulci_below_ventricle_left_half_originalRF.nii.gz
    mask_filename10=${working_dir}/${grayscale_filename_basename_noext}_resaved_levelset_sulci_below_ventricle_right_half_originalRF.nii.gz

#    mask_filename11=${working_dir}/${grayscale_filename_basename_noext}_resaved_4DL_seg_sulcal_right_half_originalRF.nii.gz
#    mask_filename12=${working_dir}/${grayscale_filename_basename_noext}_resaved_4DL_seg_sulcal_left_half_originalRF.nii.gz
#    mask_filename13=${working_dir}/${grayscale_filename_basename_noext}_resaved_4DL_seg_ventri_right_half_originalRF.nii.gz
#    mask_filename14=${working_dir}/${grayscale_filename_basename_noext}_resaved_4DL_seg_ventri_left_half_originalRF.nii.gz
#    mask_filename15=${working_dir}/${grayscale_filename_basename_noext}_resaved_4DL_seg_cistern_right_half_originalRF.nii.gz
#    mask_filename16=${working_dir}/${grayscale_filename_basename_noext}_resaved_4DL_seg_cistern_left_half_originalRF.nii.gz
#    mask_filename17=${working_dir}/${grayscale_filename_basename_noext}_resaved_4DL_seg_total_right_half_originalRF.nii.gz
#    mask_filename18=${working_dir}/${grayscale_filename_basename_noext}_resaved_4DL_seg_total_left_half_originalRF.nii.gz

    mask_filename19=${working_dir}/${grayscale_filename_basename_noext}_resaved_levelset_bet.nii.gz
    mask_filename20=${working_dir}/${grayscale_filename_basename_noext}_resaved_csf_unet.nii.gz

    mask_filename21=${working_dir}/${grayscale_filename_basename_noext}_resaved_levelset_sulci_above_ventricle.nii.gz
    mask_filename22=${working_dir}/${grayscale_filename_basename_noext}_resaved_levelset_sulci_at_ventricle.nii.gz
    mask_filename23=${working_dir}/${grayscale_filename_basename_noext}_resaved_levelset_sulci_below_ventricle.nii.gz
    mask_filename24=${working_dir}/${grayscale_filename_basename_noext}_resaved_levelset_ventricle_total.nii.gz
#    mask_filename25=${working_dir}/${grayscale_filename_basename_noext}_resaved_4DL_seg_sulcal.nii.gz
#    mask_filename26=${working_dir}/${grayscale_filename_basename_noext}_resaved_4DL_seg_ventri.nii.gz
#    mask_filename27=${working_dir}/${grayscale_filename_basename_noext}_resaved_4DL_seg_cistern.nii.gz
#    mask_filename28=${working_dir}/${grayscale_filename_basename_noext}_resaved_4DL_seg_total.nii.gz
    mask_filename29=${working_dir}/${grayscale_filename_basename_noext}_resaved_levelset_ventricle_cistern.nii.gz
    mask_filename30=${working_dir}/${grayscale_filename_basename_noext}_resaved_levelset_ventricle_cistern_right_half_originalRF.nii.gz
    mask_filename31=${working_dir}/${grayscale_filename_basename_noext}_resaved_levelset_ventricle_cistern_left_half_originalRF.nii.gz
    mask_filename32=${working_dir}/${grayscale_filename_basename_noext}_resaved_infarct_auto_removesmall_right_half_originalRF.nii.gz
    mask_filename33=${working_dir}/${grayscale_filename_basename_noext}_resaved_infarct_auto_removesmall_left_half_originalRF.nii.gz
    mask_filename34=${working_dir}/${grayscale_filename_basename_noext}_resaved_infarct_auto_removesmall.nii.gz

#_resaved_infarct_auto_removesmall.nii.gz
    calculate_left_right_ratio ${mask_filename3} ${mask_filename4} ${grayscale_filename_basename_noext}
    mask_subtraction ${mask_filename19} ${mask_filename20} ${working_dir}
    bet_mask_WITHOUT_csf=$(ls ${working_dir}/*_resaved_levelset_bet*WITHOUT*csf_unet*)
    column_name_this="bet_mask_WITHOUT_csf"
    filename_to_write=${output_directory}/${grayscale_filename_basename_noext}_bet_mask_WITHOUT_csf.csv
    call_calculate_volume_mask_from_yasheng_arguments=('call_calculate_volume_mask_from_yasheng' ${bet_mask_WITHOUT_csf} ${grayscale_filename} ${column_name_this} ${filename_to_write})
    outputfiles_present=$(python3 dividemasks_into_left_right_Nov20_2025.py "${call_calculate_volume_mask_from_yasheng_arguments[@]}")
  echo "call_calculate_volume_mask_from_yasheng::${mask_filename19}::${grayscale_filename}" >> /software/error.txt
call_calculate_volume_mask_from_yasheng ${mask_filename19} ${grayscale_filename}
call_calculate_volume_mask_from_yasheng ${mask_filename34} ${grayscale_filename}
echo "call_calculate_volume_mask_from_yasheng::${mask_filename20}::${grayscale_filename}" >> /software/error.txt
call_calculate_volume_mask_from_yasheng ${mask_filename20} ${grayscale_filename}

echo "call_calculate_volume_mask_from_yasheng::${mask_filename21}::${grayscale_filename}" >> /software/error.txt
call_calculate_volume_mask_from_yasheng ${mask_filename21} ${grayscale_filename}

echo "call_calculate_volume_mask_from_yasheng::${mask_filename22}::${grayscale_filename}" >> /software/error.txt
call_calculate_volume_mask_from_yasheng ${mask_filename22} ${grayscale_filename}

echo "call_calculate_volume_mask_from_yasheng::${mask_filename23}::${grayscale_filename}" >> /software/error.txt
call_calculate_volume_mask_from_yasheng ${mask_filename23} ${grayscale_filename}

echo "call_calculate_volume_mask_from_yasheng::${mask_filename24}::${grayscale_filename}" >> /software/error.txt
call_calculate_volume_mask_from_yasheng ${mask_filename24} ${grayscale_filename}

#echo "call_calculate_volume_mask_from_yasheng::${mask_filename25}::${grayscale_filename}" >> /software/error.txt
#call_calculate_volume_mask_from_yasheng ${mask_filename25} ${grayscale_filename}
#
#echo "call_calculate_volume_mask_from_yasheng::${mask_filename26}::${grayscale_filename}" >> /software/error.txt
#call_calculate_volume_mask_from_yasheng ${mask_filename26} ${grayscale_filename}
#
#echo "call_calculate_volume_mask_from_yasheng::${mask_filename27}::${grayscale_filename}" >> /software/error.txt
#call_calculate_volume_mask_from_yasheng ${mask_filename27} ${grayscale_filename}
#
#echo "call_calculate_volume_mask_from_yasheng::${mask_filename28}::${grayscale_filename}" >> /software/error.txt
#call_calculate_volume_mask_from_yasheng ${mask_filename28} ${grayscale_filename}

echo "call_calculate_volume_mask_from_yasheng::${mask_filename30}::${grayscale_filename}" >> /software/error.txt
call_calculate_volume_mask_from_yasheng ${mask_filename30} ${grayscale_filename}

echo "call_calculate_volume_mask_from_yasheng::${mask_filename31}::${grayscale_filename}" >> /software/error.txt
call_calculate_volume_mask_from_yasheng ${mask_filename31} ${grayscale_filename}


echo "call_calculate_volume::${mask_filename1}::${grayscale_filename_basename_noext}" >> /software/error.txt
call_calculate_volume ${mask_filename1} ${grayscale_filename_basename_noext}

echo "call_calculate_volume::${mask_filename3_1}::${grayscale_filename_basename_noext}" >> /software/error.txt
call_calculate_volume ${mask_filename3_1} ${grayscale_filename_basename_noext}

echo "call_calculate_volume::${mask_filename4_1}::${grayscale_filename_basename_noext}" >> /software/error.txt
call_calculate_volume ${mask_filename4_1} ${grayscale_filename_basename_noext}


echo "call_calculate_volume::${mask_filename2}::${grayscale_filename_basename_noext}" >> /software/error.txt
call_calculate_volume ${mask_filename2} ${grayscale_filename_basename_noext}

echo "call_calculate_volume::${mask_filename3}::${grayscale_filename_basename_noext}" >> /software/error.txt
call_calculate_volume ${mask_filename3} ${grayscale_filename_basename_noext}

echo "call_calculate_volume::${mask_filename4}::${grayscale_filename_basename_noext}" >> /software/error.txt
call_calculate_volume ${mask_filename4} ${grayscale_filename_basename_noext}

echo "call_calculate_volume::${mask_filename5}::${grayscale_filename_basename_noext}" >> /software/error.txt
call_calculate_volume ${mask_filename5} ${grayscale_filename_basename_noext}

echo "call_calculate_volume::${mask_filename6}::${grayscale_filename_basename_noext}" >> /software/error.txt
call_calculate_volume ${mask_filename6} ${grayscale_filename_basename_noext}

echo "call_calculate_volume::${mask_filename7}::${grayscale_filename_basename_noext}" >> /software/error.txt
call_calculate_volume ${mask_filename7} ${grayscale_filename_basename_noext}

echo "call_calculate_volume::${mask_filename8}::${grayscale_filename_basename_noext}" >> /software/error.txt
call_calculate_volume ${mask_filename8} ${grayscale_filename_basename_noext}

echo "call_calculate_volume::${mask_filename9}::${grayscale_filename_basename_noext}" >> /software/error.txt
call_calculate_volume ${mask_filename9} ${grayscale_filename_basename_noext}

echo "call_calculate_volume::${mask_filename10}::${grayscale_filename_basename_noext}" >> /software/error.txt
call_calculate_volume ${mask_filename10} ${grayscale_filename_basename_noext}


#echo "call_calculate_volume::${mask_filename11}::${grayscale_filename_basename_noext}" >> /software/error.txt
#call_calculate_volume ${mask_filename11} ${grayscale_filename_basename_noext}
#
#echo "call_calculate_volume::${mask_filename12}::${grayscale_filename_basename_noext}" >> /software/error.txt
#call_calculate_volume ${mask_filename12} ${grayscale_filename_basename_noext}
#
#echo "call_calculate_volume::${mask_filename13}::${grayscale_filename_basename_noext}" >> /software/error.txt
#call_calculate_volume ${mask_filename13} ${grayscale_filename_basename_noext}
#
#echo "call_calculate_volume::${mask_filename14}::${grayscale_filename_basename_noext}" >> /software/error.txt
#call_calculate_volume ${mask_filename14} ${grayscale_filename_basename_noext}
#
#echo "call_calculate_volume::${mask_filename15}::${grayscale_filename_basename_noext}" >> /software/error.txt
#call_calculate_volume ${mask_filename15} ${grayscale_filename_basename_noext}
#
#echo "call_calculate_volume::${mask_filename16}::${grayscale_filename_basename_noext}" >> /software/error.txt
#call_calculate_volume ${mask_filename16} ${grayscale_filename_basename_noext}
#
#echo "call_calculate_volume::${mask_filename17}::${grayscale_filename_basename_noext}" >> /software/error.txt
#call_calculate_volume ${mask_filename17} ${grayscale_filename_basename_noext}
#
#echo "call_calculate_volume::${mask_filename18}::${grayscale_filename_basename_noext}" >> /software/error.txt
#call_calculate_volume ${mask_filename18} ${grayscale_filename_basename_noext}

echo "call_calculate_volume::${mask_filename29}::${grayscale_filename_basename_noext}" >> /software/error.txt
call_calculate_volume ${mask_filename29} ${grayscale_filename_basename_noext}

    call_calculate_volume_mask_from_yasheng ${mask_filename19} ${grayscale_filename}
    call_calculate_volume_mask_from_yasheng ${mask_filename20} ${grayscale_filename} # "csf_sulci_above_ventricle_TOTAL"
    call_calculate_volume_mask_from_yasheng ${mask_filename21} ${grayscale_filename} #"csf_sulci_at_ventricle_TOTAL"
    call_calculate_volume_mask_from_yasheng ${mask_filename22} ${grayscale_filename} # "csf_sulci_below_ventricle_TOTAL"
    call_calculate_volume_mask_from_yasheng ${mask_filename23} ${grayscale_filename} #"csf_ventricle_TOTAL"
    call_calculate_volume_mask_from_yasheng ${mask_filename24} ${grayscale_filename} #"total_ventricle"
#    call_calculate_volume_mask_from_yasheng ${mask_filename25} ${grayscale_filename} #"SAH_VENTRICLE_TOTAL"
#    call_calculate_volume_mask_from_yasheng ${mask_filename26} ${grayscale_filename} #"SAH_cistern_TOTAL"
#    call_calculate_volume_mask_from_yasheng ${mask_filename27} ${grayscale_filename} # "SAH_TOTAL"
#    call_calculate_volume_mask_from_yasheng ${mask_filename28} ${grayscale_filename} # "SAH_TOTAL"
    call_calculate_volume_mask_from_yasheng ${mask_filename30} ${grayscale_filename} # "cistern only"
    call_calculate_volume_mask_from_yasheng ${mask_filename31} ${grayscale_filename} # "cistern only"


    call_calculate_volume ${mask_filename1} ${grayscale_filename_basename_noext}
    call_calculate_volume ${mask_filename2} ${grayscale_filename_basename_noext}
    call_calculate_volume ${mask_filename3} ${grayscale_filename_basename_noext}
    call_calculate_volume ${mask_filename4} ${grayscale_filename_basename_noext}
    call_calculate_volume ${mask_filename5} ${grayscale_filename_basename_noext}
    call_calculate_volume ${mask_filename6} ${grayscale_filename_basename_noext}
    call_calculate_volume ${mask_filename7} ${grayscale_filename_basename_noext}
    call_calculate_volume ${mask_filename8} ${grayscale_filename_basename_noext}
    call_calculate_volume ${mask_filename9} ${grayscale_filename_basename_noext}
    call_calculate_volume ${mask_filename10} ${grayscale_filename_basename_noext}

#    call_calculate_volume ${mask_filename11} ${grayscale_filename_basename_noext}
#    call_calculate_volume ${mask_filename12} ${grayscale_filename_basename_noext}
#    call_calculate_volume ${mask_filename13} ${grayscale_filename_basename_noext}
#    call_calculate_volume ${mask_filename14} ${grayscale_filename_basename_noext}
#    call_calculate_volume ${mask_filename15} ${grayscale_filename_basename_noext}
#    call_calculate_volume ${mask_filename16} ${grayscale_filename_basename_noext}
#    call_calculate_volume ${mask_filename17} ${grayscale_filename_basename_noext}
#    call_calculate_volume ${mask_filename18} ${grayscale_filename_basename_noext}
    call_calculate_volume ${mask_filename29} ${grayscale_filename_basename_noext}
    call_combine_csv_horizontally_arguments=('call_combine_csv_horizontally' ${grayscale_filename_basename_noext} ${csvfilename} ${output_directory}/${grayscale_filename_basename_noext}_SESSION_LABEL.csv)
    outputfiles_present=$(python3 dividemasks_into_left_right_Nov20_2025.py "${call_combine_csv_horizontally_arguments[@]}")

    call_insert_one_col_with_colname_colidx_arguments=('call_insert_one_col_with_colname_colidx' ${csvfilename} ${csvfilename} "FILENAME" ${grayscale_filename_basename_noext}) # ${csvfilename} ${csvfilename} ${output_directory}/$(basename ${mask_filename3%.nii*})_RATIO.csv )
    outputfiles_present=$(python3 dividemasks_into_left_right_Nov20_2025.py "${call_insert_one_col_with_colname_colidx_arguments[@]}")
        call_insert_one_col_with_colname_colidx_arguments=('call_insert_one_col_with_colname_colidx' ${csvfilename} ${csvfilename} "SESSION_ID" ${sessionID}) # ${csvfilename} ${csvfilename} ${output_directory}/$(basename ${mask_filename3%.nii*})_RATIO.csv )
        outputfiles_present=$(python3 dividemasks_into_left_right_Nov20_2025.py "${call_insert_one_col_with_colname_colidx_arguments[@]}")

    call_combine_csv_horizontally_arguments=('call_combine_csv_horizontally' ${grayscale_filename_basename_noext} ${csvfilename} ${csvfilename} ${output_directory}/${grayscale_filename_basename_noext}_SLICE_NUM.csv) # ${output_directory}/${grayscale_filename_basename_noext}_bet_mask_WITHOUT_csf.csv ${output_directory}/$(basename ${mask_filename1%.nii*}.csv) ${output_directory}/$(basename ${mask_filename2%.nii*}.csv) ${output_directory}/$(basename ${mask_filename3%.nii*}.csv) ${output_directory}/$(basename ${mask_filename4%.nii*}.csv) ${output_directory}/$(basename ${mask_filename5%.nii*}.csv) ${output_directory}/$(basename ${mask_filename6%.nii*}.csv) ${output_directory}/$(basename ${mask_filename7%.nii*}.csv) ${output_directory}/$(basename ${mask_filename8%.nii*}.csv) ${output_directory}/$(basename ${mask_filename9%.nii*}.csv) ${output_directory}/$(basename ${mask_filename10%.nii*}.csv) ${output_directory}/$(basename ${mask_filename11%.nii*}.csv) ${output_directory}/$(basename ${mask_filename12%.nii*}.csv) ${output_directory}/$(basename ${mask_filename13%.nii*}.csv) ${output_directory}/$(basename ${mask_filename14%.nii*}.csv) ${output_directory}/$(basename ${mask_filename15%.nii*}.csv) ${output_directory}/$(basename ${mask_filename16%.nii*}.csv) ${output_directory}/$(basename ${mask_filename17%.nii*}.csv) ${output_directory}/$(basename ${mask_filename18%.nii*}.csv) ${output_directory}/$(basename ${mask_filename19%.nii*}.csv) ${output_directory}/$(basename ${mask_filename20%.nii*}.csv) ${output_directory}/$(basename ${mask_filename21%.nii*}.csv) ${output_directory}/$(basename ${mask_filename22%.nii*}.csv) ${output_directory}/$(basename ${mask_filename23%.nii*}.csv) ${output_directory}/$(basename ${mask_filename24%.nii*}.csv) ${output_directory}/$(basename ${mask_filename25%.nii*}.csv) ${output_directory}/$(basename ${mask_filename26%.nii*}.csv) ${output_directory}/$(basename ${mask_filename27%.nii*}.csv) ${output_directory}/$(basename ${mask_filename28%.nii*}.csv))
    outputfiles_present=$(python3 dividemasks_into_left_right_Nov20_2025.py "${call_combine_csv_horizontally_arguments[@]}")
    call_combine_csv_horizontally_arguments=('call_combine_csv_horizontally' ${grayscale_filename_basename_noext} ${csvfilename} ${csvfilename} ${output_directory}/$(basename ${mask_filename3%.nii*})_RATIO.csv) # ${output_directory}/${grayscale_filename_basename_noext}_bet_mask_WITHOUT_csf.csv ${output_directory}/$(basename ${mask_filename1%.nii*}.csv) ${output_directory}/$(basename ${mask_filename2%.nii*}.csv) ${output_directory}/$(basename ${mask_filename3%.nii*}.csv) ${output_directory}/$(basename ${mask_filename4%.nii*}.csv) ${output_directory}/$(basename ${mask_filename5%.nii*}.csv) ${output_directory}/$(basename ${mask_filename6%.nii*}.csv) ${output_directory}/$(basename ${mask_filename7%.nii*}.csv) ${output_directory}/$(basename ${mask_filename8%.nii*}.csv) ${output_directory}/$(basename ${mask_filename9%.nii*}.csv) ${output_directory}/$(basename ${mask_filename10%.nii*}.csv) ${output_directory}/$(basename ${mask_filename11%.nii*}.csv) ${output_directory}/$(basename ${mask_filename12%.nii*}.csv) ${output_directory}/$(basename ${mask_filename13%.nii*}.csv) ${output_directory}/$(basename ${mask_filename14%.nii*}.csv) ${output_directory}/$(basename ${mask_filename15%.nii*}.csv) ${output_directory}/$(basename ${mask_filename16%.nii*}.csv) ${output_directory}/$(basename ${mask_filename17%.nii*}.csv) ${output_directory}/$(basename ${mask_filename18%.nii*}.csv) ${output_directory}/$(basename ${mask_filename19%.nii*}.csv) ${output_directory}/$(basename ${mask_filename20%.nii*}.csv) ${output_directory}/$(basename ${mask_filename21%.nii*}.csv) ${output_directory}/$(basename ${mask_filename22%.nii*}.csv) ${output_directory}/$(basename ${mask_filename23%.nii*}.csv) ${output_directory}/$(basename ${mask_filename24%.nii*}.csv) ${output_directory}/$(basename ${mask_filename25%.nii*}.csv) ${output_directory}/$(basename ${mask_filename26%.nii*}.csv) ${output_directory}/$(basename ${mask_filename27%.nii*}.csv) ${output_directory}/$(basename ${mask_filename28%.nii*}.csv))
    outputfiles_present=$(python3 dividemasks_into_left_right_Nov20_2025.py "${call_combine_csv_horizontally_arguments[@]}")

    call_combine_csv_horizontally_arguments=('call_combine_csv_horizontally' ${grayscale_filename_basename_noext} ${csvfilename} ${csvfilename} ${output_directory}/${grayscale_filename_basename_noext}_bet_mask_WITHOUT_csf.csv ${output_directory}/$(basename ${mask_filename1%.nii*}.csv)
    ${output_directory}/$(basename ${mask_filename34%.nii*}.csv)
    ${output_directory}/$(basename ${mask_filename2%.nii*}.csv)
    ${output_directory}/$(basename ${mask_filename3%.nii*}.csv)
    ${output_directory}/$(basename ${mask_filename4%.nii*}.csv)
    ${output_directory}/$(basename ${mask_filename5%.nii*}.csv)
    ${output_directory}/$(basename ${mask_filename6%.nii*}.csv)
    ${output_directory}/$(basename ${mask_filename7%.nii*}.csv)
    ${output_directory}/$(basename ${mask_filename8%.nii*}.csv)
    ${output_directory}/$(basename ${mask_filename9%.nii*}.csv)
    ${output_directory}/$(basename ${mask_filename10%.nii*}.csv)
#    ${output_directory}/$(basename ${mask_filename11%.nii*}.csv)
#    ${output_directory}/$(basename ${mask_filename12%.nii*}.csv)
#    ${output_directory}/$(basename ${mask_filename13%.nii*}.csv)
#    ${output_directory}/$(basename ${mask_filename14%.nii*}.csv)
#    ${output_directory}/$(basename ${mask_filename15%.nii*}.csv)
#    ${output_directory}/$(basename ${mask_filename16%.nii*}.csv)
#    ${output_directory}/$(basename ${mask_filename17%.nii*}.csv)
#    ${output_directory}/$(basename ${mask_filename18%.nii*}.csv)
    ${output_directory}/$(basename ${mask_filename20%.nii*}.csv)
    ${output_directory}/$(basename ${mask_filename21%.nii*}.csv)
    ${output_directory}/$(basename ${mask_filename22%.nii*}.csv)
    ${output_directory}/$(basename ${mask_filename23%.nii*}.csv)
    ${output_directory}/$(basename ${mask_filename24%.nii*}.csv)
    ${output_directory}/$(basename ${mask_filename3_1%.nii*}.csv)
    ${output_directory}/$(basename ${mask_filename4_1%.nii*}.csv)
#    ${output_directory}/$(basename ${mask_filename25%.nii*}.csv)
#    ${output_directory}/$(basename ${mask_filename26%.nii*}.csv)
#    ${output_directory}/$(basename ${mask_filename27%.nii*}.csv)
#    ${output_directory}/$(basename ${mask_filename28%.nii*}.csv)
    ${output_directory}/$(basename ${mask_filename29%.nii*}.csv))
    outputfiles_present=$(python3 dividemasks_into_left_right_Nov20_2025.py "${call_combine_csv_horizontally_arguments[@]}")

    call_saveslicesofnifti_arguments=('call_saveslicesofnifti' ${grayscale_filename} ${working_dir})
    outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_saveslicesofnifti_arguments[@]}")
    outputfile_suffix="GRAY"
    color_list='purple_maroon_black_black'
    call_masks_on_grayscale_colored_arguments=('call_masks_on_grayscale_colored' ${grayscale_filename_1} ${contrast_limits} ${outputfile_dir} ${outputfile_suffix} ${color_list} ${working_dir_1} ${mask_filename1} ${mask_filename2} ${mask_filename3} ${mask_filename4})
    outputfiles_present=$(python3 dividemasks_into_left_right_Nov20_2025.py "${call_masks_on_grayscale_colored_arguments[@]}")

    outputfile_suffix="INFARCT"
    color_list='blue_blue_red_red'
    call_masks_on_grayscale_colored_arguments=('call_masks_on_grayscale_colored' ${grayscale_filename_1} ${contrast_limits} ${outputfile_dir} ${outputfile_suffix} ${color_list} ${working_dir_1} ${mask_filename3} ${mask_filename4} ${mask_filename32} ${mask_filename33} )
    outputfiles_present=$(python3 dividemasks_into_left_right_Nov20_2025.py "${call_masks_on_grayscale_colored_arguments[@]}")


    outputfile_suffix="COMPLETE_CSF"
    color_list='red_green'
    call_masks_on_grayscale_colored_arguments=('call_masks_on_grayscale_colored' ${grayscale_filename_1} ${contrast_limits} ${outputfile_dir} ${outputfile_suffix} ${color_list} ${working_dir_1} ${mask_filename3} ${mask_filename4})

    outputfiles_present=$(python3 dividemasks_into_left_right_Nov20_2025.py "${call_masks_on_grayscale_colored_arguments[@]}")
    echo outputfiles_present::${outputfiles_present}

    outputfile_suffix="CSF_COMPARTMENTS"
    color_list='green_green_yellow_yellow_red_red_aqua_aqua_purple_purple'
    call_masks_on_grayscale_colored_arguments=('call_masks_on_grayscale_colored' ${grayscale_filename_1} ${contrast_limits} ${outputfile_dir} ${outputfile_suffix} ${color_list} ${working_dir_1} ${mask_filename3} ${mask_filename4} ${mask_filename5} ${mask_filename6} ${mask_filename7} ${mask_filename8} ${mask_filename9} ${mask_filename10} ${mask_filename30} ${mask_filename31})

    outputfiles_present=$(python3 dividemasks_into_left_right_Nov20_2025.py "${call_masks_on_grayscale_colored_arguments[@]}")
    csvfilename_trimmed=${csvfilename%.csv}_TRIMMED.csv
    cp ${csvfilename} ${csvfilename_trimmed} ##%.csv}_TRIMMED.csv
    call_write_panda_df_arguments=('call_write_panda_df' ${csvfilename_trimmed} ${latexfilename})
    outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_write_panda_df_arguments[@]}")

    call_latex_inserttext_tableNc_arguments=('call_latex_inserttext_tableNc' ${latexfilename} black_black_blue_black_black "NCCT" "CSF" "CSF Compartments" "Infarct and its mirror" ) ##"SAH Blood Segm")
    outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_latex_inserttext_tableNc_arguments[@]}")

    call_space_between_lines_arguments=('call_space_between_lines' ${latexfilename} '-3')
    outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_space_between_lines_arguments[@]}") #fuchsia_fuchsia_olive_olive_lime_lime_orange_orange
    call_latex_inserttext_tableNc_arguments=('call_latex_inserttext_tableNc_colored_with_bullet' ${latexfilename} white_red_cadmiumgreen_orange bullet_bullet_bullet_bullet "   "  "Left CSF" "Ventricle" "Infarct")
    outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_latex_inserttext_tableNc_arguments[@]}")
    call_space_between_lines_arguments=('call_space_between_lines' ${latexfilename} '-3')
    outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_space_between_lines_arguments[@]}")
    call_latex_inserttext_tableNc_arguments=('call_latex_inserttext_tableNc_colored_with_bullet' ${latexfilename} white_cadmiumgreen_red_electricpurple bullet_bullet_bullet_bullet "   "  "Right Ventricle" "Sulci at ventricle" "Infarct Mirror")

    outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_latex_inserttext_tableNc_arguments[@]}")

    call_space_between_lines_arguments=('call_space_between_lines' ${latexfilename} '-3')
    outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_space_between_lines_arguments[@]}")
    call_latex_inserttext_tableNc_arguments=('call_latex_inserttext_tableNc_colored_with_bullet' ${latexfilename} white_white_yellow_lime bullet_bullet_bullet_bullet "   "  " " "Sulci above Ventricle"  "   ")

    outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_latex_inserttext_tableNc_arguments[@]}")
    call_space_between_lines_arguments=('call_space_between_lines' ${latexfilename} '-2')
    outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_space_between_lines_arguments[@]}")
    call_latex_inserttext_tableNc_arguments=('call_latex_inserttext_tableNc_colored_with_bullet' ${latexfilename} white_white_aqua_white bullet_bullet_bullet_bullet "   "  "  " "Sulci below Ventricle"  "   ")
    outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_latex_inserttext_tableNc_arguments[@]}")
    call_space_between_lines_arguments=('call_space_between_lines' ${latexfilename} '-2')
    outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_space_between_lines_arguments[@]}")
    call_latex_inserttext_tableNc_arguments=('call_latex_inserttext_tableNc_colored_with_bullet' ${latexfilename} white_white_electricpurple_white bullet_bullet_bullet_bullet "   "  "  " "Cistern" "   ")
    outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_latex_inserttext_tableNc_arguments[@]}")

    for x in ${working_dir}/${grayscale_filename_basename_noext}*.jpg; do #_resaved_levelset_GRAY

      imagescale='0.18' #float(args.stuff[2])
      angle='90'        #float(args.stuff[3])
      space='1'         #float(args.stuff[4])
      i=0

      images[$i]='call_latex_insertimage_tableNc'
      i=$(($i + 1))
      images[$i]=${latexfilename}
      i=$(($i + 1))
      images[$i]=${imagescale}
      i=$(($i + 1))
      images[$i]=${angle}
      i=$(($i + 1))
      images[$i]=${space}
      i=$(($i + 1))

      y=${x%.*}
      echo $y
      echo "DEBUGGING STARTS"
      echo "${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_GRAY_${suffix}.jpg"
      echo "${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_COMPLETE_CSF_${suffix}.jpg"

      echo "${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_CSF_COMPARTMENTS_${suffix}.jpg"

      suffix=${y##*_}
      digit=${y##*}
#      if [[ ${digit} -gt 0 ]] ; then

      if [ ${suffix} -gt 0 ] && [ -f "${x}" ] && [ -f "${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_GRAY_${suffix}.jpg" ] && [ -f "${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_COMPLETE_CSF_${suffix}.jpg" ] && [ -f "${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_CSF_COMPARTMENTS_${suffix}.jpg" ]; then
              echo suffix::${suffix}
#      exit
        images[$i]=${x} ##{output_directory}/SAH_1_01052014_2003_2_GRAY_031.jpg
        i=$(($i + 1))

#        images[$i]=${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_GRAY_${suffix}.jpg
#        i=$(($i + 1))
        images[$i]=${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_COMPLETE_CSF_${suffix}.jpg
        i=$(($i + 1))

        images[$i]=${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_CSF_COMPARTMENTS_${suffix}.jpg
        i=$(($i + 1))
        images[$i]=${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_${suffix}_infarct.png
        i=$(($i + 1))

        outputfiles_present=$(python3 utilities_simple_trimmed.py "${images[@]}")
        echo outputfiles_present::${outputfiles_present}
      fi
    done


    call_latex_end_arguments=('call_latex_end' ${latexfilename})
    pdfilename=${output_directory}/$(basename ${latexfilename%.tex*}.pdf)
    timestampnow=$(date +"%Y-%m-%d-%H-%M-%S")

    pdfilename_1_1=${output_directory}/$(basename ${latexfilename%.tex*}_${timestampnow}.pdf)
    outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_latex_end_arguments[@]}")
    pdflatex -halt-on-error -interaction=nonstopmode -output-directory=${output_directory} ${latexfilename} ##${output_directory}/$(/usr/lib/fsl/5.0/remove_ext $this_filename)*.tex
    URI_1=${url1%/resources*}
    all_files_to_upload=()
    resource_dirname="CSF_COMPARTMENTS_ANALYSIS"

    resource_dirname="MASKS"
      csv_file=${output_directory}/${grayscale_filename_basename_noext}_SESSION_PROJECT.csv
      column_name="SESSION_PROJECT"
      col_index=$(awk -F, -v col="$column_name" 'NR==1 {
        for (i=1; i<=NF; i++) if ($i == col) { print i; exit }
      }' "$csv_file")
      first_value=$(awk -F, -v idx="$col_index" 'NR==2 { print $idx }' "$csv_file")
      database_table_name=${first_value}
      echo "database_table_name::${database_table_name}"
      function_with_arguments=('call_pipeline_step_completed' ${database_table_name} ${sessionID} ${scanID} "CSF_COMPARTMENT_PDF_COMPLETE" 0 "CSF_COMPARTMENTS_ANALYSIS" ) ##$(basename  ${fixed_image_filename}) $(basename  ${infarct_mask_binary_output_filename})  $(basename  ${registration_mat_file}) $(basename  ${registration_nii_file}) $(basename  ${mask_binary_output_dir}/${mask_binary_output_filename})  ) ##'warped_1_mov_mri_region_' )
      for f in "${all_files_to_upload[@]}"; do
        function_with_arguments+=("$f")
      done




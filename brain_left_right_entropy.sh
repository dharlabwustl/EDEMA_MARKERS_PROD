#!/bin/bash
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

final_output_directory=/outputinsidedocker
call_combine_csv_horizontally() {
  local grayscale_filename_basename_noext=${1}
  local csvfilename=${2}
  local file_to_append_horizontally=${3}
  local call_combine_csv_horizontally_arguments=('call_combine_csv_horizontally' ${grayscale_filename_basename_noext} ${csvfilename} ${csvfilename} ${file_to_append_horizontally})
  local outputfiles_present=$(python3 dividemasks_into_left_right.py "${call_combine_csv_horizontally_arguments[@]}")

}
copyoutput_to_snipr() {
  sessionID=$1
  scanID=$2
  resource_dirname=$4 #"MASKS" #sys.argv[4]
  file_suffix=$5
  output_dir=$3
  echo " I AM IN copyoutput_to_snipr "
  python3 -c "
import sys
sys.path.append('/software');
from download_with_session_ID import *;
uploadfile()" ${sessionID} ${scanID} ${output_dir} ${resource_dirname} ${file_suffix} # ${infarctfile_present}  ##$static_template_image $new_image $backslicenumber #$single_slice_filename

}

copy_masks_data() {
  echo " I AM IN copy_masks_data "
  # rm -r /ZIPFILEDIR/*
  sessionID=${1}
  scanID=${2}
  resource_dirname=${3} #str(sys.argv[4])
  output_dirname=${4}   #str(sys.argv[3])
  echo output_dirname::${output_dirname}
  python3 -c "
import sys
sys.path.append('/software');
from download_with_session_ID import *;
downloadfiletolocaldir()" ${sessionID} ${scanID} ${resource_dirname} ${output_dirname} ### ${infarctfile_present}  ##$static_template_image $new_image $backslicenumber #$single_slice_filename

}

copy_scan_data() {
  echo " I AM IN copy_scan_data "
  # rm -r /ZIPFILEDIR/*
  # rm -r ${working_dir}/*
  # rm -r ${output_dir}/*
  sessionID=$1
  dir_to_receive_the_data=${2}
  resource_dir=${3}
  # sessionId=sys.argv[1]
  # dir_to_receive_the_data=sys.argv[2]
  # resource_dir=sys.argv[3]
  # scanID=$2
  python -c "
import sys
sys.path.append('/Stroke_CT_Processing');
from download_with_session_ID import *;
get_relevantfile_in_A_DIRECTORY()" ${sessionID} ${dir_to_receive_the_data} ${resource_dir}

}
run_Registration() {
  this_filename=${1}
  this_betfilename=${2}
  #  this_csfmaskfilename=${3}
  #  this_infarctmaskfilename=${4}
  echo "BET USING LEVELSET MASK"

  /software/bet_withlevelset.sh $this_filename ${this_betfilename} #${output_directory} #Helsinki2000_1019_10132014_1048_Head_2.0_ax_Tilt_1_levelset # ${3} # Helsinki2000_702_12172013_2318_Head_2.0_ax_levelset.nii.gz #${3} # $6 $7 $8 $9 ${10}

  echo "bet_withlevelset successful" >${output_directory}/success.txt
  this_filename_brain=${this_filename%.nii*}_brain_f.nii.gz
  # cp ${this_filename_brain} ${output_directory}/ #  ${final_output_directory}/
  echo "LINEAR REGISTRATION TO TEMPLATE"
  /software/linear_rigid_registration.sh ${this_filename_brain} #${templatefilename} #$3 ${6} WUSTL_233_11122015_0840__levelset_brain_f.nii.gz
  #  echo "linear_rigid_registration successful" >>${output_directory}/success.txt
  #  echo "RUNNING IML FSL PART"
  #  /software/ideal_midline_fslpart.sh ${this_filename} # ${templatefilename} ${mask_on_template}  #$9 #${10} #$8
  #  echo "ideal_midline_fslpart successful" >>${output_directory}/success.txt
  #  echo "RUNNING IML PYTHON PART"
  #
  #  /software/ideal_midline_pythonpart.sh ${this_filename} #${templatefilename}  #$3 #$8 $9 ${10}
  #  echo "ideal_midline_pythonpart successful" >>${output_directory}/success.txt

  #  echo "RUNNING NWU AND CSF VOLUME CALCULATION "
  #
  #  /software/nwu_csf_volume.sh ${this_filename} ${this_betfilename} ${this_csfmaskfilename} ${this_infarctmaskfilename} ${lower_threshold} ${upper_threshold}
  #  echo "nwu_csf_volume successful" >>${output_directory}/success.txt
  #  thisfile_basename=$(basename $this_filename)
  #  # for texfile in $(/usr/lib/fsl/5.0/remove_ext ${output_directory}/$thisfile_basename)*.tex ;
  #  for texfile in ${output_directory}/*.tex; do
  #    pdflatex -halt-on-error -interaction=nonstopmode -output-directory=${output_directory} $texfile ##${output_directory}/$(/usr/lib/fsl/5.0/remove_ext $this_filename)*.tex
  #    rm ${output_directory}/*.aux
  #    rm ${output_directory}/*.log
  #  done
  #
  #  for filetocopy in $(/usr/lib/fsl/5.0/remove_ext ${output_directory}/$thisfile_basename)*_brain_f.nii.gz; do
  #    cp ${filetocopy} ${final_output_directory}/
  #  done
  #

  #
  #  for filetocopy in ${output_directory}/*.pdf; do
  #    cp ${filetocopy} ${final_output_directory}/
  #  done
  #  for filetocopy in ${output_directory}/*.csv; do
  #    cp ${filetocopy} ${final_output_directory}/
  #  done

}
run_IML() {
  this_filename=${1}
  this_betfilename=${2}
  #  this_csfmaskfilename=${3}
  #  this_infarctmaskfilename=${4}
  echo "BET USING LEVELSET MASK"

  /software/bet_withlevelset.sh $this_filename ${this_betfilename} #${output_directory} #Helsinki2000_1019_10132014_1048_Head_2.0_ax_Tilt_1_levelset # ${3} # Helsinki2000_702_12172013_2318_Head_2.0_ax_levelset.nii.gz #${3} # $6 $7 $8 $9 ${10}

  echo "bet_withlevelset successful" >${output_directory}/success.txt
  this_filename_brain=${this_filename%.nii*}_brain_f.nii.gz
  # cp ${this_filename_brain} ${output_directory}/ #  ${final_output_directory}/
  echo "LINEAR REGISTRATION TO TEMPLATE"
  mat_file_num=$(ls ${output_directory}/*.mat | wc -l)
  if [[ ${mat_file_num} -gt 1 ]]; then
    echo "MAT FILES PRESENT"
    #    /software/linear_rigid_registration_onlytrasnformwith_matfile.sh
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
  #    echo "RUNNING NWU AND CSF VOLUME CALCULATION "
  #
  #  /software/nwu_csf_volume.sh ${this_filename} ${this_betfilename} ${this_csfmaskfilename} ${this_infarctmaskfilename} ${lower_threshold} ${upper_threshold}
  #  echo "nwu_csf_volume successful" >>${output_directory}/success.txt
  #  thisfile_basename=$(basename $this_filename)
  #  # for texfile in $(/usr/lib/fsl/5.0/remove_ext ${output_directory}/$thisfile_basename)*.tex ;
  #  for texfile in ${output_directory}/*.tex; do
  #    pdflatex -halt-on-error -interaction=nonstopmode -output-directory=${output_directory} $texfile ##${output_directory}/$(/usr/lib/fsl/5.0/remove_ext $this_filename)*.tex
  #    rm ${output_directory}/*.aux
  #    rm ${output_directory}/*.log
  #  done
  #
  #  for filetocopy in $(/usr/lib/fsl/5.0/remove_ext ${output_directory}/$thisfile_basename)*_brain_f.nii.gz; do
  #    cp ${filetocopy} ${final_output_directory}/
  #  done
  #

  #
  #  for filetocopy in ${output_directory}/*.pdf; do
  #    cp ${filetocopy} ${final_output_directory}/
  #  done
  #  for filetocopy in ${output_directory}/*.csv; do
  #    cp ${filetocopy} ${final_output_directory}/
  #  done

}
run_divide_mask_into_left_right() {
  local grayimage=${1}
  local csf_mask_filename=${2}
  local output_directory=${3}
  local working_dir=${4}
  call_divide_a_mask_into_left_right_submasks_arguments=('call_divide_a_mask_into_left_right_submasks' ${grayimage} ${csf_mask_filename} ${output_directory} ${working_dir})
  outputfiles_present=$(python3 dividemasks_into_left_right.py "${call_divide_a_mask_into_left_right_submasks_arguments[@]}")
}

run_CSF_COMPARTMENTS_CALC() {
  this_filename=${1}
  this_betfilename=${2}
  this_csfmaskfilename=${3}
  this_infarctmaskfilename=${4}
  #  echo "BET USING LEVELSET MASK"
  #
  #  /software/bet_withlevelset.sh $this_filename ${this_betfilename} #${output_directory} #Helsinki2000_1019_10132014_1048_Head_2.0_ax_Tilt_1_levelset # ${3} # Helsinki2000_702_12172013_2318_Head_2.0_ax_levelset.nii.gz #${3} # $6 $7 $8 $9 ${10}
  #
  #  echo "bet_withlevelset successful" >${output_directory}/success.txt
  #  this_filename_brain=${this_filename%.nii*}_brain_f.nii.gz
  #  # cp ${this_filename_brain} ${output_directory}/ #  ${final_output_directory}/
  #  echo "LINEAR REGISTRATION TO TEMPLATE"
  #  /software/linear_rigid_registration.sh ${this_filename_brain} #${templatefilename} #$3 ${6} WUSTL_233_11122015_0840__levelset_brain_f.nii.gz
  #  echo "linear_rigid_registration successful" >>${output_directory}/success.txt
  #  echo "RUNNING IML FSL PART"
  #  /software/ideal_midline_fslpart.sh ${this_filename} # ${templatefilename} ${mask_on_template}  #$9 #${10} #$8
  #  echo "ideal_midline_fslpart successful" >>${output_directory}/success.txt
  #  echo "RUNNING IML PYTHON PART"
  #
  #  /software/ideal_midline_pythonpart.sh ${this_filename} #${templatefilename}  #$3 #$8 $9 ${10}
  #  echo "ideal_midline_pythonpart successful" >>${output_directory}/success.txt

  echo "RUNNING NWU AND CSF VOLUME CALCULATION "

  /software/nwu_csf_volume.sh ${this_filename} ${this_betfilename} ${this_csfmaskfilename} ${this_infarctmaskfilename} 0 1000 #${lower_threshold} ${upper_threshold}
  echo "nwu_csf_volume successful" >>${output_directory}/success.txt
  thisfile_basename=$(basename $this_filename)
  #  # for texfile in $(/usr/lib/fsl/5.0/remove_ext ${output_directory}/$thisfile_basename)*.tex ;
  #  for texfile in ${output_directory}/*.tex; do
  #    pdflatex -halt-on-error -interaction=nonstopmode -output-directory=${output_directory} $texfile ##${output_directory}/$(/usr/lib/fsl/5.0/remove_ext $this_filename)*.tex
  #    rm ${output_directory}/*.aux
  #    rm ${output_directory}/*.log
  #  done
  #
  #  for filetocopy in $(/usr/lib/fsl/5.0/remove_ext ${output_directory}/$thisfile_basename)*_brain_f.nii.gz; do
  #    cp ${filetocopy} ${final_output_directory}/
  #  done
  #
  #  for filetocopy in $(/usr/lib/fsl/5.0/remove_ext ${output_directory}/$thisfile_basename)*.mat; do
  #    cp ${filetocopy} ${final_output_directory}/
  #  done
  #
  #  for filetocopy in ${output_directory}/*.pdf; do
  #    cp ${filetocopy} ${final_output_directory}/
  #  done
  #  for filetocopy in ${output_directory}/*.csv; do
  #    cp ${filetocopy} ${final_output_directory}/
  #  done

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
  # cp ${this_filename_brain} ${output_directory}/ #  ${final_output_directory}/
  echo "LINEAR REGISTRATION TO TEMPLATE"
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
  # for texfile in $(/usr/lib/fsl/5.0/remove_ext ${output_directory}/$thisfile_basename)*.tex ;
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
  #  for eachfile in ${working_dir}/*.nii*; do
  for eachfile in ${working_dir_1}/*.nii*; do
    original_ct_file=${eachfile}
    eachfile_basename=$(basename ${eachfile})
    originalfile_basename=${eachfile_basename}
    eachfile_basename_noext=${eachfile_basename%.nii*}

    ############## files basename ##################################
    grayfilename=${eachfile_basename_noext}_resaved_levelset.nii
    if [[ "$eachfile_basename" == *".nii.gz"* ]]; then #"$STR" == *"$SUB"*
      grayfilename=${eachfile_basename_noext}_resaved_levelset.nii.gz
    fi
    betfilename=${eachfile_basename_noext}_resaved_levelset_bet.nii.gz
    #    csffilename=${eachfile_basename_noext}_resaved_csf_unet.nii.gz
    #    infarctfilename=${eachfile_basename_noext}_resaved_infarct_auto_removesmall.nii.gz
    ################################################
    ############## copy those files to the docker image ##################################
    cp ${working_dir}/${betfilename} ${output_directory}/
    #    cp ${working_dir}/${csffilename} ${output_directory}/
    #    cp ${working_dir}/${infarctfilename} ${output_directory}/
    ####################################################################################
    source /software/bash_functions_forhost.sh

    cp ${original_ct_file} ${output_directory}/${grayfilename}
    grayimage=${output_directory}/${grayfilename} #${gray_output_subdir}/${eachfile_basename_noext}_resaved_levelset.nii
    ###########################################################################

    #    #### originalfiel: .nii
    #    #### betfile: *bet.nii.gz
    #
    #    # original_ct_file=$original_CT_directory_names/
    #    levelset_infarct_mask_file=${output_directory}/${infarctfilename}
    #    echo "levelset_infarct_mask_file:${levelset_infarct_mask_file}"
    #    ## preprocessing infarct mask:
    #    python3 -c "
    #import sys ;
    #sys.path.append('/software/') ;
    #from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${original_ct_file}" "${levelset_infarct_mask_file}" "${output_directory}"

    ## preprocessing bet mask:
    levelset_bet_mask_file=${output_directory}/${betfilename}
    echo "levelset_bet_mask_file:${levelset_bet_mask_file}"
    python3 -c "

import sys ;
sys.path.append('/software/') ;
from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${original_ct_file}" "${levelset_bet_mask_file}" "${output_directory}"

    #    #### preprocessing csf mask:
    #    levelset_csf_mask_file=${output_directory}/${csffilename}
    #    echo "levelset_csf_mask_file:${levelset_csf_mask_file}"
    #    python3 -c "
    #import sys ;
    #sys.path.append('/software/') ;
    #from utilities_simple_trimmed import * ;   levelset2originalRF_new_flip()" "${original_ct_file}" "${levelset_csf_mask_file}" "${output_directory}"

    #    lower_threshold=0
    #    upper_threshold=20
    #    templatefilename=scct_strippedResampled1.nii.gz
    #    mask_on_template=midlinecssfResampled1.nii.gz

    x=$grayimage
    bet_mask_filename=${output_directory}/${betfilename}
    #    infarct_mask_filename=${output_directory}/${infarctfilename}
    #    csf_mask_filename=${output_directory}/${csffilename}
    run_Registration $x ${bet_mask_filename} #${csf_mask_filename} ${infarct_mask_filename}

  done

  # for f in ${output_directory}/*; do
  #     # if [ -d "$f" ]; then
  #         # $f is a directory
  #         rm -r $f
  #     # fi
  # done

}

midlineonly_each_scan() {
  local niftifilename_ext=${1}

  eachfile_basename_noext=''
  originalfile_basename=''
  original_ct_file=''
  #  for eachfile in ${working_dir}/*.nii*; do
  for eachfile in ${working_dir_1}/*.nii*; do
    if [[ ${eachfile} != *"levelset"* ]]; then
      # testmystring does not contain c0

      original_ct_file=${eachfile}
      eachfile_basename=$(basename ${eachfile})
      originalfile_basename=${eachfile_basename}
      eachfile_basename_noext=${eachfile_basename%.nii*}

      ############## files basename ##################################
      grayfilename=${eachfile_basename_noext}_resaved_levelset.nii
      if [[ "$eachfile_basename" == *".nii.gz"* ]]; then #"$STR" == *"$SUB"*
        grayfilename=${eachfile_basename_noext}_resaved_levelset.nii.gz
      fi
      betfilename=${eachfile_basename_noext}_resaved_levelset_bet.nii.gz
      #    csffilename=${eachfile_basename_noext}_resaved_csf_unet.nii.gz
      #    infarctfilename=${eachfile_basename_noext}_resaved_infarct_auto_removesmall.nii.gz
      ################################################
      ############## copy those files to the docker image ##################################
      cp ${working_dir}/${betfilename} ${output_directory}/
      #    cp ${working_dir}/${csffilename} ${output_directory}/
      #    cp ${working_dir}/${infarctfilename} ${output_directory}/
      ####################################################################################
      source /software/bash_functions_forhost.sh

      cp ${original_ct_file} ${output_directory}/${grayfilename}
      grayimage=${output_directory}/${grayfilename} #${gray_output_subdir}/${eachfile_basename_noext}_resaved_levelset.nii
      ###########################################################################

      #    #### originalfiel: .nii
      #    #### betfile: *bet.nii.gz
      #
      #    # original_ct_file=$original_CT_directory_names/
      #    levelset_infarct_mask_file=${output_directory}/${infarctfilename}
      #    echo "levelset_infarct_mask_file:${levelset_infarct_mask_file}"
      #    ## preprocessing infarct mask:
      #    python3 -c "
      #import sys ;
      #sys.path.append('/software/') ;
      #from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${original_ct_file}" "${levelset_infarct_mask_file}" "${output_directory}"

      ## preprocessing bet mask:
      levelset_bet_mask_file=${output_directory}/${betfilename}
      echo "levelset_bet_mask_file:${levelset_bet_mask_file}"
      python3 -c "

import sys ;
sys.path.append('/software/') ;
from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${original_ct_file}" "${levelset_bet_mask_file}" "${output_directory}"

      #    #### preprocessing csf mask:
      #    levelset_csf_mask_file=${output_directory}/${csffilename}
      #    echo "levelset_csf_mask_file:${levelset_csf_mask_file}"
      #    python3 -c "
      #import sys ;
      #sys.path.append('/software/') ;
      #from utilities_simple_trimmed import * ;   levelset2originalRF_new_flip()" "${original_ct_file}" "${levelset_csf_mask_file}" "${output_directory}"

      #    lower_threshold=0
      #    upper_threshold=20
      #    templatefilename=scct_strippedResampled1.nii.gz
      #    mask_on_template=midlinecssfResampled1.nii.gz

      x=$grayimage
      bet_mask_filename=${output_directory}/${betfilename}
      #    infarct_mask_filename=${output_directory}/${infarctfilename}
      #    csf_mask_filename=${output_directory}/${csffilename}
      run_IML $x ${bet_mask_filename} #${csf_mask_filename} ${infarct_mask_filename}
    fi
  done

  # for f in ${output_directory}/*; do
  #     # if [ -d "$f" ]; then
  #         # $f is a directory
  #         rm -r $f
  #     # fi
  # done

}
split_masks_into_two_halves() {

  eachfile_basename_noext=''
  originalfile_basename=''
  original_ct_file=''
  maskfile_extension=${1}
  for eachfile in ${working_dir_1}/*.nii*; do
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
    ####################################################################################
    source /software/bash_functions_forhost.sh

    cp ${original_ct_file} ${output_directory}/${grayfilename}
    grayimage=${output_directory}/${grayfilename} #${gray_output_subdir}/${eachfile_basename_noext}_resaved_levelset.nii
    #### preprocessing csf mask:
    levelset_csf_mask_file=${output_directory}/${csffilename}
    echo "levelset_csf_mask_file:${levelset_csf_mask_file}"
    python3 -c "
import sys ;
sys.path.append('/software/') ;
from utilities_simple_trimmed import * ;   levelset2originalRF_new_flip()" "${original_ct_file}" "${levelset_csf_mask_file}" "${output_directory}"
    templatefilename=scct_strippedResampled1.nii.gz
    mask_on_template=midlinecssfResampled1.nii.gz
    csf_mask_filename=${output_directory}/${csffilename}
    run_divide_mask_into_left_right ${grayimage} ${csf_mask_filename} ${output_directory} ${working_dir}

  done

}
nwucalculation_each_scan() {

  eachfile_basename_noext=''
  originalfile_basename=''
  original_ct_file=''
  #  for eachfile in ${working_dir}/*.nii*; do
  for eachfile in ${working_dir_1}/*.nii*; do
    original_ct_file=${eachfile}
    eachfile_basename=$(basename ${eachfile})
    originalfile_basename=${eachfile_basename}
    eachfile_basename_noext=${eachfile_basename%.nii*}

    ############## files basename ##################################
    grayfilename=${eachfile_basename_noext}_resaved_levelset.nii
    if [[ "$eachfile_basename" == *".nii.gz"* ]]; then #"$STR" == *"$SUB"*
      grayfilename=${eachfile_basename_noext}_resaved_levelset.nii.gz
    fi
    betfilename=${eachfile_basename_noext}_resaved_levelset_bet.nii.gz
    csffilename=${eachfile_basename_noext}_resaved_csf_unet.nii.gz
    infarctfilename=${eachfile_basename_noext}_resaved_infarct_auto_removesmall.nii.gz
    ################################################
    ############## copy those files to the docker image ##################################
    cp ${working_dir}/${betfilename} ${output_directory}/
    cp ${working_dir}/${csffilename} ${output_directory}/
    cp ${working_dir}/${infarctfilename} ${output_directory}/
    ####################################################################################
    source /software/bash_functions_forhost.sh

    cp ${original_ct_file} ${output_directory}/${grayfilename}
    grayimage=${output_directory}/${grayfilename} #${gray_output_subdir}/${eachfile_basename_noext}_resaved_levelset.nii
    ###########################################################################

    #### originalfiel: .nii
    #### betfile: *bet.nii.gz

    # original_ct_file=$original_CT_directory_names/
    levelset_infarct_mask_file=${output_directory}/${infarctfilename}
    echo "levelset_infarct_mask_file:${levelset_infarct_mask_file}"
    ## preprocessing infarct mask:
    python3 -c "
import sys ;
sys.path.append('/software/') ;
from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${original_ct_file}" "${levelset_infarct_mask_file}" "${output_directory}"

    ## preprocessing bet mask:
    levelset_bet_mask_file=${output_directory}/${betfilename}
    echo "levelset_bet_mask_file:${levelset_bet_mask_file}"
    python3 -c "

import sys ;
sys.path.append('/software/') ;
from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${original_ct_file}" "${levelset_bet_mask_file}" "${output_directory}"

    #### preprocessing csf mask:
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

  # for f in ${output_directory}/*; do
  #     # if [ -d "$f" ]; then
  #         # $f is a directory
  #         rm -r $f
  #     # fi
  # done

}

# #####################################################
get_nifti_scan_uri() {
  # csvfilename=sys.argv[1]
  # dir_to_save=sys.argv[2]
  # echo " I AM IN copy_scan_data "
  # rm -r /ZIPFILEDIR/*

  sessionID=$1
  working_dir=${2}
  output_csvfile=${3}
  rm -r ${working_dir}/*
  output_dir=$(dirname ${output_csvfile})
  rm -r ${output_dir}/*
  # scanID=$2
  python3 -c "
import sys
sys.path.append('/software');
from download_with_session_ID import *;
call_decision_which_nifti()" ${sessionID} ${working_dir} ${output_csvfile}

}

copy_scan_data() {
  csvfilename=${1} #sys.argv[1]
  dir_to_save=${2} #sys.argv[2]
  # 		echo " I AM IN copy_scan_data "
  # rm -r /ZIPFILEDIR/*
  # rm -r ${working_dir}/*
  # rm -r ${output_dir}/*
  # sessionID=$1
  # # scanID=$2
  python3 -c "
import sys
sys.path.append('/software');
from download_with_session_ID import *;
downloadniftiwithuri_withcsv()" ${csvfilename} ${dir_to_save}

}

getmaskfilesscanmetadata() {
  # def get_maskfile_scan_metadata():
  sessionId=${1}           #sys.argv[1]
  scanId=${2}              # sys.argv[2]
  resource_foldername=${3} # sys.argv[3]
  dir_to_save=${4}         # sys.argv[4]
  csvfilename=${5}         # sys.argv[5]
  python3 -c "
import sys
sys.path.append('/software');
from download_with_session_ID import *;
get_maskfile_scan_metadata()" ${sessionId} ${scanId} ${resource_foldername} ${dir_to_save} ${csvfilename}
}
## ratio of two halves
#def call_ratio_left_right(args):
#    returnvalue=0
#    try:
calculate_left_right_ratio() {
  local lefthalf_file=${1}
  local righthalf_file=${2}
  local grayscale_filename_basename_noext=${3}
  local column_name_this=$(basename ${lefthalf_file})
  local column_name_this=${column_name_this##*${grayscale_filename_basename_noext}_resaved_}
  local column_name_this=${column_name_this%_half_originalRF*}
  local column_name_this=${column_name_this%_left*}_RATIO
  #  local maskfile_extension=${1}
  #  local maskfile_extension_no_nii=${maskfile_extension%.nii*}
  #  local lefthalf_file=$(ls ${working_dir}/*${maskfile_extension_no_nii}_left_half_originalRF.nii.gz)
  #  local righthalf_file=$(ls ${working_dir}/*${maskfile_extension_no_nii}_right_half_originalRF.nii.gz)
  ##  local column_name=${2}
  local filename_to_write=${output_directory}/$(basename ${lefthalf_file%.nii*})_RATIO.csv
  local call_ratio_left_right_arguments=('call_ratio_left_right' ${lefthalf_file} ${righthalf_file} ${column_name_this} ${filename_to_write})
  local outputfiles_present=$(python3 dividemasks_into_left_right.py "${call_ratio_left_right_arguments[@]}")
  echo outputfiles_present::${outputfiles_present}
}

calculate_volume() {
  #  local maskfile_extension=${1}
  #  local maskfile_extension_no_nii=${maskfile_extension%.nii*}
  local column_name=${2}

  local mask_file=${1} ##$(ls ${working_dir}/*${maskfile_extension_no_nii}_${2}_half_originalRF.nii.gz)
  local mask_file_basename=$(basename ${mask_file})
  local mask_file_basename=${mask_file_basename%.nii*}
  local filename_to_write=${output_directory}/${mask_file_basename}.csv
  local call_calculate_volume_arguments=('call_calculate_volume' ${mask_file} ${column_name} ${filename_to_write})
  local outputfiles_present=$(python3 dividemasks_into_left_right.py "${call_calculate_volume_arguments[@]}")
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
  #  local column_name_this=${column_name_this%_half_originalRF*}
  local call_calculate_volume_mask_from_yasheng_arguments=('call_calculate_volume_mask_from_yasheng' ${mask_filename} ${original_nifti_file} ${column_name_this} ${filename_to_write})
  local outputfiles_present=$(python3 dividemasks_into_left_right.py "${call_calculate_volume_mask_from_yasheng_arguments[@]}")
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
  outputfiles_present=$(python3 dividemasks_into_left_right.py "${call_masks_subtraction_arguments[@]}")
  echo outputfiles_present::${outputfiles_present}
}
#mask_subtraction ${working_dir}/SAH_1_01052014_2003_2_resaved_levelset_bet_right_half_originalRF.nii.gz  ${working_dir}/SAH_1_01052014_2003_2_resaved_csf_unet_right_half_originalRF.nii.gz ${working_dir}
##rename grayscale image
#_resaved_levelset.nii.gz
overlapped_mask_on_otherimage() {
  local grayscale_filename_1=${1}
  local contrast_limits=${2}
  local outputfile_dir=${3}
  local outputfile_suffix=${4}
  local color_list=${5}
  local working_dir_1=${6}
  local -n mask_filename=${7}
  local call_masks_on_grayscale_colored_arguments=('call_masks_on_grayscale_colored' ${grayscale_filename_1} ${contrast_limits} ${outputfile_dir} ${outputfile_suffix} ${color_list} ${working_dir_1} ${mask_filename[@]})
  local outputfiles_present=$(python3 dividemasks_into_left_right.py "${call_masks_on_grayscale_colored_arguments[@]}")
  echo outputfiles_present::${outputfiles_present}

}
#for grayscale_filename in ${working_dir_1}/*.nii*; do

function call_get_resourcefiles_metadata_saveascsv_args() {

  local resource_dir=${2}   #"NIFTI"
  local output_csvfile=${4} #{array[1]}

  local URI=${1} #{array[0]}
  #  local file_ext=${5}
  #  local output_csvfile=${output_csvfile%.*}${resource_dir}.csv

  local final_output_directory=${3}
  local call_download_files_in_a_resource_in_a_session_arguments=('call_get_resourcefiles_metadata_saveascsv_args' ${URI} ${resource_dir} ${final_output_directory} ${output_csvfile})
  outputfiles_present=$(python3 download_with_session_ID.py "${call_download_files_in_a_resource_in_a_session_arguments[@]}")
  echo " I AM AT call_get_resourcefiles_metadata_saveascsv_args"

}
echo " I AM RUNNING "
################ DOWNLOAD MASKS ###############################
## METADATA in the MASK directory
URI=/data/experiments/${sessionID}

resource_dir="NIFTI_LOCATION"
output_csvfile=${sessionID}_SCANSELECTION_METADATA.csv
call_get_resourcefiles_metadata_saveascsv_args ${URI} ${resource_dir} ${working_dir} ${output_csvfile}
dir_to_save=${working_dir}
greyfile="NONE" ##'/media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/CSFSEPERATION/TESTING_CSF_SEPERATION/Krak_003_09042014_0949_MOZG_6.0_H31s_levelset.nii.gz'
betfile="NONE"  ##'/media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/CSFSEPERATION/TESTING_CSF_SEPERATION/Krak_003_09042014_0949_MOZG_6.0_H31s_levelset_bet.nii.gz'
csffile="NONE"  ##'/media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/CSFSEPERATION/TESTING_CSF_SEPERATION/Krak_003_09042014_0949_MOZG_6.0_H31s_final_seg.nii.gz'
NIFTI_SCAN_URI=''
while IFS=',' read -ra array; do

  url=${array[6]}
  NIFTI_SCAN_URI=url
  filename=$(basename ${url})


  call_download_a_singlefile_with_URIString_arguments=('call_download_a_singlefile_with_URIString' ${url} ${filename} ${dir_to_save})
  outputfiles_present=$(python3 download_with_session_ID.py "${call_download_a_singlefile_with_URIString_arguments[@]}")

  while IFS=',' read -ra array1; do
    #      echo "${array1[0]}"
    url1=${array1[0]}
    filename_nifti=$(basename ${url1})
    call_download_a_singlefile_with_URIString_arguments=('call_download_a_singlefile_with_URIString' ${url1} ${filename_nifti} ${working_dir_1})
    outputfiles_present=$(python3 download_with_session_ID.py "${call_download_a_singlefile_with_URIString_arguments[@]}")

    resource_dir="MASKS"
    output_csvfile_1=${sessionID}_MASK_METADATA.csv
    call_get_resourcefiles_metadata_saveascsv_args ${url1} ${resource_dir} ${working_dir} ${output_csvfile_1}

    while IFS=',' read -ra array2; do

      url2=${array2[6]}
      #################

      if [[ ${url2} == *"_levelset.nii.gz"* ]]; then #  || [[ ${url2} == *"_levelset_bet"* ]]  || [[ ${url2} == *"csf_unet"* ]]  ; then ##[[ $string == *"My long"* ]]; then
        echo "It's there!"
        echo "${array2[6]}"
        filename2=$(basename ${url2})
        call_download_a_singlefile_with_URIString_arguments=('call_download_a_singlefile_with_URIString' ${url2} ${filename2} ${dir_to_save})
        outputfiles_present=$(python3 download_with_session_ID.py "${call_download_a_singlefile_with_URIString_arguments[@]}")
        greyfile=${dir_to_save}/${filename2}
        echo "${greyfile}"
      fi
      if [[ ${url2} == *"_levelset_bet.nii.gz"* ]]; then #  || [[ ${url2} == *"_levelset_bet"* ]]  || [[ ${url2} == *"csf_unet"* ]]  ; then ##[[ $string == *"My long"* ]]; then
        echo "It's there!"
        echo "${array2[6]}"
        filename2=$(basename ${url2})
        call_download_a_singlefile_with_URIString_arguments=('call_download_a_singlefile_with_URIString' ${url2} ${filename2} ${dir_to_save})
        outputfiles_present=$(python3 download_with_session_ID.py "${call_download_a_singlefile_with_URIString_arguments[@]}")
        betfile=${dir_to_save}/${filename2}
        echo "${betfile}"
      fi
      if [[ ${url2} == *".mat"* ]]; then #  || [[ ${url2} == *"_levelset_bet"* ]]  || [[ ${url2} == *"csf_unet"* ]]  ; then ##[[ $string == *"My long"* ]]; then
        echo "It's there!"
        echo "${array2[6]}"
        filename2=$(basename ${url2})
        call_download_a_singlefile_with_URIString_arguments=('call_download_a_singlefile_with_URIString' ${url2} ${filename2} ${output_directory})
        outputfiles_present=$(python3 download_with_session_ID.py "${call_download_a_singlefile_with_URIString_arguments[@]}")
        csffile=${dir_to_save}/${filename2}
        echo "${csffile}"
      fi

    done < <(tail -n +2 "${working_dir}/${output_csvfile_1}")
    ##################################################
    resource_dir="SAH_SEGM"
    output_csvfile_1=${sessionID}_MASK_METADATA.csv
    call_get_resourcefiles_metadata_saveascsv_args ${url1} ${resource_dir} ${working_dir} ${output_csvfile_1}

    while IFS=',' read -ra array2; do

      url2=${array2[6]}
      #################

      if [[ ${url2} == *".nii.gz"* ]]; then #  || [[ ${url2} == *"_levelset_bet"* ]]  || [[ ${url2} == *"csf_unet"* ]]  ; then ##[[ $string == *"My long"* ]]; then
        echo "It's there!"
        echo "${array2[6]}"
        filename2=$(basename ${url2})
        call_download_a_singlefile_with_URIString_arguments=('call_download_a_singlefile_with_URIString' ${url2} ${filename2} ${dir_to_save})
        outputfiles_present=$(python3 download_with_session_ID.py "${call_download_a_singlefile_with_URIString_arguments[@]}")
        greyfile=${dir_to_save}/${filename2}
        echo "${greyfile}"
      fi

    done \
      < <(tail -n +2 "${working_dir}/${output_csvfile_1}")
    ################################################################

    midlineonly_each_scan ${filename_nifti}
    URI_1=${url1%/resources*}
    for matfiles in ${output_directory}/*.mat; do

      call_uploadsinglefile_with_URI_arguments=('call_uploadsinglefile_with_URI' ${URI_1} ${matfiles} "MASKS")
      outputfiles_present=$(python3 /software/download_with_session_ID.py "${call_uploadsinglefile_with_URI_arguments[@]}")
    done
    #
    split_masks_into_two_halves "_resaved_csf_unet.nii.gz"
    split_masks_into_two_halves "_resaved_levelset_bet.nii.gz"



    #
  done \
    < <(tail -n +2 "${dir_to_save}/${filename}")

done < <(tail -n +2 "${working_dir}/${output_csvfile}")
#
##done < <(tail -n +2 "${csv_file_tostore_latexfilename}")
##done
##################################################################################################################################

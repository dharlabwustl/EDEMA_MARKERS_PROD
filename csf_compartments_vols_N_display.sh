#!/bin/bash
export XNAT_USER=${2}
export XNAT_PASS=${3}
export XNAT_HOST=${4}
sessionID=${1}
working_dir=/workinginput
working_dir_1=/input
output_directory=/workingoutput

final_output_directory=/outputinsidedocker

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
while IFS=',' read -ra array; do
  #xx=0
  #
  ##if [ ${array[1]} == "SNIPR01_E00894" ]  ; then
  #  echo "${array[6]}"
  url=${array[6]}
  filename=$(basename ${url})

  #def call_download_a_singlefile_with_URIString(args):
  #    url=args.stuff[1]
  #    filename=args.stuff[2]
  #    dir_to_save=args.stuff[3]
  call_download_a_singlefile_with_URIString_arguments=('call_download_a_singlefile_with_URIString' ${url} ${filename} ${dir_to_save})
  outputfiles_present=$(python3 download_with_session_ID.py "${call_download_a_singlefile_with_URIString_arguments[@]}")

  while IFS=',' read -ra array1; do
    #      echo "${array1[0]}"
    url1=${array1[0]}
    #      URI=/data/experiments/${sessionID}
    resource_dir="MASKS"
    output_csvfile_1=${sessionID}_MASK_METADATA.csv
    call_get_resourcefiles_metadata_saveascsv_args ${url1} ${resource_dir} ${working_dir} ${output_csvfile_1}
    #      filename1=$(basename ${url1})
    #  call_download_a_singlefile_with_URIString_arguments=('call_download_a_singlefile_with_URIString' ${url1} ${filename1} ${dir_to_save})
    #  outputfiles_present=$(python3 download_with_session_ID.py "${call_download_a_singlefile_with_URIString_arguments[@]}")

    while IFS=',' read -ra array2; do

      url2=${array2[6]}
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
      if [[ ${url2} == *"_csf_unet.nii.gz"* ]]; then #  || [[ ${url2} == *"_levelset_bet"* ]]  || [[ ${url2} == *"csf_unet"* ]]  ; then ##[[ $string == *"My long"* ]]; then
        echo "It's there!"
        echo "${array2[6]}"
        filename2=$(basename ${url2})
        call_download_a_singlefile_with_URIString_arguments=('call_download_a_singlefile_with_URIString' ${url2} ${filename2} ${dir_to_save})
        outputfiles_present=$(python3 download_with_session_ID.py "${call_download_a_singlefile_with_URIString_arguments[@]}")
        csffile=${dir_to_save}/${filename2}
        echo "${csffile}"
      fi
      if [[ ${url2} == *"_sulci_"* ]]; then #  || [[ ${url2} == *"_levelset_bet"* ]]  || [[ ${url2} == *"csf_unet"* ]]  ; then ##[[ $string == *"My long"* ]]; then
        echo "It's there!"
        echo "${array2[6]}"
        filename2=$(basename ${url2})
        call_download_a_singlefile_with_URIString_arguments=('call_download_a_singlefile_with_URIString' ${url2} ${filename2} ${dir_to_save})
        outputfiles_present=$(python3 download_with_session_ID.py "${call_download_a_singlefile_with_URIString_arguments[@]}")
        csffile=${dir_to_save}/${filename2}
        echo "${csffile}"
      fi
      if [[ ${url2} == *"_ventricle_"* ]]; then #  || [[ ${url2} == *"_levelset_bet"* ]]  || [[ ${url2} == *"csf_unet"* ]]  ; then ##[[ $string == *"My long"* ]]; then
        echo "It's there!"
        echo "${array2[6]}"
        filename2=$(basename ${url2})
        call_download_a_singlefile_with_URIString_arguments=('call_download_a_singlefile_with_URIString' ${url2} ${filename2} ${dir_to_save})
        outputfiles_present=$(python3 download_with_session_ID.py "${call_download_a_singlefile_with_URIString_arguments[@]}")
        csffile=${dir_to_save}/${filename2}
        echo "${csffile}"
      fi
    done < <(tail -n +2 "${working_dir}/${output_csvfile_1}")

  done < <(tail -n +2 "${dir_to_save}/${filename}")

done < <(tail -n +2 "${working_dir}/${output_csvfile}")

#if [[ -f "${greyfile}" ]] && [[ -f "${betfile}" ]] && [[ -f "${csffile}" ]]; then
#  call_csf_compartments_arguments=('call_csf_compartments' ${greyfile} ${csffile} ${betfile})
#  outputfiles_present=$(python3 /software/CSF_COMPARTMENT_GITHUB_July212023.py "${call_csf_compartments_arguments[@]}")
##  echo ${outputfiles_present}
#fi
#echo ${outputfiles_present}
#URI_1=${url2%/resource*}
#resource_dirname="MASKS"
#for file_name in ${dir_to_save}/*.nii.gz; do
#  echo ${file_name}
#  if [[ ${file_name} == *"ventricle"* ]] || [[ ${file_name} == *"sulci"* ]]; then
#    call_uploadsinglefile_with_URI_arguments=('call_uploadsinglefile_with_URI' ${URI_1} ${file_name} ${resource_dirname})
#    outputfiles_present=$(python3 /software/download_with_session_ID.py "${call_uploadsinglefile_with_URI_arguments[@]}")
#    echo ${outputfiles_present}
#
#  fi
#done
## single filename NECT, its CSF mask and other relevant files
#rm /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/CSFSEPERATION/TESTING_CSF_SEPERATION/error.txt
#greyfile='/workinginput/SAH_1_01052014_2003_2_resaved_levelset.nii.gz'
### '/media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/CSFSEPERATION/TESTING_CSF_SEPERATION/Krak_003_09042014_0949_MOZG_6.0_H31s_levelset.nii.gz'
#betfile='/workinginput/SAH_1_01052014_2003_2_resaved_levelset_bet.nii.gz'
##'/media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/CSFSEPERATION/TESTING_CSF_SEPERATION/Krak_003_09042014_0949_MOZG_6.0_H31s_levelset_bet.nii.gz'
#csffile='/workinginput/SAH_1_01052014_2003_2_resaved_csf_unet.nii.gz'
##'/media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/CSFSEPERATION/TESTING_CSF_SEPERATION/Krak_003_09042014_0949_MOZG_6.0_H31s_final_seg.nii.gz'
#
#call_csf_compartments_arguments=('call_csf_compartments' ${greyfile} ${csffile} ${betfile} )
#outputfiles_present=$(python3 /software/CSF_COMPARTMENT_GITHUB_July212023.py "${call_csf_compartments_arguments[@]}" )
#echo ${outputfiles_present}
###python /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/CSFSEPERATION/CSFCOMPARTMENT/CSF_COMPARTMENT_v1_part2_July18_2023.py
##
###pdflatex /media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/SAH_N_CSF_Compartment/RESULTS/test.tex

#
##########################################################################
### GET THE SINGLE CT NIFTI FILE NAME AND COPY IT TO THE WORKING_DIR
##niftifile_csvfilename=${working_dir}/'this_session_final_ct.csv'
##get_nifti_scan_uri ${sessionID}  ${working_dir} ${niftifile_csvfilename}
#call_download_files_in_a_resource_in_a_session_arguments=('call_download_files_in_a_resource_in_a_session' ${sessionID} "NIFTI_LOCATION" ${working_dir})
#outputfiles_present=$(python3 download_with_session_ID.py "${call_download_files_in_a_resource_in_a_session_arguments[@]}")
#echo '$outputfiles_present'::$outputfiles_present
#########################################
#for niftifile_csvfilename in ${working_dir}/*NIFTILOCATION.csv; do
#  rm ${final_output_directory}/*.*
#  rm ${output_directory}/*.*
#  outputfiles_present=0
#  echo $niftifile_csvfilename
#  while IFS=',' read -ra array; do
#    scanID=${array[2]}
#    echo sessionId::${sessionID}
#    echo scanId::${scanID}
#    snipr_output_foldername="EDEMA_BIOMARKER"
#    ### check if the file exists:
#    call_check_if_a_file_exist_in_snipr_arguments=('call_check_if_a_file_exist_in_snipr' ${sessionID} ${scanID} ${snipr_output_foldername} .pdf .csv)
#    outputfiles_present=$(python3 download_with_session_ID.py "${call_check_if_a_file_exist_in_snipr_arguments[@]}")
#
#    ################################################
#    outputfiles_present=0
#    echo "outputfiles_present:: "${outputfiles_present: -1}"::outputfiles_present"
#    #echo "outputfiles_present::ATUL${outputfiles_present}::outputfiles_present"
#    if [[ "${outputfiles_present: -1}" -eq 1 ]]; then
#      echo " I AM THE ONE"
#    fi
#    if [[ "${outputfiles_present: -1}" -eq 0 ]]; then ##[[ 1 -gt 0 ]]  ; then #
#
#      echo "outputfiles_present:: "${outputfiles_present: -1}"::outputfiles_present"
#
#      copy_scan_data ${niftifile_csvfilename} ${working_dir_1} #${working_dir}
#
#      ##############################################################################################################
#
#      ## GET THE RESPECTIVS MASKS NIFTI FILE NAME AND COPY IT TO THE WORKING_DIR
#
#      #####################################################################################
#      resource_dirname='MASKS'
#      output_dirname=${working_dir}
#      while IFS=',' read -ra array; do
#        scanID=${array[2]}
#        echo sessionId::${sessionID}
#        echo scanId::${scanID}
#      done < <(tail -n +2 "${niftifile_csvfilename}")
#      echo working_dir::${working_dir}
#      echo output_dirname::${output_dirname}
#      copy_masks_data ${sessionID} ${scanID} ${resource_dirname} ${output_dirname}
#      ######################################################################################################################
#      ## CALCULATE EDEMA BIOMARKERS
#      nwucalculation_each_scan
#      ######################################################################################################################
#      ## COPY IT TO THE SNIPR RESPECTIVE SCAN RESOURCES
#      snipr_output_foldername="EDEMA_BIOMARKER"
#      file_suffixes=(.pdf .mat .csv) #sys.argv[5]
#      for file_suffix in ${file_suffixes[@]}; do
#        copyoutput_to_snipr ${sessionID} ${scanID} "${final_output_directory}" ${snipr_output_foldername} ${file_suffix}
#      done
#      ######################################################################################################################
#      echo " FILES NOT PRESENT I AM WORKING ON IT"
#    else
#      echo " FILES ARE PRESENT "
#    ######################################################################################################################
#    fi
#    ##
#
#  done < <(tail -n +2 "${niftifile_csvfilename}")
#done

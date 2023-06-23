#!/bin/bash
export XNAT_USER=${2}
export XNAT_PASS=${3}
export XNAT_HOST=${4}
project_ID=${1}
working_dir=/workinginput
output_directory=/workingoutput

final_output_directory=/outputinsidedocker
####################
call_get_resourcefiles_metadata_saveascsv() {
  URI=${1}
  resource_dir=${2}
  dir_to_receive_the_data=${3}
  output_csvfile=${4}
  python3 -c "
import sys
sys.path.append('/software');
from download_with_session_ID import *;
call_get_resourcefiles_metadata_saveascsv()" ${URI} ${resource_dir} ${dir_to_receive_the_data} ${output_csvfile}
}
## for each session
function call_get_resourcefiles_metadata_saveascsv_args() {
  local resource_dir=${2}   #"NIFTI"
  local output_csvfile=${4} #{array[1]}

  local URI=${1} #{array[0]}
  local file_ext=${5}
  local output_csvfile=${output_csvfile%.*}${resource_dir}.csv

  local final_output_directory=${3}
  local call_download_files_in_a_resource_in_a_session_arguments=('call_get_resourcefiles_metadata_saveascsv_args' ${URI} ${resource_dir} ${final_output_directory} ${output_csvfile})
  outputfiles_present=$(python3 download_with_session_ID.py "${call_download_files_in_a_resource_in_a_session_arguments[@]}")

}

sessions_list=${working_dir}/'sessions.csv'
curl -u $XNAT_USER:$XNAT_PASS -X GET $XNAT_HOST/data/projects/${project_ID}/experiments/?format=csv >${sessions_list}

## for each selected scan in the session
counter=0
while IFS=',' read -ra array; do
  sessionID="${array[1]}"
  sessionLabel=${array[5]}
  #  if [ ${sessionID} == "SNIPR01_E01115" ] ; then
  call_download_files_in_a_resource_in_a_session_arguments=('call_download_files_in_a_resource_in_a_session' ${sessionID} "NIFTI_LOCATION" ${working_dir})
  outputfiles_present=$(python3 download_with_session_ID.py "${call_download_files_in_a_resource_in_a_session_arguments[@]}")
  #  echo "outputfiles_present:: "${outputfiles_present: -1}"::outputfiles_present"

  countfiles=$(ls ${working_dir}/*.csv | wc -l)
  for niftifile_csvfilename in ${working_dir}/*NIFTILOCATION.csv; do
    if [ -f "${niftifile_csvfilename}" ]; then

      outputfiles_present=0
      echo $niftifile_csvfilename
      while IFS=',' read -ra array1; do
        scanID=${array1[2]}
        echo sessionId::${sessionID}
        echo scanId::${scanID}
        ## NIFTI present
        snipr_output_foldername="NIFTI"
        call_check_if_a_file_exist_in_snipr_arguments=('call_check_if_a_file_exist_in_snipr' ${sessionID} ${scanID} ${snipr_output_foldername} .nii)
        outputfiles_present=$(python3 download_with_session_ID.py "${call_check_if_a_file_exist_in_snipr_arguments[@]}")
        NIFTIFILE_FLAG=${outputfiles_present: -1}
        echo "NIFTIFILE_FLAG:${NIFTIFILE_FLAG}"
        if [ ${NIFTIFILE_FLAG} -eq 1 ]; then
          echo "NIFTIFILE PRESET:${NIFTIFILE_FLAG}"
          resource_dir="NIFTI"
          output_csvfile=${array1[1]}
          echo ${output_csvfile}
          #          output_csvfile=${output_csvfile%.nii*}${resource_dirname}.csv
          URI=${array1[0]}
          call_fill_single_row_each_scan_arguments=('call_fill_single_row_each_scan' ${scanID} "SESSION_ID" ${sessionID} ${sessionLabel} ${final_output_directory}/csvfilename.csv)
          outputfiles_present=$(python3 fillmaster_session_list.py "${call_fill_single_row_each_scan_arguments[@]}")
          echo "outputfiles_present:: "${outputfiles_present}"::outputfiles_present"
          #          call_get_resourcefiles_metadata_saveascsv_args ${URI} ${resource_dir} ${final_output_directory} ${output_csvfile}
          #          echo "call_get_resourcefiles_metadata_saveascsv_args:: "${outputfiles_present: -1}"::outputfiles_present"
          #          resource_dir="MASKS"
          #          call_get_resourcefiles_metadata_saveascsv_args ${URI} ${resource_dir} ${final_output_directory} ${output_csvfile}
          #          echo "call_get_resourcefiles_metadata_saveascsv_args:: "${outputfiles_present: -1}"::outputfiles_present"
          #          resource_dir="EDEMA_BIOMARKER"
          #          call_get_resourcefiles_metadata_saveascsv_args ${URI} ${resource_dir} ${final_output_directory} ${output_csvfile}
          #          call_download_files_in_a_resource_in_a_session_arguments=('call_get_resourcefiles_metadata_saveascsv_args' ${URI} ${resource_dir} ${final_output_directory} ${output_csvfile})
          #          outputfiles_present=$(python3 download_with_session_ID.py "${call_download_files_in_a_resource_in_a_session_arguments[@]}")
          #          NIFTIFILE_CSV_FLAG=${outputfiles_present: -1}
          #          echo "NIFTIFILE_CSV_FLAG:${NIFTIFILE_CSV_FLAG}"

          #          call_get_resourcefiles_metadata_saveascsv ${URI} ${resource_dir} ${dir_to_receive_the_data} ${output_csvfile}
        fi
        counter=$((counter + 1))
      done < <(tail -n +2 "${niftifile_csvfilename}")
    fi
  done
  ################################################

  if [ ${countfiles} -gt 3 ]; then
    break
  fi
done < <(tail -n +2 "${sessions_list}")
## IF type has brain-axial or brain-thin
## check NIFTI for niftifile
## check MASKS for CSF,INFARCT masks
## check EDEMA_BIOMARKER for csv and pdf files

#
#fillmaster_session_list() {
#  session_csvfile=$1
#  dir_csv=$2
#  # typeofmask=$3 #"MASKS" #sys.argv[4]
#  filenametosave=$3
#  directorytosave=$4
#  filename_latex_tosave=${5}
#  echo " I AM IN fillmaster_session_list "
#  python3 -c "
#import sys
#from fillmaster_session_list import *;
#call_insertavailablefilenames()" ${session_csvfile} ${dir_csv} ${filenametosave} ${directorytosave} ${filename_latex_tosave} # ${infarctfile_present}  ##$static_template_image $new_image $backslicenumber #$single_slice_filename
#
#}
#
#copyoutput_to_snipr() {
#  sessionID=$1
#  scanID=$2
#  resource_dirname=$4 #"MASKS" #sys.argv[4]
#  file_suffix=$5
#  output_dir=$3
#  echo " I AM IN copyoutput_to_snipr "
#  python3 -c "
#import sys
#sys.path.append('/software');
#from download_with_session_ID import *;
#uploadfile()" ${sessionID} ${scanID} ${output_dir} ${resource_dirname} ${file_suffix} # ${infarctfile_present}  ##$static_template_image $new_image $backslicenumber #$single_slice_filename
#
#}
#
#copysinglefile_to_sniprproject() {
#  projectID=$1
#  #scanID=$2
#  resource_dirname=$3 #"MASKS" #sys.argv[4]
#  file_name=$4
#  output_dir=$2
#  echo " I AM IN copysinglefile_to_sniprproject "
#  python3 -c "
#import sys
#sys.path.append('/software');
#from download_with_session_ID import *;
#uploadsinglefile_projectlevel()" ${projectID} ${output_dir} ${resource_dirname} ${file_name} # ${infarctfile_present}  ##$static_template_image $new_image $backslicenumber #$single_slice_filename
#
#}
#
#copy_masks_data() {
#  echo " I AM IN copy_masks_data "
#  # rm -r /ZIPFILEDIR/*
#  sessionID=${1}
#  scanID=${2}
#  resource_dirname=${3} #str(sys.argv[4])
#  output_dirname=${4}   #str(sys.argv[3])
#  echo output_dirname::${output_dirname}
#  python3 -c "
#import sys
#sys.path.append('/software');
#from download_with_session_ID import *;
#downloadfiletolocaldir()" ${sessionID} ${scanID} ${resource_dirname} ${output_dirname} ### ${infarctfile_present}  ##$static_template_image $new_image $backslicenumber #$single_slice_filename
#
#}
#
#call_get_resourcefiles_metadata_saveascsv() {
#  URI=${1}
#  resource_dir=${2}
#  dir_to_receive_the_data=${3}
#  output_csvfile=${4}
#  python3 -c "
#import sys
#sys.path.append('/software');
#from download_with_session_ID import *;
#call_get_resourcefiles_metadata_saveascsv()" ${URI} ${resource_dir} ${dir_to_receive_the_data} ${output_csvfile}
#}
#copy_scan_data() {
#  echo " I AM IN copy_scan_data "
#  # rm -r /ZIPFILEDIR/*
#  # rm -r ${working_dir}/*
#  # rm -r ${output_dir}/*
#  sessionID=$1
#  dir_to_receive_the_data=${2}
#  resource_dir=${3}
#  # sessionId=sys.argv[1]
#  # dir_to_receive_the_data=sys.argv[2]
#  # resource_dir=sys.argv[3]
#  # scanID=$2
#  python -c "
#import sys
#sys.path.append('/Stroke_CT_Processing');
#from download_with_session_ID import *;
#get_relevantfile_in_A_DIRECTORY()" ${sessionID} ${dir_to_receive_the_data} ${resource_dir}
#
#}
#
#run_IML_NWU_CSF_CALC() {
#  this_filename=${1}
#  this_betfilename=${2}
#  this_csfmaskfilename=${3}
#  this_infarctmaskfilename=${4}
#  this_infarctmask1filename=${5}
#  echo "this_filename=${1}
#      this_betfilename=${2}
#      this_csfmaskfilename=${3}
#      this_infarctmaskfilename=${4}
#      this_infarctmask1filename=${5}"
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
#
#  echo "RUNNING ICH volume calculation for class 2 Mask"
#
#  /software/ich_csf_volume.sh ${this_filename} ${this_betfilename} ${this_csfmaskfilename} ${this_infarctmaskfilename} ${this_infarctmask1filename} #${upper_threshold}
#  echo "ich_csf_volume successful" >>${output_directory}/success.txt
#  thisfile_basename=$(basename $this_filename)
#  # for texfile in $(/usr/lib/fsl/5.0/remove_ext ${output_directory}/$thisfile_basename)*.tex ;
#  for texfile in ${output_directory}/*.tex; do
#    pdflatex -halt-on-error -interaction=nonstopmode -output-directory=${output_directory} $texfile ##${output_directory}/$(/usr/lib/fsl/5.0/remove_ext $this_filename)*.tex
#    rm ${output_directory}/*.aux
#    rm ${output_directory}/*.log
#  done
#  #
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
#
#}
#
#ich_calculation_each_scan() {
#
#  eachfile_basename_noext=''
#  originalfile_basename=''
#  original_ct_file=''
#  for eachfile in ${working_dir}/*.nii; do
#    original_ct_file=${eachfile}
#    eachfile_basename=$(basename ${eachfile})
#    originalfile_basename=${eachfile_basename}
#    eachfile_basename_noext=${eachfile_basename%.nii*}
#
#    ############## files basename ################################## 	ICH_0001_01012017_1028_2_resaved_4DL_normalized_class1.nii.gz  114 KB
#    grayfilename=${eachfile_basename_noext}_resaved_levelset.nii
#    betfilename=${eachfile_basename_noext}_resaved_levelset_bet.nii.gz
#    csffilename=${eachfile_basename_noext}_resaved_csf_unet.nii.gz
#    infarctfilename=${eachfile_basename_noext}_resaved_4DL_normalized_class1.nii.gz  #_resaved_infarct_auto_removesmall.nii.gz
#    infarctfilename1=${eachfile_basename_noext}_resaved_4DL_normalized_class2.nii.gz #_resaved_infarct_auto_removesmall.nii.gz
#    ################################################
#    ############## copy those files to the docker image ##################################
#    cp ${working_dir}/${betfilename} ${output_directory}/
#    cp ${working_dir}/${csffilename} ${output_directory}/
#    cp ${working_dir}/${infarctfilename} ${output_directory}/
#    cp ${working_dir}/${infarctfilename1} ${output_directory}/
#    ####################################################################################
#    source /software/bash_functions_forhost.sh
#
#    cp ${original_ct_file} ${output_directory}/${grayfilename}
#    grayimage=${output_directory}/${grayfilename} #${gray_output_subdir}/${eachfile_basename_noext}_resaved_levelset.nii
#    ###########################################################################
#
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
#
#    ####################################################################
#    levelset_infarct_mask_file1=${output_directory}/${infarctfilename1}
#    echo "levelset_infarct_mask_file:${levelset_infarct_mask_file1}"
#    ## preprocessing infarct mask:
#    python3 -c "
#import sys ;
#sys.path.append('/software/') ;
#from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${original_ct_file}" "${levelset_infarct_mask_file1}" "${output_directory}"
#
#    ######################################################################
#
#    ## preprocessing bet mask:
#    levelset_bet_mask_file=${output_directory}/${betfilename}
#    echo "levelset_bet_mask_file:${levelset_bet_mask_file}"
#    python3 -c "
#
#import sys ;
#sys.path.append('/software/') ;
#from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${original_ct_file}" "${levelset_bet_mask_file}" "${output_directory}"
#
#    #### preprocessing csf mask:
#    levelset_csf_mask_file=${output_directory}/${csffilename}
#    echo "levelset_csf_mask_file:${levelset_csf_mask_file}"
#    python3 -c "
#import sys ;
#sys.path.append('/software/') ;
#from utilities_simple_trimmed import * ;   levelset2originalRF_new_flip()" "${original_ct_file}" "${levelset_csf_mask_file}" "${output_directory}"
#
#    lower_threshold=0
#    upper_threshold=20
#    templatefilename=scct_strippedResampled1.nii.gz
#    mask_on_template=midlinecssfResampled1.nii.gz
#
#    x=$grayimage
#    bet_mask_filename=${output_directory}/${betfilename}
#    infarct_mask_filename=${output_directory}/${infarctfilename}
#    infarct_mask_filename1=${output_directory}/${infarctfilename1}
#    csf_mask_filename=${output_directory}/${csffilename}
#    echo " FILENMAES:: $x ${bet_mask_filename} ${csf_mask_filename} ${infarct_mask_filename}  ${infarct_mask_filename1}"
#    run_IML_NWU_CSF_CALC $x ${bet_mask_filename} ${csf_mask_filename} ${infarct_mask_filename} ${infarct_mask_filename1}
#
#  done
#
#  # for f in ${output_directory}/*; do
#  #     # if [ -d "$f" ]; then
#  #         # $f is a directory
#  #         rm -r $f
#  #     # fi
#  # done
#
#}
#
## #####################################################
#get_nifti_scan_uri() {
#  # csvfilename=sys.argv[1]
#  # dir_to_save=sys.argv[2]
#  # echo " I AM IN copy_scan_data "
#  # rm -r /ZIPFILEDIR/*
#
#  sessionID=$1
#  working_dir=${2}
#  output_csvfile=${3}
#  rm -r ${working_dir}/*
#  output_dir=$(dirname ${output_csvfile})
#  rm -r ${output_dir}/*
#  # scanID=$2
#  python3 -c "
#import sys
#sys.path.append('/software');
#from download_with_session_ID import *;
#call_decision_which_nifti()" ${sessionID} ${working_dir} ${output_csvfile}
#
#}
#
#copy_scan_data() {
#  csvfilename=${1} #sys.argv[1]
#  dir_to_save=${2} #sys.argv[2]
#  # 		echo " I AM IN copy_scan_data "
#  # rm -r /ZIPFILEDIR/*
#  # rm -r ${working_dir}/*
#  # rm -r ${output_dir}/*
#  # sessionID=$1
#  # # scanID=$2
#  python3 -c "
#import sys
#sys.path.append('/software');
#from download_with_session_ID import *;
#downloadniftiwithuri_withcsv()" ${csvfilename} ${dir_to_save}
#
#}
#
#getmaskfilesscanmetadata() {
#  # def get_maskfile_scan_metadata():
#  sessionId=${1}           #sys.argv[1]
#  scanId=${2}              # sys.argv[2]
#  resource_foldername=${3} # sys.argv[3]
#  dir_to_save=${4}         # sys.argv[4]
#  csvfilename=${5}         # sys.argv[5]
#  python3 -c "
#import sys
#sys.path.append('/software');
#from download_with_session_ID import *;
#get_maskfile_scan_metadata()" ${sessionId} ${scanId} ${resource_foldername} ${dir_to_save} ${csvfilename}
#}
#combine_all_csvfiles_general() {
#  working_directory=${1}
#  working_directory_tocombinecsv=${2}
#  extension=${3}
#  outputfilename=${4}
#
#  python3 -c "
#import sys
#sys.path.append('/software');
#from download_with_session_ID import *;
#call_combine_all_csvfiles_general()" ${working_directory} ${working_directory_tocombinecsv} ${extension} ${outputfilename}
#}
#
#####################################################################################################################################################
#####################################################PART 1: SNIPR_ANALYTICS ########################################################################################
#####################################################################################################################################################
##########################################################################
### GET THE SINGLE CT NIFTI FILE NAME AND COPY IT TO THE WORKING_DIR
##listofsession=${final_output_directory}/'sessions.csv'
##project_ID="COLI"
##curl  -u   $XNAT_USER:$XNAT_PASS  -X GET   $XNAT_HOST/data/projects/${project_ID}/experiments/?format=csv  > ${listofsession}
#
##session_csvfile='sessions.csv' #$1
#dir_csv=$final_output_directory
## typeofmask="ICH" #$3 #"MASKS" #sys.argv[4]
##time_now=$(date -dnow +%Y%m%d%H%M)
##filenametosave=${project_ID}_CTSESSIONS_${time_now}.csv #4
##filename_latex_tosave=${project_ID}_CTSESSIONS_${time_now}.tex
##filename_pdf_tosave=${project_ID}_CTSESSIONS_${time_now}.pdf
#directorytosave=$final_output_directory
##fillmaster_session_list ${session_csvfile} ${dir_csv}  ${filenametosave} ${directorytosave} ${filename_latex_tosave}
#
### COPY IT TO THE SNIPR RESPECTIVE SCAN RESOURCES
#snipr_output_foldername="SNIPR_ANALYTICS_V1"
#call_project_resource_latest_analytic_file_arguments=('project_resource_latest_analytic_file' ${project_ID} ${snipr_output_foldername} .csv $directorytosave)
#outputfiles_present=$(python3 download_with_session_ID.py "${call_project_resource_latest_analytic_file_arguments[@]}")
##echo ${outputfiles_present}
##echo "outputfiles_present:: "${outputfiles_present: -1}"::outputfiles_present"
#previous_list_present="${outputfiles_present: -1}"
#previous_list_present=0
#if [ "${previous_list_present}" == "0" ]; then
#
#  csvfileslist=${final_output_directory}/'sessions.csv'
#  #project_ID="COLI"
#  curl -u $XNAT_USER:$XNAT_PASS -X GET $XNAT_HOST/data/projects/${project_ID}/experiments/?format=csv >${csvfileslist}
#  listofsession_current=${csvfileslist} #${csvfileslist%.csv}_not_done.csv
#else
#  echo " I am subsequent run!"
#  csvfileslist=${outputfiles_present##*CSVMASTERFILE::}
#  masktype="INFARCT"
#  call_divide_sessionlist_done_vs_undone_arguments=('call_divide_sessionlist_done_vs_undone' ${csvfileslist} ${masktype})
#  outputfiles_present=$(python3 download_with_session_ID.py "${call_divide_sessionlist_done_vs_undone_arguments[@]}")
##  echo ${outputfiles_present}
#  listofsession_previous=${csvfileslist%.csv}_done.csv
#  listofsession_current=${csvfileslist%.csv}_not_done.csv
#fi
#
##echo ${csvfileslist}
##
##echo ${listofsession_current}
##session_csvfile=$(ls $directorytosave/*.csv)
##listofsession=${final_output_directory}/'sessions.csv'
##mv $session_csvfile $listofsession
#counter=0
#while IFS=',' read -ra array; do
##  echo "${array[0]}"
#  sessionID_1="${array[1]}"
##  echo final_output_directory::${final_output_directory}
#  niftifile_csvfilename=${working_dir}/${sessionID_1}'this_session_final_ct.csv'
#
#  if [ $counter -lt 2 ]; then # $counter
##  if [ ${sessionID_1} == "SNIPR_E03515" ] ; then
##    echo "SESSIONID::${sessionID_1}"
#    get_nifti_scan_uri ${sessionID_1} ${working_dir} ${niftifile_csvfilename}
#
#    if [ -f ${niftifile_csvfilename} ]; then
##      echo "$niftifile_csvfilename exists."
#      cp ${niftifile_csvfilename} ${final_output_directory}
#      #############
#      resource_dirname='MASKS'
#      output_dirname=${final_output_directory}
#      while IFS=',' read -ra array; do
#        scanID=${array[2]}
##        echo sessionId::${sessionID}
##        echo scanId::${scanID}
#        output_csvfile=${array[1]}
#        output_csvfile=${output_csvfile%.nii*}${resource_dirname}.csv
##        echo scanId::${array[0]}::${array[1]}::${array[2]}::${array[3]}::${array[4]}::${output_csvfile}
#        URI=${array[0]}
#        resource_dir=${resource_dirname}
#        dir_to_receive_the_data=${final_output_directory}
#
#        call_get_resourcefiles_metadata_saveascsv ${URI} ${resource_dir} ${dir_to_receive_the_data} ${output_csvfile}
#
#        if [ ${project_ID} == "ICH" ]; then
##          resource_dirname="ICH_QUANTIFICATION"
#          resource_dir=${resource_dirname}
##          output_csvfile=${array[1]}
##          output_csvfile=${output_csvfile%.nii*}${resource_dirname}.csv
##          call_get_resourcefiles_metadata_saveascsv ${URI} ${resource_dir} ${dir_to_receive_the_data} ${output_csvfile}
#        else
#          resource_dirname="EDEMA_BIOMARKER"
#          resource_dir=${resource_dirname}
#          output_csvfile=${array[1]}
#          output_csvfile=${output_csvfile%.nii*}${resource_dirname}.csv
#          call_get_resourcefiles_metadata_saveascsv ${URI} ${resource_dir} ${dir_to_receive_the_data} ${output_csvfile}
#        fi
#      done < <(tail -n +2 "${niftifile_csvfilename}")
##    break
#      ##################
#
##      counter=$((counter + 1))
#    fi
#  fi
#  #if [[ $counter -gt 2 ]] ; then
#  #  break
#  #fi
#
#  #copy_latest_pdfs "ICH" ${working_dir} ${final_output_directory}
#done < <(tail -n +2 "${listofsession_current}")
#session_csvfile=${listofsession_current} #'sessions.csv' #$1
#dir_csv=$final_output_directory
## typeofmask="ICH" #$3 #"MASKS" #sys.argv[4]
#time_now=$(date -dnow +%Y%m%d%H%M)
#filenametosave=temp.csv        # ${project_ID}_CTSESSIONS_${time_now}.csv #4
#filename_latex_tosave=temp.tex # ${project_ID}_CTSESSIONS_${time_now}.tex #
#filename_pdf_tosave=temp.pdf   ## ${project_ID}_CTSESSIONS_${time_now}.pdf ##
#directorytosave=$final_output_directory
#fillmaster_session_list ${session_csvfile} ${dir_csv} ${filenametosave} ${directorytosave} ${filename_latex_tosave}
#
#
#filenametosave=${directorytosave}/${project_ID}_CTSESSIONS_${time_now}.csv #4
#if [ "${previous_list_present}" == "0" ]; then
#
#  call_concatenate_csv_list_arguments=('call_concatenate_csv_list' ${filenametosave} ${directorytosave}/temp.csv ${directorytosave}/temp.csv)
#  outputfiles_present=$(python3 download_with_session_ID.py "${call_concatenate_csv_list_arguments[@]}")
#else
#  call_concatenate_csv_list_arguments=('call_concatenate_csv_list' ${filenametosave} ${listofsession_previous} ${directorytosave}/temp.csv)
#  outputfiles_present=$(python3 download_with_session_ID.py "${call_concatenate_csv_list_arguments[@]}")
#fi
# echo ' ${filenametosave}'::${filenametosave}
##
#filename_latex_tosave=${directorytosave}/${project_ID}_CTSESSIONS_${time_now}.tex
#call_pdffromanalytics_arguments=('call_pdffromanalytics' ${filenametosave} ${filename_latex_tosave})
#outputfiles_present=$(python3 fillmaster_session_list.py "${call_pdffromanalytics_arguments[@]}")
#echo ${outputfiles_present}
### COPY IT TO THE SNIPR RESPECTIVE SCAN RESOURCES
##snipr_output_foldername="SNIPR_ANALYTICS"
#
##file_name=${filenametosave}
###file_suffixes=(  .pdf .mat .csv ) #sys.argv[5]
###for file_suffix in ${file_suffixes[@]}
###do
#filename_pdf_tosave=${directorytosave}/${project_ID}_CTSESSIONS_${time_now}.pdf
#
#pdflatex -halt-on-error -interaction=nonstopmode -output-directory=${final_output_directory} ${filename_latex_tosave}
#copysinglefile_to_sniprproject ${project_ID} "${final_output_directory}" ${snipr_output_foldername} $(basename ${filenametosave})
#copysinglefile_to_sniprproject ${project_ID} "${final_output_directory}" ${snipr_output_foldername} $(basename ${filename_pdf_tosave})
##################################################################################################################################################
##################################################PART 2: COMBINE CSVs and upload PDFs ########################################################################################
###################################################################################################################################################
###### FOR COMBINED CSV
#sessionlist_filename=${filenametosave} #args.stuff[1]
#masktype="INFARCT" ##args.stuff[2]
#filetype="CSV" #args.stuff[3]
#dir_to_save=${directorytosave} #args.stuff[4]
##upload_flag=0 #args.stuff[5]
#localfilelist_csv=${directorytosave}/csvfileslisttocombine.csv #args.stuff[5]
#listofsession_current=${listofsession_current}
#call_download_files_with_mastersessionlist_arguments=('call_download_files_with_mastersessionlist' ${sessionlist_filename} ${masktype} ${filetype} ${dir_to_save} ${localfilelist_csv} ${listofsession_current})
#outputfiles_present=$(python3 download_with_session_ID.py "${call_download_files_with_mastersessionlist_arguments[@]}" )
#echo ${outputfiles_present}
#localfilelist_csv=${localfilelist_csv}
#outputdirectory=${final_output_directory}
#combined_csv_outputfilename=${projectID}_EDEMA_BIOMARKERS_COMBINED_${time_now}.csv
#call_combinecsvs_inafileoflist_arguments=('call_combinecsvs_inafileoflist' ${localfilelist_csv} ${outputdirectory} ${combined_csv_outputfilename}  )
#outputfiles_present=$(python3 download_with_session_ID.py "${call_combinecsvs_inafileoflist_arguments[@]}" )
#snipr_output_foldername1="EDEMA_BIOMARKER_V1"
#if [ ${project_ID} == "ICH" ] ; then
#snipr_output_foldername1="ICH_BIOMARKER_V1"
#fi
#copysinglefile_to_sniprproject  ${project_ID}  "${final_output_directory}"  ${snipr_output_foldername1}  ${combined_csv_outputfilename}
#
#
##############FOR PDFs
#
#sessionlist_filename=${filenametosave} #args.stuff[1]
#masktype="INFARCT" ##args.stuff[2]
#if [ ${project_ID} == "ICH" ] ; then
#  masktype="ICH"
#fi
#filetype="PDF" #args.stuff[3]
#dir_to_save=${directorytosave} #args.stuff[4]
##upload_flag=0 #args.stuff[5]
#localfilelist_pdf=${directorytosave}/pdffilestodownload.csv #args.stuff[5]
#listofsession_current=${listofsession_current}
#call_download_files_with_mastersessionlist_arguments=('call_download_files_with_mastersessionlist' ${sessionlist_filename} ${masktype} ${filetype} ${dir_to_save} ${localfilelist_pdf} ${listofsession_current})
#outputfiles_present=$(python3 download_with_session_ID.py "${call_download_files_with_mastersessionlist_arguments[@]}" )
#
#urllistfilename=${localfilelist_pdf}
#X_level="projects"
#projectId="${project_ID}"
#resource_dirname=${snipr_output_foldername1}
#call_uploadfilesfromlistinacsv_arguments=('call_uploadfilesfromlistinacsv' ${urllistfilename} ${X_level} ${projectId} ${resource_dirname} )
#outputfiles_present=$(python3 download_with_session_ID.py "${call_uploadfilesfromlistinacsv_arguments[@]}" )
#echo "  "
#echo "  "
#echo "  "
##echo ${outputfiles_present}
#echo "END"
######
#######file_name=${filenametosave}
########file_suffixes=(  .pdf .mat .csv ) #sys.argv[5]
########for file_suffix in ${file_suffixes[@]}
########do
#######pdflatex -halt-on-error -interaction=nonstopmode   -output-directory=${final_output_directory} ${directorytosave}/${filename_latex_tosave}
#######copysinglefile_to_sniprproject  ${project_ID}  "${final_output_directory}"  ${snipr_output_foldername}  ${file_name}
#######copysinglefile_to_sniprproject  ${project_ID}  "${final_output_directory}"  ${snipr_output_foldername}  ${filename_pdf_tosave}
########done
#############################################################################################################################
#######
#######
########extension_csv='csv'
########combined_csv_outputfilename=${final_output_directory}/${project_ID}"_NIFTILIST_COMBINED.csv"
########combine_all_csvfiles_general  ${final_output_directory} ${final_output_directory} ${extension_csv} ${combined_csv_outputfilename}
########################################################
########
#########get_nifti_scan_uri ${sessionID}  ${working_dir} ${niftifile_csvfilename}
#########copy_scan_data ${niftifile_csvfilename} ${working_dir}
########
########
########
########
#######################################################################################################################
########
########## GET THE RESPECTIVS MASKS NIFTI FILE NAME AND COPY IT TO THE WORKING_DIR
########
#############################################################################################
########resource_dirname='MASKS'
########output_dirname=${working_dir}
########while IFS=',' read -ra array; do
########scanID=${array[2]}
########echo sessionId::${sessionID}
########echo scanId::${scanID}
#########call_get_resourcefiles_metadata_saveascsv ${URI} ${resource_dir} ${dir_to_receive_the_data} ${output_csvfile}
########done < <( tail -n +2 "${niftifile_csvfilename}" )
########echo working_dir::${working_dir}
########echo output_dirname::${output_dirname}
########copy_masks_data   ${sessionID}  ${scanID} ${resource_dirname} ${output_dirname}
##############################################################################################################################
########## CALCULATE EDEMA BIOMARKERS
########ich_calculation_each_scan
##############################################################################################################################
########## COPY IT TO THE SNIPR RESPECTIVE SCAN RESOURCES
########snipr_output_foldername="ICH_QUANTIFICATION"
########file_suffixes=(  .pdf .mat .csv ) #sys.argv[5]
########for file_suffix in ${file_suffixes[@]}
########do
########    copyoutput_to_snipr  ${sessionID} ${scanID} "${final_output_directory}"  ${snipr_output_foldername}  ${file_suffix}
########done
##############################################################################################################################
########

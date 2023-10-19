#!/bin/bash
export XNAT_USER=${2}
export XNAT_PASS=${3}
export XNAT_HOST=${4}
ARGS=("$@")
# Get the last argument
arguments_count=${#ARGS[@]}
#for project_ID in ${ARGS[@]}; do
for x in $(seq 0 1 $((arguments_count-1))) ; do
#  echo ${project_ID}
  if [[ $x -gt 4 ]] ; then
  echo ${ARGS[x]}
  fi
done
#
#PROJECT_ID_3=${ARGS[-1]}
#PROJECT_ID_2=${ARGS[-2]}
#PROJECT_ID_1=${ARGS[-3]}

##echo  ${outputfile}
##PROJECT_ID_1=${5}
##PROJECT_ID_2=${6}
##PROJECT_ID_3=${7}
#project_ID=${1}
#working_dir=/workinginput
#output_directory=/workingoutput
#
#final_output_directory=/outputinsidedocker
#####################
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
#copysinglefile_to_sniprproject() {
#  local projectID=$1
#  #scanID=$2
#  local resource_dirname=$3 #"MASKS" #sys.argv[4]
#  local file_name=$4
#  local output_dir=$2
#  echo " I AM IN copysinglefile_to_sniprproject "
#  python3 -c "
#import sys
#sys.path.append('/software');
#from download_with_session_ID import *;
#uploadsinglefile_projectlevel()" ${projectID} ${output_dir} ${resource_dirname} ${file_name} # ${infarctfile_present}  ##$static_template_image $new_image $backslicenumber #$single_slice_filename
#
#}
### for each session
#function call_get_resourcefiles_metadata_saveascsv_args() {
#  local resource_dir=${2}   #"NIFTI"
#  local output_csvfile=${4} #{array[1]}
#
#  local URI=${1} #{array[0]}
#  local file_ext=${5}
#  local output_csvfile=${output_csvfile%.*}${resource_dir}.csv
#
#  local final_output_directory=${3}
#  local call_download_files_in_a_resource_in_a_session_arguments=('call_get_resourcefiles_metadata_saveascsv_args' ${URI} ${resource_dir} ${final_output_directory} ${output_csvfile})
#  outputfiles_present=$(python3 download_with_session_ID.py "${call_download_files_in_a_resource_in_a_session_arguments[@]}")
#
#}
#
##sessions_list=${working_dir}/'sessions.csv'
#time_now=$(date -dnow +%Y%m%d%H%M%S)
#URI="/data/projects/"${project_ID}
#resource_dir="SNIPR_ANALYTICS_TEST"
#dir_to_receive_the_data=${working_dir}
#output_csvfile=${project_ID}"_metadata.csv"
#call_get_resourcefiles_metadata_saveascsv_args_arguments=('call_get_resourcefiles_metadata_saveascsv_args' ${URI} ${resource_dir} ${dir_to_receive_the_data} ${output_csvfile})
#outputfiles_present=$(python3 download_with_session_ID.py "${call_get_resourcefiles_metadata_saveascsv_args_arguments[@]}")
#
##copy_session=${sessions_list%.csv}_${project_ID}_ANALYTICS_${time_now}.csv
###scan_analytics=${sessions_list%sessions.csv}SCAN_ANALYTICS_${time_now}.csv
###scan_analytics_nofilename=${sessions_list%sessions.csv}SCAN_ANALYTICS_NOFILENAME${time_now}.csv
##curl -u $XNAT_USER:$XNAT_PASS -X GET $XNAT_HOST/data/projects/${project_ID}/experiments/?format=csv >${sessions_list}
##cp ${sessions_list} ${copy_session}
##counter=0
##while IFS=',' read -ra array; do
##  xx=0
##
##  #if [ ${array[1]} == "SNIPR01_E00894" ]  ; then
##  #  echo "${array[1]}"
##  #  echo "${array[5]}"
##  if [ ${array[4]} == "xnat:ctSessionData" ]; then
##    echo "${array[1]}"
##    echo "${array[5]}"
##    call_fill_sniprsession_list_arguments=('fill_sniprsession_list_SAH' ${copy_session} ${array[1]}) ##
##    ## ${working_dir}/${project_ID}_SNIPER_ANALYTICS.csv  ${project_ID} ${output_directory} )
##    outputfiles_present=$(python3 fillmaster_session_list.py "${call_fill_sniprsession_list_arguments[@]}")
##  #call_creat_analytics_onesessionscanasID_arguments=('call_creat_analytics_onesessionscanasID' ${array[1]} ${array[5]} ${scan_analytics}  ${scan_analytics_nofilename})
##  #outputfiles_present=$(python3 fillmaster_session_list.py "${call_creat_analytics_onesessionscanasID_arguments[@]}")
##  #def creat_analytics_onesessionscanasID(sessionId,sessionLabel,csvfilename,csvfilename_withoutfilename)
###  counter=$((counter + 1))
##  fi
###  if [ $counter -eq 7 ] ; then
###    break
###  fi
##done < <(tail -n +2 "${sessions_list}")
##
##
##dir_to_save=${working_dir}
##
##
##resource_dirname_at_snipr="SAH_SESSION_PROCESSING_ANALYTICS"
##call_edit_session_analytics_file_arguments=('call_edit_session_analytics_file' ${copy_session})
##outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
##
##
##copysinglefile_to_sniprproject ${project_ID} "${dir_to_save}" ${resource_dirname_at_snipr} $(basename ${copy_session})

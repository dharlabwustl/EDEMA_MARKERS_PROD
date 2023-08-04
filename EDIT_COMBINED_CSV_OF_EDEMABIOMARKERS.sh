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
copysinglefile_to_sniprproject() {
  local projectID=$1
  #scanID=$2
  local resource_dirname=$3 #"MASKS" #sys.argv[4]
  local file_name=$4
  local output_dir=$2
  echo " I AM IN copysinglefile_to_sniprproject "
  python3 -c "
import sys
sys.path.append('/software');
from download_with_session_ID import *;
uploadsinglefile_projectlevel()" ${projectID} ${output_dir} ${resource_dirname} ${file_name} # ${infarctfile_present}  ##$static_template_image $new_image $backslicenumber #$single_slice_filename

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
## Download combined csv file directory metadata
download_latest_file() {
  local URI=${1}          #/data/projects/${project_ID}
  local resource_dir=${2} #'EDEMA_BIOMARKER_TEST'
  #final_output_directory=${working_dir}
  local output_csvfile=${project_ID}_${resource_dir}"_metadata.csv"
  local call_get_resourcefiles_metadata_saveascsv_args_arguments=('call_get_resourcefiles_metadata_saveascsv_args' ${URI} ${resource_dir} ${working_dir} ${output_csvfile})
  local outputfiles_present=$(python3 download_with_session_ID.py "${call_get_resourcefiles_metadata_saveascsv_args_arguments[@]}")

  local metadata_filename=${working_dir}/${output_csvfile}
  local column_name=${3} #'URI'
  local file_ext=${4}    #'.csv'
  local outputfile_with_latestfilename=${working_dir}/${output_csvfile%.csv*}_latest_csvfile.csv
  local call_get_latest_file_from_metadata_arguments=('call_get_latest_file_from_metadata' ${metadata_filename} ${column_name} ${file_ext} ${outputfile_with_latestfilename})
  local outputfiles_present=$(python3 fillmaster_session_list.py "${call_get_latest_file_from_metadata_arguments[@]}")
  echo outputfiles_present::${outputfiles_present}
  local filename_to_download=${outputfiles_present#}

  ## downlaod scan level analytics data
  while IFS=',' read -ra array; do
    echo ${array[0]}

    local url=${array[0]}
    local filename=$(basename ${url})
    local dir_to_save=${working_dir}
    local call_download_a_singlefile_with_URIString_arguments=('call_download_a_singlefile_with_URIString' ${url} ${filename} ${dir_to_save})
    local outputfiles_present=$(python3 download_with_session_ID.py "${call_download_a_singlefile_with_URIString_arguments[@]}")
    echo outputfiles_present::${outputfiles_present}::${url}::${filename}::${dir_to_save}

  done < <(tail -n +2 "${outputfile_with_latestfilename}")

}
URI=/data/projects/${project_ID}
resource_dir='EDEMA_BIOMARKER_TEST'
column_name='URI'
file_ext='.csv'
download_latest_file ${URI} ${resource_dir} ${column_name} ${file_ext}
#
#URI=/data/projects/${project_ID}
#resource_dir='EDEMA_BIOMARKER_TEST'
##final_output_directory=${working_dir}
#output_csvfile=${project_ID}_${resource_dir}"_metadata.csv"
#call_get_resourcefiles_metadata_saveascsv_args_arguments=('call_get_resourcefiles_metadata_saveascsv_args' ${URI} ${resource_dir} ${working_dir} ${output_csvfile})
#outputfiles_present=$(python3 download_with_session_ID.py "${call_get_resourcefiles_metadata_saveascsv_args_arguments[@]}")
#
#metadata_filename=${working_dir}/${output_csvfile}
#column_name='URI'
#file_ext='.csv'
#outputfile_with_latestfilename=${working_dir}/${output_csvfile%.csv*}_latest_csvfile.csv
#call_get_latest_file_from_metadata_arguments=('call_get_latest_file_from_metadata' ${metadata_filename} ${column_name} ${file_ext} ${outputfile_with_latestfilename})
#outputfiles_present=$(python3 fillmaster_session_list.py "${call_get_latest_file_from_metadata_arguments[@]}")
#echo outputfiles_present::${outputfiles_present}
#filename_to_download=${outputfiles_present#}
#
### downlaod scan level analytics data
#while IFS=',' read -ra array; do
#  echo ${array[0]}
#
#  url=${array[0]}
#  filename=$(basename ${url})
#  dir_to_save=${working_dir}
#  call_download_a_singlefile_with_URIString_arguments=('call_download_a_singlefile_with_URIString' ${url} ${filename} ${dir_to_save})
#  outputfiles_present=$(python3 download_with_session_ID.py "${call_download_a_singlefile_with_URIString_arguments[@]}")
#  echo outputfiles_present::${outputfiles_present}::${url}::${filename}::${dir_to_save}
#
#done < <(tail -n +2 "${outputfile_with_latestfilename}")
## add columns with the values:

#
#sessions_list=${working_dir}/'sessions.csv'
#time_now=$(date -dnow +%Y%m%d%H%M%S)
#copy_session=${sessions_list%.csv}_${project_ID}_ANALYTICS_${time_now}.csv
##scan_analytics=${sessions_list%sessions.csv}SCAN_ANALYTICS_${time_now}.csv
##scan_analytics_nofilename=${sessions_list%sessions.csv}SCAN_ANALYTICS_NOFILENAME${time_now}.csv
#curl -u $XNAT_USER:$XNAT_PASS -X GET $XNAT_HOST/data/projects/${project_ID}/experiments/?format=csv >${sessions_list}
#cp ${sessions_list} ${copy_session}
#counter=0
#while IFS=',' read -ra array; do
#  xx=0
#
#  #if [ ${array[1]} == "SNIPR01_E00894" ]  ; then
#  #  echo "${array[1]}"
#  #  echo "${array[5]}"
#  if [ ${array[4]} == "xnat:ctSessionData" ]; then
#    echo "${array[1]}"
#    echo "${array[5]}"
#    call_fill_sniprsession_list_arguments=('call_fill_sniprsession_list' ${copy_session} ${array[1]}) ##
#    ## ${working_dir}/${project_ID}_SNIPER_ANALYTICS.csv  ${project_ID} ${output_directory} )
#    outputfiles_present=$(python3 fillmaster_session_list.py "${call_fill_sniprsession_list_arguments[@]}")
#  #call_creat_analytics_onesessionscanasID_arguments=('call_creat_analytics_onesessionscanasID' ${array[1]} ${array[5]} ${scan_analytics}  ${scan_analytics_nofilename})
#  #outputfiles_present=$(python3 fillmaster_session_list.py "${call_creat_analytics_onesessionscanasID_arguments[@]}")
#  #def creat_analytics_onesessionscanasID(sessionId,sessionLabel,csvfilename,csvfilename_withoutfilename)
#  #counter=$((counter + 1))
#  fi
#  #if [ $counter -eq 7 ] ; then
#  #  break
#  #fi
#done < <(tail -n +2 "${sessions_list}")
#
##call_edit_scan_analytics_file_arguments=('call_edit_scan_analytics_file'  ${scan_analytics}  ${scan_analytics_nofilename})
##outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_scan_analytics_file_arguments[@]}")
##X_level="projects"
##level_name=${project_ID}
#dir_to_save=${working_dir}
##resource_dirname_at_snipr="EDEMA_BIOMARKER_TEST"
##call_upload_pdfs_arguments=('call_upload_pdfs'  ${scan_analytics}  ${X_level} ${level_name} ${dir_to_save} ${resource_dirname_at_snipr} )
##outputfiles_present=$(python3 fillmaster_session_list.py "${call_upload_pdfs_arguments[@]}")
##
##outputfilename=${project_ID}_EDEMA_BIOMARKERS_COMBINED_${time_now}.csv
##call_download_csvs_combine_upload_v1_arguments=('call_download_csvs_combine_upload_v1'  ${scan_analytics}  ${sessions_list} ${dir_to_save} ${outputfilename} )
##outputfiles_present=$(python3 fillmaster_session_list.py "${call_download_csvs_combine_upload_v1_arguments[@]}")
##
##copysinglefile_to_sniprproject  ${project_ID}  "${dir_to_save}"  ${resource_dirname_at_snipr}  ${outputfilename}
#resource_dirname_at_snipr="SNIPR_ANALYTICS_TEST"
#call_edit_session_analytics_file_arguments=('call_edit_session_analytics_file' ${copy_session})
#outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
#
##copysinglefile_to_sniprproject  ${project_ID}  "${dir_to_save}"  ${resource_dirname_at_snipr}  $(basename ${scan_analytics} )
##copysinglefile_to_sniprproject  ${project_ID}  "${dir_to_save}"  ${resource_dirname_at_snipr}  $(basename ${scan_analytics_nofilename} )
#copysinglefile_to_sniprproject ${project_ID} "${dir_to_save}" ${resource_dirname_at_snipr} $(basename ${copy_session})

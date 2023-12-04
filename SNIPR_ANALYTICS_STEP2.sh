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
download_a_single_file() {
  local file_path_csv=${1}
  local dir_to_save=${2} #args.stuff[3]
  local projectid=${3}
  local output_filename=${4}

  while IFS=',' read -ra array; do
    echo array::${array[0]}

    local get_latest_filepath_from_metadata_arguments=('download_a_singlefile_with_URIString' ${array[0]} ${output_filename} ${dir_to_save})
    local outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
  done < <(tail -n +2 "${file_path_csv}")

}
URI="/data/projects/"${project_ID}
dir_to_receive_the_data=${working_dir}
resource_dir="${project_ID}_SESSION_ANALYTICS_1"
file_path_csv=${dir_to_receive_the_data}/${project_ID}"_${resource_dir}_resultfilepath.csv"

get_latest_filepath_from_metadata_arguments=('get_latest_filepath_from_metadata_for_analytics' ${URI} ${resource_dir} ".csv" "sessions_${project_ID}_ANALYTICS_STEP1_" ${file_path_csv})
outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
sessions_list=${working_dir}/'sessions.csv'
time_now=$(date -dnow +%Y%m%d%H%M%S)
copy_session=${sessions_list%.csv}_${project_ID}_ANALYTICS_STEP2_${time_now}.csv
download_a_single_file ${file_path_csv} ${dir_to_receive_the_data} ${project_ID} ${copy_session}

counter=0

while IFS=',' read -ra array; do
  xx=0

  if [ ${array[4]} == "xnat:ctSessionData" ]; then
    echo "${array[1]}"
    echo "${array[5]}"
    call_fill_sniprsession_list_arguments=('fill_sniprsession_list_1' ${copy_session} ${array[1]}) ##
    if [ ${project_ID} == "ICH" ]; then
      call_fill_sniprsession_list_arguments=('fill_sniprsession_list_ICH' ${copy_session} ${array[1]}) ##
    fi
    outputfiles_present=$(python3 fillmaster_session_list.py "${call_fill_sniprsession_list_arguments[@]}")
    counter=$((counter + 1))
  fi
  if [ $counter -eq 1 ]; then
    break
  fi
done < <(tail -n +2 "${copy_session}")
dir_to_save=${working_dir}
resource_dirname_at_snipr=${project_ID}"_SESSION_ANALYTICS_2"

##############################
time_now=$(date -dnow +%Y%m%d%H%M%S)
while IFS=',' read -ra array; do
  file_url=${array[14]}
  if [[ ${file_url} == *".pdf"* ]]; then
    session_ID=${array[0]}
    echo session_ID::${session_ID}
    echo file_url::${file_url}

    echo copy_session::${copy_session}
    temp_dir=${working_dir}
    echo temp_dir::${temp_dir}
    call_edit_session_analytics_file_arguments=('add_file_size' ${session_ID} ${file_url} ${copy_session} "PDF_FILE_SIZE" ${temp_dir})
    outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
  fi
done < <(tail -n +2 "${copy_session}")
##############################
#subject_list=${working_dir}/'subjects.csv'
#curl -u $XNAT_USER:$XNAT_PASS -X GET $XNAT_HOST/data/projects/${project_ID}/subjects/?format=csv >${subject_list}
#create_subject_id_arguments=('create_subject_id_from_snipr' ${subject_list} ${copy_session} ${copy_session})
#outputfiles_present=$(python3 fillmaster_session_list.py "${create_subject_id_arguments[@]}")

copysinglefile_to_sniprproject ${project_ID} "$(dirname ${copy_session})" ${resource_dirname_at_snipr} $(basename ${copy_session})

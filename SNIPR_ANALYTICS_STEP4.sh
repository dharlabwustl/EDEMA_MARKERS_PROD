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
resource_dir="${project_ID}_SESSION_ANALYTICS_3"
file_path_csv=${dir_to_receive_the_data}/${project_ID}"_${resource_dir}_resultfilepath.csv"
#get_latest_filepath_from_metadata_arguments=('get_latest_filepath_from_metadata_for_analytics' ${URI} ${resource_dir} ".csv" "sessions${project_ID}_ANALYTICS_STEP3_" ${file_path_csv})
get_latest_filepath_from_metadata_arguments=('get_latest_filepath_from_metadata_for_analytics' ${URI} ${resource_dir} ".csv" "${project_ID}_SESSIONS_RESULTS_METRICS" ${file_path_csv})

#BJH_SESSIONS_RESULTS_METRICS_20240211000149
outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
sessions_list=${working_dir}/'sessions.csv'
time_now=$(date -dnow +%Y%m%d%H%M%S)
copy_session=${sessions_list%.csv}_${project_ID}_ANALYTICS_STEP4_${time_now}.csv
download_a_single_file ${file_path_csv} ${dir_to_receive_the_data} ${project_ID} ${copy_session}
counter=0
dir_to_save=${output_directory}
while IFS=',' read -ra array; do
  echo session_name::${array[1]} #4]}
  pdf_file_location=${array[23]} #30]} #14]}
  csv_file_location=${array[23]} #33]}#15]}
#  this_session_id=${array[4]} #1]}
  n_pdffilename_length=${#pdf_file_location}
  echo ${n_pdffilename_length}
  n_csvfilename_length=${#csv_file_location}
  echo ${n_csvfilename_length}
    if [ ${n_pdffilename_length} -gt 1 ]; then
      resource_dirname_at_snipr=${project_ID}'_RESULTS_PDF'
      output_filename=$(basename ${pdf_file_location})
      get_latest_filepath_from_metadata_arguments=('download_a_singlefile_with_URIString' ${pdf_file_location} ${output_filename} ${dir_to_save})
      outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
      copysinglefile_to_sniprproject ${project_ID} "${dir_to_save}" ${resource_dirname_at_snipr} ${output_filename}
      counter=$((counter + 1))
    fi
#  if [ $counter -gt 2 ]; then
#    break
#  fi
done < <(tail -n +2 "${copy_session}")

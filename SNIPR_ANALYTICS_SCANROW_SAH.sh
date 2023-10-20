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
resource_dir="SAH_SESSION_PROCESSING_ANALYTICS"
file_path_csv=${dir_to_receive_the_data}/${project_ID}"_${resource_dir}_resultfilepath.csv"
get_latest_filepath_from_metadata_arguments=('get_latest_filepath_from_metadata' ${URI} ${resource_dir} ".csv" "sessions_SAH_ANALYTICS_20231019173144" ${file_path_csv})
outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
sessions_list=${working_dir}/${project_ID}'_sessions.csv'
time_now=$(date -dnow +%Y%m%d%H%M%S)
copy_session=${sessions_list%.csv}_ANALYTICS_${time_now}.csv
download_a_single_file ${file_path_csv} ${dir_to_receive_the_data} ${project_ID} ${copy_session}
counter=0
dir_to_save=${output_directory}


while IFS=',' read -ra array; do
  echo array::${array[3]}
  pdf_file_location=${array[3]}
  csv_file_location=${array[4]}
  n_pdffilename_length=${#pdf_file_location}
  echo ${n_pdffilename_length}
  if [ ${n_pdffilename_length} -gt 1 ]; then
    resource_dirname_at_snipr='SAH_RESULTS_PDF'
    output_filename=$(basename ${pdf_file_location})
    get_latest_filepath_from_metadata_arguments=('download_a_singlefile_with_URIString' ${pdf_file_location} ${output_filename} ${dir_to_save})
    outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
    copysinglefile_to_sniprproject  ${project_ID}  "${dir_to_save}"  ${resource_dirname_at_snipr}  ${output_filename}
    counter=$((counter + 1))
  fi
  n_csvfilename_length=${#csv_file_location}
  echo ${n_csvfilename_length}
  if [ ${n_csvfilename_length} -gt 1 ]; then
    csv_output_filename=$(basename ${csv_file_location})
    get_latest_filepath_from_metadata_arguments=('download_a_singlefile_with_URIString' ${csv_file_location} ${csv_output_filename} ${dir_to_save})
    outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
  fi

  if [ $counter -eq 2 ]; then
    break
  fi
done < <(tail -n +2 "${copy_session}")
#
csvfile_list="${working_dir}/CSV_FILENAMES_LIST.csv"
echo "CSV_FILENAMES" > ${csvfile_list}
for eachfilename in ${dir_to_save}/*.csv ; do echo $eachfilename >> ${csvfile_list} ; done
combined_metrics_results="${working_dir}/COMBINED_SESSIONS_SAH_METRICS_${time_now}.csv"
combinecsvsfiles_from_a_csv_containing_its_list_arguments=('combinecsvsfiles_from_a_csv_containing_its_list' ${csvfile_list} ${combined_metrics_results} )
outputfiles_present=$(python3 system_analysis.py "${combinecsvsfiles_from_a_csv_containing_its_list_arguments[@]}")
resource_dirname_at_snipr='SAH_RESULTS_CSV'
copysinglefile_to_sniprproject  ${project_ID}  "${working_dir}"  ${resource_dirname_at_snipr}  $(basename ${combined_metrics_results})

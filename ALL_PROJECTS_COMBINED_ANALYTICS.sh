#!/bin/bash
export XNAT_USER=${1}
export XNAT_PASS=${2}
export XNAT_HOST=${3}
working_dir=/workinginput
output_directory=/workingoutput

final_output_directory=/outputinsidedocker
ARGS=("$@")
# Get the last argument
arguments_count=${#ARGS[@]}
#for project_ID in ${ARGS[@]}; do
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

  while IFS=',' read -ra array; do
    echo array::${array[0]}
    local get_latest_filepath_from_metadata_arguments=('download_a_singlefile_with_URIString' ${array[0]} ${projectid}$(basename ${array[0]}) ${dir_to_save})
    local outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
  done < <(tail -n +2 "${file_path_csv}")

}

for x in $(seq 0 1 $((arguments_count - 1))); do
  #  echo ${project_ID}
  if [[ $x -gt 2 ]]; then

    project_ID=${ARGS[x]}
    echo PROJECTID::${project_ID}

    ##sessions_list=${working_dir}/'sessions.csv'
    time_now=$(date -dnow +%Y%m%d%H%M%S)
    URI="/data/projects/"${project_ID}
    dir_to_receive_the_data=${output_directory}
    analytics_file_dir=${working_dir}
    if [ ${project_ID} == "COLI" ]; then
      resource_dir="EDEMA_BIOMARKER_TEST"
      file_path_csv=${analytics_file_dir}/${project_ID}"_${resource_dir}_resultfilepath.csv"
      get_latest_filepath_from_metadata_arguments=('get_latest_filepath_from_metadata' ${URI} ${resource_dir} ".csv" "COLI_EDEMA_BIOMARKERS_COMBINED_20231003124834" ${file_path_csv})
      outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
      echo ${outputfiles_present}
      download_a_single_file ${file_path_csv} ${dir_to_receive_the_data}
      resource_dir="SNIPR_ANALYTICS_TEST"
      file_path_csv=${analytics_file_dir}/${project_ID}"_${resource_dir}_resultfilepath.csv"
      get_latest_filepath_from_metadata_arguments=('get_latest_filepath_from_metadata' ${URI} ${resource_dir} ".csv" "sessions_ANALYTICS_20231003124834" ${file_path_csv})
      outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
      download_a_single_file ${file_path_csv} ${analytics_file_dir} ${project_ID}

    elif [ ${project_ID} == "MGBBMC" ]; then
      resource_dir="EDEMA_BIOMARKER_TEST"
      file_path_csv=${analytics_file_dir}/${project_ID}"_${resource_dir}_resultfilepath.csv"
      get_latest_filepath_from_metadata_arguments=('get_latest_filepath_from_metadata' ${URI} ${resource_dir} ".csv" "MGBBMC_EDEMA_BIOMARKERS_COMBINED_20231009173614_modified_20231016200619" ${file_path_csv})
      outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
      download_a_single_file ${file_path_csv} ${dir_to_receive_the_data}
      resource_dir="SNIPR_ANALYTICS_TEST"
      file_path_csv=${analytics_file_dir}/${project_ID}"_${resource_dir}_resultfilepath.csv"
      get_latest_filepath_from_metadata_arguments=('get_latest_filepath_from_metadata' ${URI} ${resource_dir} ".csv" "sessions_ANALYTICS_20231009173614" ${file_path_csv})
      outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
      download_a_single_file ${file_path_csv} ${analytics_file_dir} ${project_ID}
    elif [ ${project_ID} == "ICH" ]; then
      resource_dir="ICH_QUANTIFICATION"
      file_path_csv=${analytics_file_dir}/${project_ID}"_${resource_dir}_resultfilepath.csv"
      get_latest_filepath_from_metadata_arguments=('get_latest_filepath_from_metadata' ${URI} ${resource_dir} ".csv" "ICH_EDEMA_BIOMARKERS_COMBINED_" ${file_path_csv})
      outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
      download_a_single_file ${file_path_csv} ${dir_to_receive_the_data}
      resource_dir="SNIPR_ANALYTICS"
      file_path_csv=${analytics_file_dir}/${project_ID}"_${resource_dir}_resultfilepath.csv"
      get_latest_filepath_from_metadata_arguments=('get_latest_filepath_from_metadata' ${URI} ${resource_dir} ".csv" "ICH_CTSESSIONS_202305222109" ${file_path_csv})
      outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
      download_a_single_file ${file_path_csv} ${analytics_file_dir} ${project_ID}
    fi

  fi

done
time_now=$(date -dnow +%Y%m%d%H%M%S)
csvfile_list="${working_dir}/CSV_FILENAMES_LIST.csv"
echo "CSV_FILENAMES" >${csvfile_list}
for eachfilename in ${dir_to_receive_the_data}/*.csv; do echo $eachfilename >>${csvfile_list}; done
combined_metrics_results="${working_dir}/COMBINED_PROJECTS_DIFFERENT_METRICS_${time_now}.csv"
combinecsvsfiles_from_a_csv_containing_its_list_arguments=('combinecsvsfiles_from_a_csv_containing_its_list' ${csvfile_list} ${combined_metrics_results})
outputfiles_present=$(python3 system_analysis.py "${combinecsvsfiles_from_a_csv_containing_its_list_arguments[@]}")
### histograms: CSF ratio='CSF RATIO', NWU='NWU' , ICH volumes:'ICH VOLUME' 'ICH EDEMA VOLUME'

csvfilename=${combined_metrics_results} #args.stuff[1]
column_name="NWU"                       #args.stuff[2]
output_image_name=${working_dir}/${column_name}"_HISTOGRAM.png" #args.stuff[3]
histogram_column_ina_csvfile_arguments=('histogram_column_ina_csvfile' ${csvfile_list} ${combined_metrics_results})
outputfiles_present=$(python3 system_analysis.py "${histogram_column_ina_csvfile_arguments[@]}")

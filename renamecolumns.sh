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
time_now=$(date -dnow +%Y%m%d%H%M%S)
csvfilename=${sessions_list%.csv}_${project_ID}_RESULTS_CSV_COLUMNS_RENAMED_${time_now}.csv
URI="/data/projects/"${project_ID}
dir_to_receive_the_data=${working_dir}
resource_dir="${project_ID}_RESULTS_CSV"
file_path_csv=${dir_to_receive_the_data}/${project_ID}"_${resource_dir}_resultfilepath.csv"
get_latest_filepath_from_metadata_arguments=('get_latest_filepath_from_metadata_for_analytics' ${URI} ${resource_dir} ".csv" "sessions_${project_ID}_ANALYTICS" ${file_path_csv})
outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
cp ${file_path_csv} ${csvfilename}

call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} subject_id  subject)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} label  snipr_session)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} SCAN_SELECTED  scan_selected)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} acquisition_datetime  scan_date_time)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} FILENAME_NIFTI  scan_name)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} SLICE_NUM  slices)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} res_x  px)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} res_y  py)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} slice_thickness  coverage)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} scanner  scanner_name)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} body_part  body_site)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} SCAN_DESCRIPTION  scan_kernel)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} 'LEFT CSF VOLUME'  csf_left)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} 'RIGHT CSF VOLUME'  csf_right)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} 'TOTAL CSF VOLUME'  csf_total)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} 'INFARCT SIDE'  stroke_side)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} 'NWU'  nwu)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} 'INFARCT VOLUME'  infarct_volume)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} 'BET VOLUME'  cranial)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} 'CSF RATIO'  csf_ratio)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} 'LEFT BRAIN VOLUME without CSF'  brain_left)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} 'RIGHT BRAIN VOLUME without CSF'  brain_right)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} 'NIFTIFILES_PREFIX'  scan_stem)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")

call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} 'PDF_FILE_NUM'  pdf_created)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
#resource_dirname_at_snipr=${project_ID}'_RESULTS_CSV'
#copysinglefile_to_sniprproject ${project_ID} "$(dirname ${csvfilename})" ${resource_dirname_at_snipr} $(basename ${csvfilename})
#
##resource_dirname_at_snipr=${project_ID}'_RESULTS_CSV'
#copysinglefile_to_sniprproject ${project_ID} "$(dirname ${new_analytics_file})" ${resource_dirname_at_snipr} $(basename ${new_analytics_file})


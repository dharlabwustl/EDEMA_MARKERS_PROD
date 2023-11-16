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
resource_dir="${project_ID}_SESSION_PROCESSING_ANALYTICS"
file_path_csv=${dir_to_receive_the_data}/${project_ID}"_${resource_dir}_resultfilepath.csv"
get_latest_filepath_from_metadata_arguments=('get_latest_filepath_from_metadata_for_analytics' ${URI} ${resource_dir} ".csv" "sessions_${project_ID}_ANALYTICS" ${file_path_csv})
outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
sessions_list=${working_dir}/${project_ID}'_sessions.csv'
time_now=$(date -dnow +%Y%m%d%H%M%S)
copy_session=${sessions_list%.csv}_RESULTS_${time_now}.csv
download_a_single_file ${file_path_csv} ${dir_to_receive_the_data} ${project_ID} ${copy_session}
counter=0
dir_to_save=${output_directory}
subject_list=${working_dir}/'subjects.csv'
curl -u $XNAT_USER:$XNAT_PASS -X GET $XNAT_HOST/data/projects/${project_ID}/subjects/?format=csv >${subject_list}
while IFS=',' read -ra array; do
  echo array::${array[3]}
  pdf_file_location=${array[3]}
  csv_file_location=${array[4]}
  this_session_id=${array[0]}
  n_pdffilename_length=${#pdf_file_location}
  echo ${n_pdffilename_length}
  xml_filename=${workinginput}/${this_session_id}.xml
  curl -u $XNAT_USER:$XNAT_PASS -X GET 'https://snipr.wustl.edu/app/action/XDATActionRouter/xdataction/xml_file/search_element/xnat%3ActSessionData/search_field/xnat%3ActSessionData.ID/search_value/'${this_session_id} >${xml_filename}

#  if [ ${n_pdffilename_length} -gt 1 ]; then
#    resource_dirname_at_snipr=${project_ID}'_RESULTS_PDF'
#    output_filename=$(basename ${pdf_file_location})
#    get_latest_filepath_from_metadata_arguments=('download_a_singlefile_with_URIString' ${pdf_file_location} ${output_filename} ${dir_to_save})
#    outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
#    copysinglefile_to_sniprproject ${project_ID} "${dir_to_save}" ${resource_dirname_at_snipr} ${output_filename}
#    counter=$((counter + 1))
#  fi
  n_csvfilename_length=${#csv_file_location}
  echo ${n_csvfilename_length}
  if [ ${n_csvfilename_length} -gt 1 ]; then
    csv_output_filename=$(basename ${csv_file_location})
    get_latest_filepath_from_metadata_arguments=('download_a_singlefile_with_URIString' ${csv_file_location} ${csv_output_filename} ${dir_to_save})
    outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
    append_results_to_analytics_arguments=('append_results_to_analytics' ${copy_session} ${dir_to_save}/${csv_output_filename} ${this_session_id} ${copy_session})
    outputfiles_present=$(python3 fillmaster_session_list.py "${append_results_to_analytics_arguments[@]}")
    session_id=${this_session_id}
    xmlfile=${xml_filename}
    csvfilename=${copy_session}
    subj_listfile=${subject_list}

    append_sessionxmlinfo_to_analytics_arguments=('append_sessionxmlinfo_to_analytics' ${session_id} ${xmlfile} ${csvfilename} ${subj_listfile})
    outputfiles_present=$(python3 fillmaster_session_list.py "${append_sessionxmlinfo_to_analytics_arguments[@]}")
    counter=$((counter + 1))
  fi

  if [ $counter -gt  2 ]; then
    break
  fi
#    if [ $counter -lt 160 ]; then
#      continue
#    fi
done < <(tail -n +2 "${copy_session}")
new_analytics_file_prefix=${working_dir}/${project_ID}'_SESSIONS_RESULTS_METRICS'
time_now=$(date -dnow +%Y%m%d%H%M%S)
new_analytics_file=${new_analytics_file_prefix}_${time_now}.csv
##############################EDITING################################
#remove_space_in_col_name_arguments=('remove_space_in_col_name' ${csvfilename} ${csvfilename})
#outputfiles_present=$(python3 system_analysis.py "${remove_space_in_col_name_arguments[@]}")
call_edit_session_analytics_file_arguments=('rename_columns' ${csvfilename} ${new_analytics_file} FileName_slice  FILENAME_NIFTI)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")


call_edit_session_analytics_file_arguments=('remove_columns' ${new_analytics_file} ${new_analytics_file} 'NON INFARCT DENSITY' NUMBER_NIFTIFILES	AXIAL_SCAN_NUM	THIN_SCAN_NUM	NUMBER_SELECTEDSCANS	INFARCT_FILE_NUM	CSF_FILE_NUM	PDF_FILE_NUM	CSV_FILE_NUM
 "INFARCT_MASK_FILE_PATH" "CSF_MASK_FILE_PATH" "ID" "xsiType" "PDF_FILE_SIZE"  "CSV_FILE_PATH" 'INFARCT REFLECTION VOLUME' 'INFARCT THRESH RANGE' 'NORMAL THRESH RANGE')
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")

columnname='subject_id'
new_position=0
call_edit_session_analytics_file_arguments=('call_move_one_column' ${new_analytics_file} ${columnname} ${new_position}  ${new_analytics_file})
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")

columnname='FILENAME_NIFTI'
new_position=2
call_edit_session_analytics_file_arguments=('call_move_one_column' ${new_analytics_file} ${columnname} ${new_position}  ${new_analytics_file})
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
columnname='acquisition_datetime'
new_position=2
call_edit_session_analytics_file_arguments=('call_move_one_column' ${new_analytics_file} ${columnname} ${new_position}  ${new_analytics_file})
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")

columnname='acquisition_site'
new_position=3
call_edit_session_analytics_file_arguments=('call_move_one_column' ${new_analytics_file} ${columnname} ${new_position}  ${new_analytics_file})
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
columnname='SCAN_SELECTED'
new_position=2
call_edit_session_analytics_file_arguments=('call_move_one_column' ${new_analytics_file} ${columnname} ${new_position}  ${new_analytics_file})
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")

call_edit_session_analytics_file_arguments=('sort_data_first_col_date' ${new_analytics_file} ${new_analytics_file} 'acquisition_datetime' 'subject_id' )
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")

call_edit_session_analytics_file_arguments=('remove_columns' ${new_analytics_file} ${new_analytics_file} acquisition_datetime_1)
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")

resource_dirname_at_snipr=${project_ID}'_RESULTS_CSV'
#copysinglefile_to_sniprproject ${project_ID} "$(dirname ${csvfilename})" ${resource_dirname_at_snipr} $(basename ${csvfilename})

#resource_dirname_at_snipr=${project_ID}'_RESULTS_CSV'
#copysinglefile_to_sniprproject ${project_ID} "$(dirname ${new_analytics_file})" ${resource_dirname_at_snipr} $(basename ${new_analytics_file})
#csvfile_list="${working_dir}/CSV_FILENAMES_LIST.csv"
#echo "CSV_FILENAMES" > ${csvfile_list}
#combined_metrics_results="${working_dir}/COMBINED_SESSIONS_${project_ID}_METRICS_${time_now}.csv"
#for eachfilename in ${dir_to_save}/*.csv ; do
#echo ${copy_session}::${eachfilename}::"Slice"::${combined_metrics_results}
##session_analytics_csv_inputfile=args.stuff[1]
##current_scan_result_csvfile=args.stuff[2]
##total_column_name=args.stuff[3]
##session_analytics_csv_outputfile=args.stuff[4]
##append_results_to_analytics_arguments=('append_results_to_analytics' ${copy_session} ${eachfilename}  "Slice" ${combined_metrics_results})
##outputfiles_present=$(python3 system_analysis.py "${append_results_to_analytics_arguments[@]}")
##resource_dirname_at_snipr=${project_ID}'_RESULTS_CSV'
##copysinglefile_to_sniprproject  ${project_ID}  "${working_dir}"  ${resource_dirname_at_snipr}  $(basename ${combined_metrics_results})
##echo $eachfilename >> ${csvfile_list} ;
#done

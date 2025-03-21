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

sessions_list=${working_dir}/'sessions.csv'
time_now=$(date -dnow +%Y%m%d%H%M%S)
copy_session=${sessions_list%.csv}_${project_ID}_ANALYTICS_STEP1_${time_now}.csv

curl -u $XNAT_USER:$XNAT_PASS -X GET $XNAT_HOST/data/projects/${project_ID}/experiments/?format=csv >${sessions_list}

filter_ctsession_arguments=('filter_ctsession' ${sessions_list} ${sessions_list})
outputfiles_present=$(python3 fillmaster_session_list.py "${filter_ctsession_arguments[@]}")
cp ${sessions_list} ${copy_session}
counter=0
subject_list=${working_dir}/'subjects.csv'
curl -u $XNAT_USER:$XNAT_PASS -X GET $XNAT_HOST/data/projects/${project_ID}/subjects/?format=csv >${subject_list}
csvfilename=${copy_session}
while IFS=',' read -ra array; do
#  if [ ${array[0]} == 'SNIPR02_E03847' ] ; then # | [ ${array[0]} == 'SNIPR02_E03842' ] ; then
  this_session_id=SNIPR02_E02101 #${array[0]}
  xml_filename=${working_dir}/${this_session_id}.xml
  filename_xml=$(basename ${xml_filename})   #args.stuff[2]
  dir_to_save_xml=$(dirname ${xml_filename}) #args args.stuff[3]
  download_an_xmlfile_with_URIString_arguments=('download_an_xmlfile_with_URIString' ${this_session_id} ${filename_xml} ${dir_to_save_xml})
  outputfiles_present=$(python3 download_with_session_ID.py "${download_an_xmlfile_with_URIString_arguments[@]}")
  session_id=${this_session_id}
  xmlfile=${xml_filename}
  subj_listfile=${subject_list}
  append_sessionxmlinfo_to_analytics_arguments=('append_sessionxmlinfo_to_analytics' ${session_id} ${xmlfile} ${csvfilename} ${subj_listfile})
  outputfiles_present=$(python3 fillmaster_session_list.py "${append_sessionxmlinfo_to_analytics_arguments[@]}")

  add_axial_thin_num_arguments=('add_axial_thin_num' ${session_id} ${csvfilename} ${csvfilename})
  echo 'add_axial_thin_num'::${session_id}::${csvfilename}::${csvfilename}
  outputfiles_present=$(python3 fillmaster_session_list.py "${add_axial_thin_num_arguments[@]}")
  counter=$((counter + 1))
#    if [ $counter -gt 1 ]; then
#      break
#    fi
  break
#  fi
done < <(tail -n +2 "${copy_session}")
csvfilename_before_sorting=${sessions_list%.csv}_${project_ID}_BEFORE_SORTING_STEP1_${time_now}.csv
cp ${csvfilename} ${csvfilename_before_sorting}
#create_subject_id_arguments=('create_subject_id_from_snipr' ${subject_list} ${csvfilename} ${csvfilename})
#outputfiles_present=$(python3 fillmaster_session_list.py "${create_subject_id_arguments[@]}")
new_analytics_file=${csvfilename}
call_edit_session_analytics_file_arguments=('sort_data_first_col_date' ${new_analytics_file} ${new_analytics_file}  'subject_id' 'acquisition_datetime_xml' )
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
columnname='subject_id'
new_position=0
call_edit_session_analytics_file_arguments=('call_move_one_column' ${new_analytics_file} ${columnname} ${new_position} ${new_analytics_file})
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
columnname='label'
new_position=1
call_edit_session_analytics_file_arguments=('call_move_one_column' ${new_analytics_file} ${columnname} ${new_position} ${new_analytics_file})
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")

columnname='acquisition_datetime_xml'
new_position=2
call_edit_session_analytics_file_arguments=('call_move_one_column' ${new_analytics_file} ${columnname} ${new_position} ${new_analytics_file})
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")

columnname='acquisition_site_xml'
new_position=3
call_edit_session_analytics_file_arguments=('call_move_one_column' ${new_analytics_file} ${columnname} ${new_position} ${new_analytics_file})
outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
resource_dirname_at_snipr=${project_ID}"_SESSION_ANALYTICS_1"

copysinglefile_to_sniprproject ${project_ID} "$(dirname ${new_analytics_file})" ${resource_dirname_at_snipr} $(basename ${new_analytics_file})
copysinglefile_to_sniprproject ${project_ID} "$(dirname ${csvfilename_before_sorting})" ${resource_dirname_at_snipr} $(basename ${csvfilename_before_sorting})

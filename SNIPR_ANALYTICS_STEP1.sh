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
cp ${sessions_list} ${copy_session}
counter=0
subject_list=${working_dir}/'subjects.csv'
curl -u $XNAT_USER:$XNAT_PASS -X GET $XNAT_HOST/data/projects/${project_ID}/subjects/?format=csv >${subject_list}
csvfilename=${copy_session}
while IFS=',' read -ra array; do
  this_session_id=${array[0]}
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
  outputfiles_present=$(python3 fillmaster_session_list.py "${add_axial_thin_num_arguments[@]}")
  counter=$((counter+1))
  if [ $counter -gt 2 ]; then
    break
  fi
done < <(tail -n +2 "${copy_session}")
#create_subject_id_arguments=('create_subject_id_from_snipr' ${subject_list} ${csvfilename} ${csvfilename})
#outputfiles_present=$(python3 fillmaster_session_list.py "${create_subject_id_arguments[@]}")
resource_dirname_at_snipr=${project_ID}"_SESSION_ANALYTICS_1"
copysinglefile_to_sniprproject ${project_ID} "$(dirname ${copy_session})" ${resource_dirname_at_snipr} $(basename ${copy_session})

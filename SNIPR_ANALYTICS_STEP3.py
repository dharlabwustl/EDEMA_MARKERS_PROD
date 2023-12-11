#!/usr/bin/python3
import subprocess,os,sys,glob,datetime
import pandas as pd
# sys.path.append('/software')
from fillmaster_session_list import *
from download_with_session_ID import *
from system_analysis import *
command='export XNAT_USER='+sys.argv[2] #${2}
subprocess.call(command,shell=True)
command='export XNAT_PASS='+sys.argv[3] #${3}
subprocess.call(command,shell=True)
command='export XNAT_HOST='+sys.argv[4] #${3}
subprocess.call(command,shell=True)
project_ID=sys.argv[1] #${1}
working_dir="/workinginput"
output_directory="/workingoutput"

final_output_directory="/outputinsidedocker"
####################
# call_get_resourcefiles_metadata_saveascsv() {
#   URI=${1}
#   resource_dir=${2}
#   dir_to_receive_the_data=${3}
#   output_csvfile=${4}
#   python3 -c "
# import sys
# sys.path.append('/software');
# from download_with_session_ID import *;
# call_get_resourcefiles_metadata_saveascsv()" ${URI} ${resource_dir} ${dir_to_receive_the_data} ${output_csvfile}
# }
# copysinglefile_to_sniprproject() {
#   local projectID=$1
#   #scanID=$2
#   local resource_dirname=$3 #"MASKS" #sys.argv[4]
#   local file_name=$4
#   local output_dir=$2
#   echo " I AM IN copysinglefile_to_sniprproject "
#   python3 -c "
# import sys
# sys.path.append('/software');
# from download_with_session_ID import *;
# uploadsinglefile_projectlevel()" ${projectID} ${output_dir} ${resource_dirname} ${file_name} # ${infarctfile_present}  ##$static_template_image $new_image $backslicenumber #$single_slice_filename
#
# }
# ## for each session
# function call_get_resourcefiles_metadata_saveascsv_args() {
#   local resource_dir=${2}   #"NIFTI"
#   local output_csvfile=${4} #{array[1]}
#
#   local URI=${1} #{array[0]}
#   local file_ext=${5}
#   local output_csvfile=${output_csvfile%.*}${resource_dir}.csv
#
#   local final_output_directory=${3}
#   local call_download_files_in_a_resource_in_a_session_arguments=('call_get_resourcefiles_metadata_saveascsv_args' ${URI} ${resource_dir} ${final_output_directory} ${output_csvfile})
#   outputfiles_present=$(python3 download_with_session_ID.py "${call_download_files_in_a_resource_in_a_session_arguments[@]}")
#
# }
# download_a_single_file() {
#   local file_path_csv=${1}
#   local dir_to_save=${2} #args.stuff[3]
#   local projectid=${3}
#   local output_filename=${4}
#
#   while IFS=',' read -ra array; do
#     echo array::${array[0]}
#
#     local get_latest_filepath_from_metadata_arguments=('download_a_singlefile_with_URIString' ${array[0]} ${output_filename} ${dir_to_save})
#     local outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
#   done < <(tail -n +2 "${file_path_csv}")
#
# }
def download_a_single_file(file_path_csv,dir_to_save,projectid,output_filename): # {
  file_path_csv_df=pd.read_csv(file_path_csv)
  for row_id,row in file_path_csv_df.iterrows():
    filename=row['FILE_PATH']
    get_latest_filepath_from_metadata_arguments=arguments()
    get_latest_filepath_from_metadata_arguments.stuff=['download_a_singlefile_with_URIString',filename,output_filename,dir_to_save]
    download_a_singlefile_with_URIString(get_latest_filepath_from_metadata_arguments) #outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")

URI="/data/projects/"+project_ID
dir_to_receive_the_data=working_dir
resource_dir=project_ID+"_SESSION_ANALYTICS_2"
file_path_csv=os.path.join(dir_to_receive_the_data,project_ID+"_"+resource_dir+"_resultfilepath.csv")
get_latest_filepath_from_metadata_arguments=arguments()
get_latest_filepath_from_metadata_arguments.stuff=['get_latest_filepath_from_metadata_for_analytics',URI,resource_dir,".csv", "sessions_"+project_ID+"_ANALYTICS_STEP2_", file_path_csv]
get_latest_filepath_from_metadata_for_analytics(get_latest_filepath_from_metadata_arguments)
sessions_list=os.path.join(working_dir,'sessions.csv')
time_now=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
copy_session=sessions_list.split('.csv')[0]+project_ID+'_ANALYTICS_STEP3_'+time_now+'.csv'
download_a_single_file(file_path_csv,dir_to_receive_the_data,project_ID,copy_session)
copy_session_df=pd.read_csv(copy_session)
counter=0
dir_to_save=output_directory
for row_id,row in copy_session_df.iterrows():
# while IFS=',' read -ra array; do
#   echo array::${array[22]}
  pdf_file_location=row['PDF_FILE_PATH'] #${array[22]}
  csv_file_location=row['CSV_FILE_PATH'] #${array[23]}
  this_session_id=row['ID'] #${array[1]}
  n_pdffilename_length=len(pdf_file_location) #${#pdf_file_location}
#   echo ${n_pdffilename_length}
  n_csvfilename_length=len(csv_file_location) #${#csv_file_location}
#   echo ${n_csvfilename_length}
  if n_csvfilename_length > 1 : #]; then
    csv_output_filename=os.path.basename(csv_file_location) #$(basename ${csv_file_location})
    get_latest_filepath_from_metadata_arguments=arguments()
    get_latest_filepath_from_metadata_arguments.stuff=['download_a_singlefile_with_URIString',csv_file_location,csv_output_filename,dir_to_save]
    download_a_singlefile_with_URIString(get_latest_filepath_from_metadata_arguments)
    # outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
    append_results_to_analytics_arguments=arguments()
    append_results_to_analytics_arguments.stuff=['append_results_to_analytics',copy_session,os.path.join(dir_to_save,csv_output_filename), this_session_id, copy_session]
    append_results_to_analytics(append_results_to_analytics_arguments)
    # outputfiles_present=$(python3 fillmaster_session_list.py "${append_results_to_analytics_arguments[@]}")
    counter=counter+1

    if counter > 10 : #; then
     break

# done < <(tail -n +2 "${copy_session}")
#
# new_analytics_file_prefix=${working_dir}/${project_ID}'_SESSIONS_RESULTS_METRICS'
# time_now=$(date -dnow +%Y%m%d%H%M%S)
# new_analytics_file=${new_analytics_file_prefix}_${time_now}.csv
# cp ${copy_session} ${new_analytics_file}
# ##############################EDITING################################
# call_edit_session_analytics_file_arguments=('call_edit_session_analytics_file' ${new_analytics_file})
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
#
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} FileName_slice FILENAME_NIFTI)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
#
# call_edit_session_analytics_file_arguments=('remove_columns' ${new_analytics_file} ${new_analytics_file}  xsiType 'INFARCT THRESH RANGE' 'NORMAL THRESH RANGE' 'INFARCT REFLECTION VOLUME' 'NON INFARCT DENSITY' NUMBER_NIFTIFILES NUMBER_SELECTEDSCANS INFARCT_FILE_NUM CSF_FILE_NUM CSV_FILE_NUM
#   "INFARCT_MASK_FILE_PATH" "CSF_MASK_FILE_PATH" "ID" "xsiType" "PDF_FILE_SIZE" "CSV_FILE_PATH" 'xnat:subjectassessordata/id')
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
#     if [ ${project_ID} == "ICH" ]; then
# call_edit_session_analytics_file_arguments=('remove_columns' ${new_analytics_file} ${new_analytics_file} xsiType 'INFARCT THRESH RANGE' 'NORMAL THRESH RANGE' 'INFARCT REFLECTION VOLUME' 'NON INFARCT DENSITY' NUMBER_NIFTIFILES NUMBER_SELECTEDSCANS INFARCT_FILE_NUM CSF_FILE_NUM CSV_FILE_NUM
#   "INFARCT_MASK_FILE_PATH" "CSF_MASK_FILE_PATH" "ID" "xsiType" "PDF_FILE_SIZE" "CSV_FILE_PATH" CSV_FILE_PATH	CSF_MASK	ICH_EDEMA_MASK	ICH_MASK  )
#     fi
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# #columnname='subject_id'
# #new_position=0
# #call_edit_session_analytics_file_arguments=('call_move_one_column' ${new_analytics_file} ${columnname} ${new_position} ${new_analytics_file})
# #outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
#
# columnname='FILENAME_NIFTI'
# new_position=5
# call_edit_session_analytics_file_arguments=('call_move_one_column' ${new_analytics_file} ${columnname} ${new_position} ${new_analytics_file})
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# #columnname='acquisition_datetime'
# #new_position=2
# #call_edit_session_analytics_file_arguments=('call_move_one_column' ${new_analytics_file} ${columnname} ${new_position} ${new_analytics_file})
# #outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# #
# #columnname='acquisition_site'
# #new_position=3
# #call_edit_session_analytics_file_arguments=('call_move_one_column' ${new_analytics_file} ${columnname} ${new_position} ${new_analytics_file})
# #outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# columnname='SCAN_SELECTED'
# new_position=4
# call_edit_session_analytics_file_arguments=('call_move_one_column' ${new_analytics_file} ${columnname} ${new_position} ${new_analytics_file})
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
#
# #call_edit_session_analytics_file_arguments=('sort_data_first_col_date' ${new_analytics_file} ${new_analytics_file} 'acquisition_datetime' 'subject_id')
# #outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# #csvfilename=${new_analytics_file}
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} subject_id subject)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} label snipr_session)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} SCAN_SELECTED scan_selected)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} acquisition_datetime scan_date_time)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} FILENAME_NIFTI scan_name)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} SLICE_NUM slices)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} res_x px)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# call_edit_session_analytics_file_arguments=('remove_columns' ${new_analytics_file} ${new_analytics_file} res_y)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} slice_thickness pz)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} scanner scanner_name)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} body_part body_site)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} SCAN_DESCRIPTION scan_kernel)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} 'LEFT CSF VOLUME' csf_left)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} 'RIGHT CSF VOLUME' csf_right)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} 'TOTAL CSF VOLUME' csf_total)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} 'INFARCT SIDE' stroke_side)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} 'NWU' nwu)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} 'INFARCT VOLUME' infarct_volume)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} 'BET VOLUME' cranial)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} 'CSF RATIO' csf_ratio)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} 'LEFT BRAIN VOLUME without CSF' brain_left)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} 'RIGHT BRAIN VOLUME without CSF' brain_right)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} 'NIFTIFILES_PREFIX' scan_stem)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
#
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} 'PDF_FILE_NUM' pdf_created)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} 'AXIAL_SCAN_NUM' axial_number)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# call_edit_session_analytics_file_arguments=('rename_columns' ${new_analytics_file} ${new_analytics_file} 'THIN_SCAN_NUM' axial_thin_number)
# outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# #create_subject_id_arguments=('create_subject_id' ${csvfilename} ${csvfilename})
# #outputfiles_present=$(python3 fillmaster_session_list.py "${create_subject_id_arguments[@]}")
# resource_dirname_at_snipr=${project_ID}"_SESSION_ANALYTICS_3"
# copysinglefile_to_sniprproject ${project_ID} "$(dirname ${new_analytics_file})" ${resource_dirname_at_snipr} $(basename ${new_analytics_file})
# #outputfiles_present=$(python3 fillmaster_session_list.py "${call_edit_session_analytics_file_arguments[@]}")
# copysinglefile_to_sniprproject ${project_ID} "$(dirname ${copy_session})" ${resource_dirname_at_snipr} $(basename ${copy_session})

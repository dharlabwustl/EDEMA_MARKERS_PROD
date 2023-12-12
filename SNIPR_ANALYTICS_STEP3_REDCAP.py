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
command='export XNAT_HOST='+str(sys.argv[4]).split('::::')[0] #${3}
subprocess.call(command,shell=True)
project_ID=sys.argv[1] #${1}
working_dir="/workinginput"
output_directory="/workingoutput"

final_output_directory="/outputinsidedocker"

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
  print(row['label'])
  print(pdf_file_location)
  n_pdffilename_length=len(str(pdf_file_location)) #${#pdf_file_location}
#   echo ${n_pdffilename_length}

  n_csvfilename_length=len(str(csv_file_location)) #${#csv_file_location}
#   echo ${n_csvfilename_length}
  if ".csv" in str(csv_file_location) : #]; then
    csv_output_filename=os.path.basename(csv_file_location) #$(basename ${csv_file_location})
    get_latest_filepath_from_metadata_arguments=arguments()
    get_latest_filepath_from_metadata_arguments.stuff=['download_a_singlefile_with_URIString',csv_file_location,csv_output_filename,dir_to_save]
    download_a_singlefile_with_URIString(get_latest_filepath_from_metadata_arguments)
    
    append_results_to_analytics_arguments=arguments()
    append_results_to_analytics_arguments.stuff=['append_results_to_analytics',copy_session,os.path.join(dir_to_save,csv_output_filename), this_session_id, copy_session]
    append_results_to_analytics(append_results_to_analytics_arguments)
    
    counter=counter+1

    if counter > 2 : #; then
     break


#
new_analytics_file_prefix=os.path.join(working_dir,project_ID+'_SESSIONS_RESULTS_METRICS')
time_now=datetime.datetime.now().strftime('%Y%m%d%H%M%S') 
new_analytics_file=new_analytics_file_prefix+'_'+time_now+'.csv'
command="cp " + copy_session + " " + new_analytics_file
subprocess.call(command,shell=True)

# ##############################EDITING################################
call_edit_session_analytics_file_arguments=arguments()
call_edit_session_analytics_file_arguments.stuff=['call_edit_session_analytics_file' ,new_analytics_file]
call_edit_session_analytics_file(call_edit_session_analytics_file_arguments)
# #
# #
# call_edit_session_analytics_file_arguments=arguments()
call_edit_session_analytics_file_arguments.stuff=['rename_columns' ,new_analytics_file,new_analytics_file ,'FileName_slice', 'FILENAME_NIFTI']
rename_columns(call_edit_session_analytics_file_arguments) #
# #
# call_edit_session_analytics_file_arguments=arguments()
call_edit_session_analytics_file_arguments.stuff=['remove_columns' ,new_analytics_file,new_analytics_file,  'xsiType', 'INFARCT THRESH RANGE', 'NORMAL THRESH RANGE', 'INFARCT REFLECTION VOLUME', 'NON INFARCT DENSITY', 'NUMBER_NIFTIFILES', 'NUMBER_SELECTEDSCANS' ,'INFARCT_FILE_NUM', 'CSF_FILE_NUM', 'CSV_FILE_NUM',   "INFARCT_MASK_FILE_PATH", "CSF_MASK_FILE_PATH", "ID" ,"xsiType", "PDF_FILE_SIZE", "CSV_FILE_PATH", 'xnat:subjectassessordata/id']

#
if "ICH" in project_ID:
  # call_edit_session_analytics_file_arguments=arguments()
  call_edit_session_analytics_file_arguments.stuff=['remove_columns',new_analytics_file,new_analytics_file, "xsiType", 'INFARCT THRESH RANGE', 'NORMAL THRESH RANGE', 'INFARCT REFLECTION VOLUME', 'NON INFARCT DENSITY', "NUMBER_NIFTIFILES", "NUMBER_SELECTEDSCANS" ,"INFARCT_FILE_NUM", "CSF_FILE_NUM", "CSV_FILE_NUM","INFARCT_MASK_FILE_PATH", "CSF_MASK_FILE_PATH", "ID", "xsiType", "PDF_FILE_SIZE", "CSV_FILE_PATH", "CSV_FILE_PATH",	"CSF_MASK",	"ICH_EDEMA_MASK",	"ICH_MASK"] #  )
remove_columns(call_edit_session_analytics_file_arguments)

columnname='FILENAME_NIFTI'
new_position=5
call_edit_session_analytics_file_arguments=arguments()
call_edit_session_analytics_file_arguments.stuff=['call_move_one_column', new_analytics_file,columnname,new_position,new_analytics_file]
call_move_one_column(call_edit_session_analytics_file_arguments)


columnname='SCAN_SELECTED'
new_position=4
# call_edit_session_analytics_file_arguments=arguments()
call_edit_session_analytics_file_arguments.stuff=['call_move_one_column',new_analytics_file,columnname,new_position,new_analytics_file]
call_move_one_column(call_edit_session_analytics_file_arguments)
#


call_edit_session_analytics_file_arguments.stuff=['rename_columns', new_analytics_file,new_analytics_file, 'subject_id' ,'subject']
rename_columns(call_edit_session_analytics_file_arguments)
#
call_edit_session_analytics_file_arguments.stuff=['rename_columns', new_analytics_file,new_analytics_file, "label", "snipr_session"]
rename_columns(call_edit_session_analytics_file_arguments)
#
call_edit_session_analytics_file_arguments.stuff=['rename_columns', new_analytics_file,new_analytics_file, "SCAN_SELECTED", "scan_selected"]
rename_columns(call_edit_session_analytics_file_arguments)
#
call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file,"acquisition_datetime", "scan_date_time"]
rename_columns(call_edit_session_analytics_file_arguments)
#
call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file,"FILENAME_NIFTI", "scan_name"]
rename_columns(call_edit_session_analytics_file_arguments)
#
call_edit_session_analytics_file_arguments.stuff=['rename_columns', new_analytics_file,new_analytics_file,"SLICE_NUM", "slices"]
rename_columns(call_edit_session_analytics_file_arguments)
#
call_edit_session_analytics_file_arguments.stuff=['rename_columns', new_analytics_file,new_analytics_file,"res_x", "px"]
rename_columns(call_edit_session_analytics_file_arguments)
#
call_edit_session_analytics_file_arguments.stuff=['remove_columns' , new_analytics_file,new_analytics_file, "res_y"]
remove_columns(call_edit_session_analytics_file_arguments)
#
call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file,"slice_thickness", "pz"]
rename_columns(call_edit_session_analytics_file_arguments)
#
call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file,"scanner", "scanner_name"]
rename_columns(call_edit_session_analytics_file_arguments)
#
call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, "body_part", "body_site"]
rename_columns(call_edit_session_analytics_file_arguments)
#
call_edit_session_analytics_file_arguments.stuff=['rename_columns', new_analytics_file,new_analytics_file, "SCAN_DESCRIPTION", "scan_kernel"]
rename_columns(call_edit_session_analytics_file_arguments)
#
call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file,'LEFT CSF VOLUME', "csf_left"]
rename_columns(call_edit_session_analytics_file_arguments)

call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'RIGHT CSF VOLUME', "csf_right"]
rename_columns(call_edit_session_analytics_file_arguments)

call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'TOTAL CSF VOLUME' ,"csf_total"]
rename_columns(call_edit_session_analytics_file_arguments)

call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'INFARCT SIDE', "stroke_side"]
rename_columns(call_edit_session_analytics_file_arguments)

call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'NWU' ,"nwu"]
rename_columns(call_edit_session_analytics_file_arguments)

call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'INFARCT VOLUME', "infarct_volume"]
rename_columns(call_edit_session_analytics_file_arguments)

call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'BET VOLUME', "cranial"]
rename_columns(call_edit_session_analytics_file_arguments)

call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'CSF RATIO', "csf_ratio"]
rename_columns(call_edit_session_analytics_file_arguments)

call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'LEFT BRAIN VOLUME without CSF', "brain_left"]
rename_columns(call_edit_session_analytics_file_arguments)

call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'RIGHT BRAIN VOLUME without CSF' ,"brain_right"]
rename_columns(call_edit_session_analytics_file_arguments)

call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'NIFTIFILES_PREFIX', "scan_stem"]
rename_columns(call_edit_session_analytics_file_arguments)


call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'PDF_FILE_NUM', "pdf_created"]
rename_columns(call_edit_session_analytics_file_arguments)

call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'AXIAL_SCAN_NUM', "axial_number"]
rename_columns(call_edit_session_analytics_file_arguments)

call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'THIN_SCAN_NUM' ,"axial_thin_number"]
rename_columns(call_edit_session_analytics_file_arguments)

# resource_dirname_at_snipr=project_ID+"_SESSION_ANALYTICS_3"

# uploadsinglefile_projectlevel_args_arguments=arguments()
# uploadsinglefile_projectlevel_args_arguments.stuff=['uploadsinglefile_projectlevel_args',project_ID,os.path.dirname(new_analytics_file),resource_dirname_at_snipr, os.path.basename(new_analytics_file)]
# uploadsinglefile_projectlevel_args(uploadsinglefile_projectlevel_args_arguments)
# uploadsinglefile_projectlevel_args_arguments.stuff=['uploadsinglefile_projectlevel_args',project_ID,os.path.dirname(copy_session),resource_dirname_at_snipr, os.path.basename(copy_session)]
# uploadsinglefile_projectlevel_args(uploadsinglefile_projectlevel_args_arguments)

api_token=str(sys.argv[4]).split('::::')[1] #sys.argv[5] #os.environ['REDCAP_API_TOKEN']
api_url=str(sys.argv[4]).split('::::')[2] #sys.argv[6] #'https://redcap.wustl.edu/redcap/api/'
field_id='subject'
field_value='OURTHIRDSUBJECT'
record = {
  # 'redcap_repeat_instrument':str(df_scan_sample.loc[0,'redcap_repeat_instrument']),
  # 'redcap_repeat_instance':str(df_scan_sample.loc[0,'redcap_repeat_instance']),
  'record_id':10, # str(df_scan_sample.loc[0,'record_id']),
  field_id: field_value

}
data = json.dumps([record])
fields = {
  'token': api_token,
  'content': 'record',
  'format': 'json',
  'type': 'flat',
  'data': data,
}
r = requests.post(api_url,data=fields)
print('HTTP Status: ' + str(r.status_code))
print(r.text)
# file =glob.glob('/home/atul/Downloads/*.pdf')[0] # '/home/atul/Downloads/COLI_HM25_CT_1_COLI_HM25_03092021_1954_2_thresh_0_40_VersionDate-11302022_01_07_2023.pdf'
# fields = {
#   'token': api_token,
#   'content': 'file',
#   'action': 'import',
#   # 'repeat_instrument':str(df_scan_sample.loc[0,'redcap_repeat_instrument']),
#   # 'repeat_instance':str(df_scan_sample.loc[0,'redcap_repeat_instance']),
#   'record': str(df_scan_sample.loc[0,'record_id']),
#   'field': 'session_pdf' , #'photo_as_pdf',
#   'returnFormat': 'json'
# }
#
# file_path=file
# file_obj = open(file_path, 'rb')
# r = requests.post(api_url,data=fields,files={'file':file_obj})
# file_obj.close()
#
# print('HTTP Status: ' + str(r.status_code))
# print(r.text)
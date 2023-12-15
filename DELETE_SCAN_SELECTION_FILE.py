#!/usr/bin/python
# tininfo@proteantech.in
import subprocess,os,sys,glob,datetime
import pandas as pd
# sys.path.append('/software')
from fillmaster_session_list import *
from download_with_session_ID import *
from system_analysis import *

command='export XNAT_USER='+sys.argv[2] #${2}'
subprocess.call(command,shell=True)
command='export XNAT_PASS='+sys.argv[3] #${3}
subprocess.call(command,shell=True)
# export XNAT_HOST=${4}
command='export XNAT_HOST='+sys.argv[4] #${4}
subprocess.call(command,shell=True)
project_ID=sys.argv[1] #${1}
working_dir="/workinginput"
output_directory="/workingoutput"

final_output_directory="/outputinsidedocker"

sessions_list=working_dir +'/'+'sessions.csv'
time_now=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
# $(date -dnow +%Y%m%d%H%M%S)
print(project_ID+"_"+time_now)
copy_session=sessions_list #sessions_list.split('.csv')[0]+'_'+ project_ID+ '_SESSIONS_'+time_now+'.csv'
get_metadata_project_sessionlist(project_ID,sessions_list)
#
# def download_a_single_file(file_path_csv,dir_to_save,projectid,output_filename): # {
#     file_path_csv_df=pd.read_csv(file_path_csv)
#     for row_id,row in file_path_csv_df.iterrows():
#         filename=row['FILE_PATH']
#         get_latest_filepath_from_metadata_arguments=arguments()
#         get_latest_filepath_from_metadata_arguments.stuff=['download_a_singlefile_with_URIString',filename,output_filename,dir_to_save]
#         download_a_singlefile_with_URIString(get_latest_filepath_from_metadata_arguments) #outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
#
# URI="/data/projects/"+project_ID #${project_ID}
# dir_to_receive_the_data=working_dir #${working_dir}
# resource_dir=project_ID+"_SESSION_ANALYTICS_1" #${project_ID}_SESSION_ANALYTICS_1"
# file_path_csv=os.path.join(dir_to_receive_the_data,project_ID+"_"+resource_dir+"_resultfilepath.csv") #${dir_to_receive_the_data}/${project_ID}"_${resource_dir}_resultfilepath.csv"
# get_latest_filepath_from_metadata_arguments=arguments()
# get_latest_filepath_from_metadata_arguments.stuff=['get_latest_filepath_from_metadata_for_analytics',URI,resource_dir,".csv", "sessions_"+project_ID+"_ANALYTICS_STEP1_", file_path_csv]
# get_latest_filepath_from_metadata_for_analytics(get_latest_filepath_from_metadata_arguments)
# sessions_list=os.path.join(working_dir,'sessions.csv')
# time_now=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
# copy_session=sessions_list.split('.csv')[0]+project_ID+'_ANALYTICS_STEP2_'+time_now+'.csv'
# download_a_single_file(file_path_csv,dir_to_receive_the_data,project_ID,copy_session)
# #
copy_session_df=pd.read_csv(copy_session)
counter=0
for row_id,row in copy_session_df.iterrows():
    if row['xsiType']=="xnat:ctSessionData":
        call_fill_sniprsession_list_arguments=arguments()
        URI='/data/experiments/'+row['ID']
        resource_dir='NIFTI_LOCATION'
        metadata_niftilocation=get_resourcefiles_metadata(URI,resource_dir)
        metadata_niftilocation_df = pd.read_json(json.dumps(metadata_niftilocation))
        for row_id_1,row_1 in metadata_niftilocation_df.iterrows():
            print(row['label'])
            print(row_1['URI'])
            delete_a_file_with_URIString(row_1['URI'])
        counter=counter+1

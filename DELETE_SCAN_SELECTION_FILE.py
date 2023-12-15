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

#!/usr/bin/env python
import requests,json
import pandas as pd
# from config import config
import requests, hashlib, json,glob
import os,sys,subprocess
sys.path.append("/software")
from fillmaster_session_list import *
from download_with_session_ID import *
from system_analysis import *
api_token=sys.argv[1] #os.environ['REDCAP_API_TOKEN']
api_url=sys.argv[2] #'https://redcap.wustl.edu/redcap/api/'
project_ID=sys.argv[3]
working_dir="/workinginput"
output_directory="/workingoutput"
final_output_directory="/outputinsidedocker"
fields = {
    'token':api_token, # api_token,
    'content': 'record',
    'format': 'json',
    'type': 'flat'
}
r = requests.post('https://redcap.wustl.edu/redcap/api/',data=fields)
r_json=json.dumps(r.json()) #get_niftifiles_metadata(each_axial['URI'] )) get_resourcefiles_metadata(URI,resource_dir)
df_scan = pd.read_json(r_json)
df_scan.to_csv('test.csv',index=False)
## GET the session name from session ID:
# session_label=get_session_label(session_id,outputfile="NONE.csv")
## get subject ID:

#### DOWNLOAD the result of analysis STEP1
URI="/data/projects/"+project_ID #${project_ID}
dir_to_receive_the_data=working_dir #${working_dir}
resource_dir=project_ID+"_SESSION_ANALYTICS_1" #${project_ID}_SESSION_ANALYTICS_1"
file_path_csv=os.path.join(dir_to_receive_the_data,project_ID+"_"+resource_dir+"_resultfilepath.csv")
get_latest_filepath_from_metadata_arguments=arguments()
get_latest_filepath_from_metadata_arguments.stuff=['get_latest_filepath_from_metadata_for_analytics',URI,resource_dir,".csv", "sessions_"+project_ID+"_ANALYTICS_STEP1_", file_path_csv]
get_latest_filepath_from_metadata_for_analytics(get_latest_filepath_from_metadata_arguments)

### fill each session with its projectname, subject name, instrument number, instance number

# df_scan=pd.read_csv('test.csv',index_col=False, dtype=object)
# ############FILTER TO GET THE SINGLE ROW#######################
# # df_scan_sample=df_scan[(df_scan['redcap_repeat_instance']=="2" ) & (df_scan['record_id']=='ATUL_001')].reset_index()
# df_scan_sample=df_scan[(df_scan['record_id']=="1" )].reset_index()
# #######################################################################
# field_id='subject'
# field_value='OURSECONDSUBJECT'
# print(df_scan_sample)
# record = {
#     # 'redcap_repeat_instrument':str(df_scan_sample.loc[0,'redcap_repeat_instrument']),
#     # 'redcap_repeat_instance':str(df_scan_sample.loc[0,'redcap_repeat_instance']),
#     'record_id': str(df_scan_sample.loc[0,'record_id']),
#     field_id: field_value
#
# }
# data = json.dumps([record])
# fields = {
#     'token': api_token,
#     'content': 'record',
#     'format': 'json',
#     'type': 'flat',
#     'data': data,
# }
# r = requests.post(api_url,data=fields)
# print('HTTP Status: ' + str(r.status_code))
# print(r.text)
# file =glob.glob('/home/atul/Downloads/*.pdf')[0] # '/home/atul/Downloads/COLI_HM25_CT_1_COLI_HM25_03092021_1954_2_thresh_0_40_VersionDate-11302022_01_07_2023.pdf'
# fields = {
#     'token': api_token,
#     'content': 'file',
#     'action': 'import',
#     # 'repeat_instrument':str(df_scan_sample.loc[0,'redcap_repeat_instrument']),
#     # 'repeat_instance':str(df_scan_sample.loc[0,'redcap_repeat_instance']),
#     'record': str(df_scan_sample.loc[0,'record_id']),
#     'field': 'session_pdf' , #'photo_as_pdf',
#     'returnFormat': 'json'
# }
#
# file_path=file
# file_obj = open(file_path, 'rb')
# r = requests.post(api_url,data=fields,files={'file':file_obj})
# file_obj.close()
#
# print('HTTP Status: ' + str(r.status_code))
# print(r.text)
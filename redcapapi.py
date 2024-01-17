#!/usr/bin/env python
import requests,json
import pandas as pd
# from config import config
import requests, hashlib, json,glob
import os,sys,subprocess,time
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

def fill_subjects_records(copy_session,counter_ul=99999999):
    copy_session_df=pd.read_csv(copy_session)
    counter=0
    for each_row_id,each_row in copy_session_df.iterrows():
        if  str(each_row['subject_id']) not in record_ids_done or str(each_row['subject_id'])  in record_ids_done:
            print('I AM NOT IN THE RECORD_ID_LIST')
            this_record_id=str(each_row['subject_id'])
            this_subject=str(each_row['subject_id'])
            this_redcap_repeat_instance=str(1)
            this_redcap_repeat_instrument='stroke_details'
            this_snipr_session=str(each_row['label'])
            record = {
                'redcap_repeat_instrument':this_redcap_repeat_instrument,
                'redcap_repeat_instance':this_redcap_repeat_instance,
                'record_id':this_record_id,
                'project':project_ID,
                'subject':this_subject,
                'subject_number':this_subject.split('_')[1],
                'site':project_ID+'_1'
            }
            print(record)
            # break
            data = json.dumps([record])
            fields = {
                'token': api_token,
                'content': 'record',
                'format': 'json',
                'type': 'flat',
                'data': data,
            }
            try:
                r = requests.post(api_url,data=fields)
                print('HTTP Status: ' + str(r.status_code))
                print(r.text)
                record_ids_done.append(this_record_id)
                counter=counter+1
            except:
                pass
            if counter>counter_ul:
                break

def delete_record(record_id):
    data = {
        'token':api_token,
        'action': 'delete',
        'content': 'record',
        'records[0]': str(record_id),
        'returnFormat': 'json'
    }
    r = requests.post('https://redcap.wustl.edu/redcap/api/',data=data)
    print('HTTP Status: ' + str(r.status_code))
    print(r.text)
def download_latest_redcapfile(project_ID,api_token,this_project_redcapfile):
    df_scan=''
    try:
        fields = {
            'token':api_token, # api_token,
            'content': 'record',
            'format': 'json',
            'type': 'flat'
        }
        r = requests.post('https://redcap.wustl.edu/redcap/api/',data=fields)
        r_json=json.dumps(r.json()) #get_niftifiles_metadata(each_axial['URI'] )) get_resourcefiles_metadata(URI,resource_dir)
        df_scan = pd.read_json(r_json)
        df_scan.to_csv(this_project_redcapfile,index=False)
    except:
        pass
    return df_scan
###################################################################################################

this_project_redcapfile=project_ID+'.csv'
df_scan=download_latest_redcapfile(project_ID,api_token,this_project_redcapfile)
#### DOWNLOAD the result of analysis STEP1
URI="/data/projects/"+project_ID #${project_ID}
dir_to_receive_the_data=working_dir #${working_dir}
resource_dir=project_ID+"_SESSION_ANALYTICS_3" #${project_ID}_SESSION_ANALYTICS_1"
file_path_csv=os.path.join(dir_to_receive_the_data,project_ID+"_"+resource_dir+"_resultfilepath.csv")
get_latest_filepath_from_metadata_arguments=arguments()
get_latest_filepath_from_metadata_arguments.stuff=['get_latest_filepath_from_metadata_for_analytics',URI,resource_dir,".csv", "sessions_"+project_ID+"_ANALYTICS_STEP3_", file_path_csv]
# print(get_latest_filepath_from_metadata_arguments.stuff)
get_latest_filepath_from_metadata_for_analytics(get_latest_filepath_from_metadata_arguments)
sessions_list=os.path.join(working_dir,'sessions.csv')
time_now=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
copy_session=sessions_list.split('.csv')[0]+project_ID+'_ANALYTICS_STEP1_'+time_now+'.csv'
download_a_single_file(file_path_csv,dir_to_receive_the_data,project_ID,copy_session)
### fill each session with its projectname, subject name, instrument number, instance number

# df_scan=pd.read_csv(this_project_redcapfile,index_col=False, dtype=object)

# ############FILTER TO GET THE SINGLE ROW#######################
# for each session
copy_session_df=pd.read_csv(copy_session)
record_ids_done=[]
counter=0
# print(type(df_scan['record_id'].tolist()))
########### DELETE OLD RECORDS#######################
##########for each_row_id,each_row in df_scan.iterrows():
##########    delete_record(each_row['record_id'])
##############FILL RECORD ID AND SUBJECT ID , project and subject number , VERY FIRST TIME ##############################
# fill_subjects_records(copy_session,counter_ul=20)
######################## FILL SESSION LABEL in IMAGING INSTRUMENT ############################################
unique_subjects=sorted(list(set(copy_session_df['subject_id'].tolist()))) #.sort()
print(unique_subjects)
this_project_redcapfile_latest=project_ID+'_latest.csv'
df_scan_latest=download_latest_redcapfile(project_ID,api_token,this_project_redcapfile_latest)
counter=0
def sorted_subj_list(subject_df,subject_col_name,datetime_col_name):
    datetime_col_name_1=datetime_col_name+"_1"
    # df=pd.read_csv(csvfilename)
    subject_df[datetime_col_name_1] = pd.to_datetime(subject_df[datetime_col_name], format='%m/%d/%Y %H:%M')
    df_agg = subject_df.groupby([subject_col_name])
    res_df = df_agg.apply(lambda x: x.sort_values(by=[datetime_col_name_1],ascending=True))
    x=res_df.pop(datetime_col_name_1)
    return res_df
def add_one_data_to_redcap(this_record_id,this_redcap_repeat_instrument,this_field,this_data):
    # this_redcap_repeat_instrument='imaging_data'
    # this_record_id=str(each_row['subject_id'])
    # this_snipr_session=str(each_row['label'])
    # df_scan_latest['record_id']
    try:
        record = {
            'redcap_repeat_instrument':this_redcap_repeat_instrument,
            'redcap_repeat_instance':this_redcap_repeat_instance,
            'record_id':this_record_id,
            this_field:this_data #this_snipr_session
        }
        print(record)
        # break
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
    except:
        pass
    return
for each_unique_subject in unique_subjects:
    subject_df=copy_session_df[copy_session_df['subject_id']==each_unique_subject]
    subject_col_name='subject_id'
    datetime_col_name='acquisition_datetime'
    subject_df=sorted_subj_list(subject_df,subject_col_name,datetime_col_name)
    # subject_df=subject_df[subject_df['axial_number']>0 | subject_df['axial_thin_number']>0]
    this_redcap_repeat_instance=1
    for each_row_id,each_row in subject_df.iterrows():
        print((each_row['subject_id']))
        print((each_row['acquisition_datetime']))
        add_one_data_to_redcap(each_row['subject_id'],'imaging_data','snipr_session',each_row['label'])
        add_one_data_to_redcap(each_row['subject_id'],'imaging_data','scan_stem',each_row['NIFTIFILES_PREFIX'])
        add_one_data_to_redcap(each_row['subject_id'],'imaging_data','scan_name',each_row['FileName_slice'])
        # add_one_data_to_redcap(each_row['subject_id'],'imaging_data','scan_date_time',each_row['acquisition_datetime'])
        add_one_data_to_redcap(each_row['subject_id'],'imaging_data','scan_kernel',each_row['SCAN_DESCRIPTION'])
        add_one_data_to_redcap(each_row['subject_id'],'imaging_data','stroke_side',each_row['ICH SIDE'][0])
        # add_one_data_to_redcap(each_row['subject_id'],'imaging_data','snipr_session',each_row['label'])
        # add_one_data_to_redcap(each_row['subject_id'],'imaging_data','snipr_session',each_row['label'])
        # add_one_data_to_redcap(each_row['subject_id'],'imaging_data','snipr_session',each_row['label'])
        # add_one_data_to_redcap(each_row['subject_id'],'imaging_data','snipr_session',each_row['label'])
        # add_one_data_to_redcap(each_row['subject_id'],'imaging_data','snipr_session',each_row['label'])
        # add_one_data_to_redcap(each_row['subject_id'],'imaging_data','snipr_session',each_row['label'])
        # add_one_data_to_redcap(each_row['subject_id'],'imaging_data','snipr_session',each_row['label'])
        # add_one_data_to_redcap(each_row['subject_id'],'imaging_data','snipr_session',each_row['label'])
        # add_one_data_to_redcap(each_row['subject_id'],'imaging_data','snipr_session',each_row['label'])
        # add_one_data_to_redcap(each_row['subject_id'],'imaging_data','snipr_session',each_row['label'])
        # add_one_data_to_redcap(each_row['subject_id'],'imaging_data','snipr_session',each_row['label'])
        # add_one_data_to_redcap(each_row['subject_id'],'imaging_data','snipr_session',each_row['label'])
        # add_one_data_to_redcap(each_row['subject_id'],'imaging_data','snipr_session',each_row['label'])
        # add_one_data_to_redcap(each_row['subject_id'],'imaging_data','snipr_session',each_row['label'])
        # add_one_data_to_redcap(each_row['subject_id'],'imaging_data','snipr_session',each_row['label'])
        # add_one_data_to_redcap(each_row['subject_id'],'imaging_data','snipr_session',each_row['label'])

        this_redcap_repeat_instance=this_redcap_repeat_instance+1
    counter=counter+1
    if counter >10:
        break
    # break
#     print('I AM NOT IN THE RECORD')
#     # break
#     if  str(each_row['subject_id']) not in record_ids_done or str(each_row['subject_id'])  in record_ids_done:
#         print('I AM NOT IN THE RECORD_ID_LIST')
#         this_record_id=str(each_row['subject_id'])
#         this_subject=str(each_row['subject_id'])
#         this_redcap_repeat_instance=str(1)
#         this_redcap_repeat_instrument='stroke_details'
#         this_snipr_session=str(each_row['label'])
#         record = {
#             'redcap_repeat_instrument':this_redcap_repeat_instrument,
#             'redcap_repeat_instance':this_redcap_repeat_instance,
#             'record_id':this_record_id,
#             'project':project_ID,
#             'subject':this_subject,
#             'subject_number':this_subject.split('_')[1]
#             # 'snipr_session':this_snipr_session
#         }
#         print(record)
#         # break
#         data = json.dumps([record])
#         fields = {
#             'token': api_token,
#             'content': 'record',
#             'format': 'json',
#             'type': 'flat',
#             'data': data,
#         }
#         r = requests.post(api_url,data=fields)
#         print('HTTP Status: ' + str(r.status_code))
#         print(r.text)
#         record_ids_done.append(this_record_id)
#         counter=counter+1
#         if counter>20:
#             break


# for each_row_id,each_row in copy_session_df.iterrows():
#     print(type(each_row['subject_id']))
#     # if str(each_row['subject_id']) not in df_scan['record_id'].tolist() :
#     this_project_redcapfile_latest=project_ID+'_latest1.csv'
#     df_scan_1=download_latest_redcapfile(project_ID,api_token,this_project_redcapfile_latest)
#     this_record_subject_df=df_scan[(df_scan['redcap_repeat_instance']=="2" ) & (df_scan['record_id']=='ATUL_001')].reset_index()
#     # # time.sleep(5)
#     # print(df_scan['record_id'].tolist())
#     # if str(each_row['subject_id']) not in df_scan_1['record_id'].tolist():
#     #     if str(each_row['subject_id']) not in df_scan_1['record_id'].tolist()
#     #     #     print('I AM NOT IN THE RECORD')
#     #     print(type(df_scan['record_id'].tolist()[0]))
#     #     print('I AM NOT IN THE RECORD')
#     #     # break
#     #     if  str(each_row['subject_id']) not in record_ids_done:
#     #         print('I AM NOT IN THE RECORD_ID_LIST')
#     #
#     #         #         # print(each_row['label']+':::::'+each_row['subject_id'])
#     #         this_record_id=str(each_row['subject_id'])
#     #         this_subject=str(each_row['subject_id'])
#     #         this_redcap_repeat_instance=str(1)
#     #         this_redcap_repeat_instrument='stroke_details'
#     #         this_snipr_session=str(each_row['label'])
#     #         record = {
#     #             'redcap_repeat_instrument':this_redcap_repeat_instrument,
#     #             'redcap_repeat_instance':this_redcap_repeat_instance,
#     #             'record_id':this_record_id,
#     #             'subject':this_subject
#     #             # 'snipr_session':this_snipr_session
#     #         }
#     #         print(record)
#     #         # break
#     #         data = json.dumps([record])
#     #         fields = {
#     #             'token': api_token,
#     #             'content': 'record',
#     #             'format': 'json',
#     #             'type': 'flat',
#     #             'data': data,
#     #         }
#     #         r = requests.post(api_url,data=fields)
#     #         print('HTTP Status: ' + str(r.status_code))
#     #         print(r.text)
#     #         record_ids_done.append(this_record_id)
#     #         counter=counter+1
#     #         if counter>10:
#     #             break

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
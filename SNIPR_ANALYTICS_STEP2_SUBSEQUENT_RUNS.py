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
get_latest_filepath_from_metadata_arguments.stuff=['get_latest_filepath_from_metadata_for_analytics',URI,resource_dir,".csv", "sessions"+project_ID+"_ANALYTICS_STEP2_", file_path_csv]
print(get_latest_filepath_from_metadata_arguments.stuff)
get_latest_filepath_from_metadata_for_analytics(get_latest_filepath_from_metadata_arguments)
sessions_list=os.path.join(working_dir,'sessions.csv')
time_now=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
copy_session=os.path.join(dir_to_receive_the_data,os.path.basename(sessions_list).split('.csv')[0]+project_ID+'_ANALYTICS_STEP2_'+time_now+'.csv')
download_a_single_file(file_path_csv,dir_to_receive_the_data,project_ID,os.path.basename(copy_session))
copy_session_df=pd.read_csv(copy_session)
counter=0
# dir_to_save=output_directory

#
copy_session_df=pd.read_csv(copy_session)
counter=0
for row_id,row in copy_session_df.iterrows():
    try:
        session_id=str(row['ID'])
        session_metadata=get_metadata_session(session_id)
        df_this_session = pd.read_json(json.dumps(session_metadata))
        df_axial=df_this_session.loc[(df_this_session['type'] == 'Z-Axial-Brain')] ##| (df['type'] == 'Z-Brain-Thin')]
        if df_axial.shape[0]>0:
            df_axial=df_axial.reset_index()
            columnname="z_axial_brain_quality"
            columnvalue=df_axial.at[0,'quality']
            fill_datapoint_each_session_sniprcsv(session_id,columnname,columnvalue,copy_session)
        df_thin=df_this_session.loc[(df_this_session['type'] == 'Z-Brain-Thin') & (df_this_session['quality'] == 'usable')] ##| (df['type'] == 'Z-Brain-Thin')]
        if df_thin.shape[0]>0:
            df_thin=df_thin.reset_index()
            columnname="z_thin_brain_quality"
            columnvalue=df_thin.at[0,'quality']
            fill_datapoint_each_session_sniprcsv(session_id,columnname,columnvalue,copy_session)
        columnname="SELECTED_SCAN_ID"
        # columnvalue=SELECTED_SCAN_ID
        columnvalue=get_scan_id_given_session_id_N_niftiname(session_id,str(row['NIFTIFILES_PREFIX']))
        fill_datapoint_each_session_sniprcsv(session_id,columnname,columnvalue,copy_session)
        scan_quality=get_scan_quality(session_id,columnvalue,'quality')
        columnname="SELECTED_SCAN_QUALITY"
        columnvalue=scan_quality
        fill_datapoint_each_session_sniprcsv(session_id,columnname,columnvalue,copy_session)
        if row['xsiType']=="xnat:ctSessionData" and len(str(row['PDF_FILE_PATH'])) < 5 and counter > 3:
            call_fill_sniprsession_list_arguments=arguments()
            ##
            if  "ICH" in project_ID:
                call_fill_sniprsession_list_arguments.stuff=['fill_sniprsession_list_ICH',copy_session ,row['ID']]
                fill_sniprsession_list_ICH(call_fill_sniprsession_list_arguments)
                columnname="SUBSEQUENT_RUNS"
                columnvalue="1"
                fill_datapoint_each_session_sniprcsv(session_id,columnname,columnvalue,copy_session)
                counter=counter+1
            elif "SAH"  in project_ID:
                call_fill_sniprsession_list_arguments.stuff=['fill_sniprsession_list_SAH',copy_session ,row['ID']]
                fill_sniprsession_list_SAH(call_fill_sniprsession_list_arguments)
                columnname="SUBSEQUENT_RUNS"
                columnvalue="1"
                fill_datapoint_each_session_sniprcsv(session_id,columnname,columnvalue,copy_session)
                counter=counter+1  
            else:
                call_fill_sniprsession_list_arguments.stuff=['fill_sniprsession_list_1',copy_session ,row['ID']]
                fill_sniprsession_list_1(call_fill_sniprsession_list_arguments)
                columnname="SUBSEQUENT_RUNS"
                columnvalue="1"
                fill_datapoint_each_session_sniprcsv(session_id,columnname,columnvalue,copy_session)
                counter=counter+1
        # if counter>5:
        #     break
        command='rm  ' + working_dir + '/*.nii'
        subprocess.call(command,shell=True)
        command='rm  ' + working_dir+ '/*.dcm'
        subprocess.call(command,shell=True)
    except Exception as e:
        print(e)
        pass
dir_to_save=working_dir
resource_dirname_at_snipr=project_ID+"_SESSION_ANALYTICS_2"
#
# ##############################
copy_session_df=pd.read_csv(copy_session)
counter=0
time_now=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
for row_id,row in copy_session_df.iterrows():
    if '.pdf' in str(row['PDF_FILE_PATH']) and str(row['SUBSEQUENT_RUNS']) =='1':
        file_url=row['PDF_FILE_PATH']
        session_ID=row['ID']
        temp_dir=working_dir
        call_edit_session_analytics_file_arguments=arguments()
        call_edit_session_analytics_file_arguments.stuff=['add_file_size',session_ID,file_url,copy_session, "PDF_FILE_SIZE",temp_dir]
        add_file_size(call_edit_session_analytics_file_arguments)
        counter=counter+1
    # if counter>2:
    #     break
    #     csvfilename=args.stuff[1]
    # columnname=args.stuff[2]
    # neighboring_col=args.stuff[3]
    # csvfilename_edited=args.stuff[4]
call_edit_session_analytics_file_arguments=arguments()
call_edit_session_analytics_file_arguments.stuff=['move_one_column_after_another' , copy_session, 'PDF_FILE_NUM', "REGISTRATION_SUCCESS",copy_session]
rename_columns(call_edit_session_analytics_file_arguments)
uploadsinglefile_projectlevel_args_arguments=arguments()
uploadsinglefile_projectlevel_args_arguments.stuff=['uploadsinglefile_projectlevel_args',project_ID,os.path.dirname(copy_session),resource_dirname_at_snipr, os.path.basename(copy_session)]
uploadsinglefile_projectlevel_args(uploadsinglefile_projectlevel_args_arguments)
# copysinglefile_to_sniprproject ${project_ID} "$(dirname ${copy_session})" ${resource_dirname_at_snipr} $(basename ${copy_session})

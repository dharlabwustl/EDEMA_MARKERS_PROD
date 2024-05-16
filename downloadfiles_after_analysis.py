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
copy_session=sessions_list.split('.csv')[0]+project_ID+'_ANALYTICS_STEP3_'+time_now+'.csv'
download_a_single_file(file_path_csv,dir_to_receive_the_data,project_ID,copy_session)
copy_session_df=pd.read_csv(copy_session)
counter=0
dir_to_save=output_directory
resource_dir='MASKS'
def convert_if_numeric(s):
    try:
        # Try to convert the string to an integer
        return int(s)
    except ValueError:
        # If conversion fails, return the original string
        return s
for row_id,row in copy_session_df.iterrows():

    URI=row['URI']+'/scans/' +convert_if_numeric(row['SELECTED_SCAN_ID']
    # try:
    output_csvfile=row['ID']+ '_'+ row['SELECTED_SCAN_ID'].replace('.','_') + '.csv'
    print("{}::{}::{}::{}::{}".format('get_resourcefiles_metadata_saveascsv',URI,resource_dir,dir_to_receive_the_data,output_csvfile))
    # get_resourcefiles_metadata_saveascsv(get_latest_filepath_from_metadata_arguments)))
    get_latest_filepath_from_metadata_arguments1=arguments()
    get_latest_filepath_from_metadata_arguments1.stuff=['get_resourcefiles_metadata_saveascsv',URI,resource_dir,dir_to_receive_the_data,output_csvfile]
    get_resourcefiles_metadata_saveascsv(get_latest_filepath_from_metadata_arguments1)
    # except:
    #     pass
    # get_resourcefiles_metadata_saveascsv(URI,resource_dir,dir_to_receive_the_data,output_csvfile)
    # # while IFS=',' read -ra array; do
    # #   echo array::${array[22]}
    # pdf_file_location=row['PDF_FILE_PATH'] #${array[22]}
    # csv_file_location=row['CSV_FILE_PATH'] #${array[23]}
    # infarct_mask_location=row['INFARCT_MASK_FILE_PATH'] #${array[23]}
    # this_session_id=row['ID'] #${array[1]}
    # print(row['label'])
    # print(pdf_file_location)
    # n_pdffilename_length=len(str(pdf_file_location)) #${#pdf_file_location}
    # #   echo ${n_pdffilename_length}

    # n_csvfilename_length=len(str(csv_file_location)) #${#csv_file_location}
    # n_maskfilename_length=len(str(infarct_mask_location))
    # #   echo ${n_csvfilename_length}
    # if ".nii.gz" in str(infarct_mask_location) : #]; then
    #     infarct_mask_location_basename=os.path.basename(infarct_mask_location) #$(basename ${csv_file_location})
    #     get_latest_filepath_from_metadata_arguments=arguments()
    #     get_latest_filepath_from_metadata_arguments.stuff=['download_a_singlefile_with_URIString',infarct_mask_location,infarct_mask_location_basename,dir_to_save]
    #     download_a_singlefile_with_URIString(get_latest_filepath_from_metadata_arguments)

    #     # append_results_to_analytics_arguments=arguments()
    #     # append_results_to_analytics_arguments.stuff=['append_results_to_analytics',copy_session,os.path.join(dir_to_save,csv_output_filename), this_session_id, copy_session]
    #     # append_results_to_analytics(append_results_to_analytics_arguments)

    counter=counter+1

    if counter > 10 : #; then
        break

#
# #
# new_analytics_file_prefix=os.path.join(working_dir,project_ID+'_SESSIONS_RESULTS_METRICS')
# time_now=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
# new_analytics_file=new_analytics_file_prefix+'_'+time_now+'.csv'
# command="cp " + copy_session + " " + new_analytics_file
# subprocess.call(command,shell=True)
#
# # ##############################EDITING################################
# call_edit_session_analytics_file_arguments=arguments()
# call_edit_session_analytics_file_arguments.stuff=['call_edit_session_analytics_file' ,new_analytics_file]
# call_edit_session_analytics_file(call_edit_session_analytics_file_arguments)
# # #
# # #
# # call_edit_session_analytics_file_arguments=arguments()
# call_edit_session_analytics_file_arguments.stuff=['rename_columns' ,new_analytics_file,new_analytics_file ,'FileName_slice', 'FILENAME_NIFTI']
# rename_columns(call_edit_session_analytics_file_arguments) #
# # #
# # call_edit_session_analytics_file_arguments=arguments()
# call_edit_session_analytics_file_arguments.stuff=['remove_columns' ,new_analytics_file,new_analytics_file,  'xsiType', "INFARCT VOX_NUMBERS",	"INFARCT DENSITY"	,"NON INFARCT VOX_NUMBERS" ,'INFARCT THRESH RANGE', 'NORMAL THRESH RANGE', 'INFARCT REFLECTION VOLUME', 'NON INFARCT DENSITY', 'NUMBER_NIFTIFILES', 'NUMBER_SELECTEDSCANS' ,'INFARCT_FILE_NUM', 'CSF_FILE_NUM', 'CSV_FILE_NUM',   "INFARCT_MASK_FILE_PATH", "CSF_MASK_FILE_PATH", "ID" ,"xsiType", "PDF_FILE_SIZE", "CSV_FILE_PATH", 'xnat:subjectassessordata/id', "ORGINAL_INFARCT_VOLUME",	"INFARCTUSED_VOL_RATIO"	,"NONINFACRTUSED_VOL_RATIO" ]
#
# #
# if "ICH" in project_ID:
#     # call_edit_session_analytics_file_arguments=arguments()
#     call_edit_session_analytics_file_arguments.stuff=['remove_columns',new_analytics_file,new_analytics_file, "xsiType", 'INFARCT THRESH RANGE', 'NORMAL THRESH RANGE', 'INFARCT REFLECTION VOLUME', 'NON INFARCT DENSITY', "NUMBER_NIFTIFILES", "NUMBER_SELECTEDSCANS" ,"INFARCT_FILE_NUM", "CSF_FILE_NUM", "CSV_FILE_NUM","INFARCT_MASK_FILE_PATH", "CSF_MASK_FILE_PATH", "ID", "xsiType", "PDF_FILE_SIZE", "CSV_FILE_PATH", "CSV_FILE_PATH",	"CSF_MASK",	"ICH_EDEMA_MASK",	"ICH_MASK"] #  )
# remove_columns(call_edit_session_analytics_file_arguments)
#
# columnname='FILENAME_NIFTI'
# new_position=5
# call_edit_session_analytics_file_arguments=arguments()
# call_edit_session_analytics_file_arguments.stuff=['call_move_one_column', new_analytics_file,columnname,new_position,new_analytics_file]
# call_move_one_column(call_edit_session_analytics_file_arguments)
#
#
# columnname='SCAN_SELECTED'
# new_position=4
# # call_edit_session_analytics_file_arguments=arguments()
# call_edit_session_analytics_file_arguments.stuff=['call_move_one_column',new_analytics_file,columnname,new_position,new_analytics_file]
# call_move_one_column(call_edit_session_analytics_file_arguments)
# #
#
#
# call_edit_session_analytics_file_arguments.stuff=['rename_columns', new_analytics_file,new_analytics_file, 'subject_id' ,'subject']
# rename_columns(call_edit_session_analytics_file_arguments)
# #
# call_edit_session_analytics_file_arguments.stuff=['rename_columns', new_analytics_file,new_analytics_file, "label", "snipr_session"]
# rename_columns(call_edit_session_analytics_file_arguments)
# #
# call_edit_session_analytics_file_arguments.stuff=['rename_columns', new_analytics_file,new_analytics_file, "SELECTED_SCAN_ID", "scan_selected"]
# rename_columns(call_edit_session_analytics_file_arguments)
# #
# call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file,"acquisition_datetime", "scan_date_time"]
# rename_columns(call_edit_session_analytics_file_arguments)
# #
# call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file,"FILENAME_NIFTI", "scan_name"]
# rename_columns(call_edit_session_analytics_file_arguments)
# #
# call_edit_session_analytics_file_arguments.stuff=['rename_columns', new_analytics_file,new_analytics_file,"SLICE_NUM", "slices"]
# rename_columns(call_edit_session_analytics_file_arguments)
# #
# call_edit_session_analytics_file_arguments.stuff=['rename_columns', new_analytics_file,new_analytics_file,"res_x", "px"]
# rename_columns(call_edit_session_analytics_file_arguments)
# #
# call_edit_session_analytics_file_arguments.stuff=['remove_columns' , new_analytics_file,new_analytics_file, "res_y"]
# remove_columns(call_edit_session_analytics_file_arguments)
# #
# call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file,"slice_thickness", "pz"]
# rename_columns(call_edit_session_analytics_file_arguments)
# #
# call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file,"scanner", "scanner_name"]
# rename_columns(call_edit_session_analytics_file_arguments)
# #
# call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, "body_part", "body_site"]
# rename_columns(call_edit_session_analytics_file_arguments)
# #
# call_edit_session_analytics_file_arguments.stuff=['rename_columns', new_analytics_file,new_analytics_file, "SCAN_DESCRIPTION", "scan_kernel"]
# rename_columns(call_edit_session_analytics_file_arguments)
# #
# call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file,'LEFT CSF VOLUME', "csf_left"]
# rename_columns(call_edit_session_analytics_file_arguments)
#
# call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'RIGHT CSF VOLUME', "csf_right"]
# rename_columns(call_edit_session_analytics_file_arguments)
#
# call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'TOTAL CSF VOLUME' ,"csf_total"]
# rename_columns(call_edit_session_analytics_file_arguments)
#
# call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'INFARCT SIDE', "stroke_side"]
# rename_columns(call_edit_session_analytics_file_arguments)
#
# call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'NWU' ,"nwu"]
# rename_columns(call_edit_session_analytics_file_arguments)
#
# call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'INFARCT VOLUME', "infarct_volume"]
# rename_columns(call_edit_session_analytics_file_arguments)
#
# call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'BET VOLUME', "cranial"]
# rename_columns(call_edit_session_analytics_file_arguments)
#
# call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'CSF RATIO', "csf_ratio"]
# rename_columns(call_edit_session_analytics_file_arguments)
#
# call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'LEFT BRAIN VOLUME without CSF', "brain_left"]
# rename_columns(call_edit_session_analytics_file_arguments)
#
# call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'RIGHT BRAIN VOLUME without CSF' ,"brain_right"]
# rename_columns(call_edit_session_analytics_file_arguments)
#
# call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'NIFTIFILES_PREFIX', "scan_stem"]
# rename_columns(call_edit_session_analytics_file_arguments)
#
#
# call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'PDF_FILE_NUM', "pdf_created"]
# rename_columns(call_edit_session_analytics_file_arguments)
#
# call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'AXIAL_SCAN_NUM', "axial_number"]
# rename_columns(call_edit_session_analytics_file_arguments)
#
# call_edit_session_analytics_file_arguments.stuff=['rename_columns' , new_analytics_file,new_analytics_file, 'THIN_SCAN_NUM' ,"axial_thin_number"]
# rename_columns(call_edit_session_analytics_file_arguments)
#
# resource_dirname_at_snipr=project_ID+"_SESSION_ANALYTICS_3"
#
# uploadsinglefile_projectlevel_args_arguments=arguments()
# uploadsinglefile_projectlevel_args_arguments.stuff=['uploadsinglefile_projectlevel_args',project_ID,os.path.dirname(new_analytics_file),resource_dirname_at_snipr, os.path.basename(new_analytics_file)]
# uploadsinglefile_projectlevel_args(uploadsinglefile_projectlevel_args_arguments)
# uploadsinglefile_projectlevel_args_arguments.stuff=['uploadsinglefile_projectlevel_args',project_ID,os.path.dirname(copy_session),resource_dirname_at_snipr, os.path.basename(copy_session)]
# uploadsinglefile_projectlevel_args(uploadsinglefile_projectlevel_args_arguments)
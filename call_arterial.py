# from infarct_in_each_lobar_regionsNov262024 import *

from infarct_in_each_arterial_regionsNov262024 import *
# from infarct_in_each_aretrial_regions_v2 import *
import sys,os,glob,subprocess
import pandas as pd
import time


file_session_list='sessions_COLI_ANALYTICS_STEP3_20231122041129_ordered.csv'
f_df=pd.read_csv(file_session_list)
print(f_df.columns)
def clean_dirs():
    command='rm -r workinginput/*'
    subprocess.call(command,shell=True)
    command='rm -r maskonly/*'
    subprocess.call(command,shell=True)
    command="rm -r workingoutput/*"
    subprocess.call(command,shell=True)
    command="rm -r input/*"
    subprocess.call(command,shell=True)
    command="rm -r working/*"
    subprocess.call(command,shell=True)
    command="rm -r ZIPFILEDIR/*"
    subprocess.call(command,shell=True)
    command="rm -r output/*"
    subprocess.call(command,shell=True)
    command="rm -r ZIPFILEDIR/*"
    subprocess.call(command,shell=True)
    command="rm -r NIFTIFILEDIR/*"
    subprocess.call(command,shell=True)
    command="rm -r DICOMFILEDIR/*"
    subprocess.call(command,shell=True)
    command="rm -r outputinsidedocker/*"
    subprocess.call(command,shell=True)
#     mkdir working
# mkdir input
# mkdir ZIPFILEDIR
# mkdir output
# mkdir NIFTIFILEDIR
# mkdir DICOMFILEDIR
# rm -r working/*
# rm -r input/*
# rm -r ZIPFILEDIR/*
# rm -r output/*
# rm -r NIFTIFILEDIR/*
# rm -r DICOMFILEDIR/*
# mkdir workingoutput
# mkdir workinginput
# mkdir ZIPFILEDIR
# mkdir outputinsidedocker
# mkdir software
# rm -r workinginput/*
# rm -r workingoutput/*
# rm -r outputinsidedocker/*
# rm -r workingoutput/*
# rm -r ZIPFILEDIR/*
# rm -r outputinsidedocker/*
# rm -r software/*
for row_id,row_item in f_df.iterrows():

    try:
        clean_dirs()
        # print(row_item['ID'])

        # lobar_region_volumes_n_display(SESSION_ID)

        # time.sleep(5)
        SESSION_ID=str(row_item['ID'])
        print(SESSION_ID)
        # if 'SNIPR01_E00193' not in SESSION_ID:
        # lobar_region_volumes_n_display(SESSION_ID)
        # clean_dirs()
        arterial_region_volumes_n_display(SESSION_ID)
        break
        # clean_dirs()
        # break

            # break
    except Exception as e :
        
        print(e)
        # break
        pass

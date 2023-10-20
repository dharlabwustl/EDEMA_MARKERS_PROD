#!/usr/bin/env python
# coding: utf-8
import inspect

# In[1]:


import pandas as pd
import numpy as np
import os,sys,glob
import datetime
import argparse
# sys.path.append('/media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD');
from utilities_simple import *
from download_with_session_ID import *

def combinecsvsfiles_from_a_csv_containing_its_list(args): #listofcsvfiles_filename,outputfilename):
    try:
        listofcsvfiles_filename=args.stuff[1]
        outputfilename=args.stuff[2]
        csv_counter=0
        combined_csv_df=""
        for each_file in listofcsvfiles_filename:
            try:
                each_file_df=pd.read_csv(each_file)
                if csv_counter==0:
                    combined_csv_df=each_file_df
                    csv_counter=csv_counter+1
                else:
                    combined_csv_df=pd.concat([combined_csv_df,each_file_df])
            except:
                pass
        combined_csv_df = combined_csv_df.drop_duplicates()
        combined_csv_df.to_csv(outputfilename, index=False, encoding='utf-8-sig')
        print("I SUCCEED AT ::{}".format(inspect.stack()[0][3]))
        return 1
    except:
        print("I FAILED AT ::{}".format(inspect.stack()[0][3]))
        pass
        return 0
def download_then_upload_files_withurl_from_a_csvfile(args) : #,masterfile_scans,column_name_for_url,column_name_for_session_name,file_extension,X_level,level_name,dir_to_save,resource_dirname_at_snipr):

    try:
        masterfile_scans=args.stuff[1]
        column_name_for_url=args.stuff[2]
        column_name_for_session_name=args.stuff[3]
        file_extension=args.stuff[4]
        X_level=args.stuff[5]
        level_name=args.stuff[6]
        dir_to_save=args.stuff[7]
        resource_dirname_at_snipr=args.stuff[8]
        masterfile_scans_df=pd.read_csv(masterfile_scans)
        masterfile_scans_df=masterfile_scans_df[masterfile_scans_df[column_name_for_url].str.contains(file_extension)] #df["name"].str.contains("Honda")
        for index, row in masterfile_scans_df.iterrows():
            # if len(str(row[column_name_for_url])) > 1:
            # if row['PDF_FILE_AVAILABLE']==1:
            url=row[column_name_for_url] #"PDF_FILE_NAME"]
            filename=row[column_name_for_session_name] + "_" + os.path.basename(url)
            try:
                download_with_session_ID.download_a_singlefile_with_URIString(url,filename,dir_to_save)
                download_with_session_ID.uploadsinglefile_X_level(X_level,level_name,os.path.join(dir_to_save,filename),resource_dirname_at_snipr)
            except:
                pass

        print("I SUCCEEDED AT ::{}".format(inspect.stack()[0][3]))
        subprocess.call("echo " + "I PASSED AT ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )

    except:
        print("I FAILED AT ::{}".format(inspect.stack()[0][3]))
        subprocess.call("echo " + "I FAILED AT ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
        pass

    return 0

def download_a_singlefile_with_URIString(args):
    url=args.stuff[1]
    filename=args.stuff[2]
    dir_to_save=args.stuff[3]
    print("url::{}::filename::{}::dir_to_save::{}".format(url,filename,dir_to_save))
    xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    xnatSession.renew_httpsession()
    # command="echo  " + url['URI'] + " >> " +  os.path.join(dir_to_save,"test.csv")
    # subprocess.call(command,shell=True)
    response = xnatSession.httpsess.get(xnatSession.host +url) #/data/projects/ICH/resources/179772/files/ICH_CTSESSIONS_202305170753.csv") #
    #                                                       # "/data/experiments/SNIPR02_E03548/scans/1-CT1/resources/147851/files/ICH_0001_01022017_0414_1-CT1_threshold-1024.0_22121.0TOTAL_VersionDate-11302022_04_22_2023.csv") ## url['URI'])
    zipfilename=os.path.join(dir_to_save,filename ) #"/data/projects/ICH/resources/179772/files/ICH_CTSESSIONS_202305170753.csv")) #sessionId+scanId+'.zip'
    with open(zipfilename, "wb") as f:
        for chunk in response.iter_content(chunk_size=512):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    xnatSession.close_httpsession()
    return zipfilename

def get_latest_filepath_from_metadata(args):
    URI=args.stuff[1]
    resource_dir=args.stuff[2]
    extension_to_find_list=args.stuff[3]
    SCAN_URI_NIFTI_FILEPREFIX=args.stuff[4]
    file_location_csv=args.stuff[5]
    latest_file_path=""
    try:
        metadata=get_resourcefiles_metadata(URI,resource_dir)
        df_listfile = pd.read_json(json.dumps(metadata))
        df_listfile=df_listfile[df_listfile.URI.str.contains(extension_to_find_list)]
        if len(SCAN_URI_NIFTI_FILEPREFIX)>0:
            df_listfile=df_listfile[df_listfile.URI.str.contains(SCAN_URI_NIFTI_FILEPREFIX)]
        latest_file_df=get_latest_file(df_listfile) #,SCAN_URI_NIFTI_FILEPREFIX)
        latest_file_path=str(latest_file_df.at[0,"URI"])
        latest_file_path_df=pd.DataFrame([latest_file_path])
        latest_file_path_df.columns=['FILE_PATH']
        latest_file_path_df.to_csv(file_location_csv,index=False)
        print("I SUCCEEDED AT ::{}".format(inspect.stack()[0][3]))
        subprocess.call("echo " + "I PASSED AT ::{}  >> /workingoutput/error.txt".format(latest_file_path) ,shell=True )
        # subprocess.call("echo " + "latest_file_path::{}  >> /workingoutput/error.txt".format(latest_file_path) ,shell=True )
        subprocess.call("echo " + "I PASSED AT ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
        # subprocess.call("echo " + "URI ::{}  >> /workingoutput/error.txt".format(URI) ,shell=True )
        # subprocess.call("echo " + "resource_dir::{}  >> /workingoutput/error.txt".format(resource_dir) ,shell=True )
        # subprocess.call("echo " + "extension_to_find_list ::{}  >> /workingoutput/error.txt".format(extension_to_find_list) ,shell=True )

    except:
        print("I FAILED AT ::{}".format(inspect.stack()[0][3]))
        print(" NO SUCH FILE PRESENT!!")
        # subprocess.call("echo " + "latest_file_path::{}  >> /workingoutput/error.txt".format(latest_file_path) ,shell=True )
        subprocess.call("echo " + "I FAILED AT ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
        # subprocess.call("echo " + "URI ::{}  >> /workingoutput/error.txt".format(URI) ,shell=True )
        # subprocess.call("echo " + "resource_dir::{}  >> /workingoutput/error.txt".format(resource_dir) ,shell=True )
        # subprocess.call("echo " + "extension_to_find_list ::{}  >> /workingoutput/error.txt".format(extension_to_find_list) ,shell=True )
        pass
    return latest_file_path

def create_empty_csvfile(args):

    returnvalue=0
    # print("I AM AT ::{}".format(inspect.stack()[0][3]))
    try:
        csvfilename=args.stuff[1]
        df=pd.DataFrame([1])
        df.columns=['TOREMOVE']
        df.to_csv(csvfilename)
        subprocess.call("echo " + "passed at expression::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
    except:
        subprocess.call("echo " + "failed at expression::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
        pass
    return  returnvalue


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stuff', nargs='+')
    args = parser.parse_args()
    return_value=0
    globals()[args.stuff[0]](args)
    return return_value
if __name__ == '__main__':
    main()


# In[ ]:





# In[ ]:





# In[ ]:





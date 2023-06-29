#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os,sys,glob
import datetime
import argparse
# sys.path.append('/media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD');
from utilities_simple import *
from download_with_session_ID import *
def get_latest_csvfile_singlefilename(df1,extens='.csv'):
    ## get all the rows with csv in the name:
    allfileswithprefix1_df = df1[df1['Name'].str.contains(extens)]
    # allfileswithprefix1_df = allfileswithprefix1_df[allfileswithprefix1_df['Name'].str.contains('TOTAL')]
    allfileswithprefix1_df['FILENAME']=allfileswithprefix1_df['Name']
    # 
    allfileswithprefix1_df['DATE']=allfileswithprefix1_df['Name']
    allfileswithprefix1_df['PREFIX']=allfileswithprefix1_df['Name']
    allfileswithprefix1_df[['PREFIX', 'EXT']] = allfileswithprefix1_df['PREFIX'].str.split('_thresh', 1, expand=True)
    allfileswithprefix1_df['DATE'] = allfileswithprefix1_df['DATE'].str[-14:-4]
    allfileswithprefix1_df['DATE'] = allfileswithprefix1_df['DATE'].str.replace('_', '')
    allfileswithprefix1_df["PREFIX"]=allfileswithprefix1_df["PREFIX"].apply(lambda x: os.path.splitext(os.path.basename(x))[0])
    # print(allfileswithprefix1_df['PREFIX']) #[0])
    # print(np.unique(allfileswithprefix1_df['PREFIX']).shape)
    # print(allfileswithprefix1_df['PREFIX'].shape)
    unique_session_name=np.unique(allfileswithprefix1_df['PREFIX'])
    allfileswithprefix1_df['DATETIME'] =    allfileswithprefix1_df['DATE']
    allfileswithprefix1_df['DATETIME'] = pd.to_datetime(allfileswithprefix1_df['DATETIME'], format='%m%d%Y', errors='coerce')
    # print(allfileswithprefix1_df['DATETIME'])
    # print(unique_session_name)
    # for x in range(unique_session_name.shape[0]):
    x=0
    # print(unique_session_name[x])
    x_df=allfileswithprefix1_df.loc[allfileswithprefix1_df['PREFIX'] == unique_session_name[x]]
    x_df = x_df.sort_values(by=['DATETIME'], ascending=False)
    x_df=x_df.reset_index(drop=True)
    # print(x_df)
    # if len(allfileswithprefix1)>0:
    #     allfileswithprefix=sorted(allfileswithprefix1, key=os.path.getmtime)
    filetocopy=x_df['URI'][0]
    # print(filetocopy)
    return filetocopy
def get_latest_csvfile_singlefilename_infarct(df1,extens='columndropped.csv'):
    ## get all the rows with csv in the name:
    allfileswithprefix1_df = df1[df1['Name'].str.contains(extens)]
    # allfileswithprefix1_df = allfileswithprefix1_df[allfileswithprefix1_df['Name'].str.contains('TOTAL')]
    allfileswithprefix1_df['FILENAME']=allfileswithprefix1_df['Name']
    #
    # allfileswithprefix1_df['DATE']=allfileswithprefix1_df['Name']
    allfileswithprefix1_df['DATE']=allfileswithprefix1_df['Name'].str.split("columndropped.csv").str[0]+'.csv'

    allfileswithprefix1_df['PREFIX']=allfileswithprefix1_df['Name']
    allfileswithprefix1_df[['PREFIX', 'EXT']] = allfileswithprefix1_df['PREFIX'].str.split('_thresh', 1, expand=True)
    allfileswithprefix1_df['DATE'] = allfileswithprefix1_df['DATE'].str[-14:-4]
    allfileswithprefix1_df['DATE'] = allfileswithprefix1_df['DATE'].str.replace('_', '')
    allfileswithprefix1_df["PREFIX"]=allfileswithprefix1_df["PREFIX"].apply(lambda x: os.path.splitext(os.path.basename(x))[0])
    # print(allfileswithprefix1_df['PREFIX']) #[0])
    # print(np.unique(allfileswithprefix1_df['PREFIX']).shape)
    # print(allfileswithprefix1_df['PREFIX'].shape)
    unique_session_name=np.unique(allfileswithprefix1_df['PREFIX'])
    allfileswithprefix1_df['DATETIME'] =    allfileswithprefix1_df['DATE']
    allfileswithprefix1_df['DATETIME'] = pd.to_datetime(allfileswithprefix1_df['DATETIME'], format='%m%d%Y', errors='coerce')
    # print(allfileswithprefix1_df['DATETIME'])
    # print(unique_session_name)
    # for x in range(unique_session_name.shape[0]):
    x=0
    # print(unique_session_name[x])
    x_df=allfileswithprefix1_df.loc[allfileswithprefix1_df['PREFIX'] == unique_session_name[x]]
    x_df = x_df.sort_values(by=['DATETIME'], ascending=False)
    x_df=x_df.reset_index(drop=True)
    # print(x_df)
    # if len(allfileswithprefix1)>0:
    #     allfileswithprefix=sorted(allfileswithprefix1, key=os.path.getmtime)
    filetocopy=x_df['URI'][0]
    # print(filetocopy)
    return filetocopy
def create_sessionid(csvfilename):
    df1 = pd.read_csv(csvfilename)
    if not('SESSIONID' in df1.columns):
        xx=df1['URI'].str.split('/', expand=True)
        df1['SESSIONID']=xx[3]
        df1.to_csv(csvfilename,index=False)


# In[ ]:





# In[2]:


# sessioncsv='./outputinsidedocker/sessions.csv'
# sessioncsv_df=pd.read_csv(sessioncsv)
# # sessioncsv_df['NIFTIFILENAME']=""
# # sessioncsv_df['NIFTIFILENAME_AVAILABLE']=0
# dir_csv="./outputinsidedocker"
def writetomastersession(sessioncsv_df,filename,filename_available,row,xx):
    # print("{}::{}::{}".format(sessioncsv_df,filename,filename_available))
    sessioncsv_df.loc[sessioncsv_df['ID'] ==xx[3], filename] = row['URI'] #[0]
    sessioncsv_df.loc[sessioncsv_df['ID'] ==xx[3], filename_available] = 1 ##df1['URI'][0]
    if filename=='NIFTIFILENAME':
        sessioncsv_df.loc[sessioncsv_df['ID'] ==xx[3], 'NUMBEROFSLICES'] = row['NUMBEROFSLICES'] #[0]
        sessioncsv_df.loc[sessioncsv_df['ID'] ==xx[3], 'NIFTIFILE_BASENAME'] = row['Name'] ##row['NUMBEROFSLICES'] #[0]
        # sessioncsv_df.loc[sessioncsv_df['ID'] ==xx[3], filename_available] = 1 ##df1['URI'][0]
        
    return sessioncsv_df
def write_scantype_tomastersession(sessioncsv_df,scan_type,xx):
    sessioncsv_df.loc[sessioncsv_df['ID'] ==xx[3], 'SCAN_TYPE'] = scan_type #row['NUMBEROFSLICES'] #[0]
    return sessioncsv_df

# In[3]:


def insertmaskfilesname(sessioncsv_df,dir_csv):
    for x in glob.glob(os.path.join(dir_csv,"*MASKS.csv")):
        # if 'sessions.csv' != os.path.basename(x):

        try:
            df1 = pd.read_csv(x) #, delim_whitespace=False)



            for index, row in df1.iterrows():
                            # get file extension:
                extens=row['Name'].split('.')
                # print(row['Name'])
                if 'gz' in extens[-1] : #row['Name']:
                    if '_infarct_auto_removesmall.nii.gz' in row['Name']:
                        # print("I AM HERE")
                        filename='INFARCTFILENAME'
                        filename_available='INFARCTFILE_AVAILABLE'
                    elif '_csf_unet.nii.gz' in row['Name']:
                        filename='CSFFILENAME'
                        filename_available='CSFFILE_AVAILABLE'
                    # elif '_normalized_class1.nii.gz' in row['Name']:
                    #     filename='ICHFILENAME'
                    #     filename_available='ICHFILE_AVAILABLE'
                    # elif '_normalized_class2.nii.gz' in row['Name']:
                    #     filename='ICHEDEMAFILENAME'
                    #     filename_available='ICHEDEMAFILE_AVAILABLE'
                    elif '_levelset.nii.gz' in row['Name']:
                        filename='LEVELSETFILENAME'
                        filename_available='LEVELSETFILE_AVAILABLE'
                    else:
                        continue
#                 elif 'nii' in extens[-1]: 

#                     filename='NIFTIFILENAME'
#                     filename_available='NIFTIFILE_AVAILABLE'    
                # elif 'csv' in extens[-1]:


                xx=row['URI'].split('/') #.str.split('/', expand=True)
                sessioncsv_df=writetomastersession(sessioncsv_df,filename,filename_available,row,xx)
                filename=''
                filename_available=''

        except:
            continue
    return sessioncsv_df
# def call_insertmaskfilesname():
#     dir_csv=sys.argv[1]
#     insertmaskfilesname(dir_csv)
    


# In[4]:


def insertniftifilename(sessioncsv_df,dir_csv):
    for x in glob.glob(os.path.join(dir_csv,"*this_session_final_ct.csv")):
        # if 'sessions.csv' != os.path.basename(x):
        print(" I AM AT::{}".format(inspect.stack()[0][3]))
        try:
            df1 = pd.read_csv(x) #, delim_whitespace=False)



            for index, row in df1.iterrows():
                            # get file extension:
                extens=row['Name'].split('.')
                if 'nii' in extens[-1] or  'nii' in extens[-2]:

                    filename='NIFTIFILENAME'
                    filename_available='NIFTIFILE_AVAILABLE'    
                # elif 'csv' in extens[-1]:


                xx=row['URI'].split('/') #.str.split('/', expand=True)
                sessionId=xx[3]
                scanId=xx[5]
                subprocess.call("echo " + "scanId1type::{}  >> /workingoutput/error.txt".format(scanId) ,shell=True )
                # print("sessionId::{} and scanId::{}".format(sessionId,scanId))
                scan_type=get_scan_type(sessionId,scanId)

                sessioncsv_df=writetomastersession(sessioncsv_df,filename,filename_available,row,xx)
                sessioncsv_df=write_scantype_tomastersession(sessioncsv_df,scan_type,xx)
                filename=''
                filename_available=''
                print("I SUCCEEDED AT::{}::extens::{}::filename::{}::filename_available::{}::row::{},xx::{}".format(inspect.stack()[0][3],extens[-1],filename,filename_available,row,xx))
        except:
    # except:
            print("I FAILED AT::{}".format(inspect.stack()[0][3]))
    # pass
            continue
    return sessioncsv_df
# def call_insertmaskfilesname():
#     dir_csv=sys.argv[1]
#     insertniftifilename(dir_csv)


# In[5]:


def insertedemabiomarkerfilename(sessioncsv_df,dir_csv):
    for x in glob.glob(os.path.join(dir_csv,"*EDEMA_BIOMARKER.csv")):
            # if 'sessions.csv' != os.path.basename(x):

            try:
                df1 = pd.read_csv(x) #, delim_whitespace=False)
                csvfile=get_latest_csvfile_singlefilename_infarct(df1,'.csv')
                # # if len(csvfile)>4:
                #     # print(csvfile)
                pdffile=get_latest_csvfile_singlefilename(df1,'.pdf')
                # # if len(pdffile)>4:
                print(csvfile)
                print(pdffile)
                # # def writetomastersession(sessioncsv_df,filename,filename_available,row):
                # # print("{}::{}::{}".format(sessioncsv_df,filename,filename_available))
                # # print(pdffile.split('/')[3])
                xx=pdffile.split('/')##[3]
                print(xx)
                filename='INFARCT_CSVFILENAME'
                filename_available='INFARCT_CSVFILE_AVAILABLE'
                # print(pdffile)
                sessioncsv_df.loc[sessioncsv_df['ID'] ==xx[3], filename]=str(csvfile) # row['URI'] #[0]
                sessioncsv_df.at[sessioncsv_df['ID'] ==xx[3], filename_available] = 1 ##df1['URI'][0]
                filename='INFARCT_PDFFILENAME'
                filename_available='INFARCT_PDFFILE_AVAILABLE'
                sessioncsv_df.loc[sessioncsv_df['ID'] ==xx[3], filename] =pdffile # row['URI'] #[0]
                sessioncsv_df.loc[sessioncsv_df['ID'] ==xx[3], filename_available] = 1 ##df1['URI'][0]
            except:
                continue
    return sessioncsv_df
# def call_insertedemabiomarkerfilename():
#     dir_csv=sys.argv[1]
#     insertniftifilename(dir_csv)


# In[6]:


def insertichquantificationfilename(sessioncsv_df,dir_csv):
    for x in glob.glob(os.path.join(dir_csv,"*ICH_QUANTIFICATION.csv")):
        # if 'sessions.csv' != os.path.basename(x):

        try:
            df1 = pd.read_csv(x) #, delim_whitespace=False)
            csvfile=get_latest_csvfile_singlefilename(df1,'.csv')
            # # if len(csvfile)>4:
            #     # print(csvfile)
            pdffile=get_latest_csvfile_singlefilename(df1,'.pdf')
            # # if len(pdffile)>4:
            # print(csvfile)
            # print(pdffile)
            # # def writetomastersession(sessioncsv_df,filename,filename_available,row):
            # # print("{}::{}::{}".format(sessioncsv_df,filename,filename_available))
            # # print(pdffile.split('/')[3])
            xx=pdffile.split('/')##[3]
            # print(xx[3])
            filename='ICH_CSVFILENAME'
            filename_available='ICH_CSVFILE_AVAILABLE'
            # print(pdffile)
            sessioncsv_df.loc[sessioncsv_df['ID'] ==xx[3], filename] = csvfile # row['URI'] #[0]
            sessioncsv_df.at[sessioncsv_df['ID'] ==xx[3], filename_available] = 1 ##df1['URI'][0]
            filename='ICH_PDFFILENAME'
            filename_available='ICH_PDFFILE_AVAILABLE'
            sessioncsv_df.loc[sessioncsv_df['ID'] ==xx[3], filename] = pdffile # row['URI'] #[0]
            sessioncsv_df.loc[sessioncsv_df['ID'] ==xx[3], filename_available] = 1 ##df1['URI'][0]
            print("{}::{}".format(sessioncsv_df['ID']) ) #sessioncsv_df.iloc[sessioncsv_df['ID'] ==xx[3]])
        except:
            continue
    return sessioncsv_df
# def call_insertichquantificationfilename():
#     dir_csv=sys.argv[1]
#     insertniftifilename(dir_csv)
def insertavailablefilenames(session_csvfile,dir_csv,filenametosave,directorytosave):
    try:
        sessioncsv_df=pd.read_csv(os.path.join(dir_csv,session_csvfile))
        sessioncsv_df=sessioncsv_df[sessioncsv_df['xsiType']=='xnat:ctSessionData']
        sessioncsv_df=insertniftifilename(sessioncsv_df,dir_csv)
        sessioncsv_df=insertmaskfilesname(sessioncsv_df,dir_csv)
        # if "ICH" in typeofmask:
        sessioncsv_df=insertichquantificationfilename(sessioncsv_df,dir_csv)
        # if "INFARCT" in typeofmask:
        sessioncsv_df=insertedemabiomarkerfilename(sessioncsv_df,dir_csv)

        sessioncsv_df.to_csv(os.path.join(directorytosave,filenametosave),index=False)
        print("I SUCCEEDED AT::{}".format(inspect.stack()[0][3]))
    except:
        print("I FAILED AT::{}".format(inspect.stack()[0][3]))
        pass

def insertavailablefilenames_infarct(session_csvfile,dir_csv,filenametosave,directorytosave):
    try:
        sessioncsv_df=pd.read_csv(os.path.join(dir_csv,session_csvfile))
        sessioncsv_df=sessioncsv_df[sessioncsv_df['xsiType']=='xnat:ctSessionData']
        sessioncsv_df=insertniftifilename(sessioncsv_df,dir_csv)
        sessioncsv_df=insertmaskfilesname(sessioncsv_df,dir_csv)
        # if "ICH" in typeofmask:
        # sessioncsv_df=insertichquantificationfilename(sessioncsv_df,dir_csv)
        # if "INFARCT" in typeofmask:
        sessioncsv_df=insertedemabiomarkerfilename(sessioncsv_df,dir_csv)

        sessioncsv_df.to_csv(os.path.join(directorytosave,filenametosave),index=False)
        print("I SUCCEEDED AT::{}".format(inspect.stack()[0][3]))
    except:
        print("I FAILED AT::{}".format(inspect.stack()[0][3]))
        pass
def call_insertavailablefilenames():
    session_csvfile=sys.argv[1]
    dir_csv=sys.argv[2]
    # typeofmask=sys.argv[3]
    filenametosave=sys.argv[3]
    directorytosave=sys.argv[4]
    latexfilename=os.path.join(directorytosave,sys.argv[5])
    subprocess.call("echo " + "I SUCCEEDED AT ::{}  > /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
    insertavailablefilenames_infarct(session_csvfile,dir_csv,filenametosave,directorytosave)
    masterfilename=os.path.join(directorytosave,filenametosave)
    pdffromanalytics(masterfilename,latexfilename)

### after downloading the file, which contain the list of analyzed nifti and its corresponding pdf ,from the snipr
def snipr_analytics_result(masterfilename,filenamefornotanalyzeddata,filenamefornotanalyzeddatafigure):
    # masterfilename="/media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/TESTING_EDEMA_BIOMARKER/COLI_CTSESSIONS.csv"
    # filenamefornotanalyzeddata =masterfilename.split('.csv')[0]+'notanalyzedinround1.csv'
    # filenamefornotanalyzeddatafigure =masterfilename.split('.csv')[0]+'notanalyzedinround1.png'
    masterfilename_df=pd.read_csv(masterfilename)
    xx=masterfilename_df.columns
    masterfilename_df_niftifileavailable=masterfilename_df[masterfilename_df['NIFTIFILE_AVAILABLE']==1]
    masterfilename_df_analysisnotdone=masterfilename_df_niftifileavailable[masterfilename_df[xx[-1]]!=1]
    masterfilename_df_analysisnotdone.shape
    masterfilename_df_analysisdone=masterfilename_df_niftifileavailable[masterfilename_df[xx[-1]]==1]
    masterfilename_df_analysisdone.shape
    print(masterfilename_df_niftifileavailable.shape)
    print(masterfilename_df_analysisdone.shape)
    print(masterfilename_df_analysisnotdone.shape)
    print(masterfilename_df_analysisdone.shape[0]+ masterfilename_df_analysisnotdone.shape[0])
    # afterroundfilename=filenamefornotanalyzeddata #masterfilename.split('.csv')[0]+'notanalyzedinround1.csv'
    masterfilename_df_analysisnotdone.to_csv(filenamefornotanalyzeddata,index=False)
    # print(masterfilename_df_analysisdone.shape[1]+ masterfilename_df_analysisnotdone.shape[1])
    available_columns=[item for item in masterfilename_df.columns if 'AVAILABLE' in item]
    print([item for item in masterfilename_df.columns if 'AVAILABLE' in item])
    masterfilename_df_analytics = masterfilename_df[available_columns]
    masterfilename_df_analytics
    df2 = pd.DataFrame(masterfilename_df_analytics.sum(axis=0)).T
    df2['TOTAL_NUMBER_OF_SESSIONS']=masterfilename_df.shape[0]
    try:
        df2 = df2.drop('LEVELSETFILE_AVAILABLE', axis=1)
        print(df2)
    except:
        pass
    ax=df2.T.plot.bar(legend=False ,figsize=(19, 19))
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    ax.get_figure().savefig(filenamefornotanalyzeddatafigure)
def makepdfwithimages(latexfilename,imagelist,caption="",imagescale=1, angle=0,space=1):
    latex_start(latexfilename)
    latex_begin_document(latexfilename)
    latex_start_tableNc_noboundary(latexfilename,len(imagelist))
    latex_insertimage_tableNc(latexfilename,imagelist,len(imagelist), caption=caption,imagescale=imagescale, angle=angle,space=space)
    latex_end_table2c(latexfilename)
    latex_end(latexfilename)

def pdffromanalytics(masterfilename,latexfilename):
    # masterfilename="/media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/TESTING_EDEMA_BIOMARKER/COLI_CTSESSIONS.csv"
    filenamefornotanalyzeddata =masterfilename.split('.csv')[0]+'notanalyzedinround1.csv'
    filenamefornotanalyzeddatafigure =masterfilename.split('.csv')[0]+'notanalyzedinround1.png'
    snipr_analytics_result(masterfilename,filenamefornotanalyzeddata,filenamefornotanalyzeddatafigure)
    # import datetime
    # now=datetime.datetime.now()
    # date_time = now.strftime("%m_%d_%Y") #, %H:%M:%S")
    # latexfilename =masterfilename.split('.csv')[0]+'notanalyzedinround1'+date_time+'.tex'
    imagelist=[filenamefornotanalyzeddatafigure]
    makepdfwithimages(latexfilename,imagelist)
def call_pdffromanalytics(args):
    masterfilename=args.stuff[1]
    latexfilename=args.stuff[2]
    pdffromanalytics(masterfilename,latexfilename)


def get_scan_type(sessionId,scanId1):
    # for a given sessionID and scanID
    try:
        this_session_metadata=get_metadata_session(sessionId)
        jsonStr = json.dumps(this_session_metadata)
        df1 = pd.read_json(jsonStr)
        # print("df1::{}".format(df1))
        df1['ID']=df1['ID'].apply(str)
        this_session_metadata_df_scanid=df1[df1['ID'] == str(scanId1)]
        # subprocess.call("echo " + "scanId1type::{}  >> /workingoutput/error.txt".format(str(this_session_metadata_df_scanid)) ,shell=True )
        this_session_metadata_df_scanid.reset_index(drop=True,inplace=True)
        # print("df={}::scanId::{}::this_session_metadata_df_scanid:{}".format(df1,str(scanId1),this_session_metadata_df_scanid.iloc[0]['type'])) #.loc[0,'type']))
        # #
        # # subprocess.call("echo " + "I SUCCEEDED AT ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
        # # subprocess.call("echo " + "scanId1type::{}  >> /workingoutput/error.txt".format(this_session_metadata_df_scanid.at[0,'type']) ,shell=True )
        print("I SUCCEEDED AT ::{}".format(inspect.stack()[0][3]))
        return this_session_metadata_df_scanid.iloc[0]['type']
    except:
        print("I FAILED AT ::{}".format(inspect.stack()[0][3]))

def get_latest_filepath_from_metadata(URI,resource_dir,extension_to_find_list):
    latest_file_path=""
    try:
        metadata=get_resourcefiles_metadata(URI,resource_dir)
        df_listfile = pd.read_json(json.dumps(metadata))
        df_listfile=df_listfile[df_listfile.URI.str.contains(extension_to_find_list)]
        latest_file_df=get_latest_file(df_listfile)
        latest_file_path=str(latest_file_df.at[0,"URI"])
        print("I SUCCEEDED AT ::{}".format(inspect.stack()[0][3]))
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

def scan_selected_flag_slice_num(URI_SCAN,download_dir):

    returnvalue=[0,""]
    try:
        URI_session=URI_SCAN.split('/scans')[0]
        resource_dir="NIFTI_LOCATION"
        # download_files_in_a_resource_withname( sessionId, "NIFTI_LOCATION", download_dir)
        metadata=get_resourcefiles_metadata(URI_session,resource_dir)
        f_listfile = pd.read_json(json.dumps(metadata))
        filenames=[]
        counter=0
        for index1, row in f_listfile.iterrows():
            filename=URI_session.split('/')[3]+"_"+ str(counter)+".csv"
            download_a_singlefile_with_URIString(row['URI'],filename,download_dir)
            filenames.append(filename)
            counter=counter+1
            subprocess.call("echo " + "I filename AT ::{}  >> /workingoutput/error.txt".format(filename) ,shell=True )
        if len(filenames)>0:
            for each_file in filenames:
                subprocess.call("echo " + "I URI_SCAN AT ::{}  >> /workingoutput/error.txt".format(URI_SCAN) ,shell=True )
                each_file_df=pd.read_csv(os.path.join(download_dir,each_file))
                scan_uri_derived=str(each_file_df.at[0,"URI"]).split("/resource")[0]
                if scan_uri_derived==URI_SCAN:
                # URI_SCAN_count=each_file_df.loc[each_file_df["URI"].str.split("/resources").str[0] == URI_SCAN, 'URI'].count()
                # subprocess.call("echo " + "I URI_SCAN AT ::{}  >> /workingoutput/error.txt".format(URI_SCAN) ,shell=True )
                # if URI_SCAN_count == 1 :
                #     subprocess.call("echo " + "I URI_SCAN_count AT ::{}  >> /workingoutput/error.txt".format(URI_SCAN_count) ,shell=True )
                    # URI_SCAN_df=f_listfile[f_listfile['URI']==URI_SCAN]
                    URI_SCAN_SLICE_COUNT=each_file['NUMBEROFSLICES']
                    returnvalue=[1,URI_SCAN_SLICE_COUNT]
                    return  returnvalue #=[1,URI_SCAN_SLICE_COUNT]



        subprocess.call("echo " + "I PASSED AT ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
    except Exception :
        subprocess.call("echo " + "I FAILED AT ::{}::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3],Exception) ,shell=True )
        pass
    return  returnvalue

def get_filepath_withfileext_from_metadata(URI,resource_dir,extension_to_find_list):
    latest_file_path=""
    try:
        metadata=get_resourcefiles_metadata(URI,resource_dir)
        df_listfile = pd.read_json(json.dumps(metadata))
        df_listfile=df_listfile[df_listfile.URI.str.contains(extension_to_find_list)]
        df_listfile=df_listfile.reset_index(drop=True)
        x_df=df_listfile.iloc[0]["URI"]
        # x_df=df_listfile.iloc[[0]]
        latest_file_path=str(x_df) ##get_latest_file(df_listfile)

        print("I SUCCEEDED AT ::{}".format(inspect.stack()[0][3]))
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
def check_available_file_and_document(row_identifier,extension_to_find_list,SCAN_URI,resource_dir,columnname,csvfilename):
    try:
        current_file_path=str(get_latest_filepath_from_metadata(SCAN_URI,resource_dir,extension_to_find_list))
        if len(current_file_path)>1:
            columnvalue=1
            fill_single_datapoint_each_scan(row_identifier,columnname,columnvalue,csvfilename)
        print("I SUCCEEDED AT ::{}".format(inspect.stack()[0][3]))
        subprocess.call("echo " + "I PASSED AT ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )

    except:
        print("I FAILED AT ::{}".format(inspect.stack()[0][3]))
        pass

    return 0
def fill_row_for_csvpdf_files(SCAN_URI,resource_dir,extension_to_find_list,columnname_prefix,csvfilename):
    returnvalue=["",0]
    try:
        _infarct_auto_removesmall_path=str(get_latest_filepath_from_metadata(SCAN_URI,resource_dir,extension_to_find_list))
        if len(_infarct_auto_removesmall_path)>1:
            columnname=columnname_prefix+"_FILE_AVAILABLE"
            columnvalue=1
            fill_single_datapoint_each_scan_1(SCAN_URI,columnname,columnvalue,csvfilename)
            columnname=columnname_prefix+"_FILE_NAME"
            columnvalue=_infarct_auto_removesmall_path
            fill_single_datapoint_each_scan_1(SCAN_URI,columnname,columnvalue,csvfilename)
            returnvalue=[_infarct_auto_removesmall_path,1]
    except:
        pass

    return returnvalue
def fill_row_intermediate_files(SCAN_URI,resource_dir,extension_to_find_list,columnname_prefix,csvfilename,filebasename_flag=0):
    # resource_dir="NIFTI"
    # extension_to_find_list=".nii"
    returnvalue=["",0]
    try:
        _infarct_auto_removesmall_path=get_filepath_withfileext_from_metadata(SCAN_URI,resource_dir,extension_to_find_list)
        if len(_infarct_auto_removesmall_path)>1:
            columnname=columnname_prefix+"_FILE_AVAILABLE"
            columnvalue=1
            fill_single_datapoint_each_scan_1(SCAN_URI,columnname,columnvalue,csvfilename)
            columnname=columnname_prefix+"_FILE_NAME"
            columnvalue=_infarct_auto_removesmall_path
            fill_single_datapoint_each_scan_1(SCAN_URI,columnname,columnvalue,csvfilename)
            if filebasename_flag==1:
                columnname=columnname_prefix+"_BASENAME"
                columnvalue=os.path.basename(_infarct_auto_removesmall_path).split(extension_to_find_list)[0]
                fill_single_datapoint_each_scan_1(SCAN_URI,columnname,columnvalue,csvfilename)

            returnvalue=[_infarct_auto_removesmall_path,1]
    except:
        pass
    return returnvalue
def upload_pdfs(masterfile_scans,X_level,level_name,dir_to_save,resource_dirname_at_snipr):
    try:
        masterfile_scans_df=pd.read_csv(masterfile_scans)
        masterfile_scans_df=masterfile_scans_df[masterfile_scans_df['PDF_FILE_AVAILABLE']==1]
        for index, row in masterfile_scans_df.iterrows():
            if row['PDF_FILE_AVAILABLE']==1:
                url=row["PDF_FILE_NAME"]
                filename=row['SESSION_LABEL'] + "_" + os.path.basename(url)
                try:
                    download_a_singlefile_with_URIString(url,filename,dir_to_save)
                    uploadsinglefile_X_level(X_level,level_name,os.path.join(dir_to_save,filename),resource_dirname_at_snipr)
                except:
                    pass

        print("I SUCCEEDED AT ::{}".format(inspect.stack()[0][3]))
        subprocess.call("echo " + "I PASSED AT ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )

    except:
        print("I FAILED AT ::{}".format(inspect.stack()[0][3]))
        subprocess.call("echo " + "I FAILED AT ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
        pass

    return 0

def combinecsvs_inafiles_list(listofcsvfiles_filename,outputdirectory,outputfilename,session_list):
    try:
        csv_counter=0
        combined_csv_df=""
        session_list_df=pd.read_csv(session_list)
        for each_file in listofcsvfiles_filename:
            try:
                each_file_df=pd.read_csv(each_file)
                each_file_df.at[0,'SESSION_ID']=os.path.basename(each_file).split('_')[0]+"_"+os.path.basename(each_file).split('_')[1]
                this_row_in_session_list_df=session_list_df[session_list_df['ID']==os.path.basename(each_file).split('_')[0]+"_"+os.path.basename(each_file).split('_')[1]]
                this_row_in_session_list_df=this_row_in_session_list_df.reset_index()
                each_file_df.at[0,'SESSION_LABEL']=this_row_in_session_list_df.at[0,'label']
                if csv_counter==0:
                    combined_csv_df=each_file_df
                    csv_counter=csv_counter+1
                else:
                    combined_csv_df=pd.concat([combined_csv_df,each_file_df])
            except:
                pass

        # listofcsvfiles_filename_df=pd.read_csv(listofcsvfiles_filename)
        # listofcsvfiles_filename_df_list=list(listofcsvfiles_filename_df['LOCAL_FILENAME'])
        outputfilepath=os.path.join(outputdirectory,outputfilename)
        # all_filenames = [i for i in listofcsvfiles_filename_df_list]
        # combined_csv=pd.read_csv(all_filenames[0])
        # for x in all_filenames:
        #     try:
        #         combined_csv=pd.concat([combined_csv,pd.read_csv(x)])
        #     except:
        #         pass

        combined_csv_df = combined_csv_df.drop_duplicates()
        combined_csv_df.to_csv(outputfilepath, index=False, encoding='utf-8-sig')

        print("I SUCCEED AT ::{}".format(inspect.stack()[0][3]))
        return 1
    except:
        print("I FAILED AT ::{}".format(inspect.stack()[0][3]))
        pass
        return 0
def download_csvs_combine_upload(masterfile_scans,X_level,level_name,dir_to_save,resource_dirname_at_snipr):
    try:
        masterfile_scans_df=pd.read_csv(masterfile_scans)
        masterfile_scans_df=masterfile_scans_df[masterfile_scans_df['CSV_FILE_AVAILABLE']==1]
        csv_counter=0
        # subprocess.call("echo " + "I PASSED AT ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
        now=datetime.datetime.now()
        date_time = now.strftime("%m_%d_%Y") #, %H:%M:%S")
        combined_file_name=level_name+"_COMBINED_"+date_time+".csv"
        for index, row in masterfile_scans_df.iterrows():

            if row['CSV_FILE_AVAILABLE']==1:

                url=row["CSV_FILE_NAME"]
                filename=row['SESSION_ID'] + "_" + os.path.basename(url)
                try:
                    download_a_singlefile_with_URIString(url,filename,dir_to_save)

                except:
                    subprocess.call("echo " + "I FAILED AT ::{}::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3],Exception) ,shell=True )
                    pass
        # now=datetime.datetime.now()
        # date_time = now.strftime("%m_%d_%Y") #, %H:%M:%S")
        # combined_file_name=os.path.joint(dir_to_save,level_name+"_COMBINED_"+date_time+".csv")
        # combined_df.to_csv(combined_file_name,index=False)
        # uploadsinglefile_X_level(X_level,level_name,combined_file_name,resource_dirname_at_snipr)
        # print("I SUCCEEDED AT ::{}".format(inspect.stack()[0][3]))
        # subprocess.call("echo " + "I PASSED AT ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )

    except Exception:
        print("I FAILED AT ::{}::{}".format(inspect.stack()[0][3],Exception))
        subprocess.call("echo " + "I FAILED AT ::{}::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3],Exception) ,shell=True )
        pass

    return 0
def creat_analytics_scanasID(sessionlist_filename,csvfilename,projectID,output_directory):
    returnvalue=0

    try:
        sessionlist_filename_df=pd.read_csv(sessionlist_filename)
        sessionlist_filename_df=sessionlist_filename_df[sessionlist_filename_df['xsiType']=='xnat:ctSessionData']
        counter=0
        session_counter=0
        for each_session_index, each_session in sessionlist_filename_df.iterrows():
            command="rm " + os.path.dirname(csvfilename) +"/*.pdf"
            subprocess.call(command,shell=True)
            sessionId=each_session['ID']
            if sessionId!= "SNIPR01_E02503":  #SNIPR01_E02470 "SNIPR01_E02503":  #session_counter>1:
                continue
            this_session_metadata=get_metadata_session(sessionId)
            jsonStr = json.dumps(this_session_metadata)
            # print(jsonStr)
            each_session_metadata_df = pd.read_json(jsonStr)
            if session_counter==0:
                each_session_metadata_df.to_csv(csvfilename,index=False)
                session_counter=session_counter+1
            else:
                old_session_metadata_df=pd.read_csv(csvfilename)
                combined_session_medata_data=pd.concat([old_session_metadata_df,each_session_metadata_df],ignore_index=True)
                combined_session_medata_data.to_csv(csvfilename,index=False)


            for each_session_metadata_df_row_index, each_session_metadata_df_row in each_session_metadata_df.iterrows():
                # fill_single_datapoint_each_scan_1(each_session_metadata_df_row["URI"],"columnname","columnvalue",csvfilename)
                fill_single_datapoint_each_scan_1(each_session_metadata_df_row["URI"],"SESSION_LABEL",each_session['label'],csvfilename)
                fill_single_datapoint_each_scan_1(each_session_metadata_df_row["URI"],"SESSION_ID",each_session['ID'],csvfilename)
                SCAN_URI=each_session_metadata_df_row["URI"]
                #####################
                # URI_session=SCAN_URI.split('/scans')[0]

                selection_flag_slic_num=scan_selected_flag_slice_num(SCAN_URI,os.path.dirname(csvfilename))
                subprocess.call("echo " + "selection_flag_slic_num ::{}::{}  >> /workingoutput/error.txt".format(selection_flag_slic_num[0],selection_flag_slic_num[1]) ,shell=True )
                if selection_flag_slic_num[0]==1:
                    fill_single_datapoint_each_scan_1(each_session_metadata_df_row["URI"],"SCAN_SELECTED",selection_flag_slic_num[0],csvfilename)
                    fill_single_datapoint_each_scan_1(each_session_metadata_df_row["URI"],"SLICE_COUNT",selection_flag_slic_num[1],csvfilename)



                #########################

                resource_dir="NIFTI"
                extension_to_find_list=".nii"
                columnname_prefix="NIFTI"
                fill_row_intermediate_files(SCAN_URI,resource_dir,extension_to_find_list,columnname_prefix,csvfilename)
                resource_dir="MASKS"
                extension_to_find_list="_infarct_auto_removesmall.nii.gz"
                columnname_prefix="INFARCT"
                fill_row_intermediate_files(SCAN_URI,resource_dir,extension_to_find_list,columnname_prefix,csvfilename)
                resource_dir="MASKS"
                extension_to_find_list="_csf_unet.nii.gz"
                columnname_prefix="CSF_MASK"
                fill_row_intermediate_files(SCAN_URI,resource_dir,extension_to_find_list,columnname_prefix,csvfilename)
                resource_dir="EDEMA_BIOMARKER"
                extension_to_find_list=".pdf"
                columnname_prefix="PDF"
                r_value=fill_row_for_csvpdf_files(SCAN_URI,resource_dir,extension_to_find_list,columnname_prefix,csvfilename)
                subprocess.call("echo " + "I PASSED AT ::{}:{} >> /workingoutput/error.txt".format(r_value[0],r_value[1]) ,shell=True )
                extension_to_find_list="dropped.csv"
                columnname_prefix="CSV"
                r_value=fill_row_for_csvpdf_files(SCAN_URI,resource_dir,extension_to_find_list,columnname_prefix,csvfilename)
                subprocess.call("echo " + "I PASSED AT ::{}:{} >> /workingoutput/error.txt".format(r_value[0],r_value[1]) ,shell=True )
            session_counter=session_counter+1
            if sessionId== "SNIPR01_E02503": # session_counter>6: #
                break

        now=datetime.datetime.now()
        date_time = now.strftime("%m%d%Y%H%M%S") #, %H:%M:%S")
        csvfilename_new=csvfilename.split('.csv')[0]+"_"+date_time + ".csv"
        csvfilename_df=pd.read_csv(csvfilename)
        csvfilename_df_colnames=csvfilename_df.columns
        for col_name in csvfilename_df_colnames:
            if "_FILE_NAME" in col_name:
                column_to_move = csvfilename_df.pop(col_name)
                csvfilename_df.insert(len(csvfilename_df.columns), col_name, column_to_move)

        csvfilename_df.to_csv(csvfilename_new,index=False)
        csvfilename_withoutfilename=csvfilename.split(".csv")[0]+"_"+date_time+"_NO_FILENAME.csv"
        csvfilename_df=pd.read_csv(csvfilename)
        csvfilename_df_colnames=csvfilename_df.columns
        for col_name in csvfilename_df_colnames:
            if "_FILE_NAME" in col_name:
                column_to_move = csvfilename_df.pop(col_name)
                # csvfilename_df.insert(len(csvfilename_df.columns), col_name, column_to_move)

        csvfilename_df.to_csv(csvfilename_withoutfilename,index=False)
        subprocess.call("echo " + "I PASSED AT ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
        csvfilename_1=csvfilename.split('.csv')[0]+'_'+date_time+'_session.csv'
        create_analytics_file(sessionlist_filename,csvfilename_1)
        X_level="projects"
        level_name=os.path.basename(csvfilename).split('_SNIPER_ANALYTICS.csv')[0]
        dir_to_save=os.path.dirname(csvfilename)
        resource_dirname_at_snipr="EDEMA_BIOMARKER_TEST"
        upload_pdfs(csvfilename,X_level,level_name,dir_to_save,resource_dirname_at_snipr)
        download_csvs_combine_upload(csvfilename,X_level,level_name,output_directory,resource_dirname_at_snipr)

        outputfilename=level_name+ "_"+"COMBINED_EDEMA_BIOMARKER_" + date_time+".csv"

        combinecsvs_inafiles_list(glob.glob(os.path.join(output_directory,"*.csv")),output_directory,outputfilename,sessionlist_filename)
        resource_dirname_at_snipr="SNIPR_ANALYTICS_TEST"
        try:
            uploadsinglefile_X_level(X_level,level_name,csvfilename_new,resource_dirname_at_snipr)
            # uploadsinglefile_X_level(X_level,level_name,csvfilename_1,resource_dirname_at_snipr)
        except:
            pass
        try:
            # uploadsinglefile_X_level(X_level,level_name,csvfilename_new,resource_dirname_at_snipr)
            uploadsinglefile_X_level(X_level,level_name,csvfilename_1,resource_dirname_at_snipr)
        except:
            pass
        try:
            uploadsinglefile_X_level(X_level,level_name,csvfilename_withoutfilename,resource_dirname_at_snipr)
        except:
            pass
        resource_dirname_at_snipr="EDEMA_BIOMARKER_TEST"
        uploadsinglefile_X_level(X_level,level_name,os.path.join(output_directory,outputfilename),resource_dirname_at_snipr)
        returnvalue=1

    except:
        # print("I FAILED AT ::{}".format(inspect.stack()[0][3]))
        # print("I FAILED AT ::{}".format(inspect.stack()[0][3]))
        # subprocess.call("echo " + "latest_file_path::{}  >> /workingoutput/error.txt".format(csvfilename) ,shell=True )
        subprocess.call("echo " + "I FAILED AT ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )

        pass
    return returnvalue

def fill_single_datapoint_each_scan_1(URI,columnname,columnvalue,csvfilename):
    returnvalue=0
    try:
        if os.path.exists(csvfilename):
            # identifier=identifier
            csvfilename_df=pd.read_csv(csvfilename)

            # df_and = csvfilename_df[(csvfilename_df['URI'].str.split("/").str[3]  == session_id) & (csvfilename_df['state'] == scan_id)]
            csvfilename_df.loc[csvfilename_df['URI'] ==URI, columnname] = columnvalue #row['NUMBEROFSLICES']
            csvfilename_df.to_csv(csvfilename,index=False)
            print("I PASSED AT ::{}".format(inspect.stack()[0][3]))
            returnvalue=1
        # print("I SUCCEEDED AT ::{}".format(inspect.stack()[0][3]))
        # subprocess.call("echo " + "latest_file_path::{}  >> /workingoutput/error.txt".format(csvfilename) ,shell=True )
        subprocess.call("echo " + "I PASSED AT ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
        returnvalue=1

    except:
        # print("I FAILED AT ::{}".format(inspect.stack()[0][3]))
        # print("I FAILED AT ::{}".format(inspect.stack()[0][3]))
        # subprocess.call("echo " + "latest_file_path::{}  >> /workingoutput/error.txt".format(csvfilename) ,shell=True )
        subprocess.call("echo " + "I FAILED AT ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )

        pass
    return  returnvalue

def create_analytics_file(sessionlist_filename,csvfilename):
    returnvalue=0
    try:
        sessionlist_filename_df=pd.read_csv(sessionlist_filename)
        sessionlist_filename_df=sessionlist_filename_df[sessionlist_filename_df['xsiType']=='xnat:ctSessionData']
        counter=0

        for index, row in sessionlist_filename_df.iterrows():
            identifier=""
            sessionId= row['ID']
            if sessionId!= "SNIPR01_E02503": # session_counter>6: #
                continue
            command="rm  " + os.path.dirname(csvfilename) + "/*NIFTILOCATION.csv"
            subprocess.call(command,shell=True)
            download_files_in_a_resource_withname( row['ID'], "NIFTI_LOCATION", os.path.dirname(csvfilename))
            counter_nifti_location=0
            niftilocation_files=glob.glob(os.path.join(os.path.dirname(csvfilename) + "/*NIFTILOCATION.csv"))
            infarct_file_num=0
            csf_file_num=0
            pdf_file_num=0
            csv_file_num=0
            fill_single_row_each_session(row['ID'],row['label'],csvfilename)
            for each_niftilocationfile in niftilocation_files:
                print(each_niftilocationfile)
                each_niftilocationfile_df=pd.read_csv(each_niftilocationfile)
                print("each_niftilocationfile_df.iloc[0]['ID']::{}".format(each_niftilocationfile_df.iloc[0]['ID']))
                SCAN_ID=str(each_niftilocationfile_df.iloc[0]['ID'])
                # fill_single_row_each_scan(SCAN_ID,row['ID'],row['label'],csvfilename)
                counter_nifti_location=counter_nifti_location+1
                ### PDF  STEP:
                resource_dir="EDEMA_BIOMARKER"
                extension_to_find_list=".pdf" #_infarct_auto_removesmall.nii.gz"
                SCAN_URI=each_niftilocationfile_df.iloc[0]['URI'].split('/resources')[0]
                _infarct_auto_removesmall_path=str(get_latest_filepath_from_metadata(SCAN_URI,resource_dir,extension_to_find_list))
                # check_available_file_and_document(row_identifier,extension_to_find_list,SCAN_URI,resource_dir,columnname,csvfilename)
                if len(_infarct_auto_removesmall_path)>1:
                    pdf_file_num=pdf_file_num+1
                extension_to_find_list="dropped.csv" #_infarct_auto_removesmall.nii.gz"
                _infarct_auto_removesmall_path=str(get_latest_filepath_from_metadata(SCAN_URI,resource_dir,extension_to_find_list))
                # check_available_file_and_document(row_identifier,extension_to_find_list,SCAN_URI,resource_dir,columnname,csvfilename)
                if len(_infarct_auto_removesmall_path)>1:
                    csv_file_num=csv_file_num+1
                resource_dir="MASKS"
                extension_to_find_list="_infarct_auto_removesmall.nii.gz"
                _infarct_auto_removesmall_path=get_filepath_withfileext_from_metadata(SCAN_URI,resource_dir,extension_to_find_list)
                if len(_infarct_auto_removesmall_path)>1:
                    infarct_file_num=infarct_file_num+1
                extension_to_find_list="_csf_unet.nii.gz"
                _infarct_auto_removesmall_path=get_filepath_withfileext_from_metadata(SCAN_URI,resource_dir,extension_to_find_list)
                if len(_infarct_auto_removesmall_path)>1:
                    csf_file_num=csf_file_num+1


            ### DICOM TO NIFTI STEP
            niftifiles_num=count_niftifiles_insession(row['ID'],os.path.dirname(sessionlist_filename))
            columnname="NUMBER_NIFTIFILES"
            columnvalue=str(niftifiles_num) #str(0)
            fill_datapoint_each_sessionn(row['ID'],columnname,columnvalue,csvfilename)




            axial_thin_count=count_brainaxial_or_thin(row['ID'])
            columnname="AXIAL_SCAN_NUM"
            columnvalue=axial_thin_count[0]
            fill_datapoint_each_sessionn(row['ID'],columnname,columnvalue,csvfilename)
            columnname="THIN_SCAN_NUM"
            columnvalue=axial_thin_count[1]
            fill_datapoint_each_sessionn(row['ID'],columnname,columnvalue,csvfilename)
            columnname="NUMBER_SELECTEDSCANS"
            columnvalue=str(counter_nifti_location) #str(0)

            fill_datapoint_each_sessionn(row['ID'],columnname,columnvalue,csvfilename)

            columnname="INFARCT_FILE_NUM"
            columnvalue=infarct_file_num #axial_thin_count[1]
            fill_datapoint_each_sessionn(row['ID'],columnname,columnvalue,csvfilename)
            columnname="CSF_FILE_NUM"
            columnvalue=csf_file_num #axial_thin_count[1]
            fill_datapoint_each_sessionn(row['ID'],columnname,columnvalue,csvfilename)
            columnname="PDF_FILE_NUM"
            columnvalue=pdf_file_num #axial_thin_count[1]
            fill_datapoint_each_sessionn(row['ID'],columnname,columnvalue,csvfilename)
            columnname="CSV_FILE_NUM"
            columnvalue=csv_file_num #axial_thin_count[1]
            fill_datapoint_each_sessionn(row['ID'],columnname,columnvalue,csvfilename)
            ### SEGMENTATION STEP

            counter=counter+1
            if sessionId== "SNIPR01_E02503": # session_counter>6: #
                break
            # if counter > 6:
            #     break

        # print(sessionlist_filename_df)
        print("I SUCCEEDED AT ::{}".format(inspect.stack()[0][3]))
        returnvalue=1
    except:
        print("I FAILED AT ::{}".format(inspect.stack()[0][3]))
        pass
    return returnvalue
def call_create_analytics_file(args):
    returnvalue=0
    try:
        sessionlist_filename=args.stuff[1]
        csvfilename=args.stuff[2]
        create_analytics_file(sessionlist_filename,csvfilename)
        print("I SUCCEEDED AT ::{}".format(inspect.stack()[0][3]))
        returnvalue=1
    except:
        print("I FAILED AT ::{}".format(inspect.stack()[0][3]))
        pass
    return returnvalue

def call_creat_analytics_scanasID(args):
    returnvalue=0
    try:
        sessionlist_filename=args.stuff[1]
        csvfilename=args.stuff[2]
        projectID=args.stuff[3]
        output_directory=args.stuff[4]
        creat_analytics_scanasID(sessionlist_filename,csvfilename,projectID,output_directory)
        print("I SUCCEEDED AT ::{}".format(inspect.stack()[0][3]))
        returnvalue=1
    except:
        print("I FAILED AT ::{}".format(inspect.stack()[0][3]))
        pass
    return returnvalue
def fill_single_datapoint_each_scan(identifier,columnname,columnvalue,csvfilename):
    returnvalue=0
    try:
        if os.path.exists(csvfilename):
            identifier=identifier
            # scan_type=get_single_value_from_metadata_forascan(columnvalue,str(identifier),'type')
            # scan_description=get_single_value_from_metadata_forascan(columnvalue,str(identifier),'series_description')
            # this_scan_dict={"ROW_IDENTIFIER":columnvalue+"_"+str(identifier),"SESSION_ID":columnvalue,"SESSION_LABEL":columnvalue2, "SCAN_ID":str(identifier)} #,"SCAN_TYPE":scan_type,"scan_description":scan_description}
            # this_scan_dict_df=pd.DataFrame([this_scan_dict])
            # print(this_scan_dict)
            csvfilename_df=pd.read_csv(csvfilename)
            # csvfilename_df_this_row=csvfilename_df[csvfilename_df['ROW_IDENTIFIER']==identifier]
            csvfilename_df_colname=csvfilename_df.columns
            csvfilename_df.loc[csvfilename_df['ROW_IDENTIFIER'] ==identifier, columnname] = columnvalue #row['NUMBEROFSLICES']
            # if columnname not in csvfilename_df_colname:
            #     csvfilename_df[columnname]=""
            # csvfilename_df.loc['ROW_IDENTIFIER',columnname]=columnvalue #.loc[:, ('one', 'second')]
            # csvfilename_df  = pd.concat([csvfilename_df,this_scan_dict_df],ignore_index=True)
            csvfilename_df.to_csv(csvfilename,index=False)
            # # this_scan_dict={"SCAN_ID":identifier,columnname:columnvalue}
            # last_row_index=csvfilename_df['ROW_IDENTIFIER'].iget(-1)
            # csvfilename_df.at[last_row_index+1,
            print("I PASSED AT ::{}".format(inspect.stack()[0][3]))
        else:
            columnvalue_flag=0
            # identifier=identifier
            # if len(columnvalue)>3:
            #     columnvalue_flag=1
            # scan_type=get_single_value_from_metadata_forascan(columnvalue,str(identifier),'type')
            # scan_description=get_single_value_from_metadata_forascan(columnvalue,str(identifier),'series_description')
            # first_dict={"ROW_IDENTIFIER":columnvalue+"_"+str(identifier),"SESSION_ID":columnvalue,"SESSION_LABEL":columnvalue2, "SCAN_ID":str(identifier)} #,"SCAN_TYPE":scan_type,"scan_description":scan_description}
            # print(first_dict)
            # first_dict_df=pd.DataFrame([first_dict])
            # first_dict_df.to_csv(csvfilename,index=False)

            print("I PASSED AT ::{}".format(inspect.stack()[0][3]))
    except:
        print("I FAILED AT ::{}".format(inspect.stack()[0][3]))
        pass
    return  returnvalue

def fill_datapoint_each_sessionn(identifier,columnname,columnvalue,csvfilename):
    returnvalue=0
    try:
        if os.path.exists(csvfilename):
            identifier=identifier
            # scan_type=get_single_value_from_metadata_forascan(columnvalue,str(identifier),'type')
            # scan_description=get_single_value_from_metadata_forascan(columnvalue,str(identifier),'series_description')
            # this_scan_dict={"ROW_IDENTIFIER":columnvalue+"_"+str(identifier),"SESSION_ID":columnvalue,"SESSION_LABEL":columnvalue2, "SCAN_ID":str(identifier)} #,"SCAN_TYPE":scan_type,"scan_description":scan_description}
            # this_scan_dict_df=pd.DataFrame([this_scan_dict])
            # print(this_scan_dict)
            csvfilename_df=pd.read_csv(csvfilename)
            # csvfilename_df_this_row=csvfilename_df[csvfilename_df['ROW_IDENTIFIER']==identifier]
            csvfilename_df_colname=csvfilename_df.columns
            csvfilename_df.loc[csvfilename_df['SESSION_ID'] ==identifier, columnname] = columnvalue #row['NUMBEROFSLICES']
            # if columnname not in csvfilename_df_colname:
            #     csvfilename_df[columnname]=""
            # csvfilename_df.loc['SESSION_ID',columnname]=columnvalue #.loc[:, ('one', 'second')]
            # csvfilename_df  = pd.concat([csvfilename_df,this_scan_dict_df],ignore_index=True)
            csvfilename_df.to_csv(csvfilename,index=False)
            # # this_scan_dict={"SCAN_ID":identifier,columnname:columnvalue}
            # last_row_index=csvfilename_df['ROW_IDENTIFIER'].iget(-1)
            # csvfilename_df.at[last_row_index+1,
            print("I PASSED AT ::{}".format(inspect.stack()[0][3]))
        else:
            columnvalue_flag=0
            # identifier=identifier
            # if len(columnvalue)>3:
            #     columnvalue_flag=1
            # scan_type=get_single_value_from_metadata_forascan(columnvalue,str(identifier),'type')
            # scan_description=get_single_value_from_metadata_forascan(columnvalue,str(identifier),'series_description')
            # first_dict={"ROW_IDENTIFIER":columnvalue+"_"+str(identifier),"SESSION_ID":columnvalue,"SESSION_LABEL":columnvalue2, "SCAN_ID":str(identifier)} #,"SCAN_TYPE":scan_type,"scan_description":scan_description}
            # print(first_dict)
            # first_dict_df=pd.DataFrame([first_dict])
            # first_dict_df.to_csv(csvfilename,index=False)

            print("I PASSED AT ::{}".format(inspect.stack()[0][3]))
    except:
        print("I FAILED AT ::{}".format(inspect.stack()[0][3]))
        pass
    return  returnvalue
def fill_single_row_each_session(columnvalue,columnvalue2,csvfilename):
    #first example: identifier: scan_id= SESSION_ID+SCAN_ID columnname=NIFTIFILE_NAME columnvalue=NIFTIFILENAME_VALUE columnvalue_flag= 0 or 1
    returnvalue=0
    try:
        if os.path.exists(csvfilename):
            # identifier=identifier
            # scan_type=get_single_value_from_metadata_forascan(columnvalue,str(identifier),'type')
            # scan_description=get_single_value_from_metadata_forascan(columnvalue,str(identifier),'series_description')
            this_scan_dict={"SESSION_ID":columnvalue,"SESSION_LABEL":columnvalue2} #,"SCAN_TYPE":scan_type,"scan_description":scan_description}
            this_scan_dict_df=pd.DataFrame([this_scan_dict])
            print(this_scan_dict)
            csvfilename_df=pd.read_csv(csvfilename)
            csvfilename_df  = pd.concat([csvfilename_df,this_scan_dict_df],ignore_index=True)
            csvfilename_df.to_csv(csvfilename,index=False)
            # # this_scan_dict={"SCAN_ID":identifier,columnname:columnvalue}
            # last_row_index=csvfilename_df['ROW_IDENTIFIER'].iget(-1)
            # csvfilename_df.at[last_row_index+1,
        else:
            columnvalue_flag=0
            # identifier=identifier
            if len(columnvalue)>3:
                columnvalue_flag=1
            # scan_type=get_single_value_from_metadata_forascan(columnvalue,str(identifier),'type')
            # scan_description=get_single_value_from_metadata_forascan(columnvalue,str(identifier),'series_description')
            first_dict={"SESSION_ID":columnvalue,"SESSION_LABEL":columnvalue2} #,"SCAN_TYPE":scan_type,"scan_description":scan_description}
            print(first_dict)
            first_dict_df=pd.DataFrame([first_dict])
            first_dict_df.to_csv(csvfilename,index=False)

            print("I PASSED AT ::{}".format(inspect.stack()[0][3]))
    except:
        print("I FAILED AT ::{}".format(inspect.stack()[0][3]))
        pass
    return  returnvalue
def fill_single_row_each_scan(identifier,columnvalue,columnvalue2,csvfilename):
    #first example: identifier: scan_id= SESSION_ID+SCAN_ID columnname=NIFTIFILE_NAME columnvalue=NIFTIFILENAME_VALUE columnvalue_flag= 0 or 1
    returnvalue=0
    try:
        if os.path.exists(csvfilename):
            identifier=identifier
            # scan_type=get_single_value_from_metadata_forascan(columnvalue,str(identifier),'type')
            # scan_description=get_single_value_from_metadata_forascan(columnvalue,str(identifier),'series_description')
            this_scan_dict={"ROW_IDENTIFIER":columnvalue+"_"+str(identifier),"SESSION_ID":columnvalue,"SESSION_LABEL":columnvalue2, "SCAN_ID":str(identifier)} #,"SCAN_TYPE":scan_type,"scan_description":scan_description}
            this_scan_dict_df=pd.DataFrame([this_scan_dict])
            print(this_scan_dict)
            csvfilename_df=pd.read_csv(csvfilename)
            csvfilename_df  = pd.concat([csvfilename_df,this_scan_dict_df],ignore_index=True)
            csvfilename_df.to_csv(csvfilename,index=False)
            # # this_scan_dict={"SCAN_ID":identifier,columnname:columnvalue}
            # last_row_index=csvfilename_df['ROW_IDENTIFIER'].iget(-1)
            # csvfilename_df.at[last_row_index+1,
        else:
            columnvalue_flag=0
            identifier=identifier
            if len(columnvalue)>3:
                columnvalue_flag=1
            scan_type=get_single_value_from_metadata_forascan(columnvalue,str(identifier),'type')
            scan_description=get_single_value_from_metadata_forascan(columnvalue,str(identifier),'series_description')
            first_dict={"ROW_IDENTIFIER":columnvalue+"_"+str(identifier),"SESSION_ID":columnvalue,"SESSION_LABEL":columnvalue2, "SCAN_ID":str(identifier)} #,"SCAN_TYPE":scan_type,"scan_description":scan_description}
            print(first_dict)
            first_dict_df=pd.DataFrame([first_dict])
            first_dict_df.to_csv(csvfilename,index=False)

            print("I PASSED AT ::{}::{}".format(inspect.stack()[0][3],scan_type))
    except:
        print("I FAILED AT ::{}".format(inspect.stack()[0][3]))
        pass
    return  returnvalue
def call_fill_single_row_each_scan(args):

    returnvalue=0
    # print("I AM AT ::{}".format(inspect.stack()[0][3]))
    try:
        identifier=args.stuff[1]
        # columnname=args.stuff[2]
        columnvalue=args.stuff[2]
        columnvalue2=args.stuff[3]
        csvfilename=args.stuff[4]
        fill_single_row_each_scan(identifier,columnvalue,columnvalue2,csvfilename)
        print("I PASSED AT ::{}".format(inspect.stack()[0][3]))
    except:
        print("I FAILED AT ::{}".format(inspect.stack()[0][3]))
        pass
    return  returnvalue


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stuff', nargs='+')
    args = parser.parse_args()
    name_of_the_function=args.stuff[0]
    return_value=0
    if name_of_the_function == "call_pdffromanalytics":
        return_value=call_pdffromanalytics(args)
        
    if name_of_the_function == "call_fill_single_row_each_scan":
        print(" calling call_fill_single_row_each_scan")
        return_value=call_fill_single_row_each_scan(args)

    if name_of_the_function == "call_create_analytics_file":
        print(" calling call_create_analytics_file")
        return_value=call_create_analytics_file(args)
    if name_of_the_function=="call_creat_analytics_scanasID":
        return_value=call_creat_analytics_scanasID(args)


if __name__ == '__main__':
    main()


# In[ ]:





# In[ ]:





# In[ ]:





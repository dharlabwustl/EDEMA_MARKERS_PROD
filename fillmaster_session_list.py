#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os,sys,glob
def get_latest_csvfile_singlefilename(df1,extens='.csv'):
    ## get all the rows with csv in the name:
    allfileswithprefix1_df = df1[df1['Name'].str.contains(extens)]
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
        # sessioncsv_df.loc[sessioncsv_df['ID'] ==xx[3], filename_available] = 1 ##df1['URI'][0]
        
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
                    elif '_normalized_class1.nii.gz' in row['Name']:
                        filename='ICHFILENAME'
                        filename_available='ICHFILE_AVAILABLE'
                    elif '_normalized_class2.nii.gz' in row['Name']:
                        filename='ICHEDEMAFILENAME'
                        filename_available='ICHEDEMAFILE_AVAILABLE'
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

        try:
            df1 = pd.read_csv(x) #, delim_whitespace=False)



            for index, row in df1.iterrows():
                            # get file extension:
                extens=row['Name'].split('.')
                if 'nii' in extens[-1]: 

                    filename='NIFTIFILENAME'
                    filename_available='NIFTIFILE_AVAILABLE'    
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
#     insertniftifilename(dir_csv)


# In[5]:


def insertedemabiomarkerfilename(sessioncsv_df,dir_csv):
    for x in glob.glob(os.path.join(dir_csv,"*EDEMA_BIOMARKER.csv")):
            # if 'sessions.csv' != os.path.basename(x):

            try:
                df1 = pd.read_csv(x) #, delim_whitespace=False)
                csvfile=get_latest_csvfile_singlefilename(df1,'.csv')
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
    sessioncsv_df=pd.read_csv(os.path.join(dir_csv,session_csvfile))
    sessioncsv_df=insertniftifilename(sessioncsv_df,dir_csv)
    sessioncsv_df=insertmaskfilesname(sessioncsv_df,dir_csv)
    # if "ICH" in typeofmask:
    sessioncsv_df=insertichquantificationfilename(sessioncsv_df,dir_csv)
    # if "INFARCT" in typeofmask: 
    sessioncsv_df=insertedemabiomarkerfilename(sessioncsv_df,dir_csv)
    sessioncsv_df=sessioncsv_df[sessioncsv_df['xsiType']=='xnat:ctSessionData']
    sessioncsv_df.to_csv(os.path.join(directorytosave,filenametosave),index=False)

    
    
def call_insertavailablefilenames():
    session_csvfile=sys.argv[1]
    dir_csv=sys.argv[2]
    # typeofmask=sys.argv[3]
    filenametosave=sys.argv[3]
    directorytosave=sys.argv[4]
    insertavailablefilenames(session_csvfile,dir_csv,filenametosave,directorytosave)


# In[ ]:





# In[ ]:





# In[ ]:





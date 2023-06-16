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
        print(" I AM AT::{}".format(inspect.stack()[0][3]))
        try:
            df1 = pd.read_csv(x) #, delim_whitespace=False)



            for index, row in df1.iterrows():
                            # get file extension:
                extens=row['Name'].split('.')
                if 'nii' in extens[-1] or 'nii' in 'nii' in extens[-2]:

                    filename='NIFTIFILENAME'
                    filename_available='NIFTIFILE_AVAILABLE'    
                # elif 'csv' in extens[-1]:


                xx=row['URI'].split('/') #.str.split('/', expand=True)
                sessionId=xx[3]
                scanId=xx[5]
                # print("sessionId::{} and scanId::{}".format(sessionId,scanId))
                scan_type="AA" #get_scan_type(sessionId,scanId)

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
        # sessioncsv_df=insertmaskfilesname(sessioncsv_df,dir_csv)
        # # if "ICH" in typeofmask:
        # sessioncsv_df=insertichquantificationfilename(sessioncsv_df,dir_csv)
        # # if "INFARCT" in typeofmask:
        # sessioncsv_df=insertedemabiomarkerfilename(sessioncsv_df,dir_csv)

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
    subprocess.call("echo I SUCCEEDED AT ::{}  > /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
    insertavailablefilenames(session_csvfile,dir_csv,filenametosave,directorytosave)
    masterfilename=os.path.join(directorytosave,filenametosave)
    # pdffromanalytics(masterfilename,latexfilename)

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
    df2 = df2.drop('LEVELSETFILE_AVAILABLE', axis=1)
    print(df2)
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
        print("scanId1type::{}".format(type(scanId1)))
        this_session_metadata_df_scanid=pd.DataFrame(df1.loc[df1['ID'] == int(scanId1)])
        # this_session_metadata_df_scanid.reset_index(inplace=True)
        # print("df={}::scanId::{}::this_session_metadata_df_scanid:{}".format(df1['ID'],scanId1,this_session_metadata_df_scanid.loc[0,'type']))
        print("I SUCCEEDED AT ::{}".format(inspect.stack()[0][3]))
        subprocess.call("echo I SUCCEEDED AT ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
    except:
        print("I FAILED AT ::{}".format(inspect.stack()[0][3]))




    return this_session_metadata_df_scanid.loc[0,'type']
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stuff', nargs='+')
    args = parser.parse_args()
    name_of_the_function=args.stuff[0]
    return_value=0
    if name_of_the_function == "call_pdffromanalytics":
        return_value=call_pdffromanalytics(args)


if __name__ == '__main__':
    main()


# In[ ]:





# In[ ]:





# In[ ]:





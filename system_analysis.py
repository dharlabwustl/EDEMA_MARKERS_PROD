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
def bar_chart_a_table(args):
    csvfilename=args.stuff[1]
    output_image_name=args.stuff[2]
    csvfilename_df=pd.read_csv(csvfilename)
    csvfilename_df.columns=csvfilename_df.columns.str.strip() #(' ','')
    csvfilename_df.columns=csvfilename_df.columns.str.replace('_',' ')
    # csvfilename_df.replace(np.nan,0)
    ax = csvfilename_df.plot.bar(x=list(csvfilename_df.columns)[0],rot=0)
    ax.legend(fontsize=5, loc="upper right") #,width=3) #figsize=(3,5),
    ax.set_ylabel("COUNT")
    for p in ax.patches:
        if p.get_height()>0:
            ax.annotate(str(int(p.get_height())), (p.get_x() * 1.005, p.get_height() * 1.005), fontsize=5,rotation=90)
    fig = ax.get_figure()

    fig.savefig(output_image_name)
def remove_space_in_col_name(args):
    csvfilename=args.stuff[1]
    outputfilename=args.stuff[2]
    csvfilename_df=pd.read_csv(csvfilename)
    csvfilename_df.columns=csvfilename_df.columns.str.strip() #(' ','')
    csvfilename_df.columns=csvfilename_df.columns.str.replace('_',' ')
    csvfilename_df.to_csv(outputfilename,index=False)

def combinecsvs_with_a_given_suffix(args):
    inputdirectory=args.stuff[1]
    outputfilename=args.stuff[2]
    suffix=args.stuff[3]
    f = [i for i in glob.glob(os.path.join(inputdirectory,'*{}'.format(suffix)))]
    # f=glob.glob("workinginput/*count.csv")
    merged_df=pd.read_csv(f[0])
    for x in range(len(f)):
        df=pd.read_csv(f[x])
        if df[list(df.columns)[0]][0] in list(merged_df[list(merged_df.columns)[0]]):
            merged_df.loc[merged_df[list(merged_df.columns)[0]]==df[list(df.columns)[0]][0], list(df.columns)[1]] = df[list(df.columns)[1]][0]
        else:
            merged_df=pd.concat([merged_df,df ], ignore_index=True)
    combined_csv = merged_df.drop_duplicates()
    combined_csv.replace(np.nan, '')

    combined_csv.to_csv(outputfilename, index=False, encoding='utf-8-sig')
def sum_columns(args):
    csvfilename=args.stuff[1]
    outputfilename=args.stuff[2]
    combined_csv = pd.read_csv(csvfilename) #merged_df.drop_duplicates()
    combined_csv['COMBINED']=combined_csv.sum(axis=1)
    combined_csv.to_csv(outputfilename, index=True, encoding='utf-8-sig')

def transpose_a_table(args):
    csvfilename=args.stuff[1]
    outputfilename=args.stuff[2]
    combined_csv = pd.read_csv(csvfilename) #merged_df.drop_duplicates()
    combined_csv.columns=combined_csv.columns.str.replace('_TOTAL','')
    column_names=combined_csv.columns
    combined_csv.set_index=list(combined_csv[list(combined_csv.columns)[0]])
    combined_csv=combined_csv.T
    combined_csv.set_index=list(column_names)
    combined_csv.columns = combined_csv.iloc[0]
    combined_csv['COMBINED']=combined_csv.sum(axis=1)
    combined_csv = combined_csv[1:]
    combined_csv.index.name = 'DATA TYPE'
    #export to csv
    combined_csv.replace(np.nan, '')

    combined_csv.to_csv(outputfilename, index=True, encoding='utf-8-sig')
def rename_one_column(args):
    csvfilename=args.stuff[1]
    columnname=args.stuff[2]
    new_name=args.stuff[3]
    csvfilename_edited=args.stuff[4]
    csvfilename_df=pd.read_csv(csvfilename)
    if columnname in csvfilename_df.columns:
        csvfilename_df.rename(columns={columnname:new_name}, inplace=True)
    csvfilename_df.to_csv(csvfilename_edited,index=False)
def count_a_column(args):
    csvfile_analysis=args.stuff[1]
    column_to_be_counted_in_analysis=args.stuff[2]
    cohort_name=args.stuff[3]
    # csvfile_results=args.stuff[3]
    # column_to_be_counted_in_result=args.stuff[4]
    outputcsvfilename=args.stuff[4]
    # csvfile_results_df=pd.read_csv(csvfile_results)
    csvfile_analysis_df=pd.read_csv(csvfile_analysis)
    csvfile_analysis_df.columns=csvfile_analysis_df.columns.str.strip() #(' ','')
    csvfile_analysis_df.columns=csvfile_analysis_df.columns.str.replace(' ','_')
    columname_value_count_df = pd.DataFrame()
    columname_value_count_df['COHORT_NAME'] = [cohort_name]
    columname_value_count_df[str(column_to_be_counted_in_analysis)] = [csvfile_analysis_df[str(column_to_be_counted_in_analysis)].notnull().sum()]
    # columname_value_count_df=pd.DataFrame([[cohort_name],[csvfile_analysis_df[str(column_to_be_counted_in_analysis)].notnull().sum()]])
    # columname_value_count_df.columns=['COHORT_NAME',str(column_to_be_counted_in_analysis)+'_COUNT']
    # sess_result_count_df=pd.DataFrame([csvfile_analysis_df[str(column_to_be_counted_in_analysis)].notnull().sum(),csvfile_results_df[str(column_to_be_counted_in_result)].notnull().sum()])
    # sess_result_count_df.columns=['SESSIONS_COUNT','RESULTS_COUNT']
    # columname_value_count_df.columns=columname_value_count_df.columns.str.replace('_COUNT','')
    columname_value_count_df.to_csv(outputcsvfilename,index=False)

def non_numerical_val_counter(args):

    try:
        csvfilename_input=args.stuff[1]
        column_to_be_counted=args.stuff[2]
        identifier_column_name_inoutput=args.stuff[3]
        identifier_column_value_inoutput=args.stuff[4]
        column_name=args.stuff[5]
        csvfilename_output=args.stuff[6]
        csvfilename_df=pd.read_csv(csvfilename_input)
        # csvfilename_df.columns=csvfilename_df.columns.str.strip() #(' ','')
        # csvfilename_df.columns=csvfilename_df.columns.str.replace(' ','_')
        # csvfilename_df[str(column_to_be_counted)]=pd.to_numeric(csvfilename_df[str(column_to_be_counted)],errors='coerce')
        csvfilename_output_df=pd.read_csv(csvfilename_output)
        column_value=csvfilename_df[str(column_to_be_counted)].notnull().sum() #[csvfilename_df[str(column_to_be_counted)]>=np.min(column_to_be_counted)]
        this_scan_dict={str(identifier_column_name_inoutput):str(identifier_column_value_inoutput),column_name:column_value} #+"_"+str(identifier),"SESSION_ID":columnvalue,"SESSION_LABEL":columnvalue2, "SCAN_ID":str(identifier)} #,"SCAN_TYPE":scan_type,"scan_description":scan_description}
        this_scan_dict_df=pd.DataFrame([this_scan_dict])
        csvfilename_output_df  = pd.concat([csvfilename_output_df,this_scan_dict_df],ignore_index=True)
        csvfilename_output_df.to_csv(csvfilename_output,index=False)
        subprocess.call("echo " + "passed at expression::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
    except:
        subprocess.call("echo " + "failed at expression::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
        pass
    return "I WORKED"
def combinecsvsfiles_from_a_csv_containing_its_list(args): #listofcsvfiles_filename,outputfilename):
    try:
        listofcsvfiles_filename=args.stuff[1]
        outputfilename=args.stuff[2]
        csv_counter=0
        combined_csv_df=""
        listofcsvfiles_filename_df=pd.read_csv(listofcsvfiles_filename)
        colname=list(listofcsvfiles_filename_df.columns)[0]
        # masterfile_scans_df=masterfile_scans_df[masterfile_scans_df[column_name_for_url].str.contains(file_extension)] #df["name"].str.contains("Honda")
        for index, row in listofcsvfiles_filename_df.iterrows():
        # for each_file in listofcsvfiles_filename:
            try:
                each_file=row[colname]
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
# def get_count_of_each_project_column(args):
#     csvfilename_result=args.stuff[1]
#     csvfilename_analytics=args.stuff[2]
#     column_names=args.stuff[4:]
#     csvfilename_output=args.stuff[3]
#     # column_name=args.stuff[2]
#     df=pd.read_csv(csvfilename_result)
#     df_output
#     df=df[df[str(column_name)]>=df[str(column_name)].min()]
#     df.to_csv(csvfilename_output,index=False)

# def save_column_names_ofacsvfile():
#     f2 = df1.copy()
#     with pd.ExcelWriter('output.xlsx') as writer:
#         df1.to_excel(writer, sheet_name='Sheet_name_1')
#         df2.to_excel(writer, sheet_name='Sheet_name_2')
def histogram_column_ina_csvfile(args):
    try:
        csvfilename=args.stuff[1]
        column_name=args.stuff[2]
        output_image_name=args.stuff[3]
        df=pd.read_csv(csvfilename)
        df.columns=df.columns.str.strip() #(' ','')
        df.columns=df.columns.str.replace(' ','_')

        # df[str(column_name)]=pd.to_numeric(df[str(column_name)], errors='coerce')
        # df=df[pd.to_numeric(df[str(column_name)], errors='coerce').notnull()]
        df[str(column_name)]=pd.to_numeric(df[str(column_name)],errors='coerce')

        # df[str(column_name)] = df[str(column_name)].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(float)
        # if "SAH" in column_name:
        #     df=df[df[str(column_name)]<=100]
        if "ICH" in column_name:
            # ax.set_xlim([0,100])
            df=df[df[str(column_name)]<=100]
        non_zero_items=df[df[str(column_name)]>=df[str(column_name)].min()]
        non_zero_items.to_csv(csvfilename.split('.csv')[0]+'_hist.csv')
        # if "CSF_RATIO" in column_name:
        # #     df=df[df[str(column_name)]<=1]
        #     non_zero_items=non_zero_items[non_zero_items[str(column_name)]<=1.0]
        ##################
        df=df.set_index(list(df.columns)[0]).T
        # ax = df.set_index('name').T.plot.bar(alpha=.7, rot=0, stacked=True)
        ax = df[str(column_name)].plot.hist(bins=12, alpha=0.5,color = "blueviolet", lw=0)
        # # ax = df.hist(column=column_name, bins=25, grid=False, figsize=(12,8), color='#86bf91', zorder=2, rwidth=0.9)
        # # ax = s.hist()  # s is an instance of Series
        ax.set_xlabel(str(column_name).replace("_"," "))
        if "VOLUME" in column_name or "TOTAL" in column_name:
            ax.set_xlabel(str(column_name).replace("_"," ")+'(ml)')

        ax.set_ylabel("COUNT"+"  (TOTAL: " +str(non_zero_items.shape[0]) + ")")

        # y_lim=ax.get_ylim()
        # x_lim=ax.get_xlim()
        # ax.text(int(x_lim[0]+x_lim[0]*.10),int(y_lim[1]-y_lim[1]*0.10),"TOTAL COUNT: " +str(non_zero_items.shape[0]))
        fig = ax.get_figure()

        fig.savefig(output_image_name)

        print("I SUCCEEDED AT ::{}".format(inspect.stack()[0][3]))
        subprocess.call("echo " + "I PASSED AT ::{} >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )

    except:
        print("I FAILED AT ::{}".format(inspect.stack()[0][3]))
        subprocess.call("echo " + "I FAILED AT ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
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
def get_latest_filepath_from_metadata_for_analytics(args):
    URI=args.stuff[1]
    resource_dir=args.stuff[2]
    extension_to_find_list=args.stuff[3]
    SCAN_URI_NIFTI_FILEPREFIX=args.stuff[4]
    file_location_csv=args.stuff[5]
    latest_file_path=""
    try:
        metadata=get_resourcefiles_metadata(URI,resource_dir)
        df_listfile = pd.read_json(json.dumps(metadata))
        df_listfile.to_csv(os.path.join(os.path.dirname(file_location_csv),"test.csv"),index=False)
        df_listfile=df_listfile[df_listfile.URI.str.contains(extension_to_find_list)]
        if len(SCAN_URI_NIFTI_FILEPREFIX)>0:
            df_listfile=df_listfile[df_listfile.URI.str.contains(SCAN_URI_NIFTI_FILEPREFIX)]
        latest_file_df=get_latest_file_for_analytics(df_listfile) #,SCAN_URI_NIFTI_FILEPREFIX)
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
        df_listfile.to_csv(os.path.join(os.path.dirname(file_location_csv),"test.csv"),index=False)
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
        # df=pd.DataFrame([1])
        columns=['COHORT_NAME','SESSION_COUNT','RESULTS_COUNT']
        df = pd.DataFrame(columns=columns)
        # df.columns=['TOREMOVE']
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





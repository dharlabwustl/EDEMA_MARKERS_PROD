#!/usr/bin/python

import os, sys, errno, shutil, uuid,subprocess,csv,json
import math,inspect
import glob
import re,time
import requests
import pandas as pd
import nibabel as nib
import numpy as np
# import pydicom as dicom
import pathlib
import argparse,xmltodict
from xnatSession import XnatSession
# from biomarker_db_module import BiomarkerDB
from biomarkerdbclass import  BiomarkerDB
from redcapapi_functions import *
catalogXmlRegex = re.compile(r'.*\.xml$')
XNAT_HOST_URL=os.environ['XNAT_HOST']  #'http://snipr02.nrg.wustl.edu:8080' #'https://snipr02.nrg.wustl.edu' #'https://snipr.wustl.edu'
XNAT_HOST = XNAT_HOST_URL # os.environ['XNAT_HOST'] #
XNAT_USER = os.environ['XNAT_USER']#
XNAT_PASS =os.environ['XNAT_PASS'] #
api_token=os.environ['REDCAP_API']
xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
xnatSession.renew_httpsession()
class arguments:
    def __init__(self,stuff=[]):
        self.stuff=stuff 
def fill_redcap_pdffilename(project_name,session_label,pdf_file_name):
  try:
        this_project_redcapfile_latest=project_name+'_latest.csv'
        # api_token='EC6A2206FF8C1D87D4035E61C99290FF'
        df_scan_latest=download_latest_redcapfile(api_token,this_project_redcapfile_latest)
        this_session_redcap_repeat_instance_df=df_scan_latest[df_scan_latest['snipr_session']==session_label]
        this_session_redcap_repeat_instance=str(this_session_redcap_repeat_instance_df['redcap_repeat_instance'].item())
        imaging_data_complete=str(this_session_redcap_repeat_instance_df['imaging_data_complete'].item())
        if imaging_data_complete != '2':
            add_one_file_to_redcap(subject_name,'imaging_data',this_session_redcap_repeat_instance,str('session_pdf'),pdf_file_name)
    except:
        subprocess.call("echo " + "I FAILED AT ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
        pass
       
def call_pdf_fill_for_each_row(args):
    project_name=args.stuff[1]
    csvfilename=args.stuff[2] ##  xmlfile=args.stuff[1]
    output_dirname=args.stuff[3]
    # for each snipr_session, get the PDF_FILE_PATH and download it.
    # call fill_redcap_pdffilename(project_name,snipr_session,PDF_FILE_PATH)
    df = pd.read_csv(csvfilename) 
    for _, row in df.iterrows():
      print(f"PDF_FILE_PATH: {row['PDF_FILE_PATH']}, snipr_session: {row['snipr_session']}")
      # download_a_singlefile_with_URIString(row['PDF_FILE_PATH'],os.path.basename(row['PDF_FILE_PATH']),output_dirname)
      # fill_redcap_pdffilename(project_name,row['snipr_session'],os.path.join(ouput_dirname,os.path.basename(row['PDF_FILE_PATH'])))

  

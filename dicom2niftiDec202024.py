#!/usr/bin/python

import os, sys, errno, shutil, uuid,subprocess
import math
import glob
import re,time
import requests
import pydicom as dicom
import pandas as pd
import json
from xnatSession import XnatSession
from download_with_session_ID import *;
import nibabel as nib
import DecompressDCM
# import label_probability

catalogXmlRegex = re.compile(r'.*\.xml$')
XNAT_HOST_URL='https://snipr.wustl.edu'
XNAT_HOST = os.environ['XNAT_HOST'] #XNAT_HOST_URL #
XNAT_USER =os.environ['XNAT_USER']
XNAT_PASS =os.environ['XNAT_PASS']

def dicom2nifti(session_id):
    ## download session metadata
    this_session_metadata=get_metadata_session(session_id)
    this_session_metadata_df = pd.read_json(json.dumps(this_session_metadata))
    this_scan_id=''
    for session_each_metadata_id, session_each_metadata in this_session_metadata_df.iterrows():
        result_type= str(session_each_metadata['type'])
        if 'z-axial-brain' in result_type.lower() or 'z-brain-thin' in result_type.lower():
            URL='/data/experiments/'+session_id+'/scans/'+str(session_each_metadata['ID'])
            metadata_nifti=get_resourcefiles_metadata(URL,'DICOM')
            df_scan = pd.read_json(json.dumps(metadata_nifti))
            DICOMFILEDIR='/DICOMFILEDIR'
            for df_scan_each_id, df_scan_each in df_scan.iterrows():
                download_a_singlefile_with_URIString(df_scan_each['URI'],df_scan_each['Name'],DICOMFILEDIR)

        break


    return this_scan_id
    ## if axial brain or thin axial
    ##download dicoms in a directory
    ## run dcm2niix
    ## upload
    ## delete all dicoms
if __name__ == "__main__":
    import sys
    # Ensure input arguments are provided
    if len(sys.argv) < 1:
        print("Usage: python dicom2niftiDec202024.py <grayscale_image> <mask_image>")
        sys.exit(1)
    session_id = sys.argv[1]
    try:
        dicom2nifti(session_id)
    except Exception as e:
        print(str(e))
        sys.exit(1)
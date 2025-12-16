#!/usr/bin/python
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os, sys, errno, shutil, uuid,subprocess,csv,json
import math,inspect
import glob,xnat
import re,time
import requests
import pandas as pd
import nibabel as nib
import numpy as np
import pathlib
import argparse,xmltodict
from redcapapi_functions import *
catalogXmlRegex = re.compile(r'.*\.xml$')
XNAT_HOST_URL=os.environ['XNAT_HOST']  #'http://snipr02.nrg.wustl.edu:8080' #'https://snipr02.nrg.wustl.edu' #'https://snipr.wustl.edu'
XNAT_HOST = XNAT_HOST_URL # os.environ['XNAT_HOST'] #
XNAT_USER = os.environ['XNAT_USER']#
XNAT_PASS =os.environ['XNAT_PASS'] #
api_token=os.environ['REDCAP_API']

import xnat
import inspect
import traceback
from datetime import datetime

LOG_FILE = "./xnat_session_errors.log"

def given_sessionid_get_project_n_subjectids(session_id):
    """
    Given an XNAT experiment/session ID, return (project_id, subject_id).
    Logs any exception with function name and timestamp.
    """
    func_name = inspect.currentframe().f_code.co_name

    try:
        with xnat.connect(XNAT_HOST, user=XNAT_USER, password=XNAT_PASS) as connection:
            exp = connection.experiments[session_id]
            subj = exp.subject
            # print("Project ID:", exp.project)  # project identifier
            # print("Subject ID:", subj.id)  # system-wide subject id
            # print("Subject Label:", subj.label)
            return exp.project, subj.label

    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        error_msg = (
            f"[{timestamp}] "
            f"Function: {func_name}\n"
            f"Session ID: {session_id}\n"
            f"Error: {str(e)}\n"
            f"Traceback:\n{traceback.format_exc()}\n"
            f"{'-'*80}\n"
        )

        with open(LOG_FILE, "a") as f:
            f.write(error_msg)

        # Safe failure return (important for batch pipelines)
        return None, None



def given_csvfile_proj_subjids_append(csvfile, session_id):
    """
    Read CSV with session IDs, append/overwrite PROJECT_ID and SUBJECT_ID columns.
    """
    func_name = inspect.currentframe().f_code.co_name

    try:
        df = pd.read_csv(csvfile)

        # Ensure columns exist
        df["PROJECT_ID"] = ""
        df["SUBJECT_ID"] = ""

        for idx, row in df.iterrows():
            # session_id = str(row.get(session_col, "")).strip()
            if not session_id:
                continue

            try:
                proj, subj = given_sessionid_get_project_n_subjectids(session_id)
                df.at[idx, "PROJECT_ID"] = "" if proj is None else proj
                df.at[idx, "SUBJECT_ID"] = "" if subj is None else subj
            except Exception:
                df.at[idx, "PROJECT_ID"] = ""
                df.at[idx, "SUBJECT_ID"] = ""

        out_csv = csvfile #.replace(".csv", "_with_proj_subj.csv")
        df.to_csv(out_csv, index=False)
        return out_csv

    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        err = (
            f"[{timestamp}] Function: {func_name}\n"
            f"CSV file: {csvfile}\n"
            f"Error: {str(e)}\n"
            f"Traceback:\n{traceback.format_exc()}\n"
            f"{'-' * 80}\n"
        )
        with open(LOG_FILE, "a") as f:
            f.write(err)
        return None




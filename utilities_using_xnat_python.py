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
import os
import traceback
# import xnat
import argparse,xmltodict
from redcapapi_functions import *
catalogXmlRegex = re.compile(r'.*\.xml$')
XNAT_HOST_URL=os.environ['XNAT_HOST']  #'http://snipr02.nrg.wustl.edu:8080' #'https://snipr02.nrg.wustl.edu' #'https://snipr.wustl.edu'
XNAT_HOST = XNAT_HOST_URL # os.environ['XNAT_HOST'] #
XNAT_USER = os.environ['XNAT_USER']#
XNAT_PASS =os.environ['XNAT_PASS'] #
api_token=os.environ['REDCAP_API']

# import xnat
import inspect
import traceback
from datetime import datetime
from railway_fill_database import apply_single_row_csv_to_table
LOG_FILE = "./xnat_session_errors.log"
import inspect
import traceback
from datetime import datetime

LOG_FILE = "railway_db_errors.log"

def call_apply_single_row_csv_to_table(session_id, csv_file):
    """
    Wrapper to:
    - resolve project/subject from session_id
    - use project_id as table name
    - apply single-row CSV to DB table
    """
    func_name = inspect.currentframe().f_code.co_name

    try:
        # Resolve project & subject
        project_id, subject_label = given_sessionid_get_project_n_subjectids(session_id)

        if not project_id:
            raise ValueError(f"Could not resolve project for session_id={session_id}")

        table_name = project_id  # as per your design

        result = apply_single_row_csv_to_table(
            # engine=ENGINE,                    # global/shared engine
            csv_file=csv_file,
            table_name=table_name,
            session_id=session_id,      # identifier column in CSV & DB
        )

        return result

    except Exception as e:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = (
            f"[{ts}] Function: {func_name}\n"
            f"session_id={session_id}\n"
            f"csv_file={csv_file}\n"
            f"Error: {e}\n"
            f"Traceback:\n{traceback.format_exc()}\n"
            f"{'-'*80}\n"
        )
        with open(LOG_FILE, "a") as f:
            f.write(msg)

        # Propagate or return sentinel (choose one)
        raise
        # or: return None

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




def upload_file_to_project_resource(
    project_id: str,
    resource_label: str,
    local_file_path: str,
    remote_filename: str | None = None,
    verify: bool = True,
    use_multipart: bool = True,
    log_file: str = "xnat_upload_errors.log",
) -> dict:
    """
    Upload a local file into a PROJECT-level resource folder in XNAT.

    Target REST shape (project resources):
      - Create resource folder:
          PUT  /data/projects/{project-id}/resources/{resource-label}
      - Upload file:
          PUT  /data/projects/{project-id}/resources/{resource-label}/files/{filename}
        (either multipart 'file=@...' OR raw body with ?inbody=true)
    See XNAT API docs. :contentReference[oaicite:0]{index=0}

    Returns:
      {"ok": True, "project_id": ..., "resource_label": ..., "filename": ..., "uploaded_to": ...}
      or {"ok": False, "error": "...", "where": "..."} on failure (and logs traceback).
    """
    xnat_host=XNAT_HOST
    username = XNAT_USER
    password = XNAT_PASS
    try:
        if not os.path.isfile(local_file_path):
            raise FileNotFoundError(f"Local file not found: {local_file_path}")

        filename = remote_filename or os.path.basename(local_file_path)

        # XNAT expects paths under /data/...
        resource_base = f"/data/projects/{project_id}/resources/{resource_label}"
        upload_endpoint = f"{resource_base}/files/{filename}"

        with xnat.connect(xnat_host, user=username, password=password, verify=verify) as sess:
            # xnatpy session exposes requests-like methods; use interface.* if present
            http = getattr(sess, "interface", sess)

            # 1) Ensure the project resource folder exists (idempotent PUT)
            r1 = http.put(resource_base)
            if hasattr(r1, "ok") and not r1.ok:
                raise RuntimeError(f"Failed creating/ensuring resource folder: {r1.status_code} {getattr(r1, 'text', '')}")

            # 2) Upload the file
            with open(local_file_path, "rb") as f:
                if use_multipart:
                    # multipart form upload (like: curl -F "file=@x")
                    r2 = http.put(upload_endpoint, files={"file": f})
                else:
                    # raw body upload requires inbody=true
                    r2 = http.put(upload_endpoint, params={"inbody": "true"}, data=f)

            if hasattr(r2, "ok") and not r2.ok:
                raise RuntimeError(f"Upload failed: {r2.status_code} {getattr(r2, 'text', '')}")

        return {
            "ok": True,
            "project_id": project_id,
            "resource_label": resource_label,
            "filename": filename,
            "uploaded_to": upload_endpoint,
        }

    except Exception as e:
        # Write full traceback to a log file (so you can debug auth/permissions/paths)
        try:
            with open(log_file, "a", encoding="utf-8") as lf:
                lf.write("\n" + "=" * 80 + "\n")
                lf.write(f"Error uploading to XNAT project resource\n")
                lf.write(f"xnat_host={xnat_host}\nproject_id={project_id}\nresource_label={resource_label}\nfile={local_file_path}\n")
                lf.write(f"Exception: {repr(e)}\n")
                lf.write(traceback.format_exc())
        except Exception:
            pass

        return {"ok": False, "where": "upload_file_to_project_resource", "error": str(e)}



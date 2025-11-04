#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os,json
import csv
import pandas as pd
from typing import List, Dict
from download_with_session_ID import * # get_allsessionlist_in_a_project,get_resourcefiles_metadata,download_a_singlefile_with_URIString

def given_project_download_experimentslist(project_id):
    print(f"project_id::{project_id}")
    outputfile = f"/workingoutput/{project_id}.csv"
    get_metadata_project_sessionlist(project_id, outputfile=outputfile)
    return outputfile
def given_experiment_download_scanslist(experiment_id):
    outputfile = f"/workingoutput/{experiment_id}.csv"
    get_metadata_session(experiment_id, outputfile=outputfile)
    return outputfile
def given_experiment_n_scan_download_a_resource_flist(experiment_id,scan_id,resource_dir):
    URI=f'/data/experiments/{experiment_id}/scans/{scan_id}'
    metadata_resource=get_resourcefiles_metadata(URI, resource_dir)
    df_scan = pd.read_json(json.dumps(metadata_resource))
    outputfie=os.path.join('/workingoutput',f'{experiment_id}_{scan_id}_{resource_dir}.csv')
    pd.DataFrame(df_scan).to_csv(outputfie,index=False)
    return "X"
def given_experiment_find_selected_scan(experiment_id):
    return "X"
def given_experiment_n_scan_resource_file_ext_download_the_files():
    return "X"
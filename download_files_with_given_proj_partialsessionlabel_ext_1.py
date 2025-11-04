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
    return outputfie
def given_experiment_download_a_resource_flist(experiment_id,resource_dir):
    URI=f'/data/experiments/{experiment_id}'
    metadata_resource=get_resourcefiles_metadata(URI, resource_dir)
    df_scan = pd.read_json(json.dumps(metadata_resource))
    outputfie=os.path.join('/workingoutput',f'{experiment_id}_{resource_dir}.csv')
    pd.DataFrame(df_scan).to_csv(outputfie,index=False)
    return outputfie
def given_experiment_find_selected_scan(experiment_id):
    try:
        outputfie=given_experiment_download_a_resource_flist(experiment_id, "NIFTI_LOCATION")
        outputfie_df=pd.read_csv(outputfie)
        for row_id,row in outputfie_df.iterrows():

            uri=str(row['URI'])
            outputfie_return=os.path.join('/workingoutput',os.path.basename(uri))
            download_a_singlefile_with_URIString(
            uri,
            os.path.basename(uri),
            '/workingoutput')
            break
        outputfie_return_df=pd.read_csv(outputfie_return)
        for row_id,row in outputfie_return_df.iterrows():
            scan_id=str(row['ID'])
            print(scan_id)
            return scan_id
    except Exception as e:
        print(e)

    return "NO_SCAN_ID_FOUND"
def given_experiment_n_scan_download_a_resource_flist(experiment_id,scan_id,resource_dir):
    URI=f'/data/experiments/{experiment_id}/scans/{scan_id}'
    metadata_resource=get_resourcefiles_metadata(URI, resource_dir)
    df_scan = pd.read_json(json.dumps(metadata_resource))
    outputfie=os.path.join('/workingoutput',f'{experiment_id}_{scan_id}_{resource_dir}.csv')
    pd.DataFrame(df_scan).to_csv(outputfie,index=False)
    return outputfie
    # return "X"

def given_a_file_ext_n_resource_list_download_the_file(files_in_resource,extension):
    try:
        files_in_resource_df = pd.read_csv(files_in_resource)
        for row_id, row in files_in_resource_df.iterrows():
            if extension in str(row['URI']):
                uri = str(row['URI'])
                download_a_singlefile_with_URIString(
                uri,
                os.path.basename(uri),
                '/workingoutput')
    except Exception as e:
        pass

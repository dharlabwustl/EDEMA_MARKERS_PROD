#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os,json
import csv
from typing import List, Dict
from download_with_session_ID import * # get_allsessionlist_in_a_project,get_resourcefiles_metadata,download_a_singlefile_with_URIString

def given_project_download_experimentslist(project_id):
    print(f"project_id::{project_id}")
    get_metadata_project_sessionlist(project_id, outputfile=f"/workingoutput/{project_id}.csv")
    return "X"
def given_experiment_download_scanslist(experiment_id):
    return "X"
def given_scan_download_itsfilefolderlist(scan_id):
    return "X"
def given_experiment_n_scan_download_a_resource_fflist():
    return "X"
def given_experiment_n_scan_resource_file_ext_download_the_files():
    return "X"
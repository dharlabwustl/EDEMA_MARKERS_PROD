#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
from download_with_session_ID import get_allsessionlist_in_a_project

def filter_experiment_list_by_prefix(in_csv: str, prefix: str, out_csv: str) -> str:
    """
    Read a CSV of all experiments, filter by session label prefix,
    and save the subset to a new CSV.
    """
    if not os.path.exists(in_csv):
        raise FileNotFoundError(f"Input CSV not found: {in_csv}")

    with open(in_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader if str(r.get("label", "")).startswith(prefix)]

    if not rows:
        print(f"⚠️ No experiments found with prefix '{prefix}'")
        return ""

    os.makedirs(os.path.dirname(out_csv), exist_ok=True)

    fieldnames = rows[0].keys()
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Saved {len(rows)} experiments (prefix '{prefix}') to {out_csv}")
    return out_csv

def save_experiment_list(project: str, out_csv: str) -> str:
    """
    Fetch experiment (session) list for a project and save to CSV.
    Reuses get_allsessionlist_in_a_project() from your download_with_session_ID.py.
    """
    sessions = get_allsessionlist_in_a_project(project)

    if not sessions:
        print(f"No experiments found for project {project}")
        return ""

    # Ensure directory exists
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)

    # Collect all possible field names across items
    fieldnames = set()
    for s in sessions:
        fieldnames.update(s.keys())
    fieldnames = list(fieldnames)

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sessions)

    print(f"✅ Saved {len(sessions)} experiments for project '{project}' to {out_csv}")
    prefix='VNSICH'
    out_csv_1=out_csv.split('.csv')[0]+'_'+prefix+'.csv'
    filter_experiment_list_by_prefix(out_csv, prefix, out_csv_1)
    return out_csv

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Save all experiments of a project to CSV")
    ap.add_argument("project", help="XNAT project ID")
    ap.add_argument("out_csv", help="Path to output CSV file")
    args = ap.parse_args()

    save_experiment_list(args.project, args.out_csv)




# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# XNAT Batch Downloader (reads NIFTI_LOCATION CSV for scan ID)
#
# Flow:
#   1) Get all sessions in a project.
#   2) Filter sessions whose label starts with the prefix.
#   3) For each session:
#        - Go to the resource folder `NIFTI_LOCATION`
#        - Download the CSV file in it.
#        - Read its `ID` column → selected scan.
#   4) From that scan’s resource folder (user‑provided name), download files
#      matching the given suffix (pdf, csv, etc.).
#
# Reuses your existing helpers from download_with_session_ID.py:
#   - get_allsessionlist_in_a_project
#   - download_a_file_with_ext
#   - download_a_file_with_ext is used for both the NIFTI_LOCATION.csv and
#     target resource files.
# """
# # from __future__ import annotations
#
# import os
# import csv
# import re
# from typing import List, Dict, Optional
#
# from download_with_session_ID import (
#     get_allsessionlist_in_a_project,
#     download_a_file_with_ext,
# )
#
#
# def _ensure_dir(path: str) -> None:
#     os.makedirs(path, exist_ok=True)
#
#
# def list_sessions_with_prefix(project: str, prefix: str) -> List[dict]:
#     sessions = get_allsessionlist_in_a_project(project)
#     if not prefix:
#         return sessions
#     return [s for s in sessions if str(s.get("label", "")).startswith(prefix)]
#
#
# def get_scan_id_from_nifti_location(session_id: str, out_dir: str) -> Optional[str]:
#     """Download NIFTI_LOCATION CSV for a session and extract scan ID."""
#     _ensure_dir(out_dir)
#     # Download the csv from NIFTI_LOCATION resource folder
#     download_a_file_with_ext(
#         session_id=session_id,
#         scan_id="",
#         resource_dir="NIFTI_LOCATION",
#         extensions_to_download=r"\.csv$",
#         outputfolder=out_dir,
#     )
#
#     # Find the downloaded csv file
#     csv_file = None
#     for f in os.listdir(out_dir):
#         if f.endswith(".csv"):
#             csv_file = os.path.join(out_dir, f)
#             break
#
#     if not csv_file or not os.path.exists(csv_file):
#         return None
#
#     # Read ID column
#     with open(csv_file, newline="", encoding="utf-8") as cf:
#         reader = csv.DictReader(cf)
#         for row in reader:
#             scan_id = row.get("ID") or row.get("id")
#             if scan_id:
#                 return str(scan_id)
#     return None
#
#
# def download_project_by_prefix(
#     project: str,
#     session_label_prefix: str,
#     resource_name: str,
#     file_extension: str,
#     out_dir: str,
# ) -> List[Dict[str, str]]:
#     """Main orchestrator using NIFTI_LOCATION to find scan IDs."""
#     manifest: List[Dict[str, str]] = []
#     _ensure_dir(out_dir)
#
#     sessions = list_sessions_with_prefix(project, session_label_prefix)
#
#     for s in sessions:
#         session_id = str(s.get("ID"))
#         session_label = s.get("label") or ""
#         if not session_id:
#             continue
#
#         session_dir = os.path.join(out_dir, session_label or session_id)
#         _ensure_dir(session_dir)
#
#         # Get scan ID from NIFTI_LOCATION CSV
#         scan_id = get_scan_id_from_nifti_location(session_id, session_dir)
#         if not scan_id:
#             continue
#
#         pattern = file_extension.lower().lstrip('.')
#         regex_suffix = rf"\\.{pattern}$"
#
#         download_a_file_with_ext(
#             session_id=session_id,
#             scan_id=str(scan_id),
#             resource_dir=resource_name,
#             extensions_to_download=regex_suffix,
#             outputfolder=session_dir,
#         )
#
#         manifest.append({
#             "project": project,
#             "session_id": session_id,
#             "session_label": session_label,
#             "scan_id": str(scan_id),
#             "resource": resource_name,
#             "suffix": file_extension,
#             "dest": os.path.abspath(session_dir),
#         })
#
#     return manifest
#
#
# if __name__ == "__main__":
#     import argparse, pprint
#     ap = argparse.ArgumentParser(description="Download files using NIFTI_LOCATION to locate scan IDs.")
#     ap.add_argument("project")
#     ap.add_argument("session_label_prefix")
#     ap.add_argument("resource_name")
#     ap.add_argument("file_extension")
#     ap.add_argument("out_dir")
#     args = ap.parse_args()
#
#     pp = pprint.PrettyPrinter(indent=2)
#     out = download_project_by_prefix(
#         project=args.project,
#         session_label_prefix=args.session_label_prefix,
#         resource_name=args.resource_name,
#         file_extension=args.file_extension,
#         out_dir=args.out_dir,
#     )
#     pp.pprint(out)

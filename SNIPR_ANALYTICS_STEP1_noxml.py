#!/usr/bin/env python3
"""Build and upload Step 1 analytics from XNAT REST metadata via xnatpy."""

import argparse
import logging
import os
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import ExitStack
from datetime import datetime
from functools import partial
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Lock, local
from urllib.parse import quote

import pandas as pd
import xnat
from xnat.exceptions import XNATResponseError


ENRICHMENT_COLUMNS = [
    "subject_id", "acquisition_site_xml", "acquisition_datetime_xml",
    "scanner_from_xml", "body_part_xml", "kvp_xml", "axial_number",
    "axial_thin_number", "NUMBER_NIFTIFILES",
]
FRONT_COLUMNS = [
    "subject_id", "label", "acquisition_datetime_xml", "acquisition_site_xml",
]


def result_rows(connection, uri, optional=False):
    response = connection.get(uri, format="json", accepted_status=(200, 404) if optional else (200,))
    if response.status_code == 404:
        return []
    return response.json()["ResultSet"]["Result"]


def first_item(connection, uri):
    return connection.get_json(uri)["items"][0]


def child_items(item, field):
    return next(
        (child["items"] for child in item.get("children", []) if child["field"] == field),
        [],
    )


def scan_fields(item):
    fields = item["data_fields"].copy()
    for node, names in (("scanner", ("manufacturer", "model")), ("parameters", ("kvp",))):
        children = child_items(item, node)
        if children:
            for name in names:
                fields.setdefault(f"{node}/{name}", children[0]["data_fields"].get(name))
    return fields


def dicom_fallback(connection, scans, need_datetime, need_scanner):
    if not (need_datetime or need_scanner):
        return {}

    import SimpleITK as sitk

    values = {}
    for scan in scans:
        try:
            files = result_rows(connection, f"{scan['URI']}/resources/DICOM/files", optional=True)
            if len(files) <= 2:
                continue
            with TemporaryDirectory() as temporary_dir:
                dicom = Path(temporary_dir) / "scan.dcm"
                connection.download(files[0]["URI"], str(dicom), verbose=False)
                reader = sitk.ImageFileReader()
                reader.SetFileName(str(dicom))
                reader.LoadPrivateTagsOn()
                reader.ReadImageInformation()
                if need_datetime and all(reader.HasMetaDataKey(key) for key in ("0008|0020", "0008|0030")):
                    date = reader.GetMetaData("0008|0020").strip()
                    time = reader.GetMetaData("0008|0030").strip().split(".")[0].ljust(6, "0")
                    try:
                        values["acquisition_datetime_xml"] = datetime.strptime(
                            date + time, "%Y%m%d%H%M%S"
                        ).strftime("%m/%d/%Y %H:%M")
                        need_datetime = False
                    except ValueError:
                        logging.warning("Invalid DICOM study date or time for scan %s", scan["URI"])
                if need_scanner and all(reader.HasMetaDataKey(key) for key in ("0008|0070", "0008|1090")):
                    manufacturer = reader.GetMetaData("0008|0070").strip()
                    model = reader.GetMetaData("0008|1090").strip()
                    values["scanner_from_xml"] = f"{manufacturer} {model}"
                    need_scanner = False
        except (XNATResponseError, OSError, RuntimeError):
            logging.warning("Could not read DICOM metadata for scan %s", scan["URI"])
        if not (need_datetime or need_scanner):
            break
    return values


def session_values(connection, session_id, subject_labels):
    uri = f"/data/experiments/{quote(session_id, safe='')}"
    item = first_item(connection, uri)
    fields = item["data_fields"]
    scans = result_rows(connection, f"{uri}/scans/")
    scan_items = child_items(item, "scans/scan")
    if scan_items:
        details = [scan_fields(scan) for scan in scan_items[2:]]
    else:
        details = [scan_fields(first_item(connection, scan["URI"])) for scan in scans[2:]]

    def select_scan_value(key, minimum_length):
        value = None
        for scan in details:
            if scan.get(key) is not None:
                value = scan[key]
                if len(str(value)) >= minimum_length:
                    break
        return value

    manufacturer = next(
        (scan["scanner/manufacturer"] for scan in details if len(str(scan.get("scanner/manufacturer") or "")) > 1), ""
    )
    model = next(
        (scan["scanner/model"] for scan in details if len(str(scan.get("scanner/model") or "")) > 1), ""
    )
    scanner = f"{manufacturer} {model}".strip()
    acquired = None
    if fields.get("date") and fields.get("time"):
        try:
            # Step 1 records local acquisition time to minute precision.
            date = datetime.strptime(fields["date"], "%Y-%m-%d")
            time = datetime.strptime(fields["time"][:5], "%H:%M")
            acquired = date.replace(hour=time.hour, minute=time.minute).strftime("%m/%d/%Y %H:%M")
        except ValueError:
            logging.warning("Invalid acquisition date or time for session %s", session_id)

    counts = Counter(scan["type"] for scan in scans)
    nifti_count = sum(
        ".nii" in resource_file["Name"]
        for scan in scans
        for resource_file in result_rows(connection, f"{scan['URI']}/resources/NIFTI/files", optional=True)
    )
    values = {
        "subject_id": subject_labels.get(str(fields.get("subject_ID"))),
        "acquisition_site_xml": fields.get("acquisition_site"),
        "acquisition_datetime_xml": acquired,
        "scanner_from_xml": scanner or None,
        "body_part_xml": select_scan_value("bodyPartExamined", 4),
        "kvp_xml": select_scan_value("parameters/kvp", 2),
        "axial_number": counts["Z-Axial-Brain"],
        "axial_thin_number": counts["Z-Brain-Thin"],
        "NUMBER_NIFTIFILES": nifti_count,
    }
    values.update(dicom_fallback(connection, scans, not acquired, not scanner))
    return values


def project_csv(connection, uri):
    response = connection.get(uri, format="csv")
    return pd.read_csv(StringIO(response.text), dtype={"ID": str, "label": str})


def upload_csv(connection, host, project_uri, resource, path):
    # Match the existing xnatpy helper's multipart upload through its authenticated interface.
    url = f"{host.rstrip('/')}{project_uri}/resources/{quote(resource, safe='')}/files/"
    with path.open("rb") as handle:
        response = connection.interface.post(url, files={"file": handle}, timeout=120)
    response.raise_for_status()


def enrich_sessions(connection, sessions, subject_labels, connect, workers):
    total = len(sessions)
    active_workers = min(workers, total)
    logging.info("Processing %d CT sessions with %d worker(s)", total, active_workers)
    if active_workers <= 1:
        for completed, (index, session_id) in enumerate(sessions.items(), 1):
            yield index, session_values(connection, session_id, subject_labels)
            if completed % 25 == 0 or completed == total:
                logging.info("Processed %d/%d CT sessions", completed, total)
        return

    worker = local()
    connection_lock = Lock()
    with ExitStack() as connections, ThreadPoolExecutor(max_workers=active_workers) as pool:
        def enrich(session_id):
            if not hasattr(worker, "connection"):
                with connection_lock:
                    worker.connection = connections.enter_context(connect())
            return session_values(worker.connection, session_id, subject_labels)

        pending = {pool.submit(enrich, session_id): index for index, session_id in sessions.items()}
        try:
            for completed, future in enumerate(as_completed(pending), 1):
                yield pending[future], future.result()
                if completed % 25 == 0 or completed == total:
                    logging.info("Processed %d/%d CT sessions", completed, total)
        finally:
            for future in pending:
                future.cancel()


def run(connection, host, project, working_dir, connect=None, workers=1):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    project_uri = f"/data/projects/{quote(project, safe='')}"
    sessions = project_csv(connection, f"{project_uri}/experiments/")
    sessions = sessions.loc[sessions["xsiType"] == "xnat:ctSessionData"].copy()
    subjects = project_csv(connection, f"{project_uri}/subjects/")
    subject_labels = subjects.drop_duplicates("ID").set_index("ID")["label"].to_dict()

    working_dir.mkdir(parents=True, exist_ok=True)
    sessions.to_csv(working_dir / "sessions.csv", index=False)
    subjects.to_csv(working_dir / "subjects.csv", index=False)

    analytics = sessions.copy()
    for column in ENRICHMENT_COLUMNS:
        analytics[column] = None
    for index, values in enrich_sessions(connection, sessions["ID"], subject_labels, connect, workers):
        for column, value in values.items():
            analytics.at[index, column] = value

    before_sorting = working_dir / f"sessions_{project}_BEFORE_SORTING_STEP1_{timestamp}.csv"
    final = working_dir / f"sessions_{project}_ANALYTICS_STEP1_{timestamp}.csv"
    analytics.to_csv(before_sorting, index=False)
    acquisition_dates = pd.to_datetime(
        analytics["acquisition_datetime_xml"], format="%m/%d/%Y %H:%M", errors="coerce"
    )
    analytics = analytics.assign(_acquisition_sort=acquisition_dates).sort_values(
        ["subject_id", "_acquisition_sort"], na_position="last"
    ).drop(columns="_acquisition_sort")
    columns = FRONT_COLUMNS + [column for column in analytics if column not in FRONT_COLUMNS]
    analytics.to_csv(final, columns=columns, index=False)

    resource = f"{project}_SESSION_ANALYTICS_1"
    for path in (final, before_sorting):
        upload_csv(connection, host, project_uri, resource, path)
        logging.info("Uploaded %s to %s", path, resource)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project")
    args = parser.parse_args()
    if args.project in (".", "..") or "/" in args.project or "\\" in args.project:
        parser.error("project must be an XNAT project ID")
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    host = os.environ["XNAT_HOST"]
    try:
        workers = int(os.environ.get("XNAT_STEP1_WORKERS", "4"))
        if workers < 1:
            raise ValueError
    except ValueError:
        parser.error("XNAT_STEP1_WORKERS must be a positive integer")
    connect = partial(
        xnat.connect, host, user=os.environ["XNAT_USER"],
        password=os.environ["XNAT_PASS"], no_parse_model=True,
    )
    with connect() as connection:
        run(connection, host, args.project, Path("/workinginput"), connect, workers)


if __name__ == "__main__":
    main()

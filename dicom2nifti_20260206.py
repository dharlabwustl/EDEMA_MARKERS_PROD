#!/usr/bin/env python3
# Python 3.6 compatible (no "|" union typing)

import os
import shutil
import subprocess
import zipfile
from datetime import datetime
import traceback
import json

from utilities_using_xnat_python import (
    get_session_label_from_session_id,
    xnat_upload_file_to_scan_resource,
    xnat_ensure_scan_resource_exists,
    xnat_download_scan_resource_zip,
    get_candidate_scans_for_dicom2nifti,
)

# -----------------------------
# CONFIG (mounted inside Docker)
# -----------------------------
ZIP_DIR = "/ZIPFILEDIR"         # mounted
DICOM_DIR = "/DICOMFILEDIR"     # mounted
NIFTI_DIR = "/NIFTIFILEDIR"     # mounted
ERROR_FILE = "dicom2nifti_20260206_error.txt"

# If True, keep intermediate DICOMs/NIFTIs for debugging
KEEP_LOCAL_FILES = False


# -----------------------------
# LOGGING
# -----------------------------
def log_error(msg, func_name):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if isinstance(msg, (dict, list)):
        msg_str = json.dumps(msg, indent=2, default=str)
    else:
        msg_str = str(msg)

    tb = traceback.format_exc()
    tb_str = tb if "Traceback" in tb else "No traceback"

    err = (
        f"[{ts}]\n"
        f"Function: {func_name}\n"
        f"Message:\n{msg_str}\n"
        f"Traceback:\n{tb_str}\n"
        f"{'-' * 80}\n"
    )
    with open(ERROR_FILE, "a") as f:
        f.write(err)


# -----------------------------
# LOCAL HELPERS (no XNAT)
# -----------------------------
def clear_dir(dir_path):
    """Delete everything inside dir_path but keep the directory."""
    os.makedirs(dir_path, exist_ok=True)
    for name in os.listdir(dir_path):
        fp = os.path.join(dir_path, name)
        try:
            if os.path.isdir(fp):
                shutil.rmtree(fp)
            else:
                os.remove(fp)
        except Exception:
            # don't crash cleanup
            pass


def unzip_to_dir(zip_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(out_dir)


def find_best_dicom_leaf_dir(root_dir):
    """
    XNAT zips often extract into nested folders. dcm2niix works best when
    you point it at a folder that actually contains the DICOM files.

    Strategy:
      - Prefer folders containing *.dcm
      - If none, pick folder containing the most files
    """
    best_dir = None
    best_count = -1

    # First pass: *.dcm
    for cur_root, _, files in os.walk(root_dir):
        dcm_count = sum(1 for f in files if f.lower().endswith(".dcm"))
        if dcm_count > best_count:
            best_count = dcm_count
            best_dir = cur_root

    if best_dir is not None and best_count > 0:
        return best_dir

    # Second pass: any files (some DICOMs have no .dcm extension)
    best_dir = None
    best_count = -1
    for cur_root, _, files in os.walk(root_dir):
        file_count = sum(1 for f in files if os.path.isfile(os.path.join(cur_root, f)))
        if file_count > best_count:
            best_count = file_count
            best_dir = cur_root

    if best_dir is None or best_count <= 0:
        raise RuntimeError("No files found after unzip; DICOM folder appears empty.")

    return best_dir


def run_dcm2niix_convert(dicom_dir, out_dir, out_base, force_nii=True):
    """
    Clean, single dcm2niix call.
    Writes into out_dir.
    """
    os.makedirs(out_dir, exist_ok=True)

    cmd = ["dcm2niix", "-o", out_dir, "-f", out_base, "-m", "1"]
    if force_nii:
        cmd += ["-z", "n"]  # ensure .nii
    cmd += [dicom_dir]

    print("DCM2NIIX CMD:", " ".join(cmd), flush=True)

    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Helpful in Docker logs
    if p.stdout.strip():
        print("dcm2niix STDOUT:\n" + p.stdout, flush=True)
    if p.stderr.strip():
        print("dcm2niix STDERR:\n" + p.stderr, flush=True)

    if p.returncode != 0:
        raise RuntimeError(
            "dcm2niix failed (rc={})\nCMD: {}\nSTDOUT:\n{}\nSTDERR:\n{}".format(
                p.returncode, " ".join(cmd), p.stdout, p.stderr
            )
        )


def pick_nifti_file(out_dir):
    files = [f for f in os.listdir(out_dir) if f.endswith(".nii") or f.endswith(".nii.gz")]
    if not files:
        raise RuntimeError("No NIfTI produced in {}".format(out_dir))
    full = [os.path.join(out_dir, f) for f in files]
    return max(full, key=lambda fp: os.path.getsize(fp))


def force_exact_output_name(nifti_path, out_dir, exact_filename):
    exact_path = os.path.join(out_dir, exact_filename)
    if os.path.exists(exact_path):
        os.remove(exact_path)
    os.rename(nifti_path, exact_path)
    return exact_path


# -----------------------------
# PIPELINE (XNAT + local)
# -----------------------------
def convert_scan_dicom_to_nifti_and_upload(session_id, scan_id, dicom_resource_name="DICOM", nifti_resource_name="NIFTI"):
    func_name = "convert_scan_dicom_to_nifti_and_upload"

    try:
        session_label = get_session_label_from_session_id(session_id)
        if not session_label:
            raise RuntimeError("Could not resolve session label for session_id={}".format(session_id))

        out_base = "{}_{}".format(session_label, scan_id)
        exact_filename = out_base + ".nii"

        # Use unique ZIP per scan (avoid collisions)
        os.makedirs(ZIP_DIR, exist_ok=True)
        zip_path = os.path.join(ZIP_DIR, "{}_{}_{}.zip".format(session_id, scan_id, dicom_resource_name))

        # Ensure working dirs exist
        os.makedirs(DICOM_DIR, exist_ok=True)
        os.makedirs(NIFTI_DIR, exist_ok=True)

        # IMPORTANT: clear mounted dirs per scan to avoid leftovers
        # clear_dir(DICOM_DIR)
        # clear_dir(NIFTI_DIR)

        # 1) Download resource zip
        xnat_download_scan_resource_zip(session_id, scan_id, dicom_resource_name, zip_path)
        if not os.path.exists(zip_path) or os.path.getsize(zip_path) == 0:
            raise RuntimeError("Downloaded zip missing/empty: {}".format(zip_path))

        # 2) Unzip into mounted DICOM_DIR
        unzip_to_dir(zip_path, DICOM_DIR)
        return
        # 3) Find best dicom leaf directory
        leaf_dir = find_best_dicom_leaf_dir(DICOM_DIR)
        print("Using DICOM leaf dir:", leaf_dir, flush=True)

        # 4) Convert into mounted NIFTI_DIR
        dicom2nifti_convert_select_largest_and_rename(
                leaf_dir,
                NIFTI_DIR,
                session_label,
                scan_id,
                # keep_all_niftis: bool = True,
        )
        # run_dcm2niix_convert(dicom_dir=leaf_dir, out_dir=NIFTI_DIR, out_base=out_base, force_nii=True)
        return

        # 5) Pick produced nifti and ensure exact filename
        produced = pick_nifti_file(NIFTI_DIR)
        produced_exact = force_exact_output_name(produced, NIFTI_DIR, exact_filename)

        # 6) Upload to scan resource NIFTI
        xnat_ensure_scan_resource_exists(session_id, scan_id, nifti_resource_name)
        xnat_upload_file_to_scan_resource(session_id, scan_id, nifti_resource_name, produced_exact, exact_filename)

        # Optional cleanup
        if not KEEP_LOCAL_FILES:
            try:
                os.remove(zip_path)
            except Exception:
                pass
            # clear_dir(DICOM_DIR)
            # keep NIFTI_DIR file? if you want local visibility set KEEP_LOCAL_FILES=True
            # clear_dir(NIFTI_DIR)

        print("✅ Completed:", session_id, scan_id, produced_exact, flush=True)
        return True

    except Exception as e:
        log_error(
            {
                "session_id": session_id,
                "scan_id": scan_id,
                "dicom_resource": dicom_resource_name,
                "nifti_resource": nifti_resource_name,
                "error": str(e),
                "ZIP_DIR": ZIP_DIR,
                "DICOM_DIR": DICOM_DIR,
                "NIFTI_DIR": NIFTI_DIR,
            },
            func_name,
        )
        print("❌ Failed:", session_id, scan_id, str(e), flush=True)
        return False

# import os
# import subprocess


def dicom2nifti_convert_select_largest_and_rename(
    dicom_dir: str,
    out_dir: str,
    session_label: str,
    scan_id: str,
    keep_all_niftis: bool = True,
) -> str:
    """
    Convert DICOM->NIfTI using dcm2niix, then:
      - if multiple NIfTIs produced, pick the largest by filesize
      - rename it using the same naming logic from get_dicom_using_xnat()

    Naming rule (same as your old code):
        new_filename = "_".join((
            "_".join(session_label.split("_")[0:2]),
            "{}{}_{}".format(current_filename[4:8], current_filename[0:4], current_filename[8:12]),
            scan_id
        )) + ".nii"

    Params
    ------
    dicom_dir : str
        Path to directory containing DICOM files (already present locally).
    out_dir : str
        Output directory where dcm2niix will write NIfTI(s).
    session_label : str
        Session label string (e.g., from get_session_label(sessionId)).
    scan_id : str
        Scan ID (XNAT scan ID as string).
    keep_all_niftis : bool
        If False, delete other NIfTIs in out_dir after selecting+renaming the largest.

    Returns
    -------
    str
        Full path to the renamed "selected" NIfTI.
    """
    os.makedirs(out_dir, exist_ok=True)

    # 1) Run dcm2niix (match your old behavior: -m 1, filename pattern %t)
    cmd = ["dcm2niix", "-o", out_dir, "-f", "%t", "-m", "1", dicom_dir]
    print("DCM2NIIX CMD:", " ".join(cmd), flush=True)
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.stdout.strip():
        print("dcm2niix STDOUT:\n" + p.stdout, flush=True)
    if p.stderr.strip():
        print("dcm2niix STDERR:\n" + p.stderr, flush=True)
    if p.returncode != 0:
        raise RuntimeError(
            "dcm2niix failed (rc={})\nCMD: {}\nSTDOUT:\n{}\nSTDERR:\n{}".format(
                p.returncode, " ".join(cmd), p.stdout, p.stderr
            )
        )

    # 2) Collect NIfTIs
    nifti_files = [
        f for f in os.listdir(out_dir)
        if f.endswith(".nii") or f.endswith(".nii.gz")
    ]
    if not nifti_files:
        raise RuntimeError("No NIfTI produced in {}".format(out_dir))

    # 3) Pick largest
    largest_file = max(
        nifti_files,
        key=lambda f: os.path.getsize(os.path.join(out_dir, f))
    )
    largest_path = os.path.join(out_dir, largest_file)

    # 4) Build new filename using your exact convention
    # current_filename = basename without .nii / .nii.gz
    base = os.path.basename(largest_path)
    if base.endswith(".nii.gz"):
        current_filename = base[:-7]
    else:
        current_filename = base.split(".nii")[0]

    prefix = "_".join(session_label.split("_")[0:2])
    if len(current_filename) >= 12:
        mid = "{}{}_{}".format(current_filename[4:8], current_filename[0:4], current_filename[8:12])
    else:
        # fallback if dcm2niix name isn't long enough
        mid = current_filename

    new_filename = "_".join((prefix, mid, str(scan_id))) + ".nii"
    new_path = os.path.join(out_dir, new_filename)

    if os.path.exists(new_path):
        os.remove(new_path)

    os.rename(largest_path, new_path)
    print("Selected+Renamed:", largest_path, "->", new_path, flush=True)

    # 5) Optionally delete the other NIfTIs
    if not keep_all_niftis:
        for f in nifti_files:
            fp = os.path.join(out_dir, f)
            if fp != new_path and os.path.exists(fp):
                try:
                    os.remove(fp)
                except Exception:
                    pass

    return new_path

def run_dicom2nifti_for_session(session_id, dicom_resource_name="DICOM", nifti_resource_name="NIFTI"):
    func_name = "run_dicom2nifti_for_session"
    try:
        scan_ids = get_candidate_scans_for_dicom2nifti(session_id)
        print("Candidate scans:", scan_ids, flush=True)

        ok, fail = [], []
        for scan_id in scan_ids:
            success = convert_scan_dicom_to_nifti_and_upload(
                session_id=session_id,
                scan_id=str(scan_id),
                dicom_resource_name=dicom_resource_name,
                nifti_resource_name=nifti_resource_name,
            )
            (ok if success else fail).append(str(scan_id))

        print("DONE. OK:", ok, "FAILED:", fail, flush=True)
        return {"session_id": session_id, "ok": ok, "failed": fail}

    except Exception as e:
        log_error({"session_id": session_id, "error": str(e)}, func_name)
        return {"session_id": session_id, "ok": [], "failed": [], "error": str(e)}


# Optional CLI
# if __name__ == "__main__":
#     import sys
#     sid = sys.argv[1]
#     run_dicom2nifti_for_session(sid)

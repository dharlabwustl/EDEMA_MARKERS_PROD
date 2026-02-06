import os
import shutil
import tempfile
import subprocess
import zipfile
from datetime import datetime
import traceback
import json
from utilities_using_xnat_python import get_session_label_from_session_id, xnat_upload_file_to_scan_resource,xnat_ensure_scan_resource_exists,xnat_download_scan_resource_zip,get_candidate_scans_for_dicom2nifti
ERROR_FILE="dicom2nifti_20260206_error.txt"
def log_error(msg, func_name):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Allow structured logging
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

    with open(ERROR_FILE, "a") as f:   # APPEND, not overwrite
        f.write(err)

def unzip_to_dir(zip_path: str, out_dir: str) -> None:
    """Unzip zip_path into out_dir. No XNAT."""
    os.makedirs(out_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(out_dir)


def run_dcm2niix_convert(dicom_dir: str, out_dir: str, out_base: str, force_nii: bool = True) -> None:
    """
    Run dcm2niix on dicom_dir, writing to out_dir.
    out_base is -f argument (base name). No XNAT.
    """
    os.makedirs(out_dir, exist_ok=True)
    # cmd = ["dcm2niix", "-o", out_dir, "-f", out_base, "-m", "1"]
    # out_base = f"{session_label}_{scan_id}"

    cmd = [
        "dcm2niix",
        "-o", out_dir,
        "-f", out_base,
        "-m", "1",
        "-z", "n",
        dicom_dir,
    ]

    if force_nii:
        cmd += ["-z", "n"]  # ensure .nii not .nii.gz
    cmd += [dicom_dir]

    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"dcm2niix failed (rc={p.returncode})\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}")


def pick_nifti_file(out_dir: str) -> str:
    """
    Pick the best nifti from out_dir. Strategy: choose largest .nii or .nii.gz. No XNAT.
    """
    files = [f for f in os.listdir(out_dir) if f.endswith(".nii") or f.endswith(".nii.gz")]
    if not files:
        raise RuntimeError(f"No NIfTI produced in {out_dir}")
    full = [os.path.join(out_dir, f) for f in files]
    return max(full, key=lambda fp: os.path.getsize(fp))


def force_exact_output_name(nifti_path: str, out_dir: str, exact_filename: str) -> str:
    """
    Rename/move nifti_path into out_dir/exact_filename.
    Returns new full path. No XNAT.
    """
    exact_path = os.path.join(out_dir, exact_filename)
    # If it already exists, overwrite (optional — adjust to your preference)
    if os.path.exists(exact_path):
        os.remove(exact_path)
    os.rename(nifti_path, exact_path)
    return exact_path


# -----------------------------
# ORCHESTRATOR (thin wrapper)
# -----------------------------

def convert_scan_dicom_to_nifti_and_upload(
    session_id: str,
    scan_id: str,
    dicom_resource_name: str = "DICOM",
    nifti_resource_name: str = "NIFTI",
) -> bool:
    """
    Pipeline wrapper:
      - XNAT download DICOM zip
      - unzip locally
      - dcm2niix locally
      - choose best nifti + rename to session_label_scanid.nii
      - XNAT upload to scan's NIFTI resource

    Returns True/False.
    """
    func_name = "convert_scan_dicom_to_nifti_and_upload"
    tmp_root = None

    try:
        session_label = get_session_label_from_session_id(session_id)
        if not session_label:
            raise RuntimeError(f"Could not resolve session label for session_id={session_id}")

        exact_filename = f"{session_label}_{scan_id}.nii"
        out_base = f"{session_label}_{scan_id}"  # dcm2niix base

        tmp_root = tempfile.mkdtemp(prefix=f"dcm2niix_{session_id}_{scan_id}_")
        zip_path = os.path.join(tmp_root, "dicom.zip")
        dicom_dir = os.path.join(tmp_root, "dicom")
        out_dir = os.path.join(tmp_root, "out")

        # XNAT-dependent: download
        xnat_download_scan_resource_zip(session_id, scan_id, dicom_resource_name, zip_path)

        # Local: unzip + convert
        unzip_to_dir(zip_path, dicom_dir)
        run_dcm2niix_convert(dicom_dir=dicom_dir, out_dir=out_dir, out_base=out_base, force_nii=True)

        # Local: choose output + rename exactly
        produced = pick_nifti_file(out_dir)
        produced_exact = force_exact_output_name(produced, out_dir, exact_filename)

        # XNAT-dependent: ensure resource + upload
        xnat_ensure_scan_resource_exists(session_id, scan_id, nifti_resource_name)
        xnat_upload_file_to_scan_resource(session_id, scan_id, nifti_resource_name, produced_exact, exact_filename)

        return True

    except Exception as e:
        log_error(
            {
                "session_id": session_id,
                "scan_id": scan_id,
                "dicom_resource": dicom_resource_name,
                "nifti_resource": nifti_resource_name,
                "error": str(e),
            },
            func_name,
        )
        return False

    finally:
        if tmp_root and os.path.isdir(tmp_root):
            x=1
            # shutil.rmtree(tmp_root, ignore_errors=True)


def run_dicom2nifti_for_session(session_id: str):
    scan_ids = get_candidate_scans_for_dicom2nifti(session_id)   # <-- call it here (once)
    for scan_id in scan_ids:
        convert_scan_dicom_to_nifti_and_upload(session_id, scan_id)

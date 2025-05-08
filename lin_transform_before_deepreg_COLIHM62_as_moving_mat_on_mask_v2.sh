#!/bin/bash
set -e  # Exit on error

# ====== Configuration ======
XNAT_USER=${2}
XNAT_PASS=${3}
XNAT_HOST=${4}
SESSION_ID=${1}
WORKING_DIR=/workinginput
WORKING_DIR1=/input1
OUTPUT_DIR=/workingoutput
FINAL_OUTPUT_DIR=/outputinsidedocker
SOFTWARE_DIR="/software"
MASKS=("BET" "CSF" "INFARCT")
TEMPLATE_MAT="/software/COLIHM620406202215542.nii.gz"

# ====== Logging Helper ======
log() { echo "[`date +"%Y-%m-%d %H:%M:%S"`] $1"; }

# ====== Ensure directory exists ======
ensure_dir() {
    [[ ! -d "$1" ]] && mkdir -p "$1"
}

# ====== Main Execution Flow ======
main() {
    ensure_dir "$OUTPUT_DIR"
    ensure_dir "$WORKING_DIR1"
    prepare_inputs
    for nifti in "$WORKING_DIR1"/*.nii*; do
        process_scan "$nifti"
    done
    postprocess_outputs
}

# ====== Step 1: Download Input Files ======
prepare_inputs() {
    log "Downloading CT and masks from SNIPR..."
    # your python3 calls here to fetch scans and masks
}

# ====== Step 2: Process a Single CT Scan ======
process_scan() {
    local nifti_path="$1"
    local base=$(basename "${nifti_path%.nii*}")
    log "Processing $base"

    # Run BET
    local bet_file="${WORKING_DIR}/${base}_resaved_levelset_bet.nii.gz"
    cp "$bet_file" "$OUTPUT_DIR/"
    cp "$nifti_path" "$OUTPUT_DIR/${base}_resaved_levelset.nii.gz"

    # Transform masks to original CT space
    run_python_transform "$nifti_path" "$bet_file"

    # Run BET processing
    /software/bet_withlevelset.sh "$nifti_path" "$bet_file"

    # Linear registration
    /software/linear_rigid_registration.sh "${nifti_path%.nii*}_brain_f.nii.gz"

    # Midline detection
    run_midline_detection "$nifti_path"
}

# ====== Step 3: Mask Transform ======
run_python_transform() {
    local ct="$1"
    local mask="$2"
    python3 -c "
import sys; sys.path.append('${SOFTWARE_DIR}');
from utilities_simple_trimmed import *;
levelset2originalRF_new_flip()" "$ct" "$mask" "$OUTPUT_DIR"
}

# ====== Step 4: Midline Detection ======
run_midline_detection() {
    local ct="$1"
    /software/ideal_midline_fslpart.sh "$ct"
    /software/ideal_midline_pythonpart.sh "$ct"
    /software/ideal_midline_pythonpart_V2.sh "$ct"
}

# ====== Step 5: Final Upload ======
postprocess_outputs() {
    zip -r "$OUTPUT_DIR/MIDLINENPYFILES.zip" "$OUTPUT_DIR"/*.npy
    # call upload functions via Python
    log "Upload complete."
}

# ====== Run main pipeline ======
main "$@"

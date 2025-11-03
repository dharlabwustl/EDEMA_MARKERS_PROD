#!/bin/bash
# ---- Example: batch download from XNAT ----

PROJECT="ICH"
PREFIX="VNSICH"
RESOURCE="ICH_PHE_QUANTIFICATION"
SUFFIX="pdf"
OUTDIR="/workingoutput"

python3 download_files_with_given_proj_partialsessionlabel_ext.py \
    "$PROJECT" \
    "$PREFIX" \
    "$RESOURCE" \
    "$SUFFIX" \
    "$OUTDIR"

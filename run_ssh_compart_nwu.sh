#!/usr/bin/env bash
set -euo pipefail
SESSION_ID=${1} ##'SNIPR01_E00001'
# Optional: command passed as arguments; otherwise run a simple test
REMOTE_CMD="${*:-hostname; whoami; pwd}"

sshpass -p "$CLUSTER_PASS" \
  ssh \
    -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null \
    "${CLUSTER_USER}@${CLUSTER_HOST}" \
    "bash -lc '/rdcw/fs1/dharr/Active/ATUL/PROJECTS/DOCKERIZE/SNIPR_PIPELINE/EDEMA_BIOMARKER_CSF_COMPARTMENT_PIPELINE/call_COMBINE_EDEMABIOMARKER_N_COMPARTMENTS_part2.sh \"${SESSION_ID}\"'"



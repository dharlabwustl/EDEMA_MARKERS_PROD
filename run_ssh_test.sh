#!/usr/bin/env bash
#set -euo pipefail
#SESSION_ID=${1} ##'SNIPR01_E00001'
# Optional: command passed as arguments; otherwise run a simple test
#REMOTE_CMD="${*:-hostname; whoami; pwd}"
echo "I AM HERE IN THE DOCKER"
sshpass -p "$CLUSTER_PASS" \
  ssh \
    -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null \
    "${CLUSTER_USER}@${CLUSTER_HOST}" \
    "bash -lc pwd "



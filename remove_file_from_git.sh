#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <repo_url> <path_to_file>"
  echo "Example:"
  echo "  $0 https://github.com/dharlabwustl/EDEMA_MARKERS_PROD.git Dockerfile"
  exit 1
fi

REPO_URL="$1"
FILE_PATH="$2"

REPO_DIR=$(basename "$REPO_URL" .git)

echo "==> Cloning fresh repository"
git clone "$REPO_URL"
cd "$REPO_DIR"

echo "==> Removing file from all history: $FILE_PATH"
git filter-repo --path "$FILE_PATH" --invert-paths

echo "==> Force pushing rewritten history"
git push origin --force --all
git push origin --force --tags

echo "==> DONE"
echo "File '$FILE_PATH' has been permanently removed from all Git history."
echo ""
echo "IMPORTANT:"
echo "- All collaborators must re-clone the repository."
echo "- Rotate secrets immediately if this file contained credentials."

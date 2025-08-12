To use this you need to have access to [SNIPR](https://snipr.wustl.edu/).


## Running the Multi-Session Processing Workflow

This script prepares local directories, cleans previous outputs, and runs a Docker container to process one or more XNAT sessions using a specified script.

---

### Full Command Script (annotated)

> **Prereqs:** Docker installed, XNAT credentials set, access to required repositories.

```bash

### CONVERT DICOM IMAGES into NIFTI and store in a separate folder 'NIFTI' under the scan directory.
# 1) Set the Docker image name
imagename='fsl502py369withpacksnltx'

# 2) Create required directories on the host (bind-mounted into container)
mkdir working
mkdir input
mkdir ZIPFILEDIR
mkdir output
mkdir NIFTIFILEDIR
mkdir DICOMFILEDIR
mkdir maskonly
mkdir output  # duplicate, ensures folder exists

# 3) Clean previous run contents
rm -r working/*
rm -r input1/*
rm -r ZIPFILEDIR/*
rm -r output/*
rm -r NIFTIFILEDIR/*
rm -r DICOMFILEDIR/*
rm -r maskonly/*

# 4) Additional working directories for in-container use
mkdir workingoutput
mkdir workinginput
mkdir ZIPFILEDIR
mkdir outputinsidedocker
mkdir software

# 5) Clean those as well
rm -r workinginput/*
rm -r workingoutput/*
rm -r outputinsidedocker/*
rm -r workingoutput/*
rm -r ZIPFILEDIR/*
rm -r outputinsidedocker/*
rm -r software/*
rm -r output/*

# 6) Define session IDs (list and selected one)
SESSION_IDS=(SNIPR01_E00147 SNIPR01_E00146 SNIPR01_E00193 SNIPR02_E02970 SNIPR02_E09071 SNIPR01_E00231)
SESSION_ID=SNIPR01_E00131

# 7) XNAT credentials & Docker Hub namespace
XNAT_PASS=''
XNAT_USER=''
XNAT_HOST=${XNAT_HOST_LOCAL_COMPUTER}  # e.g., 'https://snipr.wustl.edu'
docker_hub='sharmaatul11'

# 8) Script to run inside container
script_number=DICOM2NIFTI

# 9) Run the Docker container with bind mounts
docker run \
  -v $PWD/maskonly:/maskonly \
  -v $PWD/workingoutput:/workingoutput \
  -v $PWD/outputinsidedocker:/outputinsidedocker \
  -v $PWD/workinginput:/workinginput \
  -v $PWD/software:/software \
  -v $PWD/NIFTIFILEDIR:/NIFTIFILEDIR \
  -v $PWD/DICOMFILEDIR:/DICOMFILEDIR \
  -v $PWD/working:/working \
  -v $PWD/input1:/input1 \
  -v $PWD/ZIPFILEDIR:/ZIPFILEDIR \
  -v $PWD/output:/output \
  -it registry.nrg.wustl.edu/docker/nrg-repo/sharmaatul11/${imagename} \
  /callfromgithub/downloadcodefromgithub.sh \
    $SESSION_ID \
    $XNAT_USER \
    $XNAT_PASS \
    https://github.com/dharlabwustl/EDEMA_MARKERS_PROD.git \
    $script_number \
    'https://snipr.wustl.edu'








### SCAN SELECLTION BASED ON SCAN TYPE, QUALITY and SLICE NUMBERS

## Running the Multi-Session Processing Workflow

This script prepares local directories, cleans previous outputs, and runs a Docker container to process one or more XNAT sessions using a specified script.

---

### Full Command Script (annotated)

> **Prereqs:** Docker installed, XNAT credentials set, access to required repositories.

```bash
# 1) Set the Docker image name
imagename='fsl502py369withpacksnltx'

# 2) Create required directories on the host (bind-mounted into container)
mkdir working
mkdir input
mkdir ZIPFILEDIR
mkdir output
mkdir NIFTIFILEDIR
mkdir DICOMFILEDIR
mkdir maskonly
mkdir output  # duplicate, ensures folder exists

# 3) Clean previous run contents
rm -r working/*
rm -r input1/*
rm -r ZIPFILEDIR/*
rm -r output/*
rm -r NIFTIFILEDIR/*
rm -r DICOMFILEDIR/*
rm -r maskonly/*

# 4) Additional working directories for in-container use
mkdir workingoutput
mkdir workinginput
mkdir ZIPFILEDIR
mkdir outputinsidedocker
mkdir software

# 5) Clean those as well
rm -r workinginput/*
rm -r workingoutput/*
rm -r outputinsidedocker/*
rm -r workingoutput/*
rm -r ZIPFILEDIR/*
rm -r outputinsidedocker/*
rm -r software/*
rm -r output/*

# 6) Define session IDs (list and selected one)
SESSION_IDS=(SNIPR01_E00147 SNIPR01_E00146 SNIPR01_E00193 SNIPR02_E02970 SNIPR02_E09071 SNIPR01_E00231)
SESSION_ID=SNIPR01_E00131

# 7) XNAT credentials & Docker Hub namespace
XNAT_PASS=''
XNAT_USER=''
XNAT_HOST=''

# 8) Script to run inside container
script_number=SCAN_SELECTION_FILL_RC

# 9) Run the Docker container with bind mounts
docker run \
  -v $PWD/maskonly:/maskonly \
  -v $PWD/workingoutput:/workingoutput \
  -v $PWD/outputinsidedocker:/outputinsidedocker \
  -v $PWD/workinginput:/workinginput \
  -v $PWD/software:/software \
  -v $PWD/NIFTIFILEDIR:/NIFTIFILEDIR \
  -v $PWD/DICOMFILEDIR:/DICOMFILEDIR \
  -v $PWD/working:/working \
  -v $PWD/input1:/input1 \
  -v $PWD/ZIPFILEDIR:/ZIPFILEDIR \
  -v $PWD/output:/output \
  -it registry.nrg.wustl.edu/docker/nrg-repo/sharmaatul11/${imagename} \
  /callfromgithub/downloadcodefromgithub.sh \
    $SESSION_ID \
    $XNAT_USER \
    $XNAT_PASS \
    https://github.com/dharlabwustl/EDEMA_MARKERS_PROD.git \
    $script_number \
    'https://snipr.wustl.edu'

```
#!/bin/bash

# --------------------------------------------------------------------
# EDEMABIOMARKERS_WITH_REDCapFilling (docker workflow) - dummy API key
# --------------------------------------------------------------------

# 1) Docker image
imagename='registry.nrg.wustl.edu/docker/nrg-repo/sharmaatul11/fsl502py369withpacksnltx:latest'

# 2) Create required host directories (bind-mounted into the container)
mkdir -p output input1 ZIPFILEDIR software NIFTIFILEDIR DICOMFILEDIR working workinginput workingoutput outputinsidedocker

# 3) Clean previous run contents (CAUTION: deletes all files inside these folders)
rm -rf output/* input1/* ZIPFILEDIR/* software/* NIFTIFILEDIR/* DICOMFILEDIR/* working/* workinginput/* workingoutput/* outputinsidedocker/*

# 4) XNAT variables (edit before running)
SESSION_ID=REPLACE_WITH_SESSION_ID       # e.g., SNIPR_E03614
PROJECT=REPLACE_WITH_PROJECT_NAME        # e.g., SNIPR01
XNAT_USER=REPLACE_WITH_XNAT_USERNAME
XNAT_PASS=REPLACE_WITH_XNAT_PASSWORD
XNAT_HOST='https://snipr.wustl.edu'
SCRIPT_NAME='EDEMABIOMARKERS'
REDCAP_API_KEY='DUMMY_API_KEY_1234567890ABCDEF'  # Dummy API key

# 5) Optional resource limits from JSON
# DOCKER_MEM_FLAGS="--memory=8g --memory-reservation=7g"

# 6) Run Docker container
docker run ${DOCKER_MEM_FLAGS} \
  -v "$PWD/output":/output \
  -v "$PWD/input1":/input1 \
  -v "$PWD/ZIPFILEDIR":/ZIPFILEDIR \
  -v "$PWD/software":/software \
  -v "$PWD/NIFTIFILEDIR":/NIFTIFILEDIR \
  -v "$PWD/DICOMFILEDIR":/DICOMFILEDIR \
  -v "$PWD/working":/working \
  -v "$PWD/workinginput":/workinginput \
  -v "$PWD/workingoutput":/workingoutput \
  -v "$PWD/outputinsidedocker":/outputinsidedocker \
  -it "${imagename}" \
  /callfromgithub/downloadcodefromgithub.sh \
    "${SESSION_ID}" \
    "${XNAT_USER}" \
    "${XNAT_PASS}" \
    "https://github.com/dharlabwustl/EDEMA_MARKERS_PROD.git" \
    "${SCRIPT_NAME}" \
    "${XNAT_HOST}" \
    "${REDCAP_API_KEY}"

To use this you need to have access to [SNIPR](https://snipr.wustl.edu/).

### CONVERT DICOM IMAGES into NIFTI and store in a separate folder 'NIFTI' under the scan directory.

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
XNAT_PASS='Mrityor1!'
XNAT_USER=atulkumar
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
XNAT_PASS='Mrityor1!'
XNAT_USER=atulkumar
XNAT_HOST=${XNAT_HOST_LOCAL_COMPUTER}  # e.g., 'https://snipr.wustl.edu'
docker_hub='sharmaatul11'

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


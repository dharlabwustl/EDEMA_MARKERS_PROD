To use this you need to have access to [SNIPR](https://snipr.wustl.edu/).

# Uniform Workflow Scripts

## Workflow 2

### 1) Docker Image
```bash
imagename='fsl502py369withpacksnltx'
```

### 2) Create Required Directories
```bash
mkdir working
mkdir input
mkdir ZIPFILEDIR
mkdir output
mkdir NIFTIFILEDIR
mkdir DICOMFILEDIR
mkdir maskonly
mkdir output  # duplicate, ensures folder exists
mkdir workingoutput
mkdir workinginput
mkdir ZIPFILEDIR
mkdir outputinsidedocker
mkdir software
```

### 3) Clean Old Contents
```bash
rm -r working/*
rm -r input1/*
rm -r ZIPFILEDIR/*
rm -r output/*
rm -r NIFTIFILEDIR/*
rm -r DICOMFILEDIR/*
rm -r maskonly/*
rm -r workinginput/*
rm -r workingoutput/*
rm -r outputinsidedocker/*
rm -r workingoutput/*
rm -r ZIPFILEDIR/*
rm -r outputinsidedocker/*
rm -r software/*
rm -r output/*
```

### 4) Set XNAT Variables
```bash
SESSION_ID=SNIPR01_E00131
XNAT_PASS=''
XNAT_USER=''
XNAT_HOST=${XNAT_HOST_LOCAL_COMPUTER}  # e.g., 'https://snipr.wustl.edu'
```

### 5) Optional Resource Limits
```bash
# DOCKER_MEM_FLAGS="--memory=8g --memory-reservation=7g"
```

### 6) Run Docker Container
```bash
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
```

---

## Workflow 3

### 1) Docker Image
```bash
imagename='fsl502py369withpacksnltx'
```

### 2) Create Required Directories
```bash
mkdir working
mkdir input
mkdir ZIPFILEDIR
mkdir output
mkdir NIFTIFILEDIR
mkdir DICOMFILEDIR
mkdir maskonly
mkdir output  # duplicate, ensures folder exists
mkdir workingoutput
mkdir workinginput
mkdir ZIPFILEDIR
mkdir outputinsidedocker
mkdir software
```

### 3) Clean Old Contents
```bash
rm -r working/*
rm -r input1/*
rm -r ZIPFILEDIR/*
rm -r output/*
rm -r NIFTIFILEDIR/*
rm -r DICOMFILEDIR/*
rm -r maskonly/*
rm -r workinginput/*
rm -r workingoutput/*
rm -r outputinsidedocker/*
rm -r workingoutput/*
rm -r ZIPFILEDIR/*
rm -r outputinsidedocker/*
rm -r software/*
rm -r output/*
```

### 4) Set XNAT Variables
```bash
SESSION_ID=SNIPR01_E00131
XNAT_PASS=''
XNAT_USER=''
XNAT_HOST=''
```

### 5) Optional Resource Limits
```bash
# DOCKER_MEM_FLAGS="--memory=8g --memory-reservation=7g"
```

### 6) Run Docker Container
```bash
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
```

---

## Workflow 4

### 1) Docker Image
```bash
imagename='registry.nrg.wustl.edu/docker/nrg-repo/sharmaatul11/fsl502py369withpacksnltx:latest'
```

### 2) Create Required Directories
```bash
mkdir -p output input1 ZIPFILEDIR software NIFTIFILEDIR DICOMFILEDIR working workinginput workingoutput outputinsidedocker
```

### 3) Clean Old Contents
```bash
rm -rf output/* input1/* ZIPFILEDIR/* software/* NIFTIFILEDIR/* DICOMFILEDIR/* working/* workinginput/* workingoutput/* outputinsidedocker/*
```

### 4) Set XNAT Variables
```bash
SESSION_ID=REPLACE_WITH_SESSION_ID       # e.g., SNIPR_E03614
PROJECT=REPLACE_WITH_PROJECT_NAME        # e.g., SNIPR01
XNAT_USER=REPLACE_WITH_XNAT_USERNAME
XNAT_PASS=REPLACE_WITH_XNAT_PASSWORD
XNAT_HOST='https://snipr.wustl.edu'
SCRIPT_NAME='EDEMABIOMARKERS'
REDCAP_API_KEY='DUMMY_API_KEY_1234567890ABCDEF'  # Dummy API key
```

### 5) Optional Resource Limits
```bash
# DOCKER_MEM_FLAGS="--memory=8g --memory-reservation=7g"
```

### 6) Run Docker Container
```bash
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
```

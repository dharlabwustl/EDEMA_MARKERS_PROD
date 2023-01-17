#!/bin/bash 

SESSION_ID=${1}
XNAT_USER=${2}
XNAT_PASS=${3}
TYPE_OF_PROGRAM=${4}
export XNAT_HOST=${5}
echo ${TYPE_OF_PROGRAM}::TYPE_OF_PROGRAM
if [[ ${TYPE_OF_PROGRAM} == 2 ]] ;
then 
    /software/nwucalculation_session_level_allsteps_November14_2022.sh $SESSION_ID $XNAT_USER $XNAT_PASS $XNAT_HOST /input /output
fi 
if [[ ${TYPE_OF_PROGRAM} == 1 ]] ;
then 
    /software/dicom2nifti_call_sessionlevel_selected.sh  ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi 

if [[ ${TYPE_OF_PROGRAM} == 3 ]] ;
then
  PROJECT_ID=${1}
    /software/combine_csvs_and_copy_pdfs_projectlevel_Jan9_2023.sh  ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 4 ]] ;
then

   /software/nwucalculation_scan_level_allsteps.sh
fi


if [[ ${TYPE_OF_PROGRAM} == 5 ]] ;
then

   /software/nwucalculation_onlocalcomp_aftersegJan172022.sh
fi
#!/bin/bash
SESSION_ID=${1}
XNAT_USER=${2}
XNAT_PASS=${3}
TYPE_OF_PROGRAM=${4}
echo TYPE_OF_PROGRAM::${TYPE_OF_PROGRAM}
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
if [[ ${TYPE_OF_PROGRAM} == 6 ]] ;
then

   /software/combine_csvs_and_copy_pdfs_projectlevel_Jan17_2023_LocalComputer.sh
fi

if [[ ${TYPE_OF_PROGRAM} == 7 ]] ;
then
    PROJECT_ID=${1}
echo ${PROJECT_ID}::$XNAT_USER::$XNAT_PASS::$XNAT_HOST
   /software/analyzed_session_list.sh  ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 8 ]] ;
then
    PROJECT_ID=${1}
echo ${PROJECT_ID}::$XNAT_USER::$XNAT_PASS::$XNAT_HOST
   /software/nwu_with_ich_mask.sh  ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi


if [[ ${TYPE_OF_PROGRAM} == 9 ]] ;
then
  PROJECT_ID=${1}
    /software/combine_csvs_and_copy_pdfs_projectlevel_April25_2023_ICH.sh  ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 10 ]] ;
then
  PROJECT_ID=${1}
    /software/create_pipeline_performancetable.sh  ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 11 ]] ;
then
  PROJECT_ID=${1}
    /software/SNIPR_ANALYTICS_SCANROW.sh  ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 12 ]] ;
then
    /software/scan_selection_May18_2023.sh $SESSION_ID $XNAT_USER $XNAT_PASS $XNAT_HOST /input /output
fi


if [[ ${TYPE_OF_PROGRAM} == 13 ]] ;
then
    /software/scan_selection_multiple_May25_2023.sh $SESSION_ID $XNAT_USER $XNAT_PASS $XNAT_HOST /input /output
fi

if [[ ${TYPE_OF_PROGRAM} == 14 ]] ;
then
  PROJECT_ID=${1}
    /software/combine_csvs_and_copy_pdfs_projectlevel_May262023_ICH.sh  ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 15 ]] ;
then
  PROJECT_ID=${1}
    /software/SNIPR_ANALYTICS_SCANROW_ADD_COLUMN.sh  ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 16 ]] ;
then
  PROJECT_ID=${1}
    /software/SNIPR_ANALYTICS_SCANROW_TEST_A_SESSION.sh   ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi
if [[ ${TYPE_OF_PROGRAM} == 17 ]] ;
then
  PROJECT_ID=${1}
    /software/SNIPR_ANALYTICS_SESSION_ONLY.sh   ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 18 ]] ;
then
    /software/change_scantype.sh  ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi
if [[ ${TYPE_OF_PROGRAM} == 19 ]] ;
then
    PROJECT_ID=${1}
    /software/change_scantype_from_projectlevel.sh  ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 20 ]] ;
then
    /software/csf_compartments_vols_N_display.sh  ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 21 ]] ;
then
    /software/EDIT_COMBINED_CSV_OF_EDEMABIOMARKERS.sh  ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 22 ]] ;
then
    /software/call_linear_registration.sh  $SESSION_ID $XNAT_USER $XNAT_PASS $XNAT_HOST
fi
if [[ ${TYPE_OF_PROGRAM} == 23 ]] ;
then
    /software/call_reg_midline.sh  $SESSION_ID $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 24 ]] ;
then
      PROJECT_ID=${1}
    /software/NWU_INFARCT_PROCESSING_ANALYTICS.sh  ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi
if [[ ${TYPE_OF_PROGRAM} == 25 ]] ;
then
      PROJECT_ID=${1}
    /software/SNIPR_ANALYTICS_SESSION_ONLY_SAH.sh   ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 26 ]] ;
then
      PROJECT_ID_1=COLI #${1}
      PROJECT_ID_2=MGBBMC #${1}
      PROJECT_ID_3=ICH #${1}
#      PROJECT_ID_4=COLI
    /software/ALL_PROJECTS_COMBINED_ANALYTICS.sh    $XNAT_USER $XNAT_PASS $XNAT_HOST ${PROJECT_ID_1} ${PROJECT_ID_2} ${PROJECT_ID_3} #${PROJECT_ID_4}
fi

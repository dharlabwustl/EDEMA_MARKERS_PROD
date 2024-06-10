#!/bin/bash
SESSION_ID=${1}
XNAT_USER=${2}
XNAT_PASS=${3}
TYPE_OF_PROGRAM=${4}
echo TYPE_OF_PROGRAM::${TYPE_OF_PROGRAM}
#'https://redcap.wustl.edu/redcap/api/' #
echo ${REDCAP_API}
#export REDCAP_API=${6}
#echo REDCAP_API::${REDCAP_API}
# The input string
input=$XNAT_HOST ##"one::two::three::four"
# Check if '::' is present
if echo "$input" | grep -q "+"; then
  # Set the delimiter
  IFS='+'

  # Read the split words into an array
  read -ra ADDR <<< "$input"
  export XNAT_HOST=${ADDR[0]} 
  SUBTYPE_OF_PROGRAM=${ADDR[1]} 
else
export XNAT_HOST=${5} 
    echo "'+' is not present in the string"
fi


echo ${TYPE_OF_PROGRAM}::TYPE_OF_PROGRAM::${SUBTYPE_OF_PROGRAM}::${ADDR[0]}::${ADDR[2]}::${ADDR[3]}
if [[ ${TYPE_OF_PROGRAM} == 2 ]]; then
  /software/nwucalculation_session_level_allsteps_November14_2022.sh $SESSION_ID $XNAT_USER $XNAT_PASS $XNAT_HOST /input /output
fi
if [[ ${TYPE_OF_PROGRAM} == 2.1 ]]; then
  /software/nwucalculation_session_level_allsteps_November13_2023.sh $SESSION_ID $XNAT_USER $XNAT_PASS $XNAT_HOST /input /output
fi
if [[ ${TYPE_OF_PROGRAM} == 1 ]]; then
  /software/dicom2nifti_call_sessionlevel_selected.sh ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 3 ]]; then
  PROJECT_ID=${1}
  /software/combine_csvs_and_copy_pdfs_projectlevel_Jan9_2023.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi
if [[ ${TYPE_OF_PROGRAM} == 3.1 ]]; then
  PROJECT_ID=${1}
  /software/SNIPR_ANALYTICS_SESSION_ONLY_ISCHEMIA.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
#  if [[ ${PROJECT_ID} == *"COLI"* ]] ;then
#    /software/SNIPR_ANALYTICS_SESSION_ONLY_ISCHEMIA.sh  ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
#  fi
#  if [[ ${PROJECT_ID} == *"WashU"* ]] ;then
#    /software/SNIPR_ANALYTICS_SESSION_ONLY_ISCHEMIA.sh  ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
#  fi
#  if [[ ${PROJECT_ID} == *"BJH"* ]] ;then
#    /software/SNIPR_ANALYTICS_SESSION_ONLY_ISCHEMIA.sh  ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
#  fi
#  if [[ ${PROJECT_ID} == *"MGBBMC"* ]] ;then
#    /software/SNIPR_ANALYTICS_SESSION_ONLY_ISCHEMIA.sh  ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
#  fi
fi
if [[ ${TYPE_OF_PROGRAM} == 3.2 ]]; then
  PROJECT_ID=${1}
  /software/SNIPR_ANALYTICS_SCANROW_ISCHEMIA.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
#    if [[ ${PROJECT_ID} == *"COLI"* ]] ;then
#    /software/SNIPR_ANALYTICS_SCANROW_ISCHEMIA.sh  ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
#    fi
#        if [[ ${PROJECT_ID} == *"WashU"* ]] ;then
#        /software/SNIPR_ANALYTICS_SCANROW_ISCHEMIA.sh  ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
#        fi
#            if [[ ${PROJECT_ID} == *"BJH"* ]] ;then
#            /software/SNIPR_ANALYTICS_SCANROW_ISCHEMIA.sh  ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
#            fi
#                if [[ ${PROJECT_ID} == *"MGBBMC"* ]] ;then
#                /software/SNIPR_ANALYTICS_SCANROW_ISCHEMIA.sh  ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
#                fi
fi
if [[ ${TYPE_OF_PROGRAM} == 4 ]]; then

  /software/nwucalculation_scan_level_allsteps.sh
fi

if [[ ${TYPE_OF_PROGRAM} == 5 ]]; then

  /software/nwucalculation_onlocalcomp_aftersegJan172022.sh
fi
if [[ ${TYPE_OF_PROGRAM} == 6 ]]; then

  /software/combine_csvs_and_copy_pdfs_projectlevel_Jan17_2023_LocalComputer.sh
fi

if [[ ${TYPE_OF_PROGRAM} == 7 ]]; then
  PROJECT_ID=${1}
  echo ${PROJECT_ID}::$XNAT_USER::$XNAT_PASS::$XNAT_HOST
  /software/analyzed_session_list.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 8 ]]; then
  PROJECT_ID=${1}
  echo ${PROJECT_ID}::$XNAT_USER::$XNAT_PASS::$XNAT_HOST
  /software/nwu_with_ich_mask.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
#  /software/phe_nwu_calculation.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 9 ]]; then
  PROJECT_ID=${1}
  /software/combine_csvs_and_copy_pdfs_projectlevel_April25_2023_ICH.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 10 ]]; then
  PROJECT_ID=${1}
  /software/create_pipeline_performancetable.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 11 ]]; then
  PROJECT_ID=${1}
  /software/SNIPR_ANALYTICS_SCANROW.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 12 ]]; then
  /software/scan_selection_May18_2023.sh $SESSION_ID $XNAT_USER $XNAT_PASS $XNAT_HOST /input /output
fi

if [[ ${TYPE_OF_PROGRAM} == 13 ]]; then
  /software/scan_selection_multiple_May25_2023.sh $SESSION_ID $XNAT_USER $XNAT_PASS $XNAT_HOST /input /output
fi

if [[ ${TYPE_OF_PROGRAM} == 14 ]]; then
  PROJECT_ID=${1}
  /software/combine_csvs_and_copy_pdfs_projectlevel_May262023_ICH.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 15 ]]; then
  PROJECT_ID=${1}
  /software/SNIPR_ANALYTICS_SCANROW_ADD_COLUMN.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 16 ]]; then
  PROJECT_ID=${1}
  /software/SNIPR_ANALYTICS_SCANROW_TEST_A_SESSION.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi
if [[ ${TYPE_OF_PROGRAM} == 17 ]]; then
  PROJECT_ID=${1}
  /software/SNIPR_ANALYTICS_SESSION_ONLY.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 18 ]]; then
  /software/change_scantype.sh ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi
if [[ ${TYPE_OF_PROGRAM} == 19 ]]; then
  PROJECT_ID=${1}
  /software/change_scantype_from_projectlevel.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 20 ]]; then
  /software/csf_compartments_vols_N_display.sh ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 21 ]]; then
  /software/EDIT_COMBINED_CSV_OF_EDEMABIOMARKERS.sh ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 22 ]]; then
  /software/call_linear_registration.sh $SESSION_ID $XNAT_USER $XNAT_PASS $XNAT_HOST
fi
if [[ ${TYPE_OF_PROGRAM} == 23 ]]; then
  /software/call_reg_midline.sh $SESSION_ID $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 24 ]]; then
  PROJECT_ID=${1}
  /software/NWU_INFARCT_PROCESSING_ANALYTICS.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi
if [[ ${TYPE_OF_PROGRAM} == 25 ]]; then
  PROJECT_ID=${1}
  /software/SNIPR_ANALYTICS_SESSION_ONLY_SAH.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 26 ]]; then
  PROJECT_ID_1=COLI   #${1}
  PROJECT_ID_2=MGBBMC #${1}
  PROJECT_ID_3=ICH    #${1}
  PROJECT_ID_4=SAH
  #      PROJECT_ID_4=COLI
  /software/ALL_PROJECTS_COMBINED_ANALYTICS.sh $XNAT_USER $XNAT_PASS $XNAT_HOST ${PROJECT_ID_1}_${PROJECT_ID_2}_${PROJECT_ID_3}_${PROJECT_ID_4}_WashU
fi
if [[ ${TYPE_OF_PROGRAM} == 27 ]]; then
  PROJECT_ID=${1}
  /software/SNIPR_ANALYTICS_SCANROW_SAH.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 28 ]]; then
  /software/csf_compartments_vols_N_display_Oct24_2023.sh ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 29 ]]; then
  PROJECT_ID=${1}
  /software/SNIPR_ANALYTICS_SESSION_ONLY_ICH.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi
if [[ ${TYPE_OF_PROGRAM} == 30 ]]; then
  PROJECT_ID=${1}
  /software/SNIPR_ANALYTICS_SCANROW_ICH.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 31 ]]; then
  PROJECT_ID=${1}
  /software/flowchart_for_one_project.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 32 ]]; then
  PROJECT_ID=${1}
  /software/SNIPR_ANALYTICS_STEP1.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi
if [[ ${TYPE_OF_PROGRAM} == 32.1 ]]; then
  PROJECT_ID=${1}
python3  /software/SNIPR_ANALYTICS_STEP1.py ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi
if [[ ${TYPE_OF_PROGRAM} == 33.1 ]]; then
  PROJECT_ID=${1}
  /software/SNIPR_ANALYTICS_STEP2.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi
if [[ ${TYPE_OF_PROGRAM} == 33 ]]; then
  PROJECT_ID=${1}
  python3 /software/SNIPR_ANALYTICS_STEP2.py ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi
if [[ ${TYPE_OF_PROGRAM} == 34.1 ]]; then
  PROJECT_ID=${1}
  /software/SNIPR_ANALYTICS_STEP3.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi
if [[ ${TYPE_OF_PROGRAM} == 34.2 ]]; then
  PROJECT_ID=${1}
 python3 /software/SNIPR_ANALYTICS_STEP3_REDCAP.py ${PROJECT_ID} ${XNAT_USER} ${XNAT_PASS} ${XNAT_HOST}
fi
if [[ ${TYPE_OF_PROGRAM} == 34 ]]; then
  PROJECT_ID=${1}
 python3 /software/SNIPR_ANALYTICS_STEP3.py ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi
if [[ ${TYPE_OF_PROGRAM} == 35 ]]; then
  PROJECT_ID=${1}
  /software/SNIPR_ANALYTICS_STEP4.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi
if [[ ${TYPE_OF_PROGRAM} == 36 ]]; then
  SESSION_ID=${1}
  /software/brain_left_right_entropy.sh ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi
if [[ ${TYPE_OF_PROGRAM} == "DELETESCANSELECTIONFILES" ]]; then
  SESSION_ID=${1}
 python3 /software/DELETE_SCAN_SELECTION_FILE.py ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi
if [[ ${TYPE_OF_PROGRAM} == "FLIPAMASK" ]]; then
  SESSION_ID=${1}
  /software/flip_an_infarct_mask.sh  ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST '_resaved_infarct_auto_removesmall.nii.gz'
  /software/flip_an_infarct_mask.sh  ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST '_resaved_4DL_normalized_class2.nii.gz'
  /software/flip_an_infarct_mask.sh  ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST '_resaved_4DL_normalized_class1.nii.gz'
fi

if [[ ${TYPE_OF_PROGRAM} == "PHE_NWULIKE_RATIO" ]]; then
  SESSION_ID=${1}
#  /software/nwu_with_ich_mask.sh ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
  /software/phe_nwu_ich_calculation.sh   ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == "REDCAP_FILL_SESSION_NAME" ]]; then
  SESSION_ID=${1}
  PROJECT_ID=${1}
  /software/fill_redcap.sh   ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi


if [[ ${TYPE_OF_PROGRAM} == "SCAN_SELECTION" ]]; then
  SESSION_ID=${1}
  PROJECT_ID=${1}
  /software/scan_selection_Jan17_2024.sh   $SESSION_ID $XNAT_USER $XNAT_PASS $XNAT_HOST /input /output
fi
if [[ ${TYPE_OF_PROGRAM} == "SCAN_SELECTION_FILL_RC" ]]; then
  SESSION_ID=${1}
  /software/scan_selection_fill_REDCap_Feb09_2024.sh   $SESSION_ID $XNAT_USER $XNAT_PASS $XNAT_HOST /input /output
fi
###########################################################
if [[ ${TYPE_OF_PROGRAM} == 'ANALYTICS_STEP1' ]]; then
  PROJECT_ID=${1}
  /software/SNIPR_ANALYTICS_STEP1.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 'ANALYTICS_STEP2' ]]; then
  PROJECT_ID=${1}
  python3 /software/SNIPR_ANALYTICS_STEP2.py ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi
if [[ ${TYPE_OF_PROGRAM} == 'SAH_ANALYTICS_STEP2' ]]; then
  PROJECT_ID=${1}
  python3 /software/SAH_ANALYTICS_STEP2.py ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi
if [[ ${TYPE_OF_PROGRAM} == 'ANALYTICS_STEP3' ]]; then
  PROJECT_ID=${1}
 python3 /software/SNIPR_ANALYTICS_STEP3.py ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi
if [[ ${TYPE_OF_PROGRAM} == 'ANALYTICS_STEP4' ]]; then
  PROJECT_ID=${1}
  /software/SNIPR_ANALYTICS_STEP4.sh ${PROJECT_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi
if [[ ${TYPE_OF_PROGRAM} == 'DICOM2NIFTI' ]]; then
  /software/dicom2nifti_call_03132024.sh  ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi
if [[ ${TYPE_OF_PROGRAM} == 'EDEMABIOMARKERS' ]]; then
  /software/nwucalculation_session_level_allsteps_with_RC_03_22_2024.sh   ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 'FILLREDCAPONLY' ]]; then
  /software/fill_redcap_only_04_06_2024.sh   ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
fi

if [[ ${TYPE_OF_PROGRAM} == 'DOWNLOADFILESAFTERANALYSIS' ]]; then
  PROJECT_ID=${1}
  echo "${PROJECT_ID}::$XNAT_USER::$XNAT_PASS::${ADDR[0]}::${ADDR[1]}::${ADDR[2]}::${ADDR[3]}::${ADDR[4]}"
#  "${ADDR[0]}:HOST" "${ADDR[1]}:RESOURCE" "${ADDR[2]}:FILE EXTENSION" "${ADDR[3]}:LOWER LIMIT OF SUBJ NAME" "${ADDR[4]}:UPPER LIMIT OF SUBJ NAME"
 python3 /software/downloadfiles_after_analysis.py   ${PROJECT_ID} $XNAT_USER $XNAT_PASS "${ADDR[0]}" "${ADDR[1]}" "${ADDR[2]}" "${ADDR[3]}" "${ADDR[4]}"
fi
# #############################################################################################################
if [[ ${TYPE_OF_PROGRAM} == 'PROJECT_LEVEL' ]]; then
echo "I AM HERE"
  if [[ ${SUBTYPE_OF_PROGRAM} == 'PROJECT_LEVEL_SCAN_SELECTION' ]]; then
    /software/project_level_scan_selection.sh   ${SESSION_ID} $XNAT_USER $XNAT_PASS "${ADDR[0]}" "${ADDR[2]}" "${ADDR[3]}"
  fi
#   if [[ ${SUBTYPE_OF_PROGRAM} == 'PROJECT_LEVEL_DICOM2NIFTI' ]]; then
#     /software/project_level_dicom2nifti.sh   ${SESSION_ID} $XNAT_USER $XNAT_PASS "${ADDR[0]}" "${ADDR[2]}" "${ADDR[3]}"
#   if [[ ${SUBTYPE_OF_PROGRAM} == 'PROJECT_LEVEL_INFARCT_BIOMARKER' ]]; then
#     /software/project_level_infarct_biomarker.sh   ${SESSION_ID} $XNAT_USER $XNAT_PASS "${ADDR[0]}"  "${ADDR[2]}" "${ADDR[3]}"
#   fi
#   if [[ ${SUBTYPE_OF_PROGRAM} == 'PROJECT_LEVEL_ICH_BIOMARKER' ]]; then
#     /software/project_level_ich_biomarker.sh   ${SESSION_ID} $XNAT_USER $XNAT_PASS "${ADDR[0]}"  "${ADDR[2]}" "${ADDR[3]}"
#   fi
#   if [[ ${SUBTYPE_OF_PROGRAM} == 'PROJECT_LEVEL_SAH_BIOMARKER' ]]; then
#     /software/project_level_sah_biomarker.sh   ${SESSION_ID} $XNAT_USER $XNAT_PASS "${ADDR[0]}"  "${ADDR[2]}" "${ADDR[3]}"
#   fi

fi
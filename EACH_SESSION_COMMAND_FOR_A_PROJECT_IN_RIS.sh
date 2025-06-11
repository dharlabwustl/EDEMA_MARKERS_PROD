#!/bin/bash
######################
######## USER DETAILS#######
project_ID=COLI ##${1}
snipr_step='ct_preprocessing'
XNAT_PASS='Mrityor1!'
XNAT_USER=atulkumar
XNAT_HOST='https://snipr.wustl.edu'
function directory_to_create_destroy(){
working_dir=${PWD}/workinginput
working_dir_1=${PWD}/input
output_directory=${PWD}/workingoutput
final_output_directory=${PWD}/outputinsidedocker
software=${PWD}/software
ZIPFILEDIR=${PWD}/ZIPFILEDIR 
NIFTIFILEDIR=$PWD/NIFTIFILEDIR 
DICOMFILEDIR=$PWD/DICOMFILEDIR
working=$PWD/working
input=$PWD/input
output=$PWD/output
rm  -r    ${working_dir}/*
rm  -r    ${working_dir_1}/*
rm  -r    ${output_directory}/*
rm  -r    ${final_output_directory}/*
# rm  -r    ${software}
rm  -r    ${ZIPFILEDIR}/*
rm  -r    ${NIFTIFILEDIR}/*
rm  -r    ${DICOMFILEDIR}/*
rm  -r    ${working}/*
rm  -r    ${input}/*
rm  -r    ${output}/*


}
# EXAMPLE: ICH_0058_CT_20170324  SNIPR02_E03684
function ct_preprocessing(){
local SESSION_ID=${1}
git_repo='https://github.com/dharlabwustl/CSFCOMPARTMENT.git'  #####'https://github.com/dharlabwustl/CSF_COMPARTMENT_REFINEMENT.git' #'https://github.com/dharlabwustl/CT_PROCESSING_STEP1.git'
script_number=VENT_BOUND_IN_SNIPR_CSF_WITH_CISTERN_MIDLINE_WITH_COLI_HM62 #POSTPROCESSING ##PREPROCESSING #POSTPROCESSING #PREPROCESSING #2
snipr_host='https://snipr.wustl.edu' 
# /callfromgithub/downloadcodefromgithub.sh $SESSION_ID $XNAT_USER $XNAT_PASS ${snipr_host} ${git_repo} ${script_number} 
/callfromgithub/downloadcodefromgithub.sh $SESSION_ID $XNAT_USER $XNAT_PASS https://github.com/dharlabwustl/CSF_COMPARTMENT_REFINEMENT.git $script_number  https://snipr.wustl.edu 
# $SESSION_ID $XNAT_USER $XNAT_PASS https://snipr.wustl.edu https://github.com/dharlabwustl/CT_PROCESSING_STEP1.git 2
}

#######################################
# download the list of sessions
sessions_list=session.csv 
curl -u $XNAT_USER:$XNAT_PASS -X GET $XNAT_HOST/data/projects/${project_ID}/experiments/?format=csv >${sessions_list}

echo "curl -u $XNAT_USER:$XNAT_PASS -X GET $XNAT_HOST/data/projects/${project_ID}/experiments/?format=csv >${sessions_list}"
#exit
# filter_ctsession_arguments=('filter_ctsession' ${sessions_list} ${sessions_list})
# # outputfiles_present=$(python3 /software/fillmaster_session_list.py "${filter_ctsession_arguments[@]}")
###################### ##################
count=0
  while IFS=',' read -ra array; do
    if [ ${array[4]} == 'xnat:ctSessionData' ] ; then
    echo SESSION_ID::${array[0]}
    SESSION_ID=SNIPR01_E00143  ###${array[0]}   ##SNIPR_E00876  #
    SESSION_NAME=${array[5]} 
    echo xsitype::${array[4]}
    echo SESSION_NAME::${SESSION_NAME}
    directory_to_create_destroy
    echo snipr_step::${snipr_step}
    ct_preprocessing ${SESSION_ID}  

#     ##echo "$SESSION_ID,$SESSION_NAME" >> ${list_accomplished}
    count=$((count+1))
#     fi
    if [ ${count} -gt 0 ]; then
    break
    fi
    fi
done < <(tail -n +2 "${sessions_list}")

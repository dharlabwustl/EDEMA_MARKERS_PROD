#!/bin/bash
export XNAT_USER=${2}
export XNAT_PASS=${3}
export XNAT_HOST=${4}
sessionID=${1}
working_dir=/workinginput
working_dir_1=/input1
output_directory=/workingoutput

final_output_directory=/outputinsidedocker

copyoutput_to_snipr() {
sessionID=$1
scanID=$2
resource_dirname=$4 #"MASKS" #sys.argv[4]
file_suffix=$5
output_dir=$3
echo " I AM IN copyoutput_to_snipr "
python3 -c "
import sys 
sys.path.append('/software');
from download_with_session_ID import *; 
uploadfile()" ${sessionID} ${scanID} ${output_dir} ${resource_dirname} ${file_suffix} # ${infarctfile_present}  ##$static_template_image $new_image $backslicenumber #$single_slice_filename

}
copyoutput_with_prefix_to_snipr() {
sessionID=$1
scanID=$2
resource_dirname=$4 #"MASKS" #sys.argv[4]
file_suffix=$5
output_dir=$3
echo " I AM IN copyoutput_to_snipr "
python3 -c "
import sys
sys.path.append('/software');
from download_with_session_ID import *;
uploadfile_withprefix()" ${sessionID} ${scanID} ${output_dir} ${resource_dirname} ${file_suffix} # ${infarctfile_present}  ##$static_template_image $new_image $backslicenumber #$single_slice_filename

}


copy_masks_data() {
echo " I AM IN copy_masks_data "
# rm -r /ZIPFILEDIR/*
sessionID=${1}
scanID=${2}
resource_dirname=${3} #str(sys.argv[4])
output_dirname=${4}   #str(sys.argv[3])
echo output_dirname::${output_dirname}
python3 -c "
import sys 
sys.path.append('/software');
from download_with_session_ID import *; 
downloadfiletolocaldir()" ${sessionID} ${scanID} ${resource_dirname} ${output_dirname} ### ${infarctfile_present}  ##$static_template_image $new_image $backslicenumber #$single_slice_filename

}

copy_scan_data() {
echo " I AM IN copy_scan_data "
# rm -r /ZIPFILEDIR/*
# rm -r ${working_dir}/*
# rm -r ${output_dir}/*
sessionID=$1
dir_to_receive_the_data=${2}
resource_dir=${3}
# sessionId=sys.argv[1]
# dir_to_receive_the_data=sys.argv[2]
# resource_dir=sys.argv[3]
# scanID=$2
python -c "
import sys 
sys.path.append('/Stroke_CT_Processing');
from download_with_session_ID import *; 
get_relevantfile_in_A_DIRECTORY()" ${sessionID} ${dir_to_receive_the_data} ${resource_dir}

}

run_IML_NWU_CSF_CALC() {
this_filename=${1}
this_betfilename=${2}
this_csfmaskfilename=${3}
this_infarctmaskfilename=${4}
echo "BET USING LEVELSET MASK"

/software/bet_withlevelset.sh $this_filename ${this_betfilename} #${output_directory} #Helsinki2000_1019_10132014_1048_Head_2.0_ax_Tilt_1_levelset # ${3} # Helsinki2000_702_12172013_2318_Head_2.0_ax_levelset.nii.gz #${3} # $6 $7 $8 $9 ${10}

#  echo "bet_withlevelset successful" >${output_directory}/success.txt
#  this_filename_brain=${this_filename%.nii*}_brain_f.nii.gz
#  # cp ${this_filename_brain} ${output_directory}/ #  ${final_output_directory}/
#  echo "LINEAR REGISTRATION TO TEMPLATE"
#  /software/linear_rigid_registration.sh ${this_filename_brain} #${templatefilename} #$3 ${6} WUSTL_233_11122015_0840__levelset_brain_f.nii.gz
#  echo "linear_rigid_registration successful" >>${output_directory}/success.txt
#  echo "RUNNING IML FSL PART"
#  /software/ideal_midline_fslpart.sh ${this_filename} # ${templatefilename} ${mask_on_template}  #$9 #${10} #$8
#  echo "ideal_midline_fslpart successful" >>${output_directory}/success.txt
#  echo "RUNNING IML PYTHON PART"
#
#  /software/ideal_midline_pythonpart.sh ${this_filename} #${templatefilename}  #$3 #$8 $9 ${10}
#  echo "ideal_midline_pythonpart successful" >>${output_directory}/success.txt
#
#  echo "RUNNING NWU AND CSF VOLUME CALCULATION "
#
#  /software/nwu_csf_volume.sh ${this_filename} ${this_betfilename} ${this_csfmaskfilename} ${this_infarctmaskfilename} ${lower_threshold} ${upper_threshold}
#  echo "nwu_csf_volume successful" >>${output_directory}/success.txt
#  thisfile_basename=$(basename $this_filename)
#  # for texfile in $(/usr/lib/fsl/5.0/remove_ext ${output_directory}/$thisfile_basename)*.tex ;
#  for texfile in ${output_directory}/*.tex; do
#    pdflatex -halt-on-error -interaction=nonstopmode -output-directory=${output_directory} $texfile ##${output_directory}/$(/usr/lib/fsl/5.0/remove_ext $this_filename)*.tex
#    rm ${output_directory}/*.aux
#    rm ${output_directory}/*.log
#  done

#  for filetocopy in $(/usr/lib/fsl/5.0/remove_ext ${output_directory}/$thisfile_basename)*_brain_f.nii.gz; do
#    cp ${filetocopy} ${final_output_directory}/
#  done
#
#  for filetocopy in $(/usr/lib/fsl/5.0/remove_ext ${output_directory}/$thisfile_basename)*.mat; do
#    cp ${filetocopy} ${final_output_directory}/
#  done
#
#  for filetocopy in ${output_directory}/*.pdf; do
#    cp ${filetocopy} ${final_output_directory}/
#  done
#  for filetocopy in ${output_directory}/*.csv; do
#    cp ${filetocopy} ${final_output_directory}/
#  done

}

nwucalculation_each_scan() {

eachfile_basename_noext=''
originalfile_basename=''
original_ct_file=''
#  for eachfile in ${working_dir}/*.nii*; do
for eachfile in ${working_dir_1}/*.nii*; do
original_ct_file=${eachfile}
eachfile_basename=$(basename ${eachfile})
originalfile_basename=${eachfile_basename}
eachfile_basename_noext=${eachfile_basename%.nii*}

############## files basename ##################################
grayfilename=${eachfile_basename_noext}_resaved_levelset.nii
if [[ "$eachfile_basename" == *".nii.gz"* ]]; then #"$STR" == *"$SUB"*
grayfilename=${eachfile_basename_noext}_resaved_levelset.nii.gz
fi
betfilename=${eachfile_basename_noext}_resaved_levelset_bet.nii.gz
csffilename=${eachfile_basename_noext}_resaved_csf_unet.nii.gz
infarctfilename=${eachfile_basename_noext}_resaved_infarct_auto_removesmall.nii.gz
################################################
############## copy those files to the docker image ##################################
cp ${working_dir}/${betfilename} ${output_directory}/
cp ${working_dir}/${csffilename} ${output_directory}/
cp ${working_dir}/${infarctfilename} ${output_directory}/
####################################################################################
source /software/bash_functions_forhost.sh

cp ${original_ct_file} ${output_directory}/${grayfilename}
grayimage=${output_directory}/${grayfilename} #${gray_output_subdir}/${eachfile_basename_noext}_resaved_levelset.nii
###########################################################################

#### originalfiel: .nii
#### betfile: *bet.nii.gz

# original_ct_file=$original_CT_directory_names/
levelset_infarct_mask_file=${output_directory}/${infarctfilename}
echo "levelset_infarct_mask_file:${levelset_infarct_mask_file}"
## preprocessing infarct mask:
python3 -c "
import sys ;
sys.path.append('/software/') ;
from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${original_ct_file}" "${levelset_infarct_mask_file}" "${output_directory}"

## preprocessing bet mask:
levelset_bet_mask_file=${output_directory}/${betfilename}
echo "levelset_bet_mask_file:${levelset_bet_mask_file}"
python3 -c "

import sys ;
sys.path.append('/software/') ;
from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${original_ct_file}" "${levelset_bet_mask_file}" "${output_directory}"

#### preprocessing csf mask:
levelset_csf_mask_file=${output_directory}/${csffilename}
echo "levelset_csf_mask_file:${levelset_csf_mask_file}"
python3 -c "
import sys ;
sys.path.append('/software/') ;
from utilities_simple_trimmed import * ;   levelset2originalRF_new_flip()" "${original_ct_file}" "${levelset_csf_mask_file}" "${output_directory}"

lower_threshold=0
upper_threshold=20
templatefilename=${template_prefix}.nii.gz
mask_on_template=midlinecssfResampled1.nii.gz

x=$grayimage
bet_mask_filename=${output_directory}/${betfilename}
infarct_mask_filename=${output_directory}/${infarctfilename}
csf_mask_filename=${output_directory}/${csffilename}
run_IML_NWU_CSF_CALC $x ${bet_mask_filename} ${csf_mask_filename} ${infarct_mask_filename}

done

# for f in ${output_directory}/*; do
#     # if [ -d "$f" ]; then
#         # $f is a directory
#         rm -r $f
#     # fi
# done

}

# #####################################################
get_nifti_scan_uri() {
# csvfilename=sys.argv[1]
# dir_to_save=sys.argv[2]
# echo " I AM IN copy_scan_data "
# rm -r /ZIPFILEDIR/*

sessionID=$1
working_dir=${2}
output_csvfile=${3}
rm -r ${working_dir}/*
output_dir=$(dirname ${output_csvfile})
rm -r ${output_dir}/*
# scanID=$2
python3 -c "
import sys 
sys.path.append('/software');
from download_with_session_ID import *; 
call_decision_which_nifti()" ${sessionID} ${working_dir} ${output_csvfile}

}

copy_scan_data() {
csvfilename=${1} #sys.argv[1]
dir_to_save=${2} #sys.argv[2]
# 		echo " I AM IN copy_scan_data "
# rm -r /ZIPFILEDIR/*
# rm -r ${working_dir}/*
# rm -r ${output_dir}/*
# sessionID=$1
# # scanID=$2
python3 -c "
import sys 
sys.path.append('/software');
from download_with_session_ID import *; 
downloadniftiwithuri_withcsv()" ${csvfilename} ${dir_to_save}

}
uploadsinglefile(){
local sessionID=${1}
local scanID=${2}
local mask_binary_output_dir=${3}
local snipr_output_foldername=${4}
local mask_binary_output_filename=${5}

echo ${mask_binary_output_dir}/${mask_binary_output_filename}
python3 -c "
import sys
sys.path.append('/software');
from download_with_session_ID import *;
uploadsinglefile()" ${sessionID} ${scanID} ${mask_binary_output_dir} ${snipr_output_foldername} ${mask_binary_output_filename}
}
getmaskfilesscanmetadata() {
# def get_maskfile_scan_metadata():
sessionId=${1}           #sys.argv[1]
scanId=${2}              # sys.argv[2]
resource_foldername=${3} # sys.argv[3]
dir_to_save=${4}         # sys.argv[4]
csvfilename=${5}         # sys.argv[5]
python3 -c "
import sys 
sys.path.append('/software');
from download_with_session_ID import *; 
get_maskfile_scan_metadata()" ${sessionId} ${scanId} ${resource_foldername} ${dir_to_save} ${csvfilename}
}

#########################################################################
## GET THE SINGLE CT NIFTI FILE NAME AND COPY IT TO THE WORKING_DIR
#niftifile_csvfilename=${working_dir}/'this_session_final_ct.csv'
#get_nifti_scan_uri ${sessionID}  ${working_dir} ${niftifile_csvfilename}
call_download_files_in_a_resource_in_a_session_arguments=('call_download_files_in_a_resource_in_a_session' ${sessionID} "NIFTI_LOCATION" ${working_dir})
outputfiles_present=$(python3 download_with_session_ID.py "${call_download_files_in_a_resource_in_a_session_arguments[@]}")
echo '$outputfiles_present'::$outputfiles_present
########################################
for niftifile_csvfilename in ${working_dir}/*NIFTILOCATION.csv; do
rm ${final_output_directory}/*.*
rm ${output_directory}/*.*
outputfiles_present=0
echo $niftifile_csvfilename
while IFS=',' read -ra array; do
scanID=${array[2]}
echo sessionId::${sessionID}
echo scanId::${scanID}
snipr_output_foldername="PREPROCESS_SEGM"
### check if the file exists:
call_check_if_a_file_exist_in_snipr_arguments=('call_check_if_a_file_exist_in_snipr' ${sessionID} ${scanID} ${snipr_output_foldername} .pdf .csv)
outputfiles_present=$(python3 download_with_session_ID.py "${call_check_if_a_file_exist_in_snipr_arguments[@]}")

################################################
#    outputfiles_present=0
echo "outputfiles_present:: "${outputfiles_present: -1}"::outputfiles_present"
#echo "outputfiles_present::ATUL${outputfiles_present}::outputfiles_present"
if [[ "${outputfiles_present: -1}" -eq 1 ]]; then
echo " I AM THE ONE"
fi
if  [[ "${outputfiles_present: -1}" -eq 0 ]]; then ## [[ 1 -gt 0 ]]  ; then #

echo "outputfiles_present:: "${outputfiles_present: -1}"::outputfiles_present"
## GET THE SESSION CT image
copy_scan_data ${niftifile_csvfilename} ${working_dir_1} #${working_dir}
nifti_file_without_ext=$(basename $(ls ${working_dir_1}/*.nii))
nifti_file_without_ext=${nifti_file_without_ext%.nii*}
##############################################################################################################

## GET THE RESPECTIVS MASKS NIFTI FILE NAME AND COPY IT TO THE WORKING_DIR

#####################################################################################
resource_dirname='MASKS'
output_dirname=${working_dir}
while IFS=',' read -ra array; do
scanID=${array[2]}
echo sessionId::${sessionID}
echo scanId::${scanID}
done < <(tail -n +2 "${niftifile_csvfilename}")
echo working_dir::${working_dir}
echo output_dirname::${output_dirname}
copy_masks_data ${sessionID} ${scanID} ${resource_dirname} ${output_dirname}
resource_dirname='PREPROCESS_SEGM'
copy_masks_data ${sessionID} ${scanID} ${resource_dirname} ${output_dirname}
resource_dirname='EDEMA_BIOMARKER'
copy_masks_data ${sessionID} ${scanID} ${resource_dirname} ${output_dirname}

###################### BY NOW WE HAVE EVERYTHIN WE NEED #############
## RELEVANT FILES ARE : SESSION CT, TEMPLATE CT, TEMPLATE MASKS, BET MASK FROM YASHENG to  MAKE BET GRAY OF SESSION CT
## and the mat files especially the Inv.mat file let us keep the sensible names from here:
session_ct=$( ls ${working_dir_1}/*'.nii' )
session_ct_bname_noext=$(basename ${session_ct})
session_ct_bname_noext=${session_ct_bname_noext%.nii*}
#fixed_image_filename='/software/COLIHM620406202215542.nii.gz'  ####${template_prefix}.nii.gz'
infarct_mask_from_yasheng=$(ls ${working_dir}/${nifti_file_without_ext}*_resaved_infarct_auto_removesmall.nii.gz)
#      template_masks_dir='/software/mritemplate/NONLINREGTOCT/' 	COLI_HM62_04062022_1554_2_resaved_csf_unet.nii.gz
bet_mask_from_yasheng=$(ls ${working_dir}/${nifti_file_without_ext}*_resaved_levelset_bet.nii.gz)
csf_mask_from_yasheng=$(ls ${working_dir}/${nifti_file_without_ext}*_resaved_csf_unet.nii.gz)
echo "levelset_bet_mask_file:${levelset_bet_mask_file}"
python3 -c "

import sys ;
sys.path.append('/software/') ;
from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${session_ct}" "${infarct_mask_from_yasheng}" "${output_directory}"

python3 -c "

import sys ;
sys.path.append('/software/') ;
from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${session_ct}" "${bet_mask_from_yasheng}" "${output_directory}"

python3 -c "

import sys ;
sys.path.append('/software/') ;
from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${session_ct}" "${csf_mask_from_yasheng}" "${output_directory}"


# now let us make bet gray for session ct:
/software/bet_withlevelset.sh ${session_ct} ${output_directory}/$(basename ${bet_mask_from_yasheng})

#### normalize and resample the grayscale image
fixed_image_filename=${output_directory}/${session_ct_bname_noext}_brain_f.nii.gz #COLIHM620406202215542.nii.gz ##'  ####${template_prefix}.nii.gz ##${session_ct_bet_gray}
#template_prefix='scct_strippedResampled1' ##.nii.gz'COLIHM620406202215542'
#moving_image_filename=${output_directory}/${session_ct_bname_noext}_brain_f.nii.gz
#function_with_arguments=('call_normalization_N_resample_to_fixed' ${moving_image_filename}  ${fixed_image_filename} )
#echo "outputfiles_present="'$(python3 utilities_simple_trimmed.py' "${function_with_arguments[@]}"
#outputfiles_present=$(python3 utilities_simple_trimmed.py "${function_with_arguments[@]}")
#
##              fixed_image_filename=/software/${template_prefix}.nii.gz ##${session_ct_bet_gray}
##### resample the infarct image
#moving_image_filename=${output_directory}/${session_ct_bname_noext}_resaved_infarct_auto_removesmall.nii.gz
#function_with_arguments=('call_only_resample_to_fixed' ${moving_image_filename}  ${fixed_image_filename} )
#echo "outputfiles_present="'$(python3 utilities_simple_trimmed.py' "${function_with_arguments[@]}"
#outputfiles_present=$(python3 utilities_simple_trimmed.py "${function_with_arguments[@]}")
#
################################ REGISTRATION## image and get matrix
#normalized_fixed_file_name=${fixed_image_filename} ###%.nii*}'_normalized_fix.nii.gz'
#fixed_image_filename=${normalized_fixed_file_name}
## REGISTRATION OF THE GRAY LEVEL CT
moving_image_filename=/software/scct_strippedResampled1.nii.gz
#cp $fixed_image_filename $moving_image_filename
#moving_image_filename=${output_directory}/${moving_image_filename} ##%.nii*}resampled_normalized_mov.nii.gz
/software/linear_rigid_registration_v10162024.sh ${moving_image_filename}  ${fixed_image_filename} ${output_directory}
session_ct_bet_gray_lin_reg_output=${output_directory}/'mov_'$(basename ${moving_image_filename%.nii*})_fixed_$(basename  ${fixed_image_filename%.nii*})_lin1.nii.gz

#${output_directory}/mov_${session_ct_bname_noext}_brain_fresampled_normalized_mov_fixed_${template_prefix}_normalized_fix_lin1.nii.gz
#####
### apply the matrix to the infarct mask
#       normalized_fixed_file_name
#moving_image_filename=$(basename ${moving_image_filename})
registration_mat_file=${output_directory}/'mov_'$(basename ${moving_image_filename%.nii*})_fixed_$(basename  ${fixed_image_filename%.nii*})_lin1.mat

#${output_directory}/mov_${moving_image_filename%.nii*}_fixed_${template_prefix}_normalized_fix_lin1.mat
registration_nii_file=${output_directory}/'mov_'$(basename ${moving_image_filename%.nii*})_fixed_$(basename  ${fixed_image_filename%.nii*})_lin1.nii.gz

#${output_directory}/mov_${moving_image_filename%.nii*}_fixed_${template_prefix}_normalized_fix_lin1.nii.gz
#fixed_image_filename=${normalized_fixed_file_name}
## REGISTRATION OF THE INFARCT MASK
#moving_image_filename=${session_ct_bname_noext}_resaved_infarct_auto_removesmall.nii.gz
#moving_image_filename=${output_directory}/${moving_image_filename} ##%.nii*}resampled_mov.nii.gz
#mask_binary_output_dir='/input1'
/software/linear_rigid_registration_onlytrasnformwith_matfile10162024.sh  ${moving_image_filename} ${fixed_image_filename} ${registration_mat_file} ${output_directory}
#moving_image_filename=$(basename ${moving_image_filename%.nii*})
mask_binary_output_filename=mov_$(basename ${moving_image_filename%.nii*})_fixed_$(basename  ${fixed_image_filename%.nii*})_lin1.nii.gz
threshold=0
function_with_arguments=('call_gray2binary' ${mask_binary_output_dir}/${mask_binary_output_filename}  ${mask_binary_output_dir} ${threshold})
echo "outputfiles_present="'$(python3 utilities_simple_trimmed.py' "${function_with_arguments[@]}"
outputfiles_present=$(python3 utilities_simple_trimmed.py "${function_with_arguments[@]}")
infarct_mask_binary_output_filename=${mask_binary_output_dir}/${mask_binary_output_filename%.nii*}_BET.nii.gz

## REGISTRATION OF THE BET MASK
#moving_image_filename=${output_directory}/$(basename ${bet_mask_from_yasheng})
#mask_binary_output_dir='/input1'
#/software/linear_rigid_registration_onlytrasnformwith_matfile10162024.sh  ${moving_image_filename} ${fixed_image_filename} ${registration_mat_file} ${output_directory}
##moving_image_filename=$(basename ${moving_image_filename%.nii*})
#bet_binary_output_filename=mov_$(basename ${moving_image_filename%.nii*})_fixed_${fixed_image_filename}_lin1.nii.gz
#threshold=0
#function_with_arguments=('call_gray2binary' ${mask_binary_output_dir}/${bet_binary_output_filename}  ${mask_binary_output_dir} ${threshold})
#echo "outputfiles_present="'$(python3 utilities_simple_trimmed.py' "${function_with_arguments[@]}"
#outputfiles_present=$(python3 utilities_simple_trimmed.py "${function_with_arguments[@]}")
#BET_bet_binary_output_filename=${mask_binary_output_dir}/${bet_binary_output_filename%.nii*}_BET.nii.gz
##########################################
## REGISTRATION OF THE CSF MASK
moving_image_filename='/software/scct_strippedResampled1_onlyventricle.nii.gz' ##${output_directory}/$(basename ${csf_mask_from_yasheng})
mask_binary_output_dir='/input1'
/software/linear_rigid_registration_onlytrasnformwith_matfile10162024.sh  ${moving_image_filename} ${fixed_image_filename} ${registration_mat_file} ${mask_binary_output_dir}
#moving_image_filename=$(basename ${moving_image_filename%.nii*})
csf_binary_output_filename=mov_$(basename ${moving_image_filename%.nii*})_fixed_$(basename ${fixed_image_filename%.nii*})_lin1.nii.gz
threshold=0
function_with_arguments=('call_gray2binary' ${mask_binary_output_dir}/${csf_binary_output_filename}  ${mask_binary_output_dir} ${threshold})
echo "outputfiles_present="'$(python3 utilities_simple_trimmed.py' "${function_with_arguments[@]}"
outputfiles_present=$(python3 utilities_simple_trimmed.py "${function_with_arguments[@]}")
BET_csf_binary_output_filename=${mask_binary_output_dir}/${csf_binary_output_filename%.nii*}_BET.nii.gz

#########################################
snipr_output_foldername="PREPROCESS_SEGM_1"
#snipr_output_foldername='PREPROCESS_SEGM'
function_with_arguments=('call_delete_file_with_ext' ${sessionID} ${scanID} ${snipr_output_foldername} '.nii.gz' ) ##'warped_1_mov_mri_region_' )
echo "outputfiles_present="'$(python3 utilities_simple_trimmed.py' "${function_with_arguments[@]}"
#outputfiles_present=$(python3 download_with_session_ID.py "${function_with_arguments[@]}")
function_with_arguments=('call_delete_file_with_ext' ${sessionID} ${scanID} ${snipr_output_foldername} '.mat' ) ##'warped_1_mov_mri_region_' )
echo "outputfiles_present="'$(python3 utilities_simple_trimmed.py' "${function_with_arguments[@]}"
#outputfiles_present=$(python3 download_with_session_ID.py "${function_with_arguments[@]}")

#    sessionId=str(sys.argv[1])
#    scanId=str(sys.argv[2])
#    input_dirname=str(sys.argv[3])
#    resource_dirname=str(sys.argv[4])
#    file_name=str(sys.argv[5])
#/software/bet_withlevelset.sh ${registration_nii_file} ${BET_bet_binary_output_filename}  ##${mask_binary_output_dir}/${bet_binary_output_filename%.nii*}_BET.nii.gz
#betgray_of_session_ct_regis=${mask_binary_output_dir}/$(basename ${registration_nii_file%.nii*}_brain_f.nii.gz)
#full_image_filename=${registration_nii_file}
#full_image_filename_betgray=${mask_binary_output_dir}/$(basename ${full_image_filename%.nii*}_brain_f.nii.gz)

#uploadsinglefile ${sessionID} ${scanID} ${mask_binary_output_dir} ${snipr_output_foldername} ${bet_binary_output_filename%.nii*}_BET.nii.gz
#uploadsinglefile ${sessionID} ${scanID} $(dirname ${betgray_of_session_ct_regis}) ${snipr_output_foldername} $(basename  ${betgray_of_session_ct_regis})
snipr_output_foldername="PREPROCESS_SEGM_1"
#uploadsinglefile ${sessionID} ${scanID} $(dirname ${BET_bet_binary_output_filename}) ${snipr_output_foldername} $(basename  ${BET_bet_binary_output_filename})
#uploadsinglefile ${sessionID} ${scanID} $(dirname ${infarct_mask_binary_output_filename}) ${snipr_output_foldername} $(basename  ${infarct_mask_binary_output_filename})
uploadsinglefile ${sessionID} ${scanID} $(dirname ${BET_csf_binary_output_filename}) ${snipr_output_foldername} $(basename  ${BET_csf_binary_output_filename})
uploadsinglefile ${sessionID} ${scanID} ${output_directory} ${snipr_output_foldername} $(basename ${registration_mat_file})
uploadsinglefile ${sessionID} ${scanID} ${output_directory} ${snipr_output_foldername} $(basename  ${registration_nii_file})
#uploadsinglefile ${sessionID} ${scanID} "/software" ${snipr_output_foldername} $(basename  ${fixed_image_filename} )

uploadsinglefile ${sessionID} ${scanID} $(dirname ${fixed_image_filename}) ${snipr_output_foldername} $(basename  ${fixed_image_filename})
#
##file_suffixes=( ${mask_binary_output_filename%.nii*} ) #sys.argv[5]
##for file_suffix in ${file_suffixes[@]}; do
##copyoutput_with_prefix_to_snipr ${sessionID} ${scanID} "${mask_binary_output_dir}" ${snipr_output_foldername} ${file_suffix}
##done
#file_suffixes=( $(basename  ${fixed_image_filename%.nii*} ) ) #sys.argv[5]
#for file_suffix in ${file_suffixes[@]}; do
#copyoutput_with_prefix_to_snipr ${sessionID} ${scanID} "/software" ${snipr_output_foldername} ${file_suffix}
#done
#file_suffixes=( $(basename  ${registration_mat_file%.mat*} ) ) #sys.argv[5]
#for file_suffix in ${file_suffixes[@]}; do
#copyoutput_with_prefix_to_snipr ${sessionID} ${scanID} "${output_directory}" ${snipr_output_foldername} ${file_suffix}
#done
##      mask_binary_output_dir='/input1' ##/software/mritemplate/NONLINREGTOCT/BETS'
##      Transform grayscale bet
#
#
##T_output_filename=$(ls ${output_directory}/mov_${nifti_file_without_ext}*.mat) #$(ls ${working_dir}/${nifti_file_without_ext}*_resaved_levelset_brain_f_${template_prefix}lin1.mat )
##      /software/linear_rigid_registration_onlytrasnformwith_matfile10162024.sh  ${moving_image_filename} ${fixed_image_filename} ${T_output_filename} ${mask_binary_output_dir}


# transform infarct mask
#      fixed_image_filename=/software/${template_prefix}.nii.gz ##${session_ct_bet_gray}
#      moving_image_filename=${output_directory}/${nifti_file_without_ext}_resaved_infarct_auto_removesmallresampled_normalized_mov.nii.gz #$(ls ${output_directory}/*_resaved_infarct_auto_removesmall.nii.gz)
##      T_output_filename=$(ls ${working_dir}/${nifti_file_without_ext}*_resaved_levelset_brain_f_${template_prefix}lin1.mat )
#      /software/linear_rigid_registration_onlytrasnformwith_matfile10162024.sh  ${moving_image_filename} ${fixed_imnormalized_fixed_file_nameage_filename} ${T_output_filename} ${mask_binary_output_dir}
#      moving_image_output_filename=$(ls ${output_directory}/mov_*${nifti_file_without_ext}_resaved_infarct_auto_removesmallresampled_normalized_mov* ) ## #$(ls ${mask_binary_output_dir}/mov*_resaved_infarct_auto_removesmall*.nii.gz)
#      threshold=0
#      function_with_arguments=('call_gray2binary' ${moving_image_output_filename}  ${mask_binary_output_dir} ${threshold})
#      echo "outputfiles_present="'$(python3 utilities_simple_trimmed.py' "${function_with_arguments[@]}"
#      outputfiles_present=$(python3 utilities_simple_trimmed.py "${function_with_arguments[@]}")
#      snipr_output_foldername="PREPROCESS_SEGM"
#      file_suffixes=( mov ) #sys.argv[5]
#      for file_suffix in ${file_suffixes[@]}; do
#        copyoutput_with_prefix_to_snipr ${sessionID} ${scanID} "${working_dir_1}" ${snipr_output_foldername} ${file_suffix}
#      done
######################################################################################################################
echo " FILES NOT PRESENT I AM WORKING ON IT"
else
echo " FILES ARE PRESENT "
#######################################################################################################################
fi
##

done < <(tail -n +2 "${niftifile_csvfilename}")
done

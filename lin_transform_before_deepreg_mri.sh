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
templatefilename=scct_strippedResampled1.nii.gz
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
## KEEP THE SCAN ID FIXED as 'MRI1, KEEP MASKSLABEL name fixed, NIFTI is already fixed. Session ID is given
scanID='MRI1'
snipr_output_foldername='PREPROCESS_SEGM'
function_with_arguments=('call_delete_file_with_ext' ${sessionID} ${scanID} ${snipr_output_foldername} '.nii.gz' 'warped_1_mov_mri_region_' )
echo "outputfiles_present="'$(python3 download_with_session_ID.py' "${function_with_arguments[@]}"
outputfiles_present=$(python3 download_with_session_ID.py "${function_with_arguments[@]}")
# download the niftifile
#sessionID=$sessionID, scanID=$scanID , resource_dir=NIFTI
# get metadata of this session
function_with_arguments=('call_downloadfiletolocaldir_py' ${sessionID}  ${scanID} NIFTI ${working_dir_1})
echo "outputfiles_present="'$(python3 download_with_session_ID.py' "${function_with_arguments[@]}"
outputfiles_present=$(python3 download_with_session_ID.py "${function_with_arguments[@]}")
function_with_arguments=('call_downloadfiletolocaldir_py' ${sessionID}  ${scanID} MASKLABEL ${working_dir_1})
echo "outputfiles_present="'$(python3 download_with_session_ID.py' "${function_with_arguments[@]}"
outputfiles_present=$(python3 download_with_session_ID.py "${function_with_arguments[@]}")
# Get the scan ID
#### normalize and resample the grayscale image
## DOWNLOAD TEMPLATE FILES FROM SNIPR
###################NORMALIZE THE MOVING IMAGE#######################
moving_image_filename_mrigray=$(ls ${working_dir_1}/*bfc.nii*) #/software/mritemplate1/original/'BCI-DNI_brain_bfc.nii.gz'
fixed_image_filename=/software/scct_strippedResampled1.nii.gz ##${session_ct_bet_gray}
function_with_arguments=('call_normalization_N_resample_to_fixed' ${moving_image_filename_mrigray}  ${fixed_image_filename} )
echo "outputfiles_present="'$(python3 utilities_simple_trimmed.py' "${function_with_arguments[@]}"
outputfiles_present=$(python3 utilities_simple_trimmed.py "${function_with_arguments[@]}")
#
############################### REGISTRATION OF THE MOVING IMAGE## image and get matrix
normalized_fixed_file_name=${fixed_image_filename%.nii*}'_normalized_fix.nii.gz'  #} ##
moving_image_filename_mrigray_norm=${moving_image_filename_mrigray%.nii*}resampled_normalized_mov.nii.gz
/software/linear_rigid_registration_v10162024.sh ${moving_image_filename_mrigray_norm}  ${normalized_fixed_file_name} ${output_directory}
moving_image_filename_mrigray_reg_output=${output_directory}/mov_$(basename ${moving_image_filename_mrigray_norm%.nii*}_fixed_$(basename ${normalized_fixed_file_name%.nii*}_lin1.nii.gz))
moving_image_filename_mrigray_reg_mat_output=${output_directory}/mov_$(basename ${moving_image_filename_mrigray_norm%.nii*}_fixed_$(basename ${normalized_fixed_file_name%.nii*}_lin1.mat))

######################### REGISTRATION OF THE MASKS #####################
#
##### resample the region masks image
moving_image_filename_mrilabel=$(ls ${working_dir_1}/*label*) #/software/mritemplate1/original/'BCI-DNI_brain_label.nii.gz'  #${output_directory}/${session_ct_bname_noext}_resaved_infarct_auto_removesmall.nii.gz
#############################
masks_output_directory=${working_dir}
function_with_arguments=('call_separate_masks_from_multivalue_mask' ${moving_image_filename_mrilabel} ${masks_output_directory}  )
echo "outputfiles_present="'$(python3 utilities_simple_trimmed.py' "${function_with_arguments[@]}"
outputfiles_present=$(python3 utilities_simple_trimmed.py "${function_with_arguments[@]}")

masks_label_pattern=${masks_output_directory}/$(basename ${moving_image_filename_mrilabel%.nii*})
file_count=1
mask_binary_output_dir='/input1'
for each_mask_label_file in ${masks_label_pattern}_*.nii*  ; do  ###*.gz
echo each_mask_label_file::${each_mask_label_file}
this_mask_file=${each_mask_label_file}  ##_${file_count}.nii.gz
if [[ -f ${this_mask_file} ]] ; then
  echo ${this_mask_file}
function_with_arguments=('call_only_resample_to_fixed' ${this_mask_file}  ${fixed_image_filename} )
echo "outputfiles_present="'$(python3 utilities_simple_trimmed.py' "${function_with_arguments[@]}"
outputfiles_present=$(python3 utilities_simple_trimmed.py "${function_with_arguments[@]}")
moving_image_filename_mrilabel_resample=${this_mask_file%.nii*}resampled_mov.nii.gz
#mv ${moving_image_filename_mrilabel_resample} ${working_dir}/
#moving_image_filename_mrilabel_resample=${working_dir}/$(basename ${this_mask_file%.nii*}resampled_mov.nii.gz)
/software/linear_rigid_registration_onlytrasnformwith_matfile10162024.sh  ${moving_image_filename_mrilabel_resample} ${normalized_fixed_file_name} ${moving_image_filename_mrigray_reg_mat_output} ${mask_binary_output_dir}
fi
done

snipr_output_foldername='PREPROCESS_LINR'
all_moved_files=$(find ${mask_binary_output_dir} -name 'mov_'* )
for file in ${all_moved_files} ; do
echo $file
thresh=0
function_with_arguments=('call_gray2binary' ${file}  $(dirname ${file}) thresh )
echo "outputfiles_present="'$(python3 utilities_simple_trimmed.py' "${function_with_arguments[@]}"
outputfiles_present=$(python3 utilities_simple_trimmed.py "${function_with_arguments[@]}")
file1=${file%.nii*}_BET.nii.gz
echo "uploadsinglefile ${sessionID} ${scanID} $(dirname ${file}) ${snipr_output_foldername} $(basename ${file} )"
uploadsinglefile ${sessionID} ${scanID} $(dirname ${file1}) ${snipr_output_foldername} $(basename ${file1} )
done
all_moved_files=$(find ${output_directory} -name 'mov_'* )
for file in ${all_moved_files} ; do
echo $file
echo "uploadsinglefile ${sessionID} ${scanID} $(dirname ${file}) ${snipr_output_foldername} $(basename ${file} )"
uploadsinglefile ${sessionID} ${scanID} $(dirname ${file}) ${snipr_output_foldername} $(basename ${file} )
done
file='/software/scct_strippedResampled1_normalized_fix.nii.gz'
uploadsinglefile ${sessionID} ${scanID} $(dirname ${file}) NIFTI $(basename ${file} )

function_with_arguments=('call_delete_file_with_ext' ${sessionID} ${scanID} ${snipr_output_foldername} '*.nii.gz' 'warped_1_mov_mri_region_' )
echo "outputfiles_present="'$(python3 utilities_simple_trimmed.py' "${function_with_arguments[@]}"
outputfiles_present=$(python3 utilities_simple_trimmed.py "${function_with_arguments[@]}")
#
##

#
#done
#echo "uploadsinglefile ${sessionID} ${scanID} $(dirname  ${normalized_fixed_file_name})  ${snipr_output_foldername} $(basename ${normalized_fixed_file_name} )"
#uploadsinglefile ${sessionID} ${scanID} $(dirname  ${normalized_fixed_file_name}) ${snipr_output_foldername} $(basename ${normalized_fixed_file_name} )


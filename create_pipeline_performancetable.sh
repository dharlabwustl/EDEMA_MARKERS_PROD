#!/bin/bash
export XNAT_USER=${2} 
export XNAT_PASS=${3} 
export XNAT_HOST=${4} 
sessionID=${1}
project_ID=${1}
working_dir=/workinginput 
output_directory=/workingoutput

final_output_directory=/outputinsidedocker

copyoutput_to_snipr(){
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
uploadfile()" ${sessionID} ${scanID} ${output_dir} ${resource_dirname} ${file_suffix}  # ${infarctfile_present}  ##$static_template_image $new_image $backslicenumber #$single_slice_filename

}


copy_masks_data() {
echo " I AM IN copy_masks_data "
# rm -r /ZIPFILEDIR/*
sessionID=${1}
scanID=${2}
resource_dirname=${3} #str(sys.argv[4])
output_dirname=${4}  #str(sys.argv[3])
echo output_dirname::${output_dirname}
python3 -c "
import sys
sys.path.append('/software');
from download_with_session_ID import *;
downloadfiletolocaldir()" ${sessionID}  ${scanID}  ${resource_dirname}  ${output_dirname}    ### ${infarctfile_present}  ##$static_template_image $new_image $backslicenumber #$single_slice_filename


}

call_get_resourcefiles_metadata_saveascsv(){
    URI=${1}
    resource_dir=${2}
    dir_to_receive_the_data=${3}
    output_csvfile=${4}
python3 -c "
import sys
sys.path.append('/software');
from download_with_session_ID import *;
call_get_resourcefiles_metadata_saveascsv()" ${URI} ${resource_dir} ${dir_to_receive_the_data} ${output_csvfile}
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
get_relevantfile_in_A_DIRECTORY()" ${sessionID}  ${dir_to_receive_the_data} ${resource_dir}

}


run_IML_NWU_CSF_CALC()

{
this_filename=${1}
this_betfilename=${2}
this_csfmaskfilename=${3}
this_infarctmaskfilename=${4}
this_infarctmask1filename=${5}
echo "this_filename=${1}
      this_betfilename=${2}
      this_csfmaskfilename=${3}
      this_infarctmaskfilename=${4}
      this_infarctmask1filename=${5}"
echo "BET USING LEVELSET MASK"

/software/bet_withlevelset.sh $this_filename ${this_betfilename} #${output_directory} #Helsinki2000_1019_10132014_1048_Head_2.0_ax_Tilt_1_levelset # ${3} # Helsinki2000_702_12172013_2318_Head_2.0_ax_levelset.nii.gz #${3} # $6 $7 $8 $9 ${10}

echo "bet_withlevelset successful" > ${output_directory}/success.txt
this_filename_brain=${this_filename%.nii*}_brain_f.nii.gz
# cp ${this_filename_brain} ${output_directory}/ #  ${final_output_directory}/
echo "LINEAR REGISTRATION TO TEMPLATE"
/software/linear_rigid_registration.sh ${this_filename_brain} #${templatefilename} #$3 ${6} WUSTL_233_11122015_0840__levelset_brain_f.nii.gz
echo "linear_rigid_registration successful" >> ${output_directory}/success.txt
echo "RUNNING IML FSL PART"
/software/ideal_midline_fslpart.sh ${this_filename} # ${templatefilename} ${mask_on_template}  #$9 #${10} #$8
echo "ideal_midline_fslpart successful" >> ${output_directory}/success.txt
echo "RUNNING IML PYTHON PART"

/software/ideal_midline_pythonpart.sh  ${this_filename} #${templatefilename}  #$3 #$8 $9 ${10}
echo "ideal_midline_pythonpart successful" >> ${output_directory}/success.txt

echo "RUNNING ICH volume calculation for class 2 Mask"

/software/ich_csf_volume.sh  ${this_filename}   ${this_betfilename} ${this_csfmaskfilename} ${this_infarctmaskfilename}  ${this_infarctmask1filename}  #${upper_threshold}
echo "ich_csf_volume successful" >> ${output_directory}/success.txt
thisfile_basename=$(basename $this_filename)
# for texfile in $(/usr/lib/fsl/5.0/remove_ext ${output_directory}/$thisfile_basename)*.tex ;
for texfile in  ${output_directory}/*.tex ;
do
pdflatex -halt-on-error -interaction=nonstopmode   -output-directory=${output_directory} $texfile  ##${output_directory}/$(/usr/lib/fsl/5.0/remove_ext $this_filename)*.tex
rm ${output_directory}/*.aux
rm ${output_directory}/*.log
done
#
for filetocopy in $(/usr/lib/fsl/5.0/remove_ext ${output_directory}/$thisfile_basename)*_brain_f.nii.gz ;
do
cp ${filetocopy} ${final_output_directory}/
done

for filetocopy in $(/usr/lib/fsl/5.0/remove_ext ${output_directory}/$thisfile_basename)*.mat ;
do
cp ${filetocopy} ${final_output_directory}/
done

for filetocopy in ${output_directory}/*.pdf ;
do
cp ${filetocopy} ${final_output_directory}/
done
for filetocopy in  ${output_directory}/*.csv ;
do
cp ${filetocopy} ${final_output_directory}/
done

}

ich_calculation_each_scan(){


eachfile_basename_noext=''
originalfile_basename=''
original_ct_file=''
for eachfile in ${working_dir}/*.nii ;
do
original_ct_file=${eachfile}
eachfile_basename=$(basename ${eachfile})
originalfile_basename=${eachfile_basename}
eachfile_basename_noext=${eachfile_basename%.nii*}


############## files basename ################################## 	ICH_0001_01012017_1028_2_resaved_4DL_normalized_class1.nii.gz  114 KB
grayfilename=${eachfile_basename_noext}_resaved_levelset.nii
betfilename=${eachfile_basename_noext}_resaved_levelset_bet.nii.gz
csffilename=${eachfile_basename_noext}_resaved_csf_unet.nii.gz
infarctfilename=${eachfile_basename_noext}_resaved_4DL_normalized_class1.nii.gz #_resaved_infarct_auto_removesmall.nii.gz
infarctfilename1=${eachfile_basename_noext}_resaved_4DL_normalized_class2.nii.gz #_resaved_infarct_auto_removesmall.nii.gz
################################################
############## copy those files to the docker image ##################################
cp ${working_dir}/${betfilename}  ${output_directory}/
cp ${working_dir}/${csffilename}  ${output_directory}/
cp ${working_dir}/${infarctfilename}  ${output_directory}/
cp ${working_dir}/${infarctfilename1}  ${output_directory}/
####################################################################################
source /software/bash_functions_forhost.sh

cp ${original_ct_file}  ${output_directory}/${grayfilename}
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
from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${original_ct_file}"  "${levelset_infarct_mask_file}"  "${output_directory}"

####################################################################
levelset_infarct_mask_file1=${output_directory}/${infarctfilename1}
echo "levelset_infarct_mask_file:${levelset_infarct_mask_file1}"
## preprocessing infarct mask:
python3 -c "
import sys ;
sys.path.append('/software/') ;
from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${original_ct_file}"  "${levelset_infarct_mask_file1}"  "${output_directory}"

######################################################################

## preprocessing bet mask:
levelset_bet_mask_file=${output_directory}/${betfilename}
echo "levelset_bet_mask_file:${levelset_bet_mask_file}"
python3 -c "

import sys ;
sys.path.append('/software/') ;
from utilities_simple_trimmed import * ;  levelset2originalRF_new_flip()" "${original_ct_file}"  "${levelset_bet_mask_file}"  "${output_directory}"

#### preprocessing csf mask:
levelset_csf_mask_file=${output_directory}/${csffilename}
echo "levelset_csf_mask_file:${levelset_csf_mask_file}"
python3 -c "
import sys ;
sys.path.append('/software/') ;
from utilities_simple_trimmed import * ;   levelset2originalRF_new_flip()" "${original_ct_file}"  "${levelset_csf_mask_file}"  "${output_directory}"


lower_threshold=0
upper_threshold=20
templatefilename=scct_strippedResampled1.nii.gz
mask_on_template=midlinecssfResampled1.nii.gz




x=$grayimage
bet_mask_filename=${output_directory}/${betfilename}
infarct_mask_filename=${output_directory}/${infarctfilename}
infarct_mask_filename1=${output_directory}/${infarctfilename1}
csf_mask_filename=${output_directory}/${csffilename}
echo  " FILENMAES:: $x ${bet_mask_filename} ${csf_mask_filename} ${infarct_mask_filename}  ${infarct_mask_filename1}"
run_IML_NWU_CSF_CALC  $x ${bet_mask_filename} ${csf_mask_filename} ${infarct_mask_filename}  ${infarct_mask_filename1}


done


# for f in ${output_directory}/*; do
#     # if [ -d "$f" ]; then
#         # $f is a directory
#         rm -r $f
#     # fi
# done

}



# #####################################################
get_nifti_scan_uri(){
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
call_decision_which_nifti()" ${sessionID}  ${working_dir} ${output_csvfile}

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
downloadniftiwithuri_withcsv()" ${csvfilename}  ${dir_to_save}


}


getmaskfilesscanmetadata()
{
# def get_maskfile_scan_metadata():
sessionId=${1} #sys.argv[1]
scanId=${2} # sys.argv[2]
resource_foldername=${3} # sys.argv[3]
dir_to_save=${4} # sys.argv[4]
csvfilename=${5} # sys.argv[5]
python3 -c "
import sys
sys.path.append('/software');
from download_with_session_ID import *;
get_maskfile_scan_metadata()" ${sessionId}  ${scanId}  ${resource_foldername} ${dir_to_save} ${csvfilename}
}
combine_all_csvfiles_general()
{
working_directory=${1}
working_directory_tocombinecsv=${2}
extension=${3}
outputfilename=${4}


python3 -c "
import sys
sys.path.append('/software');
from download_with_session_ID import *;
call_combine_all_csvfiles_general()"  ${working_directory} ${working_directory_tocombinecsv} ${extension} ${outputfilename}
}
#########################################################################
## GET THE SINGLE CT NIFTI FILE NAME AND COPY IT TO THE WORKING_DIR
listofsession=${final_output_directory}/'sessions.csv'
#project_ID="COLI"
curl  -u   $XNAT_USER:$XNAT_PASS  -X GET   $XNAT_HOST/data/projects/${project_ID}/experiments/?format=csv  > ${listofsession}

counter=0
while IFS=',' read -ra array; do
echo "${array[0]}"
sessionID_1="${array[1]}"
echo final_output_directory::${final_output_directory}
niftifile_csvfilename=${working_dir}/${sessionID_1}'this_session_final_ct.csv'
get_nifti_scan_uri ${sessionID_1}  ${working_dir} ${niftifile_csvfilename}
if [ -f ${niftifile_csvfilename} ]; then
    echo "$niftifile_csvfilename exists."
    cp ${niftifile_csvfilename} ${final_output_directory}
    #############
    resource_dirname='MASKS'
    output_dirname=${final_output_directory}
    while IFS=',' read -ra array; do
    scanID=${array[2]}
    echo sessionId::${sessionID}
    echo scanId::${scanID}
      output_csvfile=${array[1]}
      output_csvfile=${output_csvfile%.nii*}${resource_dirname}.csv
    echo scanId::${array[0]}::${array[1]}::${array[2]}::${array[3]}::${array[4]}::${output_csvfile}
    URI=${array[0]}
    resource_dir=${resource_dirname}
    dir_to_receive_the_data=${final_output_directory}

    call_get_resourcefiles_metadata_saveascsv ${URI} ${resource_dir} ${dir_to_receive_the_data} ${output_csvfile}

    resource_dir="EDEMA_BIOMARKER"
    output_csvfile=${array[1]}
    output_csvfile=${output_csvfile%.nii*}${resource_dirname}.csv
    call_get_resourcefiles_metadata_saveascsv ${URI} ${resource_dir} ${dir_to_receive_the_data} ${output_csvfile}

    resource_dir="ICH_QUANTIFICATION"
    output_csvfile=${array[1]}
    output_csvfile=${output_csvfile%.nii*}${resource_dirname}.csv
    call_get_resourcefiles_metadata_saveascsv ${URI} ${resource_dir} ${dir_to_receive_the_data} ${output_csvfile}
    done < <( tail -n +2 "${niftifile_csvfilename}" )

    ###################

    counter=$((counter+1))
fi
if [[ $counter -gt 1 ]] ; then
  break
fi


#copy_latest_pdfs "ICH" ${working_dir} ${final_output_directory}
done < <( tail -n +2 "${listofsession}" )
#extension_csv='csv'
#combined_csv_outputfilename=${final_output_directory}/${project_ID}"_NIFTILIST_COMBINED.csv"
#combine_all_csvfiles_general  ${final_output_directory} ${final_output_directory} ${extension_csv} ${combined_csv_outputfilename}
#################################################
#
##get_nifti_scan_uri ${sessionID}  ${working_dir} ${niftifile_csvfilename}
##copy_scan_data ${niftifile_csvfilename} ${working_dir}
#
#
#
#
################################################################################################################
#
### GET THE RESPECTIVS MASKS NIFTI FILE NAME AND COPY IT TO THE WORKING_DIR
#
######################################################################################
#resource_dirname='MASKS'
#output_dirname=${working_dir}
#while IFS=',' read -ra array; do
#scanID=${array[2]}
#echo sessionId::${sessionID}
#echo scanId::${scanID}
##call_get_resourcefiles_metadata_saveascsv ${URI} ${resource_dir} ${dir_to_receive_the_data} ${output_csvfile}
#done < <( tail -n +2 "${niftifile_csvfilename}" )
#echo working_dir::${working_dir}
#echo output_dirname::${output_dirname}
#copy_masks_data   ${sessionID}  ${scanID} ${resource_dirname} ${output_dirname}
#######################################################################################################################
### CALCULATE EDEMA BIOMARKERS
#ich_calculation_each_scan
#######################################################################################################################
### COPY IT TO THE SNIPR RESPECTIVE SCAN RESOURCES
#snipr_output_foldername="ICH_QUANTIFICATION"
#file_suffixes=(  .pdf .mat .csv ) #sys.argv[5]
#for file_suffix in ${file_suffixes[@]}
#do
#    copyoutput_to_snipr  ${sessionID} ${scanID} "${final_output_directory}"  ${snipr_output_foldername}  ${file_suffix}
#done
#######################################################################################################################
#

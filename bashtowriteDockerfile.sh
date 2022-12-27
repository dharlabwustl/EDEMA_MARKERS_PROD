#!/usr/bin/env bash
parent_dir=${1}
echo 'FROM sharmaatul11/fsl502py369ltx-full:latest' > ${parent_dir}/Dockerfile
# FROM ubuntu:latest
##sharmaatul11/py310xmltodict:latest 
#ubuntu:latest 
directory_of_software='software'
echo 'RUN apt update' >> ${parent_dir}/Dockerfile
echo "RUN mkdir  -p  ${directory_of_software}" >> ${parent_dir}/Dockerfile
echo "RUN chmod  -R  777 ${directory_of_software}" >> ${parent_dir}/Dockerfile
# echo 'RUN mkdir -p /run' >> ${parent_dir}/Dockerfile
# echo 'RUN mkdir -p /ZIPFILEDIR' >> ${parent_dir}/Dockerfile
# echo 'RUN chmod -R 777 /ZIPFILEDIR' >> ${parent_dir}/Dockerfile
# echo 'RUN mkdir -p /NIFTIFILEDIR' >> ${parent_dir}/Dockerfile
# echo 'RUN chmod -R 777 /NIFTIFILEDIR' >> ${parent_dir}/Dockerfile
# cat createdirectories.txt >> ${parent_dir}/Dockerfile
echo "COPY ${parent_dir}/scct_strippedResampled1.nii.gz   /templatenifti/" >> ${parent_dir}/Dockerfile
echo "COPY  ${parent_dir}/midlinecssfResampled1.nii.gz   /templatemasks/" >> ${parent_dir}/Dockerfile
ubuntupackagestoinstall=(dcm2niix vim zip unzip curl tree)
echo ${ubuntupackagestoinstall[0]}
len_array=${#ubuntupackagestoinstall[@]}
last_num=$((len_array -1))
echo $last_num
echo "RUN apt install -y \\" >> ${parent_dir}/Dockerfile 
for x in ${ubuntupackagestoinstall[@]} ; do 
	if [[ $x = ${ubuntupackagestoinstall[last_num]} ]] ; then
		echo "  ${x}  " >> ${parent_dir}/Dockerfile
	else 
		echo "  ${x}  \\ " >> ${parent_dir}/Dockerfile
fi 
done


pipinstall=(nibabel numpy xmltodict pandas requests pydicom python-gdcm glob2 scipy pypng PyGithub)
len_array=${#pipinstall[@]}
last_num=$((pipinstall -1))
echo "RUN pip install \\" >> ${parent_dir}/Dockerfile 
for x in ${pipinstall[@]} ; do 
	if [[ $x = ${pipinstall[last_num]} ]] ; then
		echo "  ${x}  " >> ${parent_dir}/Dockerfile
	else 
		echo "  ${x}  \\ " >> ${parent_dir}/Dockerfile
fi 
done


# copyfiles_sh=(dicom2nifti_call_projectlevel_selected  dicom2nifti_call_scanlevel_selected  dicom2nifti_call_sessionlevel_selected dicom2nifti_call_subjectlevel_selected)
# len_array=${#copyfiles_sh[@]}
# last_num=$((copyfiles_sh -1))
# echo "COPY  \\" >> ${parent_dir}/Dockerfile 
# for x in ${copyfiles_sh[@]} ; do 
 
# 		echo "  ${x}.sh  \\ " >> ${parent_dir}/Dockerfile

# done
# echo "/run/  " >> ${parent_dir}/Dockerfile 
# copyfiles_sh=(dicom2nifti_call_projectlevel_selected  dicom2nifti_call_scanlevel_selected  dicom2nifti_call_sessionlevel_selected dicom2nifti_call_subjectlevel_selected)
# len_array=${#copyfiles_sh[@]}
# last_num=$((copyfiles_sh -1))
echo "COPY  \\" >> ${parent_dir}/Dockerfile 
for x in ${parent_dir}/*.sh; do
 
		echo "  ${x}  \\ " >> ${parent_dir}/Dockerfile

done
echo "/${directory_of_software}/  " >> ${parent_dir}/Dockerfile 

# copyfiles_py=(dicom2nifiti_projectlevel_selected dicom2nifiti_subjectlevel_selected dicom2nifiti_subjectlevel_selected  dicom2nifiti_alllevels_selected dicom2nifiti_projectlevel_selected dicom2nifiti_sessionlevel_selected dicom2nifiti_scanlevel_selected DecompressDCM dicom2nifiti_sessionlevel xnatSession dicom2nifiti_scanlevel writetowebpagetable label_session_Atul downloadwithrequest label_probability)
# len_array=${#copyfiles_py[@]}
# last_num=$((copyfiles_py -1))
echo "COPY  \\" >> ${parent_dir}/Dockerfile 
for x in ${parent_dir}/*.py ; do
 
		echo "  ${x}  \\ " >> ${parent_dir}/Dockerfile

done
echo "/${directory_of_software}/  " >> ${parent_dir}/Dockerfile 
# echo "COPY stroke_edema_template.xml /run/" >> ${parent_dir}/Dockerfile

# changemodes_sh=(dicom2nifti_call_projectlevel_selected dicom2nifti_call_subjectlevel_selected dicom2nifti_call_subjectlevel_selected dicom2nifti_call_alllevels_selected dicom2nifti_call_projectlevel_selected dicom2nifti_call_sessionlevel_selected dicom2nifti_call_scanlevel_selected dicom2nifti_call_scanlevel writetowebpagetable_call  label_session_call  call_downloadwithrequest )

# len_array=${#changemodes_sh[@]}
# last_num=$((changemodes_sh -1))
echo "RUN  \\" >> ${parent_dir}/Dockerfile 
# for x in ${changemodes_sh[@]} ; do 
counter=0

total_num_sh_files=$(ls -l *.sh | grep ^- | wc -l)
total_num_sh_files=$((total_num_sh_files-1))
for x in ${parent_dir}/*.sh ; do
	# if [[ $x = ${changemodes_sh[last_num]} ]] ; then
		if [[ $counter -eq ${total_num_sh_files} ]] ; then
		echo " chmod +x  /${directory_of_software}/${x}  " >> ${parent_dir}/Dockerfile
	else 
		echo " chmod +x /${directory_of_software}/${x}  &\\ " >> ${parent_dir}/Dockerfile
fi 
counter=$((counter+1))
done


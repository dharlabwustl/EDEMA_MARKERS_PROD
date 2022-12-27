FROM sharmaatul11/fsl502py369ltx-full:latest
RUN apt update
RUN mkdir  -p  software
RUN chmod  -R  777 software
COPY /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/scct_strippedResampled1.nii.gz   /templatenifti/
COPY  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/midlinecssfResampled1.nii.gz   /templatemasks/
RUN apt install -y \
  dcm2niix  \ 
  vim  \ 
  zip  \ 
  unzip  \ 
  curl  \ 
  tree  
RUN pip install \
  nibabel  \ 
  numpy  \ 
  xmltodict  \ 
  pandas  \ 
  requests  \ 
  pydicom  \ 
  python-gdcm  \ 
  glob2  \ 
  scipy  \ 
  pypng  \ 
  PyGithub  
COPY  \
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/bash_functions_forhost.sh  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/bashtowriteDockerfile1.sh  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/bashtowriteDockerfile.sh  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/bet_linreg_midline_nwu.sh  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/bet_linr_midlinereg_fsl_snipr_04142022.sh  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/bet_withlevelset.sh  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/builddockerimage.sh  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/combine_csvs_and_copy_pdfs_projectlevel_Nov15_2022.sh  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/combineCSVs.sh  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/dicom2nifti_call_sessionlevel_selected.sh  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/downloadcodefromgithub.sh  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/ideal_midline_fslpart.sh  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/ideal_midline_pythonpart.sh  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/linear_rigid_registration.sh  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/nwucalculation_scan_level_allsteps.sh  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/nwucalculation_session_level_allsteps_November14_2022.sh  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/nwucalculation_session_level_allsteps_November2_2022.sh  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/nwu_csf_volumeBASELINE.sh  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/nwu_csf_volume.sh  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/rundockercommand_fordcm2nifti.sh  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/rundockercommand.sh  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/script_to_call_main_program.sh  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/test.sh  \ 
/software/  
COPY  \
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/combineCSVs.py  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/DecompressDCM.py  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/dicom2nifiti_sessionlevel_selected.py  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/download_with_session_ID.py  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/github_dealing.py  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/hello.py  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/module_midline1.py  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/module_NWU_CSFCompartment_CalculationsBASELINE.py  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/module_NWU_CSFCompartment_Calculations.py  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/utilitiesforyashengsdocker.py  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/utilities_simple.py  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/utilities_simple_trimmed.py  \ 
  /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/xnatSession.py  \ 
/software/  
RUN  \
 chmod +x /software//media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/bash_functions_forhost.sh  &\ 
 chmod +x /software//media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/bashtowriteDockerfile1.sh  &\ 
 chmod +x /software//media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/bashtowriteDockerfile.sh  &\ 
 chmod +x /software//media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/bet_linreg_midline_nwu.sh  &\ 
 chmod +x /software//media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/bet_linr_midlinereg_fsl_snipr_04142022.sh  &\ 
 chmod +x /software//media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/bet_withlevelset.sh  &\ 
 chmod +x /software//media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/builddockerimage.sh  &\ 
 chmod +x /software//media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/combine_csvs_and_copy_pdfs_projectlevel_Nov15_2022.sh  &\ 
 chmod +x /software//media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/combineCSVs.sh  &\ 
 chmod +x /software//media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/dicom2nifti_call_sessionlevel_selected.sh  &\ 
 chmod +x /software//media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/downloadcodefromgithub.sh  &\ 
 chmod +x /software//media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/ideal_midline_fslpart.sh  &\ 
 chmod +x /software//media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/ideal_midline_pythonpart.sh  &\ 
 chmod +x /software//media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/linear_rigid_registration.sh  &\ 
 chmod +x /software//media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/nwucalculation_scan_level_allsteps.sh  &\ 
 chmod +x /software//media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/nwucalculation_session_level_allsteps_November14_2022.sh  &\ 
 chmod +x /software//media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/nwucalculation_session_level_allsteps_November2_2022.sh  &\ 
 chmod +x /software//media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/nwu_csf_volumeBASELINE.sh  &\ 
 chmod +x /software//media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/nwu_csf_volume.sh  &\ 
 chmod +x /software//media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/rundockercommand_fordcm2nifti.sh  &\ 
 chmod +x /software//media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/rundockercommand.sh  &\ 
 chmod +x /software//media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/script_to_call_main_program.sh  &\ 
 chmod +x  /software//media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/test.sh  
LABEL org.nrg.commands="[{\"name\": \"dicom2niftiusingGitHub\", \"description\": \"Apply dicom2niftiusingGitHub\", \"version\": \"1.0\", \"schema-version\": \"1.0\", \"image\": \"sharmaatul11/dicom2nifti_nwu_1:latest\", \"type\": \"docker\", \"working-directory\": \"/callfromgithub\", \"command-line\": \" /callfromgithub/downloadcodefromgithub.sh #SESSION_ID# \$XNAT_USER \$XNAT_PASS https://github.com/dharlabwustl/EDEMA_MARKERS_PROD.git 1 \", \"override-entrypoint\": true, \"mounts\": [{\"name\": \"out\", \"writable\": true, \"path\": \"/output\"}, {\"name\": \"in\", \"writable\": false, \"path\": \"/input\"}, {\"name\": \"ZIPFILEDIR\", \"writable\": true, \"path\": \"/ZIPFILEDIR\"}, {\"name\": \"software\", \"writable\": true, \"path\": \"/software\"}, {\"name\": \"NIFTIFILEDIR\", \"writable\": true, \"path\": \"/NIFTIFILEDIR\"}, {\"name\": \"DICOMFILEDIR\", \"writable\": true, \"path\": \"/DICOMFILEDIR\"}, {\"name\": \"working\", \"writable\": true, \"path\": \"/working\"}, {\"name\": \"workinginput\", \"writable\": true, \"path\": \"/workinginput\"}, {\"name\": \"workingoutput\", \"writable\": true, \"path\": \"/workingoutput\"}, {\"name\": \"outputinsidedocker\", \"writable\": true, \"path\": \"/outputinsidedocker\"}], \"environment-variables\": {}, \"ports\": {}, \"inputs\": [{\"name\": \"SESSION_ID\", \"label\": null, \"description\": null, \"type\": \"string\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"sensitive\": null, \"command-line-flag\": null, \"command-line-separator\": null, \"true-value\": null, \"false-value\": null, \"select-values\": [], \"multiple-delimiter\": null}, {\"name\": \"PROJECT\", \"label\": null, \"description\": null, \"type\": \"string\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"sensitive\": null, \"command-line-flag\": null, \"command-line-separator\": null, \"true-value\": null, \"false-value\": null, \"select-values\": [], \"multiple-delimiter\": null}], \"outputs\": [], \"xnat\": [{\"name\": \"dicom2niftiusingGitHub\", \"label\": \"dicom2niftiusingGitHub batch\", \"description\": \"dicom2niftiusingGitHub\", \"contexts\": [\"xnat:imageSessionData\"], \"external-inputs\": [{\"name\": \"session\", \"label\": null, \"description\": \"Input session\", \"type\": \"Session\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"sensitive\": null, \"provides-value-for-command-input\": null, \"provides-files-for-command-mount\": null, \"via-setup-command\": null, \"user-settable\": null, \"load-children\": false}], \"derived-inputs\": [{\"name\": \"project\", \"label\": null, \"description\": null, \"type\": \"string\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"sensitive\": null, \"provides-value-for-command-input\": \"PROJECT\", \"provides-files-for-command-mount\": null, \"user-settable\": false, \"load-children\": true, \"derived-from-wrapper-input\": \"session\", \"derived-from-xnat-object-property\": \"project-id\", \"via-setup-command\": null, \"multiple\": false, \"parser\": null}, {\"name\": \"session-id\", \"label\": null, \"description\": null, \"type\": \"string\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"sensitive\": null, \"provides-value-for-command-input\": \"SESSION_ID\", \"provides-files-for-command-mount\": null, \"user-settable\": false, \"load-children\": true, \"derived-from-wrapper-input\": \"session\", \"derived-from-xnat-object-property\": \"id\", \"via-setup-command\": null, \"multiple\": false, \"parser\": null}], \"output-handlers\": []}], \"container-labels\": {}, \"generic-resources\": {}, \"ulimits\": {}}, \
	{\"name\": \"edema_biomarkers_allstepsSessionUsingGitHub\", \"description\": \"Apply edema_biomarkers_allstepsSessionUsingGitHub\", \"version\": \"1.0\", \"schema-version\": \"1.0\", \"image\": \"sharmaatul11/dicom2nifti_nwu_1:latest\", \"type\": \"docker\", \"working-directory\": \"/callfromgithub\", \"command-line\": \" /callfromgithub/downloadcodefromgithub.sh #SESSION_ID# \$XNAT_USER \$XNAT_PASS  https://snipr.wustl.edu 2 /input /output \", \"override-entrypoint\": true, \"mounts\": [{\"name\": \"out\", \"writable\": true, \"path\": \"/output\"}, {\"name\": \"in\", \"writable\": false, \"path\": \"/input\"}, {\"name\": \"ZIPFILEDIR\", \"writable\": true, \"path\": \"/ZIPFILEDIR\"}, {\"name\": \"software\", \"writable\": true, \"path\": \"/software\"}, {\"name\": \"NIFTIFILEDIR\", \"writable\": true, \"path\": \"/NIFTIFILEDIR\"}, {\"name\": \"DICOMFILEDIR\", \"writable\": true, \"path\": \"/DICOMFILEDIR\"}, {\"name\": \"working\", \"writable\": true, \"path\": \"/working\"}, {\"name\": \"workinginput\", \"writable\": true, \"path\": \"/workinginput\"}, {\"name\": \"workingoutput\", \"writable\": true, \"path\": \"/workingoutput\"}, {\"name\": \"outputinsidedocker\", \"writable\": true, \"path\": \"/outputinsidedocker\"}], \"environment-variables\": {}, \"ports\": {}, \"inputs\": [{\"name\": \"SESSION_ID\", \"label\": null, \"description\": null, \"type\": \"string\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"sensitive\": null, \"command-line-flag\": null, \"command-line-separator\": null, \"true-value\": null, \"false-value\": null, \"select-values\": [], \"multiple-delimiter\": null}, {\"name\": \"PROJECT\", \"label\": null, \"description\": null, \"type\": \"string\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"sensitive\": null, \"command-line-flag\": null, \"command-line-separator\": null, \"true-value\": null, \"false-value\": null, \"select-values\": [], \"multiple-delimiter\": null}], \"outputs\": [], \"xnat\": [{\"name\": \"edema_biomarkers_allstepsSessionUsingGitHub\", \"label\": \"edema_biomarkers_allstepsSessionUsingGitHub batch\", \"description\": \"edema_biomarkers_allstepsSessionUsingGitHub\", \"contexts\": [\"xnat:imageSessionData\"], \"external-inputs\": [{\"name\": \"session\", \"label\": null, \"description\": \"Input session\", \"type\": \"Session\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"sensitive\": null, \"provides-value-for-command-input\": null, \"provides-files-for-command-mount\": null, \"via-setup-command\": null, \"user-settable\": null, \"load-children\": false}], \"derived-inputs\": [{\"name\": \"project\", \"label\": null, \"description\": null, \"type\": \"string\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"sensitive\": null, \"provides-value-for-command-input\": \"PROJECT\", \"provides-files-for-command-mount\": null, \"user-settable\": false, \"load-children\": true, \"derived-from-wrapper-input\": \"session\", \"derived-from-xnat-object-property\": \"project-id\", \"via-setup-command\": null, \"multiple\": false, \"parser\": null}, {\"name\": \"session-id\", \"label\": null, \"description\": null, \"type\": \"string\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"sensitive\": null, \"provides-value-for-command-input\": \"SESSION_ID\", \"provides-files-for-command-mount\": null, \"user-settable\": false, \"load-children\": true, \"derived-from-wrapper-input\": \"session\", \"derived-from-xnat-object-property\": \"id\", \"via-setup-command\": null, \"multiple\": false, \"parser\": null}], \"output-handlers\": []}], \"container-labels\": {}, \"generic-resources\": {}, \"ulimits\": {}}]"

# Session ID given
sessionID=${1}
working_dir=/workinginput
working_dir_1=/input1
output_directory=/workingoutput
call_download_files_in_a_resource_in_a_session_arguments=('call_download_files_in_a_resource_in_a_session' ${sessionID} "NIFTI_LOCATION" ${working_dir})
outputfiles_present=$(python3 download_with_session_ID.py "${call_download_files_in_a_resource_in_a_session_arguments[@]}")
# find the scan id

# donwload respective nifti and relevant masks

# resample the masks to the original nifti

# use transformation matrix to register all of them to the template (rigid registration)
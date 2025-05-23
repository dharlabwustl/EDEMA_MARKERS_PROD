# Session ID given
source ./bash_utilities.sh
working_dir=/workinginput
working_dir_1=/input1
output_directory=/workingoutput
sessionID=${1}

scanID=$(get_scan_id ${sessionID})
echo ${sessionID}::${scanID}


# donwload respective nifti and relevant masks

# resample the masks to the original nifti

# use transformation matrix to register all of them to the template (rigid registration)
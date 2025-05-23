# Session ID given
sessionID=${1}
working_dir=/workinginput
working_dir_1=/input1
output_directory=/workingoutput
call_download_files_in_a_resource_in_a_session_arguments=('call_download_files_in_a_resource_in_a_session' ${sessionID} "NIFTI_LOCATION" ${working_dir})
outputfiles_present=$(python3 download_with_session_ID.py "${call_download_files_in_a_resource_in_a_session_arguments[@]}")
# find the scan id
csv_file=$(ls ${working_dir}/*_NIFTILOCATION.csv)
#!/bin/bash

#csv_file="data.csv"
column_name="ID"
IFS=','  # Set the internal field separator to comma for CSV

# Step 1: Get the column number from the header row
col_index=$(awk -F',' -v colname="$column_name" '
NR == 1 {
    for (i = 1; i <= NF; i++) {
        if ($i == colname) {
            print i
            break
        }
    }
}' "$csv_file")

# Step 2: Use the column index to extract that column's values (excluding header)
mapfile -t values < <(awk -F',' -v col="$col_index" 'NR > 1 { print $col }' "$csv_file")

# Step 3: Print the extracted values (stored in array)
echo "Values in column '$column_name':"
for val in "${values[@]}"; do
    echo "$val"
done


# donwload respective nifti and relevant masks

# resample the masks to the original nifti

# use transformation matrix to register all of them to the template (rigid registration)
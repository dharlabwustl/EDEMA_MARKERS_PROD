working_dir=/workinginput/
get_scan_id(){
    local sessionid=${1}
    call_download_files_in_a_resource_in_a_session_arguments=('call_download_files_in_a_resource_in_a_session' ${sessionid} "NIFTI_LOCATION" ${working_dir})
    outputfiles_present=$(python3 download_with_session_ID.py "${call_download_files_in_a_resource_in_a_session_arguments[@]}")

    # Get CSV file
    csv_file=$(ls ${working_dir}/*_NIFTILOCATION.csv)

    # Extract scan ID (assuming column "ID")
    column_name="ID"
    col_index=$(awk -F',' -v colname="$column_name" '
        NR == 1 {
            for (i = 1; i <= NF; i++) {
                if ($i == colname) {
                    print i
                    break
                }
            }
        }' "$csv_file")

    scan_id=$(awk -F',' -v col="$col_index" 'NR > 1 { print $col; exit }' "$csv_file")

    echo "$scan_id"  # ✅ This line makes the function return the value
}

download_resource_dir(){
  local sessionID=${1}
  local scanID=${2}
  local resource_dir=${3}
  curl -u "$XNAT_USER:$XNAT_PASS" -X GET \
    "${XNAT_HOST}/data/experiments/${sessionID}/scans/${scanID}/resources/${resource_dir}/files?format=zip" \
    -o "${working_dir}/${sessionID}_${scanID}_${resource_dir}.zip"
  cd ${working_dir}
  mv $(find ./ -name ${resource_dir}) ./
}

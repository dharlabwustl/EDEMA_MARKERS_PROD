#working_dir=/workinginput/
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
  unzip *.zip
  rm *.zip
  mv $(find ./ -name ${resource_dir}) ./
  cd ${resource_dir}
  mv files/* ./
  rm -r files

}

to_original_nifti_rf(){
  local original_ct_file=${1}
  local levelset_infarct_mask_file=${2}
  local output_directory=${3}

  python3 -c "
import sys
sys.path.append('/software/')
from utilities_simple_trimmed import levelset2originalRF_new_flip_py
levelset2originalRF_new_flip_py(sys.argv[1], sys.argv[2], sys.argv[3])
" "$original_ct_file" "$levelset_infarct_mask_file" "$output_directory"

echo "_parsehere_${output_directory}/$(basename ${levelset_infarct_mask_file})"

}

to_bet_gray_gray_n_binary(){
  local original_ct_file=${1}
  local levelset_infarct_mask_file=${2}
  local output_directory=${3}

  python3 -c "
import sys
sys.path.append('/software/')
from utilities_simple_trimmed import betgrayfrombetbinary1_py
betgrayfrombetbinary1_py(sys.argv[1], sys.argv[2], sys.argv[3])
" "$original_ct_file" "$levelset_infarct_mask_file" "$output_directory"

echo "_parsehere_${output_directory}/$(basename ${levelset_infarct_mask_file%.nii*}_brain_f.nii.gz)"
}


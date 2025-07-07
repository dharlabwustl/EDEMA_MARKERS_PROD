XNAT_USER=${1} 
XNAT_PASS=${2} 
XNAT_HOST=${3} 
session_id=${4}
#break_after_count=${5}
resource_dir=${5}
file_extension=${6}
##session_name_to_match_copy=${session_name_to_match%.csv*}_copy.csv
##awk '{ sub("\r$", ""); print }' ${session_name_to_match} > ${session_name_to_match_copy}
#
### Function to get the column number given the column name
get_column_number() {
    local csv_file="$1"   # The CSV file to search in
    local column_name="$2" # The column name to find

    # Get the header (first line) of the CSV file
    header=$(head -n 1 "$csv_file")

    # Split the header into an array of column names
    IFS=',' read -r -a columns <<< "$header"

    # Loop through the columns and find the index of the column name
    for i in "${!columns[@]}"; do
        if [[ "${columns[$i]}" == "$column_name" ]]; then
            # Print the 1-based index (cut and other tools expect 1-based indexes)
            echo $((i  ))
            return
        fi
    done

    # If the column is not found, print an error and return a failure status
    echo "Column '$column_name' not found!" >&2
    return 1
}
#csv_file='sessions.csv'
##merged_csv='updated_shorter_v1.csv'
#curl  -u   $XNAT_USER:$XNAT_PASS  -X GET   $XNAT_HOST/data/projects/${project_id}/experiments/?format=csv  > ${csv_file}
## Extract headers
##header_shorter=$(head -n 1 ${session_name_to_match_copy}) #'/home/atul/Downloads/Missing PDFs for RIS Atul.csv')
##header_longer=$(head -n 1 ${sessions_list}) #'/home/atul/Downloads/sessionsMGBBMC_ANALYTICS_STEP3_20241209215217.csv')
##
### Determine column positions (1-based index)
##pos_name=$(echo "$header_shorter" | tr ',' '\n' | grep -n -w 'name' | cut -d: -f1)
##pos_label=$(echo "$header_longer" | tr ',' '\n' | grep -n -w 'label' | cut -d: -f1)
##pos_id=$(echo "$header_longer" | tr ',' '\n' | grep -n -w 'ID' | cut -d: -f1)
##echo ${pos_name}::${pos_label}::${pos_id}
##awk -F, -v name_col="$pos_name" -v label_col="$pos_label" -v id_col="$pos_id" '
##BEGIN {
##    OFS = FS
##}
##NR == FNR {
##    # Read longer.csv into an array
##    label = $label_col
##    id = $id_col
##    map[label] = id
##    next
##}
##FNR == 1 {
##    # For shorter.csv, print header with new SESSION_ID column
##    print $0, "SESSION_ID"
##    next
##}
##{
##    # For each row in shorter.csv, append the corresponding ID
##    name = $name_col
##    session_id = (name in map) ? map[name] : ""
##    print $0, session_id
##}
##' ${sessions_list} ${session_name_to_match_copy} > ${merged_csv} #updated_shorter_v1.csv
##cat ${merged_csv}
##
##csv_file=${merged_csv}
#column_name="ID"
#column_number=$(get_column_number "$csv_file" "$column_name")
##column_name_1="name"
##column_number_1=$(get_column_number "$csv_file" "$column_name_1")
#counter=0
## echo ${column_number}
#while IFS=',' read -ra array; do
sessionID=${session_id} #${array[${column_number}]}
scan_csv="${sessionID}scans.csv"
echo ${sessionID}
#sessionlabel=${array[${column_number_1}]}
#echo sessionName::${sessionlabel}


curl  -u   $XNAT_USER:$XNAT_PASS  -X GET   $XNAT_HOST/data/experiments/$sessionID/scans/?format=csv  > ${scan_csv}
########################
scan_csv_file=${scan_csv}
scan_column_name="ID"
scan_column_number=$(get_column_number "$scan_csv_file" "$scan_column_name")
scan_type_column_name="type"
scan_type_column_number=$(get_column_number "$scan_csv_file" "$scan_type_column_name")
echo ${scan_column_number}
echo ${scan_type_column_number}
#sessionID=
while IFS=',' read -ra array1; do
# echo


scan_type=${array1[${scan_type_column_number}]}
if [[ ${scan_type} == 'Z-Axial-Brain' || ${scan_type} == 'Z-Brain-Thin' ]]; then
scanID=${array1[${scan_column_number}]}
echo ${scan_type}
scan_csv_files_in_resource=${sessionID}_${scanID}_resources.csv
curl  -u   $XNAT_USER:$XNAT_PASS  -X GET   $XNAT_HOST/data/experiments/${sessionID}/scans/${scanID}/resources/${resource_dir}/files?format=csv  > ${scan_csv_files_in_resource}
this_column_name="URI"
this_column_number=$(get_column_number "$scan_csv_files_in_resource" "$this_column_name")
echo ${this_column_number}
while IFS=',' read -ra array2; do
uri=${array2[${this_column_number}]}
echo ${uri}
if [[ ${uri} == *${file_extension}* ]] ; then
echo ${uri}
#curl  -u   $XNAT_USER:$XNAT_PASS  -X GET   $XNAT_HOST${uri} --output $(basename ${uri})
curl  -u   $XNAT_USER:$XNAT_PASS  -X GET  -H "Connection: close" $XNAT_HOST${uri} --output ${sessionID}_${scanID}_$(basename ${uri})
#curl -u $XNAT_USER:$XNAT_PASS -X DELETE -H "Connection: close" $XNAT_HOST${uri}
fi

done < <(tail -n +2 "${scan_csv_files_in_resource}" )
fi
done < <(tail -n +2 "${scan_csv_file}" )
###################################
#counter=$(( counter + 1 ))
#echo ${counter}
#if [[ ${counter} -gt ${break_after_count} ]] ; then
#  break
#fi
#done < <(tail -n +2 "${csv_file}")
for x in ./*${file_extension}* ;
do cp ${x} /workingoutput/ ;
done




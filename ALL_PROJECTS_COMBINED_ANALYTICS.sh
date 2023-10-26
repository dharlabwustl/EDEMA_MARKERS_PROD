#!/bin/bash
export XNAT_USER=${1}
export XNAT_PASS=${2}
export XNAT_HOST=${3}

working_dir=/workinginput
output_directory=/workingoutput

final_output_directory=/outputinsidedocker
ARGS=("$@")
# Get the last argument
arguments_count=${#ARGS[@]}
IFS='_' read -r -a project_IDS <<<"${4}"
echo "${project_IDS[0]}"
arguments_count=${#project_IDS[@]}

#for project_ID in ${ARGS[@]}; do
####################
call_get_resourcefiles_metadata_saveascsv() {
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
copysinglefile_to_sniprproject() {
  local projectID=$1
  #scanID=$2
  local resource_dirname=$3 #"MASKS" #sys.argv[4]
  local file_name=$4
  local output_dir=$2
  echo " I AM IN copysinglefile_to_sniprproject "
  python3 -c "
import sys
sys.path.append('/software');
from download_with_session_ID import *;
uploadsinglefile_projectlevel()" ${projectID} ${output_dir} ${resource_dirname} ${file_name} # ${infarctfile_present}  ##$static_template_image $new_image $backslicenumber #$single_slice_filename

}
## for each session
function call_get_resourcefiles_metadata_saveascsv_args() {
  local resource_dir=${2}   #"NIFTI"
  local output_csvfile=${4} #{array[1]}

  local URI=${1} #{array[0]}
  local file_ext=${5}
  local output_csvfile=${output_csvfile%.*}${resource_dir}.csv

  local final_output_directory=${3}
  local call_download_files_in_a_resource_in_a_session_arguments=('call_get_resourcefiles_metadata_saveascsv_args' ${URI} ${resource_dir} ${final_output_directory} ${output_csvfile})
  outputfiles_present=$(python3 download_with_session_ID.py "${call_download_files_in_a_resource_in_a_session_arguments[@]}")

}
download_a_single_file() {
  local file_path_csv=${1}
  local dir_to_save=${2} #args.stuff[3]
  local projectid=${3}

  while IFS=',' read -ra array; do
    echo array::${array[0]}
    local get_latest_filepath_from_metadata_arguments=('download_a_singlefile_with_URIString' ${array[0]} ${projectid}$(basename ${array[0]}) ${dir_to_save})
    local outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
  done < <(tail -n +2 "${file_path_csv}")

}
create_histogram_and_save() {
  local column_name=${1}                      #'ICH_EDEMA_VOLUME'
  local csvfilename=${2}                      # args.stuff[2]
  local output_image_name_ichedemavolume=${3} #/$(echo ${column_name} | sed 's/ //g')"_HISTOGRAM.png" #args.stuff[3]
  local histogram_column_ina_csvfile_arguments=('histogram_column_ina_csvfile' ${csvfilename} ${column_name} ${output_image_name_ichedemavolume})
  local outputfiles_present=$(python3 system_analysis.py "${histogram_column_ina_csvfile_arguments[@]}")

}
add_image_to_texfile() {
  local imagescale=${2} #float(args.stuff[2])
  local angle='0'       #float(args.stuff[3])
  local space='1'       #float(args.stuff[4])
  local i=0
  local images=()
  images[$i]='call_latex_insertimage_tableNc'
  i=$(($i + 1))
  images[$i]=${latexfilename}
  i=$(($i + 1))
  images[$i]=${imagescale}
  i=$(($i + 1))
  images[$i]=${angle}
  i=$(($i + 1))
  images[$i]=${space}
  i=$(($i + 1))

  #if [ -f "${output_image_name_nwu}" ] && [ -f "${output_image_name_csfratio}" ] && [ -f "${output_image_name_ichvolume}" ] && [ -f "${output_image_name_ichedemavolume}" ] && [ -f "${output_image_name_sahsegtotal}" ]; then

  images[$i]=${1}
  i=$(($i + 1))
  #  images[$i]=${output_image_name_csfratio}
  #  i=$(($i + 1))
  outputfiles_present=$(python3 utilities_simple_trimmed.py "${images[@]}")
  echo outputfiles_present::${outputfiles_present}
  #call_space_between_lines_arguments=('call_space_between_lines' ${latexfilename} '-3')
  outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_space_between_lines_arguments[@]}") #fuchsia_fuchsia_olive_olive_lime_lime_orange_orange

}

for x in $(seq 0 1 $((arguments_count - 1))); do
  #  echo ${project_ID}
  #  if [[ $x -gt 2 ]]; then
  if [[ $x -gt -1 ]]; then
    #    project_ID=${ARGS[x]}
    project_ID=${project_IDS[x]}
    echo PROJECTID::${project_ID}

    ##sessions_list=${working_dir}/'sessions.csv'
    time_now=$(date -dnow +%Y%m%d%H%M%S)
    URI="/data/projects/"${project_ID}
    dir_to_receive_the_data=${output_directory}
    analytics_file_dir=${working_dir}
    if [ ${project_ID} == "COLI" ]; then
      resource_dir="EDEMA_BIOMARKER_TEST"
      file_path_csv=${analytics_file_dir}/${project_ID}"_${resource_dir}_resultfilepath.csv"
      get_latest_filepath_from_metadata_arguments=('get_latest_filepath_from_metadata_for_analytics' ${URI} ${resource_dir} ".csv" "COLI_EDEMA_BIOMARKERS_COMBINED_" ${file_path_csv})
      outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
      echo ${outputfiles_present}
      download_a_single_file ${file_path_csv} ${dir_to_receive_the_data}
      resource_dir="SNIPR_ANALYTICS_TEST"
      file_path_csv=${analytics_file_dir}/${project_ID}"_${resource_dir}_resultfilepath.csv"
      get_latest_filepath_from_metadata_arguments=('get_latest_filepath_from_metadata_for_analytics' ${URI} ${resource_dir} ".csv" "sessions_ANALYTICS_" ${file_path_csv})
      outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
      download_a_single_file ${file_path_csv} ${analytics_file_dir} ${project_ID}

    elif [ ${project_ID} == "WashU" ]; then
      resource_dir="EDEMA_BIOMARKER_TEST"
      file_path_csv=${analytics_file_dir}/${project_ID}"_${resource_dir}_resultfilepath.csv"
      get_latest_filepath_from_metadata_arguments=('get_latest_filepath_from_metadata_for_analytics' ${URI} ${resource_dir} ".csv" "WashU_EDEMA_BIOMARKERS_COMBINED_" ${file_path_csv})
      outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
      download_a_single_file ${file_path_csv} ${dir_to_receive_the_data}
      resource_dir="SNIPR_ANALYTICS_TEST"
      file_path_csv=${analytics_file_dir}/${project_ID}"_${resource_dir}_resultfilepath.csv"
      get_latest_filepath_from_metadata_arguments=('get_latest_filepath_from_metadata_for_analytics' ${URI} ${resource_dir} ".csv" "sessions_ANALYTICS_" ${file_path_csv})
      outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
      download_a_single_file ${file_path_csv} ${analytics_file_dir} ${project_ID}

    elif [ ${project_ID} == "MGBBMC" ]; then
      resource_dir="EDEMA_BIOMARKER_TEST"
      file_path_csv=${analytics_file_dir}/${project_ID}"_${resource_dir}_resultfilepath.csv"
      get_latest_filepath_from_metadata_arguments=('get_latest_filepath_from_metadata_for_analytics' ${URI} ${resource_dir} ".csv" "MGBBMC_EDEMA_BIOMARKERS_COMBINED_" ${file_path_csv})
      outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
      download_a_single_file ${file_path_csv} ${dir_to_receive_the_data}
      resource_dir="SNIPR_ANALYTICS_TEST"
      file_path_csv=${analytics_file_dir}/${project_ID}"_${resource_dir}_resultfilepath.csv"
      get_latest_filepath_from_metadata_arguments=('get_latest_filepath_from_metadata_for_analytics' ${URI} ${resource_dir} ".csv" "sessions_ANALYTICS_" ${file_path_csv})
      outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
      download_a_single_file ${file_path_csv} ${analytics_file_dir} ${project_ID}
    elif [ ${project_ID} == "SAH" ]; then
      resource_dir="SAH_RESULTS_CSV"
      file_path_csv=${analytics_file_dir}/${project_ID}"_${resource_dir}_resultfilepath.csv"
      get_latest_filepath_from_metadata_arguments=('get_latest_filepath_from_metadata_for_analytics' ${URI} ${resource_dir} ".csv" "COMBINED_SESSIONS_SAH_METRICS_" ${file_path_csv})
      outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
      download_a_single_file ${file_path_csv} ${dir_to_receive_the_data}
      resource_dir="SAH_SESSION_PROCESSING_ANALYTICS"
      file_path_csv=${analytics_file_dir}/${project_ID}"_${resource_dir}_resultfilepath.csv"
      get_latest_filepath_from_metadata_arguments=('get_latest_filepath_from_metadata_for_analytics' ${URI} ${resource_dir} ".csv" "sessions_SAH_ANALYTICS_" ${file_path_csv})
      outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
      download_a_single_file ${file_path_csv} ${analytics_file_dir} ${project_ID}

    elif [ ${project_ID} == "ICH" ]; then
      resource_dir="ICH_QUANTIFICATIONPDF"
      file_path_csv=${analytics_file_dir}/${project_ID}"_${resource_dir}_resultfilepath.csv"
      get_latest_filepath_from_metadata_arguments=('get_latest_filepath_from_metadata_for_analytics' ${URI} ${resource_dir} ".csv" "ICH2023_06_06_EDEMA_BIOMARKERS_COMBINED_" ${file_path_csv})
      outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
      download_a_single_file ${file_path_csv} ${dir_to_receive_the_data}
      resource_dir="SNIPR_ANALYTICS"
      file_path_csv=${analytics_file_dir}/${project_ID}"_${resource_dir}_resultfilepath.csv"
      get_latest_filepath_from_metadata_arguments=('get_latest_filepath_from_metadata_for_analytics' ${URI} ${resource_dir} ".csv" "ICH_CTSESSIONS_" ${file_path_csv})
      outputfiles_present=$(python3 system_analysis.py "${get_latest_filepath_from_metadata_arguments[@]}")
      download_a_single_file ${file_path_csv} ${analytics_file_dir} ${project_ID}
    fi

  fi

done

time_now=$(date -dnow +%Y%m%d%H%M%S)
csvfile_list="${working_dir}/CSV_FILENAMES_LIST.csv"
echo "CSV_FILENAMES" >${csvfile_list}
for eachfilename in ${dir_to_receive_the_data}/*.csv; do echo $eachfilename >>${csvfile_list}; done
combined_metrics_results="${working_dir}/COMBINED_PROJECTS_${4}_${time_now}.csv"
combinecsvsfiles_from_a_csv_containing_its_list_arguments=('combinecsvsfiles_from_a_csv_containing_its_list' ${csvfile_list} ${combined_metrics_results})
outputfiles_present=$(python3 system_analysis.py "${combinecsvsfiles_from_a_csv_containing_its_list_arguments[@]}")
### histograms: CSF ratio='CSF RATIO', NWU='NWU' , ICH volumes:'ICH VOLUME' 'ICH EDEMA VOLUME'
#
csvfilename=${combined_metrics_results}
latexfilename_prefix=${working_dir}/${4}
latexfilename=${latexfilename_prefix}_histograms_${time_now}.tex
#csvfilename=${latexfilename%.pdf*}.csv
call_latex_start_arguments=('call_latex_start' ${latexfilename})
outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_latex_start_arguments[@]}")
###################
csvfile_analysis=$(ls ${working_dir}/*WashUsessions_ANALYTICS_*.csv) #args.stuff[1]
column_to_be_counted_in_analysis="ID" #args.stuff[2]
cohort_name="WASHU" #args.stuff[3]
outputcsvfilename_washu="${working_dir}/${cohort_name}_${column_to_be_counted_in_analysis}_count.csv" #args.stuff[4]
call_latex_start_arguments=('count_a_column' ${csvfile_analysis} ${column_to_be_counted_in_analysis} ${cohort_name} ${outputcsvfilename_washu})
outputfiles_present=$(python3 system_analysis.py "${call_latex_start_arguments[@]}")

csvfile_analysis=$(ls ${dir_to_receive_the_data}/*WashU_EDEMA_BIOMARKERS_COMBINED_*.csv) #args.stuff[1]
column_to_be_counted_in_analysis="NWU" #args.stuff[2]
cohort_name="WASHU" #args.stuff[3]
outputcsvfilename_washu_nwu="${working_dir}/${cohort_name}_${column_to_be_counted_in_analysis}_count.csv" #args.stuff[4]
call_latex_start_arguments=('count_a_column' ${csvfile_analysis} ${column_to_be_counted_in_analysis} ${cohort_name} ${outputcsvfilename_washu_nwu})
outputfiles_present=$(python3 system_analysis.py "${call_latex_start_arguments[@]}")

csvfile_analysis=$(ls ${dir_to_receive_the_data}/*WashU_EDEMA_BIOMARKERS_COMBINED_*.csv) #args.stuff[1]
column_to_be_counted_in_analysis="CSF_RATIO" #args.stuff[2]
cohort_name="WASHU" #args.stuff[3]
outputcsvfilename_washu_nwu="${working_dir}/${cohort_name}_${column_to_be_counted_in_analysis}_count.csv" #args.stuff[4]
call_latex_start_arguments=('count_a_column' ${csvfile_analysis} ${column_to_be_counted_in_analysis} ${cohort_name} ${outputcsvfilename_washu_nwu})
outputfiles_present=$(python3 system_analysis.py "${call_latex_start_arguments[@]}")


csvfile_analysis=$(ls ${working_dir}/*COLIsessions_ANALYTICS_*.csv) #args.stuff[1]
column_to_be_counted_in_analysis="ID" #args.stuff[2]
cohort_name="COLI" #args.stuff[3]
outputcsvfilename_coli="${working_dir}/${cohort_name}_${column_to_be_counted_in_analysis}_count.csv" #args.stuff[4]
call_latex_start_arguments=('count_a_column' ${csvfile_analysis} ${column_to_be_counted_in_analysis} ${cohort_name} ${outputcsvfilename_coli})
outputfiles_present=$(python3 system_analysis.py "${call_latex_start_arguments[@]}")
##cohort_count=${working_dir}/cohort_sessions_count.csv
###echo "COHORT_NAME,SESSION_COUNT,RESULTS_COUNT" >${cohort_count}
###echo "WASHU,," >> ${cohort_count}
###echo "SAH,," >>${cohort_count}
##csvfilename_input=$(ls ${working_dir}/*WashUsessions_ANALYTICS_*.csv)
##csvfile_results=$(ls ${dir_to_receive_the_data}/*WashU_EDEMA_BIOMARKERS_COMBINED_*.csv)
##
##csvfile_analysis= ${csvfilename_input} #args.stuff[1]
##column_to_be_counted_in_analysis="ID" #args.stuff[2]
###csvfile_results=args.stuff[3]
##column_to_be_counted_in_result="NWU" #args.stuff[4]
##outputcsvfilename=${cohort_count} #args.stuff[5]
##call_latex_start_arguments=('analysis_files_count' ${csvfile_analysis} ${column_to_be_counted_in_analysis} ${csvfile_results} ${column_to_be_counted_in_result} ${outputcsvfilename})
##outputfiles_present=$(python3 system_analysis.py "${call_latex_start_arguments[@]}")
##column_to_be_counted="ID"                                                                 #args.stuff[2]
##identifier_column_name_inoutput="COHORT_NAME"                                                         #args.stuff[2]
##identifier_column_value_inoutput="WASHU"                                                            #args.stuff[3]
##column_name="SESSION_COUNT"                                                                       #args.stuff[4]
##csvfilename_output=${cohort_count}                                                                #args.stuff[6]
##echo csvfilename_input::${csvfilename_input}
##call_latex_start_arguments=('create_empty_csvfile' ${cohort_count} ) ##${column_to_be_counted} ${identifier_column_name_inoutput} ${identifier_column_value_inoutput} ${column_name} ${csvfilename_output})
##outputfiles_present=$(python3 system_analysis.py "${call_latex_start_arguments[@]}")
##call_latex_start_arguments=('non_numerical_val_counter' ${csvfilename_input} ${column_to_be_counted} ${identifier_column_name_inoutput} ${identifier_column_value_inoutput} ${column_name} ${csvfilename_output})
##outputfiles_present=$(python3 system_analysis.py "${call_latex_start_arguments[@]}")
##call_latex_start_arguments=('non_numerical_val_counter' ${csvfilename_input} ${column_to_be_counted} ${identifier_column_name_inoutput} ${identifier_column_value_inoutput} ${column_name} ${csvfilename_output})
##outputfiles_present=$(python3 system_analysis.py "${call_latex_start_arguments[@]}")
##column_name='WASHU_SESSIONS_COUNT'
##
###call_latex_start_arguments=('write_single_data_incsv_withknown_id' ${latexfilename})
###outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_latex_start_arguments[@]}")
##column_value=$(cat ${working_dir}/*WashUsessions_ANALYTICS_*.csv | wc -l)
##column_value=$((column_value - 1))
##column_value_1="" #$(cat ${dir_to_receive_the_data}/*WashU_EDEMA_BIOMARKERS_COMBINED_*.csv | wc -l )
##column_value_1=$((column_value_1 - 1))
##call_latex_start_arguments=('write_a_col_on_tex' ${latexfilename} ${column_name} ${column_value})
###outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_latex_start_arguments[@]}")
##echo "WASHU,${column_value},${column_value_1}" >>${cohort_count}
#######################
#####################
##column_name='COLISEUM_SESSIONS_COUNT'
##column_value=$(cat ${working_dir}/*COLIsessions_ANALYTICS_*.csv | wc -l)
##column_value=$((column_value - 1))
##column_value_1=$(cat ${dir_to_receive_the_data}/*COLI_EDEMA_BIOMARKERS_COMBINED_*.csv | wc -l)
##column_value_1="" #$(( column_value_1 -1 ))
##call_latex_start_arguments=('write_a_col_on_tex' ${latexfilename} ${column_name} ${column_value})
###outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_latex_start_arguments[@]}")
##echo "COLISEUM,${column_value},${column_value_1}" >>${cohort_count}
#######################
#####################
##column_name='ICH_SESSIONS_COUNT'
##column_value=$(cat ${working_dir}/*ICH_CTSESSIONS_*.csv | wc -l)
##column_value=$((column_value - 1))
##column_value_1=$(cat ${dir_to_receive_the_data}/*ICH2023_06_06_EDEMA_BIOMARKERS_COMBINED_*.csv | wc -l)
##column_value_1="" #$(( column_value_1 -1 ))
##call_latex_start_arguments=('write_a_col_on_tex' ${latexfilename} ${column_name} ${column_value})
###outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_latex_start_arguments[@]}")
##echo "ICH,${column_value},${column_value_1}" >>${cohort_count}
##csvfilename_input=$(ls ${dir_to_receive_the_data}/*ICH2023_06_06_EDEMA_BIOMARKERS_COMBINED_*.csv) #args.stuff[1]
##
###
########################
######################
###column_name='MGBBMC_SESSIONS_COUNT'
###column_value=$(cat ${working_dir}/*MGBBMCsessions_ANALYTICS_*.csv | wc -l)
###column_value=$((column_value - 1))
###column_value_1=$(cat ${dir_to_receive_the_data}/*MGBBMC_EDEMA_BIOMARKERS_COMBINED_*.csv | wc -l)
###column_value_1="" #$(( column_value_1 -1 ))
###call_latex_start_arguments=('write_a_col_on_tex' ${latexfilename} ${column_name} ${column_value})
####outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_latex_start_arguments[@]}")
###echo "MGBBMC,${column_value},${column_value_1}" >>${cohort_count}
########################
######################
###column_name='SAH_SESSIONS_COUNT'
###column_value=$(cat ${working_dir}/*sessions_SAH_ANALYTICS_*.csv | wc -l)
###column_value=$((column_value - 1))
###column_value_1=$(cat ${dir_to_receive_the_data}/*COMBINED_SESSIONS_SAH_METRICS_*.csv | wc -l)
###column_value_1="" #$(( column_value_1 -1 ))
###call_latex_start_arguments=('write_a_col_on_tex' ${latexfilename} ${column_name} ${column_value})
####outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_latex_start_arguments[@]}")
###echo "SAH,${column_value},${column_value_1}" >>${cohort_count}
###
###call_latex_start_arguments=('csvtable_on_tex' ${cohort_count} ${latexfilename})
###outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_latex_start_arguments[@]}")
########################
#####args.stuff[1]
#histogram_column_ina_csvfile_arguments=('call_remove_single_column_with_colnmname_substring' ${csvfilename} "CSF_RATIO" ${csvfilename})
#outputfiles_present=$(python3 fillmaster_session_list.py "${histogram_column_ina_csvfile_arguments[@]}")
#column_name="NWU"                                                                          #args.stuff[2]
#output_image_name_nwu=${working_dir}/$(echo ${column_name} | sed 's/ //g')"_HISTOGRAM.png" #args.stuff[3]
#create_histogram_and_save ${column_name} ${csvfilename} ${output_image_name_nwu}
#add_image_to_texfile ${output_image_name_nwu} 0.9
#column_name="CSF_RATIO"                                                                    #args.stuff[2]
#output_image_name_nwu=${working_dir}/$(echo ${column_name} | sed 's/ //g')"_HISTOGRAM.png" #args.stuff[3]
#create_histogram_and_save ${column_name} ${csvfilename} ${output_image_name_nwu}
#add_image_to_texfile ${output_image_name_nwu} 0.9
#column_name="ICH_VOLUME"                                                                   #args.stuff[2]
#output_image_name_nwu=${working_dir}/$(echo ${column_name} | sed 's/ //g')"_HISTOGRAM.png" #args.stuff[3]
#create_histogram_and_save ${column_name} ${csvfilename} ${output_image_name_nwu}
#add_image_to_texfile ${output_image_name_nwu} 0.9
#column_name="ICH_EDEMA_VOLUME"                                                             #args.stuff[2]
#output_image_name_nwu=${working_dir}/$(echo ${column_name} | sed 's/ //g')"_HISTOGRAM.png" #args.stuff[3]
#create_histogram_and_save ${column_name} ${csvfilename} ${output_image_name_nwu}
#add_image_to_texfile ${output_image_name_nwu} 0.9
#column_name="SAH_SEG_TOTAL"                                                                #args.stuff[2]
#output_image_name_nwu=${working_dir}/$(echo ${column_name} | sed 's/ //g')"_HISTOGRAM.png" #args.stuff[3]
#create_histogram_and_save ${column_name} ${csvfilename} ${output_image_name_nwu}
#add_image_to_texfile ${output_image_name_nwu} 0.9
#call_latex_end_arguments=('call_latex_end' ${latexfilename})
#outputfiles_present=$(python3 utilities_simple_trimmed.py "${call_latex_end_arguments[@]}")
#pdfilename=${output_directory}/$(basename ${latexfilename%.tex*}.pdf)
#pdflatex -halt-on-error -interaction=nonstopmode -output-directory=${output_directory} ${latexfilename} ##${output_directory}/$(/usr/lib/fsl/5.0/remove_ext $this_filename)*.tex
##URI="/data/projects/WashU"
##resource_dirname="ALL_PROJECTS_COMBINED"
##call_uploadsinglefile_with_URI_arguments=('call_uploadsinglefile_with_URI' ${URI} ${pdfilename} ${resource_dirname})
##outputfiles_present=$(python3 /software/download_with_session_ID.py "${call_uploadsinglefile_with_URI_arguments[@]}")
##call_uploadsinglefile_with_URI_arguments=('call_uploadsinglefile_with_URI' ${URI} ${csvfilename} ${resource_dirname})
##outputfiles_present=$(python3 /software/download_with_session_ID.py "${call_uploadsinglefile_with_URI_arguments[@]}")

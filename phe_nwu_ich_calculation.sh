#!/bin/bash
output_directory='/working'
rm ${output_directory}/*
SESSION_ID=${1}
XNAT_USER=${2}
XNAT_PASS=${3}
XNAT_HOST=${4}
working_dir=/workinginput
output_directory=/workingoutput
final_output_directory=/outputinsidedocker
############## CHECK IF FILES AVAILABLE #################
call_download_files_in_a_resource_in_a_session_arguments=('call_download_files_in_a_resource_in_a_session' ${SESSION_ID} "NIFTI_LOCATION" ${working_dir})
outputfiles_present=$(python3 /software/download_with_session_ID.py "${call_download_files_in_a_resource_in_a_session_arguments[@]}")
NIFTILOCATION_FILE=$(ls ${working_dir}/*NIFTILOCATION*.csv)
while IFS=',' read -ra array_ich_q; do
  uri=${array_ich_q[0]}
  SELECTED_SCAN_ID=${array_ich_q[2]}
  #################
done < <(tail -n +2 "${NIFTILOCATION_FILE}")
URI=${uri%/resources*}
echo '${URI} ${file_to_upload} "${resource_dir}"'::::${URI}::${NIFTILOCATION_FILE}  ##::${file_to_upload}::"${resource_dir}"
snipr_output_foldername='ICH_PHE_QUANTIFICATION'
call_check_if_a_file_exist_in_snipr_arguments=('call_check_if_a_file_exist_in_snipr' ${SESSION_ID} ${SELECTED_SCAN_ID} ${snipr_output_foldername} .pdf .csv)
outputfiles_present=$(python3 /software/download_with_session_ID.py "${call_check_if_a_file_exist_in_snipr_arguments[@]}")
if [[ "${outputfiles_present: -1}" -eq 1 ]]; then
  echo " I AM THE ONE"
fi
## START WORKING IF THE REQUIRED FILES DO NOT EXIST
if [[ "${outputfiles_present: -1}" -eq 0 ]]; then                  ##[[ 1 -gt 0 ]]  ; then #
  output_csvfile=${SESSION_ID}_ICH_PHE_QUANTIFICATION_METADATA.csv #${4} #{array[1]}
                                                     #{array[0]}
  call_download_files_in_a_resource_in_a_session_arguments=('call_get_resourcefiles_metadata_saveascsv_args' ${URI} ${resource_dir} ${final_output_directory} ${output_csvfile})
  outputfiles_present=$(python3 /software/download_with_session_ID.py "${call_download_files_in_a_resource_in_a_session_arguments[@]}")
  ##################
  VERSION='V_01152024'
  time_now=$(date -dnow +%m_%d_%Y)
  outputfiles_suffix=${VERSION}_${time_now}
  /software/nwu_with_ich_mask.sh ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
  #  cp /workingoutput/*.tex /working/
  cp /workingoutput/*_ICHCSF*.csv /working/
  cp /workingoutput/*.png /working/
  /software/phe_nwu_calculation.sh ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
  #  cp /workingoutput/*.tex /working/
  cp /workinginput/*NIFTILOCATION*.csv /working/
  cp /workingoutput/*_PHENWU*.csv /working/
  cp /workingoutput/*.png /working/

  #echo "HELLO" > /working/atulTOTAL.csv
  counter=0
  x=$(ls ${output_directory}/*_PHENWU*.csv)
  x1=$(ls ${output_directory}/*_ICHCSF*.csv)
  #for x in ${output_directory}/*TOTAL*.csv; do
  #  if [ ${counter} == 0 ] ; then
  grayscale_filename_basename_noext=$(basename ${x%_thres*})
  latexfilename=${output_directory}/${grayscale_filename_basename_noext}_${outputfiles_suffix}.tex
  csvfilename=${latexfilename%.tex*}.csv
  cp ${x} ${csvfilename}

  call_combine_csv_horizontally_arguments=('call_combine_csv_horizontally' ${grayscale_filename_basename_noext} ${csvfilename} ${csvfilename} ${x1}) # ${output_directory}/${grayscale_filename_basename_noext}_bet_mask_WITHOUT_csf.csv ${output_directory}/$(basename ${mask_filename1%.nii*}.csv) ${output_directory}/$(basename ${mask_filename2%.nii*}.csv) ${output_directory}/$(basename ${mask_filename3%.nii*}.csv) ${output_directory}/$(basename ${mask_filename4%.nii*}.csv) ${output_directory}/$(basename ${mask_filename5%.nii*}.csv) ${output_directory}/$(basename ${mask_filename6%.nii*}.csv) ${output_directory}/$(basename ${mask_filename7%.nii*}.csv) ${output_directory}/$(basename ${mask_filename8%.nii*}.csv) ${output_directory}/$(basename ${mask_filename9%.nii*}.csv) ${output_directory}/$(basename ${mask_filename10%.nii*}.csv) ${output_directory}/$(basename ${mask_filename11%.nii*}.csv) ${output_directory}/$(basename ${mask_filename12%.nii*}.csv) ${output_directory}/$(basename ${mask_filename13%.nii*}.csv) ${output_directory}/$(basename ${mask_filename14%.nii*}.csv) ${output_directory}/$(basename ${mask_filename15%.nii*}.csv) ${output_directory}/$(basename ${mask_filename16%.nii*}.csv) ${output_directory}/$(basename ${mask_filename17%.nii*}.csv) ${output_directory}/$(basename ${mask_filename18%.nii*}.csv) ${output_directory}/$(basename ${mask_filename19%.nii*}.csv) ${output_directory}/$(basename ${mask_filename20%.nii*}.csv) ${output_directory}/$(basename ${mask_filename21%.nii*}.csv) ${output_directory}/$(basename ${mask_filename22%.nii*}.csv) ${output_directory}/$(basename ${mask_filename23%.nii*}.csv) ${output_directory}/$(basename ${mask_filename24%.nii*}.csv) ${output_directory}/$(basename ${mask_filename25%.nii*}.csv) ${output_directory}/$(basename ${mask_filename26%.nii*}.csv) ${output_directory}/$(basename ${mask_filename27%.nii*}.csv) ${output_directory}/$(basename ${mask_filename28%.nii*}.csv))
  outputfiles_present=$(python3 /software/dividemasks_into_left_right.py "${call_combine_csv_horizontally_arguments[@]}")
  call_latex_start_arguments=('remove_columns' ${csvfilename} ${csvfilename} 'FileName_slice')
  outputfiles_present=$(python3 /software/fillmaster_session_list.py "${call_latex_start_arguments[@]}")
  call_latex_start_arguments=('call_move_one_column' ${csvfilename} 'SESSION_LABEL' 0 ${csvfilename})
  outputfiles_present=$(python3 /software/fillmaster_session_list.py "${call_latex_start_arguments[@]}")
  call_latex_start_arguments=('call_move_one_column' ${csvfilename} 'SLICE_NUM' 2 ${csvfilename})
  outputfiles_present=$(python3 /software/fillmaster_session_list.py "${call_latex_start_arguments[@]}")
  call_latex_start_arguments=('add_single_column_in1Ddata' ${csvfilename} 'SESSION_ID' ${SESSION_ID} ${csvfilename})
  outputfiles_present=$(python3 /software/fillmaster_session_list.py "${call_latex_start_arguments[@]}")
  call_latex_start_arguments=('call_move_one_column' ${csvfilename} 'SESSION_ID' 1 ${csvfilename})
  outputfiles_present=$(python3 /software/fillmaster_session_list.py "${call_latex_start_arguments[@]}")
  ########################################

  add_scan_description_arguments=('add_scan_description' ${SESSION_ID} ${SELECTED_SCAN_ID} ${csvfilename})
  outputfiles_present=$(python3 fillmaster_session_list.py "${add_scan_description_arguments[@]}")
  ######################################
  call_latex_start_arguments=('call_latex_start' ${latexfilename})
  outputfiles_present=$(python3 /software/utilities_simple_trimmed.py "${call_latex_start_arguments[@]}")
  call_latex_start_arguments=('write_table_on_texfile' ${latexfilename} ${csvfilename})
  outputfiles_present=$(python3 /software/fillmaster_session_list.py "${call_latex_start_arguments[@]}")

  for z in ${output_directory}/${grayscale_filename_basename_noext}*gray.png; do

    #              filename=args.stuff[1]
    imagescale='0.15' #float(args.stuff[2])
    angle='90'        #float(args.stuff[3])
    space='1'         #float(args.stuff[4])
    i=0
    #  for file in *
    #  do
    #      if [[ -f $file ]]; then
    #          array[$i]=$file
    #          i=$(($i+1))
    #      fi
    #  done

    #    echo $suffix;
    ## Legends
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

    y=${z%gray.*}
    #       echo $y
    suffix=${y##*_}
    image_col1="${z}"
    image_col2="${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_${suffix}_left_right_brain.png"
    image_col3="${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_${suffix}_infarct.png"
    image_col4="${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_${suffix}_class1.png"
    image_col5="${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_${suffix}_class2.png"
    image_col6="${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_${suffix}.png"
    echo ${image_col1}::${image_col2}::${image_col3}::${image_col4}::${image_col5}::${image_col6}::
    #   && [ -f "${image_col5}" ]
    if [ -f "${image_col1}" ] && [ -f "${image_col2}" ] && [ -f "${image_col3}" ] && [ -f "${image_col4}" ] && [ -f "${image_col6}" ]; then
      echo $y
      #      images[$i]=${image_col1} ##{output_directory}/SAH_1_01052014_2003_2_GRAY_031.jpg
      #      i=$(($i + 1))

      images[$i]=${image_col1} #/${grayscale_filename_basename_noext}_resaved_levelset_GRAY_${suffix}.jpg
      i=$(($i + 1))
      images[$i]=${image_col2} #/${grayscale_filename_basename_noext}_resaved_levelset_COMPLETE_CSF_${suffix}.jpg
      i=$(($i + 1))

      images[$i]=${image_col3} #/${grayscale_filename_basename_noext}_resaved_levelset_CSF_COMPARTMENTS_${suffix}.jpg
      i=$(($i + 1))
      images[$i]=${image_col4} #/${grayscale_filename_basename_noext}_resaved_levelset_SAH_COMPARTMENTS_TOTAL_${suffix}.jpg
      i=$(($i + 1))
      #    images[$i]=${image_col5} #/${grayscale_filename_basename_noext}_resaved_levelset_SAH_COMPARTMENTS_${suffix}.jpg
      #    i=$(($i + 1))

      images[$i]=${image_col6} #/SAH_1_01052014_2003_2_resaved_levelset_GRAY_${suffix}.jpg
      i=$(($i + 1))
      echo ${images[@]}
      outputfiles_present=$(python3 /software/utilities_simple_trimmed.py "${images[@]}")
      #        echo outputfiles_present::${outputfiles_present}
    fi

  done
  #  counter=$((counter +1))
  #  elif [ ${counter} -gt 0 ]; then

  #  fi
  #  break
  #done
  call_latex_end_arguments=('call_latex_end' ${latexfilename})
  pdfilename=${output_directory}/$(basename ${latexfilename%.tex*}.pdf)
  outputfiles_present=$(python3 /software/utilities_simple_trimmed.py "${call_latex_end_arguments[@]}")
  pdflatex -halt-on-error -interaction=nonstopmode -output-directory=${output_directory} ${latexfilename} ##${output_directory}/$(/usr/lib/fsl/5.0/remove_ext $this_filename)*.tex

  resource_dir='ICH_PHE_QUANTIFICATION'
  file_to_upload=${pdfilename}
  echo '${URI} ${file_to_upload} "${resource_dir}"'::::${URI}::${file_to_upload}::"${resource_dir}"
  call_uploadsinglefile_with_URI_arguments=('call_uploadsinglefile_with_URI' ${URI} ${file_to_upload} "${resource_dir}")
  outputfiles_present=$(python3 /software/download_with_session_ID.py "${call_uploadsinglefile_with_URI_arguments[@]}")
  file_to_upload=${csvfilename}
  echo '${URI} ${file_to_upload} "${resource_dir}"'::::${URI}::${file_to_upload}::"${resource_dir}"
  call_uploadsinglefile_with_URI_arguments=('call_uploadsinglefile_with_URI' ${URI} ${file_to_upload} "${resource_dir}")
  outputfiles_present=$(python3 /software/download_with_session_ID.py "${call_uploadsinglefile_with_URI_arguments[@]}")

### CHECK IF THE PDF AND CSV AVAILABLE AT ICH_QUANTIFICATION
# resource_dir=${2}   #"NIFTI"
fi

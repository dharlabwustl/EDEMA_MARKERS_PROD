#!/bin/bash
SESSION_ID=${1}
XNAT_USER=${2}
XNAT_PASS=${3}
XNAT_HOST=${4}
VERSION='V_08162023'
time_now=$(date -dnow +%m_%d_%Y)
outputfiles_suffix=${VERSION}_${time_now}
/software/nwu_with_ich_mask.sh ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
#  cp /workingoutput/*.tex /working/
cp /workingoutput/*TOTAL*.csv /working/
cp /workingoutput/*.png /working/
/software/phe_nwu_calculation.sh ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
#  cp /workingoutput/*.tex /working/
cp /workingoutput/*TOTAL*.csv /working/
cp /workingoutput/*.png /working/

output_directory='/working'
#echo "HELLO" > /working/atulTOTAL.csv
counter=0
x=$(ls ${output_directory}/*_PHENWU_TOTAL_*.csv)
x1=$(ls ${output_directory}/*_ICHCSF*.csv )
#for x in ${output_directory}/*TOTAL*.csv; do
#  if [ ${counter} == 0 ] ; then
grayscale_filename_basename_noext=$(basename ${x%_threshold*})
latexfilename=${output_directory}/${grayscale_filename_basename_noext}_${outputfiles_suffix}.tex
csvfilename=${latexfilename%.tex*}.csv
cp ${x} ${csvfilename}
call_latex_start_arguments=('call_latex_start' ${latexfilename})
outputfiles_present=$(python3 /software/utilities_simple_trimmed.py "${call_latex_start_arguments[@]}")
# 	echo ${x%_threshold*} ;

for z in ${output_directory}/$(basename ${x%_threshold*})*gray.png; do

  #              filename=args.stuff[1]
  imagescale='0.12' #float(args.stuff[2])
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
  if [ -f "${image_col1}" ] && [ -f "${image_col2}" ] && [ -f "${image_col3}" ] && [ -f "${image_col4}" ] && [ -f "${image_col5}" ] && [ -f "${image_col6}" ]; then
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
    images[$i]=${image_col5} #/${grayscale_filename_basename_noext}_resaved_levelset_SAH_COMPARTMENTS_${suffix}.jpg
    i=$(($i + 1))

    images[$i]=${image_col6} #/SAH_1_01052014_2003_2_resaved_levelset_GRAY_${suffix}.jpg
    i=$(($i + 1))
    echo ${images[@]}
    outputfiles_present=$(python3 /software/utilities_simple_trimmed.py "${images[@]}")
    #        echo outputfiles_present::${outputfiles_present}
  fi

done
#  counter=$((counter +1))
#  elif [ ${counter} -gt 0 ]; then
call_combine_csv_horizontally_arguments=('call_combine_csv_horizontally' ${grayscale_filename_basename_noext} ${csvfilename} ${csvfilename} ${x1}) # ${output_directory}/${grayscale_filename_basename_noext}_bet_mask_WITHOUT_csf.csv ${output_directory}/$(basename ${mask_filename1%.nii*}.csv) ${output_directory}/$(basename ${mask_filename2%.nii*}.csv) ${output_directory}/$(basename ${mask_filename3%.nii*}.csv) ${output_directory}/$(basename ${mask_filename4%.nii*}.csv) ${output_directory}/$(basename ${mask_filename5%.nii*}.csv) ${output_directory}/$(basename ${mask_filename6%.nii*}.csv) ${output_directory}/$(basename ${mask_filename7%.nii*}.csv) ${output_directory}/$(basename ${mask_filename8%.nii*}.csv) ${output_directory}/$(basename ${mask_filename9%.nii*}.csv) ${output_directory}/$(basename ${mask_filename10%.nii*}.csv) ${output_directory}/$(basename ${mask_filename11%.nii*}.csv) ${output_directory}/$(basename ${mask_filename12%.nii*}.csv) ${output_directory}/$(basename ${mask_filename13%.nii*}.csv) ${output_directory}/$(basename ${mask_filename14%.nii*}.csv) ${output_directory}/$(basename ${mask_filename15%.nii*}.csv) ${output_directory}/$(basename ${mask_filename16%.nii*}.csv) ${output_directory}/$(basename ${mask_filename17%.nii*}.csv) ${output_directory}/$(basename ${mask_filename18%.nii*}.csv) ${output_directory}/$(basename ${mask_filename19%.nii*}.csv) ${output_directory}/$(basename ${mask_filename20%.nii*}.csv) ${output_directory}/$(basename ${mask_filename21%.nii*}.csv) ${output_directory}/$(basename ${mask_filename22%.nii*}.csv) ${output_directory}/$(basename ${mask_filename23%.nii*}.csv) ${output_directory}/$(basename ${mask_filename24%.nii*}.csv) ${output_directory}/$(basename ${mask_filename25%.nii*}.csv) ${output_directory}/$(basename ${mask_filename26%.nii*}.csv) ${output_directory}/$(basename ${mask_filename27%.nii*}.csv) ${output_directory}/$(basename ${mask_filename28%.nii*}.csv))
outputfiles_present=$(python3 /software/dividemasks_into_left_right.py "${call_combine_csv_horizontally_arguments[@]}")
#  fi
#  break
#done
call_latex_end_arguments=('call_latex_end' ${latexfilename})
pdfilename=${output_directory}/$(basename ${latexfilename%.tex*}.pdf)
outputfiles_present=$(python3 /software/utilities_simple_trimmed.py "${call_latex_end_arguments[@]}")
pdflatex -halt-on-error -interaction=nonstopmode -output-directory=${output_directory} ${latexfilename} ##${output_directory}/$(/usr/lib/fsl/5.0/remove_ext $this_filename)*.tex

  #!/bin/bash
  SESSION_ID=${1}
  XNAT_USER=${2}
  XNAT_PASS=${3}
  XNAT_HOST=${4}

  /software/nwu_with_ich_mask.sh ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
#  cp /workingoutput/*.tex /working/
  cp /workingoutput/*TOTAL*.csv /working/
  cp /workingoutput/*.png /working/
  /software/phe_nwu_calculation.sh   ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
#  cp /workingoutput/*.tex /working/
  cp /workingoutput/*TOTAL*.csv /working/
  cp /workingoutput/*.png /working/

    for x in /working/*.png; do #_resaved_levelset_GRAY

      #              filename=args.stuff[1]
      imagescale='0.18' #float(args.stuff[2])
      angle='90'        #float(args.stuff[3])
      space='1'         #float(args.stuff[4])
      i=0

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

      y=${x%.*}
      echo $y
      suffix=${y##*_}
      if [ -f "${x}" ] && [ -f "${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_GRAY_${suffix}.jpg" ] && [ -f "${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_COMPLETE_CSF_${suffix}.jpg" ] && [ -f "${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_CSF_COMPARTMENTS_${suffix}.jpg" ] && [ -f "${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_SAH_COMPARTMENTS_TOTAL_${suffix}.jpg" ] && [ -f "${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_SAH_COMPARTMENTS_${suffix}.jpg" ]; then
        images[$i]=${x} ##{output_directory}/SAH_1_01052014_2003_2_GRAY_031.jpg
        i=$(($i + 1))

        images[$i]=${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_GRAY_${suffix}.jpg
        i=$(($i + 1))
        images[$i]=${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_COMPLETE_CSF_${suffix}.jpg
        i=$(($i + 1))

        images[$i]=${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_CSF_COMPARTMENTS_${suffix}.jpg
        i=$(($i + 1))
        #        images[$i]=${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_SAH_COMPARTMENTS_TOTAL_${suffix}.jpg
        #        i=$(($i + 1))
        images[$i]=${output_directory}/${grayscale_filename_basename_noext}_resaved_levelset_SAH_COMPARTMENTS_${suffix}.jpg
        i=$(($i + 1))

        #    images[$i]=${output_directory}/SAH_1_01052014_2003_2_resaved_levelset_GRAY_${suffix}.jpg
        #    i=$(($i + 1))
        outputfiles_present=$(python3 utilities_simple_trimmed.py "${images[@]}")
        echo outputfiles_present::${outputfiles_present}
      fi
    done

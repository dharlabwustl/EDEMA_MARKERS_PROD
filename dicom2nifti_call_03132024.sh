#!/usr/bin/env bash
export XNAT_USER=${2} 
export XNAT_PASS=${3} 
export XNAT_HOST=${4} #"https://snipr-dev-test1.nrg.wustl.edu"
python3 /software/dicom2nifiti_03132024.py  ${1}
sessionID=${1}
working_dir=/workinginput
  this_session_id=${sessionID}
  xml_filename=${working_dir}/${this_session_id}.xml
  filename_xml=$(basename ${xml_filename})   #args.stuff[2]
  dir_to_save_xml=$(dirname ${xml_filename}) #args args.stuff[3]
  download_an_xmlfile_with_URIString_arguments=('download_an_xmlfile_with_URIString' ${this_session_id} ${filename_xml} ${dir_to_save_xml})
  outputfiles_present=$(python3 download_with_session_ID.py "${download_an_xmlfile_with_URIString_arguments[@]}")
csvfile_for_redcap=${working_dir}/total_niftifiles.csv
  fill_redcap_for_selected_scan_arguments=('fill_redcap_for_selected_scan' ${xml_filename} ${csvfile_for_redcap} ) #${subj_listfile})
  outputfiles_present=$(python3 download_with_session_ID.py "${fill_redcap_for_selected_scan_arguments[@]}")


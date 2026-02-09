
sessionID=${1}
python3 -c "from utilities_using_xnat_python import xnat_set_all_scan_types_in_session; xnat_set_all_scan_types_in_session('${sessionID}')"

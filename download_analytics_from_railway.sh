project_id=${1}
todaydate="_from_railway_$(date +"%Y_%m_%d")"".csv"
filename=${project_id}${todaydate}
python3 -c "from railway_fill_database import download_as_csv; download_as_csv( '${project_id}','${filename}')"
resource_label='ANALYTICS'
local_file_path=/software/${filename}
remote_filename=${filename}
python3 -c "from utilities_using_xnat_python import upload_file_to_project_resource; upload_file_to_project_resource( '${project_id}','${resource_label}','${filename}','${filename}')"
#def upload_file_to_project_resource(
#    project_id: str,
#    resource_label: str,
#    local_file_path: str,
#    remote_filename: str | None = None,
#    verify: bool = True,
#    use_multipart: bool = True,
#    log_file: str = "xnat_upload_errors.log",
#)
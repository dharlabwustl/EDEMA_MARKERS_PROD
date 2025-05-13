import os
import shutil

# Set the root of your XNAT download and the new flat destination
source_root = "COLI_HLP45_CT_2/scans"
destination_root = "COLI_HLP45_CT_2/SCANS"

# Create destination if it doesn't exist
os.makedirs(destination_root, exist_ok=True)

# Loop through all scans
for scan_dir in os.listdir(source_root):
    scan_path = os.path.join(source_root, scan_dir)
    if not os.path.isdir(scan_path):
        continue

    # Extract scan ID (e.g., "6-Z_Axial_Brain" → "6")
    scan_id = scan_dir.split("-")[0]

    # Traverse into resources
    resources_dir = os.path.join(scan_path, "resources")
    if not os.path.isdir(resources_dir):
        continue

    for resource in os.listdir(resources_dir):
        resource_path = os.path.join(resources_dir, resource, "files")
        if not os.path.isdir(resource_path):
            continue

        # Define destination: /input/SCANS/{scan_id}/{resource}/
        dest_dir = os.path.join(destination_root, scan_id, resource)
        os.makedirs(dest_dir, exist_ok=True)

        # Copy all files to the flattened structure
        for file_name in os.listdir(resource_path):
            src_file = os.path.join(resource_path, file_name)
            dst_file = os.path.join(dest_dir, file_name)

            shutil.copy2(src_file, dst_file)

print("Directory flattening complete.")


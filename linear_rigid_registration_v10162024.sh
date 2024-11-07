#!/usr/bin/env bash
moving_image_filename=${1}
fixed_image_filename=${2}
output_directory=${3}
output_filename=${output_directory}/'mov_'$(basename ${moving_image_filename%.nii*})_fixed_$(basename  ${fixed_image_filename%.nii*})_lin1
T_output_filename=${output_filename}.mat
/usr/lib/fsl/5.0/flirt  -in "${moving_image_filename}" -ref "${fixed_image_filename}"  -dof 12 -out "${output_filename}" -omat ${T_output_filename} -cost mutualinfo -searchrx -10 10 -searchry -10 10 -searchrz -10 10

  #!/bin/bash
  SESSION_ID=${1}
  XNAT_USER=${2}
  XNAT_PASS=${3}
  XNAT_HOST=${4}

  /software/nwu_with_ich_mask.sh ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
  cp /workingoutput/*.tex /working/
  cp /workingoutput/*.csv /working/
  cp /workingoutput/*.png /working/
  /software/phe_nwu_calculation.sh   ${SESSION_ID} $XNAT_USER $XNAT_PASS $XNAT_HOST
  cp /workingoutput/*.tex /working/
  cp /workingoutput/*.csv /working/
  cp /workingoutput/*.png /working/


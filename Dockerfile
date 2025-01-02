FROM sharmaatul11/fsl502py369ltx-full:latest
RUN apt update
RUN apt -y install iputils-ping
RUN mkdir /templateventricle
COPY scct_strippedResampled1.nii.gz   /templatenifti/
COPY  midlinecssfResampled1.nii.gz   /templatemasks/
COPY scct_strippedResampled1_onlyventricle.nii.gz /templateventricle/
RUN mkdir -p /callfromgithub
RUN chmod 755 /callfromgithub
COPY downloadcodefromgithub.sh /callfromgithub/
RUN chmod +x /callfromgithub/downloadcodefromgithub.sh
RUN apt install -y \
  dcm2niix  \ 
  vim  \ 
  zip  \ 
  unzip  \ 
  curl  \ 
  git \
  tree
RUN pip3 install \
  nibabel  \ 
  numpy  \ 
  xmltodict  \ 
  pandas  \ 
  requests  \ 
  pydicom  \ 
  python-gdcm  \ 
  glob2  \ 
  scipy  \ 
  pypng  \
  PyGithub \
  SimpleITK \
  h5py \
  webcolors \
  trimesh \
  shapely \
  rtree \
  natsort \
  pytablewriter \
  mysql-connector-python==8.0.27
ENV REDCAP_API='36F3BA05DE0507BEBDFB94CC5DA13F93'


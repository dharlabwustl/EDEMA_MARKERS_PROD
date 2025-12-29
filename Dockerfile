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
  mysql-connector-python==8.0.27 \
  jupyterlab \
  SQLAlchemy \
  xnat

ENV REDCAP_API='36F3BA05DE0507BEBDFB94CC5DA13F93'
ENV GOOGLE_MYSQL_DB_IP='34.58.59.235'
ENV GOOGLE_MYSQL_DB_PASS='dharlabwustl1!'
ENV MYSQL_HOST="metro.proxy.rlwy.net"
ENV MYSQL_PORT="40006"
ENV MYSQL_DB="railway"
ENV MYSQL_USER="root"
ENV MYSQL_PASSWORD="GKRwiDNiqoCnpEBPngVcuIpEgBkuutFI"


RUN apt-get update \
 && apt-get install -y openssh-client sshpass ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Default credentials baked into image (you can override at runtime if you want)
ENV CLUSTER_HOST=compute1-client-2.ris.wustl.edu
ENV CLUSTER_USER=atulkumar
ENV CLUSTER_PASS=KarauliSarkar1!

COPY run_ssh.sh /usr/local/bin/run_ssh.sh
RUN chmod +x /usr/local/bin/run_ssh.sh

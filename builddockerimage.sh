# ./bashtowriteDockerfile.sh
parent_dir=${1}

cat ${parent_dir}/Dockerfile_part1 > Dockerfile
echo "  "
command=""
for x in ${parent_dir}*.json ;
do 
	command="${command}   ${x}  "
done
echo $command
python /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/FROM_DOCUMENTS/docker-images/command2label.py  $command  >> ${parent_dir}/Dockerfile
# imagename=$1
imagename=${2} #fsl502py369withpacksnltx
#docker build -t sharmaatul11/${imagename} .
#docker push sharmaatul11/${imagename}
docker build -t registry.nrg.wustl.edu/docker/nrg-repo/sharmaatul11/${imagename} ${parent_dir}
docker push registry.nrg.wustl.edu/docker/nrg-repo/sharmaatul11/${imagename}
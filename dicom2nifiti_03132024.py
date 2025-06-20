#!/usr/bin/python

import os, sys, errno, shutil, uuid,subprocess
import math
import glob
import re,time
import requests
import pydicom as dicom
import pandas as pd
from xnatSession import XnatSession
from download_with_session_ID import *;
import DecompressDCM
# import label_probability

catalogXmlRegex = re.compile(r'.*\.xml$')
XNAT_HOST_URL='https://snipr.wustl.edu'
XNAT_HOST = os.environ['XNAT_HOST'] #XNAT_HOST_URL #
XNAT_USER =os.environ['XNAT_USER']
XNAT_PASS =os.environ['XNAT_PASS']
xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
xnatSession.renew_httpsession()
def get_slice_idx(nDicomFiles):
    return min(nDicomFiles-1, math.ceil(nDicomFiles*0.7)) # slice 70% through the brain

def get_metadata_session(sessionId):
    url = ("/data/experiments/%s/scans/?format=json" %    (sessionId))
    # #xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    # #xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    # #xnatSession.close_httpsession()
    metadata_session=response.json()['ResultSet']['Result']
    return metadata_session

def decide_image_conversion(metadata_session,scanId):

    decision=False
    usable=False
    brain_type=False
    for x in metadata_session:
        if x['ID']  == scanId:
            print(x['ID'])

            # result_usability = response.json()['ResultSet']['Result'][0]['quality']
            result_usability = x['quality']
            print(result_usability)

            if 'usable' in result_usability.lower():
                print(True)
                usable=True
            result_type= x['type']

            if 'z-axial-brain' in result_type.lower() or 'z-brain-thin' in result_type.lower():
                print(True)
                brain_type=True

            break

    if usable==True and brain_type==True:
        decision =True

    # return
    return decision


def get_dicom_from_filesystem(sessionId, scanId):
    # Handle DICOM files that are not stored in a directory matching their XNAT scanId
    print("No DICOM found in %s directory, querying XNAT for DICOM path" % scanId)
    #xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    url = ("/data/experiments/%s/scans/%s/files?format=json&locator=absolutePath&file_format=DICOM" % 
        (sessionId, scanId))
    #xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    if response.status_code != 200:
        raise Exception("Error querying XNAT for %s DICOM files: %s %s %s" % (scanId, 
                                                                              response.status_code, 
                                                                              response.reason, 
                                                                              response.text))
    result = response.json()['ResultSet']['Result']
    # print(result[0]) #['absolutePath'])
    nDicomFiles = len(result)
    # print(nDicomFiles)
    if nDicomFiles == 0:
        raise Exception("No DICOM files for %s stored in XNAT" % scanId)

    # Get 70% file and ensure it exists
    selDicomAbs = result[get_slice_idx(nDicomFiles)]['absolutePath']
    selDicomAbs_split=selDicomAbs.split('/')
    print(selDicomAbs_split[-5]+'_'+selDicomAbs_split[-3])
    command='dcm2niix -o /output/ -f ' + selDicomAbs_split[-5]+'_'+selDicomAbs_split[-3] + '  -m 1 ' + '    /input1/DICOM'
    subprocess.call(command,shell=True)

def get_dicom_using_xnat_1(sessionId, scanId):
    # total_niftifiles=0
    #xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    
    # Handle DICOM files that are not stored in a directory matching their XNAT scanId
#####################################################################
    # sessionId='SNIPR01_E00146'
    # scanId='4'
    url = ("/data/experiments/%s/scans/%s/files?format=json&locator=absolutePath&file_format=DICOM" % 
        (sessionId, scanId))
    #xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)

    if response.status_code != 200:

        return False
        # raise Exception("Error querying XNAT for %s DICOM files: %s %s %s" % (scanId, 
        #                                                                       response.status_code, 
        #                                                                       response.reason, 
        #                                                                       response.text))
    result = response.json()['ResultSet']['Result']
    # print(result[0]) #['absolutePath'])
    nDicomFiles = len(result)
    # print(nDicomFiles)
    print("I AM AT DECIDE_IMAGE_CONVERSION")

    print(f"::{response.json()}::{nDicomFiles}")
    if nDicomFiles == 0:
        return False
        # raise Exception("No DICOM files for %s stored in XNAT" % scanId)

    # Get 70% file and ensure it exists
    selDicomAbs = result[get_slice_idx(nDicomFiles)]['absolutePath']
    selDicomAbs_split=selDicomAbs.split('/')
    print(selDicomAbs_split[-5]+'_'+selDicomAbs_split[-3])
    ######################################################################################

    # print("No DICOM found in %s directory, querying XNAT for DICOM path" % scanId)
    url = ("/data/experiments/%s/scans/%s/resources/DICOM/files?format=zip" % 
        (sessionId, scanId))

    #xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    zipfilename=sessionId+scanId+'.zip'
    with open(zipfilename, "wb") as f:
        for chunk in response.iter_content(chunk_size=512):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    command = 'unzip -d /output ' + zipfilename
    subprocess.call(command,shell=True)
    command='dcm2niix -o /output/ -f ' + "%t" + '  -m 1 ' + '    /output/*'
    subprocess.call(command,shell=True)
    ## rename nifti file:
    ####################################################
    folder_path = "/output"

    # List all NIFTI files in the folder
    nifti_files = [f for f in os.listdir(folder_path) if f.endswith(".nii") or f.endswith(".nii.gz")]

    # Find the largest file by size
    largest_file = max(nifti_files, key=lambda f: os.path.getsize(os.path.join(folder_path, f)))

    # # Print the result
    # print(f"Largest file: {largest_file}")
    largest_file_path = os.path.join(folder_path, largest_file)
    print(f"Path to largest file: {largest_file_path}")
    niftifile=largest_file_path #
    current_filename=os.path.basename(niftifile).split('.nii')[0]
    new_filename="_".join(("_".join(selDicomAbs_split[6].split("_")[0:2]),"{}{}_{}".format(current_filename[4:8],current_filename[0:4],current_filename[8:12]),scanId)) #selDicomAbs_split[-3]))
    new_filename_path=os.path.join(os.path.dirname(niftifile),new_filename+".nii")
    command = "mv "  + niftifile + "  " + new_filename_path
    subprocess.call(command,shell=True)
    #####################################################

    # for niftifile in glob.glob("/output/*.nii"):
    #     # total_niftifiles=total_niftifiles+1
    #     current_filename=largest_file_path #os.path.basename(niftifile).split('.nii')[0]
    #     new_filename="_".join(("_".join(selDicomAbs_split[6].split("_")[0:2]),"{}{}_{}".format(current_filename[4:8],current_filename[0:4],current_filename[8:12]),scanId)) #selDicomAbs_split[-3]))
    #     new_filename_path=os.path.join(os.path.dirname(niftifile),new_filename+".nii")
    #     command = "mv "  + niftifile + "  " + new_filename_path
    #     subprocess.call(command,shell=True)
    # command='dcm2niix -o /output/ -f ' + selDicomAbs_split[-5]+'_'+selDicomAbs_split[-3] + '  -m 1 ' + '    /output/*'
    # subprocess.call(command,shell=True)
    # command = 'cp /output/' + selDicomAbs_split[-5]+'_'+selDicomAbs_split[-3] + '.nii   ' + '/output/'
    # subprocess.call(command,shell=True)
    url = ("/data/experiments/%s/scans/%s/resources/NIFTI/files/" %
        (sessionId, scanId))
    # allniftifiles=glob.glob('/output/' + selDicomAbs_split[-5]+'_'+selDicomAbs_split[-3] + '*.nii')
    # for eachniftifile in allniftifiles:
    eachniftifile=new_filename_path
    files={'file':open(eachniftifile,'rb')}
    response = xnatSession.httpsess.post(xnatSession.host + url,files=files)
    print(response)
    #xnatSession.close_httpsession()
    for eachniftifile in glob.glob('/output/' +  '*.nii'):

        command= 'rm  ' + eachniftifile
        subprocess.call(command,shell=True)

    return True


def get_dicom_using_xnat(sessionId, scanId):
    # total_niftifiles=0
    # xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)

    # Handle DICOM files that are not stored in a directory matching their XNAT scanId
    #####################################################################
    # sessionId='SNIPR01_E00146'
    # scanId='4'
    session_label=get_session_label(sessionId) #, outputfile="NONE.csv")
    # url = ("/data/experiments/%s/scans/%s/files?format=json&locator=absolutePath&file_format=DICOM" %
    #        (sessionId, scanId))
    # # xnatSession.renew_httpsession()
    # response = xnatSession.httpsess.get(xnatSession.host + url)
    #
    # if response.status_code != 200:
    #     return False
    #     # raise Exception("Error querying XNAT for %s DICOM files: %s %s %s" % (scanId,
    #     #                                                                       response.status_code,
    #     #                                                                       response.reason,
    #     #                                                                       response.text))
    # result = response.json()['ResultSet']['Result']
    # # print(result[0]) #['absolutePath'])
    # nDicomFiles = len(result)
    # # print(nDicomFiles)
    # print("I AM AT DECIDE_IMAGE_CONVERSION")
    #
    # print(f"::{response.json()}::{nDicomFiles}")
    # if nDicomFiles == 0:
    #     return False
    #     # raise Exception("No DICOM files for %s stored in XNAT" % scanId)
    #
    # # Get 70% file and ensure it exists
    # selDicomAbs = result[get_slice_idx(nDicomFiles)]['absolutePath']
    # selDicomAbs_split = selDicomAbs.split('/')
    # print(selDicomAbs_split[-5] + '_' + selDicomAbs_split[-3])
    ######################################################################################

    # print("No DICOM found in %s directory, querying XNAT for DICOM path" % scanId)
    url = ("/data/experiments/%s/scans/%s/resources/DICOM/files?format=zip" %
           (sessionId, scanId))

    # xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    zipfilename = sessionId + scanId + '.zip'
    with open(zipfilename, "wb") as f:
        for chunk in response.iter_content(chunk_size=512):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    command = 'unzip -d /output ' + zipfilename
    subprocess.call(command, shell=True)
    command = 'dcm2niix -o /output/ -f ' + "%t" + '  -m 1 ' + '    /output/*'
    subprocess.call(command, shell=True)
    ## rename nifti file:
    ####################################################
    folder_path = "/output"

    # List all NIFTI files in the folder
    nifti_files = [f for f in os.listdir(folder_path) if f.endswith(".nii") or f.endswith(".nii.gz")]

    # Find the largest file by size
    largest_file = max(nifti_files, key=lambda f: os.path.getsize(os.path.join(folder_path, f)))

    # # Print the result
    # print(f"Largest file: {largest_file}")
    largest_file_path = os.path.join(folder_path, largest_file)
    print(f"Path to largest file: {largest_file_path}")
    niftifile = largest_file_path  #
    current_filename = os.path.basename(niftifile).split('.nii')[0]
    # new_filename = "_".join(("_".join(selDicomAbs_split[6].split("_")[0:2]),
    #                          "{}{}_{}".format(current_filename[4:8], current_filename[0:4], current_filename[8:12]),
    #                          scanId))  # selDicomAbs_split[-3]))
    new_filename = "_".join(("_".join(session_label.split("_")[0:2]),
                             "{}{}_{}".format(current_filename[4:8], current_filename[0:4], current_filename[8:12]),
                             scanId))
    new_filename_path = os.path.join(os.path.dirname(niftifile), new_filename + ".nii")
    print(new_filename_path)
    # return
    command = "mv " + niftifile + "  " + new_filename_path
    subprocess.call(command, shell=True)
    #####################################################

    # for niftifile in glob.glob("/output/*.nii"):
    #     # total_niftifiles=total_niftifiles+1
    #     current_filename=largest_file_path #os.path.basename(niftifile).split('.nii')[0]
    #     new_filename="_".join(("_".join(selDicomAbs_split[6].split("_")[0:2]),"{}{}_{}".format(current_filename[4:8],current_filename[0:4],current_filename[8:12]),scanId)) #selDicomAbs_split[-3]))
    #     new_filename_path=os.path.join(os.path.dirname(niftifile),new_filename+".nii")
    #     command = "mv "  + niftifile + "  " + new_filename_path
    #     subprocess.call(command,shell=True)
    # command='dcm2niix -o /output/ -f ' + selDicomAbs_split[-5]+'_'+selDicomAbs_split[-3] + '  -m 1 ' + '    /output/*'
    # subprocess.call(command,shell=True)
    # command = 'cp /output/' + selDicomAbs_split[-5]+'_'+selDicomAbs_split[-3] + '.nii   ' + '/output/'
    # subprocess.call(command,shell=True)
    url = ("/data/experiments/%s/scans/%s/resources/NIFTI/files/" %
           (sessionId, scanId))
    # allniftifiles=glob.glob('/output/' + selDicomAbs_split[-5]+'_'+selDicomAbs_split[-3] + '*.nii')
    # for eachniftifile in allniftifiles:
    eachniftifile = new_filename_path
    files = {'file': open(eachniftifile, 'rb')}
    response = xnatSession.httpsess.post(xnatSession.host + url, files=files)
    print(response)
    # xnatSession.close_httpsession()
    for eachniftifile in glob.glob('/output/' + '*.nii'):
        command = 'rm  ' + eachniftifile
        subprocess.call(command, shell=True)

    return True


if __name__ == '__main__':
    sessionId=sys.argv[1]
    total_niftifiles=0
    metadata_session=get_metadata_session(sessionId)
    for x in metadata_session:
        # if int(x['ID']) == scanId:
        command="rm -r /NIFTIFILEDIR/*"
        subprocess.call(command,shell=True)
        # for x in range(1,5):
        #     print(sys.argv[x])
        command="rm -r /ZIPFILEDIR/*"
        subprocess.call(command,shell=True)
        command="rm -r /DICOMFILEDIR/*"
        subprocess.call(command,shell=True)
        command="rm -r /output/*"
        subprocess.call(command,shell=True)
        scanId=x['ID']
        URI=x['URI']
        print("URI::{}".format(URI))
        resource_dir="NIFTI"
        extension_to_find_list=[".nii"]
        # file_present=check_if_a_file_exist_in_snipr(URI, resource_dir,extension_to_find_list)
        if 1>0 : #file_present < len(extension_to_find_list):
            print("REQUIRED NUMBER OF FILES NOT PRESENT, SO , WORKING ON IT")
            decision=decide_image_conversion(metadata_session,scanId)

            message_text="Before decision scanId: " + scanId
            command="echo " + message_text +"  >>  logmessage.txt"
            subprocess.call(command,shell=True)
            # print("Decision::{}".format(decision))
            if decision==True:

                #xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
                #xnatSession.renew_httpsession()
                outcome=get_dicom_using_xnat(sessionId, scanId)
                total_niftifiles=total_niftifiles+1
                message_text="If true decision: scanId: " + scanId
                command="echo " + message_text +"  >>  logmessage.txt"
                subprocess.call(command,shell=True)
                ####
                try:
                    resource_dirname="NIFTI"
                    # URI = "/data/experiments/"+sessionId+"/scans/"+scanId #%s")  %
                    # URI = (URI+'/resources/' + resource_dirname +'/files?format=json')
                    # df_listfile=listoffile_witha_URI_as_df(URI)
                    # now=time.localtime()
                    # date_time = time.strftime("_%m_%d_%Y",now)
                    # niftifile_location=os.path.join("/output","NIFTIFILE_LOCATION"+"_" +sessionId+"_" +scanId+date_time+".csv")
                    # df_listfile.to_csv(niftifile_location,index=False)
                    # resource_dirname="NIFTI_LOCATION"
                    # url = (("/data/experiments/%s") % (sessionId))
                    # # uploadsinglefile_with_URI(url,niftifile_location,resource_dirname)
                    # print('File:{}:: uploaded successfully',format(niftifile_location))
                except:
                    print("FILE COULD NOT BE UPLOADED")
                    pass
                ####
                if outcome==False:
                    # print("NO DICOM FILE %s:%s:%s:%s" % (sessionId, scanId))
                    message_text="If false decision: scanId: " + scanId
                    command="echo " + message_text +"  >>  logmessage.txt"
                    subprocess.call(command,shell=True)
                #xnatSession.close_httpsession()
            else:
                print("This was not axial brain image::{}".format(URI))

        else:
            print("FILES PRESENT")
    dcm2nifti_complete=0
    if total_niftifiles>0:
        dcm2nifti_complete=1
    total_niftifiles_df=pd.DataFrame([dcm2nifti_complete,total_niftifiles]).transpose()
    total_niftifiles_df.columns=['dcm2nifti_complete','nifti_files_num']
    total_niftifiles_df.to_csv('/workinginput/total_niftifiles.csv',index=False)
        # #xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
        # #xnatSession.renew_httpsession()
        # url = ("/data/experiments/%s/resources/TEST/files/" % (sessionId, scanId))
        # files={'file':open('logmessage.txt','rb')}
        # response = xnatSession.httpsess.post(xnatSession.host + url,files=files)
        # #xnatSession.close_httpsession()
        # print(response)
    xnatSession.close_httpsession()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 17:04:42 2020

@author: atul
"""
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 10:26:44 2019

@author: atul
"""
from skimage import exposure
import glob,os,csv,sys
import nibabel as nib
import numpy as np
import cv2 , re,subprocess,time,math
sys.path.append("/software")
#sys.path.append("/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/DOCKERIZE/DOCKERIZEPYTHON/docker_fsl/docker/fsl/fsl-v5.0")
from utilities_simple import *
from github import Github
#############################################################
from dateutil.parser import parse
import pandas as pd
g = Github()
repo = g.get_repo("dharlabwustl/EDEMA_MARKERS")
contents = repo.get_contents("module_NWU_CSFCompartment_Calculations.py")
dt = parse(contents.last_modified)

Version_Date="_VersionDate-" + dt.strftime("%m%d%Y")

#############################################################


now=time.localtime()


def remove_few_columns(csvfilename,columnstoremove):
    csvfilename_df=pd.read_csv(csvfilename)
    csvfilename_df.drop(columnstoremove, axis=1, inplace=True)
    csvfilename_df.to_csv(csvfilename.split('.csv')[0]+'columndropped.csv',index=False)






def determine_ICH_side(numpy_image,filename_gray_data_np_copy,niftifilename,npyfiledirectory,csf_seg_np,numpy_image_mask):
    ICH_side='NONE'
    left_ids=[]
    right_ids=[]
    left_side_ones=0
    right_side_ones=0
    for img_idx in range(numpy_image.shape[2]):
        #             print("I AM HERE 4")
        if img_idx>0 and img_idx < numpy_image.shape[2] and  filename_gray_data_np_copy.shape==csf_seg_np.shape:
            method_name="REGIS"

            slice_number="{0:0=3d}".format(img_idx)
            filename_tosave=re.sub('[^a-zA-Z0-9 \n\_]', '', os.path.basename(niftifilename).split(".nii")[0])
            this_npyfile=os.path.join(npyfiledirectory,filename_tosave+method_name+str(slice_number)+  ".npy")

            #                this_npyfile=os.path.join(npyfiledirectory,os.path.basename(niftifilename).split(".nii")[0]+str(img_idx)+npyfileextension)
            if os.path.exists(this_npyfile):
                calculated_midline_points=np.load(this_npyfile,allow_pickle=True)
                x_points2=calculated_midline_points.item().get('x_axis') #,y_points2=points_on_line(extremepoints)
                y_points2=calculated_midline_points.item().get('y_axis')
                #                            slice_3_layer= np.zeros([numpy_image.shape[0],numpy_image.shape[1],3])
                x_points2=x_points2[:,0]
                y_points2=y_points2[:,0]

                #################################################
                ######################################################################
                img_with_line_nonzero_id = np.transpose(np.nonzero(np.copy(numpy_image_mask[:,:,img_idx])))
                #                    thisimage=filename_gray_data_np_1[:,:,img_idx]
                #                    current_left_num=0
                #                    current_right_num=0
                #                    slice_3_layer= np.zeros([I_t_gray.shape[0],I_t_gray.shape[1],3])
                #                    slice_3_layer[:,:,0]= I_t_gray #imgray1
                #                    slice_3_layer[:,:,1]= I_t_gray #imgray1
                #                    slice_3_layer[:,:,2]= I_t_gray# imgray1

                #                     ICH_side="NO ICH"

                for non_zero_pixel in img_with_line_nonzero_id:
                    xx=whichsideofline((int(y_points2[511]),int(x_points2[511])),(int(y_points2[0]),int(x_points2[0])) ,non_zero_pixel)
                    if xx>0: ## RIGHT
                        #                            slice_3_layer[non_zero_pixel[0],non_zero_pixel[1],0]=0
                        #                            slice_3_layer[non_zero_pixel[0],non_zero_pixel[1],1]=100
                        #                            slice_3_layer[non_zero_pixel[0],non_zero_pixel[1],2]=200
                        right_side_ones = right_side_ones + 1 # I_t_mask[non_zero_pixel[0],non_zero_pixel[1]]
                        right_ids.append([non_zero_pixel[0],non_zero_pixel[1],img_idx])
                    #                        print()
                    if xx<0: ## LEFT
                        #                            slice_3_layer[non_zero_pixel[0],non_zero_pixel[1],0]=100
                        #                            slice_3_layer[non_zero_pixel[0],non_zero_pixel[1],1]=0
                        #                            slice_3_layer[non_zero_pixel[0],non_zero_pixel[1],2]=100
                        left_side_ones = left_side_ones + 1 #I_t_mask[non_zero_pixel[0],non_zero_pixel[1]]
                        left_ids.append([non_zero_pixel[0],non_zero_pixel[1],img_idx])

    if (left_side_ones > right_side_ones):
        ICH_side="LEFT"
        for right_id in right_ids:
            pass
            #             print("I am Left")
            # numpy_image_mask[right_id[0],right_id[1],right_id[2]]=np.min(numpy_image_mask)


    if (right_side_ones > left_side_ones):
        ICH_side="RIGHT"
        for left_id in left_ids:
            pass
            #             print("I am Right")
            # numpy_image_mask[left_id[0],left_id[1],left_id[2]]=np.min(numpy_image_mask)
    return ICH_side,numpy_image_mask


def call_nwu_csfcompartment():
    measure_ICH_Class1_Feb24_2023()
    measure_compartments_with_reg_round5_one_file_sh_v1()

def whichsideofline(line_pointA,line_pointB,point_todecide):

    return (point_todecide[0]-line_pointA[0])*(line_pointB[1]-line_pointA[1])  -  (point_todecide[1]-line_pointA[1])*(line_pointB[0]-line_pointA[0])

def measure_ICH_CLASS2_Feb_24_2023(): #niftifilename,npyfiledirectory,niftifilenamedir):
    ICH_side="NA"
    NWU="NA"
    ICH_pixels_number=0 #"NA"
    ICH_pixels_density="NA"
    nonfarct_pixels_number="NA"
    nonICH_pixels_density="NA"
    overall_ICH_vol="NA"
    overall_non_ICH_vol="NA"
    ICH_total_voxels_volume="NA"
    # print("I AM HERE1")

    niftifilename=sys.argv[1] #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/NetWaterUptake/DATA/ALLINONE_DATA_FROMJAMAL/WUSTL_798_03292019_Head_3.0_MPR_ax_20190329172552_2.nii" #sys.argv[1]
    niftifilenamedir=os.path.dirname(niftifilename)
    # grayscale_extension=sys.argv[2] #"_levelset.nii.gz"
    #    mask_extension=sys.argv[3] #"_final_seg.nii.gz" ## ICH mask extension
    npyfiledirectory=sys.argv[5]
    overall_ICH_vol=0
    overall_non_ICH_vol=0
    # SLICE_OUTPUT_DIRECTORY=sys.argv[4] #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/NetWaterUptake/RESULTS/IMAGES" #sys.argv[5]

    # csf_mask_extension=sys.argv[3]

    #    niftifilename=sys.argv[1] ## THis is the  gray file:
    #    grayfile_extension=sys.argv[2] #"_gray.nii.gz" #
    #    csf_maskfile_extension=sys.argv[3] #"_final_seg.nii.gz" #
    #    npyfiledirectory=sys.argv[4] #"/processedniftifiles" # "/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/NetWaterUptake/DATA/FU_CTs_Masks/SMOOTH_IML" # /media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/MIDLINE/RESULTS/RegistrationOnly/"
    #    niftifilenamedir=sys.argv[5] #"/inputdirectory" #sys.argv[1] #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/NetWaterUptake/DATA/FU_CTs_Masks/CTs" # "/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/CSF_Compartment/DATA/MISSINGDATA1/" #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/CSF_Compartment/DATA/NECT/ALLCOHORTINONE/TILTED"

    csf_mask_directory=os.path.dirname(sys.argv[3]) #"/inputdirectory_csfmask"
    ICH_mask_directory=os.path.dirname(sys.argv[7])
    #    print('sys.argv')
    print(sys.argv)
    SLICE_OUTPUT_DIRECTORY=sys.argv[6] #"/outputdirectory" #sys.argv[4] #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/NetWaterUptake/DATA/FU_CTs_Masks/CSF_RL_VOL_OUTPUT" #sys.argv[4] ####"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/MIDLINE/SOFTWARE/shellscript/RegistrationMethod/test"
    BET_OUTPUT_DIRECTORY=os.path.dirname(sys.argv[2])
    # BET_file_extension=sys.argv[9]
    # lower_thresh=0 #int(float(sys.argv[7])) #20 #0 # 20 #
    # upper_thresh=40 #int(float(sys.argv[8])) #80 # 40 # 80 #
    # lower_thresh_normal=20 #int(float(sys.argv[7]))
    # upper_thresh_normal=80 #int(float(sys.argv[8]))
    left_pixels_num=0
    right_pixels_num=0
    # print("ICH_mask_directory")
    # print(ICH_mask_directory)

    subject_name=os.path.basename(niftifilename).split(".nii")[0] #_gray")[0]
    count = 0
    dict_for_csv = []
    ICH_pixels_list=[]
    nonfarct_pixels_list=[]
    ICH_pixel_intensity=[]

    nonICH_pixel_intensity=[]
    # print("I AM HERE2")

    grayfilename_base=os.path.basename(niftifilename) #mask_basename+"levelset.nii.gz"

    grayfilename=niftifilename #os.path.join(levelset_file_directory,grayfilename) #os.path.join(niftifilenamedir,grayfilename)

    npyfileextension="REGISMethodOriginalRF_midline.npy"
    # print("I am here ICH_Mask_filename")

    ICH_Mask_filename=sys.argv[7] #ICH_Mask_filename_list[0] #os.path.join(niftifilenamedir,"Masks",mask_basename)
    csf_seg_maskbasename_path=sys.argv[3] #csf_seg_maskbasename_path_list[0] #os.path.join(niftifilenamedir,"Masks",csf_seg_maskbasename)
    ICH_Mask_filename_part1, ICH_Mask_filename_part2 = os.path.splitext(ICH_Mask_filename)

    ICH_side="NONE"

    if os.path.exists(csf_seg_maskbasename_path) and os.path.exists(ICH_Mask_filename) and os.path.exists(niftifilename):


        if 'hdr' in ICH_Mask_filename_part2:
            ICH_Mask_filename_data_np=resizeinto_512by512(nib.AnalyzeImage.from_filename(ICH_Mask_filename).get_fdata()) #nib.load(ICH_Mask_filename).get_fdata()
            niftifilename_data=nib.load(niftifilename).get_fdata()
            if niftifilename_data.shape[2] > ICH_Mask_filename_data_np.shape[2]:
                difference_slices=niftifilename_data.shape[2] - ICH_Mask_filename_data_np.shape[2]
                for slice_num in range(difference_slices):
                    ICH_Mask_filename_data_np[:,:,ICH_Mask_filename_data_np.shape[2]+slice_num]=ICH_Mask_filename_data_np[:,:,0]
        #             filename_gray_data_np_copy=np.copy(niftifilename_data)

        if 'gz' in ICH_Mask_filename_part2:
            ICH_Mask_filename_data_np=resizeinto_512by512(nib.load(ICH_Mask_filename).get_fdata()) #resizeinto_512by512(image_nib_nii_file_data)

            niftifilename_data=nib.load(niftifilename).get_fdata()
            if niftifilename_data.shape[2] > ICH_Mask_filename_data_np.shape[2]:
                difference_slices=niftifilename_data.shape[2] - ICH_Mask_filename_data_np.shape[2]
                for slice_num in range(difference_slices):
                    ICH_Mask_filename_data_np[:,:,ICH_Mask_filename_data_np.shape[2]+slice_num]=ICH_Mask_filename_data_np[:,:,0]

            #             filename_gray_data_np_copy=np.copy(niftifilename_data)

            ## volume of the ICH mask:
            ICH_total_voxels = ICH_Mask_filename_data_np[ICH_Mask_filename_data_np>np.min(ICH_Mask_filename_data_np)]
            ICH_total_voxels_count=ICH_total_voxels.shape[0]
            ICH_total_voxels_volume = ICH_total_voxels.shape[0]*np.prod(np.array(nib.load(niftifilename).header["pixdim"][1:4]))
            ICH_total_voxels_volume=ICH_total_voxels_volume/1000

        if len(ICH_Mask_filename_data_np.shape) == 4:
            ICH_Mask_filename_data_np=ICH_Mask_filename_data_np[:,:,:,0]

        filename_gray_data_np=resizeinto_512by512(nib.load(niftifilename).get_fdata()) #nib.load(niftifilename).get_fdata() #
        filename_gray_data_np_copy=np.copy(filename_gray_data_np)
        file_gray=niftifilename
        csf_seg_np=resizeinto_512by512(nib.load(csf_seg_maskbasename_path).get_fdata()) #nib.load(csf_seg_maskbasename_path).get_fdata() #
        min_val=np.min(csf_seg_np)
        filename_gray_data_np=contrast_stretch_np(filename_gray_data_np,1) #exposure.rescale_intensity( filename_gray_data_np , in_range=(1000, 1200))
        filename_gray_data_np_1=contrast_stretch_np(resizeinto_512by512(nib.load(grayfilename).get_fdata()),1)*255 #np.uint8(filename_gray_data_np*255) contrast_stretch_np(nib.load(grayfilename).get_fdata(),1)*255  #c
        # filename_gray_data_np[csf_seg_np>min_val]=np.min(filename_gray_data_np)#255
        numpy_image=normalizeimage0to1(filename_gray_data_np)*255 #filename_gray_data_np #

        print('filename_gray_data_np_copy size = {}'.format(filename_gray_data_np_copy.shape))
        print('csf_seg_np size = {}'.format(csf_seg_np.shape))

        # filename_gray_data_np_copy[csf_seg_np>min_val]=np.min(filename_gray_data_np_copy) #+10.0 ##255

        ICH_side,ICH_Mask_filename_data_np=determine_ICH_side(numpy_image,filename_gray_data_np_copy,niftifilename,npyfiledirectory,csf_seg_np,ICH_Mask_filename_data_np)
        # filename_gray_data_np_copy=normalizeimage0to1(filename_gray_data_np_copy)*255
        numpy_image_mask=ICH_Mask_filename_data_np
        lower_thresh=np.min(filename_gray_data_np_copy) #int(float(sys.argv[7])) #20 #0 # 20 #
        upper_thresh=np.max(filename_gray_data_np_copy) #int(float(sys.argv[8])) #80 # 40 # 80 #
        lower_thresh_normal=np.min(filename_gray_data_np_copy) #int(float(sys.argv[7]))
        upper_thresh_normal=np.max(filename_gray_data_np_copy) #int(float(sys.argv[8]))
        for img_idx in range(numpy_image.shape[2]):
            #             print("I AM HERE 4")
            if img_idx>0 and img_idx < numpy_image.shape[2] and  filename_gray_data_np_copy.shape==csf_seg_np.shape:
                method_name="REGIS"

                slice_number="{0:0=3d}".format(img_idx)
                filename_tosave=re.sub('[^a-zA-Z0-9 \n\_]', '', os.path.basename(niftifilename).split(".nii")[0])
                this_npyfile=os.path.join(npyfiledirectory,filename_tosave+method_name+str(slice_number)+  ".npy")

                #                this_npyfile=os.path.join(npyfiledirectory,os.path.basename(niftifilename).split(".nii")[0]+str(img_idx)+npyfileextension)
                if os.path.exists(this_npyfile):
                    calculated_midline_points=np.load(this_npyfile,allow_pickle=True)
                    x_points2=calculated_midline_points.item().get('x_axis') #,y_points2=points_on_line(extremepoints)
                    y_points2=calculated_midline_points.item().get('y_axis')
                    #                            slice_3_layer= np.zeros([numpy_image.shape[0],numpy_image.shape[1],3])
                    x_points2=x_points2[:,0]
                    y_points2=y_points2[:,0]

                    #################################################
                    ######################################################################
                    img_with_line_nonzero_id = np.transpose(np.nonzero(np.copy(numpy_image_mask[:,:,img_idx])))

                    lineThickness = 2
                    #                            lineThickness = 2
                    img_with_line=filename_gray_data_np_1[:,:,img_idx] #np.int8(numpy_image[:,:,img_idx])

                    v1=np.array([512,0]) ## point from the image
                    v2_1=np.array([x_points2[0],y_points2[0]]) ## point 1 from the midline
                    v2_2=np.array([x_points2[1],y_points2[1]]) ## point 2 from the midline
                    v2=v2_2-v2_1

                    angle=  angle_bet_two_vector(v1,v2)
                    angleRad=angle_bet_two_vectorRad(v1,v2)
                    ## translation:
                    points=np.array([[x_points2[0],y_points2[0]],[x_points2[511],y_points2[511]]])
                    mid_point_line=np.mean(points,axis=0)
                    # delta translation:
                    image_midpoint=np.array([int(filename_gray_data_np_1[:,:,img_idx].shape[0]/2),int(filename_gray_data_np_1[:,:,img_idx].shape[1]/2)]) #np.array([255,255])
                    translation_delta=image_midpoint-mid_point_line
                    M = np.float32([[1,0,translation_delta[0]],[0,1,translation_delta[1]]])
                    I_t_gray =cv2.warpAffine(np.copy(numpy_image[:,:,img_idx]),M,(filename_gray_data_np_1[:,:,img_idx].shape[0],filename_gray_data_np_1[:,:,img_idx].shape[1]), flags= cv2.INTER_NEAREST) # cv2.warpAffine(np.copy(numpy_image[:,:,img_idx]),M,(512,512), flags= cv2.INTER_NEAREST)
                    I_t_mask =cv2.warpAffine(np.copy(numpy_image_mask[:,:,img_idx]),M,(filename_gray_data_np_1[:,:,img_idx].shape[0],filename_gray_data_np_1[:,:,img_idx].shape[1]) , flags= cv2.INTER_NEAREST) # cv2.warpAffine(np.copy(numpy_image_mask[:,:,img_idx]),M,(512,512) , flags= cv2.INTER_NEAREST)

                    #########################################################################


                    translate_points= points+translation_delta
                    #                    show_slice_withaline(I_t_mask,translate_points)
                    points=translate_points
                    ## translation matrix
                    p1x,p1y= rotate_around_point_highperf(np.array([points[0][0],points[0][1]]), angleRad, origin=(255,255))
                    p2x,p2y= rotate_around_point_highperf(np.array([points[1][0],points[1][1]]), angleRad, origin=(255,255))
                    points1=np.array([[p1x,p1y],[p2x,p2y]])

                    I_t_r_gray=rotate_image(I_t_gray,(255,255),angle)
                    #                    show_slice_withaline(I_t_r_gray,points1)
                    I_t_r_mask=rotate_image(I_t_mask,(255,255),angle)

                    I_t_r_f_gray=cv2.flip(I_t_r_gray,0)
                    I_t_r_f_mask=cv2.flip(I_t_r_mask,0)

                    I_t_r_f_rinv_gray=rotate_image(I_t_r_f_gray,(256,256),-angle)
                    I_t_r_f_rinv_mask=rotate_image(I_t_r_f_mask,(256,256),-angle)
                    p1x,p1y= rotate_around_point_highperf(np.array([points1[0][0],points1[0][1]]), -angleRad, origin=(255,255))
                    p2x,p2y= rotate_around_point_highperf(np.array([points1[1][0],points1[1][1]]), -angleRad, origin=(255,255))
                    points1=np.array([[p1x,p1y],[p2x,p2y]])
                    #show_slice_withaline(I_t_r_f_rinv_gray,points1)
                    #                    show_slice_withaline(I_t_r_f_rinv_mask,points1)
                    M = np.float32([[1,0,-translation_delta[0]],[0,1,-translation_delta[1]]])
                    I_t_r_f_rinv_tinv_gray = cv2.warpAffine(I_t_r_f_rinv_gray,M,(512,512) , flags= cv2.INTER_NEAREST)
                    I_t_r_f_rinv_tinv_mask = numpy_image_mask[:,:,img_idx] #cv2.warpAffine(I_t_r_f_rinv_mask,M,(512,512), flags= cv2.INTER_NEAREST )
                    points1=points1-translation_delta
                    #show_slice_withaline(I_t_r_f_rinv_tinv_gray,points1)
                    #                    show_slice_withaline(I_t_r_f_rinv_tinv_mask,points1)
                    I4=np.copy(numpy_image[:,:,img_idx])
                    print("I4 size")
                    print(I4.shape)
                    print("I_t_r_f_rinv_tinv_mask")
                    print(I_t_r_f_rinv_tinv_mask.shape)
                    I4[I_t_r_f_rinv_tinv_mask>0]=255
                    I4[np.copy(numpy_image_mask[:,:,img_idx])>0]=255
                    I5=np.copy(filename_gray_data_np_copy[:,:,img_idx])
                    cv2.imwrite(os.path.join(niftifilenamedir,"I4_img" +grayfilename_base + "_1.jpg"),I4)
                    I4_img_1=cv2.imread(os.path.join(niftifilenamedir,"I4_img" +grayfilename_base + "_1.jpg"))
                    img_with_line1=cv2.line(I4_img_1, (int(points1[0][0]),int(points1[0][1])), (int(points1[1][0]),int(points1[1][1])), (0,255,0), lineThickness)
                    slice_number="{0:0=3d}".format(img_idx)
                    slice_3_layer1= np.zeros([filename_gray_data_np_copy[:,:,img_idx].shape[0],filename_gray_data_np_copy[:,:,img_idx].shape[1],3])
                    slice_3_layer1[:,:,0]= filename_gray_data_np_copy[:,:,img_idx] #imgray1
                    slice_3_layer1[:,:,0][np.copy(numpy_image_mask[:,:,img_idx])>0]=0
                    slice_3_layer1[:,:,1]= filename_gray_data_np_copy[:,:,img_idx] #imgray1
                    slice_3_layer1[:,:,1][np.copy(numpy_image_mask[:,:,img_idx])>0]=100
                    slice_3_layer1[:,:,2]= filename_gray_data_np_copy[:,:,img_idx]# imgray1
                    slice_3_layer1[:,:,2][np.copy(numpy_image_mask[:,:,img_idx])>0]=200
                    imagefilename=os.path.basename(niftifilename).split(".nii")[0].replace(".","_")+"_" +str(slice_number)
                    imagename=os.path.join(SLICE_OUTPUT_DIRECTORY,imagefilename +"_ICH.png")
                    imagename_class2=os.path.join(SLICE_OUTPUT_DIRECTORY,imagefilename +"_class2.png")
                    image_ICH_details=os.path.join(SLICE_OUTPUT_DIRECTORY,imagefilename +"_ICH_details.png")
                    image_ICH_nonICH_histogram=os.path.join(SLICE_OUTPUT_DIRECTORY,imagefilename +"_ICH_nonICH_histogram.png")
                    numpy_image_mask_flatten=numpy_image_mask[:,:,img_idx].flatten()
                    ICH_pixels_number=ICH_pixels_number+len(numpy_image_mask_flatten[np.nonzero(numpy_image_mask_flatten)]) #ICH_pixels.flatten()
                    cv2.imwrite(imagename_class2,slice_3_layer1) # img_with_line1) #
                    cv2.imwrite(imagename,img_with_line1) #
                    cv2.imwrite(image_ICH_details,img_with_line1)
    # lower_thresh=0
    # upper_thresh=0
    # lower_thresh_normal=0
    # upper_thresh_normal=0
    ICH_total_voxels_volume=ICH_pixels_number*np.prod(np.array(nib.load(niftifilename).header["pixdim"][1:4]))
    # ICH_side='AA'
    NWU=0
    # ICH_pixels_number=0
    # ICH_pixels_density=0
    nonfarct_pixels_number=0
    nonICH_pixels_density=0
    overall_ICH_vol=ICH_total_voxels_volume #0
    overall_non_ICH_vol=0


    return lower_thresh,upper_thresh,lower_thresh_normal,upper_thresh_normal, ICH_total_voxels_volume, ICH_side,NWU,ICH_pixels_number,ICH_pixels_density,nonfarct_pixels_number,nonICH_pixels_density, overall_ICH_vol,overall_non_ICH_vol



def measure_ICH_Class1_Feb24_2023(): #niftifilename,npyfiledirectory,niftifilenamedir):
    ICH_side="NA"
    NWU="NA"
    ICH_pixels_number=0 #"NA"
    ICH_pixels_density=0 #"NA"
    nonfarct_pixels_number="NA"
    nonICH_pixels_density="NA"
    overall_ICH_vol="NA"
    overall_non_ICH_vol="NA"
    ICH_total_voxels_volume="NA"
    # print("I AM HERE1")

    niftifilename=sys.argv[1] #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/NetWaterUptake/DATA/ALLINONE_DATA_FROMJAMAL/WUSTL_798_03292019_Head_3.0_MPR_ax_20190329172552_2.nii" #sys.argv[1]
    niftifilenamedir=os.path.dirname(niftifilename)
    # grayscale_extension=sys.argv[2] #"_levelset.nii.gz"
    #    mask_extension=sys.argv[3] #"_final_seg.nii.gz" ## ICH mask extension
    npyfiledirectory=sys.argv[5]
    overall_ICH_vol=0
    overall_non_ICH_vol=0
    # SLICE_OUTPUT_DIRECTORY=sys.argv[4] #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/NetWaterUptake/RESULTS/IMAGES" #sys.argv[5]

    # csf_mask_extension=sys.argv[3]

    #    niftifilename=sys.argv[1] ## THis is the  gray file:
    #    grayfile_extension=sys.argv[2] #"_gray.nii.gz" #
    #    csf_maskfile_extension=sys.argv[3] #"_final_seg.nii.gz" #
    #    npyfiledirectory=sys.argv[4] #"/processedniftifiles" # "/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/NetWaterUptake/DATA/FU_CTs_Masks/SMOOTH_IML" # /media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/MIDLINE/RESULTS/RegistrationOnly/"
    #    niftifilenamedir=sys.argv[5] #"/inputdirectory" #sys.argv[1] #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/NetWaterUptake/DATA/FU_CTs_Masks/CTs" # "/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/CSF_Compartment/DATA/MISSINGDATA1/" #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/CSF_Compartment/DATA/NECT/ALLCOHORTINONE/TILTED"

    csf_mask_directory=os.path.dirname(sys.argv[3]) #"/inputdirectory_csfmask"
    ICH_mask_directory=os.path.dirname(sys.argv[4])
    #    print('sys.argv')
    print(sys.argv)
    SLICE_OUTPUT_DIRECTORY=sys.argv[6] #"/outputdirectory" #sys.argv[4] #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/NetWaterUptake/DATA/FU_CTs_Masks/CSF_RL_VOL_OUTPUT" #sys.argv[4] ####"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/MIDLINE/SOFTWARE/shellscript/RegistrationMethod/test"
    BET_OUTPUT_DIRECTORY=os.path.dirname(sys.argv[2])
    # BET_file_extension=sys.argv[9]
    # lower_thresh=0 #int(float(sys.argv[7])) #20 #0 # 20 #
    # upper_thresh=40 #int(float(sys.argv[8])) #80 # 40 # 80 #
    # lower_thresh_normal=20 #int(float(sys.argv[7]))
    # upper_thresh_normal=80 #int(float(sys.argv[8]))
    left_pixels_num=0
    right_pixels_num=0
    # print("ICH_mask_directory")
    # print(ICH_mask_directory)

    subject_name=os.path.basename(niftifilename).split(".nii")[0] #_gray")[0]
    count = 0
    dict_for_csv = []
    ICH_pixels_list=[]
    nonfarct_pixels_list=[]
    ICH_pixel_intensity=[]

    nonICH_pixel_intensity=[]
    # print("I AM HERE2")

    grayfilename_base=os.path.basename(niftifilename) #mask_basename+"levelset.nii.gz"

    grayfilename=niftifilename #os.path.join(levelset_file_directory,grayfilename) #os.path.join(niftifilenamedir,grayfilename)

    npyfileextension="REGISMethodOriginalRF_midline.npy"
    # print("I am here ICH_Mask_filename")

    ICH_Mask_filename=sys.argv[4] #ICH_Mask_filename_list[0] #os.path.join(niftifilenamedir,"Masks",mask_basename)
    csf_seg_maskbasename_path=sys.argv[3] #csf_seg_maskbasename_path_list[0] #os.path.join(niftifilenamedir,"Masks",csf_seg_maskbasename)
    ICH_Mask_filename_part1, ICH_Mask_filename_part2 = os.path.splitext(ICH_Mask_filename)

    ICH_side="NONE"

    if os.path.exists(csf_seg_maskbasename_path) and os.path.exists(ICH_Mask_filename) and os.path.exists(niftifilename):


        if 'hdr' in ICH_Mask_filename_part2:
            ICH_Mask_filename_data_np=resizeinto_512by512(nib.AnalyzeImage.from_filename(ICH_Mask_filename).get_fdata()) #nib.load(ICH_Mask_filename).get_fdata()
            niftifilename_data=nib.load(niftifilename).get_fdata()
            if niftifilename_data.shape[2] > ICH_Mask_filename_data_np.shape[2]:
                difference_slices=niftifilename_data.shape[2] - ICH_Mask_filename_data_np.shape[2]
                for slice_num in range(difference_slices):
                    ICH_Mask_filename_data_np[:,:,ICH_Mask_filename_data_np.shape[2]+slice_num]=ICH_Mask_filename_data_np[:,:,0]
        #             filename_gray_data_np_copy=np.copy(niftifilename_data)

        if 'gz' in ICH_Mask_filename_part2:
            ICH_Mask_filename_data_np=resizeinto_512by512(nib.load(ICH_Mask_filename).get_fdata()) #resizeinto_512by512(image_nib_nii_file_data)

            niftifilename_data=nib.load(niftifilename).get_fdata()
            if niftifilename_data.shape[2] > ICH_Mask_filename_data_np.shape[2]:
                difference_slices=niftifilename_data.shape[2] - ICH_Mask_filename_data_np.shape[2]
                for slice_num in range(difference_slices):
                    ICH_Mask_filename_data_np[:,:,ICH_Mask_filename_data_np.shape[2]+slice_num]=ICH_Mask_filename_data_np[:,:,0]

            #             filename_gray_data_np_copy=np.copy(niftifilename_data)

            ## volume of the ICH mask:
            ICH_total_voxels = ICH_Mask_filename_data_np[ICH_Mask_filename_data_np>np.min(ICH_Mask_filename_data_np)]
            ICH_total_voxels_count=ICH_total_voxels.shape[0]
            ICH_total_voxels_volume = ICH_total_voxels.shape[0]*np.prod(np.array(nib.load(niftifilename).header["pixdim"][1:4]))
            ICH_total_voxels_volume=ICH_total_voxels_volume/1000

        if len(ICH_Mask_filename_data_np.shape) == 4:
            ICH_Mask_filename_data_np=ICH_Mask_filename_data_np[:,:,:,0]

        filename_gray_data_np=resizeinto_512by512(nib.load(niftifilename).get_fdata()) #nib.load(niftifilename).get_fdata() #
        filename_gray_data_np_copy=np.copy(filename_gray_data_np)
        file_gray=niftifilename
        csf_seg_np=resizeinto_512by512(nib.load(csf_seg_maskbasename_path).get_fdata()) #nib.load(csf_seg_maskbasename_path).get_fdata() #
        min_val=np.min(csf_seg_np)
        filename_gray_data_np=contrast_stretch_np(filename_gray_data_np,1) #exposure.rescale_intensity( filename_gray_data_np , in_range=(1000, 1200))
        filename_gray_data_np_1=contrast_stretch_np(resizeinto_512by512(nib.load(grayfilename).get_fdata()),1)*255 #np.uint8(filename_gray_data_np*255) contrast_stretch_np(nib.load(grayfilename).get_fdata(),1)*255  #c
        # filename_gray_data_np[csf_seg_np>min_val]=np.min(filename_gray_data_np)#255
        numpy_image=normalizeimage0to1(filename_gray_data_np)*255 #filename_gray_data_np #

        print('filename_gray_data_np_copy size = {}'.format(filename_gray_data_np_copy.shape))
        print('csf_seg_np size = {}'.format(csf_seg_np.shape))

        # filename_gray_data_np_copy[csf_seg_np>min_val]=np.min(filename_gray_data_np_copy) #+10.0 #255
        ICH_side,ICH_Mask_filename_data_np=determine_ICH_side(numpy_image,filename_gray_data_np_copy,niftifilename,npyfiledirectory,csf_seg_np,ICH_Mask_filename_data_np)
        numpy_image_mask=ICH_Mask_filename_data_np
        lower_thresh=np.min(filename_gray_data_np_copy) #int(float(sys.argv[7])) #20 #0 # 20 #
        upper_thresh=np.max(filename_gray_data_np_copy) #int(float(sys.argv[8])) #80 # 40 # 80 #
        lower_thresh_normal=np.min(filename_gray_data_np_copy) #int(float(sys.argv[7]))
        upper_thresh_normal=np.max(filename_gray_data_np_copy) #int(float(sys.argv[8]))
        for img_idx in range(numpy_image.shape[2]):
            #             print("I AM HERE 4")
            if img_idx>0 and img_idx < numpy_image.shape[2] and  filename_gray_data_np_copy.shape==csf_seg_np.shape:
                method_name="REGIS"

                slice_number="{0:0=3d}".format(img_idx)
                filename_tosave=re.sub('[^a-zA-Z0-9 \n\_]', '', os.path.basename(niftifilename).split(".nii")[0])
                this_npyfile=os.path.join(npyfiledirectory,filename_tosave+method_name+str(slice_number)+  ".npy")

                #                this_npyfile=os.path.join(npyfiledirectory,os.path.basename(niftifilename).split(".nii")[0]+str(img_idx)+npyfileextension)
                if os.path.exists(this_npyfile):
                    calculated_midline_points=np.load(this_npyfile,allow_pickle=True)
                    x_points2=calculated_midline_points.item().get('x_axis') #,y_points2=points_on_line(extremepoints)
                    y_points2=calculated_midline_points.item().get('y_axis')
                    #                            slice_3_layer= np.zeros([numpy_image.shape[0],numpy_image.shape[1],3])
                    x_points2=x_points2[:,0]
                    y_points2=y_points2[:,0]

                    #################################################
                    ######################################################################
                    img_with_line_nonzero_id = np.transpose(np.nonzero(np.copy(numpy_image_mask[:,:,img_idx])))

                    lineThickness = 2
                    #                            lineThickness = 2
                    img_with_line=filename_gray_data_np_1[:,:,img_idx] #np.int8(numpy_image[:,:,img_idx])

                    # v1=np.array([512,0]) ## point from the image
                    # v2_1=np.array([x_points2[0],y_points2[0]]) ## point 1 from the midline
                    # v2_2=np.array([x_points2[1],y_points2[1]]) ## point 2 from the midline
                    # v2=v2_2-v2_1
                    #
                    # angle=  angle_bet_two_vector(v1,v2)
                    # angleRad=angle_bet_two_vectorRad(v1,v2)
                    # ## translation:
                    points1=np.array([[x_points2[0],y_points2[0]],[x_points2[511],y_points2[511]]])
                    # mid_point_line=np.mean(points,axis=0)
                    # # delta translation:
                    # image_midpoint=np.array([int(filename_gray_data_np_1[:,:,img_idx].shape[0]/2),int(filename_gray_data_np_1[:,:,img_idx].shape[1]/2)]) #np.array([255,255])
                    # translation_delta=image_midpoint-mid_point_line
                    # M = np.float32([[1,0,translation_delta[0]],[0,1,translation_delta[1]]])
                    # I_t_gray =cv2.warpAffine(np.copy(numpy_image[:,:,img_idx]),M,(filename_gray_data_np_1[:,:,img_idx].shape[0],filename_gray_data_np_1[:,:,img_idx].shape[1]), flags= cv2.INTER_NEAREST) # cv2.warpAffine(np.copy(numpy_image[:,:,img_idx]),M,(512,512), flags= cv2.INTER_NEAREST)
                    # I_t_mask =cv2.warpAffine(np.copy(numpy_image_mask[:,:,img_idx]),M,(filename_gray_data_np_1[:,:,img_idx].shape[0],filename_gray_data_np_1[:,:,img_idx].shape[1]) , flags= cv2.INTER_NEAREST) # cv2.warpAffine(np.copy(numpy_image_mask[:,:,img_idx]),M,(512,512) , flags= cv2.INTER_NEAREST)
                    #
                    # #########################################################################
                    #
                    #
                    # translate_points= points+translation_delta
                    # #                    show_slice_withaline(I_t_mask,translate_points)
                    # points=translate_points
                    # ## translation matrix
                    # p1x,p1y= rotate_around_point_highperf(np.array([points[0][0],points[0][1]]), angleRad, origin=(255,255))
                    # p2x,p2y= rotate_around_point_highperf(np.array([points[1][0],points[1][1]]), angleRad, origin=(255,255))
                    # points1=np.array([[p1x,p1y],[p2x,p2y]])
                    #
                    # I_t_r_gray=rotate_image(I_t_gray,(255,255),angle)
                    # #                    show_slice_withaline(I_t_r_gray,points1)
                    # I_t_r_mask=rotate_image(I_t_mask,(255,255),angle)
                    #
                    # I_t_r_f_gray=cv2.flip(I_t_r_gray,0)
                    # I_t_r_f_mask=cv2.flip(I_t_r_mask,0)
                    #
                    # I_t_r_f_rinv_gray=rotate_image(I_t_r_f_gray,(256,256),-angle)
                    # I_t_r_f_rinv_mask=rotate_image(I_t_r_f_mask,(256,256),-angle)
                    # p1x,p1y= rotate_around_point_highperf(np.array([points1[0][0],points1[0][1]]), -angleRad, origin=(255,255))
                    # p2x,p2y= rotate_around_point_highperf(np.array([points1[1][0],points1[1][1]]), -angleRad, origin=(255,255))
                    # points1=np.array([[p1x,p1y],[p2x,p2y]])
                    # #show_slice_withaline(I_t_r_f_rinv_gray,points1)
                    # #                    show_slice_withaline(I_t_r_f_rinv_mask,points1)
                    # M = np.float32([[1,0,-translation_delta[0]],[0,1,-translation_delta[1]]])
                    # I_t_r_f_rinv_tinv_gray = cv2.warpAffine(I_t_r_f_rinv_gray,M,(512,512) , flags= cv2.INTER_NEAREST)
                    # I_t_r_f_rinv_tinv_mask = numpy_image_mask[:,:,img_idx] #cv2.warpAffine(I_t_r_f_rinv_mask,M,(512,512), flags= cv2.INTER_NEAREST )
                    # points1=points1-translation_delta
                    # #show_slice_withaline(I_t_r_f_rinv_tinv_gray,points1)
                    # #                    show_slice_withaline(I_t_r_f_rinv_tinv_mask,points1)
                    I4=np.copy(numpy_image[:,:,img_idx])
                    # print("I4 size")
                    # print(I4.shape)
                    # print("I_t_r_f_rinv_tinv_mask")
                    # print(I_t_r_f_rinv_tinv_mask.shape)
                    # # I4[I_t_r_f_rinv_tinv_mask>0]=255
                    I4[np.copy(numpy_image_mask[:,:,img_idx])>0]=255
                    # I5=np.copy(filename_gray_data_np_copy[:,:,img_idx])
                    cv2.imwrite(os.path.join(niftifilenamedir,"I4_img" +grayfilename_base + "_1.jpg"),I4)
                    I4_img_1=cv2.imread(os.path.join(niftifilenamedir,"I4_img" +grayfilename_base + "_1.jpg"))
                    img_with_line1=cv2.line(I4_img_1, (int(points1[0][0]),int(points1[0][1])), (int(points1[1][0]),int(points1[1][1])), (0,255,0), lineThickness)
                    slice_number="{0:0=3d}".format(img_idx)
                    imagefilename=os.path.basename(niftifilename).split(".nii")[0].replace(".","_")+"_" +str(slice_number)
                    imagename=os.path.join(SLICE_OUTPUT_DIRECTORY,imagefilename +"_ICH.png")
                    imagename_class1=os.path.join(SLICE_OUTPUT_DIRECTORY,imagefilename +"_class1.png")
                    image_ICH_details=os.path.join(SLICE_OUTPUT_DIRECTORY,imagefilename +"_ICH_details.png")
                    image_ICH_nonICH_histogram=os.path.join(SLICE_OUTPUT_DIRECTORY,imagefilename +"_ICH_nonICH_histogram.png")
                    slice_3_layer1= np.zeros([filename_gray_data_np_copy[:,:,img_idx].shape[0],filename_gray_data_np_copy[:,:,img_idx].shape[1],3])
                    slice_3_layer1[:,:,0]= filename_gray_data_np_copy[:,:,img_idx] #imgray1
                    slice_3_layer1[:,:,0][np.copy(numpy_image_mask[:,:,img_idx])>0]=100
                    slice_3_layer1[:,:,1]= filename_gray_data_np_copy[:,:,img_idx] #imgray1
                    slice_3_layer1[:,:,1][np.copy(numpy_image_mask[:,:,img_idx])>0]=0
                    slice_3_layer1[:,:,2]= filename_gray_data_np_copy[:,:,img_idx]# imgray1
                    slice_3_layer1[:,:,2][np.copy(numpy_image_mask[:,:,img_idx])>0]=100
                    numpy_image_mask_flatten=numpy_image_mask[:,:,img_idx].flatten()
                    ICH_pixels_number=ICH_pixels_number+len(numpy_image_mask_flatten[np.nonzero(numpy_image_mask_flatten)]) #ICH_pixels.flatten()
                    cv2.imwrite(imagename,img_with_line1)
                    cv2.imwrite(imagename_class1,slice_3_layer1) #img_with_line1) ##slice_3_layer1) #
                    cv2.imwrite(image_ICH_details,img_with_line1)





    # lower_thresh=0
    # upper_thresh=0
    # lower_thresh_normal=0
    # upper_thresh_normal=0
    ICH_total_voxels_volume=ICH_pixels_number*np.prod(np.array(nib.load(niftifilename).header["pixdim"][1:4]))
    # ICH_side='AA'
    NWU=0
    # ICH_pixels_number=0
    # ICH_pixels_density=0
    nonfarct_pixels_number=0
    nonICH_pixels_density=0
    overall_ICH_vol=ICH_total_voxels_volume #0
    overall_non_ICH_vol=0

    return lower_thresh,upper_thresh,lower_thresh_normal,upper_thresh_normal, ICH_total_voxels_volume, ICH_side,NWU,ICH_pixels_number,ICH_pixels_density,nonfarct_pixels_number,nonICH_pixels_density, overall_ICH_vol,overall_non_ICH_vol



def measure_compartments_with_reg_round5_one_file_sh_v1() : #niftifilenamedir,npyfiledirectory,npyfileextension):
    # $grayimage $betimage  $csfmaskimage ${ICHmaskimage}  $npyfiledirectory     $output_directory  $lower_threshold $upper_threshold
    print(" I am in measure_compartments_with_reg_round5_one_file_sh_v1() ")
    print("code added on July 15 2022")
    niftifilename=sys.argv[1] ## THis is the  gray file:
    ICH_Class2_Mask_filename=sys.argv[7]
    ICH_Class1_Mask_filename=sys.argv[4]
    niftifilenamedir=os.path.dirname(niftifilename) #sys.argv[3] #"/inputdirectory" #sys.argv[1] #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/NetWaterUptake/DATA/FU_CTs_Masks/CTs" # "/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/CSF_Compartment/DATA/MISSINGDATA1/" #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/CSF_Compartment/DATA/NECT/ALLCOHORTINONE/TILTED"

    npyfiledirectory=sys.argv[5] #"/processedniftifiles" # "/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/NetWaterUptake/DATA/FU_CTs_Masks/SMOOTH_IML" # /media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/MIDLINE/RESULTS/RegistrationOnly/"


    print(sys.argv)
    SLICE_OUTPUT_DIRECTORY=sys.argv[6] #"/outputdirectory" #sys.argv[4] #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/NetWaterUptake/DATA/FU_CTs_Masks/CSF_RL_VOL_OUTPUT" #sys.argv[4] ####"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/MIDLINE/SOFTWARE/shellscript/RegistrationMethod/test"


    lower_thresh="NA" #int(float(sys.argv[7]))
    upper_thresh="NA" #int(float(sys.argv[8]))
    lower_thresh_normal="NA"
    upper_thresh_normal="NA"
    print(niftifilename)
    print("sys.argv[2]")
    print(sys.argv[2])
    ICH_side="NA"
    NWU="NA"
    ICH_pixels_number="NA"
    ICH_pixels_density="NA"
    nonfarct_pixels_number="NA"
    nonICH_pixels_density="NA"
    overall_ICH_vol="NA"
    overall_non_ICH_vol="NA"
    ICH_total_voxels_volume="NA"
    ICH_side="NONE"
    left_brain_volume=0
    right_brain_volume=0
    gray_image_data=nib.load(sys.argv[1]).get_fdata()
    bet_image_data=nib.load(sys.argv[2]).get_fdata()
    csf_image_data=nib.load(sys.argv[3]).get_fdata()
    ICH_Class2_Mask_filename_data=nib.load(ICH_Class2_Mask_filename).get_fdata()
    ICH_Class1_Mask_filename_data=nib.load(ICH_Class1_Mask_filename).get_fdata()
    # csf_image_data[ICH_Class2_Mask_filename_data>0]=np.min(csf_image_data)
    csf_image_data[ICH_Class2_Mask_filename_data>0]=np.min(csf_image_data)
    if gray_image_data.shape[0] == bet_image_data.shape[0] == csf_image_data.shape[0]  and gray_image_data.shape[1] == bet_image_data.shape[1] == csf_image_data.shape[1]  and  gray_image_data.shape[2] == bet_image_data.shape[2] == csf_image_data.shape[2]:

        if os.path.exists(sys.argv[4]):
            ICH_image_data=nib.load(sys.argv[4]).get_fdata()
            print(sys.argv[4])

            if  gray_image_data.shape[1]  ==  ICH_image_data.shape[1] and  gray_image_data.shape[0] == ICH_image_data.shape[0]    and gray_image_data.shape[2] == ICH_image_data.shape[2]:
                lower_thresh=-1024 #"NA" #int(float(sys.argv[7]))
                upper_thresh=1024 #int(float(sys.argv[8]))
                ## check if ICH file exists: sys.argv[4]
                lower_thresh,upper_thresh,lower_thresh_normal,upper_thresh_normal, ICH_total_voxels_volume,ICH_side,NWU,ICH_pixels_number,ICH_pixels_density,nonfarct_pixels_number,nonICH_pixels_density, overall_ICH_vol,overall_non_ICH_vol= measure_ICH_Class1_Feb24_2023()
                print("CLASS1::{}::{}::{}::{}::{}::{}::{}::{}::{}::{}::{}::{}::{}".format(lower_thresh,upper_thresh,lower_thresh_normal,upper_thresh_normal, ICH_total_voxels_volume,ICH_side,NWU,ICH_pixels_number,ICH_pixels_density,nonfarct_pixels_number,nonICH_pixels_density, overall_ICH_vol,overall_non_ICH_vol))
                lower_thresh_class2,upper_thresh_class2,lower_thresh_normal_class2,upper_thresh_normal_class2, ICH_total_voxels_volume_class2,ICH_side_class2,NWU_class2,ICH_pixels_number_class2,ICH_pixels_density_class2,nonfarct_pixels_number_class2,nonICH_pixels_density_class2, overall_ICH_vol_class2,overall_non_ICH_vol_class2= measure_ICH_CLASS2_Feb_24_2023()
                print("CLASS2::{}::{}::{}::{}::{}::{}::{}::{}::{}::{}::{}::{}::{}".format(lower_thresh_class2,upper_thresh_class2,lower_thresh_normal_class2,upper_thresh_normal_class2, ICH_total_voxels_volume_class2,ICH_side_class2,NWU_class2,ICH_pixels_number_class2,ICH_pixels_density_class2,nonfarct_pixels_number_class2,nonICH_pixels_density_class2, overall_ICH_vol_class2,overall_non_ICH_vol_class2))


        niftifilename_basename_split_nii=os.path.basename(niftifilename).split(".nii")[0] #.split("_")
        # bet_filename=niftifilename_basename_split_nii+BET_file_extension
        bet_filename_path=sys.argv[2] #os.path.join(BET_OUTPUT_DIRECTORY,bet_filename)
        # now=time.localtime()
        date_time = time.strftime("_%m_%d_%Y",now)
        grayfilename=niftifilename #os.path.join(niftifilenamedir,grayfilename)
        thisfilebasename=os.path.basename(grayfilename).split("_resaved")[0]
        # csvfile_with_vol_total=os.path.join(SLICE_OUTPUT_DIRECTORY,os.path.basename(grayfilename).split(".nii")[0] + "_threshold"+ str(lower_thresh) + "_" + str(upper_thresh) + "TOTAL.csv")
        csvfile_with_vol_total=os.path.join(SLICE_OUTPUT_DIRECTORY,thisfilebasename + "_threshold"+ str(lower_thresh) + "_" + str(upper_thresh) + "TOTAL" +Version_Date+date_time + ".csv")



        latexfilename=os.path.join(SLICE_OUTPUT_DIRECTORY,thisfilebasename+"_thresh_"+str(lower_thresh) + "_" +str(upper_thresh) + Version_Date + date_time+".tex")
        latexfilename1=os.path.join(os.path.dirname(latexfilename),'table.tex')
        # latexfilename=os.path.join(SLICE_OUTPUT_DIRECTORY,os.path.basename(grayfilename).split(".nii")[0]+"_thresh_"+str(lower_thresh) + "_" +str(upper_thresh) +".tex")


        latex_start(latexfilename)
        latex_begin_document(latexfilename)
        latex_insert_line_nodek(latexfilename,"\\input{"+latexfilename1+"}")
        # row = ["FileName_slice" , "LEFT CSF VOLUME", "RIGHT CSF VOLUME","TOTAL CSF VOLUME", "ICH SIDE","NWU", "ICH VOX_NUMBERS", "ICH DENSITY", "NON ICH VOX_NUMBERS", "NON ICH DENSITY","ICH VOLUME","ICH REFLECTION VOLUME", "BET VOLUME","CSF RATIO","LEFT BRAIN VOLUME without CSF" ,"RIGHT BRAIN VOLUME without CSF","ICH THRESH RANGE","NORMAL THRESH RANGE"]
        row = ["FileName_slice" , "LEFT CSF VOLUME", "RIGHT CSF VOLUME","TOTAL CSF VOLUME", "ICH SIDE","ICH VOLUME","ICH EDEMA VOLUME", "BET VOLUME","CSF RATIO","LEFT BRAIN VOLUME without CSF" ,"RIGHT BRAIN VOLUME without CSF"]

        col_names=np.copy(np.array(row))


        with open(csvfile_with_vol_total, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(row)

        npyfileextension="REGISMethodOriginalRF_midline.npy"

        CSF_Mask_filename=sys.argv[3] #os.path.join(csf_mask_directory,mask_basename)
        print('CSF_Mask_filename')
        print(CSF_Mask_filename)
        print('niftifilename')
        print(niftifilename)

        left_pixels_num=0
        right_pixels_num=0

        ICH_mask_basename_path=sys.argv[4] #ICH_mask_basename_path_list[0] #os.path.join(niftifilenamedir,"Masks",mask_basename)




        if os.path.exists(CSF_Mask_filename) and os.path.exists(niftifilename): # and os.path.exists(ICH_mask_basename_path) :
            print("BOTH FILE EXISTS")

            print('CSF_Mask_filename')
            print(CSF_Mask_filename)
            print('niftifilename')
            print(niftifilename)


            CSF_Mask_filename_data_minus_edema=nib.load(CSF_Mask_filename).get_fdata()
            # CSF_Mask_filename_data_minus_edema[ICH_Class2_Mask_filename_data>0]=np.min(CSF_Mask_filename_data_minus_edema)
            CSF_Mask_filename_data_minus_edema[ICH_Class2_Mask_filename_data>0]=np.min(CSF_Mask_filename_data_minus_edema)
            CSF_Mask_filename_data_np=resizeinto_512by512(CSF_Mask_filename_data_minus_edema) ##nib.load(CSF_Mask_filename).get_fdata()) #nib.load(CSF_Mask_filename).get_fdata() #
            CSF_Mask_filename_data_np[CSF_Mask_filename_data_np>1]=0

            ######################### added on July 15 2022 ##################################
            #             print("56code added on July 15 2022")
            if os.path.exists(sys.argv[4]):
                ICH_image_data_1=resizeinto_512by512(nib.load(sys.argv[4]).get_fdata())
                #                 print('np.max(ICH_image_data_1):{}'.format(np.max(ICH_image_data_1)))
                print('Filename:{}'.format(os.path.basename(niftifilename)))
                print('Number of voxels in CSF mask before ICH subtraction:{}'.format(len(CSF_Mask_filename_data_np[CSF_Mask_filename_data_np>0])))

                CSF_Mask_filename_data_np[ICH_image_data_1>0]=0
                print("code for subtraction:{}".format('CSF_Mask_data[ICH_data>0]=0'))

                print('Number of voxels in CSF mask after ICH subtraction:{}'.format(len(CSF_Mask_filename_data_np[CSF_Mask_filename_data_np>0])))
            #                 print("58code added on July 15 2022")
            ##################################################################################

            #                print(np.max(CSF_Mask_filename_data_np))
            filename_gray_data_np=resizeinto_512by512(nib.load(niftifilename).get_fdata()) #nib.load(niftifilename).get_fdata() #
            filename_bet_gray_data_np=contrast_stretch_np(resizeinto_512by512(nib.load(bet_filename_path).get_fdata()),1) #contrast_stretch_np(nib.load(bet_filename_path).get_fdata(),1) #
            filename_gray_data_np=contrast_stretch_np(filename_gray_data_np,1) #exposure.rescale_intensity( filename_gray_data_np , in_range=(1000, 1200))
            filename_gray_data_np_1=contrast_stretch_np(resizeinto_512by512(nib.load(grayfilename).get_fdata()),1)*255  #contrast_stretch_np(nib.load(grayfilename).get_fdata(),1)*255 ##np.uint8(filename_gray_data_np*255)
            numpy_image=filename_gray_data_np #normalizeimage0to1(filename_gray_data_np)*255
            filename_brain_data_np_minus_CSF=np.copy(filename_bet_gray_data_np)*255
            #             filename_brain_data_np_minus_CSF[filename_bet_gray_data_np<np.max(filename_bet_gray_data_np)]=np.min(filename_brain_data_np_minus_CSF)
            filename_brain_data_np_minus_CSF[CSF_Mask_filename_data_np>=np.max(CSF_Mask_filename_data_np)]=np.min(filename_brain_data_np_minus_CSF)
            upper_slice_num=0
            lower_slice_num=0
            found_lower_slice=0
            for slice_num_csf in range(CSF_Mask_filename_data_np.shape[2]):

                if found_lower_slice==0 and np.sum(CSF_Mask_filename_data_np[:,:,slice_num_csf]) >0:
                    lower_slice_num=slice_num_csf
                    found_lower_slice=1
                if found_lower_slice==1 and np.sum(CSF_Mask_filename_data_np[:,:,slice_num_csf]) >0 :
                    upper_slice_num=slice_num_csf
            this_slice_left_volume=0
            this_slice_right_volume=0
            for img_idx in range(numpy_image.shape[2]):
                if img_idx>0 and img_idx < numpy_image.shape[2]:

                    method_name="REGIS"
                    slice_number="{0:0=3d}".format(img_idx)
                    filename_tosave=re.sub('[^a-zA-Z0-9 \n\_]', '', os.path.basename(niftifilename).split(".nii")[0])
                    this_npyfile=os.path.join(npyfiledirectory,filename_tosave+method_name+str(slice_number)+  ".npy")
                    #                        this_npyfile=os.path.join(npyfiledirectory,os.path.basename(niftifilename).split(".nii")[0]+str(img_idx)+npyfileextension)
                    #                        print(this_npyfile)
                    if os.path.exists(this_npyfile):
                        print("YES FOUND BOTH FILES")
                        print('latexfilename')
                        print(latexfilename)
                        calculated_midline_points=np.load(this_npyfile,allow_pickle=True)
                        x_points2=calculated_midline_points.item().get('x_axis') #,y_points2=points_on_line(extremepoints)
                        # print(x_points2)
                        y_points2=calculated_midline_points.item().get('y_axis')
                        slice_3_layer= np.zeros([numpy_image.shape[0],numpy_image.shape[1],3])
                        x_points2=x_points2[:,0]
                        y_points2=y_points2[:,0]
                        # print(this_npyfile)

                        img_with_line=CSF_Mask_filename_data_np[:,:,img_idx]
                        # print(np.max(img_with_line))
                        img_with_line_nonzero_id = np.transpose(np.nonzero(img_with_line))
                        thisimage=filename_gray_data_np_1[:,:,img_idx]
                        current_left_num=0
                        current_right_num=0
                        slice_3_layer= np.zeros([img_with_line.shape[0],img_with_line.shape[1],3])
                        slice_3_layer[:,:,0]= thisimage #imgray1
                        slice_3_layer[:,:,1]= thisimage #imgray1
                        slice_3_layer[:,:,2]= thisimage# imgray1


                        slice_3_layer_brain= np.zeros([img_with_line.shape[0],img_with_line.shape[1],3])
                        slice_3_layer_brain[:,:,0]= filename_brain_data_np_minus_CSF[:,:,img_idx] #imgray1
                        slice_3_layer_brain[:,:,1]= filename_brain_data_np_minus_CSF[:,:,img_idx] #imgray1
                        slice_3_layer_brain[:,:,2]= filename_brain_data_np_minus_CSF[:,:,img_idx] # imgray1
                        # font
                        font = cv2.FONT_HERSHEY_SIMPLEX

                        # org
                        org = (50, 50)

                        # fontScale
                        fontScale = 1

                        # Blue color in BGR
                        color = (0, 0, 255)

                        # Line thickness of 2 px
                        thickness = 2

                        imagefilename_gray=os.path.basename(niftifilename).split(".nii")[0].replace(".","_")+"_" +str(slice_number)+"gray"
                        slice_3_layer = cv2.putText(slice_3_layer,str(slice_number) , org, font,  fontScale, color, thickness, cv2.LINE_AA)
                        #                         slice_3_layer_brain = cv2.putText(slice_3_layer,str(slice_number) , org, font,  fontScale, color, thickness, cv2.LINE_AA)
                        cv2.imwrite(os.path.join(SLICE_OUTPUT_DIRECTORY,imagefilename_gray +".png"),slice_3_layer)
                        for non_zero_pixel in img_with_line_nonzero_id:
                            xx=whichsideofline((int(y_points2[511]),int(x_points2[511])),(int(y_points2[0]),int(x_points2[0])) ,non_zero_pixel)
                            if xx>0: ## RIGHT
                                slice_3_layer[non_zero_pixel[0],non_zero_pixel[1],0]=0
                                slice_3_layer[non_zero_pixel[0],non_zero_pixel[1],1]=255
                                slice_3_layer[non_zero_pixel[0],non_zero_pixel[1],2]=0
                                current_right_num = current_right_num + 1
                            if xx<0: ## LEFT
                                slice_3_layer[non_zero_pixel[0],non_zero_pixel[1],0]=0
                                slice_3_layer[non_zero_pixel[0],non_zero_pixel[1],1]=0
                                slice_3_layer[non_zero_pixel[0],non_zero_pixel[1],2]=255
                                current_left_num = current_left_num + 1
                        brainarea_with_nonzero_id = np.transpose(np.nonzero(filename_brain_data_np_minus_CSF[:,:,img_idx]))

                        left_brain_voxel_count=0
                        right_brain_voxel_count=0
                        for non_zero_pixel in brainarea_with_nonzero_id:
                            xx=whichsideofline((int(y_points2[511]),int(x_points2[511])),(int(y_points2[0]),int(x_points2[0])) ,non_zero_pixel)
                            if xx>0: ## RIGHT
                                slice_3_layer_brain[non_zero_pixel[0],non_zero_pixel[1],0]=0
                                slice_3_layer_brain[non_zero_pixel[0],non_zero_pixel[1],1]=255
                                slice_3_layer_brain[non_zero_pixel[0],non_zero_pixel[1],2]=0
                                right_brain_voxel_count = right_brain_voxel_count + 1
                            if xx<0: ## LEFT
                                slice_3_layer_brain[non_zero_pixel[0],non_zero_pixel[1],0]=0
                                slice_3_layer_brain[non_zero_pixel[0],non_zero_pixel[1],1]=0
                                slice_3_layer_brain[non_zero_pixel[0],non_zero_pixel[1],2]=255
                                left_brain_voxel_count = left_brain_voxel_count + 1


                        lineThickness = 2

                        this_slice_left_volume = current_left_num*np.prod(np.array(nib.load(niftifilename).header["pixdim"][1:4]))
                        this_slice_right_volume = current_right_num*np.prod(np.array(nib.load(niftifilename).header["pixdim"][1:4]))

                        this_slice_gray_left_volume = left_brain_voxel_count*np.prod(np.array(nib.load(niftifilename).header["pixdim"][1:4]))
                        this_slice_gray_right_volume = right_brain_voxel_count*np.prod(np.array(nib.load(niftifilename).header["pixdim"][1:4]))
                        this_slice_gray_left_volume=this_slice_gray_left_volume/1000
                        this_slice_gray_right_volume=this_slice_gray_right_volume/1000

                        img_with_line1=cv2.line(slice_3_layer, ( int(x_points2[0]),int(y_points2[0])),(int(x_points2[511]),int(y_points2[511])), (0,255,0), 2)

                        img_hemibrain_line1=cv2.line(slice_3_layer_brain, ( int(x_points2[0]),int(y_points2[0])),(int(x_points2[511]),int(y_points2[511])), (0,255,0), 2)
                        slice_number="{0:0=3d}".format(img_idx)


                        imagefilename=os.path.basename(niftifilename).split(".nii")[0].replace(".","_")+"_" +str(slice_number)

                        imagefilename_ICH=os.path.join(SLICE_OUTPUT_DIRECTORY,imagefilename +"_ICH.png")
                        imagename_class2=os.path.join(SLICE_OUTPUT_DIRECTORY,imagefilename +"_class2.png")
                        imagename_class1=os.path.join(SLICE_OUTPUT_DIRECTORY,imagefilename +"_class1.png")
                        image_ICH_details=os.path.join(SLICE_OUTPUT_DIRECTORY,imagefilename +"_ICH_details.png")
                        image_ICH_nonICH_histogram=os.path.join(SLICE_OUTPUT_DIRECTORY,imagefilename +"_ICH_nonICH_histogram.png")
                        image_left_right_brain=os.path.join(SLICE_OUTPUT_DIRECTORY,imagefilename +"_left_right_brain.png")


                        cv2.imwrite(os.path.join(SLICE_OUTPUT_DIRECTORY,imagefilename +".png"),img_with_line1)
                        cv2.imwrite(image_left_right_brain,slice_3_layer_brain)
                        nect_file_basename_forimagename=imagefilename

                        ## get the mask image:
                        this_slice_left_volume=this_slice_left_volume/1000
                        this_slice_right_volume=this_slice_right_volume/1000

                        ################################
                        # upper_slice_num=0
                        # lower_slice_num=0
                        # found_lower_slice=0
                        # for slice_num_csf in range(CSF_Mask_filename_data_np.shape[2]):

                        #     if found_lower_slice==0 and np.sum(CSF_Mask_filename_data_np[:,:,slice_num_csf]) >0:
                        #         lower_slice_num=slice_num_csf
                        #         found_lower_slice=1
                        #     if found_lower_slice==1 and np.sum(CSF_Mask_filename_data_np[:,:,slice_num_csf]) >0 :
                        #         upper_slice_num=slice_num_csf
                        ##########################

                        image_list=[]
                        print("lower_slice_num:{} and upper_slice_num:{}".format(lower_slice_num,upper_slice_num))
                        if os.path.exists(sys.argv[4])  and int(slice_number) >=int(lower_slice_num) and int(slice_number)<=int(upper_slice_num) :
                            latex_start_tableNc_noboundary(latexfilename,6)

                            image_list.append(os.path.join(SLICE_OUTPUT_DIRECTORY,imagefilename_gray +".png"))
                            image_list.append(image_left_right_brain)
                            # image_list.append(imagefilename_ICH)
                            image_list.append(imagename_class1)
                            image_list.append(imagename_class2)

                            # image_list.append(os.path.join(SLICE_OUTPUT_DIRECTORY,image_ICH_details))
                            image_list.append(os.path.join(SLICE_OUTPUT_DIRECTORY,imagefilename +".png"))
                            latex_insertimage_tableNc(latexfilename,image_list,len(image_list), caption="",imagescale=.2, angle=90,space=0.51)
                            latex_end_table2c(latexfilename)

                        elif int(slice_number) >=int(lower_slice_num) and int(slice_number)<=int(upper_slice_num) :
                            latex_start_tableNc_noboundary(latexfilename,2)

                            image_list.append(os.path.join(SLICE_OUTPUT_DIRECTORY,imagefilename_gray +".png"))
                            # image_list.append(imagefilename_ICH)
                            # image_list.append(os.path.join(SLICE_OUTPUT_DIRECTORY,image_ICH_details))
                            image_list.append(os.path.join(SLICE_OUTPUT_DIRECTORY,imagefilename +".png"))
                            latex_insertimage_tableNc(latexfilename,image_list,2, caption="",imagescale=0.2, angle=90,space=0.51)

                            latex_end_table2c(latexfilename)

                        left_pixels_num=left_pixels_num+this_slice_left_volume
                        right_pixels_num=right_pixels_num+this_slice_right_volume

                        left_brain_volume=left_brain_volume + this_slice_gray_left_volume
                        right_brain_volume=right_brain_volume + this_slice_gray_right_volume
            image_array=np.asarray(filename_bet_gray_data_np)
            print("image_array MINIMUM")
            print(np.min(image_array))
            BET_VOLUME = (image_array > 0).sum()*np.prod(np.array(nib.load(niftifilename).header["pixdim"][1:4])) / 1000
            CSF_RATIO=left_pixels_num/right_pixels_num
            if left_pixels_num > right_pixels_num :
                CSF_RATIO=right_pixels_num/left_pixels_num
                # thisfilebasename=os.path.basename(grayfilename).split("_levelset")[0]
            # row2 = [os.path.basename(niftifilename).split(".nii")[0] , str(left_pixels_num), str(right_pixels_num),str(left_pixels_num+right_pixels_num), ICH_side,NWU, ICH_pixels_number, ICH_pixels_density, nonfarct_pixels_number,nonICH_pixels_density,overall_ICH_vol,overall_non_ICH_vol,str(BET_VOLUME),str(CSF_RATIO),str(left_brain_volume),str(right_brain_volume),str(lower_thresh)+"to"+ str(upper_thresh),str(lower_thresh_normal) +"to" +str(upper_thresh_normal)]
            # row2 = [thisfilebasename , str(left_pixels_num), str(right_pixels_num),str(left_pixels_num+right_pixels_num), ICH_side,NWU, ICH_pixels_number, ICH_pixels_density, nonfarct_pixels_number,nonICH_pixels_density,overall_ICH_vol,overall_non_ICH_vol,str(BET_VOLUME),str(CSF_RATIO),str(left_brain_volume),str(right_brain_volume),str(lower_thresh)+"to"+ str(upper_thresh),str(lower_thresh_normal) +"to" +str(upper_thresh_normal)]
            # row2_1 = [thisfilebasename , str(left_pixels_num), str(right_pixels_num),str(left_pixels_num+right_pixels_num), ICH_side,NWU, ICH_pixels_number_class2, ICH_pixels_density_class2, nonfarct_pixels_number_class2,nonICH_pixels_density_class2,overall_ICH_vol_class2,overall_non_ICH_vol_class2,str(BET_VOLUME),str(CSF_RATIO),str(left_brain_volume),str(right_brain_volume),str(lower_thresh)+"to"+ str(upper_thresh),str(lower_thresh_normal) +"to" +str(upper_thresh_normal)]
            row2 = [thisfilebasename ,str(left_pixels_num), str(right_pixels_num),str(left_pixels_num+right_pixels_num), ICH_side,overall_ICH_vol,overall_ICH_vol_class2, str(BET_VOLUME),str(CSF_RATIO),str(left_brain_volume),str(right_brain_volume)]
            values_in_col=np.array(row2)

            # values_in_col_1=np.array(row2_1)

            with open(csvfile_with_vol_total, 'a') as f1:
                writer = csv.writer(f1)
                writer.writerow(row2)
                # writer.writerow(row2_1)
            this_nii_filename_list=[]
            # this_nii_filename_list.append(os.path.basename(niftifilename).split(".nii")[0]) #thisfilebasename
            this_nii_filename_list.append(thisfilebasename)
            this_nii_filename_df=pd.DataFrame(this_nii_filename_list)
            this_nii_filename_df.columns=['FILENAME']

            latex_start_tableNc_noboundary(latexfilename1,1)
            latex_insert_line_nodek(latexfilename1,text=this_nii_filename_df.to_latex(index=False))
            latex_end_table2c(latexfilename1)

            #             latex_insert_line_nodek(latexfilename,"\\newpage")
            #             latex_insert_line_nodate(latexfilename,"\\texttt{\\detokenize{" + os.path.basename(niftifilename).split(".nii")[0] + "}}")

            values_in_table=[]

            #             text1=[]
            #             text1.append(" Regions ")
            #             text1.append("Volume  (ml)")
            #             latex_start_tableNc(latexfilename,2)
            #             latex_inserttext_tableNc(latexfilename,text1,2,space=-1.4)

            for x in range(0,col_names.shape[0]):
                #                 text1=[]
                values_in_table.append([(str(col_names[x])).replace("_"," "),(str(values_in_col[x])).replace("_","")])
            # for x in range(0,col_names.shape[0]):
            # #                 text1=[]
            #     values_in_table.append([(str(col_names[x])).replace("_"," "),(str(values_in_col[x])).replace("_","")])
            #                 text1.append((str(col_names[x])).replace("_"," "))
            #                 text1.append((str(values_in_col[x])).replace("_",""))

            #                 latex_inserttext_tableNc(latexfilename,text1,2,space=-1.4)
            #             latex_end_table2c(latexfilename)
            values_in_table.pop(0)
            # values_in_table.pop(10)
            # values_in_table.pop(14)
            # values_in_table.pop(14)
            # for a in range(5):
            #     values_in_table.pop(4)
            # # for a in range(5):

            values_in_table_df=pd.DataFrame(values_in_table)
            values_in_table_df.columns=[" Regions ","Volume  (ml)"]
            latex_start_tableNc_noboundary(latexfilename1,1)
            # values_in_table_df=values_in_table_df.drop([4, 5,6,7,8,10,15,16])
            print("values_in_table_df::{}".format(values_in_table_df))
            values_in_table_df=values_in_table_df.reindex([3,4,5,2,1,0,7,6,8,9])
            print("values_in_table_df_rearranged::{}".format(values_in_table_df))
            latex_insert_line_nodek(latexfilename1,text=values_in_table_df.to_latex(index=False))
            latex_end_table2c(latexfilename1)
        latex_end(latexfilename)
        # remove_few_columns(csvfile_with_vol_total,["ICH VOX_NUMBERS", "ICH DENSITY", "NON ICH VOX_NUMBERS"])


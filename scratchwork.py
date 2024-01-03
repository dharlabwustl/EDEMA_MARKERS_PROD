def nwucalc_N_images(subject_name,):
    print("current_infarct_num")
    print(current_infarct_num)
    print("filename_gray_data_np_copy[non_zero_pixel[0],non_zero_pixel[1],img_idx]")
    print(filename_gray_data_np_copy[non_zero_pixel[0],non_zero_pixel[1],img_idx])
    text_space=15
    blank_3_layer = cv2.putText(blank_3_layer, "INFARCT SIDE (Orange):  " + infarct_side  + "  Slice number:" +str(slice_number) , org, font,  fontScale, color, thickness, cv2.LINE_AA)

    blank_3_layer = cv2.putText(blank_3_layer, "   "  , org, font,  fontScale, color, thickness, cv2.LINE_AA)
    #                            if infarct_pixel_counter != 0 :
    if infarct_pixel_counter != 0 :
        blank_3_layer = cv2.putText(blank_3_layer, "Infarct density:" + str(current_infarct_num/infarct_pixel_counter) , (org[0],org[1]+ 50 +text_space), font,  fontScale, color, thickness, cv2.LINE_AA)
    else:
        blank_3_layer = cv2.putText(blank_3_layer, "Infarct density:" + "Infarct count=0", (org[0],org[1]+ 50 +text_space), font,  fontScale, color, thickness, cv2.LINE_AA)


    blank_3_layer = cv2.putText(blank_3_layer, "   "  , (org[0],org[1]+ 50 +text_space*2), font,  fontScale, color, thickness, cv2.LINE_AA)
    if noninfarct_pixel_counter != 0 :
        blank_3_layer = cv2.putText(blank_3_layer,  "Non infarct density:" + str(current_noninfarct_num/noninfarct_pixel_counter) , (org[0],org[1]+ 50+text_space*3), font,  fontScale, color, thickness, cv2.LINE_AA)
    else:
        blank_3_layer = cv2.putText(blank_3_layer,  "Non infarct density:" + "Non infarct count=0" , (org[0],org[1]+ 50+text_space*3), font,  fontScale, color, thickness, cv2.LINE_AA)

    blank_3_layer = cv2.putText(blank_3_layer, "   "  , (org[0],org[1]+ 50 +text_space*4), font,  fontScale, color, thickness, cv2.LINE_AA)
    blank_3_layer = cv2.putText(blank_3_layer, "Infarct pixel count:" + str(infarct_pixel_counter) , (org[0],org[1]+ 50+text_space*5), font,  fontScale, color, thickness, cv2.LINE_AA)
    blank_3_layer = cv2.putText(blank_3_layer, "   "  , (org[0],org[1]+ 50 +text_space*6), font,  fontScale, color, thickness, cv2.LINE_AA)

    blank_3_layer = cv2.putText(blank_3_layer,  "Non infarct pixel count:" + str(noninfarct_pixel_counter) , (org[0],org[1]+ 50+text_space*7), font,  fontScale, color, thickness, cv2.LINE_AA)
    blank_3_layer = cv2.putText(blank_3_layer, "   "  , (org[0],org[1]+ 50 +text_space*8), font,  fontScale, color, thickness, cv2.LINE_AA)
    blank_3_layer = cv2.putText(blank_3_layer, "Total pixel infarct:" + str(pixels_num_total_infarct) , (org[0],org[1]+ 50+text_space*9), font,  fontScale, color, thickness, cv2.LINE_AA)
    blank_3_layer = cv2.putText(blank_3_layer, "   "  , (org[0],org[1]+ 50 +text_space*10), font,  fontScale, color, thickness, cv2.LINE_AA)
    blank_3_layer = cv2.putText(blank_3_layer,  "Total pixel non-infarct:" + str(pixels_num_total_noninfarct) , (org[0],org[1]+ 50+text_space*11), font,  fontScale, color, thickness, cv2.LINE_AA)
    blank_3_layer = cv2.putText(blank_3_layer, "   "  , (org[0],org[1]+ 50 +text_space*12), font,  fontScale, color, thickness, cv2.LINE_AA)
    blank_3_layer = cv2.putText(blank_3_layer, "Pixels lower than lower thresh in infarct:" + str(pixels_num_infarct_below_lowerthresh) , (org[0],org[1]+ 50+text_space*13), font,  fontScale, color, thickness, cv2.LINE_AA)
    blank_3_layer = cv2.putText(blank_3_layer, "   "  , (org[0],org[1]+ 50 +text_space*14), font,  fontScale, color, thickness, cv2.LINE_AA)
    blank_3_layer = cv2.putText(blank_3_layer,  "Pixels higher than upper thresh in infarct:" + str(pixels_num_infarct_above_upperthresh) , (org[0],org[1]+ 50+text_space*text_space), font,  fontScale, color, thickness, cv2.LINE_AA)
    blank_3_layer = cv2.putText(blank_3_layer, "   "  , (org[0],org[1]+ 50 +text_space*16), font,  fontScale, color, thickness, cv2.LINE_AA)
    blank_3_layer = cv2.putText(blank_3_layer, "Pixels lower than lower thresh in noninfarct:" + str(pixels_num_noninfarct_below_lowerthresh) , (org[0],org[1]+ 50+text_space*17), font,  fontScale, color, thickness, cv2.LINE_AA)
    blank_3_layer = cv2.putText(blank_3_layer, "   "  , (org[0],org[1]+ 50 +text_space*18), font,  fontScale, color, thickness, cv2.LINE_AA)
    blank_3_layer = cv2.putText(blank_3_layer,  "Pixels higher than upper thresh in noninfarct:" + str(pixels_num_noninfarct_above_upperthresh) , (org[0],org[1]+ 50+text_space*19), font,  fontScale, color, thickness, cv2.LINE_AA)

    blank_3_layer = cv2.putText(blank_3_layer, "   "  , (org[0],org[1]+ 50 +text_space*20), font,  fontScale, color, thickness, cv2.LINE_AA)
    blank_3_layer = cv2.putText(blank_3_layer, "CSF Pixels in infarct:" + str(csf_in_infarct) , (org[0],org[1]+ 50+text_space*21), font,  fontScale, color, thickness, cv2.LINE_AA)
    blank_3_layer = cv2.putText(blank_3_layer, "   "  , (org[0],org[1]+ 50 +text_space*22), font,  fontScale, color, thickness, cv2.LINE_AA)
    blank_3_layer = cv2.putText(blank_3_layer,  "CSF Pixels  in non-infarct:" + str(csf_in_noinfarct) , (org[0],org[1]+ 50+text_space*23), font,  fontScale, color, thickness, cv2.LINE_AA)



    img_with_line1=cv2.line(slice_3_layer, (int(points1[0][0]),int(points1[0][1])), (int(points1[1][0]),int(points1[1][1])), (0,255,0), lineThickness)


    cv2.imwrite(imagename,img_with_line1)
    cv2.imwrite(image_infarct_details,rotate_image(blank_3_layer,center1=[255,255],angle=-90))

    histogram_sidebyside(infarct_pixels_gt20_lt80_nonzero,noninfarct_pixels_gt20_lt80_nonzero,image_infarct_noninfarct_histogram)

    ratio_density=(np.mean(infarct_pixels_gt20_lt80_nonzero)/np.mean(noninfarct_pixels_gt20_lt80_nonzero))
    NWU_slice=(1-ratio_density) * 100  #(1- ((np.mean(infarct_pixels_gt20_lt80))/(np.mean(non_infarct_pixels_gt20_lt80)))) * 100
    this_dict={"Slice":subject_name.split('_resaved')[0]+"_" +str(img_idx),"NWU":NWU_slice,"NumberofInfarctvoxels": infarct_slice_pixel_count, "INFARCT Density":np.mean(infarct_pixels_gt20_lt80_nonzero),"NumberofNONInfarctvoxels": noninfarct_slice_pixel_count , "NONINFARCT Density":np.mean(noninfarct_pixels_gt20_lt80_nonzero) , "INFARCT Volume":infarct_pixels_volume/1000 ,"NONINFARCT Volume":non_infarct_pixels_volume/1000, "ORGINAL_INFARCT_VOLUME":"NA","INFARCTUSED_VOL_RATIO":"NA","NONINFACRTUSED_VOL_RATIO":"NA" } #,"Ventricles_Vol":ventricle_vol,"Sulci_VolL":leftcountsul,"Sulci_VolR":rightcountsul,"Ventricles_VolL":leftcountven,"Ventricles_VolR":rightcountven,"sulci_vol_above_vent": sulci_vol_above_vent,"sulci_vol_below_vent" :sulci_vol_below_vent,"sulci_vol_at_vent":sulci_vol_at_vent}
    return this_dict

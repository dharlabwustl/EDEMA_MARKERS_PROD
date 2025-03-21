############ DOWNLOAD WARPED MRI MASKS ###############
import sys,os
# sys.path.append('/media/atul/WDJan20222/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD')
from download_with_session_ID import *
from utilities_simple_trimmed import *
from mri_masks_on_session_ct_with_infarct_templatectisfixed11112024 import *
import pandas as pd
from natsort import natsorted
import  time,os,glob,subprocess
import nibabel as nib
import pandas as pd
import numpy as np
from pytablewriter import LatexTableWriter
import inspect,subprocess,sys
XNAT_USER='atulkumar'
XNAT_PASS='Mrityor1!'
XNAT_HOST='https://snipr.wustl.edu'
# SESSION_ID='SNIPR01_E00193' ## #'${1} #str(each_row['ID'])
import linecache

def trace_lines(frame, event, arg):
    if event == "line":
        filename = frame.f_code.co_filename  # Get the file name of the current line
        project_root = "./"  # Set this to your project's root directory

        # Only trace lines in your project files
        if filename.startswith(project_root):
            lineno = frame.f_lineno  # Get the current line number
            code_line = linecache.getline(filename, lineno).strip()  # Read the line from the file
            print(f"Executing Line {lineno} in {filename}: {code_line}")
    return trace_lines
sys.settrace(trace_lines)
def lobar_region_volumes_n_display(SESSION_ID):


    software_dir='software'
    region_mask_type='lobar'
    working='maskonly'
    mri_mask_dir=working #'maskonly' #'www_nitrc_org_frs/maskonly'
    file_output_dir='workinginput'
    SLICE_OUTPUT_DIRECTORY='workingoutput'
    output_directory='workingoutput'
    splitter='_fixed'
    output_dir=output_directory
    # return
    SCAN_ID,SCAN_NAME=get_selected_scan_info(SESSION_ID,file_output_dir)
    print(f'{SCAN_ID}::{SCAN_NAME}')
    # return

    working_dir_1='input'
    Version_Date="_VersionDate-" + '11122024' #dt.strftime("%m%d%Y")
    # DOWNLOAD THE REGISTERED INFARCT MASK and the REGISTERED SESSION CT
    download_an_xmlfile_with_URIString_func(SESSION_ID,f'{SESSION_ID}.xml',working_dir_1)
    # print('ATUL')
    # return
    resource_dir='MASKLABEL'
    subprocess.call("echo " + "I FAILED  AT ::{}  >> workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
    # downloadfiletolocaldir_py('SNIPR02_E14665',"MRI1",resource_dir,working_dir_1) #SNIPR01_E07218
    downloadfile_withasuffix('SNIPR02_E14665',"MRI1",working_dir_1,resource_dir,'.nii')
    downloadfile_withasuffix('SNIPR02_E14665',"MRI1",working_dir_1,resource_dir,'.csv')
    subprocess.call("echo " + "I PASSED  AT ::{}  >> workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
    #
    # return
    resource_dir='PREPROCESS_SEGM_1'
    # downloadfiletolocaldir_py('SNIPR02_E14665',"MRI1",resource_dir,mri_mask_dir)
    downloadfile_withasuffix('SNIPR02_E14665',"MRI1",mri_mask_dir,resource_dir,'COLIHM620406202215542')
    resource_dir='PREPROCESS_SEGM'
    downloadfile_withasuffix(SESSION_ID,SCAN_ID,working_dir_1,resource_dir,'COLIHM620406202215542')
    downloadfile_withasuffix(SESSION_ID,SCAN_ID,working_dir_1,resource_dir,'warped_moving_image')
    downloadfile_withasuffix(SESSION_ID,SCAN_ID,working_dir_1,resource_dir,'fixed_image')
    # downloadfiletolocaldir_py(SESSION_ID,SCAN_ID,resource_dir,working_dir_1)
    resource_dir='MASKS'
    downloadfile_withasuffix(SESSION_ID,SCAN_ID,working_dir_1,resource_dir,'.nii')
    # downloadfiletolocaldir_py(SESSION_ID,SCAN_ID,resource_dir,working_dir_1)
    resource_dir='NIFTI'
    downloadfile_withasuffix(SESSION_ID,SCAN_ID,working_dir_1,resource_dir,'.nii')
    # downloadfiletolocaldir_py(SESSION_ID,SCAN_ID,resource_dir,working_dir_1)
    directory_of_files_after_deepreg=working_dir_1
    # return
    file_without_ext=SCAN_NAME.split('.nii')[0] ##os.path.basename(session_ct_path).split('.nii')[0]
    predefined_legend=os.path.join(working_dir_1,'legend.csv') # '/software/legend.csv'
    command='mv ' + os.path.join(mri_mask_dir,'*brain.bfc'+splitter+'*.nii.gz') + '  ' + output_dir
    subprocess.call(command,shell=True)
    #
    #  ## '/software/www_nitrc_org_frs/maskonly'
    mask_img_paths=glob.glob(os.path.join(mri_mask_dir,'warped_1*_fixed_COLIHM620406202215542_lin1_BET.nii.gz')) #glob.glob(os.path.join(mri_mask_dir,'warped_1*BET.nii.gz'))  #glob.glob(os.path.join(mri_mask_dir,'*.nii.gz'))
    grayscale_img_path=os.path.join(directory_of_files_after_deepreg,'warped_moving_image.nii.gz')
    min_intensity,max_intensity=get_min_max_intensity(grayscale_img_path)
    # print(mask_img_paths)
    gray_img=nib.load(grayscale_img_path).get_fdata()
    infarct_mask_from_yasheng=os.path.join(working_dir_1,file_without_ext + '_resaved_infarct_auto_removesmall.nii.gz')
    original_gray_filename=os.path.join(working_dir_1,SCAN_NAME)
    # gray_img[gray_img<=np.min(gray_img)]
    # Intensity levels
    # min_intensity=np.min(gray_img[gray_img>10]) #np.min(gray_img)]) #20
    # max_intensity=np.max(gray_img[gray_img>np.min(gray_img)]) #60
    template_nifti_file='software/COLIHM620406202215542.nii.gz' ##scct_strippedResampled1.nii.gz'
    template_nifti_file_base_noext=os.path.basename(template_nifti_file).split('.nii')[0]
    # Find infarct mask
    # scct_strippedResampled1='scct_strippedResampled1'
    infarct_mask_pattern=f'warped_mov_{file_without_ext}_resaved_infarct_auto_removesmall_fixed_{template_nifti_file_base_noext}_lin1_BET.nii.gz'
    infarct_mask_list=glob.glob(os.path.join(directory_of_files_after_deepreg,infarct_mask_pattern)) ##f'warped_1_mov_{file_without_ext}*_resaved_infarct_auto_removesmallresampled_mov_fixed_{template_nifti_file_base_noext}_lin1.nii.gz'))
    print(infarct_mask_list)


    infarct_mask_filename=infarct_mask_list[0]
    print(infarct_mask_filename)
    post_process_smooothing_closing(infarct_mask_filename,binary_threshold=0.6,smooth_sigma=2.0)
    #################


    project_name,subject_name, session_label,acquisition_site_xml,acquisition_datetime_xml,scanner_from_xml,body_part_xml,kvp_xml=get_info_from_xml(os.path.join(working_dir_1,f'{SESSION_ID}.xml'))
    print(f"{project_name}::{subject_name}::{session_label}::{acquisition_site_xml}::{acquisition_datetime_xml}::{scanner_from_xml}::{body_part_xml}::{kvp_xml}")
    # return
    # df['session_name']
    # print("ATUL")
    # return
    # variables=[project_name,subject_name, session_label,acquisition_site_xml,acquisition_datetime_xml,scanner_from_xml,body_part_xml,kvp_xml]
    # globals_copy = globals().copy()
    # # variable_dict = {name: globals_copy()[name] for name in globals_copy() if globals_copy()[name] in variables}
    # variable_dict = {name: globals_copy[name] for name in variables if name in globals_copy}
    # df1 = pd.DataFrame([variable_dict])
    variables=[project_name,subject_name, session_label,acquisition_site_xml,acquisition_datetime_xml,scanner_from_xml,body_part_xml,kvp_xml]
    print(variables)
    # globals_copy = globals().copy()
    # variable_dict = {name: globals_copy()[name] for name in globals_copy() if globals_copy()[name] in variables}
    # variable_dict = {name: globals_copy[name] for name in variables if name in globals_copy}
    variable_dict={"project_name":project_name,"subject_name":subject_name, "session_label":session_label,"acquisition_site_xml":acquisition_site_xml,"acquisition_datetime_xml":acquisition_datetime_xml,"scanner_from_xml":scanner_from_xml,"body_part_xml":body_part_xml,"kvp_xml":kvp_xml}
    import pandas as pd
    df1 = pd.DataFrame([variable_dict])

    ## session_name, session_id,scan_name, volumes region wise, volume total, normal volume of region.
    df1['session_id']=SESSION_ID
    df1['scan_id']=SCAN_ID
    df1['scan_name']=SCAN_NAME
    df1['session_label']=session_label

    ## create arterial region columns with 0 value:
    mask_num_list = natsorted([
        os.path.basename(mask_img_path).split(splitter)[0].split('_')[-1]
        for mask_img_path in mask_img_paths
    ])
    new_columns = {f"{region_mask_type}_region{num}": 0 for num in mask_num_list}
    df1 = df1.assign(**new_columns)
    print(df1)
    # # from utilities_simple_trimmed import * ;
    levelset2originalRF_new_flip_with_params(original_gray_filename,infarct_mask_from_yasheng,output_dir) #"${original_ct_file}" "${levelset_bet_mask_file}" "${output_directory}"
    infarct_mask_in_ORF=os.path.join(output_dir,os.path.basename(infarct_mask_from_yasheng))
    infarct_volume_before_reg=measure_mask_volume(infarct_mask_in_ORF,original_gray_filename) ##([infarct_mask_filename],infarct_mask_filename,template_nifti_file,region_mask_type)
    ##
    infarct_volume_after_reg=measure_mask_volume(infarct_mask_filename,template_nifti_file) ##([infarct_mask_filename],infarct_mask_filename,template_nifti_file,region_mask_type)
    df1['infarct_volume_before_reg']=infarct_volume_before_reg
    bet_mask_from_yasheng=os.path.join(working_dir_1,file_without_ext + '_resaved_levelset_bet.nii.gz')
    # original_gray_filename=os.path.join(working_dir_1,SCAN_NAME)
    original_gray_filename_nib=nib.load(original_gray_filename)
    bet_mask_from_yasheng_nib=nib.load(bet_mask_from_yasheng)
    bet_mask_from_yasheng_nib_data=bet_mask_from_yasheng_nib.get_fdata()
    bet_mask_from_yasheng_nib_data[bet_mask_from_yasheng_nib_data<=np.min(bet_mask_from_yasheng_nib_data)]=0
    bet_mask_from_yasheng_nib_data[bet_mask_from_yasheng_nib_data>0]=1
    bet_mask_from_yasheng_nib_data_volume=(np.sum(bet_mask_from_yasheng_nib_data)*np.product(original_gray_filename_nib.header["pixdim"][1:4]))/1000
    df1['brain_volume_before_reg']=bet_mask_from_yasheng_nib_data_volume
    df1['infarct_fraction_before_reg']=infarct_volume_before_reg/bet_mask_from_yasheng_nib_data_volume
    df1['infarct_volume_after_reg']=infarct_volume_after_reg
    template_nifti_file_nib=nib.load(template_nifti_file)
    template_nifti_file_nib_data=template_nifti_file_nib.get_fdata()
    template_nifti_file_nib_data[template_nifti_file_nib_data<=np.min(template_nifti_file_nib_data)]=0
    template_nifti_file_nib_data[template_nifti_file_nib_data>0]=1
    template_nifti_file_nib_data_volume=(np.sum(template_nifti_file_nib_data)*np.product(template_nifti_file_nib.header["pixdim"][1:4]))/1000
    # df1['infarct_fraction_after_reg']=infarct_volume_after_reg/template_nifti_file_nib_data_volume
    moving_file_after_reg=os.path.join('input','warped_moving_image.nii.gz') ##f'warped_mov_{file_without_ext}_brain_f_fixed_{template_nifti_file_base_noext}_lin1_brain_f.nii.gz')
    moving_file_after_reg_nib=nib.load(moving_file_after_reg)
    moving_file_after_reg_nib_data=moving_file_after_reg_nib.get_fdata()
    moving_file_after_reg_nib_data[moving_file_after_reg_nib_data>0]=1
    moving_file_after_reg_nib_data[moving_file_after_reg_nib_data<1]=0
    moving_file_after_reg_nib_data_volume=(np.sum(moving_file_after_reg_nib_data)*np.product(template_nifti_file_nib.header["pixdim"][1:4]))/1000
    df1['brain_volume_after_reg']=moving_file_after_reg_nib_data_volume
    df1['infarct_fraction_after_reg']=infarct_volume_after_reg/moving_file_after_reg_nib_data_volume #template_nifti_file_nib_data_volume
    df1['template_brain_volume']=template_nifti_file_nib_data_volume
    print('{}::{}::{}::{}'.format(mask_img_paths,infarct_mask_filename,template_nifti_file,region_mask_type))
    df2=volumes_regions_overlapping_infarct_on_ct(mask_img_paths,infarct_mask_filename,template_nifti_file,region_mask_type,infarct_volume_after_reg,infarct_volume_before_reg=infarct_volume_before_reg,splitter=splitter)
    # df2.to_csv('test_territory.csv',index=False)
    # result = pd.concat([df1, df2], axis=1)
    # result.update(df2)
    df1.update(df2)
    # Find new columns in df1 that are not in df2
    # new_columns = df2.columns.difference(df1.columns)

    # Add only new columns from df1 to df2
    # df1 = pd.concat([df1, df2], axis=1)
    # df1=df1.drop('lobar_regionbrain.bfc', axis=1)
    # print(df1)

    #

    now=time.localtime()
    date_time = time.strftime("_%m_%d_%Y",now)
    thisfilebasename=file_without_ext
    latexfilename=os.path.join(SLICE_OUTPUT_DIRECTORY,thisfilebasename +region_mask_type+ Version_Date + date_time+".tex")
    csvfilename=os.path.join(SLICE_OUTPUT_DIRECTORY,thisfilebasename + region_mask_type+Version_Date + date_time+".csv")
    df1.to_csv(csvfilename,index=False)
    # df2.to_csv(csvfilename.split('.csv')[0]+'_territory.csv',index=False)

    start_column="session_id"
    df_for_pdf = df1.loc[:, start_column:]
    df_for_pdf['session_label']=session_label
    column_to_front = 'session_label'
    cols = [column_to_front] + [col for col in df_for_pdf.columns if col != column_to_front]
    print("cols")
    print(cols)
    df_for_pdf = df_for_pdf[cols]
    print("df_for_pdf")
    print(df_for_pdf)
    df_for_pdf = df_for_pdf.T.reset_index()
    print("df_for_pdf")
    print(df_for_pdf)
    df_for_pdf.columns = ['Column_Name', 'Value']
    df_for_pdf['Regions']=''
    df_for_pdf['legendcolor']=''

    regions_csv=pd.read_csv(os.path.join(working_dir_1,'brainsuite_labeldescription.csv'))
    legend_df=pd.read_csv(os.path.join(working_dir_1,'legend.csv'))
    ## get mask numbers:

    masknumberslist = [os.path.basename(x).split(splitter)[0].split('_')[-1]
                       for x in mask_img_paths
                       if splitter in os.path.basename(x)]
    masknumberslist_df=pd.DataFrame(masknumberslist)
    n = len(masknumberslist) #legend_df.shape[0] #(df)
    masknumberslist_df.columns=['masknumber']
    masknumberslist_df["color"] = generate_contrasting_colors(n)
    masknumberslist_df['filename']=mask_img_paths
    print(masknumberslist_df)
    # legend_df['legend'] = legend_df['color'].apply(color_box)
    # legend_df['color_image_file']=''
    masknumberslist_df['color_image_file']=''
    single_color_image('filler',"(0,0,0)",output_dir,image_height=512,image_width=512)

    for color_id,color_row in masknumberslist_df.iterrows():
        masknumberslist_df.at[color_id, 'color_image_file'] =single_color_image(color_row['masknumber'],color_row['color'],output_dir,image_height=100,image_width=200)
    for each_id,each_item in df_for_pdf.iterrows():
        each_item_region_with_num=str(each_item['Column_Name'])
        if 'lobar_region' in each_item_region_with_num:
            region_num=int(each_item_region_with_num.split('lobar_region')[1])
            print(f"region_num::{region_num}")
            try:
                print("I AM GOING TO TRY")
                territory_value = regions_csv[regions_csv['masknumber'].astype(str) == str(region_num)]['region'].values[0]
                territory_color = masknumberslist_df[masknumberslist_df['masknumber'].astype(str) == str(region_num)]['color_image_file'].values[0]
                legend_df.loc[legend_df['masknumber'].astype(str) == str(region_num), 'color'] = masknumberslist_df[masknumberslist_df['masknumber'].astype(str) == str(region_num)]['color'].values[0]
                print(f'territory_color::{territory_color}')
                print('success::')
                print(each_item['Column_Name'])
                print("I HAVE TRIED THE TRY")
            except:
                territory_value=''
                territory_color=''
                print('failure:')
                print(each_item['Column_Name'])
                pass
            # Assign the value using .loc for safer assignment
            df_for_pdf.loc[each_id, 'Regions'] = territory_value
            df_for_pdf.loc[each_id, 'legendcolor'] = territory_color
    # column_to_insert=df_for_pdf['session_label']
    # df_for_pdf.insert(0, 'session_label', column_to_insert)
    print(df_for_pdf)
    df_for_pdf[ 'legendcolor']=df_for_pdf[ 'legendcolor'].apply(lambda filename: f"\\includegraphics[scale=0.2]{{{os.path.basename(filename)}}}" if pd.notna(filename) and filename else "")
    legend_df.to_csv(os.path.join(working_dir_1,'legend.csv'),index=False)
    # ###############################
    print(f'{grayscale_img_path}, {min_intensity},{max_intensity},{infarct_mask_filename},{output_dir},{predefined_legend}') #,{mask_img_paths}')
    ## graysice with regional infarct mask
    image_prefix='regional_infarct'
    superimpose_regions_overlapping_infarct_on_ct(grayscale_img_path,mask_img_paths,infarct_mask_filename,output_dir,predefined_legend,image_prefix)

    image_prefix='regions'
    superimpose_regions_overlapping_infarct_on_ct(grayscale_img_path,mask_img_paths,grayscale_img_path,output_dir,predefined_legend,image_prefix)

    saveslicesofnifti_withgiventhresh_inmri(grayscale_img_path,500,700,savetodir=output_dir)
    image_prefix='infarct_only'
    # superimpose_singlemask_on_gray_ct(grayscale_img_path, infarct_mask_filename, output_dir, (0,0,250), image_prefix)
    superimpose_singlemask_on_gray_ct_threshgiven(grayscale_img_path, infarct_mask_filename, output_dir, (0,0,250), image_prefix,[500,700])
    image_prefix='original_ct_with_infarct_only'
    superimpose_singlemask_on_gray_ct_original(original_gray_filename, infarct_mask_in_ORF, output_dir, (0,0,250), image_prefix,[20,60])

    # latexfilename=create_a_latex_filename(filename_prefix,filename_to_write)
    latex_start(latexfilename)
    latex_begin_document(latexfilename)

    # latex_start_table1c(latexfilename)
    # latex_code = df_for_pdf.to_latex(index=False, escape=False)
    # Convert DataFrame to pytablewriter-compatible format
    # Helper function to escape LaTeX special characters
    import pandas as pd

    # Example DataFrame
######################################
    # Create the "territory" column in transpose_df and fill it with appropriate values from territory_df
    # This assumes matching logic is based on the "Column_Name" in transpose_df and corresponding columns in territory_df

    # Initialize the "territory" column with NaN
    df_for_pdf['territory'] = None

    # Iterate over each row in transpose_df
    for index, row in df_for_pdf.iterrows():
        column_name = row['Column_Name']
        # Check if a corresponding territory column exists in territory_df
        territory_column = f"{column_name}_territory"
        if territory_column in df2.columns:
            # Assign the value from territory_df to the new 'territory' column in transpose_df
            df_for_pdf.at[index, 'territory'] = df2[territory_column].iloc[0]

    # Save the updated dataframe to inspect it
    # transpose_df.to_csv('/mnt/data/Updated_Transpose.csv', index=False)

    # import ace_tools as tools; tools.display_dataframe_to_user(name="Updated Transpose DataFrame", dataframe=transpose_df)


#################################################
    # Generate LaTeX table
    for col in df_for_pdf.columns:
        df_for_pdf[col] = round_mixed_column(df_for_pdf[col])    
    df_for_pdf.to_csv(csvfilename.split('.csv')[0]+'_Transpose.csv',index=False)
    latex_table = df_to_latex_1(df_for_pdf)

    # # Save to a .tex file
    # with open("basic_latex_table.tex", "w") as file:
    #     file.write(latex_table)
    #
    # print("LaTeX table saved as 'basic_latex_table.tex'")

    # latex_table=latex_table.replace(r'_',r'\_')
    # Replace only the escaped LaTeX commands
    # latex_code  = (latex_code
    #                            .replace(r'\textbackslash textcolor', r'\textcolor')
    #                            .replace(r'\textbackslash rule', r'\rule')
    #                            .replace(r'\{', '{')
    #                            .replace(r'\}', '}')
    #                            .replace(r'\textbackslash includegraphics',r'\includegraphics'))

    latex_insert_line_nodek(latexfilename,text=latex_table)
    # latex_end_table2c(latexfilename)
    command="echo " + "start" + " > error.txt"
    subprocess.call(command,shell=True)

    for slice_num in range(nib.load(grayscale_img_path).get_fdata().shape[2]):
        image_list=[]
        latex_start_tableNc_noboundary(latexfilename,5)
        image_list.append(os.path.join('warped_moving_image_'+"{:03}".format(slice_num)+'.jpg'))
        image_list.append(os.path.join('regions_'+"{:03}".format(slice_num)+'.png'))
        image_list.append(os.path.join('regional_infarct_'+"{:03}".format(slice_num)+'.png'))
        image_list.append(os.path.join('infarct_only_'+"{:03}".format(slice_num)+'.png'))
        print(os.path.join('levelset_ct_with_infarct_only_'+"{:03}".format(slice_num)+'.png'))
        command="echo " + os.path.join('original_ct_with_infarct_only_'+"{:03}".format(slice_num)+'.png') + " >> error.txt"
        subprocess.call(command,shell=True)
        if os.path.exists(os.path.join(output_dir,'original_ct_with_infarct_only_'+"{:03}".format(slice_num)+'.png')):
            image_list.append(os.path.join('original_ct_with_infarct_only_'+"{:03}".format(slice_num)+'.png'))
        else:
            image_list.append(os.path.join('color_filler.png'))

        latex_insertimage_tableNc(latexfilename,image_list,5, caption="",imagescale=0.15, angle=90,space=0.51)
        latex_end_table2c(latexfilename)

    latex_end(latexfilename)
    command = f"sed -i 's/color\\\\_/color_/g' {latexfilename}"
    subprocess.call(command, shell=True)    #subprocess.call(command,shell=True)
    os.chdir('workingoutput')
    print(glob.glob("./*"))
    command="pdflatex *.tex  " #+ 'lobar_output/'
    subprocess.call(command,shell=True)
    command="mv *.csv   " + '../lobar_output/'
    subprocess.call(command,shell=True)
    command="mv *.pdf   " + '../lobar_output/'
    subprocess.call(command,shell=True)
    os.chdir('../')

def lobar_regions_heatmap_volumes_n_display(heatmap_nifti_file):


    software_dir='software'
    region_mask_type='lobar'
    working='maskonly'
    mri_mask_dir=working #'maskonly' #'www_nitrc_org_frs/maskonly'
    file_output_dir='workinginput'
    SLICE_OUTPUT_DIRECTORY='workingoutput'
    output_directory='workingoutput'
    splitter='_fixed'
    output_dir=output_directory
    # return
    # SCAN_ID,SCAN_NAME=get_selected_scan_info(SESSION_ID,file_output_dir)
    # print(f'{SCAN_ID}::{SCAN_NAME}')
    # return

    working_dir_1='input'
    Version_Date="_VersionDate-" + '11122024' #dt.strftime("%m%d%Y")
    # DOWNLOAD THE REGISTERED INFARCT MASK and the REGISTERED SESSION CT
    # download_an_xmlfile_with_URIString_func(SESSION_ID,f'{SESSION_ID}.xml',working_dir_1)
    # print('ATUL')
    # return
    resource_dir='MASKLABEL'
    subprocess.call("echo " + "I FAILED  AT ::{}  >> workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
    # downloadfiletolocaldir_py('SNIPR02_E14665',"MRI1",resource_dir,working_dir_1) #SNIPR01_E07218
    downloadfile_withasuffix('SNIPR02_E14665',"MRI1",working_dir_1,resource_dir,'.nii')
    downloadfile_withasuffix('SNIPR02_E14665',"MRI1",working_dir_1,resource_dir,'.csv')
    subprocess.call("echo " + "I PASSED  AT ::{}  >> workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
    #
    # return
    resource_dir='PREPROCESS_SEGM_1'
    # downloadfiletolocaldir_py('SNIPR02_E14665',"MRI1",resource_dir,mri_mask_dir)
    downloadfile_withasuffix('SNIPR02_E14665',"MRI1",mri_mask_dir,resource_dir,'COLIHM620406202215542')
    resource_dir='PREPROCESS_SEGM'
    # downloadfile_withasuffix(SESSION_ID,SCAN_ID,working_dir_1,resource_dir,'COLIHM620406202215542')
    # downloadfile_withasuffix(SESSION_ID,SCAN_ID,working_dir_1,resource_dir,'warped_moving_image')
    # downloadfile_withasuffix(SESSION_ID,SCAN_ID,working_dir_1,resource_dir,'fixed_image')
    # # downloadfiletolocaldir_py(SESSION_ID,SCAN_ID,resource_dir,working_dir_1)
    # resource_dir='MASKS'
    # downloadfile_withasuffix(SESSION_ID,SCAN_ID,working_dir_1,resource_dir,'.nii')
    # # downloadfiletolocaldir_py(SESSION_ID,SCAN_ID,resource_dir,working_dir_1)
    # resource_dir='NIFTI'
    # downloadfile_withasuffix(SESSION_ID,SCAN_ID,working_dir_1,resource_dir,'.nii')
    # downloadfiletolocaldir_py(SESSION_ID,SCAN_ID,resource_dir,working_dir_1)
    directory_of_files_after_deepreg=working_dir_1
    # return
    grayscale_img_path=template_nifti_file='software/COLIHM620406202215542.nii.gz' ##os.path.join(directory_of_files_after_deepreg,'warped_moving_image.nii.gz')
    SCAN_NAME=os.path.basename(grayscale_img_path)
    file_without_ext=SCAN_NAME.split('.nii')[0] ##os.path.basename(session_ct_path).split('.nii')[0]
    predefined_legend=os.path.join(working_dir_1,'legend.csv') # '/software/legend.csv'
    command='mv ' + os.path.join(mri_mask_dir,'*brain.bfc'+splitter+'*.nii.gz') + '  ' + output_dir
    subprocess.call(command,shell=True)
    #
    #  ## '/software/www_nitrc_org_frs/maskonly'
    mask_img_paths=glob.glob(os.path.join(mri_mask_dir,'warped_1*_fixed_COLIHM620406202215542_lin1_BET.nii.gz')) #glob.glob(os.path.join(mri_mask_dir,'warped_1*BET.nii.gz'))  #glob.glob(os.path.join(mri_mask_dir,'*.nii.gz'))

    min_intensity,max_intensity=get_min_max_intensity(grayscale_img_path)
    # print(mask_img_paths)
    gray_img=nib.load(grayscale_img_path).get_fdata()
    # infarct_mask_from_yasheng=os.path.join(working_dir_1,file_without_ext + '_resaved_infarct_auto_removesmall.nii.gz')
    original_gray_filename=grayscale_img_path #=os.path.join(directory_of_files_after_deepreg,'warped_moving_image.nii.gz')#os.path.join(working_dir_1,SCAN_NAME)
    # gray_img[gray_img<=np.min(gray_img)]
    # Intensity levels
    # min_intensity=np.min(gray_img[gray_img>10]) #np.min(gray_img)]) #20
    # max_intensity=np.max(gray_img[gray_img>np.min(gray_img)]) #60
     ##scct_strippedResampled1.nii.gz'
    template_nifti_file_base_noext=os.path.basename(template_nifti_file).split('.nii')[0]
    # Find infarct mask
    # scct_strippedResampled1='scct_strippedResampled1'
    # infarct_mask_pattern=f'warped_1_mov_{file_without_ext}_resaved_infarct_auto_removesmall_fixed_{template_nifti_file_base_noext}_lin1_BET.nii.gz'
    # infarct_mask_list=[heatmap_nifti_file] #glob.glob(os.path.join(directory_of_files_after_deepreg,infarct_mask_pattern)) ##f'warped_1_mov_{file_without_ext}*_resaved_infarct_auto_removesmallresampled_mov_fixed_{template_nifti_file_base_noext}_lin1.nii.gz'))
    # print(infarct_mask_list)


    infarct_mask_filename=heatmap_nifti_file #infarct_mask_list[0]


    #################


    # project_name,subject_name, session_label,acquisition_site_xml,acquisition_datetime_xml,scanner_from_xml,body_part_xml,kvp_xml=get_info_from_xml(os.path.join(working_dir_1,f'{SESSION_ID}.xml'))
    # print(f"{project_name}::{subject_name}::{session_label}::{acquisition_site_xml}::{acquisition_datetime_xml}::{scanner_from_xml}::{body_part_xml}::{kvp_xml}")
    # return
    # df['session_name']
    # print("ATUL")
    # return
    # variables=[project_name,subject_name, session_label,acquisition_site_xml,acquisition_datetime_xml,scanner_from_xml,body_part_xml,kvp_xml]
    # globals_copy = globals().copy()
    # # variable_dict = {name: globals_copy()[name] for name in globals_copy() if globals_copy()[name] in variables}
    # variable_dict = {name: globals_copy[name] for name in variables if name in globals_copy}
    # df1 = pd.DataFrame([variable_dict])
    project_name='INFARCT'
    variables=[project_name] ##,subject_name, session_label,acquisition_site_xml,acquisition_datetime_xml,scanner_from_xml,body_part_xml,kvp_xml]
    print(variables)
    # globals_copy = globals().copy()
    # variable_dict = {name: globals_copy()[name] for name in globals_copy() if globals_copy()[name] in variables}
    # variable_dict = {name: globals_copy[name] for name in variables if name in globals_copy}
    variable_dict={"project_name":project_name} ##,"subject_name":subject_name, "session_label":session_label,"acquisition_site_xml":acquisition_site_xml,"acquisition_datetime_xml":acquisition_datetime_xml,"scanner_from_xml":scanner_from_xml,"body_part_xml":body_part_xml,"kvp_xml":kvp_xml}
    import pandas as pd
    df1 = pd.DataFrame([variable_dict])

    ## session_name, session_id,scan_name, volumes region wise, volume total, normal volume of region.
    # df1['session_id']=SESSION_ID
    # df1['scan_id']=SCAN_ID
    # df1['scan_name']=SCAN_NAME
    # df1['session_label']=session_label

    ## create arterial region columns with 0 value:
    mask_num_list = natsorted([
        os.path.basename(mask_img_path).split(splitter)[0].split('_')[-1]
        for mask_img_path in mask_img_paths
    ])
    new_columns = {f"{region_mask_type}_region{num}": 0 for num in mask_num_list}
    df1 = df1.assign(**new_columns)
    print(df1)
    
    # # # from utilities_simple_trimmed import * ;
    # levelset2originalRF_new_flip_with_params(original_gray_filename,infarct_mask_from_yasheng,output_dir) #"${original_ct_file}" "${levelset_bet_mask_file}" "${output_directory}"
    # infarct_mask_in_ORF=os.path.join(output_dir,os.path.basename(infarct_mask_from_yasheng))
    # infarct_volume_before_reg=measure_mask_volume(infarct_mask_in_ORF,original_gray_filename) ##([infarct_mask_filename],infarct_mask_filename,template_nifti_file,region_mask_type)
    ##
    infarct_volume_after_reg=measure_mask_volume(infarct_mask_filename,template_nifti_file) ##([infarct_mask_filename],infarct_mask_filename,template_nifti_file,region_mask_type)
    # df1['infarct_volume_before_reg']=infarct_volume_before_reg
    # df1['infarct_volume_after_reg']=infarct_volume_after_reg

    print('{}::{}::{}::{}'.format(mask_img_paths,infarct_mask_filename,template_nifti_file,region_mask_type))
    df2=volumes_regions_overlapping_infarct_on_ct(mask_img_paths,infarct_mask_filename,template_nifti_file,region_mask_type,infarct_volume_after_reg,infarct_volume_before_reg=100,splitter=splitter)
    df2.to_csv('test_territory.csv',index=False)
    df1.update(df2)
    # df1=df1.drop('lobar_regionbrain.bfc', axis=1)
    # print(df1)

    #

    now=time.localtime()
    date_time = time.strftime("_%m_%d_%Y",now)
    thisfilebasename=file_without_ext
    latexfilename=os.path.join(SLICE_OUTPUT_DIRECTORY,thisfilebasename + region_mask_type+ Version_Date + date_time+".tex")
    csvfilename=os.path.join(SLICE_OUTPUT_DIRECTORY,thisfilebasename + region_mask_type+Version_Date + date_time+".csv")
    df1.to_csv(csvfilename,index=False)

    # start_column="session_id"
    df_for_pdf = df1 #.loc[:, start_column:]
    # df_for_pdf['session_label']=session_label
    # column_to_front = 'session_label'
    # cols = [column_to_front] + [col for col in df_for_pdf.columns if col != column_to_front]
    # print("cols")
    # print(cols)
    # df_for_pdf = df_for_pdf[cols]
    # print("df_for_pdf")
    # print(df_for_pdf)
    df_for_pdf = df_for_pdf.T.reset_index()
    print("df_for_pdf")
    print(df_for_pdf)
    df_for_pdf.columns = ['Column_Name', 'Value']
    df_for_pdf['Regions']=''
    df_for_pdf['legendcolor']=''

    regions_csv=pd.read_csv(os.path.join(working_dir_1,'brainsuite_labeldescription.csv'))
    legend_df=pd.read_csv(os.path.join(working_dir_1,'legend.csv'))
    ## get mask numbers:

    masknumberslist = [os.path.basename(x).split(splitter)[0].split('_')[-1]
                       for x in mask_img_paths
                       if splitter in os.path.basename(x)]
    masknumberslist_df=pd.DataFrame(masknumberslist)
    n = len(masknumberslist) #legend_df.shape[0] #(df)
    masknumberslist_df.columns=['masknumber']
    masknumberslist_df["color"] = generate_contrasting_colors(n)
    masknumberslist_df['filename']=mask_img_paths
    print(masknumberslist_df)
    # legend_df['legend'] = legend_df['color'].apply(color_box)
    # legend_df['color_image_file']=''
    masknumberslist_df['color_image_file']=''
    single_color_image('filler',"(0,0,0)",output_dir,image_height=512,image_width=512)

    for color_id,color_row in masknumberslist_df.iterrows():
        masknumberslist_df.at[color_id, 'color_image_file'] =single_color_image(color_row['masknumber'],color_row['color'],output_dir,image_height=100,image_width=200)
    for each_id,each_item in df_for_pdf.iterrows():
        each_item_region_with_num=str(each_item['Column_Name'])
        if 'lobar_region' in each_item_region_with_num:
            region_num=int(each_item_region_with_num.split('lobar_region')[1])
            print(f"region_num::{region_num}")
            try:
                print("I AM GOING TO TRY")
                territory_value = regions_csv[regions_csv['masknumber'].astype(str) == str(region_num)]['region'].values[0]
                territory_color = masknumberslist_df[masknumberslist_df['masknumber'].astype(str) == str(region_num)]['color_image_file'].values[0]
                legend_df.loc[legend_df['masknumber'].astype(str) == str(region_num), 'color'] = masknumberslist_df[masknumberslist_df['masknumber'].astype(str) == str(region_num)]['color'].values[0]
                print(f'territory_color::{territory_color}')
                print('success::')
                print(each_item['Column_Name'])
                print("I HAVE TRIED THE TRY")
            except:
                territory_value=''
                territory_color=''
                print('failure:')
                print(each_item['Column_Name'])
                pass
            # Assign the value using .loc for safer assignment
            df_for_pdf.loc[each_id, 'Regions'] = territory_value
            df_for_pdf.loc[each_id, 'legendcolor'] = territory_color
    # column_to_insert=df_for_pdf['session_label']
    # df_for_pdf.insert(0, 'session_label', column_to_insert)
    print(df_for_pdf)
    df_for_pdf[ 'legendcolor']=df_for_pdf[ 'legendcolor'].apply(lambda filename: f"\\includegraphics[scale=0.2]{{{os.path.basename(filename)}}}" if pd.notna(filename) and filename else "")
    legend_df.to_csv(os.path.join(working_dir_1,'legend.csv'),index=False)
    # ###############################
    print(f'{grayscale_img_path}, {min_intensity},{max_intensity},{infarct_mask_filename},{output_dir},{predefined_legend}') #,{mask_img_paths}')
    ## graysice with regional infarct mask
    image_prefix='regional_infarct'
    superimpose_regions_overlapping_infarct_on_ct(grayscale_img_path,mask_img_paths,infarct_mask_filename,output_dir,predefined_legend,image_prefix)

    image_prefix='regions'
    superimpose_regions_overlapping_infarct_on_ct(grayscale_img_path,mask_img_paths,grayscale_img_path,output_dir,predefined_legend,image_prefix)

    saveslicesofnifti_withgiventhresh_inmri(grayscale_img_path,500,700,savetodir=output_dir)
    image_prefix='infarct_only'
    # superimpose_singlemask_on_gray_ct(grayscale_img_path, infarct_mask_filename, output_dir, (0,0,250), image_prefix)
    superimpose_singlemask_on_gray_ct_threshgiven(grayscale_img_path, infarct_mask_filename, output_dir, (0,0,250), image_prefix,[500,700])
    # image_prefix='original_ct_with_infarct_only'
    # superimpose_singlemask_on_gray_ct_original(original_gray_filename, infarct_mask_in_ORF, output_dir, (0,0,250), image_prefix,[20,60])

    # latexfilename=create_a_latex_filename(filename_prefix,filename_to_write)
    latex_start(latexfilename)
    latex_begin_document(latexfilename)

    # latex_start_table1c(latexfilename)
    # latex_code = df_for_pdf.to_latex(index=False, escape=False)
    # Convert DataFrame to pytablewriter-compatible format
    # Helper function to escape LaTeX special characters
    import pandas as pd

    # Example DataFrame

    # Generate LaTeX table
    latex_table = df_to_latex(df_for_pdf)

    # # Save to a .tex file
    # with open("basic_latex_table.tex", "w") as file:
    #     file.write(latex_table)
    #
    # print("LaTeX table saved as 'basic_latex_table.tex'")

    # latex_table=latex_table.replace(r'_',r'\_')
    # Replace only the escaped LaTeX commands
    # latex_code  = (latex_code
    #                            .replace(r'\textbackslash textcolor', r'\textcolor')
    #                            .replace(r'\textbackslash rule', r'\rule')
    #                            .replace(r'\{', '{')
    #                            .replace(r'\}', '}')
    #                            .replace(r'\textbackslash includegraphics',r'\includegraphics'))

    latex_insert_line_nodek(latexfilename,text=latex_table)
    # latex_end_table2c(latexfilename)
    command="echo " + "start" + " > error.txt"
    subprocess.call(command,shell=True)

    for slice_num in range(nib.load(grayscale_img_path).get_fdata().shape[2]):
        image_list=[]
        latex_start_tableNc_noboundary(latexfilename,3)
        # image_list.append(os.path.join('warped_moving_image_'+"{:03}".format(slice_num)+'.jpg'))
        image_list.append(os.path.join('COLIHM620406202215542_'+"{:03}".format(slice_num)+'.jpg'))
        image_list.append(os.path.join('regions_'+"{:03}".format(slice_num)+'.png'))

        # image_list.append(os.path.join('infarct_only_'+"{:03}".format(slice_num)+'.png'))
        image_list.append(os.path.join('../heatmapoutput_v1','slice_'+"{:03}".format(slice_num)+'.png'))
        # print(os.path.join('levelset_ct_with_infarct_only_'+"{:03}".format(slice_num)+'.png'))
        # command="echo " + os.path.join('original_ct_with_infarct_only_'+"{:03}".format(slice_num)+'.png') + " >> error.txt"
        # subprocess.call(command,shell=True)
        # if os.path.exists(os.path.join(output_dir,'original_ct_with_infarct_only_'+"{:03}".format(slice_num)+'.png')):
        #     image_list.append(os.path.join('original_ct_with_infarct_only_'+"{:03}".format(slice_num)+'.png'))
        # else:
        #     image_list.append(os.path.join('color_filler.png'))

        latex_insertimage_tableNc(latexfilename,image_list,3, caption="",imagescale=0.15, angle=90,space=0.51)
        latex_end_table2c(latexfilename)

    latex_end(latexfilename)

    os.chdir('workingoutput')
    print(glob.glob("./*"))
    command="pdflatex *.tex  " #+ 'lobar_output/'
    subprocess.call(command,shell=True)
    command="mv *.csv   " + '../lobar_output/'
    subprocess.call(command,shell=True)
    command="mv *.pdf   " + '../lobar_output/'
    subprocess.call(command,shell=True)
    os.chdir('../')

def dowload_files_for_evaluation(SESSION_ID):


    software_dir='software'
    region_mask_type='lobar'
    working='maskonly'
    mri_mask_dir=working #'maskonly' #'www_nitrc_org_frs/maskonly'
    file_output_dir='workinginput'
    SLICE_OUTPUT_DIRECTORY='workingoutput'
    output_directory='workingoutput'
    splitter='_fixed'
    output_dir=output_directory
    # return
    SCAN_ID,SCAN_NAME=get_selected_scan_info(SESSION_ID,file_output_dir)
    print(f'{SCAN_ID}::{SCAN_NAME}')
    # return

    working_dir_1='input'
    Version_Date="_VersionDate-" + '11122024' #dt.strftime("%m%d%Y")
    # DOWNLOAD THE REGISTERED INFARCT MASK and the REGISTERED SESSION CT
    download_an_xmlfile_with_URIString_func(SESSION_ID,f'{SESSION_ID}.xml',working_dir_1)
    resource_dir='PREPROCESS_SEGM'
    downloadfile_withasuffix(SESSION_ID,SCAN_ID,working_dir_1,resource_dir,'COLIHM620406202215542')
    downloadfile_withasuffix(SESSION_ID,SCAN_ID,working_dir_1,resource_dir,'warped_moving_image')
    downloadfile_withasuffix(SESSION_ID,SCAN_ID,working_dir_1,resource_dir,'fixed_image')
    downloadfile_withasuffix("SNIPR02_E09008","2",working_dir_1,resource_dir,'.nii')
    # downloadfiletolocaldir_py(SESSION_ID,SCAN_ID,resource_dir,working_dir_1)
    resource_dir='MASKS'
    downloadfile_withasuffix("SNIPR02_E09008","2",working_dir_1,resource_dir,'.nii')

    downloadfile_withasuffix(SESSION_ID,SCAN_ID,working_dir_1,resource_dir,'.nii')
    # downloadfiletolocaldir_py(SESSION_ID,SCAN_ID,resource_dir,working_dir_1)
    resource_dir='NIFTI'
    downloadfile_withasuffix(SESSION_ID,SCAN_ID,working_dir_1,resource_dir,'.nii')
    # downloadfiletolocaldir_py(SESSION_ID,SCAN_ID,resource_dir,working_dir_1)
    directory_of_files_after_deepreg=working_dir_1
    # return
    file_without_ext=SCAN_NAME.split('.nii')[0] ##os.path.basename(session_ct_path).split('.nii')[0]
    # predefined_legend=os.path.join(working_dir_1,'legend.csv') # '/software/legend.csv'
    # command='mv ' + os.path.join(mri_mask_dir,'*brain.bfc'+splitter+'*.nii.gz') + '  ' + output_dir
    # subprocess.call(command,shell=True)
    #
    #  ## '/software/www_nitrc_org_frs/maskonly'
    mask_img_paths=glob.glob(os.path.join(mri_mask_dir,'warped_1*_fixed_COLIHM620406202215542_lin1_BET.nii.gz')) #glob.glob(os.path.join(mri_mask_dir,'warped_1*BET.nii.gz'))  #glob.glob(os.path.join(mri_mask_dir,'*.nii.gz'))
    grayscale_img_path=os.path.join(directory_of_files_after_deepreg,'warped_moving_image.nii.gz')
    min_intensity,max_intensity=get_min_max_intensity(grayscale_img_path)
    gray_img=nib.load(grayscale_img_path).get_fdata()
    infarct_mask_from_yasheng=os.path.join(working_dir_1,file_without_ext + '_resaved_infarct_auto_removesmall.nii.gz')
    original_gray_filename=os.path.join(working_dir_1,SCAN_NAME)

    template_nifti_file='software/COLIHM620406202215542.nii.gz' ##scct_strippedResampled1.nii.gz'
    template_nifti_file_base_noext=os.path.basename(template_nifti_file).split('.nii')[0]
    # Find infarct mask
    # scct_strippedResampled1='scct_strippedResampled1'
    infarct_mask_pattern=f'warped_1_mov_{file_without_ext}_resaved_infarct_auto_removesmall_fixed_{template_nifti_file_base_noext}_lin1_BET.nii.gz'
    infarct_mask_list=glob.glob(os.path.join(directory_of_files_after_deepreg,infarct_mask_pattern)) ##f'warped_1_mov_{file_without_ext}*_resaved_infarct_auto_removesmallresampled_mov_fixed_{template_nifti_file_base_noext}_lin1.nii.gz'))
    print(infarct_mask_list)


    infarct_mask_filename=infarct_mask_list[0]

    
    #################


    project_name,subject_name, session_label,acquisition_site_xml,acquisition_datetime_xml,scanner_from_xml,body_part_xml,kvp_xml=get_info_from_xml(os.path.join(working_dir_1,f'{SESSION_ID}.xml'))
    print(f"{project_name}::{subject_name}::{session_label}::{acquisition_site_xml}::{acquisition_datetime_xml}::{scanner_from_xml}::{body_part_xml}::{kvp_xml}")

    variables=[project_name,subject_name, session_label,acquisition_site_xml,acquisition_datetime_xml,scanner_from_xml,body_part_xml,kvp_xml]
    print(variables)
    variable_dict={"project_name":project_name,"subject_name":subject_name, "session_label":session_label,"acquisition_site_xml":acquisition_site_xml,"acquisition_datetime_xml":acquisition_datetime_xml,"scanner_from_xml":scanner_from_xml,"body_part_xml":body_part_xml,"kvp_xml":kvp_xml}
    import pandas as pd
    df1 = pd.DataFrame([variable_dict])

    ## session_name, session_id,scan_name, volumes region wise, volume total, normal volume of region.
    df1['session_id']=SESSION_ID
    df1['scan_id']=SCAN_ID
    df1['scan_name']=SCAN_NAME
    df1['session_label']=session_label





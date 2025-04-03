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
XNAT_HOST_URL=os.environ['XNAT_HOST']  #'http://snipr02.nrg.wustl.edu:8080' #'https://snipr02.nrg.wustl.edu' #'https://snipr.wustl.edu'
XNAT_HOST = XNAT_HOST_URL # os.environ['XNAT_HOST'] #
XNAT_USER = os.environ['XNAT_USER']#
XNAT_PASS =os.environ['XNAT_PASS'] #
# SESSION_ID='SNIPR01_E00193' ## #'${1} #str(each_row['ID'])
import linecache
def to_2_sigfigs(x):
    if isinstance(x, (int, float, np.number)):
        if x == 0:
            return 0
        else:
            return float(f"{x:.2g}")
    return x  # Non-numeric entries remain unchanged
import pandas as pd

def transpose_with_column_names(df, index_col_name="Original Column Name", row_prefix="Row"):
    """
    Transposes the DataFrame so that original column names become the first column.

    Parameters:
    - df: pandas DataFrame to transpose
    - index_col_name: name of the first column after transpose (default: "Original Column Name")
    - row_prefix: prefix for the new column names (default: "Row")

    Returns:
    - A transposed DataFrame with original column names as the first column
    """
    df_transposed = df.transpose().reset_index()
    df_transposed.columns = [index_col_name] + [f"{row_prefix}{i+1}" for i in range(len(df_transposed.columns) - 1)]
    return df_transposed

def binarized_region_lobar(f,latexfilename):
    # File path and loading the DataFrame
    # f = './lobar_output/COLI_HLP45_02152022_1123_6lobar_VersionDate-11122024_02_27_2025_Transpose.csv' ##COLI_HLP45_02152022_1123_6lobar_VersionDate-11122024_01_24_2025_Transpose.csv'
    try:
        # subprocess.call("echo " + "I  inside try binarized_region_artery  ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
        # f = glob.glob('/workingoutput/lobar_output/*_Transpose.csv')[0] ## COLI_HLP45_02152022_1123_6arterial_VersionDate-11122024_01_24_2025_Transpose.csv'
        # subprocess.call("echo " + "I  of try 1  ::{}  >> /workingoutput/error.txt".format(f) ,shell=True )
        import pandas as pd
        df = pd.read_csv(f)
        # f = glob.glob('/workingoutput/lobar_output/*_Transpose.csv')[0]
        # df = pd.read_csv(f)
        total_volume=df['Value']
        # Broad regions to process
        broad_regions = [
            'white matter',
            'R. Frontal Lobe',
            'L. Frontal Lobe',
            'R. cingulate gyrus',
            'L. cingulate gyrus',
            'R. Parietal Lobe',
            'L. Parietal Lobe',
            'R. Temporal Lobe',
            'L. Temporal Lobe',
            'R. Occipital Lobe',
            'L. Occipital Lobe',
            'R. Insula',
            'L. Insula',
            'Brainstem',
            'Corpus Callosum',
            'Cerebellum'


        ]
        broad_regions_df = pd.DataFrame(columns=broad_regions)
        # broad_regions = [
        #     'anterior cerebral left', 'lenticulostriate left', 'middle cerebral left',
        #     'posterior cerebral left', 'choroidal and thalamoperfurators left',
        #     'basilar left', 'cerebellar left', 'ventricle left',    'anterior cerebral right', 'lenticulostriate right', 'middle cerebral right',
        #     'posterior cerebral right', 'choroidal and thalamoperfurators right',
        #     'basilar right', 'cerebellar right', 'ventricle right'
        # ]

        # Initialize columns for each broad region with 0
        for each_broad_region in broad_regions:
            df[each_broad_region] = 0

        # Add a row for Total Regions Volume
        df.loc[len(df)] = [None] * len(df.columns)  # Initialize empty row
        df.loc[len(df) - 1, 'Regions'] = 'Total Regions Volume'
        df.loc[len(df), 'Regions'] = 'Total Regions Percentage'
        df['infarct_present']=0
        # Ensure the 'Value' column is numeric, replacing non-convertible values with 0
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce').fillna(0)
        # total_volume=df.loc[df['Column_Name']=='infarct_volume_after_reg','Value']
        total_volume = df.loc[df['Column_Name'] == 'infarct_volume_after_reg', 'Value'].iloc[0]
        # thresh_percentage=10
        thresh_percentages=[25,30,35,40,45,50]
        for thresh_percentage in thresh_percentages:
            # Process each broad region infarct_volume_after_reg
            total_volume_all_regions=0
            for each_broad_region in broad_regions:
                # Filter the DataFrame for rows where 'Regions' contains the current broad region
                df_each_region = df[df['Regions'].str.contains(each_broad_region, na=False)]
                print(f"Data for {each_broad_region}:")
                print(df_each_region)
                print("-" * 50)  # Separator for better readability



                # Calculate the sum of the 'Value' column for this region
                this_region_sum = np.sum(df_each_region['Value'])
                print(f"Sum of 'Value' for {each_broad_region}: {this_region_sum}")
                print("-" * 50)  # Separator for better readability

                # Populate the Total Regions Volume row for this region
                df.loc[df['Regions'] == 'Total Regions Volume', each_broad_region] = this_region_sum
                df.loc[df['Regions'] == 'Total Regions Percentage', each_broad_region] = (this_region_sum/total_volume) * 100
                broad_regions_df.loc[0,each_broad_region]=this_region_sum
                total_volume_all_regions=total_volume_all_regions+this_region_sum
                # if (this_region_sum/total_volume) >0:
                #     print(this_region_sum/total_volume)
                #     break
                # Iterate through each row of df_each_region
                # if ((this_region_sum/total_volume) * 100 ) > 5:
                for index, row in df_each_region.iterrows():
                    # region_name = row['Regions']
                    # value = row['Value']
                    # value_perc=value/this_region_sum  * 100
                    # thresh_perc_value=(thresh_percentage/100)*this_region_sum
                    # if value_perc >=thresh_perc_value:
                    # print(f"Processing row {index}: Region = {region_name}, Value = {value}")
                    df.loc[index, each_broad_region] = this_region_sum #value ##_perc
                    # if value_perc>10.0:
                    #     df.loc[index, 'infarct_present'] = 1 ##value ##_perc

            # Display the modified DataFrame
            print(df)


            # In[3]:


            broad_regions_df


            # In[4]:


            import pandas as pd

            # Load the data
            # file_path = '/mnt/data/COLI_HLP45_02152022_1123_6arterial_VersionDate-11122024_01_21_2025_Transpose_binarized.csv'
            data = broad_regions_df #pd.read_csv(file_path)

            # Extract regions and their left/right values
            columns = data.columns
            regions = [col.replace("L. ", "") for col in columns if "L. " in col ]




            # In[5]:


            left_values = [data[f"L. {region}"].iloc[0] for region in regions]
            right_values = [data[f"R. {region}"].iloc[0] for region in regions]
            for each_col in columns:
                if not ("L." in each_col or "R." in each_col):
                    regions.append(each_col)
            # Create a DataFrame with "region", "left", and "right"
            # all_regions_df = pd.DataFrame({
            #     "region": regions,
            #     "left": left_values,
            #     "right": right_values
            # })
            # Ensure lists have the same length by padding with NaN if necessary
            max_length = max(len(regions), len(left_values), len(right_values))

            # Create DataFrame with padding for mismatched lengths
            all_regions_df = pd.DataFrame({
                "region": regions + [np.nan] * (max_length - len(regions)),
                "left": left_values + [np.nan] * (max_length - len(left_values)),
                "right": right_values + [np.nan] * (max_length - len(right_values))
            })

            # Display the resulting DataFrame
            all_regions_df['left_plus_right']=all_regions_df['left']+all_regions_df['right']


            # In[6]:


            # # Update the existing column in df2
            # # Filter all rows in df that match any value in all_regions_df['region']
            # # Iterate through all_regions_df rows
            # for each_id, each_row in all_regions_df.iterrows():
            #     # Filter rows in df where 'Regions' matches 'region' in each_row
            #     for each_id_1, each_row_1 in df.iterrows():

            #         # print(each_row_1['Regions']) #df[df['Regions'] == str(each_row['region'])]
            #         if each_row_1['Regions']==each_row['region']:  # Check if the filtered DataFrame is not empty
            #             print(each_row_1['Regions'])
            #             # all_regions_df.iloc[all_regions_df['region']==each_row['region'],'left_plus_right']=each_row_1['Value']
            #             all_regions_df.loc[all_regions_df['region'] == each_row['region'], 'left_plus_right'] = each_row_1['Value']

            # Merge df into all_regions_df based on matching 'region' and 'Regions'
            # Merge df into all_regions_df based on matching 'region' and 'Regions'
            merged_df = all_regions_df.merge(df[['Regions', 'Value']], left_on='region', right_on='Regions', how='left')

            # Use the 'Value' column to update 'left_plus_right', preserving old values where no match is found
            merged_df['left_plus_right'] = merged_df['Value'].combine_first(merged_df['left_plus_right'])

            # Drop unnecessary columns added during merge (optional)
            merged_df.drop(columns=['Regions', 'Value'], inplace=True)

            # Assign back to all_regions_df
            all_regions_df = merged_df

            # Display the updated DataFrame
            print(all_regions_df)
            side_percent_thresh=thresh_percentage #5.0
            each_region_percent_thresh=1.0
            all_regions_df['left_perc']=all_regions_df['left']/(all_regions_df['left_plus_right']) * 100
            all_regions_df['right_perc']=all_regions_df['right']/(all_regions_df['left_plus_right']) * 100
            all_regions_df['each_region_perc']=all_regions_df['left_plus_right']/total_volume_all_regions *100
            all_regions_df['each_region_perc_label']=0
            all_regions_df['each_region_perc_label'][all_regions_df['each_region_perc']>each_region_percent_thresh]=1
            all_regions_df['right_perc']=all_regions_df['right_perc']*all_regions_df['each_region_perc_label']
            all_regions_df['right_perc_label']=0
            all_regions_df['right_perc_label'][all_regions_df['right_perc']>side_percent_thresh]=1
            all_regions_df['left_perc']=all_regions_df['left_perc']*all_regions_df['each_region_perc_label']
            all_regions_df['left_perc_label']=0
            all_regions_df['left_perc_label'][all_regions_df['left_perc']>side_percent_thresh]=1
            all_regions_df['noside_perc_label']=0
            all_regions_df.loc[
                (pd.isna(all_regions_df['left_perc'])) &
                (pd.isna(all_regions_df['right_perc'])) &
                (all_regions_df['each_region_perc_label'] > 0.0),
                'noside_perc_label'
            ] = 1

            # # Add a blank row with 'region' set to 'total_sum'
            all_regions_df.loc[len(all_regions_df)] = ["total_sum"] + [None] * (len(all_regions_df.columns) - 1)
            # numeric_cols = all_regions_df.select_dtypes(include=["float64", "int64"]).columns
            # all_regions_df[numeric_cols] = all_regions_df[numeric_cols].apply(pd.to_numeric, errors="coerce")

            # # Fill the 'total_sum' row with the column-wise sum for numeric columns
            all_regions_df.loc[all_regions_df["region"] == "total_sum", 'left'] = all_regions_df['left'].sum(skipna=True)
            all_regions_df.loc[all_regions_df["region"] == "total_sum", 'right'] = all_regions_df['right'].sum(skipna=True)
            all_regions_df.loc[all_regions_df["region"] == "total_sum", 'left_plus_right'] = all_regions_df['left_plus_right'].sum(skipna=True)
            # print(all_regions_df)
            all_regions_df = all_regions_df.applymap(to_2_sigfigs)
            all_regions_df['dominant_region']=0
            all_regions_df['dominant_region_left']=0
            all_regions_df['dominant_region_right']=0
            dominant_region_idx=all_regions_df['each_region_perc'].idxmax()
            all_regions_df.loc[dominant_region_idx,'dominant_region']=1
            if all_regions_df.loc[dominant_region_idx,'left_perc'] > all_regions_df.loc[dominant_region_idx,'right_perc']:
                all_regions_df.loc[dominant_region_idx,'dominant_region_left']=1
            if all_regions_df.loc[dominant_region_idx,'left_perc'] < all_regions_df.loc[dominant_region_idx,'right_perc']:
                all_regions_df.loc[dominant_region_idx,'dominant_region_right']=1
            # all_regions_df.to_csv(f.split('.csv')[0]+"_binarized.csv",index=False)
            # all_regions_df=transpose_with_column_names(df, index_col_name="Side_Labels", row_prefix="")
            all_regions_df.to_csv(f.split('.csv')[0]+"_"+str(thresh_percentage)+"_binarized.csv",index=False)
            latex_table = df_to_latex_2(all_regions_df,1.0,'THRESHOLD::{}\n'.format(str(thresh_percentage)))
            latex_insert_line_nodek(latexfilename,text=latex_table) ##all_regions_df.to_latex(index=False))

            # In[7]:


            all_regions_df


            # In[8]:


            # all_regions_df


            # In[ ]:





            # In[9]:


            # df['Regions']=='R. Frontal Lobe'


            # In[10]:


            # df['Regions']==all_regions_df['region']
            #


            # In[11]:


            df.shape[0]


            # In[12]:


            # #!/usr/bin/env python
            # import requests
            # data = {
            #     'token': '36F3BA05DE0507BEBDFB94CC5DA13F93',
            #     'content': 'project',
            #     'format': 'json',
            #     'returnFormat': 'json'
            # }
            # r = requests.post('https://redcap.wustl.edu/redcap/api/',data=data)
            # print('HTTP Status: ' + str(r.status_code))
            # print(r.json())


            # In[13]:


            # df['Regions']

    except Exception as e :
        error_msg = traceback.format_exc()
        subprocess.call("echo " + "I traceback error  ::{}  >> /workingoutput/error.txt".format(error_msg) ,shell=True )
        # subprocess.call(['bash', '-c', f"echo 'Traceback error: {error_msg}' >> /workingoutput/error.txt"])



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


    software_dir='/software'
    region_mask_type='lobar'
    working='/maskonly'
    mri_mask_dir=working #'maskonly' #'www_nitrc_org_frs/maskonly'
    file_output_dir='/workinginput'
    SLICE_OUTPUT_DIRECTORY='/workingoutput'
    output_directory='/workingoutput'
    splitter='_fixed'
    output_dir=output_directory
    # return
    SCAN_ID,SCAN_NAME=get_selected_scan_info(SESSION_ID,file_output_dir)
    print(f'{SCAN_ID}::{SCAN_NAME}')
    # return

    working_dir_1='/input'
    Version_Date="_VersionDate-" + '11122024' #dt.strftime("%m%d%Y")
    # DOWNLOAD THE REGISTERED INFARCT MASK and the REGISTERED SESSION CT
    download_an_xmlfile_with_URIString_func(SESSION_ID,f'{SESSION_ID}.xml',working_dir_1)
    # print('ATUL')
    # return
    resource_dir='MASKLABEL'
    subprocess.call("echo " + "I FAILED  AT ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
    # downloadfiletolocaldir_py('SNIPR02_E14665',"MRI1",resource_dir,working_dir_1) #SNIPR01_E07218
    downloadfile_withasuffix('SNIPR02_E14665',"MRI1",working_dir_1,resource_dir,'.nii')
    downloadfile_withasuffix('SNIPR02_E14665',"MRI1",working_dir_1,resource_dir,'.csv')
    subprocess.call("echo " + "I PASSED  AT ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
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
    template_nifti_file='/software/COLIHM620406202215542.nii.gz' ##scct_strippedResampled1.nii.gz'
    template_nifti_file_base_noext=os.path.basename(template_nifti_file).split('.nii')[0]
    # Find infarct mask
    # scct_strippedResampled1='scct_strippedResampled1'
    infarct_mask_pattern=f'warped_1_mov_{file_without_ext}_resaved_infarct_auto_removesmall_fixed_{template_nifti_file_base_noext}_lin1_BET.nii.gz'
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
    moving_file_after_reg=os.path.join('/input','warped_moving_image.nii.gz') ##f'warped_mov_{file_without_ext}_brain_f_fixed_{template_nifti_file_base_noext}_lin1_brain_f.nii.gz')
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
    latex_additionalPackages(latexfilename,["pdflscape","longtable"])
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
    binarized_region_lobar(csvfilename.split('.csv')[0]+'_Transpose.csv',latexfilename)
    # latex_end_table2c(latexfilename)
    command="echo " + "start" + " >> /workingoutput/error.txt"
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
    os.chdir('/workingoutput')
    print(glob.glob("./*"))
    os.makedirs('/workingoutput/lobar_output/',exist_ok=True)
    command="cp *.csv   " + '/workingoutput/lobar_output/'
    subprocess.call(command,shell=True)
    command="pdflatex -interaction=nonstopmode *.tex  " #+ 'lobar_output/'
    subprocess.call(command,shell=True)
    # command="mv *.csv   " + '../lobar_output/'
    # subprocess.call(command,shell=True)
    command="cp *.pdf   " + '/workingoutput/lobar_output/'
    subprocess.call(command,shell=True)
    os.chdir('../')
    url=f'/data/experiments/{SESSION_ID}/scans/{SCAN_ID}'
    resource_dirname='LOCATION_DISTRIBUTION_LOBAR'
    file_name=latexfilename.split('.tex')[0] +'.pdf'
    uploadsinglefile_with_URI(url,file_name,resource_dirname)
    file_name=latexfilename.split('.tex')[0] +'.csv'
    uploadsinglefile_with_URI(url,file_name,resource_dirname)

def lobar_regions_heatmap_volumes_n_display(heatmap_nifti_file):


    software_dir='/software'
    region_mask_type='lobar'
    working='/maskonly'
    mri_mask_dir=working #'maskonly' #'www_nitrc_org_frs/maskonly'
    file_output_dir='/workinginput'
    SLICE_OUTPUT_DIRECTORY='/workingoutput'
    output_directory='/workingoutput'
    splitter='_fixed'
    output_dir=output_directory
    # return
    # SCAN_ID,SCAN_NAME=get_selected_scan_info(SESSION_ID,file_output_dir)
    # print(f'{SCAN_ID}::{SCAN_NAME}')
    # return

    working_dir_1='/input'
    Version_Date="_VersionDate-" + '11122024' #dt.strftime("%m%d%Y")
    # DOWNLOAD THE REGISTERED INFARCT MASK and the REGISTERED SESSION CT
    # download_an_xmlfile_with_URIString_func(SESSION_ID,f'{SESSION_ID}.xml',working_dir_1)
    # print('ATUL')
    # return
    resource_dir='MASKLABEL'
    subprocess.call("echo " + "I FAILED  AT ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
    # downloadfiletolocaldir_py('SNIPR02_E14665',"MRI1",resource_dir,working_dir_1) #SNIPR01_E07218
    downloadfile_withasuffix('SNIPR02_E14665',"MRI1",working_dir_1,resource_dir,'.nii')
    downloadfile_withasuffix('SNIPR02_E14665',"MRI1",working_dir_1,resource_dir,'.csv')
    subprocess.call("echo " + "I PASSED  AT ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
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
    grayscale_img_path=template_nifti_file='/software/COLIHM620406202215542.nii.gz' ##os.path.join(directory_of_files_after_deepreg,'warped_moving_image.nii.gz')
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
    command="echo " + "start" + " >> /workingoutput/error.txt"
    subprocess.call(command,shell=True)

    for slice_num in range(nib.load(grayscale_img_path).get_fdata().shape[2]):
        image_list=[]
        latex_start_tableNc_noboundary(latexfilename,3)
        # image_list.append(os.path.join('warped_moving_image_'+"{:03}".format(slice_num)+'.jpg'))
        image_list.append(os.path.join('COLIHM620406202215542_'+"{:03}".format(slice_num)+'.jpg'))
        image_list.append(os.path.join('regions_'+"{:03}".format(slice_num)+'.png'))

        # image_list.append(os.path.join('infarct_only_'+"{:03}".format(slice_num)+'.png'))
        os.makedirs('/workingoutput/heatmapoutput_v1/',exist_ok=True)
        image_list.append(os.path.join('/workingoutput/heatmapoutput_v1','slice_'+"{:03}".format(slice_num)+'.png'))
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

    os.chdir('/workingoutput')
    print(glob.glob("./*"))
    command="cp *.csv   " + '/workingoutput/lobar_output/'
    subprocess.call(command,shell=True)
    os.makedirs('/workingoutput/lobar_output/',exist_ok=True)
    command="pdflatex -interaction=nonstopmode *.tex  " #+ 'lobar_output/'
    subprocess.call(command,shell=True)
    command="mv *.csv   " + '/workingoutput/lobar_output/'
    subprocess.call(command,shell=True)
    command="mv *.pdf   " + '/workingoutput/lobar_output/'
    subprocess.call(command,shell=True)
    os.chdir('../')

def dowload_files_for_evaluation(SESSION_ID):


    software_dir='/software'
    region_mask_type='lobar'
    working='/maskonly'
    mri_mask_dir=working #'maskonly' #'www_nitrc_org_frs/maskonly'
    file_output_dir='/workinginput'
    SLICE_OUTPUT_DIRECTORY='/workingoutput'
    output_directory='/workingoutput'
    splitter='_fixed'
    output_dir=output_directory
    # return
    SCAN_ID,SCAN_NAME=get_selected_scan_info(SESSION_ID,file_output_dir)
    print(f'{SCAN_ID}::{SCAN_NAME}')
    # return

    working_dir_1='/input'
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





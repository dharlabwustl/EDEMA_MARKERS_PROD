#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os,sys,subprocess,glob


# In[2]:


import numpy as np
import pandas as pd
def binarized_region_lobar(f,latexfilename):
    # File path and loading the DataFrame
    # f = './lobar_output/COLI_HLP45_02152022_1123_6lobar_VersionDate-11122024_02_27_2025_Transpose.csv' ##COLI_HLP45_02152022_1123_6lobar_VersionDate-11122024_01_24_2025_Transpose.csv'
    try:
        # subprocess.call("echo " + "I  inside try binarized_region_artery  ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
        # f = glob.glob('/workingoutput/lobar_output/*_Transpose.csv')[0] ## COLI_HLP45_02152022_1123_6arterial_VersionDate-11122024_01_24_2025_Transpose.csv'
        # subprocess.call("echo " + "I  of try 1  ::{}  >> /workingoutput/error.txt".format(f) ,shell=True )
        import pandas as pd
        df = pd.read_csv(f)
        f = glob.glob('/workingoutput/lobar_output/*_Transpose.csv')[0]
        df = pd.read_csv(f)
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
            side_percent_thresh=5.0
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
            all_regions_df.to_csv(f.split('.csv')[0]+"_binarized.csv",index=False)
            latex_table = df_to_latex_2(all_regions_df,2.0,'THRESHOLD::{}\n'.format(str(thresh_percentage)))
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



############ DOWNLOAD WARPED MRI MASKS ###############

from download_with_session_ID import *
from utilities_simple_trimmed import *
from mri_masks_on_session_ct_with_infarct_templatectisfixed11112024 import *
import pandas as pd
from natsort import natsorted
import  time,os,glob,subprocess
import nibabel as nib
# import pandas as pd
import numpy as np
from pytablewriter import LatexTableWriter
import inspect,subprocess,sys
import mysql.connector
import random
import linecache
import csv,traceback
XNAT_HOST_URL=os.environ['XNAT_HOST']  #'http://snipr02.nrg.wustl.edu:8080' #'https://snipr02.nrg.wustl.edu' #'https://snipr.wustl.edu'
XNAT_HOST = XNAT_HOST_URL # os.environ['XNAT_HOST'] #
XNAT_USER = os.environ['XNAT_USER']#
XNAT_PASS =os.environ['XNAT_PASS'] #
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

def to_2_sigfigs(x):
    if isinstance(x, (int, float, np.number)):
        if x == 0:
            return 0
        else:
            return float(f"{x:.2g}")
    return x  # Non-numeric entries remain unchanged
import pandas as pd

def add_relative_infarct_percentage(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds two percentage columns to the DataFrame:
    1. 'relative_infarct_percent': % of each 'territory' within its 'broad_region'.
    2. 'combined_broad_region_percentage': % of the total 'combined_broad_region_volume'
       with respect to total infarct volume ('infarct_volume_after_reg').

    Args:
        df (pd.DataFrame): DataFrame with 'territory', 'combined_broad_region_volume',
                           and 'infarct_volume_after_reg'.

    Returns:
        pd.DataFrame: DataFrame with added percentage columns.
    """
    # Calculate % of each region within its broad_region
    df['relative_infarct_percent'] = (
            df['Value'] / df['combined_territory_volume'] * 100
    ).round(2)

    # Extract total infarct volume from the appropriate row (e.g., where Column_Name == 'infarct_volume_after_reg')
    total_infarct_volume = pd.to_numeric(
        df.loc[df['Column_Name'] == 'infarct_volume_after_reg', 'Value'], errors='coerce'
    ).values[0]  # assuming only one such row exists

    # Compute % of each combined_broad_region_volume with respect to total infarct volume
    # df['combined_broad_region_percentage'] = (
    #         df['combined_broad_region_volume'] / total_infarct_volume * 100
    # ).round(2)
    df['combined_infarct_volume_perc'] = (
            df['combined_infarct_volume'] / total_infarct_volume * 100
    ).round(2)

    return df

def add_infarct_analysis_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds infarct-related columns to a DataFrame:
    - 'side_infarct': 'L' if left, 'R' if right, based on 'Regions'.
    - 'broad_region': region name without 'left' or 'right'.
    - 'combined_broad_region_volume': total infarct volume for each broad region.

    Args:
        df (pd.DataFrame): DataFrame with 'Regions' and 'territory' columns.

    Returns:
        pd.DataFrame: DataFrame with additional columns added.
    """
    # Side infarct determination
    df['side_infarct'] = pd.NA
    df.loc[df['Regions'].str.contains(r'\bleft\b', case=False, na=False), 'side_infarct'] = 'L'
    df.loc[df['Regions'].str.contains(r'\bright\b', case=False, na=False), 'side_infarct'] = 'R'

    # Broad region extraction
    df['broad_region'] = df['Regions'].str.replace(r'\b(left|right)\b', '', case=False, regex=True).str.strip()

    # Convert territory to numeric
    df['territory'] = pd.to_numeric(df['territory'], errors='coerce')
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    # Compute combined volume for each broad region
    broad_region_sums = df.groupby('broad_region')['territory'].sum()
    df['combined_territory_volume'] = df['broad_region'].map(broad_region_sums)
    broad_region_infarct_sums = df.groupby('broad_region')['Value'].sum()
    df['combined_infarct_volume'] = df['broad_region'].map(broad_region_infarct_sums)
    return df

def binarized_region_artery_x(f,latexfilename):
    subprocess.call("echo " + "I  binarized_region_artery  ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
    try:
        import pandas as pd
        df = pd.read_csv(f)
        df=add_infarct_analysis_columns(df)
        df=add_relative_infarct_percentage(df)
        all_regions_df=df
        thresh_percentage=25
        all_regions_df.to_csv(f.split('.csv')[0]+"_"+str(thresh_percentage)+"_binarized.csv",index=False)
        # latex_insert_line_nodek(latexfilename,text='THRESHOLD::{}\n'.format(str(thresh_percentage)))
        latex_table = df_to_latex_2(all_regions_df,1.0,'THRESHOLD::{}\n'.format(str(thresh_percentage)))
        latex_insert_line_nodek(latexfilename,text=latex_table) ##all_regions_df.to_latex(index=False))
        subprocess.call("echo " + "I  of try 1_2 ::{}  >> /workingoutput/error.txt".format(f) ,shell=True )
        subprocess.call("echo " + "I  of try 1_3 ::{}  >> /workingoutput/error.txt".format(f.split('.csv')[0]+"_"+str(thresh_percentage)+"_binarized.csv") ,shell=True )
    except Exception as e :
        error_msg = traceback.format_exc()
        subprocess.call("echo " + "I traceback error  ::{}  >> /workingoutput/error.txt".format(error_msg) ,shell=True )
        # subprocess.call(['bash', '-c', f"echo 'Traceback error: {error_msg}' >> /workingoutput/error.txt"])

def binarized_region_artery(f, latexfilename):
    subprocess.call(f"echo I binarized_region_artery ::{inspect.stack()[0][3]} >> /workingoutput/error.txt", shell=True)

    try:
        df = pd.read_csv(f)

        # Define major arterial regions to analyze
        broad_regions = [
            "anterior cerebral artery left", "anterior cerebral artery right",
            "lenticulostriate left", "lenticulostriate right",
            "middle cerebral artery left", "middle cerebral artery right",
            "posterior cerebral artery left", "posterior cerebral artery right",
            "choroidal and thalamoperfurators left", "choroidal and thalamoperfurators right",
            "basilar left", "basilar right",
            "cerebellar left", "cerebellar right",
            "ventricle left", "ventricle right"
        ]

        broad_regions_df = pd.DataFrame(columns=broad_regions)
        broad_regions_df_territory = pd.DataFrame(columns=broad_regions)

        for region in broad_regions:
            df[region] = 0

        df.loc[len(df)] = [None] * len(df.columns)
        df.loc[len(df) - 1, 'Regions'] = 'Total Regions Volume'
        df.loc[len(df), 'Regions'] = 'Total Regions Percentage'
        df['infarct_present'] = 0

        df['Value'] = pd.to_numeric(df['Value'], errors='coerce').fillna(0)
        df['territory'] = pd.to_numeric(df['territory'], errors='coerce').fillna(0)

        total_volume = df.loc[df['Column_Name'] == 'infarct_volume_after_reg', 'Value'].iloc[0]

        thresh_percentages = [25, 30, 35, 40, 45, 50]

        for thresh in thresh_percentages:
            total_volume_all_regions = 0

            for region in broad_regions:
                df_region = df[df['Regions'].str.contains(region, na=False)]

                region_value_sum = df_region['Value'].sum()
                region_territory_sum = df_region['territory'].sum()

                df.loc[df['Regions'] == 'Total Regions Volume', region] = region_value_sum
                df.loc[df['Regions'] == 'Total Regions Percentage', region] = (region_value_sum / total_volume) * 100

                broad_regions_df.loc[0, region] = region_value_sum
                broad_regions_df_territory.loc[0, region] = region_territory_sum
                total_volume_all_regions += region_value_sum

                for index in df_region.index:
                    df.loc[index, region] = region_value_sum

            regions = [col.replace(" left", "") for col in broad_regions_df.columns if " left" in col]
            left_infarct = [broad_regions_df[f"{r} left"].iloc[0] for r in regions]
            right_infarct = [broad_regions_df[f"{r} right"].iloc[0] for r in regions]
            left_territory = [broad_regions_df_territory[f"{r} left"].iloc[0] for r in regions]
            right_territory = [broad_regions_df_territory[f"{r} right"].iloc[0] for r in regions]

            all_regions_df = pd.DataFrame({
                "region": regions,
                "left_infarct": left_infarct,
                "right_infarct": right_infarct,
                "left_territory": left_territory,
                "right_territory": right_territory
            })

            all_regions_df['infarct_sum'] = all_regions_df['left_infarct'] + all_regions_df['right_infarct']
            all_regions_df['territory_sum'] = all_regions_df['left_territory'] + all_regions_df['right_territory']

            all_regions_df['left_infarct_perc'] = all_regions_df['left_infarct'] / all_regions_df['left_territory'] * 100 # all_regions_df['infarct_sum'] * 100
            all_regions_df['right_infarct_perc'] = all_regions_df['right_infarct'] / all_regions_df['right_territory'] * 100 # all_regions_df['infarct_sum'] * 100
            all_regions_df['each_region_infarct_perc'] = all_regions_df['infarct_sum'] / all_regions_df['territory_sum'] * 100

            all_regions_df['each_region_perc_label'] = (all_regions_df['each_region_infarct_perc'] > 1.0).astype(int)
            all_regions_df['right_infarct_perc'] *= all_regions_df['each_region_perc_label']
            all_regions_df['right_perc_label'] = (all_regions_df['right_infarct_perc'] > thresh).astype(int)
            all_regions_df['left_infarct_perc'] *= all_regions_df['each_region_perc_label']
            all_regions_df['left_perc_label'] = (all_regions_df['left_infarct_perc'] > thresh).astype(int)

            all_regions_df['noside_perc_label'] = 0
            all_regions_df.loc[
                (all_regions_df['left_infarct_perc'].isna()) &
                (all_regions_df['right_infarct_perc'].isna()) &
                (all_regions_df['each_region_perc_label'] > 0),
                'noside_perc_label'
            ] = 1

            all_regions_df.loc[len(all_regions_df)] = ["total_sum"] + [None] * (len(all_regions_df.columns) - 1)
            all_regions_df.loc[all_regions_df["region"] == "total_sum", 'left_infarct'] = all_regions_df['left_infarct'].sum()
            all_regions_df.loc[all_regions_df["region"] == "total_sum", 'right_infarct'] = all_regions_df['right_infarct'].sum()
            all_regions_df.loc[all_regions_df["region"] == "total_sum", 'infarct_sum'] = all_regions_df['infarct_sum'].sum()
            all_regions_df.loc[all_regions_df["region"] == "total_sum", 'left_territory'] = all_regions_df['left_territory'].sum()
            all_regions_df.loc[all_regions_df["region"] == "total_sum", 'right_territory'] = all_regions_df['right_territory'].sum()
            all_regions_df.loc[all_regions_df["region"] == "total_sum", 'territory_sum'] = all_regions_df['territory_sum'].sum()

            all_regions_df = all_regions_df.applymap(to_2_sigfigs)

            all_regions_df['dominant_region'] = 0
            all_regions_df['dominant_region_left'] = 0
            all_regions_df['dominant_region_right'] = 0
            dom_idx = all_regions_df['each_region_infarct_perc'].idxmax()
            all_regions_df.loc[dom_idx, 'dominant_region'] = 1
            if all_regions_df.loc[dom_idx, 'left_infarct_perc'] > all_regions_df.loc[dom_idx, 'right_infarct_perc']:
                all_regions_df.loc[dom_idx, 'dominant_region_left'] = 1
            elif all_regions_df.loc[dom_idx, 'left_infarct_perc'] < all_regions_df.loc[dom_idx, 'right_infarct_perc']:
                all_regions_df.loc[dom_idx, 'dominant_region_right'] = 1

            binarized_csv = f.split('.csv')[0] + f"_{thresh}_binarized.csv"
            all_regions_df.to_csv(binarized_csv, index=False)

            latex_table = df_to_latex_2(all_regions_df, 1.0, f'THRESHOLD::{thresh}\n')
            latex_insert_line_nodek(latexfilename, text=latex_table)

            subprocess.call(f"echo I completed threshold {thresh} ::{f} >> /workingoutput/error.txt", shell=True)

    except Exception as e:
        error_msg = traceback.format_exc()
        subprocess.call(f"echo I traceback error ::{error_msg} >> /workingoutput/error.txt", shell=True)

def binarized_region_artery_1(f,latexfilename):
    subprocess.call("echo " + "I  binarized_region_artery  ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
    try:
        # subprocess.call("echo " + "I  inside try binarized_region_artery  ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
        # f = glob.glob('/workingoutput/lobar_output/*_Transpose.csv')[0] ## COLI_HLP45_02152022_1123_6arterial_VersionDate-11122024_01_24_2025_Transpose.csv'
        # subprocess.call("echo " + "I  of try 1  ::{}  >> /workingoutput/error.txt".format(f) ,shell=True )
        import pandas as pd
        df = pd.read_csv(f)
        # subprocess.call("echo " + "I  of try 1  ::{}  >> /workingoutput/error.txt".format(f) ,shell=True )
        # subprocess.call("echo " + "I  of try 1  ::{}  >> /workingoutput/error.txt".format(df) ,shell=True )
        total_volume=df['Value']
        # Broad regions to process
        broad_regions = [ "anterior cerebral artery left",
                          "anterior cerebral artery right",
                          "lenticulostriate left",
                          "lenticulostriate right",
                          "middle cerebral artery left",
                          "middle cerebral artery right",
                          "posterior cerebral artery left",
                          "posterior cerebral artery right",

                          "choroidal and thalamoperfurators left",
                          "choroidal and thalamoperfurators right",
                          "basilar left",
                          "basilar right",
                          "cerebellar left",
                          "cerebellar right",
                          "ventricle left",
                          "ventricle right"
                          ]

        broad_regions_df = pd.DataFrame(columns=broad_regions)
        broad_regions_df_total = pd.DataFrame(columns=broad_regions)

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
        df['territory'] = pd.to_numeric(df['territory'], errors='coerce').fillna(0)
        # total_volume=df.loc[df['Column_Name']=='infarct_volume_after_reg','Value']
        total_volume = df.loc[df['Column_Name'] == 'infarct_volume_after_reg', 'Value'].iloc[0]
        thresh_percentages=[25,30,35,40,45,50]

        for thresh_percentage in thresh_percentages:
            # thresh_percentage=30 ##10
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
                this_region_sum_territory = np.sum(df_each_region['territory'])
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


            import pandas as pd

            # Load the data
            # file_path = '/mnt/data/COLI_HLP45_02152022_1123_6arterial_VersionDate-11122024_01_21_2025_Transpose_binarized.csv'
            data = broad_regions_df #pd.read_csv(file_path)

            # Extract regions and their left/right values
            columns = data.columns
            regions = [col.replace(" left", "") for col in columns if " left" in col]
            left_values = [data[f"{region} left"].iloc[0] for region in regions]
            right_values = [data[f"{region} right"].iloc[0] for region in regions]

            # Create a DataFrame with "region", "left", and "right"
            all_regions_df = pd.DataFrame({
                "region": regions,
                "left": left_values,
                "right": right_values
            })

            # Display the resulting DataFrame
            all_regions_df['left_plus_right']=all_regions_df['left']+all_regions_df['right']
            # all_regions_df['left_perc']=all_regions_df['left']/(all_regions_df['left']+all_regions_df['right']) * 100
            # all_regions_df['right_perc']=all_regions_df['right']/(all_regions_df['left']+all_regions_df['right']) * 100
            # all_regions_df['each_region_perc']=all_regions_df['left_plus_right']/total_volume_all_regions *100
            # all_regions_df['each_region_perc_label']=0
            # all_regions_df['each_region_perc_label'][all_regions_df['each_region_perc']>5.0]=1
            # all_regions_df['right_perc']=all_regions_df['right_perc']*all_regions_df['each_region_perc_label']
            # all_regions_df['left_perc']=all_regions_df['left_perc']*all_regions_df['each_region_perc_label']
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


            # In[4]:


            # # Add a blank row with 'region' set to 'total_sum'
            all_regions_df.loc[len(all_regions_df)] = ["total_sum"] + [None] * (len(all_regions_df.columns) - 1)
            # numeric_cols = all_regions_df.select_dtypes(include=["float64", "int64"]).columns
            # all_regions_df[numeric_cols] = all_regions_df[numeric_cols].apply(pd.to_numeric, errors="coerce")

            # # Fill the 'total_sum' row with the column-wise sum for numeric columns
            all_regions_df.loc[all_regions_df["region"] == "total_sum", 'left'] = all_regions_df['left'].sum(skipna=True)
            all_regions_df.loc[all_regions_df["region"] == "total_sum", 'right'] = all_regions_df['right'].sum(skipna=True)
            all_regions_df.loc[all_regions_df["region"] == "total_sum", 'left_plus_right'] = all_regions_df['left_plus_right'].sum(skipna=True)

            # # Fill the 'total_sum' row with the column-wise sum for numeric columns
            # # numeric_cols = all_regions_df.select_dtypes(include=["float64", "int64"]).columns
            # Compute column-wise sums (ignoring non-numeric columns)
            # sums = all_regions_df.drop(columns=["region"]).sum(skipna=True).tolist()

            # Append the sums as a new row in the dataframe
            # all_regions_df.loc[len(all_regions_df)] = ["total_sum"] + sums
            all_regions_df


            # In[5]:


            # all_regions_df.loc[all_regions_df["region"] == "total_sum", numeric_cols] = all_regions_df[numeric_cols].sum(skipna=True)

            print(all_regions_df)
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
            # all_regions_df=transpose_with_column_names(df, index_col_name="Side_Labels", row_prefix="")
            subprocess.call("echo " + "I  of try 1_1 ::{}  >> /workingoutput/error.txt".format(f) ,shell=True )
            all_regions_df.to_csv(f.split('.csv')[0]+"_"+str(thresh_percentage)+"_binarized.csv",index=False)
            # latex_insert_line_nodek(latexfilename,text='THRESHOLD::{}\n'.format(str(thresh_percentage)))
            latex_table = df_to_latex_2(all_regions_df,1.0,'THRESHOLD::{}\n'.format(str(thresh_percentage)))
            latex_insert_line_nodek(latexfilename,text=latex_table) ##all_regions_df.to_latex(index=False))

            subprocess.call("echo " + "I  of try 1_2 ::{}  >> /workingoutput/error.txt".format(f) ,shell=True )
            subprocess.call("echo " + "I  of try 1_3 ::{}  >> /workingoutput/error.txt".format(f.split('.csv')[0]+"_"+str(thresh_percentage)+"_binarized.csv") ,shell=True )


            # In[6]:


            # print(all_regions_df)
            # all_regions_df.to_csv(f.split('.csv')[0]+"_binarized.csv",index=False)
            # all_regions_df


            # In[7]:


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


            # In[8]:


            # df['Regions']


            # In[ ]:
    except Exception as e :
        error_msg = traceback.format_exc()
        subprocess.call("echo " + "I traceback error  ::{}  >> /workingoutput/error.txt".format(error_msg) ,shell=True )
        # subprocess.call(['bash', '-c', f"echo 'Traceback error: {error_msg}' >> /workingoutput/error.txt"])



def process_csv_and_update_database(csv_file):
    try:
        # Open and read the CSV file
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)  # Read the CSV into a dictionary for easier column access

            # Process the first row (assuming one row only)
            row = next(reader)

            # Extract the essential keys
            session_id = row.get("session_id")
            scan_id = row.get("scan_id")
            session_name = row.get("session_name")
            scan_name = row.get("scan_name")

            # Iterate over all columns in the row
            for column_name, column_value in row.items():
                # Skip essential keys as they are used in the function parameters
                if column_name in ["session_id", "scan_id", "session_name", "scan_name"]:
                    continue

                # Call update_or_create_column for each column
                update_or_create_column(
                    session_id=session_id,
                    scan_id=scan_id,
                    column_name=column_name,
                    column_value=column_value,
                    session_name=session_name,
                    scan_name=scan_name
                )

        print("All data from the CSV file has been successfully processed.")

    except StopIteration:
        print("The CSV file is empty or does not contain any rows.")
    except FileNotFoundError:
        print(f"File not found: {csv_file}")
    except Exception as e:
        print(f"An error occurred: {e}")


def connect_to_database():
    # Pool of random IP addresses
    ip_pool = [
        "127.0.0.1"] #,
    #     "192.168.1.100",
    #     "192.168.1.101",
    #     "203.0.113.50",
    #     "203.0.113.51"
    # ]

    random_ip = random.choice(ip_pool)

    try:
        connection = mysql.connector.connect(
            host=random_ip,
            user="root",
            password="ircadircad",
            database="snipr_results"
        )
        print(f"Connected to database at {random_ip}")
        return connection
    except mysql.connector.Error as error:
        print(f"Failed to connect to the database: {error}")
        return None


def column_exists(cursor, table_name, column_name):
    """Check if a column exists in the table."""
    cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE '{column_name}';")
    return cursor.fetchone() is not None
def insert_data(session_id, session_name, scan_id, scan_name):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        # SQL query to insert data

        sql_query = """
            INSERT INTO results (session_id, session_name, scan_id, scan_name,session_id_scan_id)
            VALUES (%s, %s, %s, %s,%s)
        """

        # Parameters for the query
        data = (session_id, session_name, scan_id, scan_name,str(session_id)+"_"+str(scan_id))

        # Execute and commit the transaction
        cursor.execute(sql_query, data)
        connection.commit()

        print(f"Record inserted successfully. ID: {cursor.lastrowid}")

    except mysql.connector.Error as error:
        print(f"Failed to insert record into table: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")


def update_or_create_column(session_id, scan_id, column_name, column_value, session_name, scan_name):
    """Ensure the column exists and update or create the row."""
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        try:
            insert_data(session_id, session_name, scan_id, scan_name)
        except:
            pass
        # Generate session_id_scan_id
        session_id_scan_id = f"{session_id}_{scan_id}"

        # Step 1: Check if the row exists
        select_query = """
            SELECT * FROM results
            WHERE session_id_scan_id = %s;
        """
        cursor.execute(select_query, (session_id_scan_id,))
        row = cursor.fetchone()

        # If the row doesn't exist, insert it
        if row is None:
            print("No matching row found. Inserting new row...")
            insert_query = """
                INSERT INTO results (session_id_scan_id, session_id, scan_id, session_name, scan_name)
                VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (session_id_scan_id, session_id, scan_id, session_name, scan_name))
            connection.commit()

        # Step 2: Check if the column exists
        if not column_exists(cursor, "results", column_name):
            # Add the column if it doesn't exist
            alter_query = f"ALTER TABLE results ADD COLUMN {column_name} VARCHAR(255);"
            cursor.execute(alter_query)
            connection.commit()
            print(f"Column '{column_name}' added as VARCHAR(255).")

        # Step 3: Update the column value for the matching row
        update_query = f"""
            UPDATE results
            SET {column_name} = %s
            WHERE session_id_scan_id = %s;
        """
        cursor.execute(update_query, (column_value, session_id_scan_id))
        connection.commit()

        print(f"'{column_name}' updated to '{column_value}' for session_id='{session_id}' and scan_id='{scan_id}'.")

    except mysql.connector.Error as error:
        print(f"Failed to execute operation: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")


# Example usage

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
def arterial_region_volumes_n_display(SESSION_ID):
    try:
        software_dir='/software'
        region_mask_type='arterial'
        working='/maskonly'
        mri_mask_dir=working #'/maskonly' #'www_nitrc_org_frs//maskonly'
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
        # downloadfiletolocaldir_py('SNIPR01_E07218',"MRI1",resource_dir,working_dir_1) #SNIPR01_E07218
        downloadfile_withasuffix('SNIPR01_E07218',"MRI1",working_dir_1,resource_dir,'.nii')
        downloadfile_withasuffix('SNIPR01_E07218',"MRI1",working_dir_1,resource_dir,'.csv')
        subprocess.call("echo " + "I PASSED  AT ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
        #
        # return
        resource_dir='PREPROCESS_SEGM_1'
        # downloadfiletolocaldir_py('SNIPR01_E07218',"MRI1",resource_dir,mri_mask_dir)
        downloadfile_withasuffix('SNIPR01_E07218',"MRI1",mri_mask_dir,resource_dir,'COLIHM620406202215542')
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
        command='mv ' + os.path.join(mri_mask_dir,'*bfc'+splitter+'*.nii.gz') + '  ' + output_dir
        subprocess.call(command,shell=True)
        #
        #  ## '/software/www_nitrc_org_frs//maskonly'
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
        subprocess.call("echo " + "I PASSED AT xml_parameters::{}  >> /workingoutput/error.txt".format((f"{project_name}::{subject_name}::{session_label}::{acquisition_site_xml}::{acquisition_datetime_xml}::{scanner_from_xml}::{body_part_xml}::{kvp_xml}")) ,shell=True )
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
        subprocess.call("echo " + "I PASSED AT xml_parameters::{}  >> /workingoutput/error.txt".format(variables) ,shell=True )

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
        moving_file_after_reg=os.path.join('/input','warped_moving_image.nii.gz') ##f'warped_mov_{file_without_ext}_brain_f_fixed_{template_nifti_file_base_noext}_lin1_brain_f.nii.gz')
        moving_file_after_reg_nib=nib.load(moving_file_after_reg)
        moving_file_after_reg_nib_data=moving_file_after_reg_nib.get_fdata()
        moving_file_after_reg_nib_data[moving_file_after_reg_nib_data>0]=1
        moving_file_after_reg_nib_data[moving_file_after_reg_nib_data<1]=0
        template_nifti_file_nib=nib.load(template_nifti_file)
        moving_file_after_reg_nib_data_nib=nib.Nifti1Image(moving_file_after_reg_nib_data,affine=template_nifti_file_nib.affine,header=template_nifti_file_nib.header)
        nib.save(moving_file_after_reg_nib_data_nib,os.path.join('/input',os.path.basename(moving_file_after_reg).split('.nii')[0]+'_BET.nii.gz'))
        moving_file_after_reg_nib_data_volume=(np.sum(moving_file_after_reg_nib_data)*np.product(template_nifti_file_nib.header["pixdim"][1:4]))/1000
        df1['brain_volume_after_reg']=moving_file_after_reg_nib_data_volume
        df1['infarct_fraction_after_reg']=infarct_volume_after_reg/moving_file_after_reg_nib_data_volume #template_nifti_file_nib_data_volume
        df1['template_brain_volume']=template_nifti_file_nib_data_volume
        print('{}::{}::{}::{}'.format(mask_img_paths,infarct_mask_filename,template_nifti_file,region_mask_type))
        df2=volumes_regions_overlapping_infarct_on_ct(mask_img_paths,infarct_mask_filename,template_nifti_file,region_mask_type,infarct_volume_after_reg,infarct_volume_before_reg=infarct_volume_before_reg,splitter=splitter)
        df1.update(df2)
        # df1=df1.drop('lobar_regionbrain.bfc', axis=1)
        # print(df1)

        #

        now=time.localtime()
        date_time = time.strftime("_%m_%d_%Y",now)
        thisfilebasename=file_without_ext
        latexfilename=os.path.join(SLICE_OUTPUT_DIRECTORY,thisfilebasename + region_mask_type+Version_Date + date_time+".tex")
        csvfilename=os.path.join(SLICE_OUTPUT_DIRECTORY,thisfilebasename + region_mask_type+Version_Date + date_time+".csv")
        df1.to_csv(csvfilename,index=False)
        process_csv_and_update_database(csvfilename)
        # update_or_create_column(session_id, scan_id, column_name, column_value, session_name, scan_name)
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

        regions_csv=pd.read_csv(os.path.join(working_dir_1,'ArterialAtlasLables.csv'))
        regions_csv['masknumber']=regions_csv['Level1_intensity']
        regions_csv['region']=regions_csv['aterial territories']
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
            if f'{region_mask_type}_region' in each_item_region_with_num:
                region_num=int(each_item_region_with_num.split(f'{region_mask_type}_region')[1])
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
                    # pass
                # Assign the value using .loc for safer assignment
                df_for_pdf.loc[each_id, 'Regions'] = territory_value
                df_for_pdf.loc[each_id, 'legendcolor'] = territory_color
        # column_to_insert=df_for_pdf['session_label']
        # df_for_pdf.insert(0, 'session_label', column_to_insert)

        print(df_for_pdf)
        df_for_pdf['legendcolor']=df_for_pdf[ 'legendcolor'].apply(lambda filename: f"\\includegraphics[scale=0.2]{{{os.path.basename(filename)}}}" if pd.notna(filename) and filename else "")
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
    #     # Generate LaTeX table
    #     # Convert all numeric-looking columns to numeric data type, if necessary
    #     df_for_pdf = df_for_pdf.apply(pd.to_numeric, errors='ignore')

    #     # Round numeric columns to 2 decimal places
    #     for col in df_for_pdf.select_dtypes(include=['float64', 'int64']).columns:
    #         df_for_pdf[col] = df_for_pdf[col].round(2)
    # Function to round numeric values but keep strings unchanged


    # Apply the function to all columns (or specific columns)
        for col in df_for_pdf.columns:
            df_for_pdf[col] = round_mixed_column(df_for_pdf[col])

        df_for_pdf.to_csv(csvfilename.split('.csv')[0]+'_Transpose.csv',index=False)
        latex_table = df_to_latex_1(df_for_pdf)
        #latex_insert_line_nodek(latexfilename,text=latex_table)

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
        binarized_region_artery(csvfilename.split('.csv')[0]+'_Transpose.csv',latexfilename)
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
            command="echo " + os.path.join('original_ct_with_infarct_only_'+"{:03}".format(slice_num)+'.png') + " >> /workingoutput/error.txt"
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
        # command="cp *.csv   " + '/workingoutput/lobar_output/'
        # subprocess.call(command,shell=True)
        # command="mv *.csv   " + '/workingoutput/lobar_output/'
        # subprocess.call(command,shell=True)
        command="cp *.pdf   " + '/workingoutput/lobar_output/'
        subprocess.call(command,shell=True)
        os.chdir('../')
        url=f'/data/experiments/{SESSION_ID}/scans/{SCAN_ID}'
        resource_dirname='LOCATION_DISTRIBUTION_ARTERY'
        delete_file_with_ext(SESSION_ID,SCAN_ID,resource_dirname,'.pdf')
        delete_file_with_ext(SESSION_ID,SCAN_ID,resource_dirname,'.csv')
        file_name=latexfilename.split('.tex')[0] +'.pdf'
        uploadsinglefile_with_URI(url,file_name,resource_dirname)
        file_name=latexfilename.split('.tex')[0] +'.csv'
        uploadsinglefile_with_URI(url,file_name,resource_dirname)
        return 1

    except Exception as e:
        error_msg = traceback.format_exc()
        subprocess.call("echo " + "I traceback error ::{}  >> /workingoutput/error.txt".format(error_msg) ,shell=True )
        return 0
        # subprocess.run(
        #     ['tee', 'error_log.txt'],
        #     input=error_msg.encode(),
        #     stdout=subprocess.DEVNULL
        # )
def arterial_regions_heatmap_volumes_n_display(heatmap_nifti_file):


    software_dir='/software'
    region_mask_type='arterial'
    working='/maskonly'
    mri_mask_dir=working #'/maskonly' #'www_nitrc_org_frs//maskonly'
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
    downloadfile_withasuffix('SNIPR01_E07218',"MRI1",working_dir_1,resource_dir,'.nii')
    downloadfile_withasuffix('SNIPR01_E07218',"MRI1",working_dir_1,resource_dir,'.csv')
    subprocess.call("echo " + "I PASSED  AT ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
    #
    # return
    resource_dir='PREPROCESS_SEGM_1'
    # downloadfiletolocaldir_py('SNIPR02_E14665',"MRI1",resource_dir,mri_mask_dir)
    downloadfile_withasuffix('SNIPR01_E07218',"MRI1",mri_mask_dir,resource_dir,'COLIHM620406202215542')
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
    command='mv ' + os.path.join(mri_mask_dir,'*bfc'+splitter+'*.nii.gz') + '  ' + output_dir
    subprocess.call(command,shell=True)
    #
    #  ## '/software/www_nitrc_org_frs//maskonly'
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

    post_process_smooothing_closing(infarct_mask_filename,binary_threshold=0.7)
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

    regions_csv=pd.read_csv(os.path.join(working_dir_1,'ArterialAtlasLables.csv'))
    regions_csv['masknumber']=regions_csv['Level1_intensity']
    regions_csv['region']=regions_csv['aterial territories']
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
        if f'{region_mask_type}_region' in each_item_region_with_num:
            region_num=int(each_item_region_with_num.split(f'{region_mask_type}_region')[1])
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
#     \usepackage{pdflscape}
# \usepackage{longtable}
    latex_additionalPackages(latexfilename,["pdflscape","longtable"])
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

    os.chdir('/workingoutput')
    print(glob.glob("./*"))
    command="pdflatex -interaction=nonstopmode *.tex  " #+ 'lobar_output/'
    subprocess.call(command,shell=True)
    command="mv *.csv   " + '../lobar_output/'
    subprocess.call(command,shell=True)
    command="mv *.pdf   " + '../lobar_output/'
    subprocess.call(command,shell=True)
    os.chdir('../')





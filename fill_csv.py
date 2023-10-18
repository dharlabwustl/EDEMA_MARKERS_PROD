#!/usr/bin/env python
# coding: utf-8
import inspect

# In[1]:


import pandas as pd
import numpy as np
import os,sys,glob
import datetime
import argparse
# sys.path.append('/media/atul/WDJan2022/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD');
from utilities_simple import *
from download_with_session_ID import *
def make_identifier_column(csvfilename_input,csvfilename_output,output_column_name):
    returnvalue=0
    try:
        csvfilename_input_df=pd.read_csv(csvfilename_input)
        csvfilename_input_df['output_column_name']="ATUL" #csvfilename_input_df[columns_list_tocombine[0]].astype(str)
        # for x in range(len(columns_list_tocombine)):
        #     if x>0:
        #         csvfilename_input_df[output_column_name]=csvfilename_input_df[output_column_name].astype(str) + "_"+ csvfilename_input_df[columns_list_tocombine[x]].astype(str)
        csvfilename_input_df.to_csv(csvfilename_output,index=False)
        subprocess.call("echo " + "passed at ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
        returnvalue=1
    except:
        subprocess.call("echo " + "passed at ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
    return returnvalue
def create_empty_csvfile(csvfilename):
    returnvalue=0
    # print("I AM AT ::{}".format(inspect.stack()[0][3]))
    try:
        df=pd.DataFrame([1,2,3])
        # df =pd.DataFrame(columns=['TOREMOVE'])
        df.columns=['TOREMOVE']
        df.to_csv(csvfilename)
        subprocess.call("echo " + "passed at ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
    except:
        subprocess.call("echo " + "failed at ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
        pass
    return  returnvalue
def call_create_empty_csvfile(args):

    returnvalue=0
    # print("I AM AT ::{}".format(inspect.stack()[0][3]))
    try:
        csvfilename=args.stuff[1]
        expression=args.stuff[0].split('call_')[1] #+"("+args.stuff[1]+")"
        eval(expression)
        # create_empty_csvfile(csvfilename)
        subprocess.call("echo " + "passed at ::{}  >> /workingoutput/error.txt".format(expression) ,shell=True )
    except:
        subprocess.call("echo " + "failed at ::{}  >> /workingoutput/error.txt".format(expression) ,shell=True )
        pass
    return  returnvalue
def call_make_identifier_column(args):

    returnvalue=0
    # print("I AM AT ::{}".format(inspect.stack()[0][3]))
    try:
        csvfilename_input=args.stuff[1]
        csvfilename_output=args.stuff[2]
        output_column_name=args.stuff[3]
        make_identifier_column(csvfilename_input,csvfilename_output,output_column_name)
        subprocess.call("echo " + "passed at ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
    except:
        subprocess.call("echo " + "failed at ::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
        pass
    return  returnvalue

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stuff', nargs='+')
    args = parser.parse_args()
    name_of_the_function=args.stuff[0]
    return_value=0
    if name_of_the_function == "call_create_empty_csvfile":
        return_value=call_create_empty_csvfile(args)
    if name_of_the_function == "call_make_identifier_column":
        return_value=call_make_identifier_column(args)
        

    return return_value
if __name__ == '__main__':
    main()


# In[ ]:





# In[ ]:





# In[ ]:





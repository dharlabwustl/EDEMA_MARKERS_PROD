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

def create_empty_csvfile(args):

    returnvalue=0
    # print("I AM AT ::{}".format(inspect.stack()[0][3]))
    try:
        csvfilename=args.stuff[1]
        df=pd.DataFrame([1])
        df.columns=['TOREMOVE']
        df.to_csv(csvfilename)
        subprocess.call("echo " + "passed at expression::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
    except:
        subprocess.call("echo " + "failed at expression::{}  >> /workingoutput/error.txt".format(inspect.stack()[0][3]) ,shell=True )
        pass
    return  returnvalue


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stuff', nargs='+')
    args = parser.parse_args()
    return_value=0
    globals()[args.stuff[0]](args)
    return return_value
if __name__ == '__main__':
    main()


# In[ ]:





# In[ ]:





# In[ ]:





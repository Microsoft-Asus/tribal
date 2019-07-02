# ------------------------------------------------------------------------------
#  Cleaning functions used across state crawlers
# ------------------------------------------------------------------------------
# define various functions to clean business record data from state SoS websites
# ------------------------------------------------------------------------------
# Table of Contents
# 0. Dependencies
# 1. cleaning_sos

# 0. Dependencies
import pandas as pd
import numpy as np

# ------------------------------------------------------------------------------
# 1. cleaning_sos
# ------------------------------------------------------------------------------
# cleaning function to get SoS data into standard format
def cleaning_sos(df, id, bizname, pzip, paddress1=None, paddress2=None, pcity=None, \
                 pstate=None, maddress1=None, \
                 maddress2=None, mcity=None, mstate=None, \
                 mzip=None, email=None, phone=None):
    # Parameters:
    # variable names from SoS data set to be standardized:
        # id: unique id
        # bizname: name of business
        # p* vars: physical address components
        # m* vars: mailing address components

    # get non-missing list of parameters passed
    params=[id, bizname, paddress1, paddress2, pcity, pstate, pzip, maddress1,
              maddress2, maddress2, mcity, mstate, mzip, email, phone]
    str_params= ['id', 'bizname', 'paddress1', 'paddress2', 'pcity', 'pstate',
                'pzip', 'maddress1', 'maddress2', 'maddress2', 'mcity',
                'mstate', 'mzip', 'email', 'phone']

    rename_dict={}
    # rename columns to standardized names
    for i,j in zip(params, str_params):
        if i != None:
            rename_dict[i]= j

    df.rename(index=str, columns=rename_dict, inplace=True)


    # clean up zip codes - drop non-numeric characters to force it to be a
    # numeric column if not already
    for i in ['pzip', 'mzip']:
        if (i in rename_dict.values()):
            if (df[i].dtype=='O'):
                df[i]=df[i].replace('', np.nan, regex=True)
                df[i]=pd.to_numeric(df[i], errors='coerce')

    # capitalize all alphabetical string chars to match FDA list
    for i in str_params:
        if (i in rename_dict.values()):
            if (df[i].dtype=='O'):
                df[i] = df[i].str.upper()

    return(df)

"""
Code:       Python 3.7.1
Created:    Dec 26 2018
Author:     Luke Patterson
"""

import time
import csv
import os
import math
import pandas as pd
import requests


"""
- This function writes the geocoded retailer dataset (dictionary) to a csv formatted file.
"""
def open_retailer_data():
    row = pd.read_csv('input/raw_Nielsen_POS_data_full.csv')
    retailer = pd.DataFrame()
    #Read the data from appropriate variables in raw csv file from Nielsen.
    # retailer['retailer_name']=row['Store Name']
    # retailer['retailer_legal_name']=""
    retailer['retailer_id']=row['TDLinx Store Code']
    retailer['retailer_streetad']=row['Store Street Address']
    retailer['retailer_city']=row['Store City']
    retailer['retailer_state']=row['Store State']
    retailer['retailer_zip']=row['Store ZIP Code'].astype('str').str[0:5]
    # retailer['retailer_fullad']= retailer['retailer_streetad'] + ' ' + retailer['retailer_city']+ ", " + \
    #     retailer['retailer_state'] + ' ' + retailer['retailer_zip']
    return(retailer)

"""
- This function takes the list of individual addresses as an argument
- The list is then broken down into individual lists of a max amount of 1,000 addresses
- Calls the write batches function to write the lists to csv files
"""
def create_batches(df):
    num_batch = math.ceil(len(df.index)/1000)
    for i in range(num_batch):
        if i != num_batch:
            batch = df.iloc[1000*i:1000*(i+1),:]
        else:
            batch = df.iloc[1000*i:len(df.index),:]
        batch.to_csv('step_3_work/batches/batch_'+str(i)+'.csv', index = False, header= False)
"""
- This is where the program is executed from start to finish.
"""

# Path for scrubbed retailer data file
retailersdf = open_retailer_data()

retailer_batches = create_batches(retailersdf)

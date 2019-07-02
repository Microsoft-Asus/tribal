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
    row = pd.read_csv('step_0_work/output/Public retail data clean.csv')
    row = row.loc[(row['Longitude']==0) | (row['Longitude'].isna()==True) |
        (row['Latitude']==0) | (row['Latitude'].isna()==True) ,:]
    retailer = pd.DataFrame()
    #Read the data from appropriate variables in raw csv file from Nielsen.
    # retailer['retailer_name']=row['Store Name']
    # retailer['retailer_legal_name']=""
    retailer['retailer_id']=row['IMPAQ_ID']
    retailer['retailer_streetad']=row['Address Line 1']
    retailer['retailer_city']=row['City']
    retailer['retailer_state']=row['State']
    retailer['retailer_zip']=row['Zip'].astype('str').str[0:5]
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
        batch.to_csv('step_0_work/batches/batch_'+str(i)+'.csv', index = False, header= False)
"""
- This is where the program is executed from start to finish.
"""

# Path for scrubbed retailer data file
retailersdf = open_retailer_data()

retailer_batches = create_batches(retailersdf)

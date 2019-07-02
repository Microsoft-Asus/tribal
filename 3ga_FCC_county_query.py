import csv
import time
import urllib
import pandas as pd
import numpy as np
import requests
import json

"""
- This function takes the geocoded location coordinates
- Lookup uses API for FCC Database
- Function returns the unique FIPS identifier for the county name
"""
def find_census_block_code(lon, lat):
    try:
        print(time.clock())
        request_address = 'http://geo.fcc.gov/api/census/area?lat='+str(lat)+'&lon='+str(lon)+'&format=json'
        fcc_req = urllib.request.urlopen(request_address).read()
        county_name = json.loads(fcc_req)['results'][0]['county_name']
        return county_name
    except:
        return 'FCC API Error'
df = pd.read_csv('step_3_work/output/List_for_FCC_query.csv')
df['County_update'] = df[['Longitude_update','Latitude_update']].apply(lambda x: find_census_block_code(x[0],x[1]),axis=1)
df.to_csv('step_3_work/output/FCC_query_output.csv',index= False)

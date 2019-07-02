# mess around with google places api
import pandas as pd
import numpy as np
import urllib.request
import urllib.parse
import json

# load in retailers data
df = pd.read_csv("step_0_work/output/Public retail data clean_geocoded.csv")

# my api key
key = 'AIzaSyB7WmtDmJrnMyKqoWWPqn9iE7IqSEaq-BQ'

# build api URL for records
res_df = pd.DataFrame(columns=['est_id', 'cand_id'])
for i in range(len(df)):
    if i % 10 == 0:
        print(i)
    # first try longitude/latitude
    # turns out this won't work
    # input_lat = df.loc[i,'retailer_latitude'].astype('str').replace(' ','%20')
    # input_long = df.loc[i,'retailer_longtitude'].astype('str').replace(' ','%20')
    # url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=' + \
    # input_lat + input_long + '&inputtype=textquery&key=' + key
    #
    # # request possible results from google places search
    # req = urllib.request.Request(url)
    # f= (urllib.request.urlopen(req))
    # data = pd.read_json(f)['candidates']



    # try full address

    input = df.loc[i,'Full Address'].replace(' ','%20')
    input_lat = df.loc[i,'Latitude'].astype('str').replace(' ','%20')
    input_long = df.loc[i,'Longitude'].astype('str').replace(' ','%20')
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=' + \
        input + '&inputtype=textquery&key=' + key + '&locationbias=point:' + \
        input_lat + ',' + input_long
    # request possible results from google places search
    req = urllib.request.Request(url)
    f= (urllib.request.urlopen(req))
    data = pd.read_json(f)['candidates']

    # if that didn't work, try name of establishment and the city/state
    if len(data.index) == 0:
        input = df.loc[i,'DBA Name'].replace(' ','%20') + '%20' +  \
            df.loc[i,'City'].replace(' ','%20') + '%20' + \
            df.loc[i,'State'].replace(' ','%20')
        url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=' + \
        input + '&inputtype=textquery&key=' + key

        # request possible results from google places search
        req = urllib.request.Request(url)
        f= (urllib.request.urlopen(req))
        data = pd.read_json(f)['candidates']
    # get details for possible matches from google places details
    fields = 'address_component,adr_address,alt_id,formatted_address,' + \
        'geometry,icon,id,name,permanently_closed,photo,' + \
        'place_id,plus_code,scope,type,url,utc_offset,vicinity,' + \
        'formatted_phone_number,international_phone_number,opening_hours,website'
    for n,j in enumerate(data):
        durl = 'https://maps.googleapis.com/maps/api/place/details/json?placeid=' + \
            j['place_id'] +'&fields='+ fields + '&key=' +key
        dreq = urllib.request.Request(durl)
        det_f= urllib.request.urlopen(dreq)
        log = pd.io.json.json_normalize((json.load(det_f))['result'])
        res_df = res_df.append(pd.concat([pd.DataFrame([[i,n]],
            columns=['est_id', 'cand_id']), log], axis=1), sort=False)
        #

res_df.to_pickle('./step_1_work/output/google_output.pkl')

#https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=4820%20Park%20Ave%20Bethesda%20MD%2020816&inputtype=textquery&key=AIzaSyB7WmtDmJrnMyKqoWWPqn9iE7IqSEaq-BQ
#https://maps.googleapis.com/maps/api/place/details/json?placeid=ChIJC8WWwYzJt4kRcArHgtC2HIs&key=AIzaSyB7WmtDmJrnMyKqoWWPqn9iE7IqSEaq-BQ

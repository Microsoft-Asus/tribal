# clean address file and create batches for data
def A_create_batches(path, input_csv,batch_loc, address_var):
    # parameters
    # path: master path to project folder
    # input_csv: csv of addresses to geocode
    # batch_loc: location of where to store batch files
    # address_var: variable with full address to use
    # id_var: variable with unique identifier to merge back
    import time
    import csv
    import os
    import math
    import pandas as pd
    import usaddress as usa
    import requests

    # load address data
    df = pd.read_csv(path + '/' + input_csv)
    # parse out the components of the address column
    def try_tag(str):
        try:
            s=usa.tag(str)
            return(s[0])
        except:
            return('Not tagged')
    addr_df = df[address_var].apply(try_tag).apply(pd.Series)

    retailer = pd.DataFrame()
    #Read the data from appropriate variables in raw csv file from Nielsen.
    # retailer['retailer_name']=row['Store Name']
    # retailer['retailer_legal_name']=""
    retailer['retailer_id']=df.index
    retailer['retailer_streetad']=addr_df['AddressNumber'].str.cat(
        [addr_df['StreetNamePreType'], addr_df['StreetName'],
        addr_df['StreetNamePostType'], addr_df['OccupancyType'],
        addr_df['OccupancyIdentifier']], na_rep='', sep = ' '
    ).str.strip()
    retailer['retailer_city']=addr_df['PlaceName']
    retailer['retailer_state']=addr_df['StateName']
    retailer['retailer_zip']=addr_df['ZipCode'].astype('str').str[0:5]
    # retailer['retailer_fullad']= retailer['retailer_streetad'] + ' ' + retailer['retailer_city']+ ", " + \
    #     retailer['retailer_state'] + ' ' + retailer['retailer_zip']

    # filter out missing addresses, fill na with missing
    retailer = retailer.fillna('')
    retailer = retailer.dropna(how = 'all', subset= ['retailer_streetad','retailer_city'])

    # create batches to run through Census geocoder
    num_batch = math.ceil(len(df.index)/1000)
    for i in range(num_batch):
        if i != num_batch:
            batch = retailer.iloc[1000*i:1000*(i+1),:]
        else:
            batch = retailer.iloc[1000*i:len(retailer.index),:]
        batch.to_csv(path+'/'+batch_loc+'/batch_'+str(i)+'.csv', index = False, header= False)

# function to take batches and conduct census geocoding
def B_census_geocoding(path, batch_path, output_path, batch_num):
    import time
    import csv
    import os
    import math
    import pandas as pd
    import censusgeocode as cg
    import requests
    import datetime

    def create_batch_paths(start_no, end_no):
        batch_paths = []
        start = start_no
        end = end_no
        for i in range(start, end):
            batch_paths.append(path + '/' + batch_path + '/batch_'+str(i)+'.csv')
        return(batch_paths)

    paths = create_batch_paths(0,batch_num)

    for h,i in enumerate(paths):
        print('Geocoding batch #' + str(h))
        start = datetime.datetime.now()
        if h == 0:
            result = cg.addressbatch(paths[h])
            df = pd.DataFrame.from_dict(result)
        else:
            df = df.append(pd.DataFrame.from_dict(cg.addressbatch(paths[h])), sort=True)
        print(datetime.datetime.now() - start)
        #df.to_csv('step_0_work/output/temp/batch_'+ str(h) +'_temp.csv', index = False)

    df.to_csv(path + '/' + output_path + '/Census_geocoded_retailers.csv', index = False)

# function to conduct google geocoding for remaining non-matches
def C_google_geocoding(path, input_path, output_path, key):
    import csv
    import time
    import requests
    import numpy as np
    import pandas as pd
    from geopy.geocoders import GoogleV3 as google
    from geopy.exc import (
        GeocoderQueryError,
        GeocoderQuotaExceeded,
        ConfigurationError,
        GeocoderParseError,
        GeocoderTimedOut,
        GeocoderServiceError,
    )
    from geopy.geocoders import Nominatim

    df = pd.read_csv(path + '/' + input_path + '/Census_geocoded_retailers.csv')
    df = df.loc[df['match']==False,:]
    df.reset_index(inplace=True, drop=True)

    coder = google(api_key=key, timeout=10)
    # subset of data set for completing partial interrupt
    #df = df[2866:]
    for i,j in df.iterrows():
        if i % 100 == 0:
            print(i)
        try:
            result = coder.geocode(j['address'])
            if result != None:
                match_type= result.raw['geometry']['location_type']
                df.loc[i,'lat']= result[1][0]
                df.loc[i,'lon']= result[1][1]
                df.loc[i,'match']='Google'
                df.loc[i,'matchtype']=match_type
        except:
            print('error in coding observation ' + str(i) )
            continue

    df.to_csv(path + '/' + output_path +'/google_geocoded_retailers.csv', index = False)

def D_clean_merge_matches(path, input_csv,input_path, output_csv, output_path):
    import pandas as pd
    import numpy as np

    # load two parts of the google geocoding and append them
    #p1_df = pd.read_csv('step_3_work/output/google_geocoded_retailers_partial.csv')
    #p2_df = pd.read_csv('step_3_work/output/google_geocoded_retailers.csv')
    #ggl_df=p1_df.append(p2_df)
    ggl_df= pd.read_csv(path + '/' + input_path + '/google_geocoded_retailers.csv')

    # load census geocoding
    cen_df = pd.read_csv(path + '/' + input_path + '/Census_geocoded_retailers.csv')

    # remove approximate google geocodings
    ggl_df.loc[ggl_df['matchtype']=='APPROXIMATE', 'lat'] = np.nan
    ggl_df.loc[ggl_df['matchtype']=='APPROXIMATE', 'lon'] = np.nan
    ggl_df.loc[ggl_df['matchtype']=='APPROXIMATE', 'match'] = 'False'
    ggl_df.loc[ggl_df['matchtype']=='APPROXIMATE', 'matchtype'] = np.nan

    cen_df.index=cen_df['id']-1
    cen_df['matchsource']='Census'
    ggl_df.index=ggl_df['id']-1

    # merge with census DataFrame
    df = cen_df
    df.update(ggl_df)
    df.loc[df['match']=='Google','matchsource']='Google'
    df.loc[df['match']=='False','matchsource']=np.nan
    df.loc[df['match']=='Google','match']='True'
    df = df.rename(columns={"lat": "Latitude", "lon": "Longitude"})
    # save final geocoded DataFrame
    df.to_csv(path + '/' + output_path + '/geocoded_retailers.csv', index = False)

    # update the original list
    ori_df = pd.read_csv(path + '/' + input_csv)
    ori_df['matchsource'] = 'Not Geocoded'
    ori_df.index = ori_df.index.astype('int')
    ori_df['Longitude'] = np.nan
    ori_df['Latitude'] = np.nan
    ori_df.update(df)
    ori_df.to_csv(path + '/' + output_csv, index = False)

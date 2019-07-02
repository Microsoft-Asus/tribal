# Geocode remaining retailers from Nielsen POS data not done by Census with
# Google geocoder
def main():
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

    df = pd.read_csv('step_3_work/output/Census_geocoded_retailers.csv')
    df = df.loc[df['match']==False,:]
    df.reset_index(inplace=True, drop=True)
    key = 'AIzaSyB7WmtDmJrnMyKqoWWPqn9iE7IqSEaq-BQ'

    coder = google(api_key=key, timeout=10)
    # subset of data set for completing partial interrupt
    #df = df[2866:]
    for i,j in df.iterrows():
        if i % 100 == 0:
            print(i)
        result = coder.geocode(j['address'])
        if result != None:
            match_type= result.raw['geometry']['location_type']
            df.loc[i,'lat']= result[1][0]
            df.loc[i,'lon']= result[1][1]
            df.loc[i,'match']='Google'
            df.loc[i,'matchtype']=match_type

    df.to_csv('step_3_work/output/google_geocoded_retailers.csv', index = False)

if __name__ == '__main__':
    main()

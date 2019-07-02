# clean up google geocode matches, and merge with census matches to make final file
def main():
    import pandas as pd
    import numpy as np

    # load two parts of the google geocoding and append them
    #p1_df = pd.read_csv('step_3_work/output/google_geocoded_retailers_partial.csv')
    #p2_df = pd.read_csv('step_3_work/output/google_geocoded_retailers.csv')
    #ggl_df=p1_df.append(p2_df)
    ggl_df= pd.read_csv('step_3_work/output/google_geocoded_retailers.csv')
    
    # load census geocoding
    cen_df = pd.read_csv('step_3_work/output/Census_geocoded_retailers.csv')

    # remove approximate google geocodings
    ggl_df.loc[ggl_df['matchtype']=='APPROXIMATE', 'lat'] = np.nan
    ggl_df.loc[ggl_df['matchtype']=='APPROXIMATE', 'lon'] = np.nan
    ggl_df.loc[ggl_df['matchtype']=='APPROXIMATE', 'match'] = 'False'
    ggl_df.loc[ggl_df['matchtype']=='APPROXIMATE', 'matchtype'] = np.nan

    cen_df.index=cen_df['id']
    cen_df['matchsource']='Census'
    ggl_df.index=ggl_df['id']

    # merge with census DataFrame
    df = cen_df
    df.update(ggl_df)
    df.loc[df['match']=='Google','matchsource']='Google'
    df.loc[df['match']=='False','matchsource']=np.nan
    df.loc[df['match']=='Google','match']='True'

    # save final geocoded DataFrame
    df.to_csv('step_3_work/output/geocoded_retailers.csv', index = False)
if __name__ == '__main__':
    main()

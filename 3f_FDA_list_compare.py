# FDA_list_compare
# now that we have a list of tribal retailers from POS, compare with
# FDA list to note which already exist on the FDA list

import pandas as pd
import numpy as np
import geopandas as gp
from shapely.geometry import Point
from functions.matching_functions import name_match_scoring as name_match
from functions.matching_functions import address_match_scoring as addr_match
from functions.matching_functions import match_select_agg
from functions.matching_functions import display_results
from functions.cleaning_functions import cleaning_sos
import math
# load original Nielsen dataset
niel_df = pd.read_csv('input/raw_Nielsen_POS_data_full.csv', low_memory=False)

# load pos data frame
pos_df = pd.read_csv('step_3_work/output/tribal_retailers.csv')
pos_df['Coordinates'] = list(zip(pos_df.lon, pos_df.lat))
pos_df['Coordinates'] = pos_df['Coordinates'].apply(Point)
pos_df = gp.GeoDataFrame(pos_df, geometry='Coordinates')
pos_df['FDA_match'] = False
pos_df['FDA_id'] = np.nan
pos_df['FDA_dist_miles'] = np.nan
pos_df['FDA_coord'] = Point()
pos_df['Niel_id'] = pos_df['id']

# merge with nielsen data frame and clean for matching
merge_df = pos_df.merge(
     niel_df, how='left', left_on='id', right_on='TDLinx Store Code'
)

# clean up merged dataframe for running matching code
merge_df.drop('id', axis=1, inplace = True)
merge_df['paddress2']= ''
merge_df['Store ZIP Code'] = merge_df['Store ZIP Code'].astype('str').str[0:5]
merge_df = cleaning_sos(merge_df, id='FDA_id', bizname='Store Name', pzip='Store ZIP Code',
    paddress1='Store Street Address', paddress2='paddress2',
    pcity='Store City', pstate='Store State')

# load fda data frame
fda_df = pd.read_csv('step_1_work/output/retailers_name_addr_update.csv')
fda_df['Coordinates'] = list(zip(fda_df.Longitude_update, fda_df.Latitude_update))
fda_df['Coordinates'] = fda_df['Coordinates'].apply(Point)
fda_df = gp.GeoDataFrame(fda_df, geometry='Coordinates')
# drop retailers with missing coordinates
fda_df = fda_df.dropna(subset = ['Longitude_update','Latitude_update'])

# try to match on names, addresses
#for i,j in fda_df.iterrows():
# set up merge_df
matches = []
for i,j in fda_df.iterrows():
    #if i % 10 == 0:
    print(i)
    # for each fda retailer, score names
    out = name_match(j, merge_df)
    out = out.merge(addr_match(j, merge_df),
        left_index=True, right_index=True, on='id')
    out = merge_df.merge(out, left_index=True, right_index=True, on='id')
    # add distance score to each Nielsen retailer which is distance in miles
    pos_coord = out.Coordinates
    fda_coord = j['Coordinates']
    # multiply by 65.32411155 to make geodist into miles
    out['dist_score'] = pos_coord.distance(fda_coord) * 65.32411155
    # match = match_selection(out, 'basic name & addr', name_wgt=0, addrnum_wgt=1,
    #     strname_wgt=.01, strtype_wgt=.01, zip_wgt=1)
    match = match_select_agg(out, name_wgt=1, addrnum_wgt=0,
        strname_wgt=0, strtype_wgt=0, zip_wgt=1, dist_thresh = .03, match_thresh = 1.95)

    # record FDA record in Nielsen data if match is found
    if len(match) > 0:
        for k in match.index:
            id = k
            merge_df.loc[id, 'FDA_match'] = True
            merge_df.loc[id, 'FDA_id'] = j['IMPAQ_ID']
            # chained assignment warning doesn't matter here, so we'll suppress
            pd.options.mode.chained_assignment = None
            pos_coord = match.loc[id,'Coordinates']
            fda_coord = j['Coordinates']
            # multiply by 65.32411155 to make geodist into miles
            dist = pos_coord.distance(fda_coord) * 65.32411155
            match.loc[id,'FDA_dist_miles']=dist
            merge_df.loc[id,'FDA_dist_miles'] = dist
            pd.options.mode.chained_assignment = 'warn'
        matches.append([j, match])

# code to output logs of matches
display_results(matches, 'name_dist_log', id='IMPAQ_ID', verbose = 1,
    vars = ['id', 'Niel_id','bizname','address','FDA_dist_miles', 'name_score', 'common_flag',
        'StreetName_score', 'StreetNamePostType_score', 'AddressNumber_score',
        'ZipCode_score', 'dist_score'])
scores=out.iloc[:,56:]

# save matched/unmatched retailers separately
merge_df.loc[merge_df['FDA_match']==True,:].to_csv('step_3_work/output/matched_retailers.csv', index = False)
merge_df.loc[merge_df['FDA_match']==False,:].to_csv('step_3_work/output/new_retailers.csv', index = False)


    # ----- Obsolete code -----
    # tried distance comparison, did not do a good job identifying matches

    # find closest fda retailer for each PoS retailer
    #for i in range(30):
    #
    # for i in range(len(pos_df)):
    #     fda_coord = fda_df.Coordinates
    #     pos_cand = pos_df['Coordinates'][i]
    #     fda_dist = fda_coord.distance(pos_cand)
    #     # for those very close, we will flag as a possible match
    #     # distance is in degrees
    #     # .0001 degrees is about .25 mile
    #     pos_df.loc[i,'FDA_dist'] = min(fda_dist)
    #     if min(fda_dist) < .0001:
    #         pos_df.loc[i,'FDA_match'] = 'Yes'
    #
    # # merge data back together to see how Nielsen and possible matches compare
    # merge_df = pos_df.merge(fda_df[['IMPAQ_ID', 'DBA Name' ,'Address Line 1', 'City',
    #                                 'State', 'Zip']], how='left', left_on='FDA_id',
    #                         right_on = 'IMPAQ_ID')
    #
    # merge_df = merge_df.loc[merge_df['FDA_match']!='No']
    # merge_df = merge_df.merge(
    #     niel_df, how='left', left_on='id', right_on='TDLinx Store Code'
    # )
    #
    # print(merge_df.loc[merge_df['FDA_match']=='Yes',['Store Name','DBA Name','FDA_dist']])

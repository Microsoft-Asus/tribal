# now that we have dataframe of possible matches, see what we can
# unearth about each match

# Clean up TODO: id var names need clean up, some duplicates floating around

# this file is for establishment records

import pandas as pd
pd.options.mode.chained_assignment = "raise"
import numpy as np
import urllib.request
import urllib.parse
import json
import geopandas as gp
from shapely.geometry import Point

# import some general matching functions
from functions.matching_functions import name_match_scoring as name_match
from functions.matching_functions import normalizeStreetSuffixes as norm
from functions.matching_functions import address_match_scoring as addr_match
from functions.matching_functions import match_select_agg
from functions.matching_functions import display_results


# load sample retailers and google output data
ret_df = pd.read_csv("step_0_work/output/Public retail data clean_geocoded.csv")
ret_df['est_id'] = ret_df.index.astype('int')
out_df = pd.read_pickle('./step_1_work/output/google_output.pkl')
out_df = out_df.loc[['establishment' in i for i in out_df['types']],:]

# standardize column names for name_match function
#ret_df.rename(columns={'Establishment Trade (DBA) Name':'DBA Name'}, inplace=True)
out_df.reset_index(inplace=True, drop=True)
out_df.rename(columns={'name':'bizname', 'id':'google_id', 'est_id': 'id'}, inplace=True)
out_df['id'] = out_df['id'].astype('int')
out_df['name_score'] = np.nan
out_df['common_flag'] = np.nan
out_df['inv_name_score'] = np.nan
out_df['inv_common_flag'] = np.nan
# columns for addr_match
out_df['AddressNumber_score'] = np.nan
out_df['StreetName_score'] = np.nan
out_df['StreetNamePostType_score'] = np.nan
out_df['ZipCode_score'] = np.nan

# find matching records
merge_df = out_df
for i,j in ret_df.iterrows():
    if i in out_df['id'].values:
        # by name
        score_df = name_match(j, out_df.loc[out_df['id']==i,:])
        # update merge_df with scores
        for k in ['name_score','common_flag']:
            merge_df.loc[merge_df['id']==i, k] = score_df.loc[:,k]

        # by address
        score_df = addr_match(j, out_df.loc[out_df['id']==i,:], addr_split=False,
            full_addr ='formatted_address')

        # update merge_df with scores
        for k in ['StreetName_score', 'StreetNamePostType_score', \
                  'AddressNumber_score', 'ZipCode_score']:
            merge_df.loc[merge_df['id']==i, k] = score_df.loc[:,k]

            #merge_df.loc[(merge_df['id']==j['id']) & (merge_df['cand_id']==j['cand_id']), k] = score_df.loc[:,k].values
# generate inverse name score by comparing names in out_df to ret_df
ret_df['id'] = ret_df['est_id']
for i,j in out_df.iterrows():
    score_df = name_match(j, ret_df.loc[ret_df['id']==j['id'],:],
        fda_colname = 'bizname', sos_colname = 'DBA Name')
    score_df = score_df.rename({'name_score': 'inv_name_score', 'common_flag':'inv_common_flag'}, axis = 1)
    for k in ['inv_name_score','inv_common_flag']:
        merge_df.loc[(merge_df['id']==j['id']) & (merge_df['cand_id']==j['cand_id']), k] = score_df.loc[:,k].values

# update name_score with maximum of name_score and inverse name score
merge_df['name_score'] = merge_df[['name_score','inv_name_score']].max(axis=1)
merge_df = merge_df.merge(ret_df[['id', 'DBA Name','Full Address','Longitude','Latitude']], how ='left', on = 'id')
merge_df['id'] = merge_df['id'].astype('int')
# keep best match
# in case of ties, take first record with max score
max=merge_df.groupby('id').name_score.max()
max = max.rename('name_score_max')
idmax=merge_df.groupby('id').name_score.idxmax()
idmax=idmax.rename('name_wheremax')
merge_df = merge_df.merge(pd.DataFrame(max), how = 'left', left_on = 'id', right_index=True)
merge_df = merge_df.merge(pd.DataFrame(idmax), how = 'left', left_on = 'id', right_index=True)
merge_df = merge_df.loc[merge_df['name_wheremax']==merge_df.index]
merge_df['match']= np.where((merge_df['name_score']==merge_df['name_score_max']) \
    & ((merge_df['name_score']>.9) | ((merge_df['StreetName_score']>=1) & \
    (merge_df['ZipCode_score']>=1) )) \
    & (merge_df['name_wheremax']==merge_df.index), \
    'Active','Not Validated')

# second stage of matching based off of distance
# calculate distance between rejected matches
merge_df['fda_coord'] = list(zip(merge_df.Longitude, merge_df.Latitude))
merge_df['fda_coord'] = merge_df['fda_coord'].apply(Point)
merge_df['ggl_coord'] = list(zip(merge_df['geometry.location.lng'], merge_df['geometry.location.lat']))
merge_df['ggl_coord'] = merge_df['ggl_coord'].apply(Point)
# multiply by 65.32411155 to make geodist into miles
dist = pd.Series()
for i,j in zip(merge_df['ggl_coord'],merge_df['fda_coord']):
    dist = dist.append(pd.Series(i.distance(j) * 65.32411155))
merge_df['dist_miles'] = dist.reset_index(drop = True)

# of those not matched, those with any name similarity and close proximity to
# original FDA store should be accepted as matches
merge_df.loc[(merge_df['dist_miles']<10) & (merge_df['name_wheremax']==merge_df.index) \
    & (merge_df['name_score']>.02), 'match'] = 'Active'


# check if any are permanently_closed. If not, we need to add a column marking
# all as False
if 'permanently_closed' not in merge_df.columns:
    merge_df['permanently_closed']= False
merge_df['match']= np.where((merge_df['permanently_closed']== True) & (merge_df['match'] == 'Active'), 'Closed',merge_df['match'])

ret_df = ret_df.merge(merge_df[['id', 'match']], how='left', on = 'id')
ret_df.to_pickle('./step_1_work/output/stores_est.pkl')
ret_df.to_csv('./step_1_work/output/stores_est.csv')
merge_df.to_csv('./step_1_work/output/documentation/google_places_output.csv', index=False)

# for those stores with establishment matches, compare/update address and DBA name

import pandas as pd
import numpy as np
import string
from functions.manual_functions import set_blists_1e
from functions.manual_functions import accept_match_1e

ret_df = pd.read_csv('step_1_work/output/retailers_for_manual_verify_complete.csv')
ggl_df = pd.read_csv('step_1_work/output/documentation/google_places_output.csv')
ggl_df = ggl_df.rename({'id':'est_id'},axis = 1)

# get est_ids to manually accept matches of
wlist_ids = accept_match_1e()
ggl_df.loc[[i in wlist_ids for i in ggl_df['est_id'].values.tolist()], 'match'] = 'Active'
ggl_df['match']= np.where((ggl_df['permanently_closed']== True) \
    & (ggl_df['match'] == 'Active'), 'Closed', ggl_df['match'])

# see if we can find anything from manual examiniation of remaining  non-matches in google data
compar_cols = ['est_id','DBA Name','bizname','Full Address','formatted_address', 'name_score',
    'AddressNumber_score','StreetName_score','StreetNamePostType_score',
    'ZipCode_score','dist_miles']
ggl_df.loc[ggl_df['match']=='Not Validated',compar_cols].to_csv( \
    'step_1_work/output/google_rejected_matches.csv', index = False)

# get part of df with those with determined establishments
df = ret_df.merge(ggl_df.loc[:, [i not in ['DBA Name','id','Full Address'] for i in ggl_df.columns]],
    how='inner', on='est_id')

df = df.loc[['establishment' in i for i in df['types']],:]
df = df.loc[((df['match']=='Active')|(df['match']=='Closed'))]
df = df.reset_index(drop=True)

# make sure google name is all caps
df ['bizname'] = df['bizname'].str.upper()
df ['DBA Name'] = df['DBA Name'].str.upper()

# Make sure all biznames from Google Places findings are in DBA name in FDA list
# split by spaces
fda_split=df.loc[:, 'DBA Name'].str.split(pat=" ", expand=True)
ggl_split=df.loc[:, 'bizname'].str.split(pat=" ", expand=True)

# clear out punctuation marks
translator = str.maketrans('', '', string.punctuation)
def punc_rm(s):
    if s!=None:
        return(str(s).translate(translator))
fda_split=fda_split.applymap(punc_rm)
ggl_split=ggl_split.applymap(punc_rm)

# do a comparison of words in the two names
match_df = pd.DataFrame(columns=ggl_split.columns, index=ggl_split.index)
for i,j in ggl_split.iterrows():
    def match_words(from_str, to_series=fda_split.iloc[i,:]):
        if from_str== None:
            return(np.nan)
        elif from_str in [i for i in to_series]:
            return(0)
        else:
            return(1)
    match_df.iloc[i,:] = j.apply(match_words)
match_df['sum'] = match_df.sum(axis=1, skipna=True)

# don't need to update those with same words
df['name_update'] = df['bizname']
df.loc[match_df['sum']==0,'name_update'] = np.nan

# duplicates in ggl_df indicate that the Google has a less specific name than
# existing database
df.loc[df['bizname'].duplicated(),'name_update'] = np.nan


# some words that don't seem to get the right place from looking at comparison list
# this is a manually tailored list, and should be updated with each unique run
blists = set_blists_1e()
ggl_blist = blists[0]
fda_blist = blists[1]
df.loc[df['bizname'].str.contains(ggl_blist,regex=True),'name_update'] = np.nan
df.loc[df['DBA Name'].str.contains(fda_blist,regex=True),'name_update'] = np.nan

# csv for comparing biz names that have extra words in ggl df
df.loc[~df['name_update'].isna(),['bizname','DBA Name']].to_csv('step_1_work/output/name_compare.csv', index=False)

# save updated names in original list, and merge in columns from google results
#new_cols = np.append(df.columns.values[[i not in ret_df.columns for i in df.columns]],'est_id')
ret_df = ret_df.merge(df[['est_id','name_update']], how='left', on='est_id')

# updating addresses
# may or may not mean I have to look at names again?

# flag non identical addresses
df['addr_diff'] = 0
for i in ['AddressNumber_score','StreetName_score','StreetNamePostType_score','ZipCode_score']:
    df.loc[df[i]<1, 'addr_diff'] = 1

# update address and geocoordinates for those non-exact addresses that
# are also somewhat close to original location
df['addr_update'] = np.nan
df['lat_update'] = np.nan
df['lon_update'] = np.nan
df.loc[(df['addr_diff'] == 1) & (df['dist_miles']<10), 'addr_update'] = \
    df.loc[(df['addr_diff'] == 1) & (df['dist_miles']<10), 'formatted_address']
df.loc[(df['addr_diff'] == 1) & (df['dist_miles']<10), 'lat_update'] = \
    df.loc[(df['addr_diff'] == 1) & (df['dist_miles']<10), 'geometry.location.lat']
df.loc[(df['addr_diff'] == 1) & (df['dist_miles']<10), 'lon_update'] = \
    df.loc[(df['addr_diff'] == 1) & (df['dist_miles']<10), 'geometry.location.lng']

# output csv for doing an address comparison
df.loc[(df['addr_diff'] == 1) & (df['dist_miles']<10),compar_cols].to_csv( \
    'step_1_work/output/addr_compare.csv', index = False)

# merge in the updates, and note where we can't update
ret_df = ret_df.merge(df[['est_id','addr_update','lat_update', 'lon_update','match']], how='left', on='est_id')
ret_df['match'] = ret_df['match'].fillna("Can't Validate")
# update operation status based on manual coding
ret_df.loc[ret_df['Manual Result']=='yes', 'match'] = 'Active'

# make new columns combining old and new updates
ret_df['DBA Name_update'] = ret_df['DBA Name']
ret_df['Full Address_update'] = ret_df['Full Address']
ret_df['Latitude_update'] = ret_df['Latitude']
ret_df['Longitude_update'] = ret_df['Longitude']
ret_df['DBA Name_update'].update(ret_df['name_update'])
ret_df['Full Address_update'].update(ret_df['addr_update'])
ret_df['Latitude_update'].update(ret_df['lat_update'])
ret_df['Longitude_update'].update(ret_df['lon_update'])

# fill in blanks with labels
for i in ['name_update', 'addr_update', 'lat_update', 'lon_update']:
    ret_df.loc[ret_df['match']=="Can't Validate",i] = \
        ret_df.loc[ret_df['match']=="Can't Validate",i].fillna("Can't Validate")
    ret_df.loc[ret_df['match']!="Can't Validate",i] = \
        ret_df.loc[ret_df['match']!="Can't Validate",i].fillna('Correct')

ret_df = ret_df.rename({'match':'biz_status'}, axis=1)
ret_df = ret_df.drop(columns='id')


# output FDA csv with updated names, addresses and geocoordinates
ret_df.to_csv('step_1_work/output/retailers_name_addr_update.csv', index=False)

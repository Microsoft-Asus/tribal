# reformat the list of new tribal retailers identifed from POS data
# then append to the FDA list of retailers for step #4: finding the owners
import pandas as pd
import numpy as np
import usaddress as usa
import re

# load new file, existing FDA list
df = pd.read_csv('step_3_work/output/new_retailers.csv')
fda_df = pd.read_csv('step_2_work/tribal_retailers.csv')

# flag whether each retailer is from the original list or from POS data
fda_df['ori_flg'] = 'From Original List'
df['ori_flg'] = 'New Retailer'
df['biz_status'] = 'Active'
# create id var that picks up at end of FDA ID's
df['IMPAQ_ID'] = pd.Series(range(fda_df['IMPAQ_ID'].max()+1, \
    len(df) + fda_df['IMPAQ_ID'].max()+1))
df = df.rename({'Owner State ':'Owner State'}, axis=1)
# add new columns in fda data
for i in ['Owner Name', 'Owner City','Owner State', 'Non-Corporate Owned', \
          'Niel_id']:
     fda_df[i] = np.nan

# create mapping of nielsen data vars to fda list data vars
var_map= {
    'paddress1':'Address Line 1',
    'pcity':'City',
    'pstate':'State',
    'pzip':'Zip',
    'bizname':'DBA Name_update',
    'address':'Full Address_update',
    'lat':'Latitude_update',
    'lon':'Longitude_update'
}

df = df.rename(var_map, axis = 1)

cols = ['IMPAQ_ID', 'Address Line 1', 'City', 'State', 'Zip', 'biz_status',
    'DBA Name_update', 'Full Address_update', 'Latitude_update',
    'Longitude_update', 'Coordinates', 'On Tribe Land', 'Assoc Tribe',
    'Assoc Res', 'ori_flg', 'Owner Name', 'Owner City','Owner State',
    'Non-Corporate Owned','Niel_id']

merge_df = fda_df.append(df.loc[:,cols], ignore_index=True, sort=False)

# split up updated address into commesurate components
# first,attempt to apply usaddress tagging
def try_tag(str_in):
    s = str_in[:-5] + str_in[-5:].replace(', USA','').replace(' USA','')
    try:
        tag = usa.tag(s)
        city = tag[0]['PlaceName']
        state = tag[0]['StateName']
        zip_code = tag[0]['ZipCode']
        address = ' '.join(tag[0].values()).replace(city,'').replace(state,'').replace(zip_code,'').strip()
        return pd.Series([address, city, state, zip_code])
    except:
        return pd.Series(['', '', '',''])
addrs = merge_df['Full Address_update'].apply(try_tag)
miss_ids = addrs.loc[addrs[0] == '',:].index
miss_df = merge_df.loc[addrs.loc[addrs[0] == '',:].index]
addrs = addrs.loc[addrs[0] != '',:]

# manual fix for those that don't tag
def addr_split(str_in):
    # strip out 'USA'
    s = str_in[:-5] + str_in[-5:].replace(', USA','').replace(' USA','')
    #s= re.sub(' +', ' ',s)
    # mess around with fixing bad zip code formats
    zip_code = s[-5:]
    if zip_code == '6382.':
        zip_code = '06832'
    if zip_code == ' 6339':
        zip_code = ' 06339'
    if zip_code == ' 6382':
        zip_code = ' 06832'
    s = s[:-5] + zip_code
    assert s[-5:].isnumeric(), zip_code + ' is not a numeric zip code'
    zip_code = s[-5:]

    # extract state and mess around with format
    state = s[-8:-6]
    if s[-7]==',':
        state = s[-9:-7]
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    assert state in states, state + " is not a state code"

    # extract city
    # note when city ends based on state position
    city_end = s.find(state) - 2

    # start of city is a bit ambiguous; some are delimited by '  ', some ', '
    find_delim = [m.start() for m in re.finditer(', ', s)]
    find_delim2 = [m.start() for m in re.finditer('  ', s)]
    find_delim3 = [0] + [m.start() for m in re.finditer(' ', s)]
    # There's always at least one ", " instance for city -> state delimiter
    # we'll count number of instances of ", " delimiter to see whether to check
    # for a ", " or a "  " delimiter for the start of the city
    if len(find_delim2)>0:
        city_start = find_delim2[-1]
    else:
        city_start = find_delim[0]
        # # if neither delimiter exists, we'll just take the next word
        # except:
        #     # fix zip codes that are in cities with two+ words
        #     if zip_code == '92264' or zip_code == '86426' or zip_code == '57770' or zip_code == '57625':
        #         city_start = find_delim3[-4]
        #     else:
        #         city_start = find_delim3[-3]

    city = s[city_start:city_end].replace(', ','')

    # save rest of address line
    address = s[0:city_start]
    return pd.Series([address, city, state, zip_code])

miss_addrs = miss_df['Full Address_update'].apply(addr_split)
# still a handful of stragglers to fix manually
miss_addrs.loc[104,1] = 'Keams Canyon'
miss_addrs.loc[990,1] = 'Torreon'
miss_addrs.loc[1467,0] = '502 N Hwy 18 Or S Price Ave'
miss_addrs.loc[1467,1] = 'Chandler'

# add to addrs dataframe
addrs = addrs.append(miss_addrs)
addrs.columns = ['Address Line 1_update','City_update', 'State_update','Zip_update']

# merge with master list
merge_df = merge_df.join(addrs)

# a couple of addresses are blank, want to revert address update for those
merge_df.loc[merge_df['City_update'] == '','addr_update'] = 'Correct'

# make fields all caps to make sure we can compare correctly to original
merge_df.City_update = merge_df.City_update.str.upper()
merge_df['Address Line 1_update'] = merge_df['Address Line 1_update'].str.upper()

# make sure those marked as correct or not validated don't change
merge_df.loc[(merge_df['addr_update'] == 'Correct') | (merge_df['addr_update'] == "Can't Validate"),'Address Line 1_update'] = \
    'No changes'
merge_df.loc[(merge_df['addr_update'] == 'Correct') | (merge_df['addr_update'] == "Can't Validate"),'City_update'] = \
    'No changes'
merge_df.loc[(merge_df['addr_update'] == 'Correct') | (merge_df['addr_update'] == "Can't Validate"),'State_update'] = \
    'No changes'
merge_df.loc[(merge_df['addr_update'] == 'Correct') | (merge_df['addr_update'] == "Can't Validate"),'Zip_update'] = \
    'No changes'

merge_df.loc[(merge_df['addr_update'] == 'Correct') | (merge_df['addr_update'] == "Can't Validate"),'Full Address_update'] = \
    merge_df.loc[(merge_df['addr_update'] == 'Correct') | (merge_df['addr_update'] == "Can't Validate"),'Address Line 1'] + ' ' + \
    merge_df.loc[(merge_df['addr_update'] == 'Correct') | (merge_df['addr_update'] == "Can't Validate"),'City'] + ', ' + \
    merge_df.loc[(merge_df['addr_update'] == 'Correct') | (merge_df['addr_update'] == "Can't Validate"),'State'] + ' ' + \
    merge_df.loc[(merge_df['addr_update'] == 'Correct') | (merge_df['addr_update'] == "Can't Validate"),'Zip'].apply(str)

# make zip codes strings and add leading 0's
merge_df['Zip'] = merge_df['Zip'].apply(str)
merge_df.loc[(merge_df['Zip'].apply(lambda x: len(str(x)))==4),'Zip'] = '0' + \
    merge_df.loc[(merge_df['Zip'].apply(lambda x: len(str(x)))==4),'Zip']
merge_df.loc[(merge_df['Zip_update'].apply(lambda x: len(str(x)))==4),'Zip_update'] = '0' + \
    merge_df.loc[(merge_df['Zip_update'].apply(lambda x: len(str(x)))==4),'Zip_update']

# merge original county back into data
ori_df = pd.read_excel('input/Public retail data_original.xlsx',dtype='str')
merge_df = merge_df.merge(ori_df[['County']],how='left',right_index=True,left_on='IMPAQ_ID')

# save csv for FCC query
merge_df.loc[merge_df['Longitude_update'].isna() == False,
    ['IMPAQ_ID','Longitude_update','Latitude_update']].to_csv(
    'step_3_work/output/List_for_FCC_query.csv', index= False)

# Load the FCC query results
fcc_df = pd.read_csv('step_3_work/output/FCC_query_output.csv')

merge_df = merge_df.merge(fcc_df[['IMPAQ_ID','County_update']], how='left',on='IMPAQ_ID')
merge_df.County_update = merge_df.County_update.str.upper()
# update County according to whether we accpeted the address modification or not
merge_df.loc[((merge_df['addr_update'] == 'Correct') | (merge_df['addr_update'] == "Can't Validate")) &  \
    (merge_df['County'].isna() == False) & (merge_df['County'] != 'nan'),'County_update'] = \
     merge_df.loc[((merge_df['addr_update'] == 'Correct')  | (merge_df['addr_update'] == "Can't Validate"))& \
    (merge_df['County'].isna() == False),'County'].apply(str)

# delineate orig/update/clean columns more clearly:
# orig: old value
# changes: if old value unchanged 'No changes', else new value
# update:  if old value unchanged old value, else new value

# some _update columns at this point are correctly specified. We will create _changes vars for those missing it
for i in ['County']:
    merge_df[i+'_changes'] = merge_df[i+'_update']
    merge_df.loc[merge_df[i+'_changes'] == merge_df[i+'_update'], i+'_changes'] = 'Correct'
    merge_df.loc[merge_df['biz_status'] == "Can't Validate", i+'_changes'] = "Can't Validate"

# some update columns need to be renamed as changes
merge_df = merge_df.rename({'name_update':'DBA Name_changes',
    'addr_update':'Full Address_changes',
    'name_update':'DBA Name_changes',
    'lat_update':'Latitude_changes',
    'lon_update':'Longitude_changes',
    'Address Line 1_update':'Address Line 1_changes',
    'City_update':'City_changes',
    'State_update':'State_changes',
    'Zip_update':'Zip_changes'},axis=1)

# some update vars need to be created
for i in ['Address Line 1','City','State','Zip']:
    merge_df[i+'_update'] = merge_df[i+'_changes']
    merge_df.loc[merge_df[i+'_changes'] == 'Correct', i+'_update'] = \
        merge_df.loc[merge_df[i+'_changes'] == 'Correct', i]
    merge_df.loc[merge_df[i+'_changes'] == "Can't Validate", i+'_update'] = \
        merge_df.loc[merge_df[i+'_changes'] == "Can't Validate", i]
    merge_df.loc[merge_df[i+'_changes'] == "No changes", i+'_update'] = \
        merge_df.loc[merge_df[i+'_changes'] == "No changes", i]
    # make sure _changes vars read no changes/can't validate correctly
    merge_df.loc[merge_df[i+'_update'] == merge_df[i], i+'_changes'] = 'Correct'
    merge_df.loc[merge_df['biz_status'] == "Can't Validate", i+'_changes'] = "Can't Validate"

# add in biz_status, on tribe land original, _changes and _update columns
merge_df=merge_df.rename({'biz_status':'Business Status_update','On Tribe Land':'On Tribe Land_update'},axis=1)
ori_df = pd.read_excel('input/Public retail data_original.xlsx',dtype='str')
ori_df['IMPAQ_ID'] = ori_df.index
merge_df = merge_df.merge(ori_df[['IMPAQ_ID','Business Status','On Tribe Land']],how='left',on='IMPAQ_ID')
merge_df['Business Status_changes']=merge_df['Business Status_update']
merge_df['On Tribe Land_changes']=merge_df['On Tribe Land_update']
# clean up biz status values
merge_df['Business Status_update']=merge_df['Business Status_update'].replace('Active','In Operation')
merge_df['Business Status_changes']=merge_df['Business Status_changes'].replace('Active','In Operation')
merge_df['Business Status_update']=merge_df['Business Status_update'].replace('Closed','Out of Business')
merge_df['Business Status_changes']=merge_df['Business Status_changes'].replace('Closed','Out of Business')

# alter the update and changes columns to be consistent with others
merge_df.loc[merge_df['Business Status']==merge_df['Business Status_update'],
    'Business Status_changes']='No changes'
merge_df.loc[merge_df['On Tribe Land']==merge_df['On Tribe Land_update'],
    'On Tribe Land_changes']='No changes'
merge_df.loc[merge_df['Business Status_update']=="Can't Validate",
    'Business Status_changes']="Can't Validate"
merge_df.loc[merge_df['On Tribe Land_update']=="Can't Validate",
    'On Tribe Land_changes']="Can't Validate"
merge_df.loc[merge_df['Business Status_update']=="Can't Validate",
    'Business Status_update']=merge_df.loc[merge_df['Business Status_update']==
    "Can't Validate",'Business Status']
merge_df.loc[merge_df['On Tribe Land_update']=="Can't Validate",
    'On Tribe Land_update']=merge_df.loc[merge_df['On Tribe Land_update']==
    "Can't Validate",'On Tribe Land']

# clean up the order of vars
column_names=['DBA Name','Address Line 1','City','State','Zip',
	'Latitude','Longitude','Full Address','County','Business Status','On Tribe Land']
cols =[]
for i in column_names:
    cols += [i,i+'_changes',i+'_update']
rest_cols = [i for i in merge_df.columns if i not in cols]
merge_df = merge_df[cols + rest_cols]
rest_cols = [i for i in merge_df.columns if i != 'IMPAQ_ID']
merge_df = merge_df[['IMPAQ_ID']+rest_cols]

# save to CSV
merge_df.to_csv('step_3_work/output/full_retailer_list_orig.csv', index= False)

# create sample of 100 new retailers for LexisNexis trial batch
merge_df.loc[merge_df['ori_flg']=='New Retailer', \
    ['IMPAQ_ID','DBA Name_update','Full Address_update','Latitude_update', \
    'Longitude_update']].sample(100,random_state=124).to_csv( \
    'step_3_work/output/Lexis_retailer_sample.csv', index= False)

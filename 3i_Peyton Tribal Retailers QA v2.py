#!/usr/bin/env python
# coding: utf-8

# In[2]:


# %load \\afsv03\Research\FDA\2732 - FDA Tribal Tobacco Retailers\Technical\Tribal_Master\3i_manual_list_changes.py
# some manual changes to full_retailer_list.csv
import pandas as pd

df=pd.read_csv('step_3_work/output/full_retailer_list_orig.csv')

# 7 retailers have shifted states; going to overwrite these values
# columns
impaq_ids = [13,54,379,569,751,1586]
update_rows = df['IMPAQ_ID'].apply(lambda x: x in impaq_ids)
change_cols = [i for i in df.columns if '_changes' in i]
update_cols = [i for i in df.columns if '_update' in i]
other_cols = ['Coordinates', 'On Tribe Land', 'Miles to Nearest Tribe',
    'Assoc Tribe', 'Assoc Res', 'Nearest Tribe', 'Nearest Res','biz_status']

df.loc[update_rows , change_cols] = "Can't validate"
for i in update_cols:
    orig_var = i.replace('_update','')
    df.loc[update_rows, i] = df.loc[update_rows, orig_var]
df.loc[update_rows , other_cols] = "Can't validate"

# this line creates a new blank column called 'Manual Validation Flag'
df['Manual Validation Flag'] = ''

# For records we should override, change this column's value to "Can't validate"
# also remember to add brief notes explaining why, for example:

# matched store is out of state, removing match
df.loc[13, "Manual Validation Flag"] = "Can't validate"
# matched store is out of state, removing match
df.loc[38, "Manual Validation Flag"] = "Can't validate"
# matched store is out of state, removing match
df.loc[54, "Manual Validation Flag"] = "Can't validate"
# Matched store has difference in Latitude, removing match
df.loc[59, "Manual Validation Flag"] = "Can't validate"
# Matched store has difference in Latitude and Longitude, removing match 
df.loc[65, "Manual Validation Flag"] = "Can't validate"
# Matched store has difference in Latitude and Longitude, removing match
df.loc[104, "Manual Validation Flag"] = "Can't validate"
# Matched store has difference in Latitude, removing match
df.loc[128, "Manual Validation Flag"] = "Can't validate"
# Matched store has difference in Latitude, removing match
df.loc[132, "Manual Validation Flag"] = "Can't validate"
# Matched store has difference in Longitude and Latitude
df.loc[222, "Manual Validation Flag"] = "Can't validate"
# Can't find the original DBA_Name when using the original address 
df.loc[341, "Manual Validation Flag"] = "Can't validate"
# Original and _update store are both their own seperate stores
df.loc[351, "Manual Validation Flag"] = "Can't validate"
# matched store is out of state, removing match 
df.loc[379, "Manual Validation Flag"] = "Can't validate"
# Difference in Longitude
df.loc[498, "Manual Validation Flag"] = "Can't validate"
# Matched store has difference in Longitude and Latitude
df.loc[517 , "Manual Validation Flag"] = "Can't validate"
# matched store is out of state, removing match
df.loc[751, "Manual Validation Flag"] = "Can't validate"
## Matched store has difference in Latitude 
df.loc[989, "Manual Validation Flag"] = "Can't validate"
# Matched store has difference in Longitude and Latitude 
df.loc[1001, "Manual Validation Flag"] = "Can't validate"
# Matched store has difference in Longitude 
df.loc[1047, "Manual Validation Flag"] = "Can't validate"
# Matched store is located far from original store location
df.loc[1103, "Manual Validation Flag"] = "Can't validate"
# Matched store is located far from original store location 
df.loc[1218, "Manual Validation Flag"] = "Can't validate"
# Matched store has difference in Longitude  
df.loc[1325, "Manual Validation Flag"] = "Can't validate"


#df.loc[, "Manual Validation Flag"] = "Can't validate"

# df.loc[13, "DBA Name_update"] = "Can't validate"
# df.loc[13, "Address Line1_update"] = "Can't validate"
# df.loc[13, "Latitude_update"] = "Can't validate"
# df.loc[13, "Longitude_update"] = "Can't validate"
# df.loc[13, "biz_status"] = "Can't validate"
#
# df.loc[38, "DBA Name_update"] = "Can't validate"
# df.loc[38, "Address Line1_update"] = "Can't validate"
# df.loc[38, "Latitude_update"] = "Can't validate"
# df.loc[38, "Longitude_update"] = "Can't validate"
# df.loc[38, "biz_status"] = "Can't validate"
#
# df.loc[54, "DBA Name_update"] = "Can't validate"
# df.loc[54, "Address Line1_update"] = "Can't validate"
# df.loc[54, "Latitude_update"] = "Can't validate"
# df.loc[54, "Longitude_update"] = "Can't validate"
# df.loc[54, "biz_status"] = "Can't validate"
#
# df.loc[59, "DBA Name_update"] = "Can't validate"
# df.loc[59, "Address Line1_update"] = "Can't validate"
# df.loc[59, "Latitude_update"] = "Can't validate"
# df.loc[59, "Longitude_update"] = "Can't validate"
# df.loc[59, "biz_status"] = "Can't validate"
#
# df.loc[65, "DBA Name_update"] = "Can't validate"
# df.loc[65, "Address Line1_update"] = "Can't validate"
# df.loc[65, "Latitude_update"] = "Can't validate"
# df.loc[65, "Longitude_update"] = "Can't validate"
# df.loc[65, "biz_status"] = "Can't validate"
#
# df.loc[104, "DBA Name_update"] = "Can't validate"
# df.loc[104, "Address Line1_update"] = "Can't validate"
# df.loc[104, "Latitude_update"] = "Can't validate"
# df.loc[104, "Longitude_update"] = "Can't validate"
# df.loc[104, "biz_status"] = "Can't validate"
#
# df.loc[128, "DBA Name_update"] = "Can't validate"
# df.loc[128, "Address Line1_update"] = "Can't validate"
# df.loc[128, "Latitude_update"] = "Can't validate"
# df.loc[128, "Longitude_update"] = "Can't validate"
# df.loc[128, "biz_status"] = "Can't validate"
#
# df.loc[132, "DBA Name_update"] = "Can't validate"
# df.loc[132, "Address Line1_update"] = "Can't validate"
# df.loc[132, "Latitude_update"] = "Can't validate"
# df.loc[132, "Longitude_update"] = "Can't validate"
# df.loc[132, "biz_status"] = "Can't validate"
#
# df.loc[172, "DBA Name_update"] = "Can't validate"
# df.loc[172, "Address Line1_update"] = "Can't validate"
# df.loc[172, "Latitude_update"] = "Can't validate"
# df.loc[172, "Longitude_update"] = "Can't validate"
# df.loc[172, "biz_status"] = "Can't validate"
#
# df.loc[195, "DBA Name_update"] = "Can't validate"
# df.loc[195, "Address Line1_update"] = "Can't validate"
# df.loc[195, "Latitude_update"] = "Can't validate"
# df.loc[195, "Longitude_update"] = "Can't validate"
# df.loc[195, "biz_status"] = "Can't validate"


df.to_csv('step_3_work/output/full_retailer_list.csv')


# In[ ]:

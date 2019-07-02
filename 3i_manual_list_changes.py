# some manual changes to full_retailer_list.csv
import pandas as pd

df=pd.read_csv('step_3_work/output/full_retailer_list_orig.csv')

# 7 retailers have shifted states; going to overwrite these values
# columns
cols = ['DBA Name_update', 'Full Address_update', 'Latitude_update',
    'Longitude_update', 'Address Line 1_update', 'City_update', 'State_update',
    'Zip_update', 'County_update']

impaq_ids = [0,13,54,379,569,751,1586]
update_rows = df['IMPAQ_ID'].apply(lambda x: x in impaq_ids)
update_cols = [i for i in cols if '_update' in i]
other_cols = ['Coordinates', 'On Tribe Land', 'Miles to Nearest Tribe',
    'Assoc Tribe', 'Assoc Res', 'Nearest Tribe', 'Nearest Res','biz_status']

df.loc[update_rows , update_cols] = 'No changes'
df.loc[update_rows , other_cols] = "Can't validate"






# NEXT PART OF THE CODE SHOULD STAY AT END OF FILE
# revalidate _changes columns
column_names=['DBA Name','Address Line 1','City','State','Zip',
	'Latitude','Longitude','Full Address','County']
for i in column_names:
    df[i+'_changes'] = df[i+'_update']
    df.loc[df[i+'_changes'] == df[i+'_update'], i+'_changes'] = 'Correct'
    df.loc[df['biz_status'] == "Can't Validate", i+'_changes'] = "Can't Validate"
df.to_csv('step_3_work/output/full_retailer_list.csv')

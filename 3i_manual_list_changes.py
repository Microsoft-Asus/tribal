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

df.to_csv('step_3_work/output/full_retailer_list.csv')

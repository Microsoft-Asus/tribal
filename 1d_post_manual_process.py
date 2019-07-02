# after manual coding of pics, finalize determinations
import pandas as pd
import numpy as np

df = pd.read_csv('step_1_work/output/retailers_for_manual_verify_coded_v2.csv')

# fix some inconsistent manual reporting
df['Manual Result'] = df['Manual Result'].str.replace('Yes','yes')
df['Manual Result'] = df['Manual Result'].str.replace('maybe ','maybe')

# update match corresponding to manual determination
# skipping this as the "match" column has changed from when the manual check
# was performed
df = df.drop(columns='match')
# df['match'].update(df['Manual Result'])
# df['match'] = df['match'].str.replace('yes','Active')
# df['match'] = df['match'].str.replace('maybe','Not Validated')
# df['match'] = df['match'].str.replace('no','Not Validated')
# df['match'] = df['match'].str.replace('Manually Verify Pic','Not Validated')

# clean up columns and export
df.to_csv('step_1_work/output/retailers_for_manual_verify_complete.csv', index = False)

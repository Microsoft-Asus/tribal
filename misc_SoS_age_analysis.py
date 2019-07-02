# analyze how old SoS documents are
import pandas as pd

df = pd.read_csv('step_4_work/output/full_retailer_list_w_owner_final.csv')
df = df.loc[df['Latest Year of Ownership Docs'].isna() == False]
df = df.loc[df['Latest Year of Ownership Docs'] != 'Unknown']
df = df.loc[df['biz_status']=='Active']
df = df.loc[df['DBA Name_update']!='7 ELEVEN']
df = df.loc[df['DBA Name_update']!='DOLLAR TREE']
df = df.loc[df['DBA Name_update']!='CHEVRON']
df = df.loc[df['DBA Name_update']!='76 GAS STATION']
df = df.loc[df['DBA Name_update']!='CVS PHARMACY']
df['age'] = 2019 - df['Latest Year of Ownership Docs'].astype('int')
print(df['age'].mean())

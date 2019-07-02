# Preliminary FDA list cleaning
import pandas as pd
import unicodedata

# load in retailers data
df = pd.read_csv("./input/Public retail data.csv", encoding='latin-1')

# create full address column
df['Full Address'] = df ['Address Line 1'] + ' ' + df['Address Line 2'].fillna('') \
    + ' ' + df['City'] + ', ' + df['State'] + ' ' + df['Zip'].astype('str')

# replace latin characters with ascii characters
for i in ['DBA Name','Address Line 1', 'Full Address', 'City']:
    df[i] =df[i].apply(lambda s: str(unicodedata.normalize('NFKD',s).encode('ascii','replace'))).str[2:-1]
    df[i] =df[i].apply(lambda s: str(unicodedata.normalize('NFKD',s).encode('ascii','strict'))).str[2:-1]
    # remove ? characters from unicodedata encoding
    df[i] = df[i].str.replace('?','',regex=False)

# save revised csv
df.to_csv("step_0_work/output/Public retail data clean.csv", index=False)

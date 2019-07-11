# compile results of all scrapers
import pandas as pd
full_df = pd.read_csv('step_4_work/output/full_retailer_list_w_owner.csv')
# columns to be added
full_df['SoS_record'] = ''
full_df['Latest Year of Ownership Docs'] = ''

# Arizona results
# has both screenshots and documents
AZ_df = pd.read_csv('C:/Users/lpatterson/AnacondaProjects/Tribal_Master/step_4_work/' +
    'AZ/AZ_FDA_matches.csv',dtype='str')
docs_df = pd.read_csv('C:/Users/lpatterson/AnacondaProjects/Tribal_Master/step_4_work/' +
    'AZ/AZ_docs_found.csv',dtype='str')
AZ_df = AZ_df.merge(docs_df[['IMPAQ_ID','doc_date']], how='left', on='IMPAQ_ID')
AZ_df.index = AZ_df.IMPAQ_ID.astype('int')
AZ_df = AZ_df[['SoS_record','entity','agent_name', 'agent_address', 'agent_city',
    'agent_state', 'agent_zip','doc_date']]
AZ_df = AZ_df.rename({'doc_date':'Latest Year of Ownership Docs'}, axis=1)
full_df.update(AZ_df)

# California results
# has both screenshots and documents
ca_df = pd.read_csv('C:/Users/lpatterson/AnacondaProjects/Tribal_Master/step_4_work/' +
    'CA/CA_FDA_matches.csv',dtype='str')
docs_df = pd.read_csv('C:/Users/lpatterson/AnacondaProjects/Tribal_Master/step_4_work/' +
    'CA/CA_docs_found.csv',dtype='str')
ca_df = ca_df.merge(docs_df[['IMPAQ_ID','doc_date']], how='left', on='IMPAQ_ID')
ca_df.index = ca_df.IMPAQ_ID.astype('int')
ca_df = ca_df[['SoS_record','entity','agent_name', 'agent_address', 'agent_city',
    'agent_state', 'agent_zip','doc_date']]
ca_df = ca_df.rename({'doc_date':'Latest Year of Ownership Docs'}, axis=1)
full_df.update(ca_df)

# Oklahoma results
# only website screenshots
ok_df = pd.read_csv("C:/Users/lpatterson/AnacondaProjects/Tribal_Master/step_4_work/OK/OK_FDA_matches.csv",dtype='str')
ok_df.index = ok_df.IMPAQ_ID.astype('int')
ok_df = ok_df[['SoS_record','entity','agent_name', 'agent_address', 'agent_city',
    'agent_state', 'agent_zip']]
# can't identify year biz ownership last updated for
ok_df['Latest Year of Ownership Docs'] = 'Unknown'
full_df.update(ok_df)

# Michigan Results
# only website screenshots
MI_df = pd.read_csv("C:/Users/lpatterson/AnacondaProjects/Tribal_Master/step_4_work/MI/MI_FDA_matches.csv",dtype='str')
MI_df.index = MI_df.IMPAQ_ID.astype('int')
MI_df = MI_df[['SoS_record','entity','agent_name', 'agent_address', 'agent_city',
    'agent_state', 'agent_zip','doc_date']]
MI_df = MI_df.rename({'doc_date':'Latest Year of Ownership Docs'}, axis=1)
full_df.update(MI_df)


# Minnesota Results
# only website screenshots
MN_df = pd.read_csv("C:/Users/lpatterson/AnacondaProjects/Tribal_Master/step_4_work/MN/MN_FDA_matches.csv",dtype='str')
MN_df.index = MN_df.IMPAQ_ID.astype('int')
MN_df = MN_df[['SoS_record','entity','agent_name', 'agent_address', 'agent_city',
    'agent_state', 'agent_zip']]
# can't identify year biz ownership last updated for
MN_df['Latest Year of Ownership Docs'] = 'Unknown'
full_df.update(MN_df)

# Montana Results
# only website screenshots
MT_df = pd.read_csv("C:/Users/lpatterson/AnacondaProjects/Tribal_Master/step_4_work/MT/MT_FDA_matches.csv",dtype='str')
docs_df = pd.read_csv('C:/Users/lpatterson/AnacondaProjects/Tribal_Master/step_4_work/' +
    'MT/MT_docs_found.csv',dtype='str')
MT_df = MT_df.merge(docs_df[['IMPAQ_ID','doc_date']], how='left', on='IMPAQ_ID')
MT_df.index = MT_df.IMPAQ_ID.astype('int')
MT_df = MT_df[['SoS_record','entity','agent_name', 'agent_address', 'agent_city',
    'agent_state', 'agent_zip','doc_date']]
MT_df = MT_df.rename({'doc_date':'Latest Year of Ownership Docs'}, axis=1)
full_df.update(MT_df.drop_duplicates())

# New Mexico Results
NM_df = pd.read_csv("C:/Users/lpatterson/AnacondaProjects/Tribal_Master/step_4_work/NM/NM_FDA_matches.csv",dtype='str')
NM_df.index = NM_df.IMPAQ_ID.astype('int')
NM_df = NM_df[['SoS_record','entity','agent_name', 'agent_address', 'agent_city',
    'agent_state', 'agent_zip']]
# can't identify year biz ownership last updated for
MN_df['Latest Year of Ownership Docs'] = 'Unknown'
full_df.update(NM_df)

# NY Results
# TODO: NY documents need to be manually extracted
NY_df = pd.read_csv("C:/Users/lpatterson/AnacondaProjects/Tribal_Master/step_4_work/NY/NY_ownership_results.csv",dtype='str')
NY_df.index = NY_df.IMPAQ_ID.astype('int')
NY_df = NY_df[['SoS_record','entity','agent_name', 'agent_address', 'agent_city',
    'agent_state', 'agent_zip']]
# can't identify year biz ownership last updated for
NY_df['Latest Year of Ownership Docs'] = 'Unknown'
full_df.update(NY_df)

# South Dakota results
# has both screenshots and documents
SD_df = pd.read_csv('C:/Users/lpatterson/AnacondaProjects/Tribal_Master/step_4_work/' +
    'SD/SD_FDA_matches.csv',dtype='str')
docs_df = pd.read_csv('C:/Users/lpatterson/AnacondaProjects/Tribal_Master/step_4_work/' +
    'SD/SD_docs_found.csv',dtype='str')
SD_df = SD_df.merge(docs_df[['IMPAQ_ID','doc_date']], how='left', on='IMPAQ_ID')
SD_df.index = SD_df.IMPAQ_ID.astype('int')
SD_df = SD_df[['SoS_record','entity','agent_name', 'agent_address', 'agent_city',
    'agent_state', 'agent_zip','doc_date']]
SD_df = SD_df.rename({'doc_date':'Latest Year of Ownership Docs'}, axis=1)
full_df.update(SD_df)

# Washington results
# has both screenshots and documents
wa_df = pd.read_csv("C:/Users/lpatterson/AnacondaProjects/Tribal_Master/step_4_work/WA/WA_ownership_results.csv",dtype='str')
docs_df = pd.read_csv('C:/Users/lpatterson/AnacondaProjects/Tribal_Master/step_4_work/' +
    'WA/WA_docs_found_pt3.csv',dtype='str')
wa_df = wa_df.merge(docs_df[['IMPAQ_ID','doc_date']], how='left', on='IMPAQ_ID')
wa_df.index = wa_df.IMPAQ_ID.astype('int')
wa_df = wa_df[['SoS_record','entity','agent_name', 'agent_address', 'agent_city',
    'agent_state', 'agent_zip']]
wa_df = wa_df.rename({'doc_date':'Latest Year of Ownership Docs'}, axis=1)
full_df.update(wa_df)

# drop random duplicate column
if 'Unnamed: 0' in full_df.columns:
    full_df = full_df.drop('Unnamed: 0', axis =1)

# remove ownership determinations for manual can't validate determinations
cols = ['entity', 'agent_name', 'agent_address', 'agent_city', 'agent_state',
    'agent_zip', 'SoS_record', 'Latest Year of Ownership Docs']
for i in cols:
    full_df.loc[full_df['Manual Validation Flag']=="Can't validate",i]=''

full_df.to_csv('step_4_work/output/full_retailer_list_w_owner_final.csv', index=False)

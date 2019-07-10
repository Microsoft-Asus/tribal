# compile results of all scrapers
import pandas as pd
full_df = pd.read_csv('step_4_work/output/full_retailer_list_w_owner.csv')
# columns to be added
full_df['SoS_record'] = ''
full_df['Latest Year of Ownership Docs'] = ''

# Oklahoma results
ok_df = pd.read_csv("C:/Users/lpatterson/AnacondaProjects/Tribal_Master/step_4_work/OK/OK_FDA_matches.csv",dtype='str')
ok_df.index = ok_df.IMPAQ_ID.astype('int')
ok_df = ok_df[['SoS_record','entity','agent_name', 'agent_address', 'agent_city',
    'agent_state', 'agent_zip']]
# can't identify year biz ownership last updated for
ok_df['Latest Year of Ownership Docs'] = 'Unknown'
full_df.update(ok_df)

# Washington results
wa_df = pd.read_csv("C:/Users/lpatterson/AnacondaProjects/Tribal_Master/step_4_work/WA/WA_ownership_results.csv",dtype='str')
docs_df = pd.read_csv('C:/Users/lpatterson/AnacondaProjects/Tribal_Master/step_4_work/' +
    'WA/WA_docs_found.csv',dtype='str')
wa_df = wa_df.merge(docs_df[['IMPAQ_ID','doc_date']], how='left', on='IMPAQ_ID')
wa_df.index = wa_df.IMPAQ_ID.astype('int')
wa_df = wa_df[['SoS_record','entity','agent_name', 'agent_address', 'agent_city',
    'agent_state', 'agent_zip']]
wa_df = wa_df.rename({'doc_date':'Latest Year of Ownership Docs'}, axis=1)
full_df.update(wa_df)

# California results
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

# drop random duplicate column
if 'Unnamed: 0' in full_df.columns:
    full_df = full_df.drop('Unnamed: 0', axis =1)

full_df.to_csv('step_4_work/output/full_retailer_list_w_owner_final.csv', index=False)

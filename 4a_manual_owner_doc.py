# record manual documentation for states with too few biz to build ownership
# scrapers for
import os
import pandas as pd
import numpy as np
import xlsxwriter

# load retailer list
df = pd.read_csv('step_3_work/output/full_retailer_list.csv')

# set up dataframe to record documentation links
doc_df = df[['IMPAQ_ID']].copy()

# add ownership columns
df['entity'] = ''
df['agent_name'] = ''
df['agent_address'] = ''
df['agent_city'] = ''
df['agent_state'] = ''
df['agent_zip'] = ''
doc_df['est_entity'] = ''
doc_df['est_agent'] = ''
doc_df['est_other'] = ''
doc_df['est_latest_update'] = ''
doc_df['notes'] = ''

# Manual recording starts here
id = 2743
df.loc[id, 'entity'] = "LEASK'S MARKET, INC."
df.loc[id, 'agent_name'] = 'DANIEL LEASK'
df.loc[id, 'agent_address'] = 'P.O. BOX 67'
df.loc[id, 'agent_city'] = ' METLAKATLA'
df.loc[id, 'agent_state'] = 'AK'
df.loc[id, 'agent_zip'] = '99926'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Annual_Report.pdf", "SoS Annual Report")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Agent_Change.pdf", "SoS Agent Change Notice")'
doc_df.loc[id, 'est_other'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_latest_update'] = '2018'

id = 2617
df.loc[id, 'entity'] = 'Not Found'
df.loc[id, 'agent_name'] = 'Not Found'
df.loc[id, 'agent_address'] = 'Not Found'
df.loc[id, 'agent_city'] = 'Not Found'
df.loc[id, 'agent_state'] = 'Not Found'
df.loc[id, 'agent_zip'] = 'Not Found'
doc_df.loc[id, 'est_entity'] = 'Not Found'
doc_df.loc[id, 'est_agent'] = 'Not Found'
doc_df.loc[id, 'est_other'] = 'Not Found'
doc_df.loc[id, 'est_latest_update'] = 'Not Found'

id = 2494
df.loc[id, 'entity'] = 'AGHSBH Marketing & Distribution, LP'
df.loc[id, 'agent_name'] = "Arooga's Management, LLC"
df.loc[id, 'agent_address'] = '7025 Allentown Blvd '
df.loc[id, 'agent_city'] = 'Harrisburg'
df.loc[id, 'agent_state'] = 'PA'
df.loc[id, 'agent_zip'] = '17112'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Annual_Report.pdf", "SoS Annual Report")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Agent_Change.pdf", "SoS Agent Change Notice")'
doc_df.loc[id, 'est_other'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_latest_update'] = '2008'
doc_df.loc[id ,'notes'] = 'Ownership in different state; matched from Nielsen record'

id = 2387
df.loc[id, 'entity'] = 'BIG LOTS, INC.'
df.loc[id, 'agent_name'] = 'Corporation Service Company'
df.loc[id, 'agent_address'] = '50 WEST BROAD STREET SUITE 1330'
df.loc[id, 'agent_city'] = 'Columbus'
df.loc[id, 'agent_state'] = 'OH'
df.loc[id, 'agent_zip'] = '43215'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Agent_Change.pdf", "SoS Agent Change Notice")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Agent_Change.pdf", "SoS Agent Change Notice")'
doc_df.loc[id, 'est_other'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_latest_update'] = '2016'
doc_df.loc[id ,'notes'] = 'Ownership in different state; matched from Nielsen record'

id = 2186
df.loc[id, 'entity'] = 'Not Found'
df.loc[id, 'agent_name'] = 'CT CORPORATION SYSTEM'
df.loc[id, 'agent_address'] = '4400 EASTON COMMONS WAY SUITE 125'
df.loc[id, 'agent_city'] = 'COLUMBUS'
df.loc[id, 'agent_state'] = 'OH'
df.loc[id, 'agent_zip'] = '43219'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Agent_Change.pdf", "SoS Agent Change Notice")'
doc_df.loc[id, 'est_latest_update'] = '2017'
doc_df.loc[id ,'notes'] = 'Ownership in different state; matched from Nielsen record'

id = 2240
df.loc[id, 'entity'] = 'Not Found'
df.loc[id, 'agent_name'] = 'CT CORPORATION SYSTEM'
df.loc[id, 'agent_address'] = '4400 EASTON COMMONS WAY SUITE 125'
df.loc[id, 'agent_city'] = 'COLUMBUS'
df.loc[id, 'agent_state'] = 'OH'
df.loc[id, 'agent_zip'] = '43219'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Agent_Change.pdf", "SoS Agent Change Notice")'
doc_df.loc[id, 'est_other'] = 'None'
doc_df.loc[id, 'est_latest_update'] = '2017'
doc_df.loc[id ,'notes'] = 'Ownership in different state; matched from Nielsen record'

id = 2455
df.loc[id, 'entity'] = 'Lyons Group, LTD'
df.loc[id, 'agent_name'] = 'Patrick T Lyons'
df.loc[id, 'agent_address'] = '334 BOYLSTON ST SUITE 500'
df.loc[id, 'agent_city'] = 'Boston'
df.loc[id, 'agent_state'] = 'MA'
df.loc[id, 'agent_zip'] = '02116'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Annual_Report.pdf", "SoS Annual Report")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_other'] = 'None'
doc_df.loc[id, 'est_latest_update'] = '2018'
doc_df.loc[id ,'notes'] = 'Ownership in different state; matched from Nielsen record'

id = 2502
df.loc[id, 'entity'] = 'Lyons Group, LTD'
df.loc[id, 'agent_name'] = 'Patrick T Lyons'
df.loc[id, 'agent_address'] = '334 BOYLSTON ST SUITE 500'
df.loc[id, 'agent_city'] = 'Boston'
df.loc[id, 'agent_state'] = 'MA'
df.loc[id, 'agent_zip'] = '02116'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Annual_Report.pdf", "SoS Annual Report")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_other'] = 'None'
doc_df.loc[id, 'est_latest_update'] = '2018'
doc_df.loc[id ,'notes'] = 'Ownership in different state; matched from Nielsen record'

id = 2555
df.loc[id, 'entity'] = 'Lyons Group, LTD'
df.loc[id, 'agent_name'] = 'Patrick T Lyons'
df.loc[id, 'agent_address'] = '334 BOYLSTON ST SUITE 500'
df.loc[id, 'agent_city'] = 'Boston'
df.loc[id, 'agent_state'] = 'MA'
df.loc[id, 'agent_zip'] = '02116'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Annual_Report.pdf", "SoS Annual Report")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_other'] = 'None'
doc_df.loc[id, 'est_latest_update'] = '2018'
doc_df.loc[id ,'notes'] = 'Ownership in different state; matched from Nielsen record'

id = 2822
df.loc[id, 'entity'] = 'RPCS Inc.'
df.loc[id, 'agent_name'] = 'Randell D. Wallace'
df.loc[id, 'agent_address'] = '300 S. John Q Hammons Parkway Suite 800'
df.loc[id, 'agent_city'] = 'Springfield'
df.loc[id, 'agent_state'] = 'MO'
df.loc[id, 'agent_zip'] = '65806'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Articles_of_Incorp.pdf", "SoS Articles of Incorporation")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_other'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_latest_update'] = '2018'
doc_df.loc[id ,'notes'] = 'Ownership in different state; matched from Nielsen record'

id = 2838
df.loc[id, 'entity'] = 'RPCS Inc.'
df.loc[id, 'agent_name'] = 'Randell D. Wallace'
df.loc[id, 'agent_address'] = '300 S. John Q Hammons Parkway Suite 800'
df.loc[id, 'agent_city'] = 'Springfield'
df.loc[id, 'agent_state'] = 'MO'
df.loc[id, 'agent_zip'] = '65806'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Articles_of_Incorp.pdf", "SoS Articles of Incorporation")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_other'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_latest_update'] = '2018'
doc_df.loc[id ,'notes'] = 'Ownership in different state; matched from Nielsen record'

id = 727
df.loc[id, 'entity'] = 'Downstream Q Store, LLC'
df.loc[id, 'agent_name'] = 'Jack Brill II'
df.loc[id, 'agent_address'] = '7215 Goldfinch'
df.loc[id, 'agent_city'] = 'Neosho'
df.loc[id, 'agent_state'] = 'MO'
df.loc[id, 'agent_zip'] = '64850'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/Existing Retailers/MO490778_' +  \
    '_SoS_Articles_of_Incorp.pdf", "SoS Articles of Incorporation")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/Existing Retailers/MO490778_' +\
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_other'] = 'None'
doc_df.loc[id, 'est_latest_update'] = '2011'

id = 2906
df.loc[id, 'entity'] = 'Island Energy Services, LLC'
df.loc[id, 'agent_name'] = 'THE CORPORATION COMPANY, INC.'
df.loc[id, 'agent_address'] = '1136 UNION MALL STE 301'
df.loc[id, 'agent_city'] = 'HONOLULU'
df.loc[id, 'agent_state'] = 'HI'
df.loc[id, 'agent_zip'] = '96813'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_other'] = 'None'
doc_df.loc[id, 'est_latest_update'] = '2017'

id =2907
df.loc[id, 'entity'] = 'Island Energy Services, LLC'
df.loc[id, 'agent_name'] = 'THE CORPORATION COMPANY, INC.'
df.loc[id, 'agent_address'] = '1136 UNION MALL STE 301'
df.loc[id, 'agent_city'] = 'HONOLULU'
df.loc[id, 'agent_state'] = 'HI'
df.loc[id, 'agent_zip'] = '96813'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_other'] = 'None'
doc_df.loc[id, 'est_latest_update'] = '2017'

id = 2744
df.loc[id, 'entity'] = 'Not Found'
df.loc[id, 'agent_name'] = 'Not Found'
df.loc[id, 'agent_address'] = 'Not Found'
df.loc[id, 'agent_city'] = 'Not Found'
df.loc[id, 'agent_state'] = 'Not Found'
df.loc[id, 'agent_zip'] = 'Not Found'
doc_df.loc[id, 'est_entity'] = 'Not Found'
doc_df.loc[id, 'est_agent'] = 'Not Found'
doc_df.loc[id, 'est_other'] = 'Not Found'
doc_df.loc[id, 'est_latest_update'] = 'Not Found'

id = 3235
df.loc[id, 'entity'] = 'Hawaii MVCC LLC'
df.loc[id, 'agent_name'] = 'Lauren R Hong Wright'
df.loc[id, 'agent_address'] = '745 Fort St STE 1501'
df.loc[id, 'agent_city'] = 'Honolulu'
df.loc[id, 'agent_state'] = 'Hawaii'
df.loc[id, 'agent_zip'] = '96813'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_other'] = 'None'
doc_df.loc[id, 'est_latest_update'] = '2019'

id = 3247
df.loc[id, 'entity'] = 'KMA CINEMAS, LLC'
df.loc[id, 'agent_name'] = 'CORPORATION SERVICE COMPANY'
df.loc[id, 'agent_address'] = '1003 BISHOP STREET SUITE 1600 PAUAHI TOWER'
df.loc[id, 'agent_city'] = 'HONOLULU'
df.loc[id, 'agent_state'] = 'HI'
df.loc[id, 'agent_zip'] = '96813'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_other'] = 'None'
doc_df.loc[id, 'est_latest_update'] = '2019'

id = 880
df.loc[id, 'entity'] = 'Not Found'
df.loc[id, 'agent_name'] = 'Not Found'
df.loc[id, 'agent_address'] = 'Not Found'
df.loc[id, 'agent_city'] = 'Not Found'
df.loc[id, 'agent_state'] = 'Not Found'
df.loc[id, 'agent_zip'] = 'Not Found'
doc_df.loc[id, 'est_entity'] = 'Not Found'
doc_df.loc[id, 'est_agent'] = 'Not Found'
doc_df.loc[id, 'est_other'] = 'Not Found'
doc_df.loc[id, 'est_latest_update'] = 'Not Found'

id = 1507
df.loc[id, 'entity'] = 'Not Found'
df.loc[id, 'agent_name'] = 'Not Found'
df.loc[id, 'agent_address'] = 'Not Found'
df.loc[id, 'agent_city'] = 'Not Found'
df.loc[id, 'agent_state'] = 'Not Found'
df.loc[id, 'agent_zip'] = 'Not Found'
doc_df.loc[id, 'est_entity'] = 'Not Found'
doc_df.loc[id, 'est_agent'] = 'Not Found'
doc_df.loc[id, 'est_other'] = 'Not Found'
doc_df.loc[id, 'est_latest_update'] = 'Not Found'

id = 1932
df.loc[id, 'entity'] = 'CVS Pharmacy, Inc.'
df.loc[id, 'agent_name'] = 'CT CORPORATION SYSTEM'
df.loc[id, 'agent_address'] = '450 VETERANS MEMORIAL PARKWAY, SUITE 7A'
df.loc[id, 'agent_city'] = 'EAST PROVIDENCE'
df.loc[id, 'agent_state'] = 'RI'
df.loc[id, 'agent_zip'] = '02914'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Articles_of_Incorp.pdf", "SoS Articles of Incorporation")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Agent_Change.pdf", "SoS Agent Change")'
doc_df.loc[id, 'est_other'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_latest_update'] = '2019'

id = 1977
df.loc[id, 'entity'] = 'CVS Pharmacy, Inc.'
df.loc[id, 'agent_name'] = 'CT CORPORATION SYSTEM'
df.loc[id, 'agent_address'] = '450 VETERANS MEMORIAL PARKWAY, SUITE 7A'
df.loc[id, 'agent_city'] = 'EAST PROVIDENCE'
df.loc[id, 'agent_state'] = 'RI'
df.loc[id, 'agent_zip'] = '02914'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Articles_of_Incorp.pdf", "SoS Articles of Incorporation")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Agent_Change.pdf", "SoS Agent Change")'
doc_df.loc[id, 'est_other'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_latest_update'] = '2019'

id = 2047
df.loc[id, 'entity'] = 'CVS Pharmacy, Inc.'
df.loc[id, 'agent_name'] = 'CT CORPORATION SYSTEM'
df.loc[id, 'agent_address'] = '450 VETERANS MEMORIAL PARKWAY, SUITE 7A'
df.loc[id, 'agent_city'] = 'EAST PROVIDENCE'
df.loc[id, 'agent_state'] = 'RI'
df.loc[id, 'agent_zip'] = '02914'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Articles_of_Incorp.pdf", "SoS Articles of Incorporation")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Agent_Change.pdf", "SoS Agent Change")'
doc_df.loc[id, 'est_other'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_latest_update'] = '2019'

id = 2677
df.loc[id, 'entity'] = 'CVS Pharmacy, Inc.'
df.loc[id, 'agent_name'] = 'CT CORPORATION SYSTEM'
df.loc[id, 'agent_address'] = '450 VETERANS MEMORIAL PARKWAY, SUITE 7A'
df.loc[id, 'agent_city'] = 'EAST PROVIDENCE'
df.loc[id, 'agent_state'] = 'RI'
df.loc[id, 'agent_zip'] = '02914'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Articles_of_Incorp.pdf", "SoS Articles of Incorporation")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Agent_Change.pdf", "SoS Agent Change")'
doc_df.loc[id, 'est_other'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_latest_update'] = '2019'

id = 2714
df.loc[id, 'entity'] = 'CVS Pharmacy, Inc.'
df.loc[id, 'agent_name'] = 'CT CORPORATION SYSTEM'
df.loc[id, 'agent_address'] = '450 VETERANS MEMORIAL PARKWAY, SUITE 7A'
df.loc[id, 'agent_city'] = 'EAST PROVIDENCE'
df.loc[id, 'agent_state'] = 'RI'
df.loc[id, 'agent_zip'] = '02914'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Articles_of_Incorp.pdf", "SoS Articles of Incorporation")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Agent_Change.pdf", "SoS Agent Change")'
doc_df.loc[id, 'est_other'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_latest_update'] = '2019'

id = 2720
df.loc[id, 'entity'] = 'CVS Pharmacy, Inc.'
df.loc[id, 'agent_name'] = 'CT CORPORATION SYSTEM'
df.loc[id, 'agent_address'] = '450 VETERANS MEMORIAL PARKWAY, SUITE 7A'
df.loc[id, 'agent_city'] = 'EAST PROVIDENCE'
df.loc[id, 'agent_state'] = 'RI'
df.loc[id, 'agent_zip'] = '02914'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Articles_of_Incorp.pdf", "SoS Articles of Incorporation")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Agent_Change.pdf", "SoS Agent Change")'
doc_df.loc[id, 'est_other'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.docx", "SoS Website Record")'
doc_df.loc[id, 'est_latest_update'] = '2019'


id = 2095
df.loc[id, 'entity'] = 'PIGGLY WIGGLY STORE NO. 34, INC.'
df.loc[id, 'agent_name'] = 'CHARLES CARSON'
df.loc[id, 'agent_address'] = '2003 ROBERTSON ST'
df.loc[id, 'agent_city'] = 'CORINTH'
df.loc[id, 'agent_state'] = 'MS'
df.loc[id, 'agent_zip'] = '38834'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/Existing Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.pdf", "SoS Website Record")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.pdf", "SoS Website Record")'
doc_df.loc[id, 'est_other'] = '=HYPERLINK("' +  \
    'documentation/New Retailers/IMPAQID_' + str(id) + \
    '_SoS_Website_Record.pdf", "SoS Website Record")'
doc_df.loc[id, 'est_latest_update'] = '1984'

id = 2220
df.loc[id, 'entity'] = 'Not Found'
df.loc[id, 'agent_name'] = 'Not Found'
df.loc[id, 'agent_address'] = 'Not Found'
df.loc[id, 'agent_city'] = 'Not Found'
df.loc[id, 'agent_state'] = 'Not Found'
df.loc[id, 'agent_zip'] = 'Not Found'
doc_df.loc[id, 'est_entity'] = 'Not Found'
doc_df.loc[id, 'est_agent'] = 'Not Found'
doc_df.loc[id, 'est_other'] = 'Not Found'
doc_df.loc[id, 'est_latest_update'] = 'Not Found'

id = 2545
df.loc[id, 'entity'] = 'Not Found'
df.loc[id, 'agent_name'] = 'Not Found'
df.loc[id, 'agent_address'] = 'Not Found'
df.loc[id, 'agent_city'] = 'Not Found'
df.loc[id, 'agent_state'] = 'Not Found'
df.loc[id, 'agent_zip'] = 'Not Found'
doc_df.loc[id, 'est_entity'] = 'Not Found'
doc_df.loc[id, 'est_agent'] = 'Not Found'
doc_df.loc[id, 'est_other'] = 'Not Found'
doc_df.loc[id, 'est_latest_update'] = 'Not Found'

id = 728
df.loc[id, 'entity'] = 'Not Found'
df.loc[id, 'agent_name'] = 'Not Found'
df.loc[id, 'agent_address'] = 'Not Found'
df.loc[id, 'agent_city'] = 'Not Found'
df.loc[id, 'agent_state'] = 'Not Found'
df.loc[id, 'agent_zip'] = 'Not Found'
doc_df.loc[id, 'est_entity'] = 'Not Found'
doc_df.loc[id, 'est_agent'] = 'Not Found'
doc_df.loc[id, 'est_other'] = 'Not Found'
doc_df.loc[id, 'est_latest_update'] = 'Not Found'

id = 2635
df.loc[id, 'entity'] = 'Not Found'
df.loc[id, 'agent_name'] = 'Not Found'
df.loc[id, 'agent_address'] = 'Not Found'
df.loc[id, 'agent_city'] = 'Not Found'
df.loc[id, 'agent_state'] = 'Not Found'
df.loc[id, 'agent_zip'] = 'Not Found'
doc_df.loc[id, 'est_entity'] = 'Not Found'
doc_df.loc[id, 'est_agent'] = 'Not Found'
doc_df.loc[id, 'est_other'] = 'Not Found'
doc_df.loc[id, 'est_latest_update'] = 'Not Found'

id = 2640
df.loc[id, 'entity'] = 'Not Found'
df.loc[id, 'agent_name'] = 'Not Found'
df.loc[id, 'agent_address'] = 'Not Found'
df.loc[id, 'agent_city'] = 'Not Found'
df.loc[id, 'agent_state'] = 'Not Found'
df.loc[id, 'agent_zip'] = 'Not Found'
doc_df.loc[id, 'est_entity'] = 'Not Found'
doc_df.loc[id, 'est_agent'] = 'Not Found'
doc_df.loc[id, 'est_other'] = 'Not Found'
doc_df.loc[id, 'est_latest_update'] = 'Not Found'

id = 2642
df.loc[id, 'entity'] = 'Not Found'
df.loc[id, 'agent_name'] = 'Not Found'
df.loc[id, 'agent_address'] = 'Not Found'
df.loc[id, 'agent_city'] = 'Not Found'
df.loc[id, 'agent_state'] = 'Not Found'
df.loc[id, 'agent_zip'] = 'Not Found'
doc_df.loc[id, 'est_entity'] = 'Not Found'
doc_df.loc[id, 'est_agent'] = 'Not Found'
doc_df.loc[id, 'est_other'] = 'Not Found'
doc_df.loc[id, 'est_latest_update'] = 'Not Found'

id = 444
df.loc[id, 'entity'] = 'Not Found'
df.loc[id, 'agent_name'] = 'Not Found'
df.loc[id, 'agent_address'] = 'Not Found'
df.loc[id, 'agent_city'] = 'Not Found'
df.loc[id, 'agent_state'] = 'Not Found'
df.loc[id, 'agent_zip'] = 'Not Found'
doc_df.loc[id, 'est_entity'] = 'Not Found'
doc_df.loc[id, 'est_agent'] = 'Not Found'
doc_df.loc[id, 'est_other'] = 'Not Found'
doc_df.loc[id, 'est_latest_update'] = 'Not Found'

id = 445
df.loc[id, 'entity'] = 'GNS, INC.'
df.loc[id, 'agent_name'] = 'GERALD F NYGAARD'
df.loc[id, 'agent_address'] = 'PO BOX AE'
df.loc[id, 'agent_city'] = 'SLOAN'
df.loc[id, 'agent_state'] = 'IA'
df.loc[id, 'agent_zip'] = '51055'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/Existing Retailers/IA319170_' +  \
    '_SoS_Website_Record.png", "SoS Website Record")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/Existing Retailers/IA319170_' +\
    '_SoS_Website_Record.png", "SoS Website Record")'
doc_df.loc[id, 'est_other'] = '=HYPERLINK("' +  \
    'documentation/Existing Retailers/IA319170_' +\
    '_SoS_Annual_Report.tif", "SoS Annual Report")'
doc_df.loc[id, 'est_latest_update'] = '1994'

id = 453
df.loc[id, 'entity'] = 'GNS, INC.'
df.loc[id, 'agent_name'] = 'GERALD F NYGAARD'
df.loc[id, 'agent_address'] = 'PO BOX AE'
df.loc[id, 'agent_city'] = 'SLOAN'
df.loc[id, 'agent_state'] = 'IA'
df.loc[id, 'agent_zip'] = '51055'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/Existing Retailers/IA319170_' +  \
    '_SoS_Website_Record.png", "SoS Website Record")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/Existing Retailers/IA319170_' +\
    '_SoS_Website_Record.png", "SoS Website Record")'
doc_df.loc[id, 'est_other'] = '=HYPERLINK("' +  \
    'documentation/Existing Retailers/IA319170_' +\
    '_SoS_Annual_Report.tif", "SoS Annual Report")'
doc_df.loc[id, 'est_latest_update'] = '1994'

id = 446
df.loc[id, 'entity'] = 'Not Found'
df.loc[id, 'agent_name'] = 'Not Found'
df.loc[id, 'agent_address'] = 'Not Found'
df.loc[id, 'agent_city'] = 'Not Found'
df.loc[id, 'agent_state'] = 'Not Found'
df.loc[id, 'agent_zip'] = 'Not Found'
doc_df.loc[id, 'est_entity'] = 'Not Found'
doc_df.loc[id, 'est_agent'] = 'Not Found'
doc_df.loc[id, 'est_other'] = 'Not Found'
doc_df.loc[id, 'est_latest_update'] = 'Not Found'

id = 447
df.loc[id, 'entity'] = 'Not Found'
df.loc[id, 'agent_name'] = 'Not Found'
df.loc[id, 'agent_address'] = 'Not Found'
df.loc[id, 'agent_city'] = 'Not Found'
df.loc[id, 'agent_state'] = 'Not Found'
df.loc[id, 'agent_zip'] = 'Not Found'
doc_df.loc[id, 'est_entity'] = 'Not Found'
doc_df.loc[id, 'est_agent'] = 'Not Found'
doc_df.loc[id, 'est_other'] = 'Not Found'
doc_df.loc[id, 'est_latest_update'] = 'Not Found'

id = 448
df.loc[id, 'entity'] = 'Not Found'
df.loc[id, 'agent_name'] = 'Not Found'
df.loc[id, 'agent_address'] = 'Not Found'
df.loc[id, 'agent_city'] = 'Not Found'
df.loc[id, 'agent_state'] = 'Not Found'
df.loc[id, 'agent_zip'] = 'Not Found'
doc_df.loc[id, 'est_entity'] = 'Not Found'
doc_df.loc[id, 'est_agent'] = 'Not Found'
doc_df.loc[id, 'est_other'] = 'Not Found'
doc_df.loc[id, 'est_latest_update'] = 'Not Found'

id = 449
df.loc[id, 'entity'] = 'Not Found'
df.loc[id, 'agent_name'] = 'Not Found'
df.loc[id, 'agent_address'] = 'Not Found'
df.loc[id, 'agent_city'] = 'Not Found'
df.loc[id, 'agent_state'] = 'Not Found'
df.loc[id, 'agent_zip'] = 'Not Found'
doc_df.loc[id, 'est_entity'] = 'Not Found'
doc_df.loc[id, 'est_agent'] = 'Not Found'
doc_df.loc[id, 'est_other'] = 'Not Found'
doc_df.loc[id, 'est_latest_update'] = 'Not Found'

id = 450
df.loc[id, 'entity'] = 'Not Found'
df.loc[id, 'agent_name'] = 'Not Found'
df.loc[id, 'agent_address'] = 'Not Found'
df.loc[id, 'agent_city'] = 'Not Found'
df.loc[id, 'agent_state'] = 'Not Found'
df.loc[id, 'agent_zip'] = 'Not Found'
doc_df.loc[id, 'est_entity'] = 'Not Found'
doc_df.loc[id, 'est_agent'] = 'Not Found'
doc_df.loc[id, 'est_other'] = 'Not Found'
doc_df.loc[id, 'est_latest_update'] = 'Not Found'

id = 451
df.loc[id, 'entity'] = 'PONCA ECONOMIC DEVELOPMENT CORPORATION (PEDCO)'
df.loc[id, 'agent_name'] = 'JAN COLWELL'
df.loc[id, 'agent_address'] = '1001 AVE H'
df.loc[id, 'agent_city'] = 'CLEAR LAKE'
df.loc[id, 'agent_state'] = 'IA'
df.loc[id, 'agent_zip'] = '51510'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/Existing Retailers/IA746688_' +  \
    '_SoS_Website_Record.png", "SoS Website Record")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/Existing Retailers/IA746688_' +\
    '_SoS_Website_Record.png", "SoS Website Record")'
doc_df.loc[id, 'est_other'] = '=HYPERLINK("' +  \
    'documentation/Existing Retailers/IA746688_' +\
    '_SoS_Certificate_of_Authority.tif", "SoS Certificate of Authority")'
doc_df.loc[id, 'est_latest_update'] = '2010'

id = 454
df.loc[id, 'entity'] = 'PONCA ECONOMIC DEVELOPMENT CORPORATION (PEDCO)'
df.loc[id, 'agent_name'] = 'JAN COLWELL'
df.loc[id, 'agent_address'] = '1001 AVE H'
df.loc[id, 'agent_city'] = 'CLEAR LAKE'
df.loc[id, 'agent_state'] = 'IA'
df.loc[id, 'agent_zip'] = '51510'
doc_df.loc[id, 'est_entity'] = '=HYPERLINK("' +  \
    'documentation/Existing Retailers/IA757691_' +  \
    '_SoS_Website_Record.png", "SoS Website Record")'
doc_df.loc[id, 'est_agent'] = '=HYPERLINK("' +  \
    'documentation/Existing Retailers/IA757691_' +\
    '_SoS_Website_Record.png", "SoS Website Record")'
doc_df.loc[id, 'est_other'] = '=HYPERLINK("' +  \
    'documentation/Existing Retailers/IA757691_' +\
    '_SoS_Certificate_of_Authority.tif", "SoS Certificate of Authority")'
doc_df.loc[id, 'est_latest_update'] = '2010'

id = 452
df.loc[id, 'entity'] = 'Not Found'
df.loc[id, 'agent_name'] = 'Not Found'
df.loc[id, 'agent_address'] = 'Not Found'
df.loc[id, 'agent_city'] = 'Not Found'
df.loc[id, 'agent_state'] = 'Not Found'
df.loc[id, 'agent_zip'] = 'Not Found'
doc_df.loc[id, 'est_entity'] = 'Not Found'
doc_df.loc[id, 'est_agent'] = 'Not Found'
doc_df.loc[id, 'est_other'] = 'Not Found'
doc_df.loc[id, 'est_latest_update'] = 'Not Found'

id = 2562
df.loc[id, 'entity'] = 'Not Found'
df.loc[id, 'agent_name'] = 'Not Found'
df.loc[id, 'agent_address'] = 'Not Found'
df.loc[id, 'agent_city'] = 'Not Found'
df.loc[id, 'agent_state'] = 'Not Found'
df.loc[id, 'agent_zip'] = 'Not Found'
doc_df.loc[id, 'est_entity'] = 'Not Found'
doc_df.loc[id, 'est_agent'] = 'Not Found'
doc_df.loc[id, 'est_other'] = 'Not Found'
doc_df.loc[id, 'est_latest_update'] = 'Not Found'

id =
df.loc[id, 'entity'] = 'Not Found'
df.loc[id, 'agent_name'] = 'Not Found'
df.loc[id, 'agent_address'] = 'Not Found'
df.loc[id, 'agent_city'] = 'Not Found'
df.loc[id, 'agent_state'] = 'Not Found'
df.loc[id, 'agent_zip'] = 'Not Found'
doc_df.loc[id, 'est_entity'] = 'Not Found'
doc_df.loc[id, 'est_agent'] = 'Not Found'
doc_df.loc[id, 'est_other'] = 'Not Found'
doc_df.loc[id, 'est_latest_update'] = 'Not Found'
# id =
# df.loc[id, 'entity'] = 'Not Found'
# df.loc[id, 'agent_name'] = 'Not Found'
# df.loc[id, 'agent_address'] = 'Not Found'
# df.loc[id, 'agent_city'] = 'Not Found'
# df.loc[id, 'agent_state'] = 'Not Found'
# df.loc[id, 'agent_zip'] = 'Not Found'
# doc_df.loc[id, 'est_entity'] = 'Not Found'
# doc_df.loc[id, 'est_agent'] = 'Not Found'
# doc_df.loc[id, 'est_other'] = 'Not Found'
# doc_df.loc[id, 'est_latest_update'] = 'Not Found'
#
# id =
# df.loc[id, 'entity'] = 'Not Found'
# df.loc[id, 'agent_name'] = 'Not Found'
# df.loc[id, 'agent_address'] = 'Not Found'
# df.loc[id, 'agent_city'] = 'Not Found'
# df.loc[id, 'agent_state'] = 'Not Found'
# df.loc[id, 'agent_zip'] = 'Not Found'
# doc_df.loc[id, 'est_entity'] = 'Not Found'
# doc_df.loc[id, 'est_agent'] = 'Not Found'
# doc_df.loc[id, 'est_other'] = 'Not Found'
# doc_df.loc[id, 'est_latest_update'] = 'Not Found'

df.to_csv('step_4_work/full_retailer_list_w_owner.csv', index=False)
doc_df.to_csv('output/documentation_links.csv', index=False)

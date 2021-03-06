def main():
    # create spreadsheets that make up the 5 sheets of the submission file
    # 1. Original Data: the original data received from FDA
    # 2. Revised Data - Change Log: Revised data with track changes
    # 3. Revised Data - Clean: Revised data with no track changes
    # 4. Sources and Documentation: Links to sources and documentation
    # 5. New Establishments: New establishments found to be within tribal lands

    import pandas as pd
    import numpy as np
    from itertools import compress
    import xlsxwriter
    import os
    from ast import literal_eval

    # ------------------------------------------------------------------------
    # 1. Orignal Data
    # ------------------------------------------------------------------------
    # copy/paste of input spreadsheet
    ori_df = pd.read_excel('input/Public retail data_original.xlsx',dtype='str')
    ori_df['IMPAQ_ID'] = ori_df.index
    ori_df.to_csv('output/1_Original_Data.csv', index = False)
    import warnings
    warnings.simplefilter('error')
    # ------------------------------------------------------------------------
    # 2. Revised Data - Change Log: Revised data with track changes
    # ------------------------------------------------------------------------
    # new columns to add to original list, and what order to put them in
    log_df = ori_df
    new_cols = [
        'DBA Name - Updated',
        'Address Line 1 - Updated',
        'City - Updated',
        'Zip - Updated',
        'County - Updated',
        'Business Status - Updated',
        'On Tribe Land - Updated',
        'Longitude - Updated',
        'Latitude - Updated',
        'DBA Name - Change Log',
        'Address Line 1 - Change Log',
        'City - Change Log',
        'Zip - Change Log',
        'County - Change Log',
        'Business Status - Change Log',
        'On Tribe Land - Change Log',
        'Longitude - Change Log',
        'Latitude - Change Log',
        'Tribe associated with location',
        'Reservation associated with location',
        'Miles to nearest tribal land',
        'Nearest tribe to location',
        'Nearest reservation to location',
        'Establishment Legal Entity',
        'Registered Agent Name',
        'Agent Address',
        'Agent City',
        'Agent State',
        'Agent Zip',
        'Latest Year of Ownership Docs'
    ]
    log_df = pd.concat([log_df,pd.DataFrame(columns=new_cols)], sort=False)
    cols_order = [
        'IMPAQ_ID',
        'REI',
        'DBA Name',
        'DBA Name - Change Log',
        'DBA Name - Updated',
        'Address Line 1',
        'Address Line 1 - Change Log',
        'Address Line 1 - Updated',
        'City',
        'City - Change Log',
        'City - Updated',
        'State',
        'Zip',
        'Zip - Change Log',
        'Zip - Updated',
        'County',
        'County - Change Log',
        'County - Updated',
        'Business Status',
        'Business Status - Change Log',
        'Business Status - Updated',
        'On Tribe Land',
        'On Tribe Land - Change Log',
        'On Tribe Land - Updated',
        'Tribe associated with location',
        'Reservation associated with location',
        'Miles to nearest tribal land',
        'Nearest tribe to location',
        'Nearest reservation to location',
        'Tribal Owned ',
        'Longitude',
        'Longitude - Change Log',
        'Longitude - Updated',
        'Latitude',
        'Latitude - Change Log',
        'Latitude - Updated',
        'EST_COMMENTS',
        'Establishment Legal Entity',
        'Registered Agent Name',
        'Agent Address',
        'Agent City',
        'Agent State',
        'Agent Zip',
        'Latest Year of Ownership Docs'
    ]
    log_df = log_df[cols_order]

    # reshape change log sheet to match format
    change_df = pd.read_csv('step_4_work/output/full_retailer_list_w_owner_final.csv')
    change_df = change_df.loc[change_df['ori_flg']=='From Original List',:]

    # standardize value labels
    change_df['Business Status_update'] = change_df['Business Status_update'].str.replace('Active', 'In Operation')
    change_df['Business Status_update'] = change_df['Business Status_update'].str.replace('Closed', 'Out of Business')
    change_df['Business Status_update'] = change_df['Business Status_update'].str.replace("Can't Validate", 'No changes')

    rename_cols = {
        'DBA Name_update': 'DBA Name - Updated',
        'Address Line 1_update': 'Address Line 1 - Updated',
        'City_update': 'City - Updated',
        'Zip_update': 'Zip - Updated',
        'County_update': 'County - Updated',
        'Business Status_update': 'Business Status - Updated',
        'On Tribe Land_update': 'On Tribe Land - Updated',
        'Assoc Tribe': 'Tribe associated with location',
        'Assoc Res': 'Reservation associated with location',
        'Miles to Nearest Tribe': 'Miles to nearest tribal land',
        'Nearest Tribe': 'Nearest tribe to location',
        'Nearest Res': 'Nearest reservation to location',
        'Longitude_update': 'Longitude - Updated',
        'Latitude_update': 'Latitude - Updated',
        'DBA Name_changes':'DBA Name - Change Log',
        'Address Line 1_changes':'Address Line 1 - Change Log',
        'City_changes':'City - Change Log',
        'Zip_changes':'Zip - Change Log',
        'County_changes':'County - Change Log',
        'On Tribe Land_changes':'On Tribe Land - Change Log',
        'Longitude_changes':'Longitude - Change Log',
        'Latitude_changes':'Latitude - Change Log',
        'Business Status_changes':'Business Status - Change Log',
        'entity': 'Establishment Legal Entity',
        'agent_name': 'Registered Agent Name',
        'agent_address': 'Agent Address',
        'agent_city': 'Agent City',
        'agent_state': 'Agent State',
        'agent_zip': 'Agent Zip'
    }

    change_df = change_df.rename(rename_cols, axis=1)
    log_df.update(change_df.loc[:,new_cols])
    # denote "no changes" in all change log columns columns
    log_df.loc[log_df['DBA Name'] == log_df['DBA Name - Updated'], 'DBA Name - Change Log'] = 'No changes'
    log_df.loc[log_df['County'] == log_df['County - Updated'], 'County - Change Log'] = 'No changes'
    log_df.loc[log_df['Business Status'] == log_df['Business Status - Updated'], 'Business Status - Change Log'] = 'No changes'
    log_df.loc[log_df['City'] == log_df['City - Updated'], 'City - Change Log'] = 'No changes'
    log_df['Longitude - Change Log'] = log_df['Longitude - Change Log'].str.replace("Correct", 'No changes')
    log_df['Latitude - Change Log'] = log_df['Latitude - Change Log'].str.replace("Correct", 'No changes')

    # replace string "nan" with blank cells
    log_df = log_df.replace('nan','')

    log_df.to_csv('output/2_Revised_Data_Change_Log.csv', index = False)

    # ------------------------------------------------------------------------
    # 3. Revised Data - Clean: Revised data without track changes
    # ------------------------------------------------------------------------
    clean_df = log_df
    # create list of updated columns
    update_cols = list(compress(clean_df.columns.tolist(), ["Updated" in i for i in clean_df.columns]))
    # paste over updated value if changed, then drop the update column
    for i in update_cols:
        orig_col = i.replace(' - Updated','')
        clean_df = clean_df.drop(orig_col, axis=1)
        clean_df = clean_df.rename({i:orig_col},axis=1)
    # drop change log columns
    clean_df = clean_df.drop([i for i in clean_df.columns if 'Change Log' in i], axis=1)
    clean_df=clean_df.replace("Can't validate",'Unknown')
    clean_df.to_csv('output/3_Revised_Data_Clean.csv',index = False)

    # ------------------------------------------------------------------------
    # 4. Sources and Documentation - Existing Retailers
    # ------------------------------------------------------------------------
    # load google places output
    ggl_df = pd.read_csv('step_1_work/output/documentation/google_places_output.csv')

    # load manual verification log
    verif_df = pd.read_csv('step_1_work/output/retailers_for_manual_verify_complete.csv')

    # create a documentation df
    doc_df = clean_df[['IMPAQ_ID','DBA Name','Miles to nearest tribal land']].merge(ori_df[['REI']], right_index=True, left_on='IMPAQ_ID',how='left')
    doc_df = doc_df.merge(ggl_df[['id','match','url']], how='left', right_on='id',left_on='IMPAQ_ID')
    doc_df = doc_df.merge(verif_df[['est_id','Manual Result']], how='left', right_on='est_id', left_on='IMPAQ_ID')
    doc_df = doc_df.drop('id', axis=1)
    doc_df.index =doc_df['IMPAQ_ID']

    # Tribal GIS Overlays
    doc_df['Overlay Path'] =  '.\\documentation\\Tribal Boundary GIS Overlays\\' \
        + doc_df['IMPAQ_ID'].astype('int').astype('str') + '_tribe_bound_overlay.html'
    # Google Maps URLs
    doc_df = doc_df.rename({'url':'Google Maps URL'}, axis=1)
    doc_df['match'] = np.where((doc_df['match']=='Active')|(doc_df['match']=='Closed'), 'Match','Not Matched')
    doc_df.loc[doc_df['match']=='Not Matched', 'url'] = np.nan

    # Google Maps Screenshots
    def find_pic(id):
        file_list = os.listdir( 'output\\documentation\\Google Maps Screenshots\\')
        file = list(compress(file_list, ['est' + str(id) + '_cand0'
            in i for i in file_list]))
        if len(file)>0:
            return  '.\\documentation\\Google Maps Screenshots\\' + file[0]
        else:
            return np.nan

    doc_df['Google Maps Screenshot'] = doc_df['IMPAQ_ID'].apply(find_pic)
    # if manually verified, we will redirect to the google maps picture(s)
    doc_df.loc[doc_df['Manual Result']=='yes', 'url'] = np.nan

    # save url's in csv file
    def make_hyperlink(value, text):
        return '=HYPERLINK("%s", "%s")' % (value, text)

    doc_df.loc[doc_df['Miles to nearest tribal land'].isna() == False,'On Tribe Land/Associated Tribe'] = \
        doc_df.loc[doc_df['Miles to nearest tribal land'].isna() == False,'Overlay Path'].apply(lambda x: make_hyperlink(x, 'Tribal Boundary GIS Overlay'))
    doc_df.loc[doc_df['Miles to nearest tribal land'].isna() == True,'On Tribe Land/Associated Tribe'] = 'Could not validate'
    # links for those that were manually verified via screenshots
    manual_loc =  (doc_df['Manual Result'] == 'yes')
    doc_df.loc[manual_loc, 'Establishment DBA Name/Address'] = doc_df.loc[manual_loc, 'Google Maps Screenshot'].apply(lambda x: make_hyperlink(x, 'Google Maps Screenshot'))
    doc_df.loc[manual_loc, 'Business Status'] = doc_df.loc[manual_loc,'Google Maps Screenshot'].apply(lambda x: make_hyperlink(x, 'Google Maps Screenshot'))
    # links for those with Google Places entry
    auto_loc = (doc_df['match'] == 'Match')
    doc_df.loc[auto_loc, 'Establishment DBA Name/Address'] = doc_df.loc[auto_loc, 'Google Maps URL'].apply(lambda x: make_hyperlink(x, 'Google Places Record'))
    doc_df.loc[auto_loc, 'Business Status'] = doc_df.loc[auto_loc,'Google Maps URL'].apply(lambda x: make_hyperlink(x, 'Google Places Record'))

    # Mark Could not validate for
    miss_loc = doc_df['match']=='Not Matched'
    doc_df.loc[miss_loc, 'Establishment DBA Name/Address']  = "Could not validate"
    doc_df.loc[miss_loc, 'Business Status']  = "Could not validate"


    # legal ownership coming later
    doc_df['Establishment Legal Entity'] = ''
    doc_df['Registered Agent Name/Address'] = ''
    doc_df['Other Associated Document'] = ''

    # read in links for ownership documentation
    # same code as in existing retailers one
    # manual links
    manual_df = pd.read_csv('output/documentation_links.csv', dtype='str')
    manual_df = manual_df.rename({
        'est_entity': 'Establishment Legal Entity',
        'est_agent': 'Registered Agent Name/Address',
        'est_other': 'Other Associated Document'
    }, axis=1)
    manual_df['IMPAQ_ID'] = manual_df['IMPAQ_ID'].astype('int')
    manual_df = manual_df.loc[manual_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    manual_df.index = manual_df['IMPAQ_ID']
    doc_df.update(manual_df)

    # Arizona
    az_df = pd.read_csv('step_4_work/AZ/AZ_FDA_matches.csv', dtype='str')
    az_df['IMPAQ_ID'] = az_df['IMPAQ_ID'].astype('int')
    az_df = az_df.loc[az_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    az_df = az_df.merge(ori_df[['REI','IMPAQ_ID']],on='IMPAQ_ID',how='left')
    az_df.index = az_df['IMPAQ_ID']
    dload_df = pd.read_csv('step_4_work/AZ/AZ_docs_found.csv', dtype='str')
    dload_df['IMPAQ_ID'] = dload_df['IMPAQ_ID'].astype('int')
    dload_df = dload_df.loc[dload_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    dload_df['doc_types'] = dload_df['doc_types'].fillna("['Website_Record']")
    # read nested lists within docs found file
    dload_df['doc_types'] = dload_df['doc_types'].apply(literal_eval)
    # logic for documentation choices
    # legal entity: registraion, then any other doc
    # agent details: SI-Complete, then any other doc
    # other: any other docs not used
    for i,row in az_df.loc[az_df['SoS_record'].isna() == False].iterrows():
        docs = dload_df.loc[dload_df['IMPAQ_ID']==row.IMPAQ_ID, 'doc_types'].values[0]
        def _get_ext(type):
            if type !='Website Record' and type !='Website_Record':
                return('.pdf')
            else:
                return('.png')
        # legal entity
        if 'Website_Record' in docs:
            doc_type = 'Website_Record'
        else:
            doc_type = docs[0]
        ext = _get_ext(doc_type)
        doc_df.loc[row.name, 'Establishment Legal Entity'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + str(row.REI) + \
            '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'
        # agent details
        doc_type= 'Website_Record'
        ext = _get_ext(doc_type)
        doc_df.loc[row.name, 'Registered Agent Name/Address'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + str(row.REI) + \
            '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'
        # other docs
        if 'Articles of Organization' in docs:
            doc_type = 'Articles of Organization'
        if len(docs) != 1:
            ext = _get_ext(doc_type)
            doc_df.loc[row.name, 'Other Associated Document'] = '=HYPERLINK("' +  \
                './documentation/Existing Retailers/' + str(row.REI) + \
                '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'

    # California
    ca_df = pd.read_csv('step_4_work/CA/CA_FDA_matches.csv', dtype='str')
    ca_df['IMPAQ_ID'] = ca_df['IMPAQ_ID'].astype('int')
    ca_df = ca_df.loc[ca_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    ca_df = ca_df.merge(ori_df[['REI','IMPAQ_ID']],on='IMPAQ_ID',how='left')
    ca_df.index = ca_df['IMPAQ_ID']
    dload_df = pd.read_csv('step_4_work/CA/CA_docs_found.csv', dtype='str')
    dload_df['IMPAQ_ID'] = dload_df['IMPAQ_ID'].astype('int')
    dload_df = dload_df.loc[dload_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    # read nested lists within docs found file
    dload_df['doc_types'] = dload_df['doc_types'].apply(literal_eval)
    # logic for documentation choices
    # legal entity: registraion, then any other doc
    # agent details: SI-Complete, then any other doc
    # other: any other docs not used
    for i,row in ca_df.loc[ca_df['SoS_record'].isna() == False].iterrows():
        docs = dload_df.loc[dload_df['IMPAQ_ID']==row.IMPAQ_ID, 'doc_types'].values[0]
        def _get_ext(type):
            if type !='Website Record' and type !='Website_Record':
                return('.pdf')
            else:
                return('.png')
        # legal entity
        if 'REGISTRATION' in docs:
            doc_type = 'REGISTRATION'
        elif len(docs) != 0:
            doc_type = docs[0]
        else:
            doc_type = 'Website_Record'
        ext = _get_ext(doc_type)
        doc_df.loc[row.name, 'Establishment Legal Entity'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + str(row.REI) + \
            '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'
        # agent details
        doc_type= 'Website_Record'
        ext = _get_ext(doc_type)
        doc_df.loc[row.name, 'Registered Agent Name/Address'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + str(row.REI) + \
            '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'
        # other docs
        if 'SI-COMPLETE' in docs and 'REGISTRATION' in docs:
            doc_type = docs[0]
        elif len(docs) > 1:
            doc_type = docs[1]
        if len(docs) != 1:
            ext = _get_ext(doc_type)
            doc_df.loc[row.name, 'Other Associated Document'] = '=HYPERLINK("' +  \
                './documentation/Existing Retailers/' + str(row.REI) + \
                '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'

    # Oklahoma
    # run state_scrapers/OK/OK_3_fetch_document
    # load output below
    ok_df = pd.read_csv('step_4_work/OK/OK_FDA_matches.csv', dtype='str')
    ok_df['IMPAQ_ID'] = ok_df['IMPAQ_ID'].astype('int')
    ok_df = ok_df.loc[ok_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    # Add in REI
    #ok_df = ok_df.merge(ori_df[['REI','IMPAQ_ID']],on='IMPAQ_ID',how='left')
    ok_df.index = ok_df['IMPAQ_ID']
    # note website record for all oklahoma matches
    for i,row in ok_df.loc[ok_df['SoS_record'].isna() == False].iterrows():
        doc_df.loc[row.name, 'Establishment Legal Entity'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + row.REI + \
            '_SoS_Website_Record.png", "SoS Website Record")'
        doc_df.loc[row.name, 'Registered Agent Name/Address'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + row.REI + \
            '_SoS_Website_Record.png", "SoS Website Record")'
        doc_df.loc[row.name, 'Other Associated Document'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + row.REI + \
            '_SoS_Website_Record.png", "SoS Website Record")'

    # Michigan
    MI_df = pd.read_csv('step_4_work/MI/MI_FDA_matches.csv', dtype='str')
    MI_df['IMPAQ_ID'] = MI_df['IMPAQ_ID'].astype('int')
    MI_df = MI_df.loc[MI_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    MI_df = MI_df.merge(ori_df[['REI','IMPAQ_ID']],on='IMPAQ_ID',how='left')
    MI_df.index = MI_df['IMPAQ_ID']
    dload_df = pd.read_csv('step_4_work/MI/MI_docs_found.csv', dtype='str')
    dload_df['IMPAQ_ID'] = dload_df['IMPAQ_ID'].astype('int')
    dload_df = dload_df.loc[dload_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    dload_df['doc_types'] = dload_df['doc_types'].fillna("['Website_Record']")
    # read nested lists within docs found file
    dload_df['doc_types'] = dload_df['doc_types'].apply(literal_eval)
    # logic for documentation choices
    # legal entity: registraion, then any other doc
    # agent details: SI-Complete, then any other doc
    # other: any other docs not used
    for i,row in MI_df.loc[MI_df['SoS_record'].isna() == False].iterrows():
        docs = dload_df.loc[dload_df['IMPAQ_ID']==row.IMPAQ_ID, 'doc_types'].values[0]
        def _get_ext(type):
            if type !='Website Record' and type !='Website_Record':
                return('.pdf')
            else:
                return('.png')
        # legal entity
        if 'Website_Record' in docs:
            doc_type = 'Website_Record'
        else:
            doc_type = docs[0]
        ext = _get_ext(doc_type)
        doc_df.loc[row.name, 'Establishment Legal Entity'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + str(row.REI) + \
            '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'
        # agent details
        doc_type= 'Website_Record'
        ext = _get_ext(doc_type)
        doc_df.loc[row.name, 'Registered Agent Name/Address'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + str(row.REI) + \
            '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'
        # other docs
        if 'ARTICLES OF ORGANIZATION' in docs:
            doc_type = 'ARTICLES OF ORGANIZATION'
        if len(docs) != 1:
            ext = _get_ext(doc_type)
            doc_df.loc[row.name, 'Other Associated Document'] = '=HYPERLINK("' +  \
                './documentation/Existing Retailers/' + str(row.REI) + \
                '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'

    # Minnesota
    # load output below
    MN_df = pd.read_csv('step_4_work/MN/MN_FDA_matches.csv', dtype='str')
    MN_df['IMPAQ_ID'] = MN_df['IMPAQ_ID'].astype('int')
    MN_df = MN_df.loc[MN_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    # Add in REI
    MN_df = MN_df.merge(ori_df[['REI','IMPAQ_ID']],on='IMPAQ_ID',how='left')
    MN_df.index = MN_df['IMPAQ_ID']
    # note website record for all Minnesota matches
    for i,row in MN_df.loc[MN_df['SoS_record'].isna() == False].iterrows():
        doc_df.loc[row.name, 'Establishment Legal Entity'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + row.REI + \
            '_SoS_Website_Record.png", "SoS Website Record")'
        doc_df.loc[row.name, 'Registered Agent Name/Address'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + row.REI + \
            '_SoS_Website_Record.png", "SoS Website Record")'
        doc_df.loc[row.name, 'Other Associated Document'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + row.REI + \
            '_SoS_Website_Record.png", "SoS Website Record")'

    # Montana
    # load output below
    MT_df = pd.read_csv('step_4_work/MT/MT_FDA_matches.csv', dtype='str')
    MT_df['IMPAQ_ID'] = MT_df['IMPAQ_ID'].astype('int')
    MT_df = MT_df.loc[MT_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    # Add in REI
    MT_df = MT_df.merge(ori_df[['REI','IMPAQ_ID']],on='IMPAQ_ID',how='left')
    MT_df.index = MT_df['IMPAQ_ID']
    # note website record for all Montana matches
    for i,row in MT_df.loc[MT_df['SoS_record'].isna() == False].iterrows():
        doc_df.loc[row.name, 'Establishment Legal Entity'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + row.REI + \
            '_SoS_Website_Record.png", "SoS Website Record")'
        doc_df.loc[row.name, 'Registered Agent Name/Address'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + row.REI + \
            '_SoS_Website_Record.png", "SoS Website Record")'
        doc_df.loc[row.name, 'Other Associated Document'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + row.REI + \
            '_SoS_Website_Record.png", "SoS Website Record")'

    # New Mexico
    # load output below
    NM_df = pd.read_csv('step_4_work/NM/NM_FDA_matches.csv', dtype='str')
    NM_df['IMPAQ_ID'] = NM_df['IMPAQ_ID'].astype('int')
    NM_df = NM_df.loc[NM_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    # Add in REI
    NM_df = NM_df.merge(ori_df[['REI','IMPAQ_ID']],on='IMPAQ_ID',how='left')
    NM_df.index = NM_df['IMPAQ_ID']
    # note website record for all Montana matches
    for i,row in NM_df.loc[NM_df['SoS_record'].isna() == False].iterrows():
        doc_df.loc[row.name, 'Establishment Legal Entity'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + row.REI + \
            '_SoS_Website_Record.png", "SoS Website Record")'
        doc_df.loc[row.name, 'Registered Agent Name/Address'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + row.REI + \
            '_SoS_Website_Record.png", "SoS Website Record")'
        doc_df.loc[row.name, 'Other Associated Document'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + row.REI + \
            '_SoS_Website_Record.png", "SoS Website Record")'

    # New York
    #TODO: Docs need to be manually extracted
    # load output below
    NY_df = pd.read_csv('step_4_work/NY/NY_ownership_results.csv', dtype='str')
    NY_df['IMPAQ_ID'] = NY_df['IMPAQ_ID'].astype('int')
    NY_df = NY_df.loc[NY_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    # Add in REI
    #NY_df = NY_df.merge(ori_df[['REI','IMPAQ_ID']],on='IMPAQ_ID',how='left')
    NY_df.index = NY_df['IMPAQ_ID']
    # note website record for all Montana matches
    for i,row in NY_df.loc[NY_df['SoS_record'].isna() == False].iterrows():
        doc_df.loc[row.name, 'Establishment Legal Entity'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + row.REI + \
            '_SoS_Website_Record.png", "SoS Website Record")'
        doc_df.loc[row.name, 'Registered Agent Name/Address'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + row.REI + \
            '_SoS_Website_Record.png", "SoS Website Record")'
        doc_df.loc[row.name, 'Other Associated Document'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + row.REI + \
            '_SoS_Website_Record.png", "SoS Website Record")'

    # South Dakota
    SD_df = pd.read_csv('step_4_work/SD/SD_FDA_matches.csv', dtype='str')
    SD_df['IMPAQ_ID'] = SD_df['IMPAQ_ID'].astype('int')
    SD_df = SD_df.loc[SD_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    SD_df = SD_df.merge(ori_df[['REI','IMPAQ_ID']],on='IMPAQ_ID',how='left')
    SD_df.index = SD_df['IMPAQ_ID']
    dload_df = pd.read_csv('step_4_work/SD/SD_docs_found.csv', dtype='str')
    dload_df['IMPAQ_ID'] = dload_df['IMPAQ_ID'].astype('int')
    dload_df = dload_df.loc[dload_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    # read nested lists within docs found file, and deduplicate
    dload_df['doc_types'] = dload_df['doc_types'].apply(literal_eval).apply(lambda x: list(set(x)))
    # logic for documentation choices
    # legal entity: registraion, then any other doc
    # agent details: notice of change, then annual report, then any other doc
    # other: any other docs not used
    for i,row in SD_df.loc[SD_df['SoS_record'].isna() == False].iterrows():
        docs = dload_df.loc[dload_df['IMPAQ_ID']==row.IMPAQ_ID, 'doc_types'].values[0]
        def _get_ext(type):
            if type !='Website Record' and type !='Website_Record':
                return('.pdf')
            else:
                return('.png')
        # legal entity
        if 'Initial Filing' in docs:
            doc_type = 'Initial Filing'
        else:
            doc_type = docs[0]
        ext = _get_ext(doc_type)
        doc_df.loc[row.name, 'Establishment Legal Entity'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + str(row.REI) + \
            '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'
        # agent details
        doc_type= 'Website_Record'
        ext = _get_ext(doc_type)
        doc_df.loc[row.name, 'Registered Agent Name/Address'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + str(row.REI) + \
            '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'
        # other docs
        # make sure its a different doc
        if len(docs) != 1:
            temp_docs = [i for i in docs if i!= doc_type and i != 'Cancellation']
            doc_type = temp_docs[0]
            ext = _get_ext(doc_type)
            doc_df.loc[row.name, 'Other Associated Document'] = '=HYPERLINK("' +  \
                './documentation/Existing Retailers/' + str(row.REI) + \
                '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'


    # Washington
    wa_df = pd.read_csv('step_4_work/WA/WA_ownership_results.csv', dtype='str')
    wa_df['IMPAQ_ID'] = wa_df['IMPAQ_ID'].astype('int')
    wa_df = wa_df.loc[wa_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    wa_df = wa_df.merge(ori_df[['REI','IMPAQ_ID']],on='IMPAQ_ID',how='left')
    wa_df.index = wa_df['IMPAQ_ID']
    dload_df = pd.read_csv('step_4_work/WA/WA_docs_found.csv', dtype='str')
    dload_df['IMPAQ_ID'] = dload_df['IMPAQ_ID'].astype('int')
    dload_df = dload_df.loc[dload_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    # read nested lists within docs found file, and deduplicate
    dload_df['doc_types'] = dload_df['doc_types'].apply(literal_eval).apply(lambda x: list(set(x)))
    # logic for documentation choices
    # legal entity: registraion, then any other doc
    # agent details: notice of change, then annual report, then any other doc
    # other: any other docs not used
    for i,row in wa_df.loc[wa_df['SoS_record'].isna() == False].iterrows():
        docs = dload_df.loc[dload_df['IMPAQ_ID']==row.IMPAQ_ID, 'doc_types'].values[0]
        def _get_ext(type):
            if type !='Website Record' and type !='Website_Record':
                return('.pdf')
            else:
                return('.png')
        # legal entity
        if 'ARTICLES OF INCORPORATION' in docs:
            doc_type = 'ARTICLES OF INCORPORATION'
        elif 'CERTIFICATE OF FORMATION' in docs:
            doc_type = 'CERTIFICATE OF FORMATION'
        else:
            doc_type = docs[0]
        ext = _get_ext(doc_type)
        doc_df.loc[row.name, 'Establishment Legal Entity'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + str(row.REI) + \
            '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'
        # agent details
        doc_type= 'Website_Record'
        ext = _get_ext(doc_type)
        doc_df.loc[row.name, 'Registered Agent Name/Address'] = '=HYPERLINK("' +  \
            './documentation/Existing Retailers/' + str(row.REI) + \
            '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'
        # other docs
        # make sure its a different doc
        if len(docs) != 1:
            temp_docs = [i for i in docs if i!= doc_type]
            doc_type = temp_docs[0]
            ext = _get_ext(doc_type)
            doc_df.loc[row.name, 'Other Associated Document'] = '=HYPERLINK("' +  \
                './documentation/Existing Retailers/' + str(row.REI) + \
                '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'


    # column list to follow
    final_cols = [
        'IMPAQ_ID',
        'REI',
        'DBA Name',
        'On Tribe Land/Associated Tribe',
        'Establishment DBA Name/Address',
        'Business Status',
        'Establishment Legal Entity',
        'Registered Agent Name/Address',
        'Other Associated Document'
    ]
    final_df = doc_df[final_cols]
    writer = pd.ExcelWriter('output/4_Existing_Sources_Documentation.xlsx', engine='xlsxwriter')
    final_df.to_excel(writer,index = False)

    # add some formatting to excel workbook
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    link_fmt = workbook.add_format()
    link_fmt.set_underline(True)
    link_fmt.set_font_color('blue')
    plain_fmt = workbook.add_format()
    plain_fmt.set_font_color('black')
    plain_fmt.set_underline(False)
    worksheet.set_column('D:I', 30, None)
    worksheet.set_column('C:C', 60, None)
    worksheet.set_column('A:B', 9, None)
    # worksheet.conditional_format('D:I', {'type': 'formula',
    #                                        'criteria': '="Could not validate"',
    #                                        'format': link_fmt})
    worksheet.conditional_format('D2:I1933', {'type': 'cell',
                                        'criteria': 'equal to',
                                        'value':    '"Could not validate"',
                                        'format':   plain_fmt})
    worksheet.conditional_format('D2:I1933', {'type': 'cell',
                                        'criteria': 'not equal to',
                                        'value':    '"Could not validate"',
                                        'format':   link_fmt})
    writer.save()
    writer.close()

    # ------------------------------------------------------------------------
    # 5. New Retailers
    # ------------------------------------------------------------------------
    new_df = pd.read_csv('step_4_work/output/full_retailer_list_w_owner_final.csv')
    new_df = new_df.loc[new_df['ori_flg']!='From Original List',:]

    # align column names with existing retailer column names
    new_df['Latitude'] = new_df['Latitude_update']
    new_df['Longitude'] = new_df['Longitude_update']
    new_df['DBA Name'] = new_df['DBA Name_update']
    new_df['County'] = new_df['County_update']

    # keep same columns as in revised data clean
    rename_cols = {
        'On Tribe Land': 'On Tribe Land',
        'Assoc Tribe': 'Tribe associated with location',
        'Assoc Res': 'Reservation associated with location',
        'biz_status': 'Business Status',
        'entity': 'Establishment Legal Entity',
        'agent_name': 'Registered Agent Name',
        'agent_address': 'Agent Address',
        'agent_city': 'Agent City',
        'agent_state': 'Agent State',
        'agent_zip': 'Agent Zip'
    }
    new_df = new_df.rename(rename_cols,axis=1)

    new_cols = ['REI', 'Miles to nearest tribal land', \
        'Nearest tribe to location', 'Nearest reservation to location', \
        'Tribal Owned ']
    for i in new_cols:
        new_df[i] = ''
    new_df['Miles to nearest tribal land'] = 0
    new_df['Tribal Owned '] = 'Unknown'

    new_df = new_df[[i for i in clean_df.columns if i != 'EST_COMMENTS' and
        '- Change Log' not in i and '- Updated' not in i]]
    # populate REI, biz stat, tribe land columns
    new_df['REI']='New Retailer'
    new_df['Business Status']='In Operation'
    new_df['On Tribe Land']='Yes'

    new_df.to_csv('output/5_New_Retailers.csv',index = False)

    #------------------------------------------------------------------------------
    # 6. Raw Nielsen Supporting Data for New Retailers
    #------------------------------------------------------------------------------
    niel_df = pd.read_csv('step_4_work/output/full_retailer_list_w_owner_final.csv')
    niel_df = niel_df.loc[niel_df['ori_flg']!='From Original List',:]
    niel_ids = niel_df.Niel_id.astype('int').tolist()

    raw_niel = pd.read_csv('input/raw_Nielsen_POS_data_full.csv', low_memory=False)
    raw_niel['Sells Tobacco Products?'] = 'Yes'
    raw_niel = raw_niel.rename({'TDLinx Store Code':'Nielsen ID'},axis=1)
    raw_niel = raw_niel.loc[[i in niel_ids for i in raw_niel['Nielsen ID'].tolist()],:]
    raw_niel = niel_df[['IMPAQ_ID','Niel_id']].merge(raw_niel, how='inner', left_on='Niel_id', right_on='Nielsen ID')
    raw_niel = raw_niel.drop('Niel_id', axis=1)
    raw_niel.index = raw_niel['IMPAQ_ID']
    raw_niel.to_csv('output/6_Nielsen_Supporting_Data.csv',index=False)

    # ------------------------------------------------------------------------
    # 7. Sources and Documentation - New Retailers
    # ------------------------------------------------------------------------
    # create a documentation df
    doc_df = new_df[['IMPAQ_ID','DBA Name','Miles to nearest tribal land']].merge(ori_df[['REI']], right_index=True, left_on='IMPAQ_ID',how='left')
    doc_df = doc_df.merge(ggl_df[['id','match','url']], how='left', right_on='id',left_on='IMPAQ_ID')
    doc_df = doc_df.merge(verif_df[['est_id','Manual Result']], how='left', right_on='est_id', left_on='IMPAQ_ID')
    doc_df = doc_df.drop('id', axis=1)
    doc_df.index =doc_df['IMPAQ_ID']
    # Tribal GIS Overlays
    doc_df['Overlay Path'] =  '.\\output\\documentation\\Tribal Boundary GIS Overlays\\' \
        + doc_df['IMPAQ_ID'].astype('int').astype('str') + '_tribe_bound_overlay.html'

    # save url's in csv file
    def make_hyperlink(value, text):
        return '=HYPERLINK("%s", "%s")' % (value, text)

    doc_df.loc[doc_df['Miles to nearest tribal land'].isna() == False,'On Tribe Land/Associated Tribe'] = \
        doc_df.loc[doc_df['Miles to nearest tribal land'].isna() == False,'Overlay Path'].apply(lambda x: make_hyperlink(x, 'Tribal Boundary GIS Overlay'))
    doc_df.loc[doc_df['Miles to nearest tribal land'].isna() == True,'On Tribe Land/Associated Tribe'] = 'Could not validate'

    doc_df['Establishment DBA Name/Address'] = '=HYPERLINK("' +  \
        '6_Nielsen_Supporting_Data.csv", "Nielsen POS Data, Nielsen ID #' \
         + raw_niel['Nielsen ID'].astype('str') + '")'
    doc_df['Business Status'] = '=HYPERLINK("' +  \
        '6_Nielsen_Supporting_Data.csv", "Nielsen POS Data, Nielsen ID #' \
         + raw_niel['Nielsen ID'].astype('str') + '")'

    # legal ownership coming later
    doc_df['REI'] = 'New retailer'
    doc_df['Establishment Legal Entity'] = ''
    doc_df['Registered Agent Name/Address'] = ''
    doc_df['Other Associated Document'] = ''

    # read in links for ownership documentation
    # same code as in existing retailers one
    # manual links
    manual_df = pd.read_csv('output/documentation_links.csv', dtype='str')
    manual_df = manual_df.rename({
        'est_entity': 'Establishment Legal Entity',
        'est_agent': 'Registered Agent Name/Address',
        'est_other': 'Other Associated Document'
    }, axis=1)
    manual_df['IMPAQ_ID'] = manual_df['IMPAQ_ID'].astype('int')
    manual_df = manual_df.loc[manual_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    manual_df.index = manual_df['IMPAQ_ID']
    doc_df.update(manual_df)

    # Arizona
    az_df = pd.read_csv('step_4_work/AZ/AZ_FDA_matches.csv', dtype='str')
    az_df['IMPAQ_ID'] = az_df['IMPAQ_ID'].astype('int')
    az_df = az_df.loc[az_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    az_df = az_df.merge(ori_df[['REI','IMPAQ_ID']],on='IMPAQ_ID',how='left')
    az_df.index = az_df['IMPAQ_ID']
    dload_df = pd.read_csv('step_4_work/AZ/AZ_docs_found.csv', dtype='str')
    dload_df['IMPAQ_ID'] = dload_df['IMPAQ_ID'].astype('int')
    dload_df = dload_df.loc[dload_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    # read nested lists within docs found file
    dload_df['doc_types'] = dload_df['doc_types'].apply(literal_eval)
    # logic for documentation choices
    # legal entity: registraion, then any other doc
    # agent details: SI-Complete, then any other doc
    # other: any other docs not used
    for i,row in az_df.loc[az_df['SoS_record'].isna() == False].iterrows():
        docs = dload_df.loc[dload_df['IMPAQ_ID']==row.IMPAQ_ID, 'doc_types'].values[0]
        def _get_ext(type):
            if type !='Website Record' and type !='Website_Record':
                return('.pdf')
            else:
                return('.png')
        # legal entity
        if 'Website_Record' in docs:
            doc_type = 'Website_Record'
        else:
            doc_type = docs[0]
        ext = _get_ext(doc_type)
        doc_df.loc[row.name, 'Establishment Legal Entity'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'
        # agent details
        doc_type= 'Website_Record'
        ext = _get_ext(doc_type)
        doc_df.loc[row.name, 'Registered Agent Name/Address'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'
        # other docs
        if 'Articles of Organization' in docs:
            doc_type = 'Articles of Organization'
        if len(docs) != 1:
            ext = _get_ext(doc_type)
            doc_df.loc[row.name, 'Other Associated Document'] = '=HYPERLINK("' +  \
                './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
                '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'

    # California
    ca_df = pd.read_csv('step_4_work/CA/CA_FDA_matches.csv', dtype='str')
    ca_df['IMPAQ_ID'] = ca_df['IMPAQ_ID'].astype('int')
    ca_df = ca_df.loc[ca_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    ca_df.index = ca_df['IMPAQ_ID']
    dload_df = pd.read_csv('step_4_work/CA/CA_docs_found.csv', dtype='str')
    dload_df['IMPAQ_ID'] = dload_df['IMPAQ_ID'].astype('int')
    dload_df = dload_df.loc[dload_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    # read nested lists within docs found file
    dload_df['doc_types'] = dload_df['doc_types'].apply(literal_eval)
    # logic for documentation choices
    # legal entity: registraion, then any other doc
    # agent details: SI-Complete, then any other doc
    # other: any other docs not used
    for i,row in ca_df.loc[ca_df['SoS_record'].isna() == False].iterrows():
        docs = dload_df.loc[dload_df['IMPAQ_ID']==row.IMPAQ_ID, 'doc_types'].values[0]
        def _get_ext(type):
            if type !='Website Record' and type !='Website_Record':
                return('.pdf')
            else:
                return('.png')
        # legal entity
        if 'REGISTRATION' in docs:
            doc_type = 'REGISTRATION'
        else:
            doc_type = docs[0]
        ext = _get_ext(doc_type)
        doc_df.loc[row.name, 'Establishment Legal Entity'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'
        # agent details
        doc_type= 'Website_Record'
        ext = _get_ext(doc_type)
        doc_df.loc[row.name, 'Registered Agent Name/Address'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'
        # other docs
        if 'SI-COMPLETE' in docs and 'REGISTRATION' in docs:
            doc_type = docs[0]
        elif len(docs) != 1:
            doc_type = docs[1]
        if len(docs) != 1:
            ext = _get_ext(doc_type)
            doc_df.loc[row.name, 'Other Associated Document'] = '=HYPERLINK("' +  \
                './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
                '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'

    # Michigan
    MI_df = pd.read_csv('step_4_work/MI/MI_FDA_matches.csv', dtype='str')
    MI_df['IMPAQ_ID'] = MI_df['IMPAQ_ID'].astype('int')
    MI_df = MI_df.loc[MI_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    MI_df = MI_df.merge(ori_df[['REI','IMPAQ_ID']],on='IMPAQ_ID',how='left')
    MI_df.index = MI_df['IMPAQ_ID']
    dload_df = pd.read_csv('step_4_work/MI/MI_docs_found.csv', dtype='str')
    dload_df['IMPAQ_ID'] = dload_df['IMPAQ_ID'].astype('int')
    dload_df = dload_df.loc[dload_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    dload_df['doc_types'] = dload_df['doc_types'].fillna("['Website_Record']")
    # read nested lists within docs found file
    dload_df['doc_types'] = dload_df['doc_types'].apply(literal_eval)
    # logic for documentation choices
    # legal entity: registraion, then any other doc
    # agent details: SI-Complete, then any other doc
    # other: any other docs not used
    for i,row in MI_df.loc[MI_df['SoS_record'].isna() == False].iterrows():
        docs = dload_df.loc[dload_df['IMPAQ_ID']==row.IMPAQ_ID, 'doc_types'].values[0]
        def _get_ext(type):
            if type !='Website Record' and type !='Website_Record':
                return('.pdf')
            else:
                return('.png')
        # legal entity
        if 'Website_Record' in docs:
            doc_type = 'Website_Record'
        else:
            doc_type = docs[0]
        ext = _get_ext(doc_type)
        doc_df.loc[row.name, 'Establishment Legal Entity'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'
        # agent details
        doc_type= 'Website_Record'
        ext = _get_ext(doc_type)
        doc_df.loc[row.name, 'Registered Agent Name/Address'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'
        # other docs
        if 'ARTICLES OF ORGANIZATION' in docs:
            doc_type = 'ARTICLES OF ORGANIZATION'
        if len(docs) != 1:
            ext = _get_ext(doc_type)
            doc_df.loc[row.name, 'Other Associated Document'] = '=HYPERLINK("' +  \
                './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
                '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'
    # Minnesota
    # load output below
    MN_df = pd.read_csv('step_4_work/MN/MN_FDA_matches.csv', dtype='str')
    MN_df['IMPAQ_ID'] = MN_df['IMPAQ_ID'].astype('int')
    MN_df = MN_df.loc[MN_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    # Add in REI
    #MN_df = MN_df.merge(ori_df[['REI','IMPAQ_ID']],on='IMPAQ_ID',how='left')
    MN_df.index = MN_df['IMPAQ_ID']
    # note website record for all Minnesota matches
    for i,row in MN_df.loc[MN_df['SoS_record'].isna() == False].iterrows():
        doc_df.loc[row.name, 'Establishment Legal Entity'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_Website_Record.png", "SoS Website Record")'
        doc_df.loc[row.name, 'Registered Agent Name/Address'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_Website_Record.png", "SoS Website Record")'
        doc_df.loc[row.name, 'Other Associated Document'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_Website_Record.png", "SoS Website Record")'

    # Montana
    # load output below
    MT_df = pd.read_csv('step_4_work/MT/MT_FDA_matches.csv', dtype='str')
    MT_df['IMPAQ_ID'] = MT_df['IMPAQ_ID'].astype('int')
    MT_df = MT_df.loc[MT_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    # Add in REI
    MT_df = MT_df.merge(ori_df[['REI','IMPAQ_ID']],on='IMPAQ_ID',how='left')
    MT_df.index = MT_df['IMPAQ_ID']
    # note website record for all Montana matches
    for i,row in MT_df.loc[MT_df['SoS_record'].isna() == False].iterrows():
        doc_df.loc[row.name, 'Establishment Legal Entity'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_Website_Record.png", "SoS Website Record")'
        doc_df.loc[row.name, 'Registered Agent Name/Address'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_Website_Record.png", "SoS Website Record")'
        doc_df.loc[row.name, 'Other Associated Document'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_Website_Record.png", "SoS Website Record")'

    # New Mexico
    # load output below
    NM_df = pd.read_csv('step_4_work/NM/NM_FDA_matches.csv', dtype='str')
    NM_df['IMPAQ_ID'] = NM_df['IMPAQ_ID'].astype('int')
    NM_df = NM_df.loc[NM_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    # Add in REI
    #NM_df = NM_df.merge(ori_df[['REI','IMPAQ_ID']],on='IMPAQ_ID',how='left')
    NM_df.index = NM_df['IMPAQ_ID']
    # note website record for all Montana matches
    for i,row in NM_df.loc[NM_df['SoS_record'].isna() == False].iterrows():
        doc_df.loc[row.name, 'Establishment Legal Entity'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_Website_Record.png", "SoS Website Record")'
        doc_df.loc[row.name, 'Registered Agent Name/Address'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_Website_Record.png", "SoS Website Record")'
        doc_df.loc[row.name, 'Other Associated Document'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_Website_Record.png", "SoS Website Record")'

    # New York
    #TODO: Docs need to be manually extracted
    # load output below
    NY_df = pd.read_csv('step_4_work/NY/NY_ownership_results.csv', dtype='str')
    NY_df['IMPAQ_ID'] = NY_df['IMPAQ_ID'].astype('int')
    NY_df = NY_df.loc[NY_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    # Add in REI
    #NY_df = NY_df.merge(ori_df[['REI','IMPAQ_ID']],on='IMPAQ_ID',how='left')
    NY_df.index = NY_df['IMPAQ_ID']
    # note website record for all Montana matches
    for i,row in NY_df.loc[NY_df['SoS_record'].isna() == False].iterrows():
        doc_df.loc[row.name, 'Establishment Legal Entity'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_Website_Record.png", "SoS Website Record")'
        doc_df.loc[row.name, 'Registered Agent Name/Address'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_Website_Record.png", "SoS Website Record")'
        doc_df.loc[row.name, 'Other Associated Document'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_Website_Record.png", "SoS Website Record")'

    # Oklahoma
    # run state_scrapers/OK/OK_3_fetch_document
    # load output below
    ok_df = pd.read_csv('step_4_work/OK/OK_FDA_matches.csv', dtype='str')
    ok_df['IMPAQ_ID'] = ok_df['IMPAQ_ID'].astype('int')
    ok_df = ok_df.loc[ok_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    ok_df.index = ok_df['IMPAQ_ID']
    # note website record for all oklahoma matches
    for i,row in ok_df.loc[ok_df['SoS_record'].isna() == False].iterrows():
        doc_df.loc[row.name, 'Establishment Legal Entity'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_Website_Record.png", "SoS Website Record")'
        doc_df.loc[row.name, 'Registered Agent Name/Address'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_Website_Record.png", "SoS Website Record")'
        doc_df.loc[row.name, 'Other Associated Document'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_Website_Record.png", "SoS Website Record")'

    # South Dakota
    SD_df = pd.read_csv('step_4_work/SD/SD_FDA_matches.csv', dtype='str')
    SD_df['IMPAQ_ID'] = SD_df['IMPAQ_ID'].astype('int')
    SD_df = SD_df.loc[SD_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    SD_df = SD_df.merge(ori_df[['REI','IMPAQ_ID']],on='IMPAQ_ID',how='left')
    SD_df.index = SD_df['IMPAQ_ID']
    dload_df = pd.read_csv('step_4_work/SD/SD_docs_found.csv', dtype='str')
    dload_df['IMPAQ_ID'] = dload_df['IMPAQ_ID'].astype('int')
    dload_df = dload_df.loc[dload_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    # read nested lists within docs found file, and deduplicate
    dload_df['doc_types'] = dload_df['doc_types'].apply(literal_eval).apply(lambda x: list(set(x)))
    # logic for documentation choices
    # legal entity: registraion, then any other doc
    # agent details: notice of change, then annual report, then any other doc
    # other: any other docs not used
    for i,row in SD_df.loc[SD_df['SoS_record'].isna() == False].iterrows():
        docs = dload_df.loc[dload_df['IMPAQ_ID']==row.IMPAQ_ID, 'doc_types'].values[0]
        def _get_ext(type):
            if type !='Website Record' and type !='Website_Record':
                return('.pdf')
            else:
                return('.png')
        # legal entity
        if 'Initial Filing' in docs:
            doc_type = 'Initial Filing'
        else:
            doc_type = docs[0]
        ext = _get_ext(doc_type)
        doc_df.loc[row.name, 'Establishment Legal Entity'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'
        # agent details
        doc_type= 'Website_Record'
        ext = _get_ext(doc_type)
        doc_df.loc[row.name, 'Registered Agent Name/Address'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'
        # other docs
        # make sure its a different doc
        if len(docs) != 1:
            temp_docs = [i for i in docs if i!= doc_type and i != 'Cancellation']
            doc_type = temp_docs[0]
            ext = _get_ext(doc_type)
            doc_df.loc[row.name, 'Other Associated Document'] = '=HYPERLINK("' +  \
                './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
                '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'

    # Washington
    wa_df = pd.read_csv('step_4_work/WA/WA_ownership_results.csv', dtype='str')
    wa_df['IMPAQ_ID'] = wa_df['IMPAQ_ID'].astype('int')
    wa_df = wa_df.loc[wa_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    wa_df.index = wa_df['IMPAQ_ID']
    dload_df = pd.read_csv('step_4_work/WA/WA_docs_found.csv', dtype='str')
    dload_df['IMPAQ_ID'] = dload_df['IMPAQ_ID'].astype('int')
    dload_df = dload_df.loc[dload_df['IMPAQ_ID'].isin(doc_df.IMPAQ_ID)].reset_index(drop=True)
    # read nested lists within docs found file, and deduplicate
    dload_df['doc_types'] = dload_df['doc_types'].apply(literal_eval).apply(lambda x: list(set(x)))
    # logic for documentation choices
    # legal entity: registraion, then any other doc
    # agent details: notice of change, then annual report, then any other doc
    # other: any other docs not used
    for i,row in wa_df.loc[wa_df['SoS_record'].isna() == False].iterrows():
        docs = dload_df.loc[dload_df['IMPAQ_ID']==row.IMPAQ_ID, 'doc_types'].values[0]
        def _get_ext(type):
            if type !='Website Record' and type !='Website_Record':
                return('.pdf')
            else:
                return('.png')
        # legal entity
        if 'ARTICLES OF INCORPORATION' in docs:
            doc_type = 'ARTICLES OF INCORPORATION'
        elif 'CERTIFICATE OF FORMATION' in docs:
            doc_type = 'CERTIFICATE OF FORMATION'
        else:
            doc_type = docs[0]
        ext = _get_ext(doc_type)
        doc_df.loc[row.name, 'Establishment Legal Entity'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'
        # agent details
        doc_type= 'Website_Record'
        ext = _get_ext(doc_type)
        doc_df.loc[row.name, 'Registered Agent Name/Address'] = '=HYPERLINK("' +  \
            './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
            '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'
        # other docs
        # make sure its a different doc
        if len(docs) != 1:
            temp_docs = [i for i in docs if i!= doc_type]
            doc_type = temp_docs[0]
            ext = _get_ext(doc_type)
            doc_df.loc[row.name, 'Other Associated Document'] = '=HYPERLINK("' +  \
                './documentation/New Retailers/IMPAQID_' + str(row.IMPAQ_ID) + \
                '_SoS_'+ doc_type + ext + '",' + '"SoS ' + doc_type + '")'

    # column list to follow
    final_cols = [
        'IMPAQ_ID',
        'REI',
        'DBA Name',
        'On Tribe Land/Associated Tribe',
        'Establishment DBA Name/Address',
        'Business Status',
        'Establishment Legal Entity',
        'Registered Agent Name/Address',
        'Other Associated Document'
    ]
    final_df = doc_df[final_cols]
    writer = pd.ExcelWriter('output/7_New_Sources_Documentation.xlsx', engine='xlsxwriter')
    final_df.to_excel(writer,index = False)

    # add some formatting to excel workbook
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    link_fmt = workbook.add_format()
    link_fmt.set_underline(True)
    link_fmt.set_font_color('blue')
    plain_fmt = workbook.add_format()
    plain_fmt.set_font_color('black')
    plain_fmt.set_underline(False)
    worksheet.set_column('D:I', 35, None)
    worksheet.set_column('C:C', 37, None)
    worksheet.set_column('A:A', 9, None)
    worksheet.set_column('A:A', 14, None)
    # worksheet.conditional_format('D:I', {'type': 'formula',
    #                                        'criteria': '="Could not validate"',
    #                                        'format': link_fmt})
    worksheet.conditional_format('D2:I1933', {'type': 'cell',
                                        'criteria': 'equal to',
                                        'value':    '"Could not validate"',
                                        'format':   plain_fmt})
    worksheet.conditional_format('D2:I1933', {'type': 'cell',
                                        'criteria': 'not equal to',
                                        'value':    '"Could not validate"',
                                        'format':   link_fmt})
    writer.save()
    writer.close()
if __name__ == "__main__":
    main()

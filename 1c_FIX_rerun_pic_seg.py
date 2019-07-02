# error caused a segment of retailers to get wrong retailers' pictures
# fixing that in this file
# original 1C should function on rerun, this doesn't need to be rerun with future
# replications

import unicodedata
import pandas as pd
import numpy as np
import urllib.request
import urllib.parse
import json
from PIL import Image

# load in 1st iteration of manual coding
ori_df =  pd.read_csv('step_1_work/output/retailers_for_manual_verify.csv')
code_df = pd.read_csv('step_1_work/output/retailers_for_manual_verify_coded.csv')
mrg_df = ori_df.merge(code_df[['est_id', 'Manual Result']], how='left', on='est_id')

# find those stores requiring manual verificaiton that have not received it
mrg_df = mrg_df.loc[(mrg_df['Manual Result'].isna()) & ((mrg_df['match']=='Manually Verify Pic'))]

# find matches in google output for these
df = pd.read_csv('step_1_work/output/documentation/google_places_output.csv')
df['est_id']=df['est_id'].astype('int')
# turns out there's only 6 rows that messed up
coord = mrg_df[['est_id','Full Address','Latitude','Longitude']].merge(df, how = 'left', on = ['est_id'])
# my api key
key = 'AIzaSyB7WmtDmJrnMyKqoWWPqn9iE7IqSEaq-BQ'
for i in coord.iterrows():
    print(i[1]['est_id'])
    # check if they have street view close by
    meta_url = 'https://maps.googleapis.com/maps/api/streetview/metadata?size=1500x600&location=' + \
        str(i[1]['Latitude']) + "," + str(i[1]['Longitude']) + '&key=' + key
    req = urllib.request.Request(meta_url)
    f= urllib.request.urlopen(req)
    log = json.load(f)
    if log['status'] == 'OK':
        # if so, we go to retrieve it
        pano_id= log['pano_id']
        images = []
        for j in np.arange(0,360, step = 60):
            url = 'https://maps.googleapis.com/maps/api/streetview?size=1500x600&pano=' + \
                pano_id + '&heading=' + str(j) + \
                '&fov=60&source=outdoor&key=' + key
            # works better with pano_id I think
            #url = 'https://maps.googleapis.com/maps/api/streetview?size=1500x600&location=' + \
                #str(i[1][0]) + "," + str(i[1][1]) + '&heading=' + str(j) + \
                #'&fov=60&source=outdoor&key=' + key
            fname =  '_angle_' + str(j)
            urllib.request.urlretrieve(url, './step_1_work/output/pictures/temp/'+ fname + '.jpg')
            images.append(Image.open('./step_1_work/output/pictures/temp/'+ fname + '.jpg'))
        # then stitch together the pics into a panorama
        widths, heights = zip(*(i.size for i in images))
        total_widths= round(sum(widths))
        max_height = max(heights)
        new_im = Image.new('RGB', (total_widths, max_height))
        x_offset = 0
        for im in images:
            new_im.paste(im, (x_offset,0))
            x_offset += im.size[0]
            # some google names are weird, need to make sure they are all ascii chars
            sname = str(unicodedata.normalize('NFKD',i[1]['bizname']).encode('ascii','replace'))[2:-1]
            fname = "est" + str(i[1]['est_id']) + "_" + "cand" + str(i[1]['cand_id']) \
                + "_" + sname.replace('/','_').replace('?','').replace(':','').replace('"','') # need to make sure there's no filename forbidden chars
        new_im.save('./step_1_work/output/pictures/'+ fname + '.jpg')
        # WHERE I LEFT OFF: getting panorama's from up and down the street
        coord.loc[i[0], 'found_pic'] = 1
    else:
        # if no pic found with coordinates, will try with address
        input = i[1]['Full Address'].replace(' ','%20')
        meta_url = 'https://maps.googleapis.com/maps/api/streetview/metadata?size=1500x600' + \
         '&location=' + input + '&key=' + key
        req = urllib.request.Request(meta_url)
        f= urllib.request.urlopen(req)
        log = json.load(f)
        if log['status'] == 'OK':
            # if so, we go to retrieve it
            pano_id= log['pano_id']
            images = []
            for j in np.arange(0,360, step = 60):
                url = 'https://maps.googleapis.com/maps/api/streetview?size=1500x600&pano=' + \
                    pano_id + '&heading=' + str(j) + \
                    '&fov=60&source=outdoor&key=' + key
                # works better with pano_id I think
                #url = 'https://maps.googleapis.com/maps/api/streetview?size=1500x600&location=' + \
                    #str(i[1][0]) + "," + str(i[1][1]) + '&heading=' + str(j) + \
                    #'&fov=60&source=outdoor&key=' + key
                fname =  '_angle_' + str(j)
                urllib.request.urlretrieve(url, './step_1_work/output/pictures/temp/'+ fname + '.jpg')
                images.append(Image.open('./step_1_work/output/pictures/temp/'+ fname + '.jpg'))
            # then stitch together the pics into a panorama
            widths, heights = zip(*(i.size for i in images))
            total_widths= round(sum(widths))
            max_height = max(heights)
            new_im = Image.new('RGB', (total_widths, max_height))
            x_offset = 0
            for im in images:
                new_im.paste(im, (x_offset,0))
                x_offset += im.size[0]
            # some google names are weird, need to make sure they are all ascii chars
            sname = str(unicodedata.normalize('NFKD',i[1]['name']).encode('ascii','replace'))[2:-1]
            fname = "est" + str(i[1]['est_id']) + "_" + "cand" + str(i[1]['cand_id']) \
                + "_" + sname.replace('/','_').replace('?','').replace(':','').replace('"','') # need to make sure there's no filename forbidden chars
            new_im.save('./step_1_work/output/pictures/'+ fname + '.jpg')
            coord.loc[i[0], 'found_pic'] = 1
        else:
            coord.loc[i[0], 'found_pic'] = 0
coord.to_csv('retailers_for_manual_verify_fix.csv')

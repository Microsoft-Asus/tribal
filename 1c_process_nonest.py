# Separating this into part 2 so I don't have to keep using API calls to continue development
# now that we have dataframe of possible matches, see what we can
# unearth about each match
import unicodedata
import pandas as pd
import numpy as np
import urllib.request
import urllib.parse
import json
from PIL import Image

# my api key
key = 'AIzaSyB7WmtDmJrnMyKqoWWPqn9iE7IqSEaq-BQ'

# load sample output data
df = pd.read_pickle('./step_1_work/output/google_output.pkl')
df['est_id']=df['est_id'].astype('int')
ret_df = pd.read_pickle('./step_1_work/output/stores_est.pkl')
# get street view photo for those retailers with long and latitude
coord = df[['est_id', 'cand_id']].merge(ret_df.loc[ret_df['match']=='Not Validated',['est_id']], on='est_id')
coord = coord.merge(df, how = 'left', on = ['est_id','cand_id'])
coord = coord[['geometry.location.lat','geometry.location.lng', 'est_id',
    'place_id','cand_id','name']]

coord['found_pic'] = np.nan
coord.reset_index(drop= True, inplace= True)
for i in coord[0:228].iterrows():
    # check if they have street view close by
    meta_url = 'https://maps.googleapis.com/maps/api/streetview/metadata?size=1500x600&location=' + \
        str(i[1][0]) + "," + str(i[1][1]) + '&key=' + key
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
        # WHERE I LEFT OFF: getting panorama's from up and down the street
        coord.loc[i[0], 'found_pic'] = 1
    else:
        # if no pic found with coordinates, will try with address
        input = ret_df.loc[i[1]['est_id'], 'Full Address'].replace(' ','%20')
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

coord['est_id']= coord['est_id'].astype('int')
ret_df = ret_df.merge(coord[['est_id','found_pic']].drop_duplicates(), how = 'left', on='est_id')
ret_df.loc[ret_df['found_pic'] == 1 , 'match'] = 'Manually Verify Pic'
ret_df.loc[ret_df['found_pic'] == 0 , 'match'] = 'Not Validated'
ret_df['match'] = ret_df['match'].fillna('Not Validated')

# save results
ret_df.to_csv('./step_1_work/output/retailers_for_manual_verify.csv', index=False)

# pictures in ret_df were then manually examined for the presence or absence of
# a commerical building in the vicinity of the streetview picture
# file 1d takes the completed results of that file, and cleans it
# file 1e then merges the results back and proceeds

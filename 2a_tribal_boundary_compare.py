# Take geocoded retailers and do a tribal boundary comparisons to determine
# if retailers are within tribal borders and if so, what tribe/reservation
#def main():
import pandas as pd
import numpy as np
import geopandas as gp
from shapely.geometry import Point
# read geocoded retailers with matches
df = pd.read_csv('step_1_work/output/retailers_name_addr_update.csv')
df['Coordinates'] = list(zip(df.Longitude_update, df.Latitude_update))
df['Coordinates'] = df['Coordinates'].apply(Point)
df = gp.GeoDataFrame(df, geometry='Coordinates')
df['On Tribe Land'] = 'No'
df['Miles to Nearest Tribe'] = np.nan
df['Assoc Tribe'] = np.nan
df['Assoc Res'] = np.nan
df['Nearest Tribe'] = np.nan
df['Nearest Res'] = np.nan

# read in tribal boundary shapefile
border = gp.read_file('input/aiannah shapefiles/tl_2018_us_aiannh.shp')

# remove shapes not part of "Tribal Country"
border = border.loc[
    (border['CLASSFP'] == "D1") |
    (border['CLASSFP'] == "D2") |
    (border['CLASSFP'] == "D3") |
    (border['CLASSFP'] == "D0") |
    (border['CLASSFP'] == "F1") |
    (border['CLASSFP'] == "D5") |
    (border['CLASSFP'] == "D8"), :
]
bord_buff = border.copy()
bord_buff.geometry = border.buffer(1/65.32411155)
# Check for overlap between retailer locations and tribal borders
def within_shape(shp, pnt):
    return(pnt.intersects(shp))

# Create data set of those with valid coordinates
for i in df.loc[(df['Longitude']!=0) & (df['Longitude'].isna()==False),:].index:
    if i % 100 == 0:
         print(i)
    coord = df.loc[i,'Coordinates']
    # check exact shape
    match_id = border.geometry.apply(within_shape, args=[coord])
    if len(border[match_id])>0:
        match=border.loc[match_id]
        match.reset_index(inplace=True, drop=True)
        df.loc[i,'On Tribe Land'] = 'Yes'
        df.loc[i,'Miles to Nearest Tribe'] = 0
        df.loc[i,'Assoc Tribe'] = match.loc[0,'NAME']
        df.loc[i,'Assoc Res'] = match.loc[0,'NAMELSAD']
    else:

        # # check within one mile
        # match_id = bord_buff.geometry.apply(within_shape, args=[coord])
        # if len(bord_buff[match_id])>0:
        #     match=bord_buff.loc[match_id]
        #     match.reset_index(inplace=True, drop=True)
        #     df.loc[i,'On Tribe Land'] = 'Within 1 mile'
        #     df.loc[i,'Assoc Tribe'] = match.loc[0,'NAME']
        #     df.loc[i,'Assoc Res'] = match.loc[0,'NAMELSAD']

        # going to report distance to nearest reservation instead of one mile cutoff
        min_dist = np.min([coord.distance(b) for b in border.geometry])
        match = border.iloc[np.argmin([coord.distance(b) for b in border.geometry]),:]
        df.loc[i,'On Tribe Land'] = 'No'
        # convert from degrees to miles
        df.loc[i,'Miles to Nearest Tribe'] = min_dist*65.32411155
        df.loc[i,'Nearest Tribe'] = match.loc['NAME']
        df.loc[i,'Nearest Res'] = match.loc['NAMELSAD']

# note those retailers without Coordinates
df.loc[(df['Longitude']==0) | (df['Longitude'].isna()==True),'On Tribe Land'] = 'Unknown'
df.loc[(df['Longitude']==0) | (df['Longitude'].isna()==True),'Assoc Tribe'] = 'Unknown'
df.loc[(df['Longitude']==0) | (df['Longitude'].isna()==True),'Assoc Res'] = 'Unknown'

# save resulting data DataFrame
df.to_csv('step_2_work/tribal_retailers.csv', index = False)

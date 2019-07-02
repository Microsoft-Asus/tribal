# Take geocoded retailers and do a tribal boundary comparisons to determine
# if retailers are within tribal borders and if so, what tribe/reservation
import pandas as pd
import numpy as np
import geopandas as gp
from shapely.geometry import Point

# read geocoded retailers with matches
df = pd.read_csv('step_3_work/output/geocoded_retailers.csv')
df = df.loc[df['match']==True]
df.reset_index(inplace=True, drop =True)
df['Coordinates'] = list(zip(df.lon, df.lat))
df['Coordinates'] = df['Coordinates'].apply(Point)
df = gp.GeoDataFrame(df, geometry='Coordinates')
df['On Tribe Land'] = 'No'
df['Assoc Tribe'] = np.nan
df['Assoc Res'] = np.nan
# read in tribal boundary shapefile
border = gp.read_file('input/aiannah shapefiles/tl_2018_us_aiannh.shp')
import pdb; pdb.set_trace()
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
# Check for overlap between retailer locations and tribal borders
def within_shape(shp, pnt):
    return(pnt.intersects(shp))
for i in range(len(df)):
    if i % 1000 == 0:
         print(i)
    coord = df.loc[i,'Coordinates']
    match_id = border.geometry.apply(within_shape, args=[coord])
    if len(border[match_id])>0:
        match=border.loc[match_id]
        match.reset_index(inplace=True, drop=True)
        df.loc[i,'On Tribe Land'] = 'Yes'
        df.loc[i,'Assoc Tribe'] = match.loc[0,'NAME']
        df.loc[i,'Assoc Res'] = match.loc[0,'NAMELSAD']

# filter to keep only those found to be on tribal Land
df = df.loc[df['On Tribe Land']=='Yes']

# save resulting data DataFrame
df.to_csv('step_3_work/output/tribal_retailers.csv', index = False)

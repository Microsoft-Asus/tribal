# Geocode retailers from Nielsen POS data with census geocoder
def main():
    import time
    import csv
    import os
    import math
    import pandas as pd
    import censusgeocode as cg
    import requests
    import datetime
    paths = create_batch_paths(0,10)

    for h,i in enumerate(paths):
        # sleep 30 seconds in between batches for minimizing risk of timing out
        time.sleep(30)
        print('Geocoding batch #' + str(h))
        start = datetime.datetime.now()
        if h == 0:
            result = cg.addressbatch(paths[h])
            df = pd.DataFrame.from_dict(result)
        else:
            df = df.append(pd.DataFrame.from_dict(cg.addressbatch(paths[h])), sort=True)
        print(datetime.datetime.now() - start)
        df.to_csv('step_3_work/output/temp/batch_'+ str(h) +'_temp.csv', index = False)

    df.to_csv('step_3_work/output/Census_geocoded_retailers.csv', index = False)
    #retailer_data = queue_batches(paths)


def create_batch_paths(start_no, end_no):
    batch_paths = []
    start = start_no
    end = end_no
    for i in range(start, end+1):
        batch_paths.append('step_3_work/batches/batch_'+str(i)+'.csv')
    return(batch_paths)


if __name__ == '__main__':
    main()

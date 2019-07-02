# file for manual functions that deals with unique quirks of
# need to be redone/re-examined in the future to be properly tailored

# function defining black lists of DBA name string values. the presence of one
# of these values in the google/fda DBA names respectively stops the update of
# the FDA DBA name with the Google name
# list is tailored to the resulting matches of the particular FDA data set,
# and should be changed if a new FDA data set is used.
def set_blists_1e():
    ggl_blist = '|'.join(['SCHOOL','GOVERNMENT','NATIONAL HISTORIC', '&', 'â€“', 'ATM ',
        'INC','LLC', "'", 'SAVON', 'DEPARTMENT','TRIBE OF', ' CO','COMANCHE','¤',
        'COMMUNITY CENTER','TONTO APACHE TRIBE','LIBRARY','SHPG','VENUE','CHAPTER',
        'GENEALOGY','W.D.','SNOQUALMIE', 'DAYS INN','QUECHAN TRIBE'])
    fda_blist = '|'.join(['LLC', 'INC', '-','/','&','â€“', "'", 'MARKET PLACE'])
    return((ggl_blist, fda_blist))

# function to accept specific matches based on manual examination of google and
# FDA data
def accept_match_1e():
    wlist = [1869,53,42,890,1910,1834,1340,963,1763,1920,1843,1636,767,1559, \
        1882, 1604, 7, 9, 24, 160, 430,117, 1527, 1061]
    return(wlist)

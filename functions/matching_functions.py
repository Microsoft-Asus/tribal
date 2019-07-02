# ------------------------------------------------------------------------------
#  Matching functions used across state crawlers
# ------------------------------------------------------------------------------
# define various functions to determine matches between establishments from FDA
# and business records from state SoS websites

# ------------------------------------------------------------------------------
# Table of Contents
# 1. name_match_scoring
# 2. match_selection


# ------------------------------------------------------------------------------
# 1. name_match_scoring
# ------------------------------------------------------------------------------
# Dependencies
import pandas as pd
import numpy as np
import string
from wordfreq import word_frequency
# identify match based on similarity of FDA DBA and SoS business names
def name_match_scoring(fda_row, sos_df, fda_colname = 'DBA Name', sos_colname = 'bizname', id_var='id'):

# Input: a record from FDA list
# Parameters:

    # fda_row:   row of  of FDA list
    # sos_df:   dataframe of Biz records to match FDA store to
    # fda, sos colname: name of column with biz name in respective data sets
# Output: SoS dataframe with name match scores
    # split by spaces
    fda_split=pd.Series(fda_row[fda_colname]).str.split(pat=" ", expand=True)
    sos_split=sos_df.loc[:, sos_colname].str.split(pat=" ", expand=True)

    # clear out punctuation marks
    translator = str.maketrans('', '', string.punctuation)
    def punc_rm(s):
        if s!=None:
            s = str(s).translate(translator).upper()
            s = s.replace('-', ' ')
            s = s.replace('/', ' ')
            return(s)
    fda_split=fda_split.applymap(punc_rm)
    sos_split=sos_split.applymap(punc_rm)
    # also making sure everything is capitalized for comparison compatabilit

    # strip out incorporation words (INC, LLC, LLP, LTD, CO)
    incorp=['INC', 'LLC', 'LLP', 'LTD', 'CO']
    sos_split.replace(incorp, [None,None,None,None,None], inplace=True,method='bfill')
    fda_split.replace(incorp, [None,None,None,None,None], inplace=True,method='bfill')
    fda_split.dropna(inplace=True, axis=1)

    # score typical frequency of words in the DBA name
    # Matches of uncommon words (likely to be proper words) will be weighted higher
        # than matches of common words

    def freq_str(str):
        if str!=None:
            return(word_frequency(str, 'en'))
    score_fda=fda_split.applymap(freq_str)
    score_sos=sos_split.applymap(freq_str)

    # If the entire DBA string is too short and common, we don't want to attempt a match on
    # name alone. Generate full score for this purpose later
    full_score=freq_str(' '.join([i for i in fda_split.iloc[0,:]]))

    # for words not in corpus (score=0), they are likely proper nouns
    # we'll assess their weight as very high when inverting
    score_fda=score_fda.mask(score_fda==0,.000001)
    score_sos=score_sos.mask(score_sos==0,.000001)

    # generate weights by inverting then normalizing to sum to 1
    score_fda=1/score_fda
    score_fda=score_fda.fillna(0)
    score_fda=score_fda.div(score_fda.sum(axis=1), axis=0)
    score_sos=1/score_sos
    score_sos=score_sos.fillna(0)
    score_sos=score_sos.div(score_sos.sum(axis=1), axis=0)
    # Assess match score
    def match_words(from_str, to_series=fda_split.iloc[0,:]):
        if from_str in [i for i in to_series]:
            return(1)
        else:
            return(0)

    match_df = sos_split.applymap(match_words)
    score_df = sos_df.loc[:, [id_var]]
    score_df['name_score'] = (score_sos * match_df).sum(axis=1)

    # common score >.00001, or two or fewer words as well as a common score >.000001
    # seems to be the right cutoff from manual examination of a subset of names
    score_df['common_flag']=0
    if (full_score>.000001 and len(fda_split)<=4) or (full_score>.00001):
        score_df.loc[:,'common_flag']=1

    # flag where score is highest
    # max=score_df.loc[:,'name_score'].max()
    # score_df.loc[:,'name_max_sc']=max
    # if max != 0:
    #     score_df.loc[:,'max_loc']=np.where(score_df['name_score']==max,1,0)
    # else:
    #     score_df.loc[:,'max_loc']=-1
    return(score_df)

# ------------------------------------------------------------------------------
# 2. address_match_scoring
# ------------------------------------------------------------------------------
# Dependencies
import pandas as pd
import numpy as np
import string
from wordfreq import word_frequency
import usaddress as usa
# function to match address of DBA and registered biz
def address_match_scoring(fda_row, sos_df, addr_split=True, full_addr=None, update=False):
    # fda_row - row from fda retailer data DataFrame
    # sos_df - df of possible matches for FDA retailer
    # addr_split - does address need to be concatenated or is there a full address
    #   field already?
    # full_addr - if addr_split is False, string of the name of the full address
    #   column

    # names of address components and corresponding matching method
    type_names = ['StreetName', 'StreetNamePostType', 'AddressNumber', 'ZipCode']
    match_meth = ['contains', 'contains', 'exact', 'exact']
    # throwaway function to clear out punctuation marks from addresses
    translator = str.maketrans('', '', string.punctuation)
    def punc_rm(s):
        if s!=None:
            return(str(s).translate(translator))
    # throwaway function to try and tag what addresses we can
    # seems to be able to tag virtually everything in WA SoS in the tests I did
    def try_tag(str):
        try:
            s=usa.tag(str)
            if 'StreetNamePostType' in s[0]:
                s[0]['StreetNamePostType'] = normalizeStreetSuffixes(
                    s[0]['StreetNamePostType'].lower())
            return(s[0])
        except:
            return('Not tagged')


    # split address components with usaddress
    fda_addr = ''
    if update == False:
        for i in ['Address Line 1', 'Address Line 2', 'City', 'State', 'Zip']:
                fda_addr = fda_addr + ' '+ str(fda_row[i])
    else:
        for i in ['Address Line 1_update', 'City_update',
        'State_update', 'Zip_update']:
                fda_addr = fda_addr + ' '+ str(fda_row[i])
    fda_addr = punc_rm(fda_addr)
    fda_split = try_tag(fda_addr)
    # continue if fda address has been tagged, else return -1 matching
    if isinstance(fda_split, dict):
        if addr_split == True:
            # clear out punctuation marks from addresses
            sos_addr = sos_df['paddress1']
            sos_addr = sos_addr.str.cat(sos_df[['paddress2', 'pcity', 'pstate']], sep = ' ')
            sos_addr = sos_addr.str.cat(sos_df['pzip'].astype('str').str.replace(
                '.0','', regex=False), sep = ' ')
        else:
            sos_addr = sos_df[full_addr]
        sos_addr = sos_addr.apply(punc_rm)
        sos_split = sos_addr.apply(try_tag)
        # remove those not tagged
        sos_split = sos_split.loc[sos_split != 'Not tagged']
        # match components of addresses
        def match_words_contains(from_str):
            if fda_part in fda_split and from_str != None:
                if from_str.upper() in fda_split[fda_part].upper():
                    return(1)
                else:
                    return(0)
            else:
                return(np.nan)

        def match_words_exact(from_str):
            if fda_part in fda_split and from_str != None:
                if from_str.upper() == fda_split[fda_part].upper():
                    return(1)
                else:
                    return(0)
            else:
                return(np.nan)

        score_df = sos_df.loc[:, ['id']]
        for i,j in zip(type_names, match_meth):
            sos_street = sos_split.loc[sos_split.apply(lambda x: i in x)]
            sos_street = sos_street.apply(lambda y: y[i])
            sos_street = sos_street.str.split(pat=" ", expand=True)
            fda_part = i
            if j == 'contains':
                match_df = sos_street.applymap(match_words_contains)
            if j == 'exact':
                match_df = sos_street.applymap(match_words_exact)

            score_df[i +'_score'] = match_df.sum(axis=1)/match_df.count(axis=1)

    else:
        score_df = sos_df.loc[:, ['id']]
        for i in type_names:
            score_df[i + '_score']=-1
    return(score_df)


# ------------------------------------------------------------------------------
# 3. match_selection
# ------------------------------------------------------------------------------
# take scores and return matches that meet set criteria
def match_selection(score_df, criteria, name_lvl=.95, addrnum_lvl=1,
    strname_lvl=1, strtype_lvl=1, zip_lvl=1):
    if criteria=='basic addr':
        score_df['match']=0
        score_df.loc[(score_df['AddressNumber_score']>=addrnum_lvl) &
            (score_df['StreetName_score']>=strname_lvl) &
            (score_df['StreetNamePostType_score']>=strtype_lvl) &
            (score_df['ZipCode_score']>=zip_lvl), 'match'] =1
        score_df = score_df.loc[score_df['match']==1, :]
    if criteria=='basic name':
        score_df['match']=0
        score_df.loc[(score_df['name_score']>=name_lvl),'match'] \
        =1
        score_df = score_df.loc[score_df['match']==1, :]
    if criteria=='basic name & addr':
        score_df['match']=0
        score_df.loc[(score_df['AddressNumber_score']>=addrnum_lvl) &
            (score_df['StreetName_score']>=strname_lvl) &
            (score_df['name_score']>=name_lvl) &
            (score_df['StreetNamePostType_score']>=strtype_lvl) &
            (score_df['ZipCode_score']>=zip_lvl),'match'] \
            = 1
        score_df = score_df.loc[score_df['match']==1, :]
    return(score_df)

# variant function that aggregates all scores based on pre-assigned weights
def match_select_agg(score_df, name_wgt=.95, addrnum_wgt=1, \
    strname_wgt=1, strtype_wgt=1, zip_wgt=1, dist_thresh=.05, match_thresh = None):
    if match_thresh == None:
        match_thresh =name_wgt + addrnum_wgt + strname_wgt + strtype_wgt \
            + zip_wgt + dist_wgt

    # aggregate scores based on specified weights
    score_df['score'] = score_df['name_score'] * name_wgt + \
        score_df['AddressNumber_score'] * addrnum_wgt + \
        score_df['StreetName_score'] * strname_wgt + \
        score_df['StreetNamePostType_score'] * strtype_wgt + \
        score_df['ZipCode_score'] * zip_wgt
    score_df['match']=0
    score_df.loc[(score_df['score']>=match_thresh),'match']= 1
    # add matches for stores that are closer to the FDA store than the specified threshold
    score_df.loc[(score_df['dist_score']<=dist_thresh),'match']= 1
    score_df = score_df.loc[score_df['match']==1, :]
    return(score_df)

# ------------------------------------------------------------------------------
# 4. display_results
# ------------------------------------------------------------------------------
# dependencies
import sys

# function to print out results of matching scores
def display_results(matches, file, id='REI', verbose=2, vars=None):
    # vars should be a list if verbose =1
    stdoutOrigin=sys.stdout
    sys.stdout = open('./logs/' + file + ".txt", "w")
    print('-------------Summary----------------')
    print('FDA retailers inputted: ' + str(len(matches)))
    match_num = 0
    for i in matches:
        if len(i[1].index) > 0:
            match_num += 1
    print('At least one match found for ' + str(match_num) + ' FDA retailers')
    print('Number of matches for each FDA retailer')
    for i in matches:
        if len(i[1].index) > 0:
            print(str(i[0][id]) + ' ' + str(len(i[1].index)))
    # verbose = 1 -> print elements in vars only
    if verbose==1:
        for i in matches:
            if len(i[1].index) > 0:
                print('-------------FDA Store----------------')
                print(i[0])
                for j, row in i[1].iterrows():
                    print('-------------SOS candidate ' + str(j) + '----------------')
                    print(row[vars])
    # verbose = 2 -> print all elements
    if verbose==2:
        for i in matches:
            if len(i[1].index) > 0:
                print('-------------FDA Store----------------')
                print(i[0])
                for j, row in i[1].iterrows():
                    print('-------------SOS candidate ' + str(j) + '----------------')
                    print(row)

    sys.stdout.close()
    sys.stdout=stdoutOrigin

# 5. Normalize street suffix
def normalizeStreetSuffixes(inputValue):
        '''
        Use common abbreviations -> USPS standardized abbreviation to replace common street suffixes

        Obtains list from https://www.usps.com/send/official-abbreviations.htm
        '''
        usps_street_abbreviations = {'trpk': 'tpke', 'forges': 'frgs', 'bypas': 'byp', 'mnr': 'mnr', 'viaduct': 'via', 'mnt': 'mt',
         'lndng': 'lndg', 'vill': 'vlg', 'aly': 'aly', 'mill': 'ml', 'pts': 'pts', 'centers': 'ctrs', 'row': 'row', 'cnter': 'ctr',
          'hrbor': 'hbr', 'tr': 'trl', 'lndg': 'lndg', 'passage': 'psge', 'walks': 'walk', 'frks': 'frks', 'crest': 'crst', 'meadows': 'mdws',
           'freewy': 'fwy', 'garden': 'gdn', 'bluffs': 'blfs', 'vlg': 'vlg', 'vly': 'vly', 'fall': 'fall', 'trk': 'trak', 'squares': 'sqs',
            'trl': 'trl', 'harbor': 'hbr', 'frry': 'fry', 'div': 'dv', 'straven': 'stra', 'cmp': 'cp', 'grdns': 'gdns', 'villg': 'vlg',
             'meadow': 'mdw', 'trails': 'trl', 'streets': 'sts', 'prairie': 'pr', 'hts': 'hts', 'crescent': 'cres', 'pass': 'pass',
              'ter': 'ter', 'port': 'prt', 'bluf': 'blf', 'avnue': 'ave', 'lights': 'lgts', 'rpds': 'rpds', 'harbors': 'hbrs',
               'mews': 'mews', 'lodg': 'ldg', 'plz': 'plz', 'tracks': 'trak', 'path': 'path', 'pkway': 'pkwy', 'gln': 'gln',
                'bot': 'btm', 'drv': 'dr', 'rdg': 'rdg', 'fwy': 'fwy', 'hbr': 'hbr', 'via': 'via', 'divide': 'dv', 'inlt': 'inlt',
                 'fords': 'frds', 'avenu': 'ave', 'vis': 'vis', 'brk': 'brk', 'rivr': 'riv', 'oval': 'oval', 'gateway': 'gtwy',
                  'stream': 'strm', 'bayoo': 'byu', 'msn': 'msn', 'knoll': 'knl', 'expressway': 'expy', 'sprng': 'spg',
                   'flat': 'flt', 'holw': 'holw', 'grden': 'gdn', 'trail': 'trl', 'jctns': 'jcts', 'rdgs': 'rdgs',
                    'tunnel': 'tunl', 'ml': 'ml', 'fls': 'fls', 'flt': 'flt', 'lks': 'lks', 'mt': 'mt', 'groves': 'grvs',
                     'vally': 'vly', 'ferry': 'fry', 'parkway': 'pkwy', 'radiel': 'radl', 'strvnue': 'stra', 'fld': 'fld',
                      'overpass': 'opas', 'plaza': 'plz', 'estate': 'est', 'mntn': 'mtn', 'lock': 'lck', 'orchrd': 'orch',
                       'strvn': 'stra', 'locks': 'lcks', 'bend': 'bnd', 'kys': 'kys', 'junctions': 'jcts', 'mountin': 'mtn',
                        'burgs': 'bgs', 'pine': 'pne', 'ldge': 'ldg', 'causway': 'cswy', 'spg': 'spg', 'beach': 'bch', 'ft': 'ft',
                         'crse': 'crse', 'motorway': 'mtwy', 'bluff': 'blf', 'court': 'ct', 'grov': 'grv', 'sprngs': 'spgs',
                          'ovl': 'oval', 'villag': 'vlg', 'vdct': 'via', 'neck': 'nck', 'orchard': 'orch', 'light': 'lgt',
                           'sq': 'sq', 'pkwy': 'pkwy', 'shore': 'shr', 'green': 'grn', 'strm': 'strm', 'islnd': 'is',
                            'turnpike': 'tpke', 'stra': 'stra', 'mission': 'msn', 'spngs': 'spgs', 'course': 'crse',
                             'trafficway': 'trfy', 'terrace': 'ter', 'hway': 'hwy', 'avenue': 'ave', 'glen': 'gln',
                              'boul': 'blvd', 'inlet': 'inlt', 'la': 'ln', 'ln': 'ln', 'frst': 'frst', 'clf': 'clf',
                               'cres': 'cres', 'brook': 'brk', 'lk': 'lk', 'byp': 'byp', 'shoar': 'shr', 'bypass': 'byp',
                                'mtin': 'mtn', 'ally': 'aly', 'forest': 'frst', 'junction': 'jct', 'views': 'vws', 'wells': 'wls', 'cen': 'ctr',
                                 'exts': 'exts', 'crt': 'ct', 'corners': 'cors', 'trak': 'trak', 'frway': 'fwy', 'prarie': 'pr', 'crossing': 'xing',
                                  'extn': 'ext', 'cliffs': 'clfs', 'manors': 'mnrs', 'ports': 'prts', 'gatewy': 'gtwy', 'square': 'sq', 'hls': 'hls',
                                   'harb': 'hbr', 'loops': 'loop', 'mdw': 'mdw', 'smt': 'smt', 'rd': 'rd', 'hill': 'hl', 'blf': 'blf',
                                    'highway': 'hwy', 'walk': 'walk', 'clfs': 'clfs', 'brooks': 'brks', 'brnch': 'br', 'aven': 'ave',
                                     'shores': 'shrs', 'iss': 'iss', 'route': 'rte', 'wls': 'wls', 'place': 'pl', 'sumit': 'smt', 'pines': 'pnes',
                                      'trks': 'trak', 'shoal': 'shl', 'strt': 'st', 'frwy': 'fwy', 'heights': 'hts', 'ranches': 'rnch',
                                       'boulevard': 'blvd', 'extnsn': 'ext', 'mdws': 'mdws', 'hollows': 'holw', 'vsta': 'vis', 'plains': 'plns',
                                        'station': 'sta', 'circl': 'cir', 'mntns': 'mtns', 'prts': 'prts', 'shls': 'shls', 'villages': 'vlgs',
                                         'park': 'park', 'nck': 'nck', 'rst': 'rst', 'haven': 'hvn', 'turnpk': 'tpke', 'expy': 'expy', 'sta': 'sta',
                                          'expr': 'expy', 'stn': 'sta', 'expw': 'expy', 'street': 'st', 'str': 'st', 'spurs': 'spur', 'crecent': 'cres',
                                           'rad': 'radl', 'ranch': 'rnch', 'well': 'wl', 'shoals': 'shls', 'alley': 'aly', 'plza': 'plz', 'medows': 'mdws',
                                            'allee': 'aly', 'knls': 'knls', 'ests': 'ests', 'st': 'st', 'anx': 'anx', 'havn': 'hvn', 'paths': 'path', 'bypa': 'byp',
                                             'spgs': 'spgs', 'mills': 'mls', 'parks': 'park', 'byps': 'byp', 'flts': 'flts', 'tunnels': 'tunl', 'club': 'clb', 'sqrs': 'sqs',
                                              'hllw': 'holw', 'manor': 'mnr', 'centre': 'ctr', 'track': 'trak', 'hgts': 'hts', 'rnch': 'rnch', 'crcle': 'cir', 'falls': 'fls',
                                               'landing': 'lndg', 'plaines': 'plns', 'viadct': 'via', 'gdns': 'gdns', 'gtwy': 'gtwy', 'grove': 'grv', 'camp': 'cp', 'tpk': 'tpke',
                                                'drive': 'dr', 'freeway': 'fwy', 'ext': 'ext', 'points': 'pts', 'exp': 'expy', 'ky': 'ky', 'courts': 'cts', 'pky': 'pkwy', 'corner': 'cor',
                                                 'crssing': 'xing', 'mnrs': 'mnrs', 'unions': 'uns', 'cyn': 'cyn', 'lodge': 'ldg', 'trfy': 'trfy', 'circle': 'cir', 'bridge': 'brg',
                                                  'dl': 'dl', 'dm': 'dm', 'express': 'expy', 'tunls': 'tunl', 'dv': 'dv', 'dr': 'dr', 'shr': 'shr', 'knolls': 'knls', 'greens': 'grns',
                                                   'tunel': 'tunl', 'fields': 'flds', 'common': 'cmn', 'orch': 'orch', 'crk': 'crk', 'river': 'riv', 'shl': 'shl', 'view': 'vw',
                                                    'crsent': 'cres', 'rnchs': 'rnch', 'crscnt': 'cres', 'arc': 'arc', 'btm': 'btm', 'blvd': 'blvd', 'ways': 'ways', 'radl': 'radl',
                                                     'rdge': 'rdg', 'causeway': 'cswy', 'parkwy': 'pkwy', 'juncton': 'jct', 'statn': 'sta', 'gardn': 'gdn', 'mntain': 'mtn',
                                                      'crssng': 'xing', 'rapid': 'rpd', 'key': 'ky', 'plns': 'plns', 'wy': 'way', 'cor': 'cor', 'ramp': 'ramp', 'throughway': 'trwy',
                                                       'estates': 'ests', 'ck': 'crk', 'loaf': 'lf', 'hvn': 'hvn', 'wall': 'wall', 'hollow': 'holw', 'canyon': 'cyn', 'clb': 'clb',
                                                        'cswy': 'cswy', 'village': 'vlg', 'cr': 'crk', 'trce': 'trce', 'cp': 'cp', 'cv': 'cv', 'ct': 'cts', 'pr': 'pr', 'frg': 'frg',
                                                         'jction': 'jct', 'pt': 'pt', 'mssn': 'msn', 'frk': 'frk', 'brdge': 'brg', 'cent': 'ctr', 'spur': 'spur', 'frt': 'ft', 'pk': 'park',
                                                          'fry': 'fry', 'pl': 'pl', 'lanes': 'ln', 'gtway': 'gtwy', 'prk': 'park', 'vws': 'vws', 'stravenue': 'stra', 'lgt': 'lgt',
                                                           'hiway': 'hwy', 'ctr': 'ctr', 'prt': 'prt', 'ville': 'vl', 'plain': 'pln', 'mount': 'mt', 'mls': 'mls', 'loop': 'loop',
                                                            'riv': 'riv', 'centr': 'ctr', 'is': 'is', 'prr': 'pr', 'vl': 'vl', 'avn': 'ave', 'vw': 'vw', 'ave': 'ave', 'spng': 'spg',
                                                             'hiwy': 'hwy', 'dam': 'dm', 'isle': 'isle', 'crcl': 'cir', 'sqre': 'sq', 'jct': 'jct', 'jctn': 'jct', 'mountain': 'mtn',
                                                              'keys': 'kys', 'parkways': 'pkwy', 'drives': 'drs', 'tunl': 'tunl', 'jcts': 'jcts', 'knl': 'knl', 'center': 'ctr',
                                                               'driv': 'dr', 'tpke': 'tpke', 'sumitt': 'smt', 'canyn': 'cyn', 'ldg': 'ldg', 'harbr': 'hbr', 'rest': 'rst', 'shoars': 'shrs',
                                                                'vist': 'vis', 'gdn': 'gdn', 'islnds': 'iss', 'hills': 'hls', 'cresent': 'cres', 'point': 'pt', 'lake': 'lk', 'vlly': 'vly',
                                                                 'strav': 'stra', 'crossroad': 'xrd', 'bnd': 'bnd', 'strave': 'stra', 'stravn': 'stra', 'knol': 'knl', 'vlgs': 'vlgs',
                                                                  'forge': 'frg', 'cntr': 'ctr', 'cape': 'cpe', 'height': 'hts', 'lck': 'lck', 'highwy': 'hwy', 'trnpk': 'tpke', 'rpd': 'rpd',
                                                                   'boulv': 'blvd', 'circles': 'cirs', 'valleys': 'vlys', 'vst': 'vis', 'creek': 'crk', 'mall': 'mall', 'spring': 'spg',
                                                                    'brg': 'brg', 'holws': 'holw', 'lf': 'lf', 'est': 'est', 'xing': 'xing', 'trace': 'trce', 'bottom': 'btm',
                                                                     'streme': 'strm', 'isles': 'isle', 'circ': 'cir', 'forks': 'frks', 'burg': 'bg', 'run': 'run', 'trls': 'trl',
                                                                      'radial': 'radl', 'lakes': 'lks', 'rue': 'rue', 'vlys': 'vlys', 'br': 'br', 'cors': 'cors', 'pln': 'pln',
                                                                       'pike': 'pike', 'extension': 'ext', 'island': 'is', 'frd': 'frd', 'lcks': 'lcks', 'terr': 'ter',
                                                                        'union': 'un', 'extensions': 'exts', 'pkwys': 'pkwy', 'islands': 'iss', 'road': 'rd', 'shrs': 'shrs',
                                                                         'roads': 'rds', 'glens': 'glns', 'springs': 'spgs', 'missn': 'msn', 'ridge': 'rdg', 'arcade': 'arc',
                                                                          'bayou': 'byu', 'crsnt': 'cres', 'junctn': 'jct', 'way': 'way', 'valley': 'vly', 'fork': 'frk',
                                                                           'mountains': 'mtns', 'bottm': 'btm', 'forg': 'frg', 'ht': 'hts', 'ford': 'frd', 'hl': 'hl',
                                                                            'grdn': 'gdn', 'fort': 'ft', 'traces': 'trce', 'cnyn': 'cyn', 'cir': 'cir', 'un': 'un', 'mtn': 'mtn',
                                                                             'flats': 'flts', 'anex': 'anx', 'gatway': 'gtwy', 'rapids': 'rpds', 'villiage': 'vlg', 'flds': 'flds',
                                                                              'coves': 'cvs', 'rvr': 'riv', 'av': 'ave', 'pikes': 'pike', 'grv': 'grv', 'vista': 'vis', 'pnes': 'pnes',
                                                                               'forests': 'frst', 'field': 'fld', 'branch': 'br', 'grn': 'grn', 'dale': 'dl', 'rds': 'rds', 'annex': 'anx',
                                                                                'sqr': 'sq', 'cove': 'cv', 'squ': 'sq', 'skyway': 'skwy', 'ridges': 'rdgs', 'hwy': 'hwy', 'tunnl': 'tunl',
                                                                                 'underpass': 'upas', 'cliff': 'clf', 'lane': 'ln', 'land': 'land', 'bch': 'bch', 'dvd': 'dv', 'curve': 'curv',
                                                                                  'cpe': 'cpe', 'summit': 'smt', 'gardens': 'gdns'}
        words = inputValue.split()
        for w in words:
            if w in usps_street_abbreviations.keys():
                inputValue = inputValue.replace(w, usps_street_abbreviations[w])
        return(inputValue)

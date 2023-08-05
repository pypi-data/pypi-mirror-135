import numpy as np
import copy
from sf import *

##############################################################################
def smplrnd(x, prc=50, seed=None):
    # x - data sample: data frame or np.array
    # prc - percentage of observations to keep: float in interval [0, 100]
    # seed - the seed of the random number generator, default is None
    r = rand([x.shape[0], 1], seed=seed)
    rs = r < prc/100        # Select rows to keep
    if isinstance(x, (np.ndarray)):
        if len(x.shape)==1: return x[rs]
        elif len(x.shape)==2: return x[rs.flatten(),:]
    if isinstance(x, pd.DataFrame): return x.loc[rs,:]
##############################################################################
def smplstr(x, prc, ixk, seed=None):
    '''
    x - data sample: data frame or np.array
    ixk - indexes of the key variables, which define the strata, where each combination of unique values coresponds to a strata.
    Let there are two variables defining the strata with 2 and 3 unique values, respectively and xk11 is the first unique value of the first variable, xk12 is the second unique value of xk1, etc. Then the strata are:
    stratum | definition
        1   |{xk11, xk21}
        2   |{xk11, xk22}
        3   |{xk11, xk23}
        4   |{xk12, xk21}
        5   |{xk12, xk22}
        6   |{xk12, xk23}
    prc - list of percentage of observations to keep per strata: float in interval [0, 100]
    seed - the seed of the random number generator, default is None
    '''
    uxk = {}
    ni = nans((len(ixk), 1))
    h = 0
    for i in ixk: 
        uxk[h] = np.unique(x[:,i])
        ni[h] = len(uxk[h])
        h += 1
        
    xs = np.empty([0,x.shape[1]])
    ws = np.empty([0,1])
    s = strata(uxk, np.empty([0,len(ixk)]), 0, len(ixk))
    for si in range(len(s)):
        cnd = np.full((x.shape[0],), True)
        i = 0
        for sii in s[si,:]:
            cnd = cnd & (x[:,ixk[i]]==int(sii))
            i += 1
        xsi = smplrnd(x[cnd,:], prc=prc[si], seed=seed)
        xs = np.vstack((xs, xsi))
        N0 = sum(cnd)
        N = xsi.shape[0]
        ws = np.vstack((ws, np.full((N, 1), N0/N)))
    return xs, ws
##############################################################################
def strata(uxk, sk, kk, mk0):
    mk = len(uxk)
    s = np.empty((0, mk))
    for k in uxk[kk]:
        if mk > 1:
            uxk1 = copy.deepcopy(uxk)
            del uxk1[kk]
            sk = strata(uxk1, sk, kk+1, mk0)
            sk = np.hstack((np.full((sk.shape[0], 1), k), sk))
            s = np.vstack((s, sk))
        else:
            sk = c_(uxk[kk])
            s = np.vstack((s, sk))
            break
    return s
##############################################################################
def usmpl(x, met='rand', prc=50, ixk=None, seed=None):
    if met == 'rand':  
        N = x.shape[0]
        xs = smplrnd(x, prc=prc, seed=seed)
        ws = np.ones((N, 1))
    elif met == 'strat':
        xs, ws = smplstr(x, prc=prc, ixk=ixk, seed=seed)
    elif met == 'syst': pass # todo: implement more sampling methods...
    return xs, ws
##############################################################################
# def smplsys():
##############################################################################
# def smplcnn():
##############################################################################
# def smplrnn():
##############################################################################
# def smplenn():...
##############################################################################


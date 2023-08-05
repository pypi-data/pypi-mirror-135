"""
D A T A   C L E A N N I N G
-----------------------------------------
author: OPEN-MAT
Matlab version:
    Alexander Efremov
    26 Apr 2009
    course: Multivariable Control Systems
-----------------------------------------
"""
import numpy as np
import copy
from aislab.gnrl.sf import *
from aislab.md_reg import *
##############################################################################
#def filna(x):
##############################################################################
def filconst(x, c=0, met=None):
    x1 = copy.deepcopy(x)
    m = x1.shape[1]
    inan = np.isnan(x1)
    ix = np.argwhere(inan)
    if met == 'mean':      c = np.nanmean(x, axis=0)
    elif met == 'mode':    c = np.nan # calc mode
    elif met == 'median':  c = np.nan # calc median
    elif isinstance(c, (int, float)): c = np.tile(np.array([c]), m)
    for i in range(m):
        x1[inan[:, i], i] = c[i]
    return x1, ix
##############################################################################
#def filinterp():
##############################################################################
def filmdl(x):
    x1 = copy.deepcopy(x)
    m = x1.shape[1]
    inan = np.isnan(x)
    ix = np.argwhere(inan)
    DV = 1 - inan
    nnan = np.sum(inan, axis=0)
    mx = np.nanmean(x1, axis=0)
    iy = np.argsort(nnan)
    for j in range(30):
        for i in iy:
            if nnan[i] == 0: continue
            yi = c_(x1[:, i])
            xi = np.delete(x1, i, axis=1)
            mxi = np.delete(mx, i)
            for j in range(m-1): xi[np.isnan(xi[:, j]), j] = mxi[j]  # fill temporary na-s with mean
            iD = DV[:, i] == 1
            iV = DV[:, i] == 0
            mdl = lspm(xi[iD, :], c_(yi[iD, 0]), pm0=1)
            x1[iV, i] = lspm_apl(xi[iV, :], c_(yi[iV, 0]), mdl).flatten()
    return x1, ix
##############################################################################


"""
author: OPEN-MAT
date: 	15.06.2019
Matlab version: 26 Apr 2009
Course: Multivariable Control Systems
"""
import numpy as np
from sf import *

###################################################################################
# non-lin transf
# - nltransf, opt_params_of_nl_funcs
def nltrsf(x, y, tr, crit='pears'):
    tr1 = np.array(tr)
    x = x - np.min(x)
    X = x
    if any(tr1 == 'pow2'):   X = np.hstack((X, np.power(x, 2)))
    if any(tr1 == 'pow3'):   X = np.hstack((X, np.power(x, 3)))
    if any(tr1 == 'sqrt'):   X = np.hstack((X, np.sqrt(x)))
    if any(tr1 == 'rcpr'):   X = np.hstack((X, 1/(1 + x)))
    if any(tr1 == 'log'):    X = np.hstack((X, np.log(1 + x)))
    X = np.hstack((X, y))
    if crit == 'pears':
        crt_all = abs(np.corrcoef(X.T))
        crt_all = crt_all[:-1,-1]
    elif crit == 'spear':
        pass # crt = spearman...
    ix = np.argmax(crt_all)
    xt = X[:,]
    tr_all = ['orig'] + tr
    crt_best = crt_all[ix]
    tr_best = tr_all[ix]
    xt = X[:,ix]
    tfmdl = {'ix_best':ix,
             'crt_best':crt_best,
             'tr_best':tr_best,
             'xt':xt,
             'crt_all':c_(crt_all),
             'tr_all':c_(tr_all),
             
            }
    return tfmdl
###################################################################################


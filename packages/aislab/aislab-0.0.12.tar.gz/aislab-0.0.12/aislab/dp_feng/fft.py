"""
author: OPEN-MAT
date: 	15.06.2019
Matlab version: 26 Apr 2009
Course: Multivariable Control Systems
"""
import numpy as np
from sf import *

# normalization
# normlz()				met=rnml, std, centr, minzer, scale_std, scale_range
# centr():				# needed for...
# minzer():				# needed for non-linear transformations
# scale():				# needed for... (met=std/range)
###################################################################################
def stdn(x, w=None, mxd=None, stdxd=None):
    N, m = x.shape
    one = np.ones((N, 1))

    if w is None and mxd is None and stdxd is None:
        mxd = np.zeros((m, 1))
        stdxd = np.ones((m, 1))
        mx = c_(np.mean(x, axis=0))
        stdx = c_(np.std(x, axis=0))
    elif mxd is None and stdxd is None:
        mxd = np.zeros((m, 1))
        stdxd = np.ones((m, 1))
        Nw = np.sum(w)
        mx = r_(x)@w/Nw
        stdx = np.sqrt(np.sum((x - one@mx.T)**2*np.tile(w, np.size(x, 2))).T/(Nw - 1))
    elif stdxd is None:
        stdxd = mxd
        mxd = w
        mx = c_(np.mean(x))
        stdx = c_(np.std(x))
    else:
        Nw = np.sum(w)
        mx = r_(x)@w/Nw
        stdx = c_(np.sqrt(np.sum(x**2*np.tile(w, np.size(x, 2)))/(Nw - 1)))
    stdx[stdx==0] = 1
    x = (x - one@mx.T)@np.diag((stdx**-1*stdxd).flatten()) + one@mxd.T
    st = {'mx':mx,
          'stdx':stdx
	     }
    return x, st
##############################################################################
def rnml(x, xl=None, xh=None):
    N, m = x.shape
    if xl is None: xl = 0
    if xh is None: xh = 1
    if isinstance(xl, (int, float)): xl = np.matlib.repmat(xl,1,m)
    if isinstance(xh, (int, float)): xh = np.matlib.repmat(xh,1,m)
    minx = np.min(x, axis=0)
    maxx = np.max(x, axis=0)
    x = (x - minx)/(maxx - minx)*(xh - xl)
    st = {'minx':minx,
          'maxx':maxx
	     }
    return x, st
##############################################################################    


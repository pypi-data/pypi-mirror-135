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
from gnrl.sf import *
from md_reg import *
##############################################################################
def cap(x, pc=98, tolp=None, n=3, met='mx'):
    '''
    x - data frame or array
    p - maximum acceptable percentile
    tolp - maximum acceptable difference in percentage between the relative difference between initial and capped variable.
        If tolp is defined, then x will be capped only if:
            abs(mx - mxc)/mx >= tolp, in case of met ='mx' 
            abs(sd - sdc)/sd >= tolp, in case of met ='sdx' 
        Otherwise, if pdm is not defined, then capping will be directly applied without analysis.
        
    xc - capped variable
    ix - indexes of capped values in x
    '''
    xc = copy.deepcopy(x)
    mx = np.mean(x)
    if met=='mx':
        xp = np.percentile(x, pc)
        ix,temp = np.where(x > xp)
        xc[ix] = xp
        if tolp is not None:
            if abs((mx - np.mean(xc))/np.max(mx, initial=1e-6)) >= tolp/100:
                return xc, ix
            else:
                return x, np.empty((0,0))
        else:
            return xc, ix
    elif met=='sdx':
        sx = np.std(x)
        ix1 = np.where(x - mx > sx*n)
        ix2 = np.where(x - mx < -sx*n)
        ix = np.sort(np.hstack((ix1, ix2)))
        x1 = copy.deepcopy(x)
        x1 = np.delete(x1, ix.flatten())
        sx1 = np.std(x1)
        if tolp is not None and abs((sx - sx1)/np.max(sx, initial=1e-6)) >= tolp/100:
            xc[ix1] = np.max(x1)
            xc[ix2] = np.min(x1)
            return xc, ix
        else:
            return x, np.empty((0,0))
        
    
##############################################################################
#def capfloor():
##############################################################################
def floor(x, pc=98, tolp=None, n=3, met='mx'):
    '''
    x - data frame or array

    p - minimum acceptable percentile
    dmp - maximum acceptable percentage difference between the mean values of initial and capped variable. 
        If dmp is defined, then x will be capped only if mxc - mx >= dmp. 
        Otherwise, if pdm is not defined, then capping will be directly applied without analysis.

        
    xf - floored variable
    ix - indexes of floored values in x
    '''
    xf, xi = cap(-x, 100-pc, tolp=tolp)
    xf = -xf
    return xf, xi
#def shave(x, n, met):
#	'''
#	'''
#    yf, nn = filtgauss(x, [], [], [])
#
#    std_y = np.std(x - yf)
#    upLmt = yf + int(n)*std_y
#    lowLmt = yf - int(n)*std_y
#    upLmt = upLmt.reshape(1000, 1)
#    lowLmt = lowLmt.reshape(1000, 1)
#
#    # find spikes
#    sp1 = x > upLmt
#    sp2 = x < lowLmt
#    sp = sp1 + sp2
#    ix1 = np.where(sp == True)
#    ix1 = ix1[0]
#
#    if met == 'lin':
#        ix = np.where(abs(sp[2:] ^ sp[1:len(sp) - 1]) > 0)
#        ix = ix[0]
#        ix = ix.reshape(len(ix), 1)
#        sy = x  # shaved y
#
#        if sp.all() == 1:  # first value / s / is a spike
#            sy[1:ix[1]] = x(ix[1] + 1)
#            ix = ix[2:]
#
#        if sp[sp.all()] == 1:  # last value/s/ is a spike
#            sy[ix[len(ix)] + 1:len(ix)] = x[ix[len(ix) - 1]]
#            ix = ix[1:len(ix) - 1]
#
#        if len(ix) != 0:
#            k1 = ix[0::2]
#            k2 = ix[0::2] + 2
#
#            a = np.divide(((x[k1] - x[k2]).reshape(5, 1)), (k2 - k1))
#            b = (x[k1]).reshape(5, 1) - a*k1
#            for i in range(0, len(k1)):
#                k_vec = list(range(int(k1[i] + 1), int(k2[i])))
#                sy[k_vec] = (a[i]*k_vec - b[i]).reshape(1, 1)
#    else:
#        # Add different methods for outlier replacement
#        print("unknown method for outliers replacement")
#    return sy, ix1, lowLmt, upLmt
#

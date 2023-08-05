"""
author: OPEN-MAT
date: 	15.06.2019
Matlab version: 26 Apr 2009
Course: Multivariable Control Systems
"""
import numpy as np
from aislab.gnrl.sf import *
####################################################################################
# def trnd():
####################################################################################
def permdl(x, w=None, T=7, n=None, met='blk'):
    if w is None: w = ones(x.shape)
    N = len(x)
    T = int(T)
    n = int(n)
    h = int(np.floor(N/T))
    S = x[:h*T].reshape(h, T)
    W = w[:h*T].reshape(h, T)
    if N > h*T:
        ss = nans((1, np.ceil(N/T).astype(int)*T - N))
        S = np.vstack((S, np.hstack((x[h*T:].T, ss))))
        W = np.vstack((W, np.hstack((w[h*T:].T, ss))))

    if met == 'blk':
        Nw = np.nancumsum(W, axis=0).astype(float)
        Nw[n:, :] = Nw[n:, :] - Nw[:-n, :]
        Nw[Nw == 0] = 1e-6
        pm = np.nancumsum(S*W, axis=0)
        pm[n:, :] = pm[n:, :] - pm[:-n, :]
        pm = pm/Nw
        ind = T if len(x) % T == 0 else len(x) % T
        pm = c_(pm.flatten()[:(-ind-1)])
    elif met == 'rec':
        Nw = np.nansum(W, axis=0).astype(float)
        Nw[Nw == 0] = 1e-6
        pm = np.nansum(S*W, axis=0)/Nw
        ind = T if len(x) % T == 0 else len(x) % T
        pm = np.roll(pm, -ind)
    return pm
####################################################################################
# 	T determination = f(Rxx), f(fft), ...

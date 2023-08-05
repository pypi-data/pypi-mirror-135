"""
author: OPEN-MAT
date: 	21.05.2021
"""
import numpy as np
from aislab.gnrl.bf import * # c_
from aislab.gnrl.sf import * # rand...

pi = np.pi
##############################################################################
def harmnc(size=(100,1), rw=(0,100), rfi=(0,2*np.pi), ra=(0,1), rc=(0,1), se=0, seed=0):
    N, m = size
    wmin, wmax = rw
    fimin, fimax = rfi
    amin, amax = ra
    cmin, cmax = rc
    t = c_(np.arange(0, N)/N)
    w = rand((1, m), wmin, wmax, seed=seed+1)
    fi = rand((1, m), fimin, fimax, seed=seed+2)
    a = rand((1, m), amin, amax, seed=seed+3)
    x0 = np.ones((N, 1))@rand((1, m), cmin, cmax, seed=seed+4)
    x1 = np.sin(t*2*pi*w + fi)*a
    x = x0 + x1
    e = randn((N, m), 0, 1, seed=seed)*np.std(x)*se
    x = x + e
    return x
##############################################################################


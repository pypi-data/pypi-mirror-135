"""
    author: OPEN-MAT
    date: 	15.06.2019
    Matlab version: 26 Apr 2009
    Course: Multivariable Control Systems
"""
import numpy as np
from numpy import matlib
import scipy.sparse as sp
from scipy.sparse import diags
from scipy.sparse.linalg import inv as spinv  # for csc format
from scipy.sparse.linalg import spsolve  # for csr format

from aislab.gnrl.bf import*# c_
from aislab.gnrl.sf import *
from aislab.gnrl.measr import*# vaf
from aislab.op_nlopt import*# stopcrt

##############################################################################
# def dm2dv():
##############################################################################
def dmpm(U=m_(), Y=m_(), E=m_(), na=None, nb=None, nc=None, pm0=None, ivi=None, par={}):
    """
     DM2M constructs the data matrix for a model in a parameter matrix form.
     F = dmpm(U, Y, E, na, nb, nc)
     
     Inputs:
       U - [N x m] input data matrix with structure
           U = [u(1) u(n + 2) ... u(N)]'
           where N is the length of the observation interval and u(i) is m dimensional vectos
       Y - [N x r] output data matrix with structure
           Y = [y(1) y(2) ... y(N)]',
       E - [N x r] residual data matrix with structure
           E = [e(1) e(2) ... e(N)]',
       par - structure with fields:
         na - maximum degree of polynomials in A(q^-1)
         nb - maximum degree of polynomials in B(q^-1)
         nc - maximum degree of polynomials in C(q^-1)
         intercept - 1 if model has intercept, otherwise 0. Default is 0.
    
     Outputs:
       F - [N - n x z] data matrix /z = na*r + nb*m + nc*r/
    """

    if type(U) != np.ndarray:   U = np.array([U])
    if type(Y) != np.ndarray:   Y = np.array([Y])
    if type(E) != np.ndarray:   E = np.array([E])
    N = int()
    if len(U) > 0:  N, m = U.shape
    else:           m = 0
    if len(Y) > 0:  N, r = Y.shape
    else:           r = 0
    if len(E) > 0:  N, r = E.shape
    if not N > 0: raise Exception('In DMPM(): At least one data matrix should not be empty...')
    if np.any(m_(na) == None):
        if 'na' in par: na = par['na']
        else:           na = np.zeros((r, 1))
    if np.any(m_(nb) == None):
        if 'nb' in par: nb = par['nb']
        else:           nb = np.zeros((1, m))
    if np.any(m_(nc) == None):
        if 'nc' in par: nc = par['nc']
        else:           nc = np.zeros((r, 1))
    if np.any(m_(pm0) == None):
        if 'pm0' in par: pm0 = par['pm0']
        else:            pm0 = np.zeros((r, 1))

    if isinstance(nb, np.ndarray) and nb.shape[1] == 0: nb = 0
    na = int(np.max(na))  # Current dmpm() works with na, nb, nc - scalars, todo: should work with 1D arrays
    nb = int(np.max(nb))
    nc = int(np.max(nc))
    pm0 = int(np.max(pm0))
    n = np.max([na, nb, nc])
    if ivi is None:
        Fi = np.ones((N - n, pm0))
        Fy = nans((N - n, na*r))
        Fu = nans((N - n, nb*m))
        Fe = nans((N - n, nc*r))
        if na > 0 and Y.size > 0:
            for i in range(na - 1, -1, -1): Fy[:, (na - i - 1)*r:(na - i)*r] = -Y[(n - na + i):(N - na + i)]
        if nb > 0 and U.size > 0:
            for i in range(nb - 1, -1, -1): Fu[:, (nb - i - 1)*m:(nb - i)*m] = U[(n - nb + i):(N - nb + i)]
        if nc > 0 and E.size > 0:
            for i in range(nc - 1, -1, -1): Fe[:, (nc - i - 1)*r:(nc - i)*r] = E[(n - nc + i):(N - nc + i)]
        F = np.hstack((Fi, Fy, Fu, Fe))
    else:
        F = nans(N - n, len(ivi))
        if pm0: F[:, 0] = ones((N - n,))
        j2 = 0
        if na > 0 and Y.size > 0:
            for i in range(na - 1, -1, -1):
                jj = m_([na - i - 1, na - i])*r + pm0
                ind = find((ivi >= jj[0]) & (ivi < jj[1]))
                jj = ivi[ind] - pm0 - (na-i-1)*r
                j1 = j2
                j2 += len(ind)
                F[:, ind] = -Y[(n - na + i):(N - na + i), jj]
        j2 = 0
        if nb > 0 and U.size > 0:
            for i in range(nb - 1, -1, -1):
                jj = m_([nb - i - 1, nb - i])*m + pm0 + na*r
                ind = find((ivi >= jj[0]) & (ivi < jj[1]))
                jj = ivi[ind] - pm0 - na*r - (nb-i-1)*m
                j1 = j2
                j2 += len(ind)
                F[:, ind] = U[(n - nb + i):(N - nb + i), jj]
        j2 = 0
        if nc > 0 and E.size > 0:
            # for i in range(nc - 1, -1, -1): Fe[:, (nc - i - 1)*r:(nc - i)*r] = E[(n - nc + i):(N - nc + i)]
            for i in range(nc - 1, -1, -1):
                jj = m_([nc - i - 1, nc - i])*r + pm0 + na*r + nb*m
                ind = find((ivi >= jj[0]) & (ivi < jj[1]))
                jj = ivi[ind] - pm0 - na*r - nb*m - (na-i-1)*r
                j1 = j2
                j2 += len(ind)
                F[:, ind] = E[(n - nc + i):(N - nc + i), jj]
    return F


##############################################################################
def dmpv(U=m_(), Y=m_(), E=m_(), na=None, nb=None, nc=None, pm0=None, ivi=None, mxtp='dense', par={}):
    if type(U) != np.ndarray:   U = np.array([U])
    if type(Y) != np.ndarray:   Y = np.array([Y])
    if type(E) != np.ndarray:   E = np.array([E])
    N = int()
    if len(U) > 0:  N, m = U.shape
    else:           m = 0
    if len(Y) > 0:  N, r = Y.shape
    else:           r = 0
    if len(E) > 0:  N, r = E.shape
    if not N > 0: raise Exception('In DMPV(): At least one data matrix should be not empty...')

    if isinstance(na, (int, float)):  na = np.full([r, r], na)
    if isinstance(nb, (int, float)):  nb = np.full([r, m], nb)
    if isinstance(nc, (int, float)):  nc = np.full([r, r], nc)
    if isinstance(pm0, (int, float)): pm0 = np.full([r, 1], pm0)
    if (np.array([na == None])).any():
        if 'na' in par: na = par['na']
        else:           na = np.zeros((r, r))
    if (np.array([nb == None])).any():
        if 'nb' in par: nb = par['nb']
        else:           nb = np.zeros((r, m))
    if (np.array([nc == None])).any():
        if 'nc' in par: nc = par['nc']
        else:           nc = np.zeros((r, r))
    if (np.array([pm0 == None])).any():
        if 'pm0' in par:    pm0 = par['pm0']
        else:               pm0 = np.zeros((r, 1))

    n = int(np.max([np.max(na), np.max(nb), np.max(nc)]))

    Int = np.tile(pm0.T, (N, 1))
    ni = np.diag(pm0.flatten());
    if mxtp == 'dense':     F = np.empty(((N - n)*r, 0))
    elif mxtp[1] == 'csc':  F = sp.csc_matrix(((N - n)*r, 0), dtype=float)
    elif mxtp[1] == 'csr':  F = sp.csr_matrix(((N - n)*r, 0), dtype=float)
    elif mxtp[1] == 'bsr':  F = sp.bsr_matrix(((N - n)*r, 0), dtype=float)
    else: raise Exception("In DMPV(): Parameter 'mxtp' is not specified correctly - it could be: {'dense', ['dok','csc'], ['dok','csr'], ['ili','csc'], ['ili','csr']}")
    for i in range(r):
        MM = np.empty((N - n, 0))
        M = np.empty((N - n, 0))
        for factors, nn in enumerate([ni, na, nb, nc]):
            if factors == 0:    M = Int
            elif factors == 1:  M = -Y
            elif factors == 2:  M = U
            elif factors == 3:  M = E
            if nn.size > 0 and M.size > 0:
                rr = nn.shape[1]
                nn = nn.astype(int)
                for j in range(rr):
                    if nn[i, j] > 0:
                        if n + 1 > N:   Mi = M[:, j]
                        else:           Mi = M[:, j].T
                        for ii in range(nn[i, j]):
                            Mi = np.roll(M[:, j], ii + 1, axis=0)[n:].reshape((N - n, 1))
                            MM = np.hstack((MM, Mi))
        sni = np.sum(ni[i], initial=0)
        sna = np.sum(na[i], initial=0)
        snb = np.sum(nb[i], initial=0)
        snc = np.sum(nc[i], initial=0) if nc.size > 0 else 0
        pi = int(sni + sna + snb + snc)
        if mxtp == 'dense':     Fi = np.zeros(((N - n)*r, pi))
        elif mxtp[0] == 'dok':  Fi = sp.dok_matrix(((N - n)*r, pi), dtype=float)
        elif mxtp[0] == 'lil':  Fi = sp.lil_matrix(((N - n)*r, pi), dtype=float)
        elif mxtp[0] == 'coo':  Fi = sp.coo_matrix(((N - n)*r, pi), dtype=float)
        else: raise Exception("In DMPV(): Parameter 'mxtp' is not specified correctly - it could be: {'dense', ['dok','csc'], ['dok','csr'], ['ili','csc'], ['ili','csr']}")
        Fi[range(i, (N - n)*r, r)] = MM
        if mxtp == 'dense':     F = np.hstack((F, Fi))
        elif mxtp[1] == 'csc':  F = sp.hstack((F, Fi.tocsc()))
        elif mxtp[1] == 'csr':  F = sp.hstack((F, Fi.tocsr()))
        elif mxtp[1] == 'bsr':  F = sp.hstack((F, Fi.tobsr()))
        else: raise Exception("In DMPV(): Parameter 'mxtp' is not specified correctly - it could be: {'dense', ['dok','csc'], ['dok','csr'], ['ili','csc'], ['ili','csr']}")
    return F
##############################################################################
# todo: make dv2m() faster - skip for->for
def dv2m(x, cols):
    if x.shape[0] % cols != 0:
        print('Incorect data dimensions...')
        return None
    rows = int(x.shape[0]/cols)
    X = nans((rows, cols))
    current_pos = 0
    for row in range(0, rows):
        for column in range(0, cols):
            X[row][column] = x[current_pos]
            current_pos += 1
    return X
##############################################################################
def elspm(U, Y, W=None, na=0, nb=0, nc=0, pm0=0, maxiter=50, axcnv=None, xcnv=1e-8, afcnv=None, fcnv=1e-8, gcnv=None, dsp=False, smr=None):
    N, r = Y.shape
    n = max(na, nb, nc)
    nn = n - max(na, nb)

    if W is not None: raise Exception('In ELSPM: The functionality when W is not None is still not implemented...')

    Parx = lspm(U, Y, na=na, nb=nb, pm0=pm0)
    Farx = dmpm(U[nn:], Y[nn:], na=na, nb=nb, nc=0, pm0=pm0)
    E = np.vstack((np.zeros([n, r]), Y[n:, :] - lin_apl(Farx, Parx)))
    f = np.sum(np.diag(E.T@E)/N)
    # if nc == 0: return Pm, E
    Pm = np.vstack((Parx, np.zeros([r*nc, r])))
    itr = 0
    iterate = 1
    while iterate:
        itr += 1
        F = np.hstack((Farx, dmpm(E=E, nc=nc)))
        Pm_1 = Pm
        FF = F.T@F
        FF_inv = nsinv(FF)
        Pm = FF_inv@F.T@Y[n:]
        E = np.vstack((np.zeros((n, r)), Y[n:] - F@Pm))
        f_1 = f
        f = np.sum(np.diag(E.T@E)/N)
        Pm1 = m_()
        if f > f_1:
            Pm1 = Pm_1
            Pm = (Pm + Pm_1)/2
            E = np.vstack((np.zeros((n, r)), Y[n:] - F@Pm))
            if dsp == True:
                print('\n iter: ', itr, '\n Reduce step size...')
        iterate, msg = stopcrt(x=Pm, F=f, xx=Pm_1, FF=f_1, itr=itr, maxiter=50, xcnv=1e-8, fcnv=1e-8)
    if dsp == True:
        print("It took [elspm.py]", itr, "iterations to reach the end condition.")
        print(maxiter, "is the maximum number of iterations.")
    if smr is None: return Pm
    else:           return Pm, F, FF, FF_inv
##############################################################################
def elspv(U, Y, W=None, na=0, nb=0, nc=0, pm0=0, maxiter=50, axcnv=None, xcnv=1e-8, afcnv=None, fcnv=1e-8, gcnv=None, dsp=False, smr=None):
    N, r = Y.shape
    if len(U) > 0:  m = U.shape[1]
    else:           m = 0
    if isinstance(na, (int, float)):  na = np.full([r, r], na)
    if isinstance(nb, (int, float)):  nb = np.full([r, m], nb)
    if isinstance(nc, (int, float)):  nc = np.full([r, r], nc)
    if isinstance(pm0, (int, float)): pm0 = np.full([r, 1], pm0)
    n = int(np.max(np.hstack((na, nb, nc))))
    nn = int(n - np.max(np.hstack((na, nb))))

    if W is not None: raise Exception('In ELSPV: The functionality when W is not None is still not implemented...')

    parx = lspv(U, Y, na=na, nb=nb, pm0=pm0)
    Parx = pv2m(parx, na, nb, pm0=pm0)
    #
    # F1 = dmpm(U[nn:], Y[nn:], na=na, nb=nb, pm0=pm0)
    # Pm1 = nsinv(F1.T@F1)@F1.T@Y[n:]
    # Ym1 = F1@Pm1
    # E1 = np.vstack((np.zeros((n, r)), Y[n:] - Ym1))
    # f1 = np.sum(np.diag(E1.T@E1)/N)
    # mad(Pm1, Parx)
    #
    Farx = dmpm(U[nn:], Y[nn:], na=np.max(np.max(na)), nb=np.max(np.max(nb)), pm0=np.max(pm0))
    E = np.vstack((np.zeros([n, r]), Y[n:, :] - lin_apl(Farx, Parx)))
    f = np.sum(np.diag(E.T@E)/N)
    pm = np.vstack((parx, np.zeros((int(np.sum(nc)), 1))))
    Pm = np.vstack((pv2m(pm, na=na, nb=nb, pm0=pm0), np.zeros((r*int(np.max(nc)), r))))

    itr = 0
    iterate = 1
    while iterate:
        itr += 1
        F = dmpv(U, Y, E, na=na, nb=nb, nc=nc, pm0=pm0)  # todo: sparse
        pm_1 = pm
        Pm_1 = Pm
        FF = F.T@F
        FF_inv = nsinv(FF)
        pm = FF_inv@F.T@vec(Y[n:].T)  # to-do: sparse
        Pm = pv2m(pm, na=na, nb=nb, nc=nc, pm0=pm0)
        Ym = dv2m(F@pm, r)
        E = np.vstack((np.zeros([n, r]), Y[n:] - Ym))

        E = zeros(N, r)
        pm1 = lspv(U=U, Y=Y, E=E*0, na=na, nb=nb, nc=nc, pm0=pm0)
        Pm1 = pv2m(pm1, na=na, nb=nb, nc=nc, pm0=pm0)
        Pm2 = lspm(U=U, Y=Y, E=E*0, na=na[0,0], nb=nb[0,0], nc=nc[0,0], pm0=pm0[0,0])
        mad(Pm1, Pm2)
        #
        # F1 = dmpm(U[nn:], Y[nn:], na=na, nb=nb, E=E, nc=nc, pm0=pm0)
        # Pm1 = nsinv(F1.T@F1)@F1.T@Y[n:]
        # Ym1 = F1@Pm1
        # E1 = np.vstack((np.zeros((n, r)), Y[n:] - Ym1))
        # mad(Pm1, Pm)
        # mad(Ym1, Ym)
        #
        # # F = dmpv(U, Y, E, na=na, nb=nb, nc=nc, pm0=pm0)
        f_1 = f
        f = np.sum(np.diag(E.T@E)/N)
        if f > f_1:
            pm1 = pm_1
            pm = c_(pm)
            pm = (pm + pm_1)/2
            if dsp:
                print('iter: ', itr, ' Reduce step size!')
        iterate, msg = stopcrt(x=Pm, F=f, xx=Pm_1, FF=f_1, itr=itr, maxiter=50, xcnv=1e-8, fcnv=1e-8)
    pm = pm1 if f > f_1 else pm
    if smr is None: return pm
    else:           return pm, F, FF, FF_inv
##############################################################################
def lin_apl(x, pm): return x@pm
##############################################################################
# glspm():
# glspm_apl():
# glspv():
# glspv_apl():
# ivpm():
# ivpm_apl():
# ivpv():
# ivpv_apl():
# linreg OR ar, arx, armax, sarimax...
##############################################################################
def lspm(U=m_(), Y=m_(), E=m_(), Farx=m_(), F=m_(), W=m_(), na=0, nb=0, nc=0, pm0=False, ivi=None, smr=None):
    """
    Parameters
    ----------
    U : array, matrix
        input data matrix
    Y : array, matrix
        output data matrix
    par : dict; optional
        dictionary. The default is {'na':0, 'nb':0, 'pm0':False}.

    Returns
    -------
    Pm : TYPE
        DESCRIPTION.

    Description
    -----------
     LSPV calculates Least Squares (LS) estimates of ARX model in parameter matrix form.
     In case of static model factors are in matrix is U.
     mod = lspm_fit(U, Y, na, nb) determines the LS-estimates of ARX model
        A(q^-1)*yk = B(q^-1)*uk + ek
     represented in a parameter matrix form
        yk = Pm'*fk + ek,
     where:
        A(q^-1) is [el x el] polynomial matrix
           A(q^-1) = I + A1*q^-1 + ...  + Ana*q^-na 
        B(q^-1) is [el x m] polynomial matrix
           B(q^-1) = 0 + B1*q^-1 + ...  + Bnb*q^-nb
        na and nb are the maximum degrees of the polynomials in A(q^-1) and B(q^-1)
        respectively
        k - current time instant.
        uk - input vector in the k-th time instant /with m elements/
        yk - output vector in the k-th time instant /with el elements/
        ek - residual vector in the k-th time instant  /with el elements/
        fk - regression vector with [el*na + m*nb] elements in the k-th
        Pm - parameter matrix

     Inputs: 
       Y - [N x el] output data matrix with structure
           Y = [y(1) y(2) ... y(N)]',
           where N is the length of the observation interval
       U - [N x m] input data matrix with structure
           U = [u(1) u(2) ... u(N)]'
       w - [N x 1] input weight (optional - if no weight, then w = [])
       par - structure with fields:
         na - polynomials degree in A(q^-1)
         nb - polynomials degree in B(q^-1)
         intercept - 1 if model has intercept, otherwise 0. Default is 0.
    
     Outputs: 
        mod.Pm - [el*na + m*nb x el] matrix, containing the estimates of the model parameters
             Pm = [A1 A2 ... Ana B1 B2 ... Bnb]'
        mod.par
    """

    N, r = Y.shape
    m = U.shape[1]
    n = max(na, nb, nc)
    if len(F) == 0 and n > 0:       # dynamic model
        F = dmpm(U, Y, E, na=na, nb=nb, nc=nc, pm0=pm0, ivi=ivi)
    elif pm0:                       # static model with intercept
        F = np.hstack((np.ones((F.shape[0], 1)), F))
    elif len(F) == 0 and n == 0:    # unknown model type
        Pm = m_([])
        FF = m_([])
        FF_inv = m_([])
        if smr is None: return Pm
        else:           return Pm, F, FF, FF_inv
    if W is None or len(W) == 0:    # no weight
        FF = F.T@F
        FF_inv = nsinv(FF)
        Pm = FF_inv@F.T@Y[n:, :]
    else:
        if W.shape[1] > 1:  raise Exception('In LSPM: The functionality when W is a marix is still not implemented...')  # should use a tensor sparse representation
        W = W[n:, :]
        FF = F.T@(W*F)
        FF_inv = nsinv(FF)
        Pm = FF_inv@F.T@(W*Y[n:, :])
    if smr is None: return Pm
    else:           return Pm, F, FF, FF_inv
##############################################################################
def lspv(U=m_(), Y=m_(), E=m_(), Farx=m_(), F=m_(), W=m_(), na=None, nb=None, nc=None, pm0=False, ivi=None, mxtp='dense', smr=None):
    ww = W
    
    N, r = Y.shape
    m = U.shape[1]
    if na is None: na = zeros(r, r)
    elif isinstance(na, (int, float)): na = int(na); na = ones(r, r)*na
    if nb is None: na = zeros(r, r)
    elif isinstance(nb, (int, float)): nb = int(nb); nb = ones(r, m)*nb
    if nc is None: nc = zeros(r, r)
    elif isinstance(nc, (int, float)): nc = int(nc); nc = ones(r, r)*nc
    n = int(np.max(np.max(np.hstack((na, nb, nc)))))
    if len(F) == 0 and n > 0:       # dynamic model
        F = dmpv(U, Y, E, na=na, nb=nb, nc=nc, pm0=pm0, mxtp=mxtp)
    elif pm0:  # static model with intercept
        F = np.hstack((np.ones((F.shape[0], 1)), F))
    elif len(F) == 0 and n == 0:  # unknown model type
        pm = m_([])
        FF = m_([])
        FF_inv = m_([])
        if smr is None: return pm
        else:           return pm, F, FF, FF_inv
    if W is None or len(W) == 0:  # no weight
        if mxtp == 'dense': FF = F.T@F;     FF_inv = nsinv(FF);     pm = FF_inv@F.T@vec(Y[n:,:].T)
        else:
            FF = F.transpose()*F
            if np.any(mxtp[1] in ['csr', 'bsr']): FF_inv = [];                pm = c_(spsolve(FF, F.transpose()*(vec(Y[n:,:].transpose())))) #!!!!! FF_inv = [] - da ia smetna
            elif mxtp[1] == 'csc':                FF_inv = spinv(FF.tocsc()); pm = FF_inv*F.transpose()*(vec(Y[n:,:].transpose()))
    else:
        if W.shape[1] == 1 and Y.shape[1] > 1:  W = m_(W[n:N,:]*ones(1, r), ((N-n)*r, 1))
        elif W.shape[1] > 1:                    W = m_(W[n:N,:], ((N-n)*r, 1))
        if mxtp == 'dense':
            FF = F.T@(W*F); FF_inv = nsinv(FF);     pm = FF_inv@F.T@(W*vec(Y[n:,:].T))
        else:
            if W.shape[1] == 1 and Y.shape[1] > 1:  W = m_(W[n:N,:]*ones(1, r), ((N-n)*r, 1))
            elif W.shape[1] > 1:                    W = m_(W[n:N,:], ((N-n)*r, 1))
            W = diags(W.flatten())
            FF = F.transpose()*(W*F)
            if np.any(mxtp[1] in ['csr', 'bsr']): FF_inv = [];              pm = c_(spsolve(FF, F.transpose()*(W*vec(Y[n:,:].transpose()))))
            elif mxtp[1] == 'csc':                FF_inv = spinv(FF.tocsc()); pm = FF_inv*F.transpose()*(W*vec(Y[n:,:].transpose()))
    if smr is None: return pm
    else:           return pm, F, FF, FF_inv
##############################################################################
def pm2v(Pm, na=None, nb=None, nc=0, pm0=0):
    # todo: include nc and pm0
    r = m = 1
    z = na + nb
    if z == 0: return np.empty((1, 1))
    pm = np.array(())
    for i in range(0, r):
        pari = Pm[:, i]
        if na > 0:
            for j in range(0, r):
                pij = pari[j + j:r*na + j:r]
                pm = np.hstack((pm, pij))
        if nb > 0:
            for j in range(0, m):
                pij = pari[j + j + r*na:m*nb + j + r*na:m]
                pm = np.hstack((pm, pij))
    return c_(pm)
##############################################################################
def pv2m(pm,
         na=None,
         nb=None,
         nc=None,
         pm0=None,
         par={}):
    if not np.array([nb == None]).any():
        r, m = nb.shape
    elif not np.array([na == None]).any():
        r = na.shape[0]
        m = 0
    elif not np.array([nc == None]).any():
        r = nc.shape[0]  # todo: use try-except --> at least one of {na, nb, nc} should be provided
        m = 0
    if np.array([na == None]).any():
        if 'na' in par:
            na = par['na']
        else:
            na = np.zeros((r, r))
    if np.array([nb == None]).any():
        if 'nb' in par:
            nb = par['nb']
        else:
            nb = np.zeros((r, m))
    if np.array([nc == None]).any():
        if 'nc' in par:
            nc = par['nc']
        else:
            nc = np.zeros((r, r))
    if np.array([pm0 == None]).any():
        if 'pm0' in par:
            pm0 = par['pm0']
        else:
            pm0 = np.zeros((r, 1))

    pm = c_(pm)
    nna = int(np.max(na)) if na.size > 0 else 0
    nnb = int(np.max(nb)) if nb.size > 0 else 0
    nnc = int(np.max(nc)) if nc.size > 0 else 0
    nni = np.any(pm0)
    z = r*nna + m*nnb + r*nnc + nni
    if z == 0:
        Pm = m_()
        return Pm
    Pm = np.zeros((r, z))
    ii = 0
    for i in range(0, r):
        if pm0.size > 0:
            if pm0[i]:
                Pm[i, 0] = pm[int(ii)]
                ii += pm0[i]
        if nna:
            for j in range(0, r):
                Pm[i, (nni + j):(nni + j + int(na[i, j]*r)):r] = pm[int(0 + ii):int(na[i, j] + ii), 0]
                ii += na[i, j]
        if nnb:
            for j in range(0, m):
                Pm[i, (nni + j + r*nna):int(nni + j + r*nna + nb[i, j]*m):m] = pm[int(0 + ii):int(nb[i, j] + ii), 0]
                ii += nb[i, j]
        if nnc:
            for j in range(0, r):
                Pm[i, (nni + j + r*nna + m*nnb):int(nni + j + r*nna + m*nnb + nc[i, j]*r):r] = pm[int(0 + ii):int(nc[i, j] + ii), 0]
                ii += nc[i, j]
    return Pm.T
##############################################################################
# function Y = repmatc(X, m)
# % Columnwise reproduction (m times) of X matrix, i.e. Y = [X X ... X]
# """ USE np.tile """
# def repmatc(X, m):
#     n = X.shape[1]
#     n = size(X,2)
#     Y = X(:, rem(0:(n*m - 1), n) + 1);
#     return Y
##############################################################################
# model_list = roblspm(U, Y, par, opt_dvaf, opt_max_iter, opt_hst)
def roblspm(U, Y, na=0, nb=0, pm0=0, maxiter=50, dvaf=1e-2, hst=0):
    """
    Parameters
    ----------
    U : vector, matrix
        independent variables.
    Y : vector, matrix
        dependent variables.
    par : dict, optional
        DESCRIPTION. The default is {'na':0, 'nb':0, 'pm0':False}.
    opt : dict, optional
        DESCRIPTION. The default is {'maxiter': 100, 'dvaf': 1e-2 , 'hst': 0}.
        maxiter: maximum number of iterations to run
        dvaf: delta in "variance accounted for" statistics*100; 0% is bad, 100% is good
        hst: whether to keep iteration history in the model object

    Returns
    -------
    return_list : TYPE
        DESCRIPTION.

    """
    N, r = Y.shape
    m = U.shape[1]
    n = max([na, nb])
    F = dmpm(U, Y, na=na, nb=nb, nc=0, pm0=pm0)
    Pm = nsinv(F.T@F)@F.T@Y[n:N][:]
    Ym = F@Pm
    Y1 = Y[n:, :]
    vafw = vaf(Y1, Ym)
    vaf0 = vafw
    if hst:
        VAFw = vafw
        VAF = vaf0
        PM = pm2v(Pm, na=na, nb=nb, pm0=0) # todo: make pm2v() to work for pm0=1
    iter_n = 0
    iterate = 1
    while iterate:
        iter_n += 1
        ww = np.minimum(1, np.maximum(1e-8, 1/abs(Y1 - Ym)))
        for i in range(r):
            Wi = np.matlib.repmat(c_(ww[:, i]), 1, r*na + m*nb)
            Pm[:, i] = nsinv(F.T@(Wi*F))@F.T@(ww[:, i]*Y1[:, i])
        Ym = F@Pm
        vafw_1 = vafw
        vafw = vaf(Y1, Ym, ww)
        vaf0 = vaf(Y1, Ym)
        if hst:
            PM = np.append(PM, pm2v(Pm, na, nb, pm0=0)) if PM.size > 0 else pm2v(Pm, na, nb, pm0=0)
            VAFw = np.append(VAFw, vafw)
            VAF = np.append(VAF, vaf0)
        iterate = 0 if any(abs(vafw - vafw_1) <= dvaf) or iter_n >= maxiter else 1
    if hst:
        st = {'PM':PM, 'vafw':vafw, 'vaf0':vaf0, 'iterations':iter_n}
    else:
        st = []
    return Pm, st
##############################################################################
def roblspm_apl(U, Y, Pm, na=0, nb=0, pm0=0):
    F = dmpm(U, Y, na=na, nb=nb)
    Ym = F@Pm
    return Ym
##############################################################################
def roblspv(U, Y, na=0, nb=0, pm0=0, maxiter=50, dvaf=1e-2, hst=0):
    N, r = Y.shape
    if len(U) > 0:
        N, m = U.shape
    else:
        m = 0
    if len(Y) > 0:
        N, r = Y.shape
    else:
        r = 0
    if not N > 0:
        print('In ELSPV: At least one data matrix should be not empty...')
        return None
    if isinstance(na, (int, float)):  na = np.full([r, r], na)
    if isinstance(nb, (int, float)):  nb = np.full([r, m], nb)
    if isinstance(pm0, (int, float)): pm0 = np.full([r, 1], pm0)
    n = int(np.max(np.hstack((na, nb))))
    y = vec(Y[n:].T)
    F = dmpv(U, Y, na=na, nb=nb, pm0=pm0)
    pm = nsinv(F.T@F)@F.T@y
    ym = F@pm
    vafw = vaf(dv2m(y, r), dv2m(ym, r))
    vaf0 = vafw
    if hst:
        VAFw = vafw
        VAF = vaf0
        PM = pm
        YM = ym
    # -------------------------------------------------------------------    
    iter_n = 0
    iterate = True
    while iterate:
        iter_n += 1
        # print("THIS IS ITERATION ", iter_n)
        w = np.minimum(1, np.maximum(1e-8, abs(y - ym)**-1))  ## CHECK
        # ww = repmatc(w, size(F, 2)); ## what is repmatC ?
        ww = np.tile(w, F.shape[1])
        # ww and F should have one same dimension:
        pm = np.linalg.inv(F.T@(ww*F))@(ww*F).T@y
        ym = F@pm
        vafw_1 = vafw
        vafw = vaf(dv2m(y, r), dv2m(ym, r), dv2m(w, r))
        vaf0 = vaf(dv2m(y, r), dv2m(ym, r))

        if hst:
            PM = np.hstack((PM, pm))
            VAFw = np.hstack((VAFw, vafw))
            VAF = np.hstack((VAF, vaf0))
            YM = np.hstack((YM, ym))
        if any(abs(vafw - vafw_1)) <= dvaf or iter_n >= maxiter:
            iterate = False
    if hst:  # st.
        st = {'PM':PM, 'vafw':vafw, 'vaf0':vaf0, 'iterations':iter_n}
    else:
        st = []
    # ----------------------------------------------------------------
    return pm, st
##############################################################################
# def roblspv_apl():
##############################################################################

"""
    author: OPEN-MAT
    date: 	15.06.2019
    Matlab version: 26 Apr 2009
    Course: Multivariable Control Systems
"""
import numpy as np
from numpy import matlib

from aislab.md_reg.linest import *
from aislab.md_fsel.swlinr import *
from aislab.gnrl.bf import *# c_
from aislab.gnrl.sf import *
from aislab.gnrl.measr import*

##############################################################################
def arx(U, Y, W=None, na=None, nb=None, pm0=None, cnames=None, rtp='PV', mxtp='dense', smr=True, fsel=None, SLE=0.05, SLS=0.05, crit_nbm={'p_Fp':'max','AIC':'all'}, mdl_init='empty', ivi=None, val_prc=0, fsel_dsp=False, s_min=1e-12):
    # Check rtp and par
    if not rtp=='PM' and not rtp=='PV': raise Exception("In ARX(): Parameter rtp has not a correct value (should be 'PM' or 'PV').")

    # Check data matrices & W
    U = chkdm(U, N=len(Y), name='U', fname='ARX()')
    Y = chkdm(Y, N=len(Y), name='Y', fname='ARX()')
    W = chkw(W, N=len(Y), fname='ARMAX()')

    # Sizes of the data matrices
    N, r = Y.shape
    m = U.shape[1]

    # Check na and nb
    na = chkn(n=na, size=(r, r), rtp=rtp, name='na', fname='ARX()')
    nb = chkn(n=nb, size=(r, m), rtp=rtp, name='nb', fname='ARX()')
    n = np.max(np.hstack((na, nb)))
    if np.max(n) == 0: raise Exception('In ARX(): At least one model structure parameter (na, nb) must be non negative or with non-negative elements.')

    # Check pm0
    pm0 = chkpm0(pm0, r=r, rtp=rtp, fname='ARX()')

    if cnames is None:  cnames = names(na=na, nb=nb, pm0=pm0, r=r, m=m, rtp=rtp)
    
    # check rtp
    if not np.any(rtp in ['PM', 'PV']): raise Exception('In ARX(): rtp should be \'PM\' - Parameter Matrix Representation or \'PV\' - Parameter Vector Representation.')

    # check ivi
    ivi = checkivi(ivi, rtp=rtp, r=r)

    mtp = 'arx'
    if fsel is None:
        mdl = ts(U, Y, W=W, na=na, nb=nb, pm0=pm0, ivi=ivi, cnames=cnames.flatten(), mtp=mtp, rtp=rtp, smr=smr, s_min=s_min)
    elif fsel == 'SWR':
        mdl = swlinr(U=U, Y=Y, W=W, na=na, nb=nb, pm0=pm0, cnames=cnames, mtp=mtp, rtp=rtp, met=fsel, SLE=SLE, SLS=SLS, crit_nbm=crit_nbm, mdl_init=mdl_init, ivi=ivi, val_prc=val_prc, s_min=s_min, dsp=fsel_dsp)
        
    return mdl

def armax(U, Y, W=None, na=None, nb=None, nc=None, pm0=None, rtp='PV', smr=True):
    # Check rtp and par
    if not rtp=='PM' and not rtp=='PV': raise Exception("In ARMAX(): Parameter rtp has not a correct value (should be 'PM' or 'PV').")

    # Check data matrices & W
    U = chkdm(U, N=len(Y), name='U', fname='ARMAX()')
    Y = chkdm(Y, N=len(Y), name='Y', fname='ARMAX()')
    W = chkw(W, N=len(Y), fname='ARMAX()')

    # Sizes of the data matrices
    N, r = Y.shape
    m = U.shape[1]

    # Check na, nb and nc
    na = chkn(n=na, size=(r, r), rtp=rtp, name='na', fname='ARMAX()')
    nb = chkn(n=nb, size=(r, m), rtp=rtp, name='nb', fname='ARMAX()')
    nc = chkn(n=nc, size=(r, r), rtp=rtp, name='nc', fname='ARMAX()')
    # Check pm0
    pm0 = chkpm0(pm0, r=r, rtp=rtp, fname='ARMAX()')

    mtp = 'armax'
    mdl = ts(U, Y, W, na, nb, nc, pm0, mtp, rtp, smr)
    # if smr: mdl = stat()
    return mdl
##############################################################################

##############################################################################
def armax_apl(mdl=None, U=None, Y=None, E=None, pm=None, na=None, nb=None, pm0=None, rtp='PV', smr=False, sim=False, ltv=False):
    if mdl is not None: # todo: remove all model structure parameters (na, nb, nc, pm0, rtp) and keep only mdl
        pm = mdl['pm']
        na = mdl['na']
        nb = mdl['nb']
        nc = mdl['nc']
        pm0 = mdl['pm0']
        rtp = mdl['rtp']
        m = mdl['m']
        r = mdl['r']

    if rtp == 'PV':
        pm = pv2m(pm, na, nb, nc, pm0=pm0) # if model in PV form --> goto PM form
        na = np.max(np.max(na))
        nb = np.max(np.max(nb))
        nc = np.max(np.max(nc))
        pm0 = np.max(pm0)
    n = np.max(np.max(np.hstack((na, nb, nc))))
    if not sim:
        if n == 0:
            if pm0: U = np.hstack((np.ones((U.shape[0], 1)), U))
            Ym = lin_apl(U, pm)
        else:
            F = dmpm(U, Y, na=na, nb=nb, pm0=pm0)
            Yarx = lin_apl(F, pm[:(pm0 + na*r + nb*m), :])
            E = Y[n:, :] - Yarx[(n-np.max([na, nb])):, :]
            F = dmpm(E=E, nc=nc)
            Yma = lin_apl(F, pm[(pm0 + na * r + nb * m):, :])
            Ym = Yarx[nc:, :] + Yma
    else:
        N = U.shape[0]
        r = pm.shape[1]
        if E is None: E = zeros((N, r))
        Ym = np.zeros((N, r))
        for k in range(nn, N):
            fi = dmpm(U[k - nn:k + 1, :], Ym[k - nn:k + 1, :], E[k - nn:k + 1, :], na=na, nb=nb, nc=nc, pm0=pm0)
            Ym[k, :] = fi@pm + r_(E[k, :])
    if smr is None: F = m_([])
    return Ym, F

##############################################################################
def arx_apl(mdl=None, U=None, Y=None, E=None, pm=None, na=None, nb=None, pm0=None, rtp='PV', ivi=None, smr=False, sim=False, ltv=False):
    if mdl is not None: # todo: remove all model structure parameters (na, nb, nc, pm0, rtp) and keep only mdl
        if isinstance(mdl, list): mdl = mdl[-1] # if mdl is generated by swlinr()
        pm = mdl['pm']
        na = mdl['na']
        nb = mdl['nb']
        pm0 = mdl['pm0']
        rtp = mdl['rtp']
        m = mdl['m']
        r = mdl['r']
        if 'ivi' in mdl: ivi = mdl['ivi']
    if not sim:
        if rtp == 'PV':
            pm = pv2m(pm, na, nb, pm0=pm0)  # if model in PV form --> goto PM form
            na = np.max(np.max(na))
            nb = np.max(np.max(nb))
            pm0 = np.max(pm0)
            ivi = np.arange(r*na + m*nb + pm0)
        n = int(np.max(np.hstack((na, nb))))
        if n == 0:
            if pm0: U = np.hstack((np.ones((U.shape[0], 1)), U))
            Ym = lin_apl(U, pm)
        else:
            
            F = dmpm(U, Y, na=na, nb=nb, pm0=pm0, ivi=ivi)
            Ym = lin_apl(F, pm) # Ym = lin_apl(F, pm[:(pm0 + na*r + nb*m), :])
    else:
        N = U.shape[0]
        if ltv and rtp == 'PV': r, m = nb.shape
        else:                   r = pm.shape[1] # !!!!! m = ?
        nna = np.max(np.max(na))
        nnb = np.max(np.max(nb))
        if E is None: E = zeros((N, r))
        if smr: F = nans(N, np.max(pm0) + r*nna + m*nnb)
        Ym = np.zeros((N, r))
        n = int(np.max(np.hstack((na, nb))))
        if ltv:
            for k in range(n, N):
                if rtp == 'PV':
                    pmk = pv2m(pm[:, k], na, nb, pm0=pm0)
                fi = dmpm(U[k - n:k + 1, :], Ym[k - n:k + 1, :], na=na, nb=nb, pm0=pm0, ivi=ivi)
                Ym[k, :] = fi@pmk + r_(E[k, :])
                if smr: F[k-n, :] = fi
        else:
            for k in range(n, N):
                if rtp == 'PV':
                    pm = pv2m(pm, na, nb, pm0=pm0)
                fi = dmpm(U[k - n:k + 1, :], Ym[k - n:k + 1, :], na=na, nb=nb, pm0=pm0, ivi=ivi)
                Ym[k, :] = fi@pm + r_(E[k, :])
                if smr: F[k-n, :] = fi

    if smr: return Ym, F
    else:   return Ym  #  F = m_([])

##############################################################################
def chkdm(X, N=None, name=None, fname=None):
    if N == 0: raise Exception('In ' + fname + ': Data matrices must not be empty.')
    try:
        size = (N, X.shape[1])
        if type(X) != np.ndarray:   X = m_(X, size)
    except:
        raise Exception('In ' + fname + ': ' + name + ' must be a matrix (np.ndarray or a list with appropriate dimension) with ' + str(N) + ' rows.')
    if X.size == 0:
        raise Exception('In ' + fname + ': ' + name + ' must not be empty matrix.')
    return X

##############################################################################
def checkivi(ivi, rtp=None, r=None):
    try:
        if rtp == 'PM':
            if isinstance(ivi, (int, float)): ivi = m_([ivi], tp=int)
            if isinstance(ivi, list): ivi = m_(ivi, tp=int)
        else:
            if isinstance(ivi, list) and len(ivi) == r:
                for i in np.arange(r):
                    if isinstance(ivi[i], (int, float)): ivi[i] = m_([ivi[i]], tp=int)
                    if isinstance(ivi[i], list): ivi[i] = m_(ivi[i], tp=int)
            else: raise Exception('In ARX(): ivi should be a scalar, list or 1D nd.array.')
    except: raise Exception('In ARX(): ivi should be a scalar, list or 1D nd.array.')
    return ivi

##############################################################################
def chkn(n=None, size=None, rtp=None, name=None, fname=None):
    # n is a scalar
    if isinstance(n, (int, float, str, np.int64)):
        n = int(n)
        if rtp == 'PV': n = np.full((size[0], size[1]), n)
    # PV & n is a list or np.ndarray
    if rtp == 'PV':
        msg  ='In ' + fname + ': In PV representation ' + name + ' must be an integer scalar or a matrix (np.ndarray or list with appropriate structure) of size ' + str(size[0]) + ' x ' + str(size[1]) + '.'
        try:
            n = m_(n, size)
            if np.any(n.shape != size): raise Exception(msg)
        except: raise Exception(msg)
    # PM & n is a scalar
    if rtp == 'PM' and not (isinstance(n, int) or np.all(n.shape == (1, 1))):   raise Exception('In ' + fname + ': In PM representation ' + name + ' must be an integer scalar or a matrix (np.ndarray or list) of size 1 x 1.')
    if rtp == 'PM' and not isinstance(n, int):   n = n[0, 0]
    # values of n
    if np.any(n == np.nan) or np.any(n == np.inf) or np.any(n < 0):  raise Exception('In ' + fname + ': ' + name + ' must be nonnegative integer.')
    return n

##############################################################################
def chkpm0(pm0, r=None, rtp=None, fname=None):
    # pm0 is a scalar
    if isinstance(pm0, (int, float, str, np.int64)):
        pm0 = int(pm0)
        if rtp == 'PV': pm0 = np.full((r, 1), pm0)
    # PV & pm0 is a list or np.ndarray
    if rtp == 'PV':
        msg  ='In ' + fname + ': In PV representation pm0 must be an integer scalar or a matrix (np.ndarray or list with appropriate structure) of size ' + str(r) + ' x ' + str(1) + '.'
        try:
            pm0 = m_(pm0, (r, 1))
            if np.any(pm0.shape != (r, 1)): raise Exception(msg)
        except: raise Exception(msg)
    # PM & pm0 is a scalar
    if rtp == 'PM' and not (isinstance(pm0, int) or np.all(n.shape != (1, 1))):   raise Exception('In ' + fname + ': In PM representation pm0 must be an integer scalar or a matrix (np.ndarray or list) of size 1 x 1.')
    # values of pm0
    if not np.all((pm0 != 0) | (pm0 != 1)):  raise Exception('In ' + fname + ': pm0 must be integer - 0 or 1.')
    return pm0

##############################################################################
def chkw(X, N=None, fname=None):
    if N == 0: raise Exception('In ' + fname + ': Weight factor must not be empty.')
    try:
        size = (N, X.shape[1])
        if type(X) != np.ndarray:   X = m_(X, size)
    except:
        raise Exception('In ' + fname + ': Weight factor must be a column vector (np.ndarray or list) with length ' + str(N) + '.')
    if X.size == 0:
        raise Exception('In ' + fname + ': Weight factor must not be empty matrix.')
    return X

##############################################################################
def names(name='var_', z=1, na=None, nb=None, nc=None, pm0=None, r=None, m=None, rtp=None):
    # z - number of factors
    # n - number(s) pf lagged variables
    if rtp == None: return c_([name + str(i) for i in range(1, z+1)])

    cnames = []
    if rtp == 'PM':
        if pm0 is not None:
            if isinstance(pm0, np.ndarray): pm0 = int(pm0[0, 0])
            if pm0: cnames = cnames + ['intercept']
        if na is not None:
            if isinstance(na, np.ndarray): na = int(na[0, 0])
            if not isinstance(na, int): na = int(na)
            cnames = cnames + names1('-y', n=na, rtp='PM', r=r)
        if nb is not None:
            if isinstance(nb, np.ndarray): nb = int(nb[0, 0])
            if not isinstance(nb, int): nb = int(nb)
            cnames = cnames + names1('u', nb, rtp='PM', r=m)
        if nc is not None:
            if isinstance(nc, np.ndarray): nc = int(nc[0, 0])
            if not isinstance(nc, int): nc = int(nc)
            cnames = cnames + names1('e', nc, rtp='PM', r=r)

        return c_(cnames)
    elif rtp == 'PV':
        if pm0 is not None and isinstance(pm0, (int, float)): pm0 = repmat(pm0, r, 1)
        if na is not None and isinstance(na, (int, float)): na = repmat(na, r, r)
        if nb is not None and isinstance(nb, (int, float)): nb = repmat(nb, r, m)
        if nc is not None and isinstance(nc, (int, float)): nc = repmat(nc, r, r)
        for i in range(1, r + 1):
            if pm0 is not None and pm0[i-1]:  cnames = cnames + ['intercept -> y' + str(i) + '(k)']
            if na is not None:
                for j in range(1, r + 1): cnames = cnames + names1('-y', na[i-1, j-1], rtp='PV', i=i, j=j)
            if nb is not None:
                for j in range(1, m + 1): cnames = cnames + names1('u', nb[i-1, j-1], rtp='PV', i=i, j=j)
            if nc is not None:
                for j in range(1, r + 1): cnames = cnames + names1('e', na[i-1, j-1], rtp='PV', i=i, j=j)
    return c_(cnames)

##############################################################################
def names1(name, n, rtp=None, r=None, m=None, i=None, j=None):
    if rtp == 'PM':
        # cnames = [name + str(i) + '_(k-' + str(k) + ')' for k in range(1, n + 1) for i in range(1, r+1)]
        cnames = [name + str(i) + '(k-' + str(k) + ')' for k in range(1,n+1) for i in range(1, r+1)]
    elif rtp == 'PV':
        # cnames = [name + str(i) + ',' + str(j) + '_(k-' + str(k) + ')' for k in range(1, n+1)]
        # cnames = [name + str(i) + ',' + str(j) + ',k-' + str(k) + '' for k in range(1, n+1)]
          cnames = [name + str(j) + '(k-' + str(k) + ') -> y' + str(i) + '(k)' for k in range(1, n+1)]
    return cnames


##############################################################################
def ts(U, Y, W=None, na=None, nb=None, nc=None, pm0=None, ivi=None, cnames=None, mtp=None, rtp=None, mxtp='dense', smr=None, s_min=1e-12):
    if mtp == 'arx':
        if rtp == 'PM':     pm, F, FF, FF_inv = lspm(U, Y, W=W, na=na, nb=nb, pm0=pm0, ivi=ivi, smr=smr)
        elif rtp == 'PV':   pm, F, FF, FF_inv  = lspv(U, Y, W=W, na=na, nb=nb, pm0=pm0, ivi=ivi, smr=smr, mxtp=mxtp)
        mdl = {'pm': pm,
               'na': na,
               'nb': nb,
               'pm0': pm0,
               'ivi': ivi,
               'm': U.shape[1],
               'r': Y.shape[1],
               'mtp': mtp,
               'rtp': rtp,
               'cnames': cnames,
               'smr': smr,
               }
    if mtp == 'armax':
        if rtp == 'PM':     pm, F, FF, FF_inv  = elspm(U, Y, na=na, nb=nb, nc=nc, pm0=pm0, smr=smr)
        elif rtp == 'PV':   pm, F, FF, FF_inv  = elspv(U, Y, na=na, nb=nb, nc=nc, pm0=pm0, smr=smr)
        # st = stat(...) - from swlinr
        mdl = {'pm': pm,
               'na': na,
               'nb': nb,
               'nc': nc,
               'pm0': pm0,
               'm': U.shape[1],
               'r': Y.shape[1],
               'mtp': mtp,
               'rtp': rtp,
               'cnames': cnames,
               'smr': smr,
               }

    if smr:
        # From {F, Y, W} are calc all stats.
        # These 3 matrices could be for val sample, i.e. {Fv, Yv, Wv}
        # and smr to represent both st_dev=f(F, Y, W, FF, FF_inv) and st_val=(Fv, Yv, Wv).
        mdl['st'] = {}
        if mtp == 'arx':
            N = Y.shape[0]
            n = np.max(np.max(np.hstack((na, nb))))
            if rtp == 'PM':
                st0 = stats(F, Y[n:, :], W[n:,:], m=mdl['m'], r=mdl['r'], na=na, nb=nb, nc=nc, pm0=pm0, rtp='PM', s_min=s_min)
            elif rtp == 'PV':
                st0 = stats(F, Y[n:, :], W[n:,:], rtp='PV', m=mdl['m'], r=mdl['r'], na=na, nb=nb, nc=nc, pm0=pm0, s_min=s_min)
            z = st0['z']
            pm = mdl['pm']
            FF = st0['FF']
            rcM = 1 / np.linalg.cond(FF)  # todo: create function in sf, calculating condition number
            if rcM < 1e-3:  P = nsinv(FF, s_min)
            else:           P = np.linalg.inv(FF)
            if isinstance(z, np.ndarray):
                if ivi is None:
                    ivi = []; ivo = []
                    for zi in z:
                        ivi.append(np.arange(zi))
                        ivo.append(np.array([]).astype(int))
            else:
                if ivi is None: ivi = np.arange(z)
                ivo = np.array([]).astype(int)
            mdl['ivi'] = ivi
            mdl['ivo'] = ivo
            FY = st0['FY']
            wF = st0['wF']
            st_ext = stmdl(FB='BE1', model=mdl, rtp=rtp, FY=FY, P=P, wF=wF, n2=z, n1=[], st0=st0)
            mdl['p'] = z
            mdl = {**mdl, **[htmdl('BE1', [], 'BE', z, ivi, ivo, cnames, [], pm, st_ext['ovr'], rtp=rtp)][0]}

    1;
    return mdl


# # mdl['pm']     --> swlinr
# # mdl['mtp']    --> swlinr
# # mdl['na']
# # mdl['pm0']
# # mdl['smr']...  st --> swlinr
# Ym, mdl = arx_apl(mdl, U, Y, smr=True)
# # ? mdl['Ym']

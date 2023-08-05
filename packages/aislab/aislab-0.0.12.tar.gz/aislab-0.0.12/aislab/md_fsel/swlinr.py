# S T E P W I S E   L I N E A R  R E G R E S S I O N
#--------------------------------------
# Author: Alexander Efremov
# Date:   05.09.2009 /matlab version/
# Course: Multivariable Control Systems
#--------------------------------------
import numpy as np
from numpy.matlib import repmat
import pandas as pd
import copy
import warnings as wn

from gnrl.sf import *
from gnrl.measr import *

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('precision', 5)

# def gswlinr():
###################################################################################
###################################################################################
def bElimin(model, st0, met, cnames, s_min, SLS, crit_nbm, iterate):
    Nw, r, z, FY, FF, wF, ivi, ivo, n1, n2 = parin(st0, model[-1])
    # ----- Calculate significance of factors in the model -----
    if met == 'FR' and n2 == z:
        iterate = 0
        return model, iterate
    ivi0 = ivi
    ivo0 = ivo
    if ivi.shape[0] > 1:
        n1 = ivi.shape[0]
        n2 = n2 - 1
        pm = nans((n2, r), n1)
        st = []
        for i in np.arange(n1):
            ivi = ivi0[np.hstack((np.arange(0, i), np.arange(i + 1, n1)))]
            pmi, P = mdl(sm_(FF, ivi, ivi), sm_(FY, ivi), s_min)
            pm[:, :, i] = pmi
            st = st + [stmdl(FB='BE', model=model[-1], FY=sm_(FY, ivi), P=P, wF=sm_(wF, ivi), n2=n2, n1=n1, st0=st0)]
        st_in = [s['in'] for s in st]
        model[-1] = htmdl('BE2', model[-1], st=st_in)
        flg = 1
    else:
        # model[-1] = htmdl('BE2', model[-1])
        flg = 0
    # ----- Find next best model -----
    if met == 'FR': return model, st0, iterate
    if flg:
        p_Fpi, pmi, sti, ind = nextmdl('BE2', model, st, pm, crit_nbm)
        if p_Fpi > SLS:
            ivi = delrc(ivi0, ind)
            ivo = np.hstack((ivo, ivi0[ind]))
            z = htmdl('BE1', model[-1], 'BE', n2, ivi, ivo, cnames, ivi0[ind], pmi, sti)
            model = model + [z]
        else:
            if met == 'BR':
                iterate = 0
            else:
                model[-1]['FB'] = 'BE_stop'
    elif met == 'BR':
        iterate = 0
    else:
        model[-1]['FB'] = 'BE_stop'
    return model, iterate


###################################################################################
def firstmdl(st0, mdl_init, s_min, cnames, ivi, rtp='PM'):
    if mdl_init == 'full':
        z = st0['z']
        FF = st0['FF']
        FY = st0['FY']
        wF = st0['wF']
        ivi = np.arange(z)
        ivo = np.array([]).astype(int)
        n2 = z
        pm, P = mdl(FF, FY, s_min)
        st_ext = stmdl('BE1', [], FY, P, wF, n2, [], st0)
        # st_ext2 = stmdl('FS1', [], FY, P, wF, n2, [], st0)
        model = [htmdl('BE1', [], 'BE', n2, ivi, ivo, cnames, [], pm, st_ext['ovr'])]
    elif mdl_init == 'empty':
        z = st0['z']
        if rtp == 'PM':
            cn = cnames[0]
            FF = np.array([[st0['FF'][0, 0]]])
            FY = np.array([st0['FY'][0]])
            wF = np.array([st0['wF'][0, 0]])
            ivi = m_([0])
            ivo = np.arange(1, z)
            n2 = 1
        else:
            cz = np.hstack((0, np.cumsum(z[:-1]))).astype(int)
            cn = cnames[cz]
            r = st0['r']
            FF = zeros(r, r); FY = nans(r, 1); wF = nans(1, r); ivi = [None]*r; ivo = [None]*r
            for i in np.arange(r):
                ii = cz[i]
                FF[i, i] = np.array([[st0['FF'][ii, ii]]])
                FY[i] = np.array([st0['FY'][ii]])
                wF[0, i] = np.array([st0['wF'][0, ii]])
                ivi[i] = m_([ii])
                ivo[i] = np.arange(1, z[i])
            n2 = ones((r,))
        pm, P = mdl(FF, FY, s_min)
        model0 = {'ivi': ivi,
                  'ivo': ivo
                 }
        st_ext = stmdl(FB='FS1', model=model0, rtp=rtp, FY=FY, P=P, wF=wF, n2=n2, n1=[], st0=st0)
        model = [htmdl('FS1', [], 'FS', n2, ivi, ivo, cnames, [], pm, st_ext['ovr'])]
    elif mdl_init == 'init':
        z = st0['z']
        # ivo = np.array(list(set(np.arange(z)) - set(ivi.flatten())))
        # n2 = ivi.shape[0]
        # FF = sm_(st0['FF'], ivi, ivi)
        # FY = sm_(st0['FY'], ivi)
        # wF = sm_(st0['wF'], ivi)
        # pm, P = mdl(FF, FY, s_min)
        # model0 = {'ivi': ivi,
        #           'ivo': ivo
        #          }
        # st_ext = stmdl(FB='FS1', model=model0, rtp=rtp, FY=FY, P=P, wF=wF, n2=n2, n1=[], st0=st0)
        # model = [htmdl('FS1', [], 'FS', n2, ivi, ivo, cnames, [], pm, st_ext['ovr'])]
        
        if rtp == 'PM':
            ivo = np.array(list(set(np.arange(z)) - set(ivi.flatten())))
            n2 = ivi.shape[0]
            cn = cnames[ivi]
            FF = sm_(st0['FF'], ivi, ivi)
            FY = sm_(st0['FY'], ivi)
            wF = sm_(st0['wF'], ivi)
        else:
            r = st0['r']
            if ivi is None:
                cz = np.hstack((0, np.cumsum(z[:-1]))).astype(int)
                cn = cnames[cz]
                FF = zeros(r, r);
                FY = nans(r, 1);
                wF = nans(1, r);
                ivo = [m_([])]*r
                ivo = [m_([])]*r
                for i in np.arange(r):
                    ii = cz[i]
                    FF[i, i] = np.array([[st0['FF'][ii, ii]]])
                    FY[i] = np.array([st0['FY'][ii]])
                    wF[0, i] = np.array([st0['wF'][0, ii]])
                    ivi[i] = m_([ii])
                    ivo[i] = np.arange(1, z[i])
                n2 = ones((r,))
            else:
                ivo = [m_([])]*r
                n2 = [None]*r
                cn = m_([[]], 0, 1)
                FFi = [None]*r
                zz = np.hstack((0, np.cumsum(z)))
                for i in np.arange(r):
                    ii = ivi[i]
                    ivo[i] = np.array(list(set(np.arange(zz[i], zz[i+1])) - set(ii)))
                    n2[i] = ii.shape[0]
                    cn = np.vstack((cn, cnames[ii]))
                    FFi[i] = sm_(st0['FF'], ii, ii)
                    if i == 0:
                        FY = sm_(st0['FY'], ii)
                        wF = sm_(st0['wF'], ii)
                    else:
                        FY = np.vstack((FY, sm_(st0['FY'], ii)))
                        wF = np.hstack((wF, sm_(st0['wF'], ii)))
                FF = blkdiag(FFi)
        pm, P = mdl(FF, FY, s_min)
        model0 = {'ivi': ivi,
                  'ivo': ivo
                 }
        st_ext = stmdl(FB='FS1', model=model0, rtp=rtp, FY=FY, P=P, wF=wF, n2=n2, n1=[], st0=st0)
        model = [htmdl('FS1', [], 'FS', n2, ivi, ivo, cnames, [], pm, st_ext['ovr'])]
    else:
        raise Exception('Initial model structure is not defined...')
    return model
###################################################################################
def fSelect(model, st0, met, cnames, s_min, SLE, crit_nbm, iterate):
    # if len(model) > 1 and len(model[-1]['st']['in']) == 0: return model, st0, par # las1
    if model[-1]['FB'] == 'BE':
        if iterate == 0: iterate = -1
        return model, iterate  # las1t step was BE

    # todo: calc model(end).st.out when BR is succesfull --> calc in bElimin.m
    # if length(model) > 1 && isempty(model(end).st_in),  model_new = model(end);  model = model(1:end - 1); # successful BE step
    # else,                                               model_new = [];
    # end
    Nw, r, z, FY, FF, wF, ivi, ivo, n1, n2 = parin(st0, model[-1])
    # ----- Calculate significance of not entered factors  -----
    if not len(ivo) == 0:
        n1 = ivi.shape[0]
        n2 = n1 + 1
        ivi0 = np.hstack((np.matlib.repmat(ivi, z - n1, 1), c_(ivo)))
        pm = nans((n2, r), len(ivo))
        st = []
        for i in np.arange(z - n2 + 1):
            ivi = ivi0[i, :]
            pmi, P = mdl(sm_(FF, ivi, ivi), sm_(FY, ivi), s_min)
            pm[:, :, i] = pmi
            st = st + [stmdl(FB='FS', model=model[-1], FY=sm_(FY, ivi), P=P, wF=sm_(wF, ivi), n2=n2, n1=n1, st0=st0)]
        st_out = [s['out'] for s in st]
        model[-1] = htmdl('FS2', model[-1], st=st_out)
        flg = 1
    else:
        # model[-1] = htmdl('FS2', model[-1])
        flg = 0
    # ----- Find next best model -----
    # todo: calc model(end).st_in when BR is succesfull --> calc in bElimin.m
    # if ~strcmp(met, 'FR') && ~isempty(model_new), model(end + 1) = model_new; return, end   # Successful BE step
    if flg:
        p_Fpi, pmi, sti, ind = nextmdl('FS2', model, st, pm, crit_nbm)
        if not len(p_Fpi) == 0 and p_Fpi <= SLE:
            ivi = ivi0[ind[0], :]
            ivo1 = ivo[ind[0]]
            ivo = np.delete(ivo, ind, 0)
            model = model + [htmdl('FS1', model[-1], 'FS', n2, ivi, ivo, cnames, ivo1, pmi, sti)]
        else:
            iterate = 0
    else:
        iterate = 0
    return model, iterate


###################################################################################
def htmdl(mode=None, model0=None, FB=None, n2=None, ivi=None, ivo=None, cnames=None, ind2=None, pm=None, st={}, rtp='PM'):
    model = copy.deepcopy(model0)
    if len(model) == 0: model = {}; model
    if not 'st' in model:  model['st'] = {}
    if not 'in' in model['st']:  model['st']['in'] = {}
    if not 'out' in model['st']: model['st']['out'] = {}
    if not 'ovr' in model['st']: model['st']['ovr'] = {}
    # Model history
    if mode == 'FS1' or mode == 'BE1':
        if rtp == 'PM':
            model['cname_i'] = m_(cnames)[ivi]
            model['cname_o'] = m_(cnames)[ivo]
        elif rtp == 'PV':
            z = 0
            model['cname_i'] = [np.nan]*st['r']
            for i in range(len(ivi)):
                ivi_i = ivi[i] + z
                z += len(ivi[i])
                model['cname_i'][i] = m_(cnames)[ivi_i]
            z = 0
            model['cname_o'] = [np.nan]*st['r']
            for i in range(len(ivo)):
                ivo_i = ivo[i] + z
                z += len(ivo[i])
                model['cname_o'][i] = m_(cnames)[ivo_i]
        model['FB'] = FB
        model['n'] = n2
        model['xio'] = m_(cnames)[ind2] # todo: make it an array 1 x r
        model['pm'] = pm
        model['m'] = st['m']
        model['r'] = st['r']
        model['na'] = st['na']
        model['nb'] = st['nb']
        model['nc'] = st['nc']
        model['pm0'] = st['pm0']
        model['rtp'] = rtp
        model['ivi'] = ivi
        model['ivo'] = ivo
        model['st']['in'] = {}
        model['st']['out'] = {}
        model['st']['ovr'] = st
    elif mode == 'FS2':
        model['st']['out'] = st
    elif mode == 'BE2':
        model['st']['in'] = st
    return model


###################################################################################
def mdl(FF=None, Fy=None, s_min=1e-12):
    if FF.size == 1:
        P = 1/FF
    else:
        rcM = 1/np.linalg.cond(FF)  # todo: create function in sf, calculating condition number
        if rcM < 1e-3:  P = nsinv(FF, s_min)
        else:           P = np.linalg.inv(FF)
    pm = P@Fy
    return pm, P


###################################################################################
def nextmdl(mode=None, model=None, st_ovr=None, pm=None, crit=None):
    if crit is None or 'p_Fp' not in crit: crit = {'p_Fp': 'max'}
    if len(model) > 1:  model1 = model[-2]
    else:               model1 = None
    model = model[-1]
    if mode == 'FS2':
        st = model['st']['out']
        n = len(st)
        # if crit['p_Fp'] == 'min':    Fp = c_([np.max(st[i]['Fp']) for i in np.arange(n)])
        # elif crit['p_Fp'] == 'max':  Fp = c_([np.min(st[i]['Fp']) for i in np.arange(n)])
        # elif crit['p_Fp'] == 'avg':  Fp = c_([np.mean(st[i]['Fp']) for i in np.arange(n)]) # todo: check all p_Fp[i] as mean(Fp) does not correspond to mean(p_Fp)
        if crit['p_Fp'] == 'min':    p_Fp = c_([np.min(st[i]['p_Fp']) for i in np.arange(n)])
        elif crit['p_Fp'] == 'max':  p_Fp = c_([np.max(st[i]['p_Fp']) for i in np.arange(n)])
        elif crit['p_Fp'] == 'avg':  p_Fp = c_([np.mean(st[i]['p_Fp']) for i in np.arange(n)])
        cnd = m_(True, (n, 1))
        if len(crit) > 0:
            r = model['st']['ovr']['r']
            if 'AIC' in crit and model1 is not None:
                aic = m_([st[i]['AIC'] for i in np.arange(n)])
                aic1 = model1['st']['ovr']['AIC']
                cnd1 = aic <= aic1
                cnd2 = np.isinf(aic) & (np.sign(aic) == -1)  # aic = -inf
                cnd = cnd & (cnd1 | cnd2)
                if crit['AIC'] == 'all': cnd = c_(np.all(cnd, axis=1))
                elif crit['AIC'] == 'avg': cnd = c_(np.round(np.mean(cnd, axis=1)))
                elif crit['AIC'] == 'any': cnd = c_(np.any(cnd, axis=1))

            if 'Cp' in crit and model1 is not None:
                cp = m_([st[i]['Cp'] for i in np.arange(n)])
                cnd1 = (cp > model1['n'] - 1) | (cp < 0)
                cnd2 = np.isnan(cp)
                cnd = cnd & (cnd1 | cnd2)
                if crit['Cp'] == 'all': cnd = c_(np.all(cnd, axis=1))
                elif crit['Cp'] == 'avg': cnd = c_(np.round(np.mean(cnd, axis=1)))
                elif crit['Cp'] == 'any': cnd = c_(np.any(cnd, axis=1))

        __, ind1 = sort(p_Fp.flatten(), 'asscend')
        ind = ind1[find(cnd[ind1].flatten(), 1, 'first')]
        if not len(ind) == 0:
            p_Fpi = p_Fp[ind[0]]
            pmi = pm[:, :, ind[0]]
            st_ovri = st_ovr[ind[0]]['ovr']
        else:
            p_Fpi = []
            pmi = []
            st_ovri = []
    else:
        if mode == 'BE2':
            n = len(model['st']['in'])
            p_Fp = m_([model['st']['in'][i]['p_Fp'] for i in np.arange(n)])
            if crit['p_Fp'] == 'min':    p_Fp = c_(np.min(p_Fp, axis=1))
            elif crit['p_Fp'] == 'max':  p_Fp = c_(np.max(p_Fp, axis=1))
            elif crit['p_Fp'] == 'avg':  p_Fp = c_(np.mean(p_Fp, axis=1))

            p_Fpi, ind = max1(p_Fp, naskip=True)
            pmi = pm[:, :, ind]
            st_ovri = st_ovr[ind]['ovr']
    return p_Fpi, pmi, st_ovri, ind


###################################################################################
def parin(st0, model):
    Nw = st0['Nw']
    r = st0['r']
    z = st0['z']
    FY = st0['FY']
    FF = st0['FF']
    wF = st0['wF']
    ivi = model['ivi']
    ivo = model['ivo']
    n1 = len(ivi) - 1
    n2 = n1 + 1
    return Nw, r, z, FY, FF, wF, ivi, ivo, n1, n2


###################################################################################
def stats(x=None, y=None, w=None, rtp='PM', m=None, r=None, na=None, nb=None, nc=None, pm0=None, ivi=None, s_min=1e-12):
    if r is None: r = y.shape[1]
    if rtp == 'PM':
        if m is None: m = []
        N, z = x.shape
        Nw = sum(w)[0]
        FF = x.T@(w*x)
        FY = x.T@(w*y)
        wF = w.T@x
        mF = x.T@w/Nw
        my = y.T@w/Nw
        YFPFY = FY.T@nsinv(FF, s_min)@FY
        SSY = y.T@(y*w)
        SST = (y - repmat(r_(my), N, 1)).T@((y - repmat(r_(my), N, 1))*w)
        SSE = SSY - YFPFY;
        SSE[SSE < 0] = 0

        ssy = np.diag(SSY)
        sst = np.diag(SST)
        mset = np.diag(SSE)/(N - z)
    elif rtp == 'PV':
        if m is None: m_flg=1; m = 0
        else: m_flg = 0
        if pm0 is None: pm0 = zeros(r, 1)
        if na is None: na = zeros(r, r)
        if nb is None: nb = zeros(r, m)
        if nc is None: nc = zeros(r, r)
        z = np.sum(np.hstack((pm0, na, nb, nc)), axis=1).astype(int)
        if m_flg: m = []
        cz = np.hstack((0, np.cumsum(z))).astype(int)
        if ivi is not None: zz = ivi
        N = y.shape[0]
        Nw = sum(w)
        wv = vec(repmat(w, 1, r).T)
        yv = vec(y.T)
        FF = x.T@(wv*x)
        FY = x.T@(wv*yv)
        wF = wv.T@x
        mF = x.T@wv/Nw
        my = y.T@w/Nw
        YFPFY = nans((r,))
        ssy = nans((r,))
        sst = nans((r,))
        for i in np.arange(r):
            i1, i2 = cz[i:i+2]
            yi = c_(y[:, i])
            FFi = FF[i1:i2, i1:i2]
            FYi = FY[i1:i2, :]
            YFPFY[i] = (FYi.T@nsinv(FFi, s_min)@FYi)[0, 0]
            ssy[i] = yi.T@(yi*w)
            sst[i] = ((yi - my[i]).T@((yi - my[i])*w))[0, 0]
        sse = ssy - YFPFY;  sse[sse < 0] = 0
        mset = sse/(N - z)

    st0 = {'N': N,
           'Nw': Nw,
           'z': z,
           'm': m,
           'r': r,
           'FF': FF,
           'FY': FY,
           'wF': wF,
           'mF': mF,
           'my': my,
           'ssy': ssy,
           'sst': sst,
           'mset': mset,
           'na': na,
           'nb': nb,
           'nc': nc,
           'pm0': pm0
           }
    return st0


###################################################################################
def stmdl(FB=None, model=None, rtp='PM', FY=None, P=None, wF=None, n2=np.nan, n1=np.nan, st0=None):
    r = st0['r']
    m = st0['m']
    na = st0['na']
    nb = st0['nb']
    nc = st0['nc']
    pm0 = st0['pm0']

    N = st0['N']
    Nw = st0['Nw']
    ssy = st0['ssy']
    sst = st0['sst']
    mset = st0['mset']
    my = m_(st0['my']).flatten()
    if model is not None and 'st' in model and 'ovr' in model['st']:
        ssm_1 = model['st']['ovr']['ssm']
        sse_1 = model['st']['ovr']['sse']
    if rtp == 'PM':
        YFPFY = FY.T@P@FY
        sse = (ssy - np.diag(YFPFY)).flatten();                     sse[sse < 0] = 0  # matlab syntaxis: sse = max([0, ssy - YFPFY])
        ssm = np.diag(YFPFY).flatten();                             ssm[ssm < 0] = 0
        ssr = np.diag(YFPFY + Nw*my**2 - 2*my*(wF@P@FY)).flatten(); ssr[ssr < 0] = 0
    elif rtp == 'PV':
        ivi = model['ivi']
        ivo = model['ivo']
        YFPFY = nans((r,))
        wFPFY = nans((r,))
        ni_1 = 0
        for i in np.arange(r):
            ni = len(ivi[i])
            ii += np.arange(ni_1, ni)
            ni_1 = ni
            if isinstance(ii, int):
                FYi = m_(FY[ii, :], 1, 1)
                wFi = m_(wF[:, ii], 1, 1)
                Pi = m_([P[ii][ii]], 1, 1) # Pi = P(ind(i), ind(i))
            else:
                FYi = FY[ii, :]
                wFi = wF[:, ii]
                Pi = P[ii][:, ii] # Pi = P(ind(i), ind(i))
            PiFYi = Pi@FYi
            YFPFY[i] = (FYi.T@PiFYi)[0, 0]
            wFPFY[i] = (wFi@PiFYi)[0, 0]
        sse = (ssy - YFPFY).flatten(); sse[sse < 0] = 0  # matlab syntaxis: sse = max([0, ssy - YFPFY])
        ssm = YFPFY.flatten();         ssm[ssm < 0] = 0
        ssr = (YFPFY + Nw*my**2 - 2*my*(wFPFY)).flatten();   ssr[ssr < 0] = 0

    v1o = n2
    v2 = N - n2
    Fo = ssr/sse*v2/v1o
    p_Fo = pvalF(Fo, v1o, v2, 'ot')
    mse = sse/(N - n2)
    ste = np.sqrt(c_(np.diag(P))*r_(mse))
    R2 = ssr/sst
    R2 = 1 - sse/sst
    R2adj = 1 - (1 - R2)*(Nw - 1)/(Nw - n2)
    vaf = R2adj*100;  vaf[vaf < 0] = 0
    cp = sse/mset + 2*n2 - N
    aic = np.log(sse) + 2/N*n2
    sc = np.log(sse) + np.log(N)/N*n2
    if model is not None and 'st' in model and 'ovr' in model['st'] and 'R2' in model['st']['ovr']:
        R2_1 = model['st']['ovr']['R2']
    # else:
    #     R2_1 = np.nan
    if FB == 'FS':
        R2prt = R2 - R2_1
        v1p = np.abs(n2 - n1)
        t2ss = np.array([np.max(np.hstack((0, (ssm - ssm_1).flatten())))])
        Fp = t2ss/sse*v2/v1p
        p_Fp = pvalF(Fp, v1p, v2, 'ot').flatten()
    elif FB == 'BE':
        R2prt = R2_1 - R2
        v1p = np.abs(n2 - n1)
        t2ss = np.array([np.max(np.hstack((0, (ssm_1 - ssm).flatten())))])
        Fp = t2ss/sse_1*v2/v1p
        p_Fp = pvalF(Fp, v1p, v2, 'ot').flatten()
    else:
        R2prt = None
        v1p = None
        t2ss = None
        Fp = None
        p_Fp = None

    st = {};
    st['ovr'] = {}
    st['ovr']['m'] = m
    st['ovr']['r'] = r

    st['ovr']['na'] = na
    st['ovr']['nb'] = nb
    st['ovr']['nc'] = nc
    st['ovr']['pm0'] = pm0
    st['ovr']['rtp'] = rtp
    st['ovr']['v1'] = n2
    st['ovr']['v2'] = v2
    st['ovr']['ssr'] = ssr
    st['ovr']['ssm'] = ssm
    st['ovr']['sse'] = sse
    st['ovr']['MSE'] = mse
    st['ovr']['STE'] = ste
    st['ovr']['R2'] = R2
    st['ovr']['R2adj'] = R2adj
    st['ovr']['VAF'] = vaf
    st['ovr']['BIC'] = sc
    st['ovr']['Fo'] = Fo
    st['ovr']['p_Fo'] = p_Fo
    st['ovr']['Cp'] = cp
    st['ovr']['AIC'] = aic

    if FB == 'FS':
        st['out'] = {}
        st['out']['v1p'] = v1p
        st['out']['t2ss'] = t2ss
        st['out']['Fp'] = Fp
        st['out']['p_Fp'] = p_Fp
        st['out']['R2prt'] = R2prt
        st['out']['Cp'] = cp
        st['out']['AIC'] = aic
    elif FB == 'BE':
        st['in'] = {}
        st['in']['t2ss'] = t2ss
        st['in']['Fp'] = Fp
        st['in']['p_Fp'] = p_Fp
        st['in']['v1p'] = v1p
        st['in']['R2prt'] = R2prt
        st['in']['Cp'] = cp
        st['in']['AIC'] = aic
    return st


###################################################################################
def swlinr(F=None, U=None, Y=None, W=None, na=None, nb=None, nc=None, pm0=None, cnames=None, mtp=None, rtp='PM', met='SWR', SLE=0.05, SLS=0.05, crit_nbm={'p_Fp':'max','AIC':'any','Cp':'any'}, crit_nbm_tp='min', mdl_init='empty', ivi=m_(tp=int), val_prc=0, s_min=1e-12, dsp=False):
    N, r = Y.shape
    if F is not None:
        if rtp == 'PV': raise Exception('In SWLINR(): Input parameter F is set only when the model is in the parameter-vector form (the parameter rtp = \'PV\').')
        m = None
    if cnames is None: cnames = ['var_' + str(i) for i in range(m)]
    if mdl_init == 'empty' and (isinstance(pm0, (np.ndarray, list)) and np.sum(pm0) < r or isinstance(pm0, (int, float)) and pm0 == 0):
        if pm0 is not None and np.sum(pm0) < r: wn.warn('In SWLINR(): Intercept(s) introduced in the model as the feature selection starts with "empty" initial model (the parameter mdl_init = \'empty\') that is equivalent to "intercept-only model".')
        pm0 = ones(r, 1)
        if F is not None:
            F = np.hstack((np.ones((N, 1)), F))
            cnames = ['intercept'] + cnames
            ivi = np.hstack((1, ivi + 1))

    if U is not None and mtp=='arx':
        n = np.max(np.hstack((na, nb)))
        if rtp == 'PM':     F = dmpm(U, Y, na=na, nb=nb, pm0=pm0)
        elif rtp == 'PV':   F = dmpv(U, Y, na=na, nb=nb, pm0=pm0)
        m = U.shape[1]
        Y = Y[n:, :]
        if F is not None: W = W[n:, :]

    st0 = stats(F, Y, W, rtp=rtp, m=m, r=r, na=na, nb=nb, nc=nc, pm0=pm0, s_min=s_min)

    model = firstmdl(st0, mdl_init, s_min, cnames, ivi, rtp)
    iterate = 1
    while iterate > 0:
        model, iterate = bElimin(model, st0, met, cnames, s_min, SLS, crit_nbm, iterate)
        model, iterate = fSelect(model, st0, met, cnames, s_min, SLE, crit_nbm, iterate)
        visualz(model, iterate, dsp, mdl_init)
    return model


###################################################################################
def visualz(model, iterate, dsp, mdl_init):
    if not dsp: return
    model0 = copy.deepcopy(model)
    i2 = iterate
    if i2 == -1:
        i1, i2 = 1, 0
    else:
        i1 = 0
    for step in np.arange(len(model0) - 2 + i1, len(model0) - i2):
        model = model0[step]
        print('Step: ', step, '  =================================================================================================================')
        if model['FB'] == 'FS' and step != 0:
            print('Added factor: ', model['xio'])
        elif model['FB'] == 'BE' and step != 0:
            print('Removed factor: ', model['xio'])
        elif mdl_init == 'init':
            print('Initial model: ', model['cname_i'].flatten())
        elif model['FB'] == 'FS' and step == 0:
            print('Initial model: intercept')
        elif model['FB'] == 'BE' and step == 0:
            print('Initial model: full')
        elif model['FB'] == 'BE' and step == 0:
            print('Initial model: full')

        if 'Fo' in model['st']['ovr'] and dsp == 'all' or dsp == 'ovr':
            print('--- Overall model measures ---')
            st = model['st']['ovr']
            df1 = np.full((1, 1), st['v1'])
            df2 = np.full((1, 1), st['v2'])
            #    SSR = st['ssr']
            #    SSM = st['ssm']
            SSE = st['sse']
            MSE = st['MSE']
            R2 = st['R2']
            R2a = st['R2adj']
            VAF = st['VAF']
            BIC = st['BIC']
            AIC = st['AIC']
            Cp = st['Cp']
            OverallF = st['Fo']
            pval_OverallF = st['p_Fo']
            print(pd.DataFrame({'df1': df1[0],
                                'df2': df2[0],
                                'OverallF': OverallF[0],
                                'pval_OverallF': pval_OverallF[0],
                                'SSE': SSE[0],
                                'MSE': MSE[0],
                                'R2': R2[0],
                                'R2adj': R2a[0],
                                'BIC': BIC[0],
                                'AIC': AIC[0],
                                'Cp': Cp[0]
                                }))
            print('------------------------------------------------------')
            print(' ')
        if 'st' in model and 'in' in model['st'] and dsp == 'all':
            print('--- Partial model measures ---')
            Variable = c_(model['cname_i'])
            Estimates = model['pm']
            st = model['st']['in']
            if st is not None:
                n = len(st)
                T2SS = nans((n, 1))
                PartialF = nans((n, 1))
                pval_PartialF = nans((n, 1))
                PartialR2 = nans((n, 1))
                for i in np.arange(n):
                    T2SS[i] = st[i]['t2ss']
                    PartialF[i] = st[i]['Fp']
                    pval_PartialF[i] = st[i]['p_Fp']
                    PartialR2[i] = st[i]['R2prt']
                SandardError = model['st']['ovr']['STE']
                if not len(PartialF) == 0 and PartialF.shape == Variable.shape:
                    print(pd.DataFrame({'Variable': Variable[:, 0],
                                        'Estimates': Estimates[:, 0],
                                        'SandardError': SandardError[:, 0],
                                        'T2SS': T2SS[:, 0],
                                        'PartialR2': PartialR2[:, 0],
                                        'PartialF': PartialF[:, 0],
                                        'pval_PartialF': pval_PartialF[:, 0]
                                        }))
                else:
                    print('    Empty set...')
            else:
                print('    Empty set...')
            print('------------------------------------------------------')
            print(' ')
        if 'st' in model and 'out' in model['st'] and dsp == 'all':
            print('--- Measures of eligible to enter variables ---')
            Variable = c_(model['cname_o'])
            st = model['st']['out']
            n = len(st)
            T2SS = nans((n, 1))
            PartialF = nans((n, 1))
            pval_PartialF = nans((n, 1))
            PartialR2 = nans((n, 1))
            for i in np.arange(n):
                T2SS[i] = st[i]['t2ss']
                PartialF[i] = st[i]['Fp']
                pval_PartialF[i] = st[i]['p_Fp']
                PartialR2[i] = st[i]['R2prt']
            if not len(PartialF) == 0 and len(PartialF) == len(Variable):
                print(pd.DataFrame({'Variable': Variable[:, 0],
                                    'T2SS': T2SS[:, 0],
                                    'PartialR2': PartialR2[:, 0],
                                    'PartialF': PartialF[:, 0],
                                    'pval_PartialF': pval_PartialF[:, 0]
                                    }))
            else:
                print('    Empty set...')
            print('------------------------------------------------------')
            print(' ')
            ###################################################################################
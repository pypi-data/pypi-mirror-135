import numpy as np
import pandas as pd
from op_nlopt.ord12 import *
from op_nlopt.cstm import *
from gnrl.sf import *
from gnrl.measr import *

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


###################################################################################
def add_model(model, model_1, FB):
    if FB == 'FS':
        AIC = model['ovr']['AIC']
        BIC = model['ovr']['BIC']
    else:
        AIC = model['st']['ovr']['AIC']
        BIC = model['st']['ovr']['BIC']
    AIC_1 = model_1['st']['ovr']['AIC']
    BIC_1 = model_1['st']['ovr']['BIC']
    if AIC > AIC_1: better = 0
    else:           better = 1
    if BIC > BIC_1: better = 0
    else:           better = 1

    return better
###################################################################################
def bElimin(model, step, x, y, w, met, SLS, pm0, st0, cnames, metpminit, met_opt, maxiter, fcnv, afcnv, xcnv, gcnv, dsp,
            iterate, sc, dsp_op, smeth, su, p_decr, p_incr, smin):
    # Backward Elimination Step
    if met == 'FR': return model, step, st0
    Nw, z, ivi, ivo, n1, n2 = parin(st0, model[-1])
    ivi0 = ivi
    if met == 'FR': return model, step, st0
    # ----- Find next best model -----
    if ivi.shape[0] > 1:
        p_Fpi, ind = nextmdl('BE2', model[-1])

        #    if length(model) == 6,  # simulate insignificant factor
        #       p_Fpi = 0.4; ind = 3;
        #    end

        if p_Fpi > SLS:
            ivi = ivi0[np.hstack((np.arange(0, ind), np.arange(ind + 1, len(ivi))))]
            ivo = np.hstack((ivo, ivi0[ind]))
            model1 = mdl(x[:, ivi], y, w, ivi, n2 - 1, st0, pm0, cnames, metpminit, met_opt, maxiter, fcnv, afcnv, xcnv,
                         gcnv, sc, dsp_op, smeth, su, p_decr, p_incr)
            ym = lgr_apl(x[:, ivi], model1['pm'])
            st_ext = stmdl('FS1', x, y, ym, w, st0, model1, n2 - 1, ivi, ivo, smin)

            better_mdl = add_model(model1, model[-1], 'BE')
            if better_mdl:
                model = model + [htmdl('BE1', [], 'BE', n2 - 1, ivi, ivo, cnames, ivi0[ind], model1['pm'], st_ext)]
                visualz(model, iterate, dsp)
                for i in np.arange(0, len(model) - 1):
                    if len(model[i]['ivi']) == len(model[-1]['ivi']) and all(
                        model[i]['ivi'] == model[-1]['ivi']): iterate = 0
                step = 'BE'
            else:
                if met == 'BR' or step == 'FS_STOP': iterate = 0
                step = 'BE_STOP'
        else:
            if met == 'BR' or step == 'FS_STOP': iterate = 0
            step = 'BE_STOP'
    else:
        if met == 'BR' or step == 'FS_STOP': iterate = 0
        step = 'BE_STOP'

    return model, step, st0, iterate


###################################################################################
def firstmdl(x, y, w, cnames, st0, smin, mdl_init, ivi, pm0, metpminit, met_opt, maxiter, fcnv, afcnv, xcnv, gcnv, sc,
             dsp_op, smeth, su, p_decr, p_incr):
    if mdl_init == 'full':
        z = st0['z']
        ivi = np.arange(z)
        ivo = np.array([]).astype(int)
        n2 = ivi.shape[0]
        model = mdl(x, y, w, ivi, n2, st0, pm0, cnames, metpminit, met_opt, maxiter, fcnv, afcnv, xcnv, gcnv, sc,
                    dsp_op, smeth, su, p_decr, p_incr)
        ym = lgr_apl(x, model)
        st_ext = stmdl('BE1', x, y, ym, w, st0, model, n2, ivi, ivo, smin)
        model = [htmdl('BE1', [], 'BE', n2, ivi, ivo, cnames, [], model['pm'], st_ext)]
    else:
        if mdl_init == 'empty':
            z = st0['z']
            ivi = np.array([0])
            ivo = np.arange(1, z)
            n2 = ivi.shape[0]
            modelInt = {}
            modelInt['st'] = st0['modelInt']
            modelInt['pm'] = st0['modelInt']['pm']
            st_ext = stmdl('FS1', x, y, st0['modelInt']['ovr']['ym0'], w, st0, modelInt, n2, ivi, ivo, smin);
            pm = st0['modelInt']['pm']
            model = [htmdl('FS1', [], 'FS', n2, ivi, ivo, cnames, [], pm, st_ext)]
        else:
            if mdl_init == 'init':
                z = st0['z']
                ivo = np.setxor1d(c_(np.arange(z)), ivi)
                n2 = ivi.shape[0]
                model = mdl(x[:, ivi], y, w, ivi, n2, st0, pm0, cnames, metpminit, met_opt, maxiter, fcnv, afcnv, xcnv,
                            gcnv, sc, dsp_op, smeth, su, p_decr, p_incr)
                ym = lgr_apl(x[:, ivi], model)
                st_ext = stmdl('BE1', x, y, ym, w, st0, model, n2, ivi, ivo, smin)
                model = [htmdl('BE1', [], 'BE', n2, ivi, ivo, cnames, [], model['pm'], st_ext)]
            else:
                raise Exception('First model type is not defined...')

    step = 'START'
    return model, step, st0


###################################################################################
def fSelect(model, step, x, y, w, met, SLE, pm0, st0, cnames, metpminit, met_opt, maxiter, fcnv, afcnv, xcnv, gcnv, dsp,
            iterate, sc, dsp_op, smeth, su, p_decr, p_incr, smin):
    # Forward Selection Step
    if met == 'BR' or step == 'BE': return model, step, st0, iterate
    Nw, z, ivi, ivo, n1, n2 = parin(st0, model[-1])
    # ----- Find next best model -----
    if not len(ivo) == 0:
        minPvalSne, ind = nextmdl('FS2', model[-1])
        if minPvalSne <= SLE:
            ivi0 = np.hstack((np.matlib.repmat(ivi, z - n2, 1), c_(ivo)))
            ivi = ivi0[ind, :]
            ivo = np.delete(ivo, ind)
            model1 = mdl(x[:, ivi], y, w, ivi, n2 + 1, st0, pm0, cnames, metpminit, met_opt, maxiter, fcnv, afcnv, xcnv,
                         gcnv, sc, dsp_op, smeth, su, p_decr, p_incr)
            ym = lgr_apl(x[:, ivi], model1['pm'])
            st_ext = stmdl('FS1', x, y, ym, w, st0, model1, n2 + 1, ivi, ivo, smin)

            better_mdl = add_model(st_ext, model[-1], 'FS')
            if better_mdl:
                model = model + [htmdl('FS1', [], 'FS', n2 + 1, ivi, ivo, cnames, ivi[-1], model1['pm'], st_ext)]
                visualz(model, iterate, dsp)
                for i in np.arange(0, len(model) - 1):
                    if len(model[i]['ivi']) == len(model[-1]['ivi']) and all(
                        model[i]['ivi'] == model[-1]['ivi']): iterate = 0
                step = 'FS'
            else:
                if met == 'FR' or step == 'BE_STOP': iterate = 0
                step = 'FS_STOP'
        else:
            if met == 'FR' or step == 'BE_STOP': iterate = 0
            step = 'FS_STOP'
    else:
        if met == 'FR' or step == 'BE_STOP': iterate = 0
        step = 'FS_STOP'

    return model, step, st0, iterate


###################################################################################
def htmdl(mode, model, FB, n2, ivi, ivo, cnames, ind2, pm, st):
    if len(model) == 0: model = {}; model
    if not 'st' in model:  model['st'] = {}
    if not 'in' in model['st']:  model['st']['in'] = {}
    if not 'out' in model['st']: model['st']['out'] = {}
    if not 'ovr' in model['st']: model['st']['ovr'] = {}
    # Model history
    if mode == 'FS1' or mode == 'BE1':
        if ivi.shape[0] == 0:
            model['cname_i'] = c_(np.array(['']))
        else:
            model['cname_i'] = np.array(cnames)[ivi]
        if ivo.shape[0] == 0:
            model['cname_o'] = c_(np.array(['']))
        else:
            model['cname_o'] = np.array(cnames)[ivo]
        model['FB'] = FB
        model['n'] = n2
        model['xio'] = np.array(cnames)[ind2]
        model['pm'] = pm
        model['ivi'] = ivi
        model['ivo'] = ivo
        model['st']['in'] = st['in']
        model['st']['out'] = st['out']
        model['st']['ovr'] = st['ovr']
    elif mode == 'FS2':
        model['st']['out'] = st
    elif mode == 'BE2':
        model['st']['in'] = st

    return model


###################################################################################
def mdl(x, y, w, ivi, n2, st0, pm0, cnames, metpminit, meth, maxiter, fcnv, afcnv, xcnv, gcnv, sc, dsp_op, smeth, su,
        p_decr, p_incr):
    # Initial model parameters
    lambda_ = st0['modelInt']['pm']
    if metpminit == 'zero':
        pm = np.vstack((c_([lambda_]), np.zeros((n2 - 1, 1))))
    elif metpminit == 'prev':
        pm = pm0
    elif metpminit == 'fapp':
        model0 = lspm(x, (y - 0.5)*2*lambda_)
        pm = model0['Pm']
    # Arguments for func, grad, hes calculation
    if len(x.shape) == 1: x = c_(x)
    args = {}
    args['data'] = np.hstack((x, y, w, np.zeros((st0['N'], 1))))
    if np.size(ivi) == 1:
        args['cnames'] = c_(np.array([cnames[ivi]]))
    else:
        args['cnames'] = c_(np.array(cnames)[ivi])
    args['x'] = pm
    args['ivi'] = ivi
    args['pm0'] = pm0
    args['cnames'] = cnames
    args['metpminit'] = metpminit
    #    func = par['func
    #    grad = par['grad
    #    hes = par['hes
    func = 1
    grad = 1
    hes = 1
    pm, F, g, H, Hinv, __ = newton(pm, f_lgr, g_lgr, h_lgr, args, meth, maxiter, fcnv, afcnv, xcnv, gcnv, sc, dsp_op, smeth, su, p_incr, p_decr)
    # # Denormalization
    # pm = denormPar(dset, pmn);

    model = {'pm': pm,
             'st': {'ovr': {'F': F,
                            'g': g,
                            'H': H,
                            'Hinv': Hinv}
                    }
             }
    return model


###################################################################################
def nextmdl(mode, model):
    #    model = model[-1]
    if mode == 'FS2':
        pvalSne = model['st']['out']['p_valSne']
        minPvalSne, ind = min1(pvalSne, naskip=True)
    else:
        if mode == 'BE2':
            p_valW = model['st']['in']['p_valW']
            # p_valW[0] = 0 # !!!!!!!!!!!!!!!!!!!
            minPvalSne, ind = max1(p_valW)
    return minPvalSne, ind


###################################################################################
def parin(st0, model):
    Nw = st0['Nw']
    z = st0['z']
    ivi = model['ivi']
    ivo = model['ivo']
    n1 = len(ivi) - 1
    n2 = n1 + 1;
    return Nw, z, ivi, ivo, n1, n2


###################################################################################
def scrChiSq(x, y, ym0, ym, w, st0, model, mode, ivi, ivo, smin):
    # Score Chi-Square statistics for group-wise selection/elimination
    # --------------------------
    # Author: Alexander Efremov
    # Date:   20.12.2009
    # --------------------------
    z = st0['z']
    n1 = len(ivi)
    g = model['st']['ovr']['g']
    Hinv = model['st']['ovr']['Hinv']
    n = x.shape[1]
    if mode == 'resid':
        Fish = (x*ym*(1 - ym)*w).T @ x
        g = x.T @ ((y - ym)*w)
        invFish = nsinv(Fish, smin)
        S = g.T @ invFish @ g
    elif mode == 'globNul':
        ni = len(ivi)
        xin = x[:, ivi]
        F11 = (xin*ym0*(1 - ym0)*w).T @ xin
        g11 = xin.T @ ((y - ym0)*w)
        S = g11.T @ nsinv(F11, smin) @ g11
    elif mode == 'freg':
        nci = ivi.shape[0]
        nco = ivo.shape[0]
        if nci == 0:
            S = np.nan
            return S
        gin = g
        if nco == 0:
            S = c_(np.array([]))
            return S
        S = nans((nco, 1))
        fi = np.hstack((np.matlib.repmat(ivi, z - n1, 1), c_(ivo)))
        for i in np.arange(0, nco):
            xout = x[:, int(ivo[i])]
            if not any(xout - xout[0]):
                S[i, 0] = 0
                continue
            gout = -xout.T @ ((y - ym)*w)

            Hi = (x[:, fi[i, :]]*ym*(1 - ym)*w).T @ x[:, fi[i, :]]
            g = np.vstack((gin, gout))

            # args = {'data': np.hstack((x[:, fi[i, :]], y, w, ym))}
            # g = g_lgr(args)
            # Hi = h_lgr(args)
            rcHi = 1/np.linalg.cond(Hi)
            if rcHi < np.inf: # 1e-6:
                S[i, 0] = (g.T@(nsinv(Hi, smin))@g)[0, 0]
            else:
                pass
                # S[i, 0] = (g.T@(inv2(Hi, Hinv, smin))@g)[0, 0]
        S[S < 0] = 0
    return S


###################################################################################
def swlogr(x, y, w, cnames=None, SLE=0.05, SLS=0.05, pm0=1, dsp=False, nbm_crit=np.array([]), mdl_init='empty', met='SWR',
           metpminit='zero', ivi=np.empty([1, ]).astype(int), met_opt='newt', gcnv=1e-8, fcnv=0, afcnv=0, xcnv=0,
           maxiter=100, smin=1e-12, dsp_op=np.array([1, 2]), smeth='fprev2', p_incr=1.2, p_decr=0.6, sl=1e-12, su=1,
           sc=None):
    N = x.shape[0]
    if cnames is None: cnames = ['var_' + str(i) for i in range(m)]
    if pm0 == 1:
        x = np.hstack((np.ones((N, 1)), x))
        cnames = ['intercept'] + cnames
        ivi = np.hstack((1, ivi + 1))
    iterate = 1
    st0 = stats(x, y, w, smin, pm0, cnames, metpminit, ivi, met_opt, maxiter, fcnv, afcnv, xcnv, gcnv, sc, dsp_op, dsp, smeth, su, p_decr, p_incr)
    model, step, st0 = firstmdl(x, y, w, cnames, st0, smin, mdl_init, ivi, pm0, metpminit, met_opt, maxiter, fcnv, afcnv, xcnv, gcnv, sc, dsp_op, smeth, su, p_decr, p_incr)
    while iterate:
        model, step, st0, iterate = bElimin(model, step, x, y, w, met, SLS, pm0, st0, cnames, metpminit, met_opt,
                                            maxiter, fcnv, afcnv, xcnv, gcnv, dsp, iterate, sc, dsp_op, smeth, su,
                                            p_decr, p_incr, smin)
        model, step, st0, iterate = fSelect(model, step, x, y, w, met, SLE, pm0, st0, cnames, metpminit, met_opt,
                                            maxiter, fcnv, afcnv, xcnv, gcnv, dsp, iterate, sc, dsp_op, smeth, su,
                                            p_decr, p_incr, smin)
    return model


###################################################################################
def stats(x, y, w, smin, pm0, cnames, metpminit, ivi, met_opt, maxiter, fcnv, afcnv, xcnv, gcnv, sc, dsp_op, dsp, smeth,
          su, p_decr, p_incr):
    N, z = x.shape
    Nw = sum(w)
    my = y.T @ w/Nw
    st0 = {'N': N,
           'Nw': Nw,
           'z': z,
           'my': my,
           'modelInt': {'pm': np.log(my/(1 - my))}}
    modelInt = mdl(x[:, 0], y, w, 0, 1, st0, pm0, cnames, metpminit, met_opt, maxiter, fcnv, afcnv, xcnv, gcnv, sc,
                   dsp_op, smeth, su, p_decr, p_incr)
    modelInt['FB'] = 'FS'
    modelInt['xio'] = 'intercept'
    modelInt['cname_i'] = c_(np.array(['intercept']))
    modelInt['cname_o'] = c_(np.array(cnames[1:z]))
    ym0 = lgr_apl(x[0, 0], modelInt['pm'])

    st0['modelInt']['ovr'] = modelInt['st']['ovr']
    st0['modelInt']['ovr']['ym0'] = ym0
    st0['modelInt']['pm'] = modelInt['pm']
    st_ext = stmdl('BE1', x, y, ym0, w, st0, modelInt, 1, 0, c_(np.arange(1, z)), smin)
    st0['modelInt'] = st_ext
    st0['modelInt']['ovr']['ym0'] = ym0
    st0['modelInt']['pm'] = modelInt['pm']
    modelInt['st'] = st_ext
    visualz([modelInt], 1, dsp)
    return st0


###################################################################################
def stmdl(FB, x, y, ym, w, st0, model, n2, ivi, ivo, smin):
    import warnings
    warnings.filterwarnings("ignore", category=RuntimeWarning)

    N = st0['N']
    Nw = st0['Nw']
    z = st0['z']
    if not isinstance(ivi, np.ndarray): ivi = np.array([ivi])

    ym0 = np.matlib.repmat(st0['modelInt']['ovr']['ym0'], N, 1)
    if len(ym) == 1: ym = np.matlib.repmat(ym, N, 1)
    ivi0 = np.hstack((np.matlib.repmat(ivi, z - n2, 1), c_(ivo)))
    L0 = -st0['modelInt']['ovr']['F']
    L = - model['st']['ovr']['F']
    Hinv = model['st']['ovr']['Hinv']
    pm = model['pm']
    n = n2

    # Overall Stats & Model Measures /AIC, SC, Rg2, Rg2n, Rg2adj/
    st = {};
    st['ovr'] = {};
    st['in'] = {};
    st['out'] = {};
    st['globNul'] = {}
    st['ovr']['N'] = N
    st['ovr']['Nw'] = Nw
    st['ovr']['F'] = model['st']['ovr']['F']
    st['ovr']['g'] = model['st']['ovr']['g']
    st['ovr']['H'] = model['st']['ovr']['H']
    st['ovr']['Hinv'] = model['st']['ovr']['Hinv']
    st['ovr']['AIC'] = - 2*L + 2*n
    st['ovr']['BIC'] = - 2*L + (n + 0)*np.log(N)
    st['ovr']['Rg2'] = 1 - np.exp(2*(L0 - L)/(N - 1))
    st['ovr']['Rg2n'] = 1 - np.exp(2*(L0 - L)/(Nw - 1))
    st['ovr']['Rg2adj'] = st['ovr']['Rg2']/(1 - np.exp(2*L0/(N - 1)))
    st['ovr']['Rg2adjn'] = st['ovr']['Rg2n']/(1 - np.exp(2*L0/(Nw - 1)))
    st['ovr']['VAF'] = vaf(y, ym, w, p=len(model['pm']))

    # Individual Estimate Measures /stdpe, W, Psi, PsiL, PsiU/
    FishInv = Hinv
    stde = c_(np.sqrt(np.diag(FishInv)))
    st['in']['W'] = (pm/stde) ** 2
    v = np.ones(st['in']['W'].shape)
    st['in']['p_valW'] = gamq(v/2, st['in']['W'][:, 0]/2)
    st['in']['Psi'] = np.exp(pm)
    st['in']['PsiL'] = np.exp(pm - 1.96*stde)
    st['in']['PsiU'] = np.exp(pm + 1.96*stde)

    st['in']['stdpe'] = stde
    if n > 0 and FB != 'full' or FB != 'BR':
        # - Residual Score Chi-Square Test
        st['ovr']['Sr'] = scrChiSq(x, y, ym0, ym, w, st0, model, 'resid', ivi, ivo, smin)
        v = np.array([x.shape[1] - n])
        st['ovr']['p_valSr'] = gamq(v/2, st['ovr']['Sr']/2)
        st['ovr']['dfSr'] = v
        # - Chi-Square Score for not entered factors
        st['out']['Sne'] = scrChiSq(x, y, ym0, ym, w, st0, model, 'freg', ivi, ivo, smin)
        v = np.matlib.repmat(ivi0.shape[1], len(ivo), 1)
        st['out']['p_valSne'] = gamq(v/2, st['out']['Sne']/2)
        # Global Null Hypothesis Test: BETA=0
        v = n - 1
        # - LogLikelihood Ratio
        L = - model['st']['ovr']['F']
        L0 = - st0['modelInt']['ovr']['F']
        st['ovr']['globNul'] = {'LR': 2*(L - L0)}
        st['ovr']['globNul']['p_valLR'] = gamq(v/2, st['ovr']['globNul']['LR']/2)
        st['ovr']['globNul']['dfLR'] = v
        # - Score
        st['ovr']['globNul']['S0'] = scrChiSq(x, y, ym0, ym, w, st0, model, 'globNul', ivi, ivo, smin)
        v = n*np.ones(st['ovr']['globNul']['S0'].shape) - 1
        st['ovr']['globNul']['p_valS0'] = gamq(v/2, st['ovr']['globNul']['S0']/2)
        st['ovr']['globNul']['dfS0'] = v
        # - Wald
        pm0 = np.vstack((st0['modelInt']['pm'], np.zeros((n - 1, 1))))
        pm = model['pm']
        dp = pm - pm0
        xin = x[:, ivi]
        F1 = (xin*ym*(1 - ym)*w).T @ xin
        Finv1 = nsinv(F1, smin)
        if n > 1:
            stdpe = c_(np.sqrt(np.diag(Finv1)))
            st['ovr']['globNul']['W0'] = sum((dp[1:, :]/stdpe[1:, :]) ** 2)
            v = n*np.ones(st['ovr']['globNul']['W0'].shape) - 1
            st['ovr']['globNul']['p_valW0'] = gamq(v/2, st['ovr']['globNul']['W0']/2)
            st['ovr']['globNul']['dfW0'] = v
    else:
        st['Sr'] = NaN
        st['p_valSr'] = NaN
        st['Sne'] = nans((len(model['ifo']), 1))
        st['p_valSne'] = nans((len(model['ifo']), 1))
        st['globNul']['LR'] = NaN
        st['globNul']['p_valLR'] = NaN
        st['globNul']['S0'] = NaN
        st['globNul']['p_valS0'] = NaN
        st['ovr']['globNul']['W0'] = NaN
        st['ovr']['globNul']['p_valW0'] = NaN
        st['ovr']['globNul']['df'] = NaN

    # # Measures of Association
    # st = assoc(model, st, y, ym);
    # # Variance Inflation Factor
    # st.in.VIF = vif(x(:, ivi));
    return st


###################################################################################
def visualz(model, iterate, dsp):
    if not dsp: return
    step = len(model) - iterate
    print('Step: ', step, '  =================================================================================================================')
    modelInt = model[0]
    model = model[-1]
    FB = model['FB']
    if FB == 'FS' and step != 0:
        print('Added factor: ', model['xio'])
    elif FB == 'BE' and step != 0:
        print('Removed factor: ', model['xio'])
    elif FB == 'FS' and step == 0:
        print('Initial model: intercept')
    elif FB == 'BE' and step == 0:
        print('Initial model: full')

    pm = model['pm']
    n = len(pm)
    if dsp == 'all':
        if n > 1:
            print('--- Overall model fit measures ---')
            Rg2 = model['st']['ovr']['Rg2n']
            MaxRescRg2 = model['st']['ovr']['Rg2adjn']
            VAF = model['st']['ovr']['VAF']
            AIC_Intercept = modelInt['st']['ovr']['AIC']
            BIC_Intercept = modelInt['st']['ovr']['BIC']
            BIC_Current = model['st']['ovr']['BIC']
            AIC_Current = model['st']['ovr']['AIC']
            L = model['st']['ovr']['F']
            L0 = modelInt['st']['ovr']['F']
            Neg2LogL_Intercept = - 2*L0
            Neg2LogL_Current = - 2*L
            print(pd.DataFrame({'Rg2': Rg2.flatten(),
                                'MaxRescRg2': MaxRescRg2.flatten(),
                                'VAF': VAF.flatten(),
                                'BIC_Intercept': BIC_Intercept.flatten(),
                                'BIC_Current': BIC_Current.flatten(),
                                'AIC_Intercept': AIC_Intercept.flatten(),
                                'AIC_Current': AIC_Current.flatten(),
                                'Neg2LogL_Intercept': Neg2LogL_Intercept.flatten(),
                                'Neg2LogL_Current': Neg2LogL_Current.flatten()
                                }))
            print('------------------------------------------------------')
            print(' ')
        print(np.array(['--- Analysis of Maximum Likelihood Estimates & Odds Ratio Estimates ---']))
        No = np.arange(1, n + 1) - 1
        Variable = model['cname_i'].flatten()
        DF = np.ones(pm.shape[0])
        Estimate = pm[:, 0]
        StandardError = model['st']['in']['stdpe'][:, 0]
        WaldChiSquare = model['st']['in']['W'][:, 0]
        PrWaldChiSquare = model['st']['in']['p_valW'][:, 0]
        #    VIF = model.st.in.VIF;
        OddsRatio = model['st']['in']['Psi'][:, 0]
        Lower95Prc = model['st']['in']['PsiL'][:, 0]
        Upper95Prc = model['st']['in']['PsiU'][:, 0]
        #    disp(table(No, Variable, DF, Estimate, StandardError, VIF, WaldChiSquare, PrWaldChiSquare, OddsRatio, Lower95Prc, Upper95Prc))
        print(pd.DataFrame({'No': No,
                            'Variable': Variable,
                            'DF': DF,
                            'Estimate': Estimate,
                            'StandardError': StandardError,
                            'WaldChiSquare': WaldChiSquare,
                            'PrWaldChiSquare': PrWaldChiSquare,
                            'OddsRatio': OddsRatio,
                            'Lower95Prc': Lower95Prc,
                            'Upper95Prc': Upper95Prc
                            }))
        print('------------------------------------------------------')
        print(' ')
        if n > 1:
            print(np.array(['--- Global Null Hypothesis Test: BETA=0 ---']))
            if (step > 0 and str(dsp) == str('all')) or str(FB) == str('BR'):
                if len(model['ivi']) > 1:
                    LR = model['st']['ovr']['globNul']['LR']
                    p_valLR = model['st']['ovr']['globNul']['p_valLR']
                    S0 = model['st']['ovr']['globNul']['S0']
                    p_valS0 = model['st']['ovr']['globNul']['p_valS0']
                    W0 = model['st']['ovr']['globNul']['W0']
                    p_valW0 = model['st']['ovr']['globNul']['p_valW0']
                    dfLR = model['st']['ovr']['globNul']['dfLR']
                    dfS0 = model['st']['ovr']['globNul']['dfS0']
                    dfW0 = model['st']['ovr']['globNul']['dfW0']
                else:
                    LR = NaN
                    p_valLR = NaN
                    S0 = NaN
                    p_valS0 = NaN
                    W0 = NaN
                    p_valW0 = NaN
                    dfLR = NaN
                    dfS0 = NaN
                    dfW0 = NaN
            Test = np.transpose(np.array(['Likelihood Ratio', 'Score', 'Wald']))
            Chi_Sq = np.hstack([LR.flatten(), S0.flatten(), W0[-1]])
            DF = np.hstack([dfLR, dfS0.flatten(), dfW0[-1]])
            pval = np.hstack([p_valLR.flatten(), p_valS0.flatten(), p_valW0[-1]])
            print(pd.DataFrame({'Test': Test,
                                'Chi_Sq': Chi_Sq,
                                'DF': DF,
                                'pval': pval
                                }))
            print('------------------------------------------------------')
            print('\n')
        print(np.array(['--- Residual Chi-Square Test ---']))
        ChiSq = model['st']['ovr']['Sr'][:, 0]
        DF = model['st']['ovr']['dfSr']
        p_valChiSq = model['st']['ovr']['p_valSr'][:, 0]
        print(pd.DataFrame({
            'ChiSq': ChiSq,
            'DF': DF,
            'p_valChiSq': p_valChiSq
        }))
        print('------------------------------------------------------')
        print(' ')

    if 'in' in model['st'] and dsp == 'all':
        if n > 1:
            #       disp(['---------- Association of Prediction and Observed Response ----'])
            #       Pc = model['st['ovr.assoc.Pc;
            #       Pd = model['st['ovr.assoc.Pd;
            #       Pt = model['st['ovr.assoc.Pt;
            #       Nt = model['st['ovr.assoc.Nt;
            #       SomersD = model['st['ovr.assoc.SomersD;
            #       gamma = model['st['ovr.assoc.gamma;
            #       tau_a = model['st['ovr.assoc.tau_a;
            #       c = model['st['ovr.assoc.c;
            #       RankCorStats = {'PrcConcordant', 'PrcDiscordant', 'PrcTied', 'Pairs', 'Somers'' D', 'Gamma', 'Tau_a', 'c'}';
            #       Values = [Pc Pd, Pt, Nt, SomersD, gamma, tau_a, c]';
            #       disp(table(RankCorStats, Values))
            #       disp(['------------------------------------------------------'])
            #       disp([' ']')
            pass

    if n > 1:
        print(np.array(['--- Factors Eligible for Removal ---']))
        No = np.arange(2, n + 1) - 1
        Variable = model['cname_i'][1:]
        W = model['st']['in']['W'][:, 0]
        p_valW = model['st']['in']['p_valW'][:, 0]
        DF = np.ones((W.shape[1 - 1] - 1,))
        WaldChiSquare = W[1:]
        PrWaldChiSquare = p_valW[1:]
        print(pd.DataFrame({'No': No,
                            'Variable': Variable,
                            'DF': DF,
                            'WaldChiSquare': WaldChiSquare,
                            'PrWaldChiSquare': PrWaldChiSquare
                            }))
        print('------------------------------------------------------')
        print(' ')
        if not FB == 'BE':
            print('No factors are removed in Step', step)
            print(' ')

    if 'out' in model['st'] and dsp == 'all':
        print('---Factors Eligible for Entry ---')
        ScoreChiSq = model['st']['out']['Sne'][:, 0]
        p_valScoreChiSq = model['st']['out']['p_valSne'][:, 0]
        No = np.arange(1, len(ScoreChiSq) + 1)
        DF = np.ones((ScoreChiSq.shape[0],))
        Variable = model['cname_o'].flatten()
        if len(ScoreChiSq) > 0:
            print(pd.DataFrame({'No': No,
                                'Variable': Variable,
                                'DF': DF,
                                'ScoreChiSq': ScoreChiSq,
                                'p_valScoreChiSq': p_valScoreChiSq
                                }))
        else:
            print('No factors are eligible for entry...')
        print('------------------------------------------------------')
        print(' ')

    # if dsp == 'all': toc2()

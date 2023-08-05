import numpy as np
# import numpy.matlib
from aislab.gnrl.sf import *

###################################################################################
def dspl(flg, **kwargs):
    if flg == 2:
        ivi = kwargs['args']['ivi']
        x = kwargs['x']
        F = kwargs['F']
        itr = kwargs['itr']
        cnames = c_(kwargs['args']['cnames'])

        s = kwargs['s']
        spc = '   '
        if itr == 0:
            print('---------- Newton-Raphson Method Log ------------')
            print('[Iter][  Step  ][Objective Function]', cnames[:, 0])
            print(itr, 'initial', s, F, x.T)
        else:
            meth = kwargs['meth']
            print(itr, meth, s, F, x.T)
    elif flg == 1:
            x = kwargs['x']
            xx = kwargs['xx']
            F = kwargs['F']
            FF = kwargs['FF']
            g = kwargs['g']
            H = kwargs['H']
            Hinv = kwargs['Hinv']
            itr = kwargs['itr']
            msg = kwargs['msg']
            print(' ')
            if not len(FF) == 0:
                print('Last Change of F: ', (F - FF[0])[0])
            print('Last Gradient')
            print(g)
            if 'A' == msg:
                print('Convergence criterion (FCONV = ', kwargs['fcnv'], ') satisfied. /Initial model/')
            elif 'B' == msg:
                print('Stopping Rule (MaxIter = ', kwargs['maxiter'], ') satisfied. /', itr, '/')
            elif 'C' == msg:
                print('Convergence criterion (FCONV = ', kwargs['fcnv'], ') satisfied. /', np.abs(F - FF[0])/np.max(np.abs(FF[0]), initial=1e-6), '/')
            elif 'D' == msg:
                print('Convergence criterion (ABSFCONV = ', kwargs['afcnv'], ') satisfied. /', np.abs(F - FF[0]), '/')
            elif 'E' == msg:
                print('Convergence criterion (XCONV = ', kwargs['xcnv'], ') satisfied. /', (x - xx[:, 0]).T/x, '/')
            elif 'F' == msg:
                print('Convergence criterion (GCONV = ', kwargs['gcnv'], ') satisfied. /', np.abs(g.T@Hinv@g)/(np.abs(F) + 1e-6), '/')
            elif 'G' == msg:
                print('Termination: reaching the uncretainty level...')
            elif 'H' == msg:
                print('Termination: Hessian is a zero matrix...')
            else:
                print('Termination is caused by unknown reason...')
            print('----------------------------------------------------------')
            print('\n')
###################################################################################
def optOmit(x, xx, F, FF, g, g_1, H, H_1, Hinv, Hinv_1, iterate, s, tmp, sc, smeth, dsp_op):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    msg = 0
    flg = 0
    # tmp['F'] = np.inf
    sc = None
    if smeth == 'fprev2' or smeth == 'fprev3':
        if iterate == 1 and F > FF[0]:
            if F < tmp['F']:
                sc = s/2
                tmp['F'] = F
                tmp['x'] = x
                tmp['g'] = g
                tmp['H'] = H
                tmp['Hinv'] = Hinv
                x = c_(xx[:, 0])
                F = FF[0]
                g = g_1
                H = H_1
                Hinv = Hinv_1
            else:
                if np.any(dsp_op == 2): print('The uncertainty level has been reached and the precision could not be increased. Note: it is assumed that the objective function is unimodal. The optimization is terminated.')
                if FF[0] < tmp['F']:
                    F = FF[0]
                    x = c_(xx[:, 0])
                    g = g_1
                    H = H_1
                    Hinv = Hinv_1
                else:
                    x = tmp['x']
                    F = tmp['F']
                    g = tmp['g']
                    H = tmp['H']
                    Hinv = tmp['Hinv']
                iterate = 0
                msg = 'G'
            flg = 1
    return x, F, g, H, Hinv, tmp, sc, iterate, msg, flg
###################################################################################
def stepPar(s, F, FF, g, g_1, iter, flg, sc, smeth, su, p_decr, p_incr):
    # Stepsize Determination
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    if not sc is None:
        s = sc
    elif smeth == 'fprev2' or smeth == 'fprev3':
        #    smax = par['s_max']
        nn = len(FF)
        FF[np.arange(nn, 3)] = np.nan
        c = nans((3,))
        c[0] = FF[1] < FF[2]
        c[1] = FF[0] < FF[1]
        c[2] = F < FF[0]
        if (iter == 1 or iter == 2) and c[2] == 0:
            s1 = p_decr*s
        elif iter > 1 and smeth == 'fprev2':
            if np.all(c[2] == 1):
                s1 = p_incr*s
            else:
                s1 = p_decr*s
        elif iter > 2 and smeth == 'fprev3':
            if np.all(c == np.array([1, 1, 1])):
                s1 = p_incr*s
            elif np.all(c == np.array([1, 1, 0])):
                s1 = p_decr*s
            elif np.all(c == np.array([1, 0, 1])):
                s1 = s
            elif np.all(c == np.array([1, 0, 0])):
                s1 = p_decr*s
            elif np.all(c == np.array([0, 1, 1])):
                s1 = s
            elif np.all(c == np.array([0, 1, 0])):
                s1 = p_decr*s
            elif np.all(c == np.array([0, 0, 1])):
                s1 = s
            elif np.all(c == np.array([0, 0, 0])):
                s1 = p_decr*s
        else:
            s1 = s
        s = min([s1, su*np.abs(p_incr - 1)/5 + s])
        if s > su:   s = su
        if flg == 1: s = s/2
    elif smeth == 'gang':
        if iter < 1:
            s = 1
        else:
            norm2g = np.sqrt(g.T@g)
            norm2g_1 = np.sqrt(g_1.T@g_1)
            s = 1e-10 + (np.pi - np.arccos(min(1, g_1.T@g/max(norm2g_1*norm2g, 1e-06))))/np.pi*(su - 1e-10)
    elif smeth == 'none':
        s = 1
    return s
###################################################################################
def stopcrt(x=None, F=None, xx=None, FF=None, g=None, H=None, Hinv=None, itr=None, maxiter=None, fcnv=None, afcnv=None, xcnv=None,
            gcnv=None, sc=None):
    # Stopping Criteria
    # Contains a set of convergence criteria for NR, NRLS, NRPI, SD, etc.
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    if FF is None:
        F_1 = None
    elif isinstance(FF, (int, float)):
        F_1 = FF
    else:
        F_1 = FF[0, 0]
    if isinstance(xx, list) and len(xx) == 0:
        x_1 = None
    elif isinstance(xx, (int, float)):
        x_1 = xx
    else:
        x_1 = xx[:, 0]
    iterate = 1
    msg = '0'
    if maxiter is not None and itr >= maxiter:
        iterate = 0
        msg = 'B'
        return iterate, msg
    if fcnv is not None and not F_1 and np.abs(F - F_1)/min(np.array([1e12, np.abs(F_1) + 1e-6])) < fcnv:
        iterate = 0
        msg = 'C'
        return iterate, msg
    if afcnv is not None and not F_1 is None and np.abs(F - F_1) < afcnv:
        iterate = 0
        msg = 'D'
        return iterate, msg
    if xcnv is not None and not x_1 is None:
        x_1 = c_(x_1)
        d = nans(x.shape)
        ind1 = np.argwhere(np.abs(x_1) < 0.01)
        ind2 = np.argwhere(np.abs(x_1) >= 0.01)
        d[ind1, 0] = x[ind1, 0] - x_1[ind1, 0]
        d[ind2, 0] = (x[ind2, 0] - x_1[ind2, 0])/x_1[ind2, 0]
        if np.all(np.abs(d) <= xcnv):
            iterate = 0
            msg = 'E'
            return iterate, msg
    if gcnv is not None and np.abs(g.T@Hinv@g)/(np.abs(F) + 1e-6) < gcnv:
        iterate = 0
        msg = 'F'
        return iterate, msg
    return iterate, msg
###################################################################################

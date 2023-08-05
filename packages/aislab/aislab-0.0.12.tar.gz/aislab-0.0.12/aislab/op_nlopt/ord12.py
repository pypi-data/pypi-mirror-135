import numpy as np
#import numpy.matlib
from aislab.gnrl.sf import *
from .nlopt import *

# ###################################################################################
# def gnewton():
# ###################################################################################
# def steepd():
# ###################################################################################
# def qnewton():
# ###################################################################################
# def cgrad():
###################################################################################
def newton(x, func, grad, hes, args, met_opt='newt', maxiter=50, fcnv=None, afcnv=None, xcnv=None, gcnv=1e-6, sc=None, dsp_op=[2], smeth='fprev2', su=1, p_incr=1.2, p_decr=0.6, rcondH=1e-6, s=1):
# Newton-Raphson Method
#---------------------------------------------
# Author: Alexander Efemov
# Date:   20.12.2009
# Course: Modelling and Processes Optimization
#---------------------------------------------
    tmp = {}
    tmp['F'] = np.inf
    xx = []
    F = [];    FF = np.ones((3,1))*np.inf
    g = [];    g_1 = []
    H = [];    Hinv = []
    flg_omit = 0
    iterate = 1
    itr = 0


    # #########################################################
    # ah = args['data'].shape[1]
    # ax = args['data'][:, np.arange(0, ah - 3)]
    # ay = c_(args['data'][:, -3])
    # # aw = c_(args['data'][:, -2])
    # apm = args['x']
    # if x.shape[1] == 0: ax = c_(ax)
    # aym = apl_expW(ax, apm)
    # ae = ay - aym
    #
    # import matplotlib.pyplot as plt
    #
    # plt.scatter(ax, ay)
    # plt.plot(ax, apl_expW(ax, apm), 'r')
    # plt.show()
    # # print(ae.T @ ae)
    #
    # import matplotlib.pyplot as plt
    #
    # plt.scatter(ax, ay)
    # plt.plot(ax, apl_expW(ax, apm), 'k')
    # plt.show()
    # #########################################################

    while iterate:
        if not len(F) == 0:
            if itr == 1: FF = np.ones((3,1))*F
            else: FF = np.vstack((F, FF[:3]))
        if not len(g) == 0: g_1 = g
        if not len(H) == 0: H_1 = H; Hinv_1 = Hinv
        F, args = func(args)
        g = grad(args)
        H = hes(args)
        # # Termination & Display
        if np.all(np.all(H == 0)):
            if dsp_op >= 1: print('Hessian is a zero matrix. Optimization is terminated.')
            iterate = 0
            msg = 'H'
            continue
        # Hessian Inverse
        if not len(Hinv)==0: Hinv_1 = Hinv
        rcH = 1/np.linalg.cond(H)
        if rcH < rcondH: Hinv = nsinv(H)
        else:          Hinv = np.linalg.inv(H)
        iterate, msg = stopcrt(x, F, xx, FF, g, H, Hinv, itr, maxiter, fcnv, afcnv, xcnv, gcnv, sc)
        if itr > 0 and iterate: x, F, g, H, Hinv, tmp, sc, iterate, msg, flg_omit = optOmit(x, xx, F, FF, g, g_1, H, H_1, Hinv, Hinv_1, iterate, s, tmp, sc, smeth, dsp_op)
        if iterate == 0:
            if itr > 1 and F > FF[0]: F = FF[0]; x = c_(xx[:, 0]); g = g_1; H = H_1; Hinv = Hinv_1
        # dspl_logr(flg, x, F, itr, args.cnames, par)
        if dsp_op == 2: dspl(flg=dsp_op, x=x, F=F, itr=itr, args=args, s=s, meth=met_opt)
        if iterate == 0: continue
        # Descent Direction (p) & Quadratic Approx Step Size (p_len)
        p = -Hinv@g
        p_len = max([1e-12, np.sqrt(p.T@p)[0, 0]])
        p = p/p_len
        # Step Size Parameter
        s = stepPar(s, F, FF, g, g_1, itr, flg_omit, sc, smeth, su, p_decr, p_incr)
        mu = s*p_len
        # Line Search OR Polynomial Interpolation
        # if par['met_opt'] == 'newtls':
        #     opt1 = par; opt1.p = p; opt1.xx = x; opt1.x = mu
        #     mu, __ = newton_ls(opt1, dset, pOpt)
        # else:
        #     if par['meth_opt'] == 'newtpi' and itr > 0 and np.abs(F - FF[0])/np.abs(FF[0] + 1e-6) > 1e-6:
        #         opt1 = par; opt1.p = p; opt1.mu = mu
        #         mu = polIntMin(opt1, dset, pOpt)
        #         if mu < 0: mu = -mu; p = -p; print('Wrong polynomial interpolation')
        # Parameters Updatee
        if not len(x) == 0:
            if len(xx) == 0:
                xx = x
            else:
                if xx.shape[1] == 1: xx = np.hstack((x, xx))
                else:                xx = np.hstack((x, c_(xx[:, 0])))
        x = x + mu*p
        args['x'] = x
        itr = itr + 1

# end of optimization cycle
    if not msg != None: msg = 'E'
    if len(Hinv) == 0:
        rcH = 1/np.linalg.cond(H)
        if rcH < 1e-6: Hinv = nsinv(H)
        else:          Hinv = np.linalg.inv(H)
    if dsp_op: dspl(flg=1, x=x, xx=xx, F=F, FF=FF, g=g, H=H, Hinv=Hinv, itr=itr, msg=msg, maxiter=maxiter, fcnv=fcnv, afcnv=afcnv, xcnv=xcnv, gcnv=gcnv)
    return x, F, g, H, Hinv, itr


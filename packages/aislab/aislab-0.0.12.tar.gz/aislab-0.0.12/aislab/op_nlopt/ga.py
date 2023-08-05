import numpy as np
import pandas as pd

from aislab.gnrl.sf import *
from aislab.gnrl.measr import *
from aislab.tests.cstm_ga_scoring import *

##############################################################################

def fobj_sim(max_F, itrConstF):
    s = np.sum(F[0] == F)
    if s == itrConstF:  res = True
    else:               res = False

    # result = False
    # br = 0
    # for i in range(len(max_F) - 1):
    #     if max_F[i] == max_F[i + 1]:    br += 1
    #     else:                           br = 0
    # if br == itrConstF - 1: result = True
    return result

##############################################################################
def genopt(fobj, args, n=1, lb=0, ub=1, tpg='float', mod_indv='single', Nind=100, mut_rate=50, mut_strength=2, mut_met='Gauss', mut_stdev=70, pairing_met='Fbest', select_met='Fhalf', itrConstF=10, maxiter=100):
    # first generation
    indvs = population(Nind, n, lb, ub, tpg, mod_indv, 0)
    F = fobj(indvs, args)
    F, ind = sort(F)
    indvs = indvs[ind]
    FF = np.array([F[0]])
    iterate = stopcrt_ga(FF, 0, itrConstF, maxiter)
    itr = 0
    while iterate:
        itr += 1
        if not iterate: break
        # select next parents
        selected, Fsel, best, Fbst = selection(indvs, F, itr, select_met)
        # make couples
        couples = pairing(selected, Fsel, itr, met=pairing_met)
        # mating
        children = mating(couples, tpg, itr, mod=mod_indv)
        # mutate
        mutated = mutation(np.vstack((selected, children)), n, lb, ub, tpg, itr, mut_met, mut_rate, mut_strength, mut_stdev)
        # next generation
        indvs = np.vstack((mutated[:-1], best))
        F = np.vstack((c_(fobj(mutated[:-1], args)), Fbst)).flatten()
        F, ind = sort(F)
        indvs = indvs[ind]
        FF = np.append(FF, F[0])
        print(itr, 'Fmin = ', F[0])
        iterate = stopcrt_ga(FF, itr, itrConstF, maxiter)
    x_opt = np.array(indvs[0])
    F_opt = F[0]

    return F_opt, x_opt
##############################################################################
# def individual(args, seed):  # ng - number of genes, lb - lower bound, ub - upper bound
def individual(N, n=1, lb=0, ub=1, tpg=float, mod='single', seed=0):  # ng - number of genes, lb - lower bound, ub - upper bound
    # n - number(s) of gens - scalar (for mod='single') or list (for mod='seq2')
    # lb - lower bound(s) - scalar (for mod='single') or list (for mod='seq2')
    # ub - upper bound(s) - scalar (for mod='single') or list (for mod='seq2')
    # tpg - gens type: int, float
    # mod - mode: single, seq2...

    if mod == 'single':       # x is vector of size n in the range 0, 1
        x = rand((N, n), l=lb, h=ub, tp=tpg, seed=seed).flatten().tolist()

    elif mod == 'seq2': # x consists of two sequences of integers of length nc1 and nc2 respectively and ranges [lb1, ub1] and [lb2, ub2].
        # ORIG
        nc1, nc2 = n
        ub1, ub2 = ub
        lb1, lb2 = lb

        indv_1 = rand((N, nc1), l=lb1, h=ub1, tp=tpg, seed=seed).flatten().tolist()
        indv_2 = rand((N, nc2), l=lb2, h=ub2, tp=tpg, seed=seed + nc1 + 1).flatten().tolist()

        # comment this when N > 1
        indv_1.sort()
        indv_2.sort()
        # comment this when N > 1

        x = indv_1 + indv_2
    return x

##############################################################################
def mating(selected, tpg, itr, mod='single', met='Single Point'):
    N = len(selected)
    n = len(selected[0][0])
    j = 0
    children = nans((2*N, n))
    for i in range(len(selected)):
        parents = selected[i]
        if met == 'Single Point':
            cut = rand(l=1, h=n, tp=tpg, seed=itr+i)[0, 0]
            children[j, :] = np.hstack((parents[0][0:cut], parents[1][cut:]))
            j += 1
            children[j, :] = np.hstack((parents[1][0:cut], parents[0][cut:]))
            j += 1
        if met == 'Two Pionts':
            cut_1 = rand(l=1, h=n - 1, tp=tpg, seed=seed)
            cut_2 = rand(l=1, h=n, tp=tpg, seed=seed + cut_1)
            br = 0
            while cut_2 < cut_1:
                br += 1
                cut_2 = rand(l=1, h=n, tp=tpg, seed=seed + 2 + br)
            child = [parents[0][0:cut_1] + parents[1][cut_1:cut_2] + [parents[0][cut_2:]]]
            child.append([parents[1][0:cut_1] + parents[0][cut_1:cut_2] + [parents[1][cut_2:]]])

    return children

##############################################################################
def mutation(indvs, n, lb, ub, tpg, seed, mut_met, mut_rate, mut_strength, mut_stdev):
    if isinstance(n, list):     n = np.sum(n)
    if isinstance(lb, list):    minx = np.min(lb)
    else:                       minx = lb
    if isinstance(ub, list):    maxx = np.min(ub)
    else:                       maxx = ub

    i_mut = find(rand(size=(len(indvs),), seed=seed) < mut_rate/100)
    Nmut = len(i_mut)
    ind = rand(size=(Nmut, mut_strength), l=0, h=n-1, tp='int', seed=seed+1)
    if mut_met == 'Gauss':
        r = randn((Nmut, mut_strength), m=0, s=mut_stdev, seed=seed)
        for i in range(len(i_mut)): indvs[i_mut[i], ind[i]] = indvs[i_mut[i], ind[i]] + r[i, :]
    if mut_met == 'Reset':
        r = rand((Nmut, mut_strength), l=minx, h=maxx, tp=tpg, seed=seed)
        for i in range(len(i_mut)): indvs[i_mut[i], ind[i]] = r[i, :]
    return indvs.astype(tpg) # mutated individual
##############################################################################
def pairing(indvs, F, seed, met='Fbest'):
    n = len(indvs)
    n2 = n // 2
    if met == 'Fbest':
        parents = [[indvs[i], indvs[i + 1]] for i in range(n2)]
    elif met == 'rnd':
        i1 = rand((n2,), l=0, h=n - 1, tp='int', seed=seed)
        i2 = rand((n2,), l=0, h=n - 1, tp='int', seed=seed + n2)
        p1 = indvs[i1]
        p2 = indvs[i2]
        parents = []
        for i in range(n2):
            parents.append([p1[i], p2[i]])
            j = 0
            while np.all(p1[i] == parents[i][1]):
                j += 1
                parents[i][1] = indvs[rand(l=0, h=n - 1, tp='int', seed=seed+2*n+j)[0, 0]]
    elif met == 'wrnd':
        ind = (np.isinf(F) == False) & (np.isnan(F) == False)
        if all(ind == False):   print('ERROR in roulette method: at least one weight should be a number...'); return []
        w, _ = rnml(-c_(F[ind]))
        w = np.vstack((0, w))
        i1 = roulette(w, n=n2, seed=seed).astype(int).flatten()
        i2 = roulette(w, n=n2, seed=seed + n).astype(int).flatten()
        p1 = indvs[i1,:]
        p2 = indvs[i2]
        parents = []
        for i in range(n2):
            parents.append([p1[i], p2[i]])
            j = 0
            while np.all(p1[i] == parents[i][1]):
                j += 1
                parents[i][1] = indvs[roulette(w, 1, seed=seed + 2*n + j).astype(int).flatten()]
    return parents

##############################################################################
def population(N, n, lb, ub, tpg, mod_indv, itr):
    m = np.sum(n)
    pop = nans((N, m))
    for i in range(N):
        seed = (itr + i)*m
        pop[i,:] = individual(1, n, lb, ub, tpg, mod_indv, seed)
    # pop = individual(N, n, lb, ub, tpg, mod_indv, seed)

    return pop

##############################################################################
def roulette(w, n, seed=0):
    from aislab.dp_feng.binenc import cut
    wr, _ = rnml(c_(w.cumsum()), 0, 1)
    c = np.unique(wr)[:-1]
    r = rand(size=(n,), seed=seed)
    return cut(r, cuts=c) - 1

##############################################################################
def selection(indvs, F, seed, met='Fhalf'):
    # select best individual
    indvbst = indvs[0]
    Fbst = F[0]
    indvs = indvs[1:]
    F = F[1:]
    n = len(F)
    ns = int(np.ceil(n/2))
    if met == 'roulette':
        ind = (np.isinf(F) == False) & (np.isnan(F) == False)
        if all(ind == False):   print('ERROR in roulette method: at least one weight should be a number...'); return []
        w, _ = rnml(-c_(F[ind]))
        w = np.vstack((0, w))
        sind = roulette(w, n=n//2, seed=seed).astype(int)
        indvsel = indvs[sind]
        Fsel = F[sind]
    elif met == 'Fhalf':
        indvsel = indvs[:ns]
        Fsel = F[:ns]
    elif met == 'rnd':
        ind = rand((ns,), l=0, h=len(F) - 1, tp='int', seed=seed)
        indvsel = indvs[ind]
        Fsel = F[ind]

    return indvsel, Fsel, indvbst, Fbst

##############################################################################
def stopcrt_ga(fitness_min, itr, itrConstF, maxiter):
    iterate = 1
    if itr >= maxiter:                  iterate = 0
    if np.sum(fitness_min[-1] == fitness_min) >= itrConstF:  iterate = 0
    return iterate
##############################################################################

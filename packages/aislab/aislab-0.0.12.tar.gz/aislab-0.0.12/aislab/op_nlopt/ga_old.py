import numpy as np
import pandas as pd

from aislab.gnrl.sf import *
from aislab.gnrl.measr import *
from aislab.op_nlopt.cstm import *

##############################################################################
def firstgen(pop, fobj, args):
    # F = [fobj(pop[x], args) for x in range(len(pop))]
    F = fobj(pop, args)
    sorted_F = sorted([[pop[x], F[x]] for x in range(len(pop))], key=lambda x: x[1])
    population = [sorted_F[x][0] for x in range(len(sorted_F))]
    F = [sorted_F[x][1] for x in range(len(sorted_F))]
    return {'individuals': population, 'F': sorted(F)}

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
    pop = population(Nind, n, lb, ub, tpg, mod_indv, 0)
    gen = []
    gen.append(firstgen(pop, fobj, args))
    fitness_avg = np.array([sum(gen[0]['F'])/len(gen[0]['F'])])
    fitness_min = np.array([min(gen[0]['F'])])
    iterate = True
    itr = 0
    while iterate:
        itr += 1
        iterate = stopcrt_ga(fitness_min, fitness_avg, itr, itrConstF, maxiter)
        if not iterate: break
        gen.append(nextgen(args, gen[-1], fobj, mod_indv, itr, n, lb, ub, Nind, select_met, pairing_met, mut_rate, mut_met, mut_strength, mut_stdev))
        fitness_avg = np.append(fitness_avg, sum(gen[-1]['F'])/len(gen[-1]['F']))
        fitness_min = np.append(fitness_min, min(gen[-1]['F']))
        print(itr, 'Fmin = ', gen[-1]['F'][0])
    x_opt = np.array(gen[-1]['individuals'][0])
    F_opt = gen[-1]['F'][0]

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
def mating(parents, seed, mod='single', met='Single Point'):
    n = len(parents[0])
    if met == 'Single Point':
        cut = rand(l=1, h=n, tp='int', seed=seed)[0, 0]
        child = [parents[0][0:cut] + parents[1][cut:]]
        child.append(parents[1][0:cut] + parents[0][cut:])
    seed = seed + 1
    if met == 'Two Pionts':
        # cut = rand((2,), l=1, h=n, tp='int', seed=seed)
        # if cut[0] == cut[1]:
        #     cut = cut[0]
        #     if cut - 1 > n - cut
        #         cut_1 = rand(l=1, h=cut, tp='int', seed=seed + cut_1)
        #         cut_2 = cut
        #     else:
        #         cut_1 = cut
        #         cut_2 = rand(l=cut, h=n, tp='int', seed=seed + cut_1)
        # else:
        #     cut_1 = np.min(cut)
        #     cut_2 = np.max(cut)

        cut_1 = rand(l=1, h=n - 1, tp='int', seed=seed)
        cut_2 = rand(l=1, h=n, tp='int', seed=seed + cut_1)
        br = 0
        while cut_2 < cut_1:
            br += 1
            cut_2 = rand(l=1, h=n, tp='int', seed=seed + 2 + br)
        child = [parents[0][0:cut_1] + parents[1][cut_1:cut_2] + [parents[0][cut_2:]]]
        child.append([parents[1][0:cut_1] + parents[0][cut_1:cut_2] + [parents[1][cut_2:]]])
    return child

##############################################################################
def mutation(indv, n, lb, ub, seed, i_mut, i, mut_met, mut_strength, mut_stdev):
    if not any(i_mut == i): return indv
    if isinstance(n, list):     n = np.sum(n)
    if isinstance(lb, list):    minx = np.min(lb)
    else:                       minx = lb
    if isinstance(ub, list):    maxx = np.min(ub)
    else:                       maxx = ub

    ind = rand(size=(mut_strength,), l=0, h=n-1, tp='int', seed=seed)
    if mut_met == 'Gauss':
        for x in ind:
            seed = seed*x + 1
            indv[x] = int(indv[x] + randn(m=0, s=mut_stdev, seed=seed))
    if mut_met == 'Reset':
        for x in ind:
            seed = seed*x + 1
            indv[x] = rand(l=minx, h = maxx, tp='int', seed=seed)[0, 0]
    return indv # mutated individual
##############################################################################
def nextgen(args, gen, fobj, mod, itr, n, lb, ub, Nind, select_met, pairing_met, mut_rate, mut_met, mut_strength, mut_stdev):
    best = {}
    best['individuals'] = gen['individuals'].pop(0)
    best['F'] = gen['F'].pop(0)
    selected = selection(gen, itr, select_met)
    parents = pairing(best, selected, itr, met=pairing_met)
    children = [[[mating(parents[i], itr + i + j, mod=mod) for i in range(len(parents))][j][h] for h in range(2)] for j in range(len(parents))]
    children1 = [children[i][0] for i in range(len(parents))]
    children2 = [children[i][1] for i in range(len(parents))]
    unmutated = selected['individuals'] + children1 + children2
    N = len(gen['individuals'])
    i_mut = find(rand(size=(N,), seed=itr) < mut_rate/100)
    mutated = [mutation(unmutated[i], n, lb, ub, itr*Nind + i, i_mut, i, mut_met, mut_strength, mut_stdev) for i in range(N)]
    indvs = mutated + [best['individuals']]
    next_sgen = {}
    F = np.append(fobj(mutated, args), best['F'])
    sorted_next_gen = sorted([[indvs[x], F[x]] for x in range(len(indvs))], key=lambda x: x[1])
    next_sgen['individuals'] = [sorted_next_gen[x][0] for x in range(len(sorted_next_gen))]
    next_sgen['F'] = [sorted_next_gen[x][1] for x in range(len(sorted_next_gen))]
    return next_sgen

##############################################################################
def pairing(best, selected, seed, met='Fbest'):
    indvs = [best['individuals']] + selected['individuals']
    F = [best['F']] + selected['F']
    n = len(indvs)
    if met == 'Fbest':
        parents = [[indvs[i], indvs[i + 1]] for i in range(n // 2)]
    if met == 'rnd':
        parents = []
        n2 = n // 2
        for i in range(n2):
            seed = seed + n2 + i
            parents.append([indvs[rand(l=0, h=n - 1, tp='int', seed=seed)[0, 0]],
                            indvs[rand(l=0, h=n - 1, tp='int', seed=seed + n2)[0, 0]]])
            br = 0
            while parents[i][0] == parents[i][1]:
                br += 1
                seed = seed + 2*n2 + i + br
                parents[i][1] = indvs[rand(l=0, h=n - 1, tp='int', seed=seed)[0, 0]]
    if met == 'wrnd':
        normalized_F = sorted([F[i]/sum(F) for i in range(n // 2)], reverse=True)
        csum = np.array(normalized_F).cumsum()
        parents = []
        for i in range(n // 2):
            parents.append([indvs[roulette(csum, rand(seed=seed + i))], indvs[roulette(csum, rand(seed=seed + n + i))]])
            j = 0
            while parents[i][0] == parents[i][1]:
                j += 1
                parents[i][1] = indvs[roulette(csum, rand(seed=seed + 2*n + j))]
    return parents


##############################################################################
def population(N, n, lb, ub, tpg, mod_indv, itr):

    nn = np.sum(n)

    pop = []
    for i in range(N):
        seed = (itr + i)*nn
        pop += [individual(1, n, lb, ub, tpg, mod_indv, seed)]
    # pop = individual(N, n, lb, ub, tpg, mod_indv, seed)

    return pop


##############################################################################
def roulette(cum_sum, chance):
    cumF = list(cum_sum.copy())
    cumF.append(chance)
    cumF = sorted(cumF)
    return cumF.index(chance)


##############################################################################
def selection(gen, seed, met='Fhalf'):
    FF = gen['F']
    n = len(gen['individuals'])
    ns = int(np.ceil(n/2))
    if met == 'roulette':
        ind = np.isinf(FF) == False
        if all(ind == False):   sF = 1
        else:                   sF = np.sum(FF[ind]) +1e-6*(np.sum(FF[ind]) == 0)
        # sorted(F)
        # F1 = copy.deepcopy(F)
        # Fn = rnml(F)
        Fn = sorted([FF[i]/sF for i in range(len(FF))], reverse=False)  # normalization of F
        cumFn = np.array(Fn).cumsum()
        selected = []
        for i in range(n // 2):
            selected.append(roulette(cumFn, rand(seed=seed + i)[0, 0]))
            j = 0
            while len(set(selected)) != len(selected):
                j += 1
                selected[i] = roulette(cumFn, rand(seed + n + j)[0, 0])
        selected = {'individuals': [gen['individuals'][int(selected[i])] for i in range(n // 2)],
                    'F': [FF[int(selected[i])] for i in range(n // 2)]}
    elif met == 'Fhalf':
        selected_indvs = [gen['individuals'][i] for i in range(ns)]
        Fwinners = [FF[i] for i in range(ns)]
        selected = {'individuals': selected_indvs, 'F': Fwinners}
    elif met == 'rnd':
        selected_indvs = [gen['individuals'][rand(l=0, h=len(FF) - 1, tp='int', seed=seed + i)[0, 0]] for i in range(ns)]
        Fwinners = [FF[rand(l=0, h=len(FF) - 1, tp='int', seed=seed + i)[0, 0]] for i in range(ns)]
        selected = {'individuals': selected_indvs, 'F': Fwinners}
    return selected

##############################################################################

def stopcrt_ga(fitness_min, fitness_avg, itr, itrConstF, maxiter):
    iterate = 1
    if itr >= maxiter:                  iterate = 0
    # if max(fitness_max) >= 0:           iterate = 0
    # if max(fitness_avg) >= 0:           iterate = 0
    if np.sum(fitness_min[-1] == fitness_min) >= itrConstF:  iterate = 0
    return iterate
##############################################################################

def tables(x, args):
    from aislab.gnrl.sf import sort
    from aislab.dp_feng.binenc import cut

    data = args['data']  # data set
    nc1 = args['nc1']  # number of cut-offs w.r.t. first (GB) scorecard
    nc2 = args['nc2']  # number of cut-offs w.r.t. second (GBR) scorecard

    lb1 = args['lb1']  # lower bound for cut-offs of the first scorecard
    lb2 = args['lb2']  # lower bound for cut-offs of the second scorecard
    ub1 = args['ub1']  # upper bound for cut-offs of the first scorecard
    ub2 = args['ub2']  # upper bound for cut-offs of the second scorecard
    minx = np.min([args['minx'], np.min(x)])  # upper bound for cut-offs of the first scorecard
    maxx = np.max([args['maxx'], np.max(x)])  # upper bound for cut-offs of the second scorecard


    x1, ss = sort(c_(x[:nc1, ]))
    x2, ss = sort(c_(x[nc1:, ]))
    minx = np.min([minx, np.min(x)])  # upper bound for cut-offs of the first scorecard
    maxx = np.max([maxx, np.max(x)])  # upper bound for cut-offs of the second scorecard
    x1 = (x1 - minx)/(maxx - minx)*(ub1 - lb1) + lb1
    x2 = (x2 - minx)/(maxx - minx)*(ub2 - lb2) + lb2
    x1 = np.round(x1.flatten())
    x2 = np.round(x2.flatten())

    cs = np.hstack((x1, x2))

    GB_zones = cut(data['Score_GB'].values, x1).flatten()
    GBR_zones = cut(data['Score_GBR'].values, x2).flatten()

    names1 = ['GB_A']
    for i in range(nc1 - 1): names1.append('GB_G' + str(i+1))
    names1.append('GB_R')
    names2 = ['GBR_A']
    for i in range(nc2 - 1): names2.append('GBR_G' + str(i+1))
    names2.append('GBR_R')
    # confusion matrix
    good = confm(-GB_zones, -GBR_zones, w=data['Good'].values, ux1=range(1-len(names1), 1), ux2=range(1-len(names2), 1)).astype(int)
    bad = confm(-GB_zones, -GBR_zones, w=data['Bad'].values, ux1=range(1-len(names1), 1), ux2=range(1-len(names2), 1)).astype(int)
    reject = confm(-GB_zones, -GBR_zones, w=data['Reject'].values, ux1=range(1-len(names1), 1), ux2=range(1-len(names2), 1)).astype(int)

    # n1 = len(names1)
    # for i in range(n1):
    #     if i not in np.unique(GB_zones):
    #         good = np.hstack((good[:, :i], nans((n1, 1)), good[:, (i+1):]))
    # n2 = len(names2)
    # for i in range(n2):
    #     if i not in np.unique(GBR_zones):
    #         good = np.vstack((good[:i, :], nans((1, n2)), good[(i+1):, :]))


    good = pd.DataFrame(good, index=names1, columns=names2)
    bad = pd.DataFrame(bad, index=names1, columns=names2)
    reject = pd.DataFrame(reject, index=names1, columns=names2)

    bad_rate = bad/(good + bad)*100
    total_gb = good + bad
    total = total_gb + reject
    return good, bad, reject, total_gb, total, bad_rate, cs


##############################################################################
def tables2(G, B, R, TGB, TGBR, BR, args):
    # GB Scorecard
    nc1 = args['nc1']  # number of cut-offs w.r.t. first (GB) scorecard
    nc2 = args['nc2']  # number of cut-offs w.r.t. first (GB) scorecard
    names1 = ['Accept']
    for i in range(nc1 - 1): names1.append('GB_G' + str(i+1))
    names1.append('Reject')
    names1.append('Total')
    names2 = ['Accept']
    for i in range(nc2 - 1): names2.append('GB_G' + str(i+1))
    names2.append('Reject')
    names2.append('Total')
    G1 = np.sum(G, axis=1)
    B1 = np.sum(B, axis=1)
    R1 = np.sum(R, axis=1)
    BadRej = B1 + R1
    TGBR1 = np.sum(TGBR, axis=1)
    TotalPrc = TGBR1/np.sum(TGBR1)*100
    BR = B1/(G1 + B1)*100
    BadAndRejectRate = BadRej/(G1 + BadRej)*100
    T1 = np.vstack((G1, B1, R1, BadRej, TGBR1, np.round(TotalPrc, 1), np.round(BR, 1), np.round(BadAndRejectRate, 1)))
    BR1 = np.sum(B1)/np.sum(G1 + B1)
    BadAndRejectRate1 = np.sum(B1 + R1)/np.sum(G1 + B1 + R1)
    Tot1 = [np.sum(np.sum(G1)), np.sum(np.sum(B1)), np.sum(np.sum(R1)), np.sum(np.sum(BadRej)), np.sum(np.sum(TGBR1)),
            np.sum(np.sum(TotalPrc)), BR1, BadAndRejectRate1]
    Tot = np.round(np.array([Tot1]).T, 1)
    T1 = np.hstack((T1, Tot))
    T1 = pd.DataFrame(T1, index=['Good', 'Bad', 'Reject', 'BadAndReject', 'Total', 'TotalPrc', 'BadRate', 'BadAndRejectRate'], columns=names1)
    # GBR Scorecard
    G2 = np.sum(G, axis=0)
    B2 = np.sum(B, axis=0)
    R2 = np.sum(R, axis=0)
    BadRej = B2 + R2
    TGBR2 = np.sum(TGBR, axis=0)
    TotalPrc = TGBR2/np.sum(TGBR2)*100
    BR = B2/(G2 + B2)*100
    BadAndRejectRate = BadRej/(G2 + BadRej)*100
    T2 = np.vstack((G2, B2, R2, BadRej, TGBR2, np.round(TotalPrc, 1), np.round(BR, 1), np.round(BadAndRejectRate, 1)))
    BR1 = np.sum(B2)/np.sum(G2 + B2)
    BadAndRejectRate1 = np.sum(B2 + R2)/np.sum(G2 + B2 + R2)
    Tot1 = [np.sum(np.sum(G2)), np.sum(np.sum(B2)), np.sum(np.sum(R2)), np.sum(np.sum(BadRej)), np.sum(np.sum(TGBR2)),
            np.sum(np.sum(TotalPrc)), BR1, BadAndRejectRate1]
    Tot = np.round(np.array([Tot1]).T, 2)
    T2 = np.hstack((T2, Tot))
    T2 = pd.DataFrame(T2, index=['Good', 'Bad', 'Reject', 'BadAndReject', 'Total', 'TotalPrc', 'BadRate', 'BadAndRejectRate'], columns=names2)
    return T1, T2
###############################################################################

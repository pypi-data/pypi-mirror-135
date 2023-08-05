"""
author: OPEN-MAT
date: 	15.06.2019
Matlab version:
    author: Alexander Efremov
    date:   26 Apr 2009
    course: Multivariable Control Systems
"""
import numpy as np

##############################################################################
def blkdiag(x):
    if isinstance(x, (int, float, str, np.int64)): y = np.array([x])
    if isinstance(x, (list, tuple)):
        for i in np.arange(len(x)):
            if isinstance(x[i], (int, float, str, np.int64)): xi = m_([x[i]])
            elif isinstance(x[i], (list, tuple)):             xi = m_([x[i]])
            else:                                             xi = x[i]
            if xi.ndim == 1: xi = m_([xi])
            if i == 0:
                y = xi
                continue
            y = np.vstack((y, zeros(xi.shape[0], y.shape[1])))
            y = np.hstack((y, np.vstack((zeros(y.shape[0] - xi.shape[0], xi.shape[1]), xi))))
    return y
##############################################################################
def c_(x):
    if isinstance(x, (int, float, str, np.int64)): x = np.array([x])
    return np.reshape(x, (len(x), 1))
##############################################################################
def cmp(x, y, skipna=False, skipinf=False):
    if isinstance(x, list): x = np.array(x)
    if isinstance(y, list): y = np.array(y)
    if skipna:
        ix = np.isnan(x) == False
        iy = np.isnan(y) == False
        ind = ix & iy
        x = x[ind]
        y = y[ind]
    if skipinf:
        ix = np.isinf(x) == False
        iy = np.isinf(y) == False
        ind = ix & iy
        x = x[ind]
        y = y[ind]
    return np.max(np.max(np.abs(x - y)))
##############################################################################
def delrc(x, i, j=None):
    '''
    DELRC deletes i-th row and j-th column of matrix x.
    If x is mxn, the resulting matrix is m-1 x n-1.
    If x is n dimensional row or column vector, the resulting vector is n-1 dimensional.
    '''
    if len(x.shape) == 1:
        n = len(x)
        res = np.empty((n-1), x.dtype)
        res[:i] = x[:i]
        res[i:] = x[i+1:]
    elif x.shape[0] > 1 and x.shape[1] > 1:
        if j is None: j = i
        n = x.shape[0]
        res = np.empty((n-1, n-1), x.dtype)
        res[:i, :j] = x[:i, :j]
        res[:i, j:] = x[:i, j+1:]
        res[i:, :j] = x[i+1:, :j]
        res[i:, j:] = x[i+1:, j+1:]
    elif x.shape[0] == 1:
        n = x.shape[1]
        res = np.empty((1, n-1), x.dtype)
        res[0, :i] = x[0, :i]
        res[0, i:] = x[0, i+1:]
    elif x.shape[1] == 1:
        n = x.shape[0]
        res = np.empty((n-1, 1), x.dtype)
        res[:i, 0] = x[:i, 0]
        res[i:, 0] = x[i+1:, 0]
    return res
##############################################################################
def diff(x):
    if x.shape[1] > 1: dx = x[1:, :] - x[:-1, :]
    else:              dx = x[1:] - x[:-1]
    return dx
##############################################################################
def eps(tp=None):
    if tp is None: return np.finfo(float).eps
    if tp is np.float32: return np.finfo(tp).eps
##############################################################################
def eye(size, size2=None):
    if size2 is None:
        if isinstance(size, (int, np.int64, float)): size = [size, size]
        if len(size) == 1: size = (int(size[0]),)
        else:              size = int(size[0]), int(size[1])
    else:
        try:
            size = int(size), int(size2)
        except:
            raise Exception('In EYE(): Incorrect input parameters. Should be ones((<rows>, <cols>)), ones(<rows>, <cols>) or ones(<rows_cols>).')

    s11 = np.min(np.min(size))
    s12 = (s11, size[1] - s11)
    s21 = (size[0] - s11, s11)
    s22 = (s21[0], s12[1])
    res = np.vstack((np.hstack((np.eye(s11), np.zeros(s12))), np.hstack((np.zeros(s21), np.zeros(s22))))) 
    return res
##############################################################################
def find(x, n=None, pos=None):
    if len(x.shape) == 1:
        ind, = np.where(x)
        if n is None:
            if pos is None: res = ind
            elif pos == 'first': res = ind[0]
            elif pos == 'last': res = ind[-1]
        else:
            if pos is None: res = ind[:n]
            elif pos == 'first': res = ind[:n]
            elif pos == 'last': res = ind[-n:]
    else:
        c,r = np.where(x.T)
        if n is None:
            if pos is None: res = r,c
            elif pos == 'first': res = r[0],c[0]
            elif pos == 'last': res = r[-1],c[-1]
        else:
            if pos is None: res = r[:n],c[:n]
            elif pos == 'first': res = r[:n],c[:n]
            elif pos == 'last': res = r[-n:],c[-n:]
    return res
###################################################################################
def hnkl(x, n=None, flp=False):
    N = len(x)
    if n == None: n = N
    if not flp:
        if n == N:
            X = r_(x)
        else:
            ind = np.tile(np.arange(N - n + 1).reshape(-1, 1), (1, n)) + np.tile(np.arange(n), (N - n + 1, 1))
            X = np.take(x, ind)
    else:
        if n == N:
            ind = np.arange(N-1, -1, -1)
            X = r_(x[ind, :])
        else:
            ind = np.tile(np.arange(N - n + 1).reshape(-1, 1), (1, n)) + np.tile(np.arange(n-1, -1, -1), (N - n + 1, 1))
            X = np.take(x, ind)

    return X
###################################################################################
def ind2sub(array_shape, ind):
    # Transforms linear indices (row wise) into {row, col} indices of 2D array
    # Replicates matlabs ind2sub
    rows = (ind.astype("int32") // array_shape[1])
    cols = (ind.astype("int32") % array_shape[1])
    return(rows, cols)
###################################################################################
def isnum(x):
    if np.issubdtype(np.array([x]).dtype, np.number): return True
    return False
###################################################################################
def m_(x=[], size=None, size2=None, tp=None):
    # m_() = m_(size=(0,0)) --> array([], shape=(0, 0), dtype=float64)
    # m_([])                --> array([], dtype=float64)
    
    try:
        if size is None:    res = np.array(x)
        elif size2 is None:
            if isinstance(size, (int, np.int64, float)): size = [size, size]
            if len(size) == 1:  size = (int(size[0]),)
            else:               size = int(size[0]), int(size[1])
            if isinstance(x, (int, np.int64, float)): return np.full(size, x)
            else: res = np.reshape(np.array([x]), size)
        else:
            size = int(size), int(size2)
            size1 = (zeros(1, 2).astype(int)).flatten()
            size1[:] = size
            size1[(np.array(size) == 1).flatten()] = 0
            if isinstance(x, (int, np.int64, float)): res = np.full(size, x)
            else: res = np.reshape(np.array([x]), size)
    except: raise Exception('In M_(): Incorrect input parameters. Should be m_(x, (<rows>, <cols>)), m_(x, <rows>, <cols>) or m_(x, <rows_cols>).')
    if tp is not None:  return res.astype(tp)
    else: return res
###################################################################################
def max1(x, axis=0, naskip=False):
    # Returns maximum element of an array and corresponding index
    if naskip: x[np.isnan(x)] = min(x[np.invert(np.isnan(x))]) - 1
    if x.ndim == 2:
        N, m = x.shape
        if axis == 0:
            xmax = np.amax(x, axis=axis)
            i1, i2 = np.where(x == xmax)
            ind = nans((1, m))
            for i in range(m): ind[0, i] = i1[i2 == i][0]
            xmax = r_(xmax)
        if axis == 1:
            xmax = c_(np.amax(x, axis=axis))
            i1, i2 = np.where(x == xmax)
            ind = nans((N, 1))
            for i in range(N): ind[i, 0] = i2[i1 == i][0]
        if any(np.array([N, m]) == 1):
            xmax = xmax.flatten()[0]
            ind = ind.flatten()[0]
    else:
        xmax = np.amax(x)
        i1, = np.where(x == xmax)
        ind = i1[0]
    ind = ind.astype(int)
    return xmax, ind
##############################################################################
def min1(x, axis=0, naskip=False):
    # Returns minimum element of an array and corresponding index
    if naskip: x[np.isnan(x)] = max(x[np.invert(np.isnan(x))]) + 1
    if x.ndim == 2:
        N, m = x.shape
        if axis == 0:
            xmin = np.amin(x, axis=axis)
            i1, i2 = np.where(x == xmin)
            ind = nans((1, m))
            for i in range(m): ind[0, i] = i1[i2 == i][0]
            xmin = r_(xmin)
        if axis == 1:
            xmin = c_(np.amin(x, axis=axis))
            i1, i2 = np.where(x == xmin)
            ind = nans((N, 1))
            for i in range(N): ind[i, 0] = i2[i1 == i][0]
        if any(np.array([N, m]) == 1):
            xmin = xmin.flatten()[0]
            ind = ind.flatten()[0]
    else:
        xmin = np.amin(x)
        i1, = np.where(x == xmin)
        ind = i1[0]
    ind = ind.astype(int)

    return xmin, ind
##############################################################################
def nans(size, size2=None):
    if size2 is None:
        if isinstance(size, (int, np.int64, float)): size = [size, size]
        if len(size) == 1: size = (int(size[0]),)
        else:              size = int(size[0]), int(size[1])
    else:
        try:
            if isinstance(size, (int, np.int64, float)):  size = int(size), int(size2)
            else:                               size = int(size[0]), int(size[1]), int(size2) # for 3d tensors
        except:
            raise Exception('In NANS(): Incorrect input parameters. Should be nans((<rows>, <cols>)), nans(<rows>, <cols>) or nans(<rows_cols>).')
    res = np.full(size, np.nan)
    return res
###################################################################################
def num2lst(a):
    # Converts array to list. If array is 2D, then i-th element of the list is a list consisting the elements of the i-th row of.
    if type(a) is np.ndarray: return [num2lst(x) for x in a]
    else:                     return a
##############################################################################
def ones(size, size2=None):
    if size2 is None:
        if isinstance(size, (int, np.int64, float)): size = [size, size]
        if len(size) == 1: size = (int(size[0]),)
        else:              size = int(size[0]), int(size[1])
    else:
        try:
            if isinstance(size, (int, np.int64, float)):  size = int(size), int(size2)
            else:                               size = int(size[0]), int(size[1]), int(size2) # for 3d tensors
        except:
            raise Exception('In ONES(): Incorrect input parameters. Should be ones((<rows>, <cols>)), ones(<rows>, <cols>) or ones(<rows_cols>).')
    res = np.ones(size)
    return res
##############################################################################
def r_(x):
    if isinstance(x, (int, float, str, np.int64)): x = np.array([x])
    return np.reshape(x, (1, len(x)))
##############################################################################
def sm_(x, i, j=None):
    '''
    SM_() returns a submatrix consisting of rows i and columns j of the initial matrix x.
    i and j are listis, or np.arrays - row or column vectors consisting of the indexes of
    the rows and columns, respectively to keep in the resulting submatrix.
    If only i is given, then the resulting matrix consists of i-th rows and columns of x.
    If x is n dimensional row or column vector, the result is again vector consisting of i elements of x.

    '''
    if len(i.shape) > 1: i = i.flatten()
    if j is not None and len(j.shape) > 1: j = j.flatten()
    i = i.astype(int)
    if j is not None: j = j.astype(int)
    if len(x.shape) == 1:   return x[np.ix_(i)]
    elif x.shape[0] > 1 and x.shape[1] > 1:
        if j is None:       return x[np.ix_(i)]
        else:               return x[np.ix_(i, j)]
    elif x.shape[0] == 1:   return x[0, np.ix_(i)]
    elif x.shape[1] == 1:   return x[np.ix_(i)]
###############################################################################
def sumls(ls1, ls2): return [x + y for x, y in zip(ls1, ls2)]
###################################################################################
def vec(x):
    if type(x) is not np.ndarray: x = m_(x)
    return c_(x.T.flatten())
##############################################################################
def zeros(size, size2=None):
    if size2 is None:
        if isinstance(size, (int, np.int64, float)): size = [size, size]
        if len(size) == 1: size = (int(size[0]),)
        else:              size = int(size[0]), int(size[1])
    else:
        try:
            if isinstance(size, (int, np.int64, float)):  size = int(size), int(size2)
            else:                               size = int(size[0]), int(size[1]), int(size2) # for 3d tensors
        except:
            raise Exception('In ZEROS(): Incorrect input parameters. Should be ones((<rows>, <cols>)), ones(<rows>, <cols>) or ones(<rows_cols>).')

    res = np.zeros(size)
    return res
##############################################################################
##############################################################################
##############################################################################
# # python equivalent of matlabs' tic & toc functions
# # taken from: https://stackoverflow.com/questions/5849800/what-is-the-python-equivalent-of-matlabs-tic-and-toc-functions
# import time
# def TicTocGenerator():
#     # Generator that returns time differences
#     ti = 0           # initial time
#     tf = time.time() # final time
#     while True:
#         ti = tf
#         tf = time.time()
#         yield tf-ti # returns the time difference
#
# TicToc = TicTocGenerator() # create an instance of the TicTocGen generator
#
# # This will be the main function through which we define both tic() and toc()
# def toc(dsp=1, tempBool=True):
#     # Prints the time difference yielded by generator instance TicToc
#     tempTimeInterval = next(TicToc)
#     if tempBool:
#         if dsp: print('Elapsed time ', dsp, ': %f seconds.\n' %tempTimeInterval )
#     return tempTimeInterval
#
# def tic():
#     # Records a time in TicToc, marks the beginning of a time interval
#     toc(tempBool=False)
# TicToc2 = TicTocGenerator() # create another instance of the TicTocGen generator
#
# def toc2(dsp=1, tempBool=True):
#     # Prints the time difference yielded by generator instance TicToc2
#     tempTimeInterval = next(TicToc2)
#     if tempBool:
#         if dsp: print('Elapsed time ', dsp, ': %f seconds.\n' %tempTimeInterval)
#     return tempTimeInterval
# def tic2():
#     # Records a time in TicToc2
#     toc2(tempBool=False)
# ##############################################################################

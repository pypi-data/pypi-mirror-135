##############################################################################
# python equivalent of matlabs' tic & toc functions
# taken from: https://stackoverflow.com/questions/5849800/what-is-the-python-equivalent-of-matlabs-tic-and-toc-functions
import time
def TicTocGenerator():
    # Generator that returns time differences
    ti = 0           # initial time
    tf = time.time() # final time
    while True:
        ti = tf
        tf = time.time()
        yield tf-ti # returns the time difference

TicToc = TicTocGenerator() # create an instance of the TicTocGen generator
# This will be the main function through which we define both tic() and toc()
def toc(msg=None, dsp=True):
    # Prints the time difference yielded by generator instance TicToc
    tempTimeInterval = next(TicToc)
    if dsp:
        if msg is None: print('Elapsed time: %f seconds.\n' %tempTimeInterval, sep='')
        else:           print(msg, ': %f seconds.\n' %tempTimeInterval, sep='')
    return tempTimeInterval

def tic(msg=None):
    # Records a time in TicToc, marks the beginning of a time interval
    if msg is not None: print(msg)
    toc(dsp=False)

TicToc1 = TicTocGenerator() # create another instance of the TicTocGen generator
def toc1(msg=None, dsp=True):
    tempTimeInterval = next(TicToc1)
    if dsp:
        if msg is None: print('Elapsed time: %f seconds.\n' % tempTimeInterval, sep='')
        else:           print(msg, ': %f seconds.\n' % tempTimeInterval, sep='')
    return tempTimeInterval
def tic1(msg=None):
    if msg is not None: print(msg)
    toc1(dsp=False)

TicToc2 = TicTocGenerator() # create another instance of the TicTocGen generator
def toc2(msg=None, dsp=True):
    tempTimeInterval = next(TicToc2)
    if dsp:
        if msg is None: print('Elapsed time: %f seconds.\n' % tempTimeInterval, sep='')
        else:           print(msg, ': %f seconds.\n' % tempTimeInterval, sep='')
    return tempTimeInterval
def tic2(msg=None):
    if msg is not None: print(msg)
    toc2(dsp=False)

TicToc3 = TicTocGenerator() # create another instance of the TicTocGen generator
def toc3(msg=None, dsp=True):
    tempTimeInterval = next(TicToc3)
    if dsp:
        if msg is None: print('Elapsed time: %f seconds.\n' % tempTimeInterval, sep='')
        else:           print(msg, ': %f seconds.\n' % tempTimeInterval, sep='')
    return tempTimeInterval
def tic3(msg=None):
    if msg is not None: print(msg)
    toc3(dsp=False)

TicToc4 = TicTocGenerator() # create another instance of the TicTocGen generator
def toc4(msg=None, dsp=True):
    tempTimeInterval = next(TicToc4)
    if dsp:
        if msg is None: print('Elapsed time: %f seconds.\n' % tempTimeInterval, sep='')
        else:           print(msg, ': %f seconds.\n' % tempTimeInterval, sep='')
    return tempTimeInterval
def tic4(msg=None):
    if msg is not None: print(msg)
    toc4(dsp=False)

TicToc5 = TicTocGenerator() # create another instance of the TicTocGen generator
def toc5(msg=None, dsp=True):
    tempTimeInterval = next(TicToc5)
    if dsp:
        if msg is None: print('Elapsed time: %f seconds.\n' % tempTimeInterval, sep='')
        else:           print(msg, ': %f seconds.\n' % tempTimeInterval, sep='')
    return tempTimeInterval
def tic5(msg=None):
    if msg is not None: print(msg)
    toc5(dsp=False)
##############################################################################

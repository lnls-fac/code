"""
InteractivePlot
    Interactive plot for debugging. 

Afonso Haruo Carnielli Mukai (FAC - LNLS)

2013-12-17: v0.1
"""

import multiprocessing
import mmap
import InteractivePlotServer


_SHM_LENGTH = 10


class Plot(object):
    
    def __init__(self, window_title='Plot'):
        self.shm = mmap.mmap(fileno=-1, length=_SHM_LENGTH)
        self.conn, conn2 = multiprocessing.Pipe(duplex=True)
        
        args = (self.shm, conn2, window_title)
        process = multiprocessing.Process(target=InteractivePlotServer.start,
                                          args=args)
        process.start()
    
    def plot(self, x=None, y=None,
             color='blue',
             line_style='-',
             line_width='1.0',
             marker='None'):
        
        # If only y is supplied, build x as indices
        if x == None:
            x = range(len(y))
        
        # Set shared memory
        
        # Send command


if __name__ == '__main__':
    p = Plot()

import math
import numpy as np

def polyfit(x,y,monomials):
    X = np.zeros((len(x),len(monomials)))
    N = np.zeros((len(x),len(monomials)))
    for i in range(X.shape[1]):
        X[:,i] = x
        N[:,i] = monomials[i]
    XN = X ** N
    y_ = np.zeros((len(y), 1))
    y_[:,0] = y
    XNt = np.transpose(XN) 
    b =  np.dot(XNt,y_)
    X =  np.dot(XNt, XN)
    r = np.linalg.lstsq(X, b)
    return r[0][:,0]
        
        
        
    
    
# pi = math.pi
# 
# def sin(x):
#     
#     if type(x) is numpy.ndarray:
#         return numpy.sin(x)
#     else:
#         return math.sin(x)
#     
# def cos(x):
#     
#     if type(x) is numpy.ndarray:
#         return numpy.cos(x)
#     else:
#         return math.cos(x)
#     
# def tan(x):
#     
#     if type(x) is numpy.ndarray:
#         return numpy.tan(x)
#     else:
#         return math.tan(x)


    
    
    
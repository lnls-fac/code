import math
import numpy as np
import matplotlib.pyplot as plt

def polyfit(x,y,monomials, algorithm='lstsq'):
    
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
    
    if algorithm is 'lstsq':
        r      = np.linalg.lstsq(X,b)
        coeffs = r[0][:,0]
    else:
        r       = np.linalg.solve(X,b)
        coeffs  = r[:,0]

    # finds maximum diff and its base value        
    y_fitted   = np.dot(XN, coeffs)
    y_diff     = abs(y_fitted - y_[:,0])
    max_error  = max(y_diff)
    idx        = [i for i,value in enumerate(y_diff) if value == max_error]
    base_value = y_[idx[0],0] 

    return (coeffs, (max_error,base_value))
    
    
    
import math
import numpy

pi = math.pi

def sin(x):
    
    if type(x) is numpy.ndarray:
        return numpy.sin(x)
    else:
        return math.sin(x)
    
def cos(x):
    
    if type(x) is numpy.ndarray:
        return numpy.cos(x)
    else:
        return math.cos(x)

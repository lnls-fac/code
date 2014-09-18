#!/usr/bin/env python3 

import fieldmap

fname = 'fieldmap.txt'
fm = fieldmap.FieldMap(fname, 
                       analysis_missing_field = True, 
                       polyfit_exponents = [2,3,4,5,6,7,8],
                       threshold_field_fraction = 0.1)

bx, by, bx = fm.interpolate(0,0,3000)

print(fm)
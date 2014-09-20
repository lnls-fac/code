#!/usr/bin/env python3 

import sys
import fieldmap as fmap


def run(file_name):
    
    # loads fieldmap from file
    fm = fmap.FieldMap(file_name)
    
    # calculates missing integrals
    fm.field_extrapolation_analysis(threshold_field_fraction = 0.3, 
                                    polyfit_exponents = [2,3,4,5,6,7,8,9,10])
    
    # prints basic information
    print('DIPOLE ANALYSIS')
    print('===============')
    print(fm)
    fm.clear_extrapolation_coefficients()
  
  
if __name__ == "__main__":
    
    argv = sys.argv
    run(argv[1])
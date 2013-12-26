#!/usr/bin/python

from distutils.core import setup, Extension

module1 = Extension('fieldmapcpp', 
            sources = [ 
            'fieldmapcpp.cpp',
            # module aux. functions
            'fieldmapcpp_read_pos.cpp',
            # module functionalities
            'fieldmapcpp_load_fieldmap.cpp',
            'fieldmapcpp_unload_fieldmap.cpp',
            'fieldmapcpp_interpolate_fieldmap.cpp',
            'fieldmapcpp_nr_fieldmaps.cpp',
            'fieldmapcpp_clear.cpp',
            # trackc++
            '../../../../fieldmap/API.cpp',
            '../../../../fieldmap/FieldMap.cpp',
            '../../../../fieldmap/odeint.cpp',
            '../../../../fieldmap/load_fieldmap.cpp',
            '../../../../fieldmap/interpolate_fieldmap.cpp',
            '../../../../fieldmap/nr_fieldmaps.cpp',
            '../../../../fieldmap/clear.cpp',
            ],
            language = "c++",
            #extra_compile_args = ["-std=c++11"],
           )

setup (name        = 'fieldmapcpp',
       version     = '1.0',
       description = 'This a module for loading and interpolating on fieldmaps. It also does runge-kutta integration.',
       ext_modules = [module1])

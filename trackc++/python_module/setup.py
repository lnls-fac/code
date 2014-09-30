#!/usr/bin/python

from distutils.core import setup, Extension

module1 = Extension('trackc++', 
            sources = [ 
            'trackcpp.cpp',
            # module aux. functions
            'trackcpp_read_particles.cpp',
            'trackcpp_read_lattice.cpp',
            'trackcpp_read_accelerator.cpp',
            # module functionalities
            'trackcpp_linepass.cpp',
            'trackcpp_ringpass.cpp',
            'trackcpp_findm66.cpp',
            # trackc++
            '../elements.cpp',
            '../lattice.cpp',
            '../passmethods.cpp',
            '../tracking.cpp',
            ],
            language = "c++",
            extra_compile_args = ["-std=c++11"],
           )

setup (name        = 'trackc++',
       version     = '1.0',
       description = 'This a module for efficiently tracking charged particles in transport lines and in storage rings',
       ext_modules = [module1])

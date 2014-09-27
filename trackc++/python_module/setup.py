#!/usr/bin/python

from distutils.core import setup, Extension

module1 = Extension('trackc++', 
            sources = [ 
            'trackc++.cpp',
            # module aux. functions
            'trackc++_read_particles.cpp',
            'trackc++_read_lattice.cpp',
            # module functionalities
            'trackc++_linepass.cpp',
            'trackc++_ringpass.cpp',
            'trackc++_findm66.cpp',
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

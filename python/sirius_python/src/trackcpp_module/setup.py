#!/usr/bin/python

from distutils.core import setup, Extension

module1 = Extension('trackcpp', 
            sources = [ 
            'trackcpp.cpp',
            # module aux. functions
            'trackcpp_read_particles.cpp',
            'trackcpp_read_lattice.cpp',
            # module functionalities
            'trackcpp_track1turn.cpp',
            # trackc++
            '../../../trackc++/elements.cpp',
            '../../../trackc++/lattice.cpp',
            '../../../trackc++/passmethods.cpp',
            '../../../trackc++/tracking.cpp',
            ]
           )

setup (name        = 'trackcpp',
       version     = '1.0',
       description = 'This a module for efficiently tracking charged particles in transport lines and in storage rings',
       ext_modules = [module1])
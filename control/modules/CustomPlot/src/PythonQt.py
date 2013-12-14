"""
PythonQt
    Select between PyQt4 and PySide.
    
    If the environment variable PYTHON_QT is set to PySide, use PySide;
    otherwise, use PyQt4.

Afonso Haruo Carnielli Mukai (FAC - LNLS)

2013-12-13: v0.1
"""

import os


PYTHON_QT = 'PYTHON_QT'
env = os.environ
if PYTHON_QT in env:
    python_qt = env[PYTHON_QT]
    if python_qt == 'PySide':
        from PySide import *
else:
    from PyQt4 import *

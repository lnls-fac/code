#!/usr/bin/env python3

import pyaccel as _pyaccel
import sirius as _sirius
import sys as _sys

_the_ring = _sirius.SI_V07.create_accelerator()

_result = {True:'passed.', False:'FAILED!'}

class TestSuiteException(Exception):
    pass

def _printresult(msg, flag):
    print('   ' + msg + ' test ... ', end='')
    print(_result[flag])
    if not flag:
        raise TestSuiteException('test failed')

def _float_comparison(f1,f2,tol):
    diff = f1 - f2
    return diff < tol

def run_test_suite(msg, suite):
    try:
        print('-- ' + msg)
        suite()
        print()
    except TestSuiteException:
        _sys.exit(-1)

def accelerator_creation():

    _printresult('accelerator energy', _the_ring.energy == 3e9)
    _printresult('accelerator harmonic number', _the_ring.harmonic_number == 864)
    _printresult('accelerator cavity_on', _the_ring.cavity_on == False)
    _printresult('accelerator radiation_on', _the_ring.radiation_on == False)
    _printresult('accelerator vchamber_on', _the_ring.vchamber_on == False)
    _printresult('accelerator number of elements', len(_the_ring) == 3279)
    _printresult('accelerator length', _float_comparison(_the_ring.length, 518.398, 1e-10))

def findspos():

    r = _pyaccel.lattice.findspos()

if __name__ == '__main__':

    run_test_suite('accelerator creation suite', accelerator_creation)

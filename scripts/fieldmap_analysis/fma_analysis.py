#!/usr/bin/env python3 

import os
import sys


def help():

    print('NAME')
    print('       fma_analys.py - drive routine used to perform analysis of field maps from 3D magnet models.')
    print()
    print('SYNOPSIS')
    print('       fma_analysis.py [COMMAND]')
    print()
    print('DESCRIPTION')
    print('       Accepts commands (single argument) that specify what type of action to do.')
    print('       Valid commands are (uselly invoked in order):')
    print()
    print('       help')
    print('              prints this text')
    print()
    print('       clean')
    print('              cleans all output files in current directory')
    print()
    print('       edit')
    print('              open gedit and edit input files')
    print()
    print('       run')
    print('              run the complete analysis')
    print()
    print('       summary')
    print('              prints summary of resultas and plots analysis results')
    print()

def edit():

    os.system('gedit -s rawfield.in trajectory.in multipoles.in model.in &')

def clean():

    os.system('rm -rf *.out *.txt *.pdf *.pkl')

def run():

    print('1/6 - cleaning directory...'), os.system('./fma_analysis.py clean')
    print('2/6 - rawfield analysis...'), os.system('./fma_rawfield.py > rawfield.out')
    print('3/6 - trajectory calculation...'), os.system('./fma_trajectory.py > trajectory.out')
    print('4/6 - multipoles calculation...'), os.system('./fma_multipoles.py > multipoles.out')
    print('5/6 - model creation...'), os.system('./fma_model.py > model.out')
    print('6/6 - analysis summary and visualization...'), summary()

def summary():

    ''' reads and prints summary '''
    try:
        with open('rawfield.out', 'r') as fp:
            content = fp.read()
        print(content)
    except:
        pass
    try:
        with open('trajectory.out', 'r') as fp:
            content = fp.read()
        print(content)
    except:
        pass
    try:
        with open('multipoles.out', 'r') as fp:
            content = fp.read()
        print(content)
    except:
        pass
    try:
        with open('model.out', 'r') as fp:
            content = fp.read()
        print(content)
    except:
        pass


    ''' unites all pdf figs '''
    try:
        os.system('ls *fig*.pdf 1> /dev/null 2> /dev/null && rm -rf analysis.pdf')
        os.system('ls *fig*.pdf 1> /dev/null 2> /dev/null && pdfunite *.pdf analysis.pdf')
        os.system('rm -rf *fig*.pdf')    
    except:
        pass


    ''' shows summary figure '''
    try:
        os.system('okular analysis.pdf 2> /dev/null')
    except:
        pass


if len(sys.argv) != 2:
    help()
if sys.argv[1] == 'help':
    help()
if sys.argv[1] == 'clean':
    clean()
if sys.argv[1] == 'run':
    run()
if sys.argv[1] == 'edit':
    edit()


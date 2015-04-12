#!/bin/bash

cd $FACCODE/trackc++; make all -j && make install
cd $FACCODE/trackc++/python_swig_module; make all -j && make install


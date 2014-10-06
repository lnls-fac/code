#!/bin/bash

rm -rf build
python setup.py build
python setup.py install --record create_module_log.txt

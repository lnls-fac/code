#!/usr/bin/env python3

import unittest
import testelements


suite_list = []
suite_list.append(testelements.get_suite())

tests = unittest.TestSuite(suite_list)
unittest.TextTestRunner(verbosity=2).run(tests)


import unittest
import numpy
import pyaccel
import trackcpp

import sirius

class TestTracking(unittest.TestCase):

    def setUp(self):
        self.the_ring = sirius.SI_V07.create_accelerator()

    def tearDown(self):
        pass

    def test_elementpass(self):
        self.assertEqual(self.the_ring.energy, 3e9)


def tracking_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTracking)
    return suite


def get_suite():
    suite_list = []
    suite_list.append(tracking_suite())
    return unittest.TestSuite(suite_list)

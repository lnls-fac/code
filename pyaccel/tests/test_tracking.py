
import unittest
import numpy
import pyaccel
import trackcpp

import sirius

class TestTracking(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_elementpass(self):

        accelerator = {'energy':sirius.SI_V07.energy,
                       'harmonic_number':sirius.SI_V07.harmonic_number,
                       'cavity_on':sirius.SI_V07.default_cavity_on,
                       'radiation_on':sirius.SI_V07.default_radiation_on,
                       'vchamber_on':sirius.SI_V07.default_vchamber_on}

        # tracks one particle through a quadrupole
        q = pyaccel.elements.quadrupole(fam_name='q', length=1.0, K=2.0)
        r = pyaccel.tracking.elementpass(element=q, pos=[0.001,0,0,0,0,0], **accelerator)
        self.assertAlmostEqual(sum(r), -0.00124045591936, places=12)

        # tracks two particles (lists) through a sextupole
        s = pyaccel.elements.sextupole(fam_name='s', length=1.0, S=2.0)
        r = pyaccel.tracking.elementpass(element=s, pos=[[0.001,0,0,0,0,0],[0,0,0.001,0,0,0]], **accelerator)
        self.assertAlmostEqual(sum(r[:,0])+sum(r[:,1]),0.0020000033337366449, places=12)

        # tracks one particle through a bending magnet with radiation on
        b = pyaccel.elements.rbend(fam_name='b', length=0.1, angle=0.1, K=0.2)
        accelerator['radiation_on'] = True
        r = pyaccel.tracking.elementpass(element=s, pos=[0.001,0.001,0.002,0.002,0.003,0.003], **accelerator)
        self.assertAlmostEqual(sum(r), 0.015038971318609795, places=12)


def tracking_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTracking)
    return suite


def get_suite():
    suite_list = []
    suite_list.append(tracking_suite())
    return unittest.TestSuite(suite_list)

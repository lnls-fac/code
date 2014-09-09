#!/usr/bin/env python3

import unittest
import numpy
import calcemit
import model
import testlinac


class TestCalcEmit(unittest.TestCase):

    def setUp(self):
        sigma_11 = 40e-9
        sigma_12 = 5e-9
        sigma_22 = 60e-9

        sigma_0 = numpy.array([[sigma_11, sigma_12], [sigma_12, sigma_22]])
        self.emit = numpy.sqrt(numpy.linalg.det(sigma_0))

        k = numpy.linspace(-0.8, -0.3, 50)

        m = model.Model(testlinac.element_list())
        q_idx = 0

        k_orig = m.elements[q_idx].k
        measured_beam_size = []
        for x in k:
            quadrupole = m.elements[q_idx].k = x
            r = m.matrix()
            sigma_out = r.dot(sigma_0).dot(r.transpose())
            measured_beam_size.append(numpy.sqrt(sigma_out[0, 0]))
        m.elements[q_idx].k = k_orig

        self.result = calcemit.calc_emit(m, q_idx, k, measured_beam_size)

    def test_calc_emit(self):
        calculated_emit = self.result[0]
        self.assertAlmostEqual(calculated_emit, self.emit, places=11,
                               msg="wrong value for calculated emittance")

    def test_calc_emit_error(self):
        calculated_emit_error = self.result[1]
        self.assertAlmostEqual(calculated_emit_error, 0.0, places=11,
                               msg="calculated emittance error too large")


def calc_emit_suite():
     suite = unittest.TestLoader().loadTestsFromTestCase(TestCalcEmit)
     return suite


def suite():
    suite_list = []
    suite_list.append(calc_emit_suite())
    return unittest.TestSuite(suite_list)

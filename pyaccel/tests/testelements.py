
import unittest
import numpy
import pyaccel
import trackcpp


class TestElement(unittest.TestCase):

    def setUp(self):
        self.element = pyaccel.elements.Element()

    def test_attributes(self):
        attributes = [
                'fam_name',
                'pass_method',
                'length',
                'nr_steps',
                'hkick',
                'vkick',
                'angle',
                'angle_in',
                'angle_out',
                'gap',
                'fint_in',
                'fint_out',
                'thin_KL',
                'thin_SL',
                'frequency',
                'voltage',
                'kicktable',
                'hmax',
                'vmax',
                'polynom_a',
                'polynom_b',
                't_in',
                't_out',
                'r_in',
                'r_out'
        ]

        for a in attributes:
            r = hasattr(self.element, a)
            self.assertTrue(r, "attribute '" + a + "' not found")

    def test_default_init(self):
        self.assertEqual(self.element.fam_name, "")
        self.assertEqual(self.element.length, 0.0)

    def test_array_sizes(self):
        self.assertEqual(len(self.element.t_in), 6)
        self.assertEqual(len(self.element.t_out), 6)
        self.assertEqual(self.element.r_in.shape, (6, 6))
        self.assertEqual(self.element.r_out.shape, (6, 6))

    def test_t_in_out(self):
        # Set entire vector
        t = [6.0, 5.0, 4.0, 3.0, 2.0, 1.0]
        self.element.t_in = t
        for i in range(len(t)):
            self.assertAlmostEqual(self.element.t_in[i], t[i])

        # Set single element
        self.element.t_in[0] = -10.0
        self.assertAlmostEqual(self.element.t_in[0], -10.0)

        # Set list of indices
        self.element.t_out[[1, 3, 5]] = [1.0, 3.0, 5.0]
        self.assertAlmostEqual(self.element.t_out[1], 1.0)
        self.assertAlmostEqual(self.element.t_out[3], 3.0)
        self.assertAlmostEqual(self.element.t_out[5], 5.0)

        # Set slice
        self.element.t_out[3:] = [-1.0, -2.0, -3.0]
        self.assertAlmostEqual(self.element.t_out[3], -1.0)
        self.assertAlmostEqual(self.element.t_out[4], -2.0)
        self.assertAlmostEqual(self.element.t_out[5], -3.0)

    def test_r_in_out(self):
        # Set entire matrix
        r = numpy.random.normal(size=(6, 6))
        self.element.r_in = r

        for i in range(r.shape[0]):
            for j in range(r.shape[1]):
                self.assertAlmostEqual(self.element.r_in[i, j], r[i, j])

        # Set single element
        self.element.r_in[2, 5] = -10.0
        self.assertAlmostEqual(self.element.t_in[2, 5], -10.0)

        # # Set list of indices
        # self.element.t_out[[1, 3, 5]] = [1.0, 3.0, 5.0]
        # self.assertAlmostEqual(self.element.t_out[1], 1.0)
        # self.assertAlmostEqual(self.element.t_out[3], 3.0)
        # self.assertAlmostEqual(self.element.t_out[5], 5.0)
        #
        # # Set slice
        # self.element.t_out[3:] = [-1.0, -2.0, -3.0]
        # self.assertAlmostEqual(self.element.t_out[3], -1.0)
        # self.assertAlmostEqual(self.element.t_out[4], -2.0)
        # self.assertAlmostEqual(self.element.t_out[5], -3.0)


def element_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestElement)
    return suite


def get_suite():
    suite_list = []
    suite_list.append(element_suite())
    return unittest.TestSuite(suite_list)

#!/usr/bin/env python3

import numpy
import numpy.linalg


def calc_emit(model, quadrupole_idx, k, measured_beam_size):
    sigma_out_11 = numpy.power(measured_beam_size, 2)

    r = []
    for x in k:
        model.elements[quadrupole_idx].k = x
        matrix = model.matrix()
        r_1 = matrix[0, 0]**2
        r_2 = 2*matrix[0, 0]*matrix[0, 1]
        r_3 = matrix[0, 1]**2
        r.append([r_1, r_2, r_3])
    r = numpy.array(r)

    u, s, v = numpy.linalg.svd(r, full_matrices=False)

    r_inv = v.transpose().dot(numpy.diag(1/s)).dot(u.transpose())
    sigma_vec = r_inv.dot(sigma_out_11)

    sigma_in = numpy.array([[sigma_vec[0], sigma_vec[1]],
                            [sigma_vec[1], sigma_vec[2]]])

    emit = numpy.sqrt(numpy.linalg.det(sigma_in))

    return (emit, 1.0)

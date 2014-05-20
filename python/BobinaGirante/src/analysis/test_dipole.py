import numpy
import rotcoil
import matplotlib.pyplot as plt

default_r0             = 17.5/1000  # [m]
default_harmonics      = [1,2,3,4,5,6,7]
default_plot_label     = 'multipoles'

''' SPECS '''
''' ----- '''
def test_dipole_multipole_model(integration_type = 'integrated_rotated_coil_length'):
    
    harmonics       = [1,2,3,4,5,6,7,8,9,10]
    if integration_type == 'integrated_rotated_coil_length':
        ''' longitudinally integrated in rotating coil length (836 mm)'''
        absolute_LN_avg = 2.37355e-2 # [T.m]  
        relative_LN_avg = [1,2.265e-2,-1.547e-2,9.660e-4,3.940e-3,-2.718e-3,9.328e-4,-1.886e-4,2.163e-5,-1.113e-6]
    elif integration_type == 'integrated_total_length':
        ''' longitudinally integrated in total 3D model length (1600 mm)'''
        absolute_LN_avg = 2.39522e-2 # [T.m]  
        relative_LN_avg = [1,2.244e-2,-1.533e-2,9.567e-4,3.904e-3,-2.694e-3,9.243e-4,-1.869e-4,2.143e-5,-1.103e-6]
    else:
        Exception('invalid integrated type')

    relative_LS_avg = [0] * 10
    relative_LN_std = [0] * 10
    relative_LS_std = [0] * 10
    m = rotcoil.multipoles(harmonics = harmonics, r0 = default_r0,  
                           relative_LN_avg = relative_LN_avg,
                           relative_LS_avg = relative_LS_avg,
                           relative_LN_std = relative_LN_std,
                           relative_LS_std = relative_LS_std,
                           )
    m.main_multipole = (1,absolute_LN_avg)
    m.calc_absolute_multipoles()
    return m


def reconstruct_field_rolloff(data, x = None):
    
    if x is None:
        x = numpy.linspace(0,17.5/1000,50)
        
    nrpts = len(data)
    #main_multipole = data[0].main_multipole

    field = numpy.zeros((nrpts,len(x)))
    for i in range(nrpts):
        harms = data[i].harmonics
        for j in range(len(x)):
            for k in range(len(harms)):
                field[i,j] += data[i].absolute_LN_avg[k] * (x[j] ** (harms[k]-1.0))
        plt.plot(x, field[i,:])
        plt.show()
        plt.close() 
           
             
                

def test_dipole_repetibility(folder,
                             harmonics = default_harmonics,
                             r0 = default_r0,                                  
                             plot_label = 'TEST_DIPOLE',
                             ymin_multipoles = 1e-6,
                             ymin_skew_angle = 1e-2,
                             legend = None,
                             plot_normal_multipoles_flag = True, 
                             plot_skew_multipoles_flag = True,
                             plot_skew_angle_flag = True):
    """ loads measurement test dipole data and does repetibility analysis """
    
    ''' loads rotating coil data from folder '''
    measurements    = rotcoil.read_measurements_from_folder(folder = folder)
    ''' creates 'multipole' objects '''
    multipole       = rotcoil.multipoles(measurements[0], harmonics = harmonics, r0 = r0)
    ''' defines normal quadrupole of first data file as main multipole for normalization '''
    main_multipole  = multipole.select_main_multipole(1)
    ''' does multipolar analysis on raw data '''
    multipoles      = rotcoil.calc_multipoles_from_measurements(measurements, harmonics, r0, main_multipole = main_multipole)
    ''' loads multipoles from simulations '''
    multipoles      = [test_dipole_multipole_model(integration_type = 'integrated_rotated_coil_length')] + multipoles
    multipoles[0].calc_relative_multipoles(main_multipole = main_multipole)
    
 
    #reconstruct_field_rolloff(multipoles)
    
    if plot_normal_multipoles_flag or plot_skew_multipoles_flag:
        rotcoil.bar_plot_multipoles_repetibility(multipoles, harmonics = harmonics, r0 = r0,                                  
                                                 plot_label = plot_label, ymin = ymin_multipoles, legend = legend,
                                                 plot_normal_multipoles_flag = plot_normal_multipoles_flag, 
                                                 plot_skew_multipoles_flag = plot_skew_multipoles_flag,
                                                 plot_skew_angle_flag = False,
                                                 base_bar = True)
    if plot_skew_angle_flag:
        rotcoil.bar_plot_multipoles_repetibility(multipoles[1:], harmonics = harmonics, r0 = r0,                                  
                                                 plot_label = plot_label, ymin = ymin_skew_angle, legend = legend,
                                                 plot_normal_multipoles_flag = False, 
                                                 plot_skew_multipoles_flag = False,
                                                 plot_skew_angle_flag = plot_skew_angle_flag,
                                                 base_bar = False)
        
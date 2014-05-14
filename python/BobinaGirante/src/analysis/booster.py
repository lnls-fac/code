import rotcoil

default_energy         = 3.0        # [GeV]
default_r0             = 17.5/1000  # [m]
default_harmonics      = [1,2,3,4,5,6,7]
default_quad_harmonics = [1,2,3,4,5,6,7,8,9,10,14]

default_plot_label = 'multipoles'


def quadrupole_multipole_specs():
    
    harmonics       = [2,3,4,5,6,7,8,9,10,14]
    relative_LN_avg = [1,0,0,0,-1e-3,0,0,0,1.1e-3,8e-5]
    relative_LN_std = [0,7e-4,4e-4,4e-4,4e-4,4e-4,4e-4,4e-4,4e-4,4e-4]
    relative_LS_avg = [0,0,0,0,0,0,0,0,0,0]
    relative_LS_std = [0,1e-4,5e-4,1e-4,1e-4,1e-4,1e-4,1e-4,1e-4,1e-4]
    m = rotcoil.multipoles(                        
                 harmonics = harmonics,  
                 r0 = default_r0, 
                 #main_multipole = (2,max_quad_strength * brho), 
                 relative_LN_avg = relative_LN_avg,
                 relative_LS_avg = relative_LS_avg,
                 relative_LN_std = relative_LN_std,
                 relative_LS_std = relative_LS_std,
                 )
    return m
    
                 
    
def plot_multipoles_repetibility(folder,
                                 main_harmonic,
                                 spec_multipoles = None,
                                 harmonics = default_harmonics,
                                 r0 = default_r0,                                  
                                 plot_label = default_plot_label,
                                 ymin = 1e-6,
                                 colors = None,
                                 alpha_blending = 0.6,
                                 legend = None,
                                 display_plot = True):
    
    data = rotcoil.read_folder(folder)
    if spec_multipoles is None:
        multipoles = []
    else:
        multipoles = [spec_multipoles]
    main_multipole = None
    for d in data:
        m = rotcoil.multipoles(measurement = d, harmonics = harmonics)
        m.calc_absolute_multipoles()
        if main_multipole is None:
            main_multipole = m.select_main_multipole(main_harmonic)
        m.calc_relative_multipoles(r0 = r0, main_multipole = main_multipole)
        multipoles.append(m)

    rotcoil.plot_normal_multipoles(multipoles, plot_label = plot_label, harmonics = harmonics, 
                                   ymin = ymin, colors = colors, alpha_blending = alpha_blending, legend = legend, 
                                   display_plot = display_plot)
    
def test_dipole_repetibility(folder,
                             harmonics = default_harmonics,
                             r0 = default_r0,                                  
                             plot_label = 'TEST_DIPOLE',
                             ymin = 1e-6,
                             colors = None,
                             alpha_blending = 0.6,
                             legend = None,
                             display_plot = True):
    plot_multipoles_repetibility(folder, main_harmonic = 1, harmonics = default_harmonics, r0 = default_r0,                                  
                                 plot_label = plot_label, ymin = 1e-6, colors = None, alpha_blending = 0.6, legend = None, display_plot = True)
    
def quadrupoles_repetibility(folder,
                             harmonics = default_quad_harmonics,
                             r0 = default_r0,                                  
                             plot_label = 'QUADRUPOLES',
                             ymin = 1e-6,
                             colors = None,
                             alpha_blending = 0.6,
                             legend = None,
                             display_plot = True):
    
    spec_multipoles = quadrupole_multipole_specs()
    
    plot_multipoles_repetibility(folder, spec_multipoles = spec_multipoles, main_harmonic = 2, harmonics = harmonics, r0 = default_r0,                                  
                                 plot_label = plot_label, ymin = ymin, colors = None, alpha_blending = 0.6, legend = None, display_plot = True)
    
    
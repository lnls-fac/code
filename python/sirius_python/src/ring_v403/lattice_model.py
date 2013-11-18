import mathphysicslibs.constants as consts
import mathphysicslibs.functions as mfuncs
from   pyring.elements import *
import pyring.lattice as lattice
from   set_magnet_strength_ac10 import *
from   lattice_parameters import *

def create_lattice(mode = 'AC10', energy = 3e9):
    
    #harmonic_number = 864
    
    #%% passmethods
    #%  ===========
    
    drif_pass_method = PassMethods.pm_drift_pass
    bend_pass_method = PassMethods.pm_bnd_mpole_symplectic4_pass
    quad_pass_method = PassMethods.pm_str_mpole_symplectic4_pass
    sext_pass_method = PassMethods.pm_str_mpole_symplectic4_pass
    mark_pass_method = PassMethods.pm_identity_pass
    corr_pass_method = PassMethods.pm_corrector_pass

    #%% elements
    #%  ========


    #% --- drift spaces ---

    id_length = 2.0 # % [m]

    #dia      = drift(fam_name = 'dia', length = 3.269200, pass_method = drif_pass_method)
    dia1     = drift(fam_name = 'dia', length = id_length/2, pass_method = drif_pass_method)
    dia2     = drift(fam_name = 'dia', length = 3.26920-id_length/2, pass_method = drif_pass_method)
    #dib      = drift(fam_name = 'dib', length = 2.909200, pass_method = drif_pass_method)
    dib1     = drift(fam_name = 'dib', length = id_length/2, pass_method = drif_pass_method)
    dib2     = drift(fam_name = 'dib', length = 2.909200-id_length/2, pass_method = drif_pass_method)
    d10      = drift(fam_name = 'd10', length = 0.100000, pass_method = drif_pass_method)
    d11      = drift(fam_name = 'd11', length = 0.110000, pass_method = drif_pass_method)
    d12      = drift(fam_name = 'd12', length = 0.120000, pass_method = drif_pass_method)
    d13      = drift(fam_name = 'd13', length = 0.130000, pass_method = drif_pass_method)
    d15      = drift(fam_name = 'd15', length = 0.150000, pass_method = drif_pass_method)
    d17      = drift(fam_name = 'd17', length = 0.170000, pass_method = drif_pass_method)
    d18      = drift(fam_name = 'd18', length = 0.180000, pass_method = drif_pass_method)
    d20      = drift(fam_name = 'd20', length = 0.200000, pass_method = drif_pass_method)
    d22      = drift(fam_name = 'd22', length = 0.220000, pass_method = drif_pass_method)
    d23      = drift(fam_name = 'd23', length = 0.230000, pass_method = drif_pass_method)
    d26      = drift(fam_name = 'd26', length = 0.260000, pass_method = drif_pass_method)
    d32      = drift(fam_name = 'd32', length = 0.320000, pass_method = drif_pass_method)
    d44      = drift(fam_name = 'd44', length = 0.440000, pass_method = drif_pass_method)

    #% --- markers ---
    mc       = marker(fam_name = 'mc',      pass_method = mark_pass_method)
    mia      = marker(fam_name = 'mia',     pass_method = mark_pass_method)
    mib      = marker(fam_name = 'mib',     pass_method = mark_pass_method)
    mb1      = marker(fam_name = 'mb1',     pass_method = mark_pass_method)
    mb2      = marker(fam_name = 'mb2',     pass_method = mark_pass_method)
    mb3      = marker(fam_name = 'mb3',     pass_method = mark_pass_method)
    inicio   = marker(fam_name = 'inicio',  pass_method = mark_pass_method)
    fim      = marker(fam_name = 'fim',     pass_method = mark_pass_method)
    mid      = marker(fam_name = 'id_end',  pass_method = mark_pass_method)

    #% --- beam position monitors ---
    mon      = marker(fam_name = 'BPM', pass_method = mark_pass_method)

    #% --- quadrupoles ---
    qaf      = quadrupole(fam_name = 'qaf',  length = 0.340000, k = qaf_strength,  pass_method = quad_pass_method)
    qad      = quadrupole(fam_name = 'qad',  length = 0.140000, k = qad_strength,  pass_method = quad_pass_method)
    qbd2     = quadrupole(fam_name = 'qbd2', length = 0.140000, k = qbd2_strength, pass_method = quad_pass_method)
    qbf      = quadrupole(fam_name = 'qbf',  length = 0.340000, k = qbf_strength,  pass_method = quad_pass_method)
    qbd1     = quadrupole(fam_name = 'qbd1', length = 0.140000, k = qbd1_strength, pass_method = quad_pass_method)
    qf1      = quadrupole(fam_name = 'qf1',  length = 0.250000, k = qf1_strength,  pass_method = quad_pass_method)
    qf2      = quadrupole(fam_name = 'qf2',  length = 0.250000, k = qf2_strength,  pass_method = quad_pass_method)
    qf3      = quadrupole(fam_name = 'qf3',  length = 0.250000, k = qf3_strength,  pass_method = quad_pass_method)
    qf4      = quadrupole(fam_name = 'qf4',  length = 0.250000, k = qf4_strength,  pass_method = quad_pass_method)

    #% --- bending magnets --- 
    deg_2_rad = (mfuncs.pi/180.0)


    #% -- b1 --
    dip_nam =  'b1'
    dip_len =  0.828080
    dip_ang =  2.766540 * deg_2_rad
    dip_K   = -0.78
    dip_S   =  0
    h1      = rbend(fam_name = dip_nam, length = dip_len/2, angle = dip_ang/2, angle_in = 1*dip_ang/2, angle_out = 0*dip_ang/2, k = dip_K, s = dip_S, pass_method = bend_pass_method)                    
    h2      = rbend(fam_name = dip_nam, length = dip_len/2, angle = dip_ang/2, angle_in = 0*dip_ang/2, angle_out = 1*dip_ang/2, k = dip_K, s = dip_S, pass_method = bend_pass_method)                    
    B1      = [h1, mb1, h2]

    #% -- b2 --
    dip_nam =  'b2'
    dip_len =  1.228262
    dip_ang =  4.103510 * deg_2_rad
    dip_K   = -0.78
    dip_S   =  0.00
    h1      = rbend(fam_name = dip_nam, length = dip_len/2, angle = dip_ang/2, angle_in = 1*dip_ang/2, angle_out = 0*dip_ang/2, k = dip_K, s = dip_S, pass_method = bend_pass_method)                    
    h2      = rbend(fam_name = dip_nam, length = dip_len/2, angle = dip_ang/2, angle_in = 0*dip_ang/2, angle_out = 1*dip_ang/2, k = dip_K, s = dip_S, pass_method = bend_pass_method)
    B2      = [h1, mb2, h2]

    #% -- b3 --
    dip_nam =  'b3'
    dip_len =  0.428011
    dip_ang =  1.429950 * deg_2_rad
    dip_K   = -0.78
    dip_S   =  0.00
    h1      = rbend(fam_name = dip_nam, length = dip_len/2, angle = dip_ang/2, angle_in = 1*dip_ang/2, angle_out = 0*dip_ang/2, k = dip_K, s = dip_S, pass_method = bend_pass_method)                    
    h2      = rbend(fam_name = dip_nam, length = dip_len/2, angle = dip_ang/2, angle_in = 0*dip_ang/2, angle_out = 1*dip_ang/2, k = dip_K, s = dip_S, pass_method = bend_pass_method)
    B3      = [h1, mb3, h2]

    #% -- bc --
    dip_nam =  'bc'
    dip_len =  0.125394
    dip_ang =  1.4 * deg_2_rad
    dip_K   =  0.00
    dip_S   = -18.93
        
    bce      = rbend(fam_name = dip_nam, length = dip_len/2, angle = dip_ang/2, angle_in = 1*dip_ang/2, angle_out = 0*dip_ang/2, k = dip_K, s = dip_S, pass_method = bend_pass_method)                    
    bcs      = rbend(fam_name = dip_nam, length = dip_len/2, angle = dip_ang/2, angle_in = 0*dip_ang/2, angle_out = 1*dip_ang/2, k = dip_K, s = dip_S, pass_method = bend_pass_method)
    BC      = [bce, mc, bcs]


    #% --- correctors ---
    ch     = corrector(fam_name = 'hcm',  length = 0, kick_angle = [0, 0], pass_method = corr_pass_method)
    cv     = corrector(fam_name = 'vcm',  length = 0, kick_angle = [0, 0], pass_method = corr_pass_method)
    crhv   = corrector(fam_name = 'crhv', length = 0, kick_angle = [0,0], pass_method = corr_pass_method)


    #% --- sextupoles ---    
    sa1      = sextupole(fam_name = 'sa1', length = 0.150000, s = sa1_strength, pass_method = sext_pass_method)
    sa2      = sextupole(fam_name = 'sa2', length = 0.150000, s = sa2_strength, pass_method = sext_pass_method)
    sb1      = sextupole(fam_name = 'sb1', length = 0.150000, s = sb1_strength, pass_method = sext_pass_method)
    sb2      = sextupole(fam_name = 'sb2', length = 0.150000, s = sb2_strength, pass_method = sext_pass_method)
    sd1      = sextupole(fam_name = 'sd1', length = 0.150000, s = sd1_strength, pass_method = sext_pass_method)
    sf1      = sextupole(fam_name = 'sf1', length = 0.150000, s = sf1_strength, pass_method = sext_pass_method)
    sd2      = sextupole(fam_name = 'sd2', length = 0.150000, s = sd2_strength, pass_method = sext_pass_method)
    sd3      = sextupole(fam_name = 'sd3', length = 0.150000, s = sd3_strength, pass_method = sext_pass_method)
    sf2      = sextupole(fam_name = 'sf2', length = 0.150000, s = sf2_strength, pass_method = sext_pass_method)
           
    #% --- rf cavity ---
    cav = rfcavity(fam_name = 'cav', length = 0, energy = energy, voltage = 2.5e6, frequency = 500e6, harmonic_number = harmonic_number, pass_method = 'cavity_pass')
    

    #%% lines 
    
    insa   = [ dia1, mid, dia2, crhv, cv, d12, ch, d12, sa2, d12, mon, d12, qaf, d23, qad, d17, sa1, d17];
    insb   = [ dib1, mid, dib2, d10, crhv, qbd2, d12, cv, d12, ch, d12, sb2, d12, mon, d12, qbf, d23, qbd1, d17, sb1, d17];
    
    cline1 = [ d32, cv,  d12, ch,  d15, sd1, d17, qf1, d12, mon, d11, sf1, d20, qf2, d17, sd2, d12, ch, d10, mon, d10];
    cline2 = [ d18, cv,  d26, sd3, d17, qf3, d12, mon, d11, sf2, d20, qf4, d15, ch,  crhv, d12, mon, d44];
    cline3 = [ d44, mon, d12, ch,  d15, qf4, d20, sf2, d11, mon, d12, qf3, d17, sd3, d26, cv, crhv, d18];
    cline4 = [ d20, ch,  d12, sd2, d17, qf2, d20, sf1, d11, mon, d12, qf1, d17, sd1, d15, ch,  d12, cv, d22, mon, d10];
    
    #%% Injection Section
    dmiainj  = drift(fam_name = 'dmiainj', length = 0.3, pass_method = drif_pass_method)
    dinjk3   = drift(fam_name = 'dinjk3' , length = 0.3, pass_method = drif_pass_method)
    dk3k4    = drift(fam_name = 'dk3k4'  , length = 0.6, pass_method = drif_pass_method)
    dk4pmm   = drift(fam_name = 'dk4pmm' , length = 0.2, pass_method = drif_pass_method)
    dpmmcv   = drift(fam_name = 'dpmmcv' , length = (3.2692 - 0.3 - 0.3 - 0.6 - 0.2 - 3*0.6), pass_method = drif_pass_method)
    dcvk1    = drift(fam_name = 'dcvk1'  , length = (3.2692 - 0.6 - 1.4 - 2*0.6), pass_method = drif_pass_method)
    dk1k2    = drift(fam_name = 'dk1k2'  , length = 0.6, pass_method = drif_pass_method)
    sef      = sextupole(fam_name = 'sef', length = 0.6, k = 0.0, pass_method = sext_pass_method); #%corrector('sef', 0.6, [0 0], 'CorrectorPass');
    dk2sef   = drift(fam_name = 'dk2mia' , length = 0.8, pass_method = drif_pass_method)
  
    kick     = corrector(fam_name = 'kick', length = 0.6, kick_angle = [0, 0], pass_method = corr_pass_method)
    pmm      = sextupole(fam_name = 'pmm', length = 0.6, s = 0.0, pass_method = sext_pass_method);
    inj      = marker(fam_name = 'inj', pass_method = mark_pass_method)
     
    insaend  = [cv, d12, ch, d12, sa2, d12, mon, d12, qaf, d23, qad, d17, sa1, d17]
    insainj  = [dmiainj, inj, dinjk3, kick, dk3k4, kick, dk4pmm, pmm, dpmmcv, insaend]
    injinsa  = [insaend[::-1], dcvk1, kick, dk1k2, kick, dk2sef, sef]
    
    
    
    B3BCB3 = [ B3, d13, BC, d13, B3];     


#     %% the_ring
#     
#     % Lattice Ordering
#     % ----------------
#     % 
#     % R01 C01 R02 C02 R03 C03 R04 C04 R05 C05 R06 C06 R07 C07 R08 C08 R09 C09 R10 C10
#     % R11 C11 R12 C12 R13 C13 R14 C14 R15 C15 R16 C16 R17 C17 R18 C18 R19 C19 R20 C20
#     % 
#     % High Beta (mia) : R01, R03, R05, R07, R09, R11, R13, R15, R17, R19
#     % Low  Beta (mib) : R02, R04, R06, R08, R10, R12, R14, R16, R18, R20
#     %
#     % injection: straight section R01
#     % cavities:  straight section R03
    
    
    
    R01 = [injinsa, fim, inicio, mia, insainj]  #% injection sector, marker of the lattice model starting element
    #R01 = [insa[::-1], fim, inicio, mia, insa]  #% injection sector, marker of the lattice model starting element    
    R03 = [insa[::-1], mia, cav, insa]        #% sector with cavities
    R05 = [insa[::-1], mia, insa]
    R07 = [insa[::-1], mia, insa]
    R09 = [insa[::-1], mia, insa]
    R11 = [insa[::-1], mia, insa]
    R13 = [insa[::-1], mia, insa]
    R15 = [insa[::-1], mia, insa]
    R17 = [insa[::-1], mia, insa]
    R19 = [insa[::-1], mia, insa]
         
    R02 = [insb[::-1], mib, insb]
    R04 = [insb[::-1], mib, insb]
    R06 = [insb[::-1], mib, insb]
    R08 = [insb[::-1], mib, insb]
    R10 = [insb[::-1], mib, insb]
    R12 = [insb[::-1], mib, insb]
    R14 = [insb[::-1], mib, insb]
    R16 = [insb[::-1], mib, insb]
    R18 = [insb[::-1], mib, insb]
    R20 = [insb[::-1], mib, insb]
    
    
    C01 = [ B1, cline1, B2, cline2, B3BCB3, cline3, B2, cline4, B1 ]
    C02 = [ B1, cline1, B2, cline2, B3BCB3, cline3, B2, cline4, B1 ]
    C03 = [ B1, cline1, B2, cline2, B3BCB3, cline3, B2, cline4, B1 ]
    C04 = [ B1, cline1, B2, cline2, B3BCB3, cline3, B2, cline4, B1 ]
    C05 = [ B1, cline1, B2, cline2, B3BCB3, cline3, B2, cline4, B1 ]
    C06 = [ B1, cline1, B2, cline2, B3BCB3, cline3, B2, cline4, B1 ]
    C07 = [ B1, cline1, B2, cline2, B3BCB3, cline3, B2, cline4, B1 ]
    C08 = [ B1, cline1, B2, cline2, B3BCB3, cline3, B2, cline4, B1 ]
    C09 = [ B1, cline1, B2, cline2, B3BCB3, cline3, B2, cline4, B1 ]
    C10 = [ B1, cline1, B2, cline2, B3BCB3, cline3, B2, cline4, B1 ]
    C11 = [ B1, cline1, B2, cline2, B3BCB3, cline3, B2, cline4, B1 ]
    C12 = [ B1, cline1, B2, cline2, B3BCB3, cline3, B2, cline4, B1 ]
    C13 = [ B1, cline1, B2, cline2, B3BCB3, cline3, B2, cline4, B1 ]
    C14 = [ B1, cline1, B2, cline2, B3BCB3, cline3, B2, cline4, B1 ]
    C15 = [ B1, cline1, B2, cline2, B3BCB3, cline3, B2, cline4, B1 ]
    C16 = [ B1, cline1, B2, cline2, B3BCB3, cline3, B2, cline4, B1 ]
    C17 = [ B1, cline1, B2, cline2, B3BCB3, cline3, B2, cline4, B1 ]
    C18 = [ B1, cline1, B2, cline2, B3BCB3, cline3, B2, cline4, B1 ]
    C19 = [ B1, cline1, B2, cline2, B3BCB3, cline3, B2, cline4, B1 ]
    C20 = [ B1, cline1, B2, cline2, B3BCB3, cline3, B2, cline4, B1 ]
    
    the_ring = [
        R01, C01, R02, C02, R03, C03, R04, C04, R05, C05,
        R06, C06, R07, C07, R08, C08, R09, C09, R10, C10,
        R11, C11, R12, C12, R13, C13, R14, C14, R15, C15,
        R16, C16, R17, C17, R18, C18, R19, C19, R20, C20,
    ]

    the_ring = list(lattice.flatten(the_ring))
    
    # shift lattice to start at the marker 'inicio'
    idx = lattice.findcells(the_ring, 'fam_name', 'inicio')
    the_ring = the_ring[idx[0]:] + the_ring[:idx[0]-1]


    # check if there are elements with negative lengths
    lens = lattice.getcellstruct(the_ring, 'length', range(len(the_ring)))
    if any([l < 0 for l in lens]):
        raise Exception('negative drift in lattice!')
    
    # sets cavity frequency according to lattice length
    C = lattice.findspos(the_ring, len(the_ring))
    rev_freq = consts.light_speed / C
    rf_idx = lattice.findcells(the_ring, 'fam_name', 'cav')
    for idx in rf_idx:
        the_ring[idx].frequency = rev_freq * harmonic_number
    lattice.setcavity(the_ring, 'on'); 
    lattice.setradiation(the_ring, 'off');


    return the_ring 
    
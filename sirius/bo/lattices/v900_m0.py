default_energy  = 0.15 #[GeV]
harmonic_number = 828 

def create_lattice(energy = default_energy):

    from pyaccel import Drift, Marker, Quadrupole, Sextupole, HCorrector, VCorrector, RBend, RFCavity
    from pyaccel.lattice import buildlat
    
    rf_voltage = 150e3 if energy == 0.15 else 950e3
        
    b_length_hedge     = 1.152 #[m]
    b_length_segmented = 1.538 #[m]
    half_model_diff    = (b_length_segmented - b_length_hedge)/2.0
    
    lt       = Drift(fam_name='lt',      length=2.146000)
    lt2      = Drift(fam_name='lt2',     length=2.146000-half_model_diff) 
    l20      = Drift(fam_name='l20',     length=0.200000)
    l25      = Drift(fam_name='l25',     length=0.250000)
    l25_2    = Drift(fam_name='l25_2',   length=0.250000-half_model_diff)
    l30_2    = Drift(fam_name='l30_2',   length=0.300000-half_model_diff)
    l36      = Drift(fam_name='l36',     length=0.360000)
    l60      = Drift(fam_name='l60',     length=0.600000)
    l80      = Drift(fam_name='l80',     length=0.800000)
    l100     = Drift(fam_name='l100',    length=1.000000)
    lm25     = Drift(fam_name='lm25',    length=1.896000)
    lm30     = Drift(fam_name='lm30',    length=1.846000)
    lm40     = Drift(fam_name='lm40',    length=1.746000)
    lm45     = Drift(fam_name='lm45',    length=1.696000)
    lm60     = Drift(fam_name='lm60',    length=1.546000)
    lm66     = Drift(fam_name='lm66',    length=1.486000)
    lm70     = Drift(fam_name='lm70',    length=1.446000)
    lm120    = Drift(fam_name='lm120',   length=0.946000)
    lm105    = Drift(fam_name='lm105',   length=1.096000)
    lkk      = Drift(fam_name='lkk',     length=0.741000)
    lm60_kk  = Drift(fam_name='lm60_kk', length=0.805000)
    
    kick_in  = Marker(fam_name='kick_in')
    kick_ex  = Marker(fam_name='kick_ex')
    sept_in  = Marker(fam_name='sept_in')
    sept_ex  = Marker(fam_name='sept_ex')
    
    qd       = Quadrupole(fam_name='qd', length=0.200000, K=0.000000)
    qf       = Quadrupole(fam_name='qf', length=0.100000, K=1.882100)
    sf       = Sextupole (fam_name='sf', length=0.200000, S=6.331497)
    sd       = Sextupole (fam_name='sd', length=0.200000, S=0.000000)
    
    bpm      = Marker(fam_name='bpm')
    hcm      = HCorrector(fam_name='hcm', hkick=0.0)
    vcm      = VCorrector(fam_name='vcm', vkick=0.0)

    b01 = RBend(fam_name='b', length=1.000000000000000E-03, 
                angle=+1.426485950996607E-05, angle_in=0, angle_out=0, 
                gap=0, fint_in=0, fint_out=0, 
                polynom_a=[0,0,0,0,0,0,0],
                polynom_b=[+4.140577271934239E-05, +3.058605208196647E-02, -8.251801752174037E+00, -1.257804343190303E+02, 
                             -1.878934962563991E+05, -1.670003254353561E+06, +3.079228436209509E+09])
    b02 = RBend(fam_name='b', length=1.580000000000000E-01, 
                angle=+1.179618086127569E-03, angle_in=0, angle_out=0, 
                gap=0, fint_in=0, fint_out=0, 
                polynom_a=[0,0,0,0,0,0,0],
                polynom_b=[+0.000000000000000E+00, +4.855295535374061E-03, -7.216745503658560E-01, +3.061480477170636E+00, 
                           -9.532253730626083E+01, -1.138817354802063E+03, +7.896135726359183E+05])            
    b03 = RBend(fam_name='b', length=3.000000000000003E-02, 
                angle=+1.459353758750183E-03, angle_in=0, angle_out=0, 
                gap=0, fint_in=0, fint_out=0, 
                polynom_a=[0,0,0,0,0,0,0], 
                polynom_b=[+0.000000000000000E+00, -9.506765125433098E-02, -1.657771745012960E+00, +2.456999406155903E+01, 
                           +4.157933504094569E+03, +5.002371662930900E+03, -1.022424406403009E+08])
    b04 = RBend(fam_name='b', length=3.399999999999992E-02, 
                angle=+3.412178069747464E-03, angle_in=0, angle_out=0, 
                gap=0, fint_in=0, fint_out=0, 
                polynom_a=[0,0,0,0,0,0,0],
                polynom_b=[+0.000000000000000E+00, -2.079714071591720E-01, -1.920477735683628E+00, +5.810211405032815E+00,
                           -3.509300682929235E+03, +6.420776809816113E+04, +6.291399026007216E+07])
    b05 = RBend(fam_name='b', length=1.580000000000000E-01, 
                angle=+1.662526504959806E-02, angle_in=0, angle_out=0, 
                gap=0, fint_in=0, fint_out=0, 
                polynom_a=[0,0,0,0,0,0,0],
                polynom_b=[+0.000000000000000E+00, -1.859620865317806E-01, -1.883162915218852E+00, -1.596178727167645E-01, 
                           -8.441889487347562E+01, +1.847758710080948E+03, -1.274410000899198E+06])
    b06 = RBend(fam_name='b', length=1.920000000000000E-01, 
                angle=+1.994573240088625E-02, angle_in=0, angle_out=0, 
                gap=0, fint_in=0, fint_out=0, 
                polynom_a=[0,0,0,0,0,0,0], 
                polynom_b=[+0.000000000000000E+00, -2.119930065064550E-01, -1.926905039970153E+00, -3.604593481630426E+00,
                           -8.571181055182160E+01, -7.508028910206927E+03, -1.055179786595804E+06])
    b07 = RBend(fam_name='b', length=1.960000000000000E-01, 
                angle=+2.019544084717638E-02, angle_in=0, angle_out=0, 
                gap=0, fint_in=0, fint_out=0, 
                polynom_a=[0,0,0,0,0,0,0],
                polynom_b=[+0.000000000000000E+00, -2.272573009556761E-01, -1.993793351671241E+00, -6.474955824281598E+00, 
                           +2.179224582442633E+02, -2.005269082855995E+04, -7.440279279190110E+06]) 
     
    pb = Marker(fam_name='pb')
    mb = Marker(fam_name='mb')
    b  = [pb, b01,b02,b03,b04,b05,b06,b07,mb,b07,b06,b05,b04,b03,b02,b01, pb]

    rfc = RFCavity(fam_name='cav', length=0, frequency=0, voltage=rf_voltage)
    
    lfree     = lt
    lfree_2   = lt2
    lqd_2     = [lm45, qd, l25_2]
    lsd_2     = [lm45, sd, l25_2]
    lsf       = [lm40, sf, l20];
    lch       = [lm25, hcm, l25];
    lcv_2     = [lm30, vcm, l30_2];
    lsdcv_2   = [lm70, vcm, l25, sd, l25_2];
    fodo1     = [qf, lfree, lfree_2, b, lfree_2, bpm, lsf, qf];
    fodo2     = [qf, lfree, lqd_2, b, lcv_2[::-1], bpm, lch, qf]
    fodo2sd   = [qf, lfree, lqd_2, b, lsdcv_2[::-1], bpm, lch, qf]
    fodo1sd   = [qf, lfree, lfree_2, b, lsd_2[::-1], bpm, lsf, qf]
    boos      = [fodo1sd, fodo2, fodo1, fodo2, fodo1, fodo2sd, fodo1, fodo2, fodo1, fodo2]
    lke       = [l60, kick_ex, lkk, kick_ex, lm60_kk]
    lcvse_2   = [l36, sept_ex, lm66, vcm, l30_2]
    lmonch    = [l100, bpm, lm120, hcm, l20]
    lsich     = [lm105, sept_in, l80, hcm, l25]
    lki       = [l60, kick_in, lm60]
    fodo2kese = [qf, lke, lqd_2, b, lcvse_2[::-1], lmonch, qf]
    fodo2si   = [qf, lfree, lqd_2, b, lcv_2[::-1], bpm, lsich, qf]
    fodo1ki   = [qf, lki, lfree_2, b, lfree_2, bpm, lsf, qf]
    fodo1ch   = [qf, lch[::-1], lfree_2, b, lfree_2, bpm, lsf, qf]
    fodo1rf   = [qf, lfree, rfc, lfree_2, b, lfree_2, bpm, lsf, qf]

    boosinj   = [fodo1sd, fodo2kese, fodo1ch, fodo2si, fodo1ki, fodo2sd, fodo1, fodo2, fodo1, fodo2]
    boosrf    = [fodo1sd, fodo2, fodo1ch, fodo2, fodo1rf, fodo2sd, fodo1, fodo2, fodo1, fodo2]
    boocor    = [boosinj, boos, boosrf, boos, boos]
    elist     = boocor

    the_ring  = buildlat(elist)
    print(len(the_ring))
    
    return the_ring
                


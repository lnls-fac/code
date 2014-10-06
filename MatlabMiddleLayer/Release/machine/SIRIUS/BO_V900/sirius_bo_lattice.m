function r = sirius_bo_lattice(varargin)
%maquina com simetria 50, formada por dipolos e quadrupolos com sextupolos
%integrados. 15/08/2012 - Fernando.
% modelode segmentado dos dipolos. 10/04/2014
% mudança de padrão para baixa energia.

%%% HEADER SECTION %%%

global THERING

deg2rad = pi/180;
const = lnls_constants;
energy = 0.15e9; % eV

lattice_version = 'BO_V900';
for i=1:length(varargin)
	energy = varargin{i} * 1e9;
end
mode = 'O';
version = '0';

harmonic_number = 828;
if energy == 0.15e9, rf_voltage = 150e3; else rf_voltage = 950e3; end

lattice_title = [lattice_version '_' mode version];
fprintf(['   Loading lattice ' lattice_title ' - ' num2str(energy/1e9) ' GeV' '\n']);

bend_pass_method = 'BndMPoleSymplectic4Pass';
quad_pass_method = 'StrMPoleSymplectic4Pass';
sext_pass_method = 'StrMPoleSymplectic4Pass';

% loads magnet strengths
set_magnets_strength_booster;

lt       = drift('lt',      2.146000, 'DriftPass');
lt2      = drift('lt2',     2.146000-0.1930, 'DriftPass');
l20      = drift('l20',     0.200000, 'DriftPass');
l25      = drift('l25',     0.250000, 'DriftPass');
l25_2    = drift('l25_2',   0.250000-0.1930, 'DriftPass');
l30      = drift('l30',     0.300000, 'DriftPass');
l30_2    = drift('l30_2',   0.300000-0.1930, 'DriftPass');
l36      = drift('l36',     0.360000, 'DriftPass');
l44      = drift('l44',     0.440000, 'DriftPass');
l60      = drift('l60',     0.600000, 'DriftPass');
l80      = drift('l80',     0.800000, 'DriftPass');
l100     = drift('l100',    1.000000, 'DriftPass');
lm25     = drift('lm25',    1.896000, 'DriftPass');
lm30     = drift('lm30',    1.846000, 'DriftPass');
lm40     = drift('lm40',    1.746000, 'DriftPass');
lm45     = drift('lm45',    1.696000, 'DriftPass');
lm60     = drift('lm60',    1.546000, 'DriftPass');
lm66     = drift('lm66',    1.486000, 'DriftPass');
lm70     = drift('lm70',    1.446000, 'DriftPass');
lm120    = drift('lm120',   0.946000, 'DriftPass');
lm105    = drift('lm105',   1.096000, 'DriftPass');
lkk      = drift('lkk',     0.741000, 'DriftPass');
lm60_kk  = drift('lm60_kk', 0.805000, 'DriftPass');

kick_in  = marker('kick_in', 'IdentityPass');
kick_ex  = marker('kick_ex', 'IdentityPass');
sept_in  = marker('sept_in', 'IdentityPass');
sept_ex  = marker('sept_ex', 'IdentityPass');

qd       = quadrupole('qd', 0.200000, 0.000000, quad_pass_method);
qf       = quadrupole('qf', 0.100000, 1.882100, quad_pass_method);
sf       = sextupole ('sf', 0.200000, 6.331497, sext_pass_method);
sd       = sextupole ('sd', 0.200000, 0.000000, sext_pass_method);
    
bpm      = marker('bpm', 'IdentityPass');
hcm      = corrector('hcm', 0, [0, 0], 'CorrectorPass');
vcm      = corrector('vcm', 0, [0, 0], 'CorrectorPass');


%segmentation based on field map of model6
b01 = rbend_sirius('b', 1.000000000000000E-03, +1.426485950996607E-05, ...
                   0, 0, 0, 0, 0, [0,0,0,0,0,0,0], ...
                   [+4.140577271934239E-05, +3.058605208196647E-02, ...
                    -8.251801752174037E+00, -1.257804343190303E+02, ...
                    -1.878934962563991E+05, -1.670003254353561E+06, ...
                    +3.079228436209509E+09], bend_pass_method);
b02 = rbend_sirius('b', 1.580000000000000E-01, +1.179618086127569E-03, ...
                   0, 0, 0, 0, 0, [0,0,0,0,0,0,0], ...
                   [+0.000000000000000E+00, +4.855295535374061E-03, ...
                    -7.216745503658560E-01, +3.061480477170636E+00, ...
                    -9.532253730626083E+01, -1.138817354802063E+03, ...
                    +7.896135726359183E+05], bend_pass_method);
b03 = rbend_sirius('b', 3.000000000000003E-02, +1.459353758750183E-03, ...
                   0, 0, 0, 0, 0, [0,0,0,0,0,0,0], ...
                   [+0.000000000000000E+00, -9.506765125433098E-02, ...
                   -1.657771745012960E+00, +2.456999406155903E+01, ...
                   +4.157933504094569E+03, +5.002371662930900E+03, ...
                   -1.022424406403009E+08], bend_pass_method);
b04 = rbend_sirius('b', 3.399999999999992E-02, +3.412178069747464E-03, ...
                   0, 0, 0, 0, 0, [0,0,0,0,0,0,0], ...
                   [+0.000000000000000E+00, -2.079714071591720E-01, ...
                   -1.920477735683628E+00, +5.810211405032815E+00, ...
                   -3.509300682929235E+03, +6.420776809816113E+04, ...
                   +6.291399026007216E+07], bend_pass_method);
b05 = rbend_sirius('b', 1.580000000000000E-01, +1.662526504959806E-02, ...
                   0, 0, 0, 0, 0, [0,0,0,0,0,0,0], ...
                   [+0.000000000000000E+00, -1.859620865317806E-01, ...
                   -1.883162915218852E+00, -1.596178727167645E-01, ...
                   -8.441889487347562E+01, +1.847758710080948E+03, ...
                   -1.274410000899198E+06], bend_pass_method);
b06 = rbend_sirius('b', 1.920000000000000E-01, +1.994573240088625E-02, ...
                   0, 0, 0, 0, 0, [0,0,0,0,0,0,0], ...
                   [+0.000000000000000E+00, -2.119930065064550E-01, ...
                   -1.926905039970153E+00, -3.604593481630426E+00, ...
                   -8.571181055182160E+01, -7.508028910206927E+03, ...
                   -1.055179786595804E+06], bend_pass_method);
b07 = rbend_sirius('b', 1.960000000000000E-01, +2.019544084717638E-02, ...
                   0, 0, 0, 0, 0, [0,0,0,0,0,0,0], ...
                   [+0.000000000000000E+00, -2.272573009556761E-01, ...
                   -1.993793351671241E+00, -6.474955824281598E+00, ...
                   +2.179224582442633E+02, -2.005269082855995E+04, ...
                   -7.440279279190110E+06], bend_pass_method);
pb = marker('pb', 'IdentityPass');
mb = marker('mb', 'IdentityPass');
bd = [pb, b01,b02,b03,b04,b05,b06,b07,mb,b07,b06,b05,b04,b03,b02,b01, pb];

 
rfc = rfcavity('cav', 0, rf_voltage, 0, harmonic_number, 'CavityPass'); % RF frequency will be set later.

% b         = bd;
% lfree     = lt;
% lfree2    = lt2;
% lqd       = [lm45, qd, l25];
% lsd       = [lm45, sd, l25];
% lsf       = [lm40, sf, l20];
% lch       = [lm25, hcm, l25];
% lcv       = [lm30, vcm, l30];
% lsdcv     = [lm70, vcm, l25, sd, l25];
% fodo1     = [qf, lfree, lfree, b, lfree, bpm, lsf, qf];
% fodo2     = [qf, lfree, lqd, b, fliplr(lcv), bpm, lch, qf];
% fodo2sd   = [qf, lfree, lqd, b, fliplr(lsdcv), bpm, lch, qf];
% fodo1sd   = [qf, lfree, lfree, b, fliplr(lsd), bpm, lsf, qf];
% boos      = [fodo1sd, fodo2, fodo1, fodo2, fodo1, fodo2sd, fodo1, fodo2, fodo1, fodo2];
% lke       = [l60, kick_ex, lkk, kick_ex, lm60_kk];
% lcvse     = [l36, sept_ex, lm66, vcm, l30];
% lmonch    = [l100, bpm, lm120, hcm, l20];
% lsich     = [lm105, sept_in, l80, hcm, l25];
% lki       = [l60, kick_in, lm60];
% fodo2kese = [qf, lke, lqd, b, fliplr(lcvse), lmonch, qf];
% fodo2si   = [qf, lfree, lqd, b, fliplr(lcv), bpm, lsich, qf];
% fodo1ki   = [qf, lki, lfree, b, lfree, bpm, lsf, qf];
% boosinj   = [fodo1sd, fodo2kese, fodo1, fodo2si, fodo1ki, fodo2sd, fodo1, fodo2, fodo1, fodo2];
% fodo1rf   = [qf, lfree, rfc, lfree, b, lfree, bpm, lsf, qf];
% boosrf    = [fodo1sd, fodo2, fodo1, fodo2, fodo1rf, fodo2sd, fodo1, fodo2, fodo1, fodo2];
% boocor    = [boosinj, boos, boosrf, boos, boos];
% %booster   = [boos, boos, boos, boos, boos];
% elist     = boocor;

          
b         = bd;
lfree     = lt;
lfree_2    = lt2;
%lqd       = [lm45, qd, l25];
lqd_2      = [lm45, qd, l25_2];
%lsd       = [lm45, sd, l25];
lsd_2      = [lm45, sd, l25_2];
lsf       = [lm40, sf, l20];
lch       = [lm25, hcm, l25];
%lcv       = [lm30, vcm, l30];
lcv_2     = [lm30, vcm, l30_2];
%lsdcv     = [lm70, vcm, l25, sd, l25];
lsdcv_2   = [lm70, vcm, l25, sd, l25_2];
fodo1     = [qf, lfree, lfree_2, b, lfree_2, bpm, lsf, qf];
fodo2     = [qf, lfree, lqd_2, b, fliplr(lcv_2), bpm, lch, qf];
fodo2sd   = [qf, lfree, lqd_2, b, fliplr(lsdcv_2), bpm, lch, qf];
fodo1sd   = [qf, lfree, lfree_2, b, fliplr(lsd_2), bpm, lsf, qf];
boos      = [fodo1sd, fodo2, fodo1, fodo2, fodo1, fodo2sd, fodo1, fodo2, fodo1, fodo2];
lke       = [l60, kick_ex, lkk, kick_ex, lm60_kk];
%lcvse     = [l36, sept_ex, lm66, vcm, l30];
lcvse_2   = [l36, sept_ex, lm66, vcm, l30_2];
lmonch    = [l100, bpm, lm120, hcm, l20];
lsich     = [lm105, sept_in, l80, hcm, l25];
lki       = [l60, kick_in, lm60];
fodo2kese = [qf, lke, lqd_2, b, fliplr(lcvse_2), lmonch, qf];
fodo2si   = [qf, lfree, lqd_2, b, fliplr(lcv_2), bpm, lsich, qf];
fodo1ki   = [qf, lki, lfree_2, b, lfree_2, bpm, lsf, qf];
boosinj   = [fodo1sd, fodo2kese, fodo1, fodo2si, fodo1ki, fodo2sd, fodo1, fodo2, fodo1, fodo2];
fodo1rf   = [qf, lfree, rfc, lfree_2, b, lfree_2, bpm, lsf, qf];
boosrf    = [fodo1sd, fodo2, fodo1, fodo2, fodo1rf, fodo2sd, fodo1, fodo2, fodo1, fodo2];
boocor    = [boosinj, boos, boosrf, boos, boos];
%booster   = [boos, boos, boos, boos, boos];
elist     = boocor;


% builds AT model from 'elist' vector
THERING = buildlat(elist);
THERING = setcellstruct(THERING, 'Energy', 1:length(THERING), energy);

% computes total length and sets RF frequency
L0_tot = findspos(THERING, length(THERING)+1);
rev_freq     = const.c / L0_tot;
rf_idx       = findcells(THERING, 'FamName', 'cav');
rf_frequency = rev_freq * harmonic_number; 
THERING{rf_idx}.Frequency = rf_frequency;
fprintf(['   RF frequency set to ' num2str(rf_frequency/1e6) ' MHz.\n']);

% set default NumIntSteps values
THERING = set_num_integ_steps(THERING);

% defines vacuum chamber for all elements
THERING = set_vacuum_chamber(THERING);

% preloads passmethods
lnls_preload_passmethods;

r = THERING;





function r = sirius_bo_lattice_old(varargin)
%maquina com simetria 50, formada por dipolos e quadrupolos com sextupolos
%integrados. 15/08/2012 - Fernando.
% modelode segmentado dos dipolos. 10/04/2014
% mudança de padrão para baixa energia.

%%% HEADER SECTION %%%

global THERING

const = lnls_constants;
energy = 0.15e9; % eV

lattice_version = 'BO_V810';
for i=1:length(varargin)
	energy = varargin{i} * 1e9;
end
mode = 'Opt';
version = '2';

harmonic_number = 828;
if energy == 0.15e9, voltage = 150e3; else voltage = 950e3; end
RFC = rfcavity('CAV', 0, voltage, 499654000, harmonic_number, 'CavityPass');

lattice_title = [lattice_version '_' mode version];
fprintf(['   Loading lattice ' lattice_title ' - ' num2str(energy/1e9) ' GeV' '\n']);

bend_pass_method = 'BndMPoleSymplectic4Pass';
quad_pass_method = 'StrMPoleSymplectic4Pass';
sext_pass_method = 'StrMPoleSymplectic4Pass';

%carrega as forcas dos magnetos;
set_magnets_strength_booster;


% B_length = 1.1520;
% B_angle  = 360 / 50;
% B_gap    = 0.028;
% B_fint1  = 0.0;
% B_fint2  = 0.0;
% B_edge   = (B_angle/2)*(pi/180)*1;
% b1 = rbend_sirius('B', B_length, B_angle*(pi/180), B_edge, B_edge, ...
%     B_gap, B_fint1, B_fint2, [0 0 0 0], [0, B_strength, B_sext, 0], bend_pass_method);
% pb = marker('PB', 'IdentityPass');
% b = [pb, b1, pb];

%segmentation based on field map of model6
b01 = rbend_sirius('B', 1.000000000000000E-03, +1.426485950996607E-05, ...
                   0, 0, 0, 0, 0, [0,0,0,0,0,0,0], ...
                   [+4.140577271934239E-05, +3.058605208196647E-02, ...
                    -8.251801752174037E+00, -1.257804343190303E+02, ...
                    -1.878934962563991E+05, -1.670003254353561E+06, ...
                    +3.079228436209509E+09], bend_pass_method);
b02 = rbend_sirius('B', 1.580000000000000E-01, +1.179618086127569E-03, ...
                   0, 0, 0, 0, 0, [0,0,0,0,0,0,0], ...
                   [+0.000000000000000E+00, +4.855295535374061E-03, ...
                    -7.216745503658560E-01, +3.061480477170636E+00, ...
                    -9.532253730626083E+01, -1.138817354802063E+03, ...
                    +7.896135726359183E+05], bend_pass_method);
b03 = rbend_sirius('B', 3.000000000000003E-02, +1.459353758750183E-03, ...
                   0, 0, 0, 0, 0, [0,0,0,0,0,0,0], ...
                   [+0.000000000000000E+00, -9.506765125433098E-02, ...
                   -1.657771745012960E+00, +2.456999406155903E+01, ...
                   +4.157933504094569E+03, +5.002371662930900E+03, ...
                   -1.022424406403009E+08], bend_pass_method);
b04 = rbend_sirius('B', 3.399999999999992E-02, +3.412178069747464E-03, ...
                   0, 0, 0, 0, 0, [0,0,0,0,0,0,0], ...
                   [+0.000000000000000E+00, -2.079714071591720E-01, ...
                   -1.920477735683628E+00, +5.810211405032815E+00, ...
                   -3.509300682929235E+03, +6.420776809816113E+04, ...
                   +6.291399026007216E+07], bend_pass_method);
b05 = rbend_sirius('B', 1.580000000000000E-01, +1.662526504959806E-02, ...
                   0, 0, 0, 0, 0, [0,0,0,0,0,0,0], ...
                   [+0.000000000000000E+00, -1.859620865317806E-01, ...
                   -1.883162915218852E+00, -1.596178727167645E-01, ...
                   -8.441889487347562E+01, +1.847758710080948E+03, ...
                   -1.274410000899198E+06], bend_pass_method);
b06 = rbend_sirius('B', 1.920000000000000E-01, +1.994573240088625E-02, ...
                   0, 0, 0, 0, 0, [0,0,0,0,0,0,0], ...
                   [+0.000000000000000E+00, -2.119930065064550E-01, ...
                   -1.926905039970153E+00, -3.604593481630426E+00, ...
                   -8.571181055182160E+01, -7.508028910206927E+03, ...
                   -1.055179786595804E+06], bend_pass_method);
b07 = rbend_sirius('B', 1.960000000000000E-01, +2.019544084717638E-02, ...
                   0, 0, 0, 0, 0, [0,0,0,0,0,0,0], ...
                   [+0.000000000000000E+00, -2.272573009556761E-01, ...
                   -1.993793351671241E+00, -6.474955824281598E+00, ...
                   +2.179224582442633E+02, -2.005269082855995E+04, ...
                   -7.440279279190110E+06], bend_pass_method);
pb = marker('PB', 'IdentityPass');
mb = marker('MB', 'IdentityPass');
b = [pb, b01,b02,b03,b04,b05,b06,b07,mb,b07,b06,b05,b04,b03,b02,b01, pb];

qd   = quadrupole('QD', 0.20, qd_strength, quad_pass_method);

%coef do mapa de campo.
polB = [[0 2.35824E-01], 0*[0 5.80904E+00 0 -1.10084E+05 0 8.17767E+08 0 ...
       -3.13863E+12 0 6.58302E+15 0 -7.11141E+18 0 3.54236E+21 0 -6.05227E+23]];
 
polB = polB/polB(2)* qf_strength;
qf   = quadrupole_sirius('QF', 0.10, polB*0, polB, quad_pass_method);
% qf   = quadrupole('qf', 0.10, qf_strength, quad_pass_method);
mqf   = marker('MQF', 'IdentityPass');

sf = sextupole('SF', 0.20, sf_strength, sext_pass_method);

sd = sextupole('SD', 0.20, sd_strength, sext_pass_method);

inicio   = marker('INICIO', 'IdentityPass');
fim      = marker('FIM',    'IdentityPass');
inj      = marker('INJ', 'IdentityPass');
mon      = marker('BPM', 'IdentityPass');


ch = corrector('HCM', 0.10, [0 0], 'StrMPoleSymplectic4Pass');
cv = corrector('VCM', 0.10, [0 0], 'StrMPoleSymplectic4Pass');

hlt      = drift('HLT',  2.146000/2, 'DriftPass');
l15      = drift('L15',  0.150000, 'DriftPass');
l20      = drift('L25',  0.200000, 'DriftPass');
l30      = drift('L30',  0.300000, 'DriftPass');
l81      = drift('L70',  0.800581, 'DriftPass');
lm30     = drift('LM30', 1.846000, 'DriftPass');
lm35     = drift('LM35', 1.796000, 'DriftPass');
lm45     = drift('LM45', 1.696000, 'DriftPass');
lm75     = drift('LM70', 1.396000, 'DriftPass');
lm109    = drift('LM100',0.995419, 'DriftPass');


%kicker de injecao
kick_in  = drift('KICK_IN', 0.500, 'DriftPass');
l37      = drift('L37',  0.370000, 'DriftPass');
lm87     = drift('LM87', 1.276000, 'DriftPass');
lki     = [l37, kick_in, lm87]; % kicker de injecao
%septum de injecao
sept_in  = drift('SEPT_IN', 0.500, 'DriftPass');
lm145     = drift('LM145', 0.596000, 'DriftPass');
l75      = drift('L75',  0.750000, 'DriftPass');
%kicker de extracao
kick_ex  = drift('KICK_EX',0.500, 'DriftPass');
l42      = drift('L42',  0.426000, 'DriftPass');
l28      = drift('L24',  0.281044, 'DriftPass');
l22      = drift('L23',  0.219478, 'DriftPass');
kick_e   = [l22, kick_ex, l28, kick_ex, l22]; % ao todo dah 1.72m
%septum de extracao: tamanho nao realista. projecao na orbita do booster eh
%menor
sept_ex  = drift('SEPT_EX', 0.800, 'DriftPass');
sept_ex = [sept_ex l20 sept_ex];
l04      = drift('l04',  0.0460000, 'DriftPass');

mlt      = marker('MLT', 'IdentityPass');


%Standard:

diff_b_len = 1.538 - 1.1520;
hlt2 = drift('HLT',  2.146000/2-diff_b_len/2, 'DriftPass');
lfree_2   = [hlt mlt hlt2];
l25_2     = drift('L25',  0.250000-diff_b_len/2, 'DriftPass');
lqd       = [lm45, qd, l25_2];
lcv_2     = [l25_2, cv, lm35];
lsd_2     = [l25_2, sd, lm45];
lsdcv_2   = [l25_2, sd, l20, cv, lm75];
lcvmon_2  = [l25_2, cv, lm109, mon, l81]; % 1) desloca bpm do centro p/ cam. vac. elip.

lfree   = [hlt mlt hlt];
lsf     = [lm35, sf, l15];
lch     = [lm30, ch, l20];
fodo1   = [mqf, qf, lfree, lfree_2, b, fliplr(lfree_2), mon, lsf, qf];
fodo2   = [mqf, qf, lfree, lqd, b, lcv_2, mon, lch, qf];
fodo1sd = [mqf, qf, lfree, lfree_2, b, lsd_2, mon, lsf, qf];
fodo2sd = [mqf, qf, lfree, lqd, b, lsdcv_2, mon, lch, qf];
boos=[fodo1sd, fodo2, fodo1, fodo2, fodo1, fodo2sd, fodo1, fodo2, fodo1, fodo2];

%Injection and Extraction
%lcvmon  = [l81, mon, lm114, cv, l30]; % 1) desloca bpm do centro p/ cam. vac. elip.
lke     = [l42, kick_e]; % kikcer de extracao
lse     = [l30, sept_ex, l04]; % septum de extracao
lsich   = [lm145, sept_in, l75, ch, l20]; % septum de injecao


fodo2ke  = [mqf, qf, lke, lqd, b, lcvmon_2, lch, qf]; % aplic de 1
fodo1se = [mqf, qf, lse, lfree_2, b, fliplr(lfree_2), mon, lsf, qf];
fodo2si = [mqf, qf, lfree, lqd, b, lcv_2, mon, lsich, qf];
fodo1ki = [mqf, qf, lki, lfree_2, b, fliplr(lfree_2), mon, lsf, qf];
booin=[fodo1sd,fodo2ke,fodo1se,fodo2si,fodo1ki,fodo2sd,fodo1,fodo2,fodo1,fodo2];

% RF section

fodo1rf = [mqf, qf, lfree, RFC, lfree_2, b, fliplr(lfree_2), mon, lsf, qf];
boosrf  = [fodo1sd,fodo2,fodo1,fodo2,fodo1rf,fodo2sd,fodo1,fodo2,fodo1,fodo2];

boocor  = [inicio, booin, boos, boosrf, boos, boos, fim];

%%% TAIL SECTION %%%

elist = boocor;
THERING = buildlat(elist);
% mbegin = findcells(THERING, 'FamName', 'BEGIN');
% if ~isempty(mbegin), THERING = circshift(THERING, [0 -(mbegin(1)-1)]); end
% THERING{end+1} = struct('FamName','END','Length',0,'PassMethod','IdentityPass');
THERING = setcellstruct(THERING, 'Energy', 1:length(THERING), energy);


% Compute total length and RF frequency
L0_tot = findspos(THERING, length(THERING)+1);
rev_freq    = const.c / L0_tot;
rf_idx      = findcells(THERING, 'FamName', 'CAV');
THERING{rf_idx}.Frequency = rev_freq * harmonic_number;


% Ajusta NumIntSteps
THERING = set_num_integ_steps(THERING);

% Define Camara de Vacuo
THERING = set_vacuum_chamber(THERING);

% pre-carrega passmethods de forma a evitar problema com bibliotecas recem-compiladas
lnls_preload_passmethods;

r = THERING;


function the_ring = set_vacuum_chamber(the_ring0)

% y = +/- y_lim * sqrt(1 - (x/x_lim)^n);

the_ring = the_ring0;
bends_vchamber = [0.0117 0.0117 1]; % n = 100: ~rectangular
other_vchamber = [0.018  0.018  1];   % n = 1;   circular/eliptica

bends = findcells(the_ring, 'BendingAngle');
other = setdiff(1:length(the_ring), bends);

for i=1:length(bends)
    the_ring{bends(i)}.VChamber = bends_vchamber;
end

for i=1:length(other)
    the_ring{other(i)}.VChamber = other_vchamber;
end


function the_ring = set_num_integ_steps(the_ring0)

the_ring = the_ring0;

bends = findcells(the_ring, 'BendingAngle');
quads = setdiff(findcells(the_ring, 'K'), bends);
sexts = setdiff(findcells(the_ring, 'PolynomB'), [bends quads]);
kicks = findcells(the_ring, 'XGrid');

dl = 0.03;

bends_len = getcellstruct(the_ring, 'Length', bends);
bends_nis = ceil(bends_len / dl);
bends_nis = max([bends_nis'; 10 * ones(size(bends_nis'))]);
the_ring = setcellstruct(the_ring, 'NumIntSteps', bends, bends_nis);
the_ring = setcellstruct(the_ring, 'NumIntSteps', quads, 10);
the_ring = setcellstruct(the_ring, 'NumIntSteps', sexts, 5);
the_ring = setcellstruct(the_ring, 'NumIntSteps', kicks, 1);



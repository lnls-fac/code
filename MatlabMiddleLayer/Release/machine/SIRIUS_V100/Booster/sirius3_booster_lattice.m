function r = sirius3_booster_lattice(varargin)
%máquina com simetria 48, formada por dipolos e quadrupolos com sextupolos
%integrados. 15/08/2012 - Fernando.

%%% HEADER SECTION %%%

global THERING

const = lnls_constants;
energy = 3e9; % eV


for i=1:length(varargin)
	energy = varargin{i} * 1e9;
end

harmonic_number = 832;
RFC = rfcavity('RF', 0, 1.8e+6, 500000000.0000, harmonic_number, 'CavityPass');


bend_pass_method = 'BndMPoleSymplectic4Pass';
quad_pass_method = 'StrMPoleSymplectic4Pass';
sext_pass_method = 'StrMPoleSymplectic4Pass';


B_length = 1.2000;
B_angle  = 360 / 48;
B_gap    = 0.025;
B_fint1  = 0.5;
B_fint2  = 0.5;
B_strength = -0.180000;
B_sext     = -1.618795;
qf_sext    = 1.533775;


qd   = quadrupole('QD', 0.10, 0.0, quad_pass_method);
qf   = quadrupole('QF', 0.15, 1.203450, quad_pass_method);

sf = sextupole('SF', 0.15, 0.360610, sext_pass_method);
sd = sextupole('SD', 0.15, -1.700732, sext_pass_method);

inj = marker('INJ', 'IdentityPass');
mon = marker('BPM', 'IdentityPass');
           
b = rbend_sirius('B', B_length, (B_angle)*(pi/180), 1*(B_angle/2)*(pi/180), 1*(B_angle/2)*(pi/180), B_gap, B_fint1, B_fint2, [0 0 0 0], [0 B_strength B_sext 0], bend_pass_method);

ch = corrector('HCM', 0, [0 0], 'CorrectorPass');
cv = corrector('VCM', 0, [0 0], 'CorrectorPass');


lf = drift('ATR', 2.073500, 'DriftPass');
lfq = drift('ATR', 2.073500, 'DriftPass');
lfs = drift('ATR', 1.923500, 'DriftPass');
ld = drift('ATR', 0.200000, 'DriftPass');
ls = drift('ATR', 0.15000, 'DriftPass');


fodo    = [qf, ls, ch, lf, mon, lf, cv, ls, b, ls, lf, lf, ls, qf];    
fodod   = [qf, ls, ch, lf, mon, lf, cv, ls, b, ld, qd, lfq, lfq, qf];
fodosf  = [qf, ls, sf, ls, ch, lfs, mon, lfs, cv, ls, b, ls, lf, lf, ls, qf];
fodosd  = [qf, ls, ch, lfs, mon, lfs, cv, ls, sd, ls, b, ls, lf, lf, ls, qf];
BOOS    = [fodod, fodosf, fodod, fodosd, fodod, fodo];
BOOSTER = [BOOS BOOS BOOS BOOS BOOS BOOS BOOS BOOS RFC];

%%% TAIL SECTION %%%

elist = BOOSTER;
THERING = buildlat(elist);
mbegin = findcells(THERING, 'FamName', 'BEGIN');
if ~isempty(mbegin), THERING = circshift(THERING, [0 -(mbegin(1)-1)]); end
THERING{end+1} = struct('FamName','END','Length',0,'PassMethod','IdentityPass');
THERING = setcellstruct(THERING, 'Energy', 1:length(THERING), energy);


% Compute total length and RF frequency
L0_tot = findspos(THERING, length(THERING)+1);
rev_freq    = const.c / L0_tot;
rf_idx      = findcells(THERING, 'FamName', 'RF');
THERING{rf_idx}.Frequency = rev_freq * harmonic_number;

% Insert sextupole in the qf family
qfind = findcells(THERING, 'FamName', 'QF');
THERING = setcellstruct(THERING, 'PolynomB', qfind, qf_sext, 3);

% just in case
lnls_preload_passmethods;

r = THERING;
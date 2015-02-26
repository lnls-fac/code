function sirius_si_multipole_systematic_errors

% multipole order convention: n=0(dipole), n=1(quadrupole), and so on. 


% QUADRUPOLES Q14 MODEL2
% ======================
r0            = 11.7/1000;
monomials     = [ 5,       9,       13,       17];
Bn_normal     = [-3.6e-4, +1.4e-3, -5.9e-04, +5.7e-5];
An_skew       = [ 0.0,     0.0,     0.0,      0.0];
main_monomial = {1, 'normal'}; 
families      = findmemberof('q14');
insert_multipoles(families, monomials, Bn_normal, An_skew, main_monomial, r0);

% QUADRUPOLES Q20 MODEL3
% ======================
r0            = 11.7/1000;
monomials     = [ 5,       9,       13,       17];
Bn_normal     = [-3.7e-4, +1.4e-3, -5.7e-04, +3.8e-5];
An_skew       = [ 0.0,     0.0,     0.0,      0.0];
main_monomial = {1, 'normal'}; 
families      = findmemberof('q20');
insert_multipoles(families, monomials, Bn_normal, An_skew, main_monomial, r0);

% QUADRUPOLES Q30 MODEL4
% ======================
r0            = 11.7/1000;
monomials     = [ 5,       9,       13,       17];
Bn_normal     = [-3.9e-4, +1.5e-3, -6.0e-04, +4.8e-5];
An_skew       = [ 0.0,     0.0,     0.0,      0.0];
main_monomial = {1, 'normal'}; 
families      = findmemberof('q30');
insert_multipoles(families, monomials, Bn_normal, An_skew, main_monomial, r0);


function insert_multipoles(families, monomials, Bn_normal, An_skew, main_monomial, r0)

global THERING

% expands lists of multipoles
new_monomials = monomials+1;    % converts to tracy convention of multipole order
new_Bn_normal = zeros(max(new_monomials),1);
new_An_skew   = zeros(max(new_monomials),1);
new_Bn_normal(new_monomials,1) = Bn_normal;
new_An_skew(new_monomials,1)   = An_skew;
if strcmpi(main_monomial{2}, 'normal')
    new_main_monomial = main_monomial{1} + 1;
else
    new_main_monomial = -(main_monomial{1} + 1);
end

% adds multipoles
for i=1:length(families)
    family  = families{i};
    idx     = findcells(THERING, 'FamName', family);
    THERING = lnls_set_multipoles(THERING, new_Bn_normal, new_An_skew, new_main_monomial, r0, idx);
end



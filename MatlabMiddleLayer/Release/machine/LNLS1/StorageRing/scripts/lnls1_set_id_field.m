function lnls1_set_id_field(id, field)

global THERING

% HARD EDGE model for the IDs
% This model preserves:
%   1. maximum deflection angle of the sinusoidal field
%   2. intrinsic vertical focusing
% [See. Wiedemann, "Particle Accelerator Physics", pg. 141. 3rd Edition]
% [In this ref. HardEdge length is a factor of 2 smaller than correct value.]

% available IDs in UVX
ids_label   =  {'AWG01', 'AWG09', 'AON11'};
ids_lengths = [2.7, 1.02, 2.85];
ids_period  = [0.18, 0.06, 0.05];
ids_poles   = {...
    [0.5 repmat([-1 1],1,14) -0.5]; ...
    [0.5 repmat([-1 1],1,16) -0.5]; ...
    [-0.5 repmat([-1 1],1,56) 0.5] ...
    };

% gets id index
id_idx   = strcmpi(ids_label, id);
idx      = findcells(THERING, 'FamName', id);

% turns off id
if (field == 0)
    % models zero field ID as a pure drift space
    THERING = setcellstruct(THERING, 'PassMethod', idx, 'DriftPass');
    THERING = setcellstruct(THERING, 'Length', idx, ids_lengths(id_idx)/length(idx));
    return;
end

energy = getenergymodel;
[~, ~, b_rho] = lnls_beta_gamma(energy);

id_label  = ids_label{id_idx};
period    = ids_period(id_idx);
poles_str = ids_poles{id_idx};
lhe       = 4 * period / pi^2;

% temporary lattices building blocks
idperiod  = [drift(id_label, 0, 'DriftPass') rbend(id_label, 0, 0, 0, 0, 0, 'BndMPoleSymplectic4Pass') drift(id_label, 0, 'DriftPass')];
idperiod  = buildlat(idperiod);
idperiod{1}.Energy = energy; idperiod{2}.Energy = energy; idperiod{3}.Energy = energy;
idperiod{1}.Field  = field;  idperiod{2}.Field  = field;  idperiod{3}.Figure = field;
markers   = [marker('BEGIN', 'IdentityPass') marker('LCENTER', 'IdentityPass')];
markers   = buildlat(markers);
markers{1}.Energy = energy; markers{2}.Energy = energy; 
markers{1}.Field  = field;  markers{2}.Field  = field;


% builds the ID model
idlattice = {};
for p=1:length(poles_str)
    pole_strength = poles_str(p);
    pole_field    = field * pole_strength;
    rho0          = b_rho / pole_field;
    rho           = 4 * rho0 / pi;
    bending_angle = lhe/rho;
    drift_len     = (period/2) - 2*rho*sin(0.5*bending_angle);
    % upstream drift
    idperiod{1}.Length = drift_len / 2;
    % bending dipole
    idperiod{2}.Length        = lhe;
    idperiod{2}.BendingAngle  = bending_angle;
    idperiod{2}.EntranceAngle = bending_angle/2;
    idperiod{2}.ExitAngle     = bending_angle/2;
    % downstream drift
    idperiod{3}.Length = drift_len / 2;
    % adds to lattice being built
    idlattice = [idlattice idperiod];
    % adds marker at center
    if (p == floor(length(poles_str)/2))
        if strcmpi(id_label, 'AWG01')
            % inserts markers 'BEGIN' and 'LCENTER' in the middle of AWG01
            idlattice = [idlattice markers];
        else
            idlattice = [idlattice markers(2)];
        end
    end
end


% inserts de ID model into the lattice

% first moves first cavity as first element (this is needed because AWG01 is split in TR01)
famname_first = THERING{1}.FamName;
cav_idx  = findcells(THERING, 'FamName', 'RF');
THERING = [THERING(cav_idx(1):end) THERING(1:(cav_idx(1)-1))]; 
idx      = findcells(THERING, 'FamName', id);
% inserts ID into lattice
THERING = [THERING(1:(idx(1)-1)) idlattice THERING((idx(end)+1):end)];
% shift lattice back to original position
idx_first  = findcells(THERING, 'FamName', famname_first);
THERING = [THERING(idx_first:end) THERING(1:idx_first-1)];


function study_coupling


global THERING;

clc;
%filename = fullfile('/home/fac_files/data/sirius_mml/lattice_errors/CONFIG_V500_AC10_6_40ums_symm_coup','CONFIG_machines_cod_symm_coup_corrected.mat');
filename = fullfile('/home/fac_files/data/sirius_mml/lattice_errors/CONFIG_V500_AC10_6_40ums_IDs_symm_coup','CONFIG_V500_AC10_6_40ums_IDs_symm_coup_machines_cod_symm_coup_corrected.mat');
load(filename);

%machine = machine(1:2);

quads = setdiff(findcells(machine{1}, 'K'), findcells(machine{1}, 'BendingAngle'))';
%famnames = unique(getcellstruct(machine{1}, 'FamName', quads));

for i=1:length(machine)
    THERING = machine{i};
    [Tilt, Eta, EpsX, EpsY, EmittanceRatio(i,1), ENV, DP, DL, BeamSize] = calccoupling;
    R13 = getcellstruct(machine{1}, 'R1', quads, 1, 3);
    angle(i,:) = asin(R13);
    fprintf('%02i: %7.4f %%\n', i, 100*EmittanceRatio(i));
end
fprintf('mean: %f %f %%\n', 100*mean(EmittanceRatio), 100*std(EmittanceRatio));
for i=1:length(machine)
    THERING = machine{i};
    THERING = lnls_set_rotation_ROLL(1.05 * 1.55 * 0.67 *  1.106194690265487 * angle(i,:), quads, THERING);
    [Tilt, Eta, EpsX, EpsY, NewEmittanceRatio(i,1), ENV, DP, DL, BeamSize] = calccoupling;
    fprintf('%02i: %7.4f %%\n', i, 100*NewEmittanceRatio(i));
    machine{i} = THERING;
end
fprintf('mean: %f %f %%\n', 100*mean(NewEmittanceRatio), 100*std(NewEmittanceRatio));

save('CONFIG_machines_cod_symm_coup_corrected_1p0_coup.mat', 'machine');

disp('ok');

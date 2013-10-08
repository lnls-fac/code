
% first, we load the lattice
lattice_errors([pwd '/cod_matlab']);
machines = load([pwd '/cod_matlab/CONFIG_machines_cod_corrected.mat']);
storage_ring = machines.machine;

param.energy_deviation  = (-4:4)*1e-2;
param.radius_resolution = 1e-4;
param.nr_turns          = 5000;
param.points_angle      = repmat([1/2, 3/4, 1]*pi +1e-3, length(param.energy_deviation), 1);
param.points_radius     = repmat([1, 2.5,  5]*1e-3,     length(param.energy_deviation), 1);


x = zeros(length(storage_ring),length(param.points_angle))
for ii = 1:length(storage_ring)
    r = lnls_dynapt(storage_ring{ii},param);
    x(ii,:) = r.points_x(en0,:);
    y(ii,:) = r.points_y(en0,:);
    x_en(ii,:) = r.points_x(:,end)'; 
end

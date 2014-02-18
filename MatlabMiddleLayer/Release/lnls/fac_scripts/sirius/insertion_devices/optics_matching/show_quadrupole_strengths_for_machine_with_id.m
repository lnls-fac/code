function show_quadrupole_strengths_for_machine_with_id(the_ring)

clc;

% loads the_ring
if ~exist('the_ring','var')
    load('the_ring_withids_ac10_5_newIDs.mat');
end

% loops over elements
current_id = '';
straight_nr = 0;
end_of_dsec = 1;
for i=1:length(the_ring)
    if isfield(the_ring{i}, 'XGrid') && ~strcmpi(the_ring{i}.FamName, current_id)
         fprintf('%04i: %10s\n', i, the_ring{i}.FamName);
         current_id = the_ring{i}.FamName;
    end
    if isfield(the_ring{i},'K') && ~isfield(the_ring{i}, 'BendingAngle')
        fprintf('%04i: %10s -> %+09.6f\n', i, the_ring{i}.FamName, the_ring{i}.K);
    elseif isfield(the_ring{i}, 'XGrid') && ~strcmpi(the_ring{i}.FamName, current_id)
        fprintf('%04i: %10s\n', i, the_ring{i}.FamName);
        current_id = the_ring{i}.FamName;
    end
    if strcmpi(the_ring{i}.FamName, 'mb1')
        fprintf('\n');
    end
end
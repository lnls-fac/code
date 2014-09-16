function show_changes_in_quadrupole_strengths_for_machine_with_id(the_ring2, the_ring1)

clc;

% loads the_ring
if ~exist('the_ring','var')
    load('the_ring.mat'); the_ring1 = the_ring;
    load('the_ring_withids.mat'); the_ring2 = the_ring;
end

idx1 = setdiff(findcells(the_ring1, 'K'), findcells(the_ring1, 'BendingAngle'));
idx2 = setdiff(findcells(the_ring2, 'K'), findcells(the_ring2, 'BendingAngle'));
K1 = getcellstruct(the_ring1, 'K', idx1);
K2 = getcellstruct(the_ring2, 'K', idx2);

idx = 1; mia_nr = 1; mib_nr = 1; max_abs_var = 0; current_id = '';
for i=1:length(the_ring2)
    if strcmpi(the_ring2{i}.FamName, 'mia')
        fprintf('[ MIA-%02i ]\n', mia_nr);
        mia_nr = mia_nr + 1;
    end
    if strcmpi(the_ring2{i}.FamName, 'mib')
        fprintf('[ MIB-%02i ]\n', mib_nr);
        mib_nr = mib_nr + 1;
    end
    if isfield(the_ring{i},'K') && ~isfield(the_ring{i}, 'BendingAngle')
        k1 = the_ring1{idx1(idx)}.K; idx = idx + 1;
        k2 = the_ring2{i}.K;
        dk = 100*(k2-k1)/abs(k1);
        if (abs(dk) > max_abs_var), max_abs_var = abs(dk); end
        fprintf('%10s : K1 %+09.6f, K2 %+09.6f, dK %+09.6f, dK %+6.2f %%\n', the_ring{i}.FamName, k1, k2, k2-k1, dk);
    end
    if isfield(the_ring{i}, 'XGrid') && ~strcmpi(the_ring{i}.FamName, current_id)
        fprintf('<%s>\n', the_ring{i}.FamName);
        current_id = the_ring{i}.FamName;
    end
    if strcmpi(the_ring{i}.FamName, 'mb1')
        fprintf('---\n');
    end
end
fprintf('\n\n');
fprintf('Max. variation dK: %+6.2f\n', max_abs_var);
return;
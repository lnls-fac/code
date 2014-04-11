function r = correct_cod_fast(r, selection, sv_list, nr_iterations)

fprintf(['--- correct_cod [' datestr(now) '] ---\n']);

machine = r.machine;

if ischar(sv_list) && strcmpi(sv_list, 'all')
    sv_list = min(size(r.params.dynamic.cod_respm.S,1));
end

scale_x = 1e-9;
scale_y = 1e-9;

mi = findcells(r.params.the_ring,'FamName','mia');
mi = [mi findcells(r.params.the_ring,'FamName','mib')];
mi = sort([mi findcells(r.params.the_ring,'FamName','mc')]);
fprintf('    Dynamic COD @ beamlines exit     \n\n');
fprintf('%03s |   codx[nm]    |   cody[nm]    | max. kick [nrad]\n', 'i');
fprintf('    | (max)  (std)  | (max)  (std)  |   x     y   \n');

r.correctors.dynamic.orbit.hcm_str = zeros(length(selection),length(r.params.dynamic.hcm_idx));
r.correctors.dynamic.orbit.vcm_str = zeros(length(selection),length(r.params.dynamic.vcm_idx));
for i=selection
    
    if r.config.dynamic.calc_respm_cod_each_machine
        respm = calc_respm_cod(machine{i}, r.params.dynamic.bpm_idx, r.params.dynamic.hcm_idx, r.params.dynamic.vcm_idx, true);
        r.params.dynamic.cod_respm = respm.respm;
    end
    
    random_codx = r.errors.dynamic.errors_x(i,r.params.dynamic.bpm_idx);
    random_cody = r.errors.dynamic.errors_y(i,r.params.dynamic.bpm_idx);
    
    goal_codx = r.params.dynamic.ref_cod.codx(i,r.params.dynamic.bpm_idx) + random_codx;
    goal_cody = r.params.dynamic.ref_cod.cody(i,r.params.dynamic.bpm_idx) + random_cody;
    best_fm = Inf;
    for s=sv_list
        [machine{i} hkicks vkicks tcodx tcody] = cod_sg(r.params.dynamic, s, machine{i}, nr_iterations, goal_codx, goal_cody);
        fm = std([(tcodx(r.params.dynamic.bpm_idx)-goal_codx)/scale_x, (tcody(r.params.dynamic.bpm_idx)-goal_cody)/scale_y]);
        
        if (fm < best_fm)
            best_fm      = fm;
            best_hkicks  = hkicks;
            best_vkicks  = vkicks;
            best_machine = machine{i};
            best_codx    = tcodx;
            best_cody    = tcody;
        else
            machine{i} = best_machine;
        end
    end
    % restores best config of orbit correction singular values
    r.machine{i} = best_machine;
    hkicks     = best_hkicks;
    vkicks     = best_vkicks;
    codx_dyn = best_codx(mi)-r.params.dynamic.ref_cod.codx(i,mi);
    cody_dyn = best_cody(mi)-r.params.dynamic.ref_cod.cody(i,mi);
    
    %save value of correctors, for later statistics
    r.correctors.dynamic.orbit.hcm_str(i,:) = hkicks;
    r.correctors.dynamic.orbit.vcm_str(i,:) = vkicks;
    
    fprintf('%03i | %6.2f %6.2f | %6.2f %6.2f | %6.3f %6.3f \n', i, ...
        1e9*max(abs(codx_dyn)), 1e9*std(codx_dyn), ...
        1e9*max(abs(cody_dyn)), 1e9*std(cody_dyn), ...
        1e9*max(abs(hkicks)), 1e9*max(abs(vkicks)));
end
fprintf('\n');
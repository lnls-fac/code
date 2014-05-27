function r = correct_cod_slow(r, selection, sextupole_ramp, sv_list, nr_iterations)

fprintf(['--- correct_cod [' datestr(now) '] ---\n']);

machine = r.machine;

if ischar(sv_list) && strcmpi(sv_list, 'all')
    sv_list = min(size(r.params.static.cod_respm.S,1));
end

scale_x = 200e-6;
scale_y = 200e-6;

codx = zeros(length(machine), length(r.params.the_ring));
cody = zeros(length(machine), length(r.params.the_ring));
fprintf('%03s |   codx[um]    |   cody[um]    | max. kick [urad]\n', 'i');
fprintf('    | (max)  (std)  | (max)  (std)  |   x     y   \n');

r.correctors.static.orbit.hcm_str = zeros(length(selection),length(r.params.static.hcm_idx));
r.correctors.static.orbit.vcm_str = zeros(length(selection),length(r.params.static.vcm_idx));

if r.params.correct2bba_orbit
    ind_bba = get_bba_ind(r);
end

for i=selection
    
    sext_idx = getappdata(0, 'Sextupole_Idx');
    sext_str = getcellstruct(machine{i}, 'PolynomB', sext_idx, 1, 3);
    
    random_codx = r.errors.static.errors_x(i,r.params.static.bpm_idx);
    random_cody = r.errors.static.errors_y(i,r.params.static.bpm_idx);
    if r.params.correct2bba_orbit
        bba_codx = r.errors.static.errors_x(i,ind_bba);
        bba_cody = r.errors.static.errors_y(i,ind_bba);
    else
        bba_codx = 0;
        bba_cody = 0;
    end
    goal_codx = random_codx + bba_codx;
    goal_cody = random_cody + bba_cody;
    
    
    for j=1:length(sextupole_ramp)
              
        best_fm = Inf;
        machine{i} = set_sextupoles(machine{i}, sextupole_ramp(j), sext_str);
              
        for s=sv_list
            [machine{i}, hkicks, vkicks, tcodx, tcody] = cod_sg(r.params.static, s, machine{i}, nr_iterations, goal_codx, goal_cody);
            fm = std([(tcodx(r.params.static.bpm_idx)-goal_codx)/scale_x, (tcody(r.params.static.bpm_idx)-goal_cody)/scale_y]);
            %fm = max([(tcodx(r.params.static.bpm_idx)-goal_codx)/scale_x, (tcody(r.params.static.bpm_idx)-goal_cody)/scale_y]);
            %fm = max([(tcodx)/scale_x, (tcody)/scale_y]);
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
        machine{i} = best_machine;
        hkicks     = best_hkicks;
        vkicks     = best_vkicks;
        %if (j == 1),
        %   machine{i} = set_ids(machine{i}, 'on');
        %end
    end
    codx(i,:)    = best_codx;
    cody(i,:)    = best_cody;   
    %save value of correctors, for later statistics
    r.correctors.static.orbit.hcm_str(i,:) = hkicks;
    r.correctors.static.orbit.vcm_str(i,:) = vkicks;
    r.machine{i} = machine{i};
    fprintf('%03i | %6.2f %6.2f | %6.2f %6.2f | %6.2f %6.2f \n', i, ...
        1e6*max(abs(codx(i,:))), 1e6*std(codx(i,:)), ...
        1e6*max(abs(cody(i,:))), 1e6*std(cody(i,:)), ...
        1e6*max(abs(hkicks)), 1e6*max(abs(vkicks)));
 end
fprintf('\n');


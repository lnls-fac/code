function r = correct_cod_slow(r, selection, sextupole_ramp, sing_val, max_nr_iters,tolerancia)

if ischar(sing_val) && strcmpi(sing_val, 'all')
    sing_val = min(size(r.params.static.cod_respm.S,1));
end

fprintf(['--- correct_cod [' datestr(now) '] ---\n']);
fprintf('Sextupoles Ramp :');fprintf(' %4.2f ',sextupole_ramp);
fprintf('\nNumber Of Singular Values : %4d\n',sing_val);
fprintf('Max Number of Orbit Correction iterations : %4d\n',max_nr_iters);
fprintf('Tolerância : %7.2e\n\n', tolerancia);
machine = r.machine;

fprintf('%3s |   codx[um]    |   cody[um]    | maxkick[urad] | nr_iters | nr_str_red\n', 'i');
fprintf('    | (max)  (std)  | (max)  (std)  |   x      y    |          |\n');

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
    
    nr_iters = zeros(1,length(sextupole_ramp));
    n_times = nr_iters;
    for j=1:length(sextupole_ramp)
              
        machine{i} = set_sextupoles(machine{i}, sextupole_ramp(j), sext_str);
        [machine{i}, hkicks, vkicks, codx, cody, nr_iters(j), n_times(j)] = ...
                        cod_sg(r.params.static, sing_val, machine{i}, max_nr_iters, ...
                        goal_codx, goal_cody, tolerancia);
        
        %if (j == 1),
        %   machine{i} = set_ids(machine{i}, 'on');
        %end
        % adicionei essa condicao para o script indicar que a máquina é instável.
        if any(isnan([codx,cody]))
            fprintf('Machine %03i unstable @ sextupole ramp = %5.1f %%\n',i,sextupole_ramp(j)*100);
            machine{i} = set_sextupoles(machine{i}, 1, sext_str);
            break;
        end
    end

    %save value of correctors, for statistics
    r.correctors.static.orbit.hcm_str(i,:) = hkicks;
    r.correctors.static.orbit.vcm_str(i,:) = vkicks;
    r.machine{i} = machine{i};
    
    fprintf('%03i | %6.2f %6.2f | %6.2f %6.2f | %6.2f %6.2f |', i, ...
        1e6*max(abs(codx)), 1e6*std(codx), 1e6*max(abs(cody)), 1e6*std(cody), ...
        1e6*max(abs(hkicks)), 1e6*max(abs(vkicks)));
    stri = sprintf(' %2d /', nr_iters); fprintf('%9s |',stri(1:end-1));
    stri = sprintf(' %2d /', n_times); fprintf('%9s \n',stri(1:end-1));
 end
fprintf('\n');
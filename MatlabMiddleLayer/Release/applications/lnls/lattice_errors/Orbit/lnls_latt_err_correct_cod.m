function machine = correct_cod(name, machine, orbit, goal_codx, goal_cody)

nr_mach = length(machine);

if ~exist('goal_codx','var')
    goal_codx = zeros(nr_mach,length(orbit.bpm_idx));
elseif size(goal_codx,1) == 1
    goal_codx = repmat(goal_codx,nr_mach,1);
end
if ~exist('goal_cody','var')
    goal_cody = zeros(nr_mach,length(orbit.bpm_idx));
elseif size(goal_cody,1) == 1
    goal_cody = repmat(goal_cody,nr_mach,1);
end

save([name,'_correct_cod_input.mat'], 'orbit', 'goal_codx', 'goal_cody');

calc_respm = false;
if ~isfield(orbit,'respm'), calc_respm = true; end

fprintf(['\nCorrecting COD [' datestr(now) ']:\n']);
fprintf('Sextupoles Ramp :');fprintf(' %4.2f ',orbit.sext_ramp);
if isnumeric(orbit.svs), svs = num2str(orbit.svs);else svs = orbit.svs;end
fprintf('\nNumber Of Singular Values : %4s\n',svs);
fprintf('Max Number of Orbit Correction iterations : %4d\n',orbit.max_nr_iter);
fprintf('Tolerância : %7.2e\n\n', orbit.tolerance);
fprintf('%3s |   codx[um]    |   cody[um]    | maxkick[urad] | nr_iters | nr_str_red\n', 'i');
fprintf('    | (max)  (std)  | (max)  (std)  |   x      y    |          |\n');


if orbit.correct2bba_orbit
    ind_bba = get_bba_ind(machine{1});
end

sext_idx = findcells(machine{1},'PolynomB');
random_cod = zeros(2,length(orbit.bpm_idx));
for i=1:nr_mach
    sext_str = getcellstruct(machine{i}, 'PolynomB', sext_idx, 1, 3);
    
    if orbit.simul_bpm_err
        random_cod = getcellstruct(machine{i},'Offsets',orbit.bpm_idx);
        random_cod = cell2mat(random_cod)';
    end
    if orbit.correct2bba_orbit
        T1 = getcellstruct(machine{i},'T1',ind_bba,1,1);
        T2 = getcellstruct(machine{i},'T2',ind_bba,1,1);
        bba_codx = (T2-T1)'/2;
        T1 = getcellstruct(machine{i},'T1',ind_bba,1,3);
        T2 = getcellstruct(machine{i},'T2',ind_bba,1,3);
        bba_cody = (T2-T1)'/2;
    else
        bba_codx = 0;
        bba_cody = 0;
    end
    gcodx = goal_codx(i,:) + random_cod(1,:) + bba_codx;
    gcody = goal_cody(i,:) + random_cod(2,:) + bba_cody;
    
    niter = zeros(1,length(orbit.sext_ramp));
    ntimes = niter;
    for j=1:length(orbit.sext_ramp)
        machine{i} = setcellstruct(machine{i},'PolynomB',sext_idx,orbit.sext_ramp(j)*sext_str, 1, 3);
        if calc_respm
            orbit.respm = calc_respm_cod(machine{i}, orbit.bpm_idx, orbit.hcm_idx, orbit.vcm_idx);
            orbit.respm = orbit.respm.respm;
        end
        [machine{i},hkck,vkck,codx,cody,niter(j),ntimes(j)] = cod_sg(orbit, machine{i}, gcodx, gcody);
        if any(isnan([codx,cody]))
            fprintf('Machine %03i unstable @ sextupole ramp = %5.1f %%\n',i,sextupole_ramp(j)*100);
            machine{i} = setcellstruct(machine{i},'PolynomB',sext_idx, sext_str, 1, 3);
            break;
        end
    end
   
    fprintf('%03i | %6.2f %6.2f | %6.2f %6.2f | %6.2f %6.2f |', i, ...
        1e6*max(abs(codx)), 1e6*std(codx), 1e6*max(abs(cody)), 1e6*std(cody), ...
        1e6*max(abs(hkck)), 1e6*max(abs(vkck)));
    stri = sprintf(' %2d /', niter); fprintf('%9s |',stri(1:end-1));
    stri = sprintf(' %2d /', ntimes); fprintf('%9s \n',stri(1:end-1));
 end
fprintf('\n');
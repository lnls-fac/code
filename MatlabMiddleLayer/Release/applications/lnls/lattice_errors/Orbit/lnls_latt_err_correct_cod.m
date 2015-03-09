function machine = lnls_latt_err_correct_cod(name, machine, orbit, goal_codx, goal_cody)
% function machine = lnls_latt_err_correct_cod(name, machine, orbit, goal_codx, goal_cody)
%
% Correct orbit of several machines.
%
% INPUTS:
%   name     : name of the file to which the inputs will be saved
%   machine  : cell array of lattice models to correct the orbit.
%   goal_codx: horizontal reference orbit to use in correction. May be a vector
%      defining the orbit for each bpm. In this case the reference will be the
%      same for all the machines. Or Can be a matrix with dimension
%      nr_machines X nr_bpms, to define different orbits among the machines.
%      If not passed a default of zero will be used;
%   goal_cody: same as goal_codx but for the vertical plane.
%   orbit    : structure with fields:
%      bpm_idx   - bpm indexes in the model;
%      hcm_idx   - horizontal correctors indexes in the model;
%      vcm_idx   - vertical correctors indexes in the model;
%      sext_ramp - If existent, must be a vector with components less than
%         one, denoting a fraction of sextupoles strengths used in each step
%         of the correction. For example, if sext_ramp = [0,1] the correction
%         algorithm will be called two times for each machine. In the first
%         time the sextupoles strengths will be zeroed and in the second
%         time they will be set to their correct value.
%      svs      - may be a number denoting how many singular values will be
%         used in the correction or the string 'all' to use all singular
%         values. Default: 'all';
%      max_nr_iter - maximum number of iteractions the correction
%         algortithm will perform at each call for each machine;
%      tolerance - if in two subsequent iteractions the relative difference
%         between the error function values is less than this value the
%         correction is considered to have converged and will terminate.
%      correct2bba_orbit - if true, the goal orbit will be set in relation
%         to the magnetic center of the quadrupole nearest to each bpm.
%      simul_bpm_err - if true, the Offset field defined in the bpms in the
%         lattice will be used to simulate an error in the determination of
%         the goal orbit. Notice that there must exist an Offset field defined
%         in the lattice models of the machine array for each bpm, in order to
%         this simulation work. Otherwise an error will occur.
%      respm - structure with fields M, S, V, U which are the response
%         matrix and its SVD decomposition. If NOT present, the function
%         WILL CALCULATE the response matrix for each machine in each step
%         defined by sext_ramp.
%
% OUTPUT:
%   machine : cell array of lattice models with the orbit corrected.
%      

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

if ~isfield(orbit,'sext_ramp'), orbit.sext_ramp = 1; end;

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
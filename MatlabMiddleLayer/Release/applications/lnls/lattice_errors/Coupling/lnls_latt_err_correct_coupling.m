function machine = lnls_latt_err_correct_coupling(name, machine, coup)
% function machine = lnls_latt_err_correct_optics(name, machine, coup)
%
% Correct coupling of several machines.
%
% INPUTS:
%   name     : name of the file to which the inputs will be saved;
%   machine  : cell array of lattice models to symmetrize the optics.
%   coup     : structure with fields:
%      bpm_idx   - bpm indexes in the model;
%      hcm_idx   - horizontal correctors indexes in the model;
%      vcm_idx   - vertical correctors indexes in the model;
%      scm_idx   - indexes of the skew quads which will be used to symmetrize;
%      svs       - may be a number denoting how many singular values will be
%         used in the correction or the string 'all' to use all singular
%         values. Default: 'all';
%      max_nr_iter - maximum number of iteractions the correction
%         algortithm will perform at each call for each machine;
%      tolerance - if in two subsequent iteractions the relative difference
%         between the error function values is less than this value the
%         correction is considered to have converged and will terminate.
%      simul_bpm_corr_err - if true, the Gains field defined in the bpms  and 
%         the Gain field defined in the correctors in thelattice will be used
%         to simulate gain errors in these elements, changing the response
%         matrix calculated. Notice that the supra cited fields must exist
%         in the lattice models of the machine array for each bpm and corrector
%         in order for this this simulation to work. Otherwise an error will occur.
%      respm - structure with fields M, S, V, U which are the coupling response
%         matrix and its SVD decomposition. If NOT present, the function
%         WILL CALCULATE the coupling response matrix for each machine.
%
% OUTPUT:
%   machine : cell array of lattice models with the orbit corrected.

nr_machines = length(machine);

calc_respm = false;
if ~isfield(coup,'respm'), calc_respm = true; end

save([name,'_correct_coup_input.mat'], 'coup');

fprintf(['--- correct_coupling [' datestr(now) '] ---\n']);
if isnumeric(coup.svs), svs = num2str(coup.svs);else svs = coup.svs;end
fprintf('\nNumber Of Singular Values : %4s\n',svs);
fprintf('Max Number of Correction iterations : %4d\n',coup.max_nr_iter);
fprintf('Tolerância : %7.2e\n\n', coup.tolerance);

fprintf('mac | Max Kl |  chi2  | Tilt  |      Coup[%%]      | NIters | NRedStr\n');
fprintf('    | [1/km] |        | [deg] |  Ey/Ex  | Tracking|        |\n');
fprintf('%s',repmat('-',1,69));
for i=1:nr_machines
        R=0;
        T = 0;
        try
            [T, ~, ~, ~, R, ~, ~, ~, ~] = calccoupling(machine{i});
        end
        
        if calc_respm
            [respm, ~] = calc_respm_coupling(machine{i}, coup);
            coup.respm = respm;
        end
        
        RTr = mean(lnls_calc_emittance_coupling(machine{i}));
        [machine{i}, skewstr, iniFM, bestFM, iter, n_times] = coup_sg(machine{i}, coup);
        RTr2 = mean(lnls_calc_emittance_coupling(machine{i}));
        R2=0;
        T2 = 0;
        try
            [T2, ~, ~, ~, R2, ~, ~, ~, ~] = calccoupling(machine{i});
        end
        %fprintf('%03i| skewstr[1/m^2] %+6.4f(max) %6.4f(std) | coup %8.5f (std) | tilt[deg] %5.2f -> %5.2f (std), k[%%] %5.2f -> %5.2f (std)\n', i, max(abs(skewstr)), std(skewstr), best_fm, std(Tilt)*180/pi, std(Tilt2)*180/pi, 100*Ratio, 100*Ratio2);
        fprintf('\n%03d | %6s | %6.3f | %5.2f | %7.3f | %7.3f |  %4s  |  %4s \n',...
            i, ' ', iniFM, std(T)*180/pi,  100*[R, RTr],' ',' ');  
        fprintf('%3s | %6.2f | %6.3f | %5.2f | %7.4f | %7.4f |  %4d  |  %4d \n',...
            ' ', 1000*max(abs(skewstr)), bestFM, std(T2)*180/pi,  100*[R2, RTr2], iter, n_times);
        fprintf('%s',repmat('-',1,69));
end
fprintf('\n');
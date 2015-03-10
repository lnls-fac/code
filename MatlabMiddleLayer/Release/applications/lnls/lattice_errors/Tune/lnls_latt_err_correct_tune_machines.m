function machine = lnls_latt_err_correct_tune_machines(tune, machine)
% function machine = lnls_latt_err_correct_optics(name, machine, coup)
%
% Correct tune of several machines.
%
% INPUTS:
%   machine : cell array of lattice models to symmetrize the optics.
%   tune    : structure with fields
%      families - families of quadrupoles to be used in correction;
%      goal - desired tunes;
%      max_iter - maximum number of iteractions to be performed;
%      tolerance - if at some iteraction the difference the disered and
%         current tunes is less than this value, the correction is considered
%         to have converged and will terminate.
%
% OUTPUT:
%   machine : cell array of lattice models with the tune corrected.
%

fprintf(['--- correct_tunes [' datestr(now) '] ---\n']);
fprintf('Goal Tunes :');fprintf(' %7.4f ',tune.goal);
fprintf('\nFamilies Used for Correction :');fprintf(' %s ',tune.families{:});
fprintf('\nMax Number of Orbit Correction iterations : %4d\n',tune.max_iter);
fprintf('Tolerância : %7.2e\n\n', tune.tolerance);

fprintf('%3s | %15s | %9s | %15s \n', 'mac','initial tunes', 'converge?', 'final tunes');
for i=1:length(machine)
    [machine{i}, converged, tunes0, tunesi] = lnls_correct_tunes(machine{i}, tune.families, ...
        tune.goal, tune.max_iter, tune.tolerance);
    if converged
        fprintf('%03i | %7.4f %7.4f | %9s | %7.4f %7.4f \n', i, tunesi,'   yes   ', tunes0);
    else
        fprintf('%03i | %7.4f %7.4f | %9s | %7.4f %7.4f \n', i, tunesi,'   no    ', tunes0);
    end
end

fprintf('\n');
function machine = correct_tune_machines(tune, machine)

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
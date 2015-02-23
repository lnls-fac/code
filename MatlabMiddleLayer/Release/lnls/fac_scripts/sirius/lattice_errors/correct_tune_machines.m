function machine = correct_tune_machines(r, selection)

fprintf(['--- correct_tunes [' datestr(now) '] ---\n']);
fprintf('Goal Tunes :');fprintf(' %7.4f ',r.params.static.tune_goal);
fprintf('\nFamilies Used for Correction :');fprintf(' %s ',r.params.static.tune_families{:});
fprintf('\nMax Number of Orbit Correction iterations : %4d\n',r.params.static.tune_max_iter);
fprintf('Tolerância : %7.2e\n\n', r.params.static.tune_tolerancia);
machine = r.machine;

fprintf('%3s | %15s | %9s | %15s \n', 'mac','initial tunes', 'converge?', 'final tunes');
for i=selection
    [machine{i}, converged, tunes0, tunesi] = lnls_correct_tunes(machine{i}, r.params.static.tune_families, ...
        r.params.static.tune_goal, r.params.static.tune_max_iter, r.params.static.tune_tolerancia);
    if converged
        fprintf('%03i | %7.4f %7.4f | %9s | %7.4f %7.4f \n', i, tunesi,'   yes   ', tunes0);
    else
        fprintf('%03i | %7.4f %7.4f | %9s | %7.4f %7.4f \n', i, tunesi,'   no    ', tunes0);
    end
end

fprintf('\n');
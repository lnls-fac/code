function machine = correct_tune_machines(r, selection)

fprintf(['--- correct_tunes [' datestr(now) '] ---\n']);

machine = r.machine;

fprintf('%3s | %9s | %11s %7.4f %7.4f\n', 'i', 'converged', 'goal_tunes:', r.params.static.tune_goal);
for i=selection
    [machine{i}, converged, tunes0] = correct_tunes(machine{i}, r.params.static.tune_families, ...
        r.params.static.tune_goal, r.params.static.tune_max_iter, r.params.static.tune_tolerancia);
    if converged
        fprintf('%03i | %9s |\n', i, '   yes   ');
    else
        fprintf('%03i | %9s | %11s %7.4f %7.4f \n', i, '   no    ', 'tunes:',tunes0);
    end
end

fprintf('\n');
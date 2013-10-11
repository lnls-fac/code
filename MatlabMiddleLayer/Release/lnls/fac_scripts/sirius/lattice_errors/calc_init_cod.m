function init_cod = calc_init_cod(r, selection)

fprintf(['--- calc_closed_orbit [' datestr(now) '] ---\n']);
for i=selection
    r.machine{i} = set_sextupoles(r.machine{i}, 0);
    [codx cody] = calc_cod(r.machine{i});
    init_cod.codx(i,:) = codx;
    init_cod.cody(i,:) = cody;
    fprintf('%03i| codx[mm] %6.3f(max) %6.3f(std) %+7.3f(avg) | cody[mm] %6.3f(max) %6.3f(std) %+7.3f(avg)\n', i, 1e3*max(abs(codx)), 1e3*std(codx), 1e3*mean(codx), 1e3*max(abs(cody)), 1e3*std(cody), 1e3*mean(cody));
end
dlmwrite([r.config.label '_codx_sextoff_nocor.dat'],    1e3*init_cod.codx, 'precision',    '%+8.4f', 'newline', 'pc', 'delimiter', ' ');
dlmwrite([r.config.label '_cody_sextoff_nocor.dat'],    1e3*init_cod.cody, 'precision',    '%+8.4f', 'newline', 'pc', 'delimiter', ' ');
fprintf('\n');


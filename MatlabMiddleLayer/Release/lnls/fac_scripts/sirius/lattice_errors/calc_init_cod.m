function init_cod = calc_init_cod(r, selection)

fprintf(['--- calc_closed_orbit [' datestr(now) '] ---\n\n']);
fprintf('%3s|       codx[mm]       |       codx[mm]       \n', 'ind');
fprintf('   |   (max)  (std)  (avg)  | (max)  (std)  (avg)  \n');
for i=selection
    sext_idx = getappdata(0, 'Sextupole_Idx');
    sext_str = getcellstruct(r.params.the_ring, 'PolynomB', sext_idx, 1, 3);
    r.machine{i} = set_sextupoles(r.machine{i}, 0, sext_str);
    %r.machine{i} = set_ids(r.machine{i}, 'off');
    [codx, cody] = calc_cod(r.machine{i});
    %r.machine{i} = set_ids(r.machine{i}, 'on');
    init_cod.codx(i,:) = codx;
    init_cod.cody(i,:) = cody;
    fprintf('%03i| %6.2f %6.2f %6.2f | %6.2f %6.2f %6.2f \n', i, ...
        1e3*max(abs(codx)), 1e3*std(codx), 1e3*mean(codx), ...
        1e3*max(abs(cody)), 1e3*std(cody), 1e3*mean(cody));
end
% dlmwrite([r.config.label '_codx_sextoff_nocor.dat'],    1e3*init_cod.codx, 'precision',    '%+8.4f', 'newline', 'pc', 'delimiter', ' ');
% dlmwrite([r.config.label '_cody_sextoff_nocor.dat'],    1e3*init_cod.cody, 'precision',    '%+8.4f', 'newline', 'pc', 'delimiter', ' ');
fprintf('\n');


function tracy3_read_machines_generate_flat_file(archive_name,inicio)
%function tracy3_read_machines_generate_flat_file(archive_name)
%function tracy3_read_machines_generate_flat_file(archive_name,inicio)
%
% History
%
% 2013-05-01: Ximenes. Adicionei opção de browser pelo arquivo com máquinas aleatórias. Também adicionei rotina que shifta modelo do anel.
% 2012-??-??: Fernando. versão inicial.

if ~exist('archive_name','var')
    [FileName,path,~] = uigetfile('*.mat','select machines file',fullfile(pwd, 'cod_matlab', 'CONFIG_machines_cod_corrected.mat'));
    if isnumeric(path), return; end;
    machines = load(fullfile(path, FileName));
    path = pwd;
else
    % path = '~/redes_tracy/Sirius/Sirius_v200/flat_files/AC10_test/orb_cor/';
    path = pwd;
    machines = load([path '/cod_matlab/' archive_name '.mat']);
end

[status result] = system('ls | grep rms | wc -l');
n_pastas = str2double(result);

if(n_pastas~=length(machines.machine))
    error('inconsistent: either pwd not correct or n_pasts <> length(machines)');
    return;
end

for i=1:n_pastas
    flat_name = [sprintf('rms%02d', i) sprintf('/rms%02d', i) '.dat'];
    full_name = fullfile(path, flat_name);
    the_ring = machines.machine{i};
    if exist('inicio','var')
        the_ring = start_at_first_element(the_ring, inicio);
    end
%     the_ring = modify_the_ring(machines.machine{i});
    lnls_at2tracyflat(the_ring,full_name);
end

function the_ring = modify_the_ring(the_ring_old)

the_ring = the_ring_old;
idx = findcells(the_ring, 'FamName', 'IDm');
for i=1:length(idx)
    polyB = the_ring{idx(i)}.PolynomB;
    polyBnew = polyB .* (2*(rand(1,length(polyB)) - 0.5));
    the_ring{idx(i)}.PolynomB = polyBnew;
end


function the_ring = start_at_first_element(the_ring_old, famname)

idx = findcells(the_ring_old, 'FamName', famname);
the_ring = [the_ring_old(idx(1):end) the_ring_old(1:(idx(1)-1))];
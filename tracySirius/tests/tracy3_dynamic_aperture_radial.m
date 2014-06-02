function tracy3_dynamic_aperture_radial


path = '/home/fac_files/data/sirius_tracy/';
path = '/home/fac_files/code/tracySirius/tests';
path = uigetdir(path,'Em qual pasta estao os dados?');
if (path==0); return; end;
     
[~, result] = system(['find ' path ' -type d | grep rms | wc -l']);
n_pastas = str2double(result);

for i=1:n_pastas
    if (i == 1)
        figure; hold all;
    end
    data = importdata('daxy_radial.out', ' ', 4); data = data.data;
    plot(1000*data(:,1), 1000*data(:,2), 'x', 'MarkerSize', 10, 'Color', [0,0,0]);
end


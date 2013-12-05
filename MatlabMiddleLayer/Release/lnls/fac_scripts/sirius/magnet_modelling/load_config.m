function parms = load_config(config)

pathstr = fullfile('D:\Arq\fac_files\data\sirius_mml\magnet_modelling', 'CONFIGS', config);
addpath(pathstr); 
parms = CONFIG(pathstr);
rmpath(pathstr);

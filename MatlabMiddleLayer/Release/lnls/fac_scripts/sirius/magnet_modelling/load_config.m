function parms = load_config(config)

pathstr = fullfile(lnls_get_root_folder(), 'data','sirius_mml','magnet_modelling', 'CONFIGS', config);
addpath(pathstr); 
parms = CONFIG(pathstr);
rmpath(pathstr);

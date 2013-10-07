function parms = load_config(config)

pathstr = fullfile('CONFIGS', config);
addpath(pathstr); 
parms = CONFIG(pathstr); 
rmpath(pathstr);

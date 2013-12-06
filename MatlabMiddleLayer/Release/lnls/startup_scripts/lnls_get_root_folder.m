function root_folder = lnls_get_root_folder()

if strcmpi(computer, 'PCWIN') || strcmpi(computer, 'PCWIN64')
    if exist(['C:' filesep 'Arq'], 'file')
        root_folder = ['C:' filesep 'Arq' filesep 'fac_files'];
    else
        root_folder = ['D:' filesep 'Arq' filesep 'fac_files'];
    end
else
    root_folder = '/home/fac_files';
end
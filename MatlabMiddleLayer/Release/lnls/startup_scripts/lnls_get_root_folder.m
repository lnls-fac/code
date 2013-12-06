function root_folder = get_lnls_root_folder()

if strcmpi(computer, 'PCWIN') || strcmpi(computer, 'PCWIN64')
    if exist(['C:' filesep 'Arq'], 'file')
        root_folder = ['C:' filesep 'Arq'];
    else
        root_folder = ['D:' filesep 'Arq'];
    end
else
    root_folder = ['/home'];
end
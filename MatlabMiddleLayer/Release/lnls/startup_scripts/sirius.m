function sirius(varargin)
% Inicializa as estruturas do MML-LNLS e conecta com servidor LNLS1LinkS
%
% Historico
% 
% 2011-06-02: c??pia modificada da vers??o do LNLS1
% 2011-04-28: nova vers??o. script transformado em fun????o.
% 2010-09-16: coment??rios iniciais no c??digo

Disconnect = false;

default_version = '_V500';

for i=length(varargin):-1:1
    if ischar(varargin{i})
        if any(strcmpi(varargin{i}, {'SelectServer'})), SelectServer = true; end;
        if any(strcmpi(varargin{i}, {'NoServer'})), NoServer = true; end;
        if any(strcmpi(varargin{i}, {'Disconnect'})), Disconnect = true; end;
        if ~isempty(strfind(varargin{i}, '_V')), default_version = varargin{i}; end;
    end
end

if Disconnect
    try
        lnls1_comm_disconnect;
        rmappdata(0, 'PVServer');
        switch2sim;
    catch
    end
    return;
end

% inicializa estruturas do MML
cdir = pwd;
root_folder = get_lnls_root_folder();
cd(fullfile(root_folder, 'fac_files', 'code', 'MatlabMiddleLayer','Release','mml'))

setpathsirius(['SIRIUS' default_version], 'StorageRing', 'sirius_link');
cd(cdir);
clear cdir;

addpath(genpath(fullfile(root_folder, 'fac_files', 'code', 'MatlabMiddleLayer','Release','lnls','fac_scripts','sirius','lattice_errors')));
addpath(fullfile(root_folder, 'fac_files', 'code', 'MatlabMiddleLayer','Release','lnls','fac_scripts','tracy3'), '-begin');
addpath(genpath(fullfile(root_folder, 'fac_files', 'code', 'MatlabMiddleLayer','Release','machine','LTBA_V200')));


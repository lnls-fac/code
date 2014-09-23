function sirius(varargin)
% Inicializa as estruturas do MML-LNLS e conecta com servidor LNLS1LinkS
%
% Historico
%
% 2011-06-02: c??pia modificada da vers??o do LNLS1
% 2011-04-28: nova vers??o. script transformado em fun????o.
% 2010-09-16: coment??rios iniciais no c??digo

Disconnect = false;

default_version = '_V03';

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
root_folder = lnls_get_root_folder();
cd(fullfile(root_folder, 'code', 'MatlabMiddleLayer','Release','mml'))

% remove toolbox/finance/finsupport/ do path para previnir conflito com
% funcao drift da Financial Toolbox (se pasta est?? no caminho, para evitar warningMessage)
fins = fullfile(matlabroot, 'toolbox', 'finance', 'finsupport');
if ~isempty(strfind(path, fins))
    rmpath(fins);
end

setpathsirius(['SIRIUS' default_version], 'StorageRing', 'sirius_link');
cd(cdir);
clear cdir;

addpath(genpath(fullfile(root_folder, 'code', 'MatlabMiddleLayer','Release','lnls','fac_scripts','sirius','lattice_errors')));
addpath(fullfile(root_folder, 'code', 'MatlabMiddleLayer','Release','lnls','fac_scripts','tracy3'), '-begin');
addpath(fullfile(root_folder, 'code', 'MatlabMiddleLayer','Release','lnls','fac_scripts','trackcpp'), '-begin');
addpath(genpath(fullfile(root_folder, 'code', 'MatlabMiddleLayer','Release','machine','LTBA_V200')));

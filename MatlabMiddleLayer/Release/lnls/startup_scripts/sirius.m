function sirius_new(varargin)
% Inicializa as estruturas do MML-LNLS e conecta com servidor LNLS1LinkS
%
% Historico
%
% 2011-06-02: copia modificada da versao do LNLS1
% 2011-04-28: nova versao. script transformado em funcao.
% 2010-09-16: comentarios iniciais no codigo

Disconnect = false;

default_version = 'SI.V03';

for i=length(varargin):-1:1
    if ischar(varargin{i})
        if any(strcmpi(varargin{i}, {'SelectServer'})), SelectServer = true; end;
        if any(strcmpi(varargin{i}, {'NoServer'})), NoServer = true; end;
        if any(strcmpi(varargin{i}, {'Disconnect'})), Disconnect = true; end;
        if ~isempty(strfind(varargin{i}, 'V')), default_version = varargin{i}; end;
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
mmlpaths = textscan(path(), '%s', 'delimiter', pathsep); mmlpaths = mmlpaths{1};
for i=1:length(mmlpaths)
    if ~isempty(strfind(mmlpaths{i},'MatlabMiddleLayer')) && isempty(strfind(mmlpaths{i}, 'startup_scripts'))
        rmpath(mmlpaths{i})
    end
end

setpathsirius('SIRIUS', default_version, 'sirius_link');
cd(cdir);
clear cdir;

addpath(genpath(fullfile(root_folder, 'code', 'MatlabMiddleLayer','Release','lnls','fac_scripts','sirius','lattice_errors')));
addpath(fullfile(root_folder, 'code', 'MatlabMiddleLayer','Release','lnls','fac_scripts','tracy3'), '-begin');
addpath(fullfile(root_folder, 'code', 'MatlabMiddleLayer','Release','lnls','fac_scripts','trackcpp'), '-begin');

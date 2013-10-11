function sirius_booster(versao, varargin)
% Inicializa as estruturas do MML-LNLS e conecta com servidor LNLS1LinkS
%
% Hist???rico
% 
% 2011-06-02: c???pia modificada da vers???o do LNLS1
% 2011-04-28: nova vers???o. script transformado em fun??????o.
% 2010-09-16: coment???rios iniciais no c???digo

Disconnect = false;

for i=length(varargin):-1:1
    if ischar(varargin{i})
        if any(strcmpi(varargin{i}, {'SelectServer'})), SelectServer = true; end;
        if any(strcmpi(varargin{i}, {'NoServer'})), NoServer = true; end;
        if any(strcmpi(varargin{i}, {'Disconnect'})), Disconnect = true; end;
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

try
    cd('C:\Arq\MatlabMiddleLayer\Release\mml\');
catch
    cd('/opt/MatlabMiddleLayer/Release/mml/');
end

if ~exist('versao', 'var')
    versao = 'V701';
end
setpathlnls(['BOOSTER_' versao],'StorageRing', 'sirius_link');
cd(cdir);
clear cdir;

if strcmpi(computer, 'PCWIN')
    addpath(genpath('C:\Arq\MatlabMiddleLayer\Release\lnls\fac_scripts\sirius\lattice_errors'));
    addpath(fullfile('C:\Arq\MatlabMiddleLayer\Release', 'lnls', 'fac_scripts', 'tracy3'), '-begin');
    addpath(genpath('C:\Arq\MatlabMiddleLayer\Release\machine\LTLB_V100'));
    addpath(genpath('C:\Arq\MatlabMiddleLayer\Release\machine\LTBA_V100'));
else
    addpath(genpath('/opt/MatlabMiddleLayer/Release/lnls/fac_scripts/sirius/lattice_errors'));
    addpath(genpath('/opt/MatlabMiddleLayer/Release/lnls/fac_scripts/tracy3'));
    addpath(genpath('/opt/MatlabMiddleLayer/Release/machine/LTLB_V100'));
    addpath(genpath('/opt/MatlabMiddleLayer/Release/machine/LTBA_V100'));
end

return;
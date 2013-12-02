function sirius_ltlb(varargin)
%
% Historico
% 
% 2013-12-02: inicio

Disconnect = false;

default_version_sr   = '_V500';
default_version_ltlb = '_V200';

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
if any(strcmpi(computer, {'PCWIN', 'PCWIN64'}))
    cd('C:\Arq\MatlabMiddleLayer\Release\mml\');
else
    cd('/home/fac_files/code/MatlabMiddleLayer/Release/mml/');
end

setpathsirius(['SIRIUS' default_version_sr], ['LTLB' default_version_ltlb], 'sirius_link');
cd(cdir);
clear cdir;

if any(strcmpi(computer, {'PCWIN','PCWIN64'}))
    addpath(genpath('C:\Arq\MatlabMiddleLayer\Release\lnls\fac_scripts\sirius\lattice_errors'));
    addpath(fullfile('C:\Arq\MatlabMiddleLayer\Release', 'lnls', 'fac_scripts', 'tracy3'), '-begin');
else
    addpath(genpath('/home/fac_files/code/MatlabMiddleLayer/Release/lnls/fac_scripts/sirius/lattice_errors'));
    addpath(genpath('/home/fac_files/code/MatlabMiddleLayer/Release/lnls/fac_scripts/tracy3'));
end

return;



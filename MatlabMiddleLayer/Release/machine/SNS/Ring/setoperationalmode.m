function setoperationalmode(ModeNumber)
%SETOPERATIONALMODE - Switches between the various operational modes
%  setoperationalmode(ModeNumber)
%
%  See also aoinit, updateatindex, snsinit

% to do
% 1. golden chro?
% 2. hw2physics converstions
% 3. channel names
% 4. tolerances


global THERING

% Check if the AO exists
checkforao;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Accelerator Dependent Modes %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if nargin < 1
    ModeNumber = [];
end
if isempty(ModeNumber)
    %ModeNumber = 1;
    ModeCell = {'SNS Operations', 'SNS Model'};
    [ModeNumber, OKFlag] = listdlg('Name','SNS','PromptString','Select the Operational Mode:', 'SelectionMode','single', 'ListString', ModeCell, 'ListSize', [450 200]);
    if OKFlag ~= 1
       fprintf('   Operational mode not changed\n');
       return
    end
    if ModeNumber == 2
       ModeNumber = 101;  % Model
    end
end



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Accelerator Data Structure %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
AD = getad;
AD.Machine = 'SNS';             % Will already be defined if setpathmml was used
AD.SubMachine = 'Ring';         % Will already be defined if setpathmml was used
AD.OperationalMode = '';        % Gets filled in later
AD.Energy = 1.783272;           % Make sure this is the same as bend2gev at the production lattice!
AD.InjectionEnergy = 1.783272;
AD.HarmonicNumber = 1;

% Defaults RF for disperion and chromaticity measurements (must be in Hardware units)
AD.DeltaRFDisp = 1000e-6;
AD.DeltaRFChro = [-2000 -1000 0 1000 2000] * 1e-6;


% Tune processor delay: delay required to wait
% to have a fresh tune measurement after changing
% a variable like the RF frequency.
AD.TuneDelay = 0.0;


% SP-AM Error level
% AD.ErrorWarningLevel = 0 -> SP-AM errors are Matlab errors {Default}
%                       -1 -> SP-AM errors are Matlab warnings
%                       -2 -> SP-AM errors prompt a dialog box
%                       -3 -> SP-AM errors are ignored (ErrorFlag=-1 is returned)
AD.ErrorWarningLevel = 0;


%%%%%%%%%%%%%%%%%%%%%
% Operational Modes %
%%%%%%%%%%%%%%%%%%%%%

% Mode setup variables (mostly path and file names)
% AD.OperationalMode - String used in titles
% MachineName - String used to build directory structure off DataRoot
% ModeName - String used for mode directory name off DataRoot/MachineName
% OpsFileExtension - string add to default file names
MachineName = lower(AD.Machine);
if ModeNumber == 1
    % Experimental mode
    AD.OperationalMode = 'SNS 1.78 GeV';
    ModeName = 'Experimental';
    OpsFileExtension = '_SNS';

    % AT lattice
    AD.ATModel = 'snslattice';
    %snslattice;
    
    % Golden TUNE is with the TUNE family
    AO = getao;
    AO.TUNE.Monitor.Golden = [
        0.4133
        0.3633
        NaN];
    setao(AO);

    % Golden chromaticity is in the AD (must be in Physics units!)
    AD.Chromaticity.Golden = [.5; .5];  % ???

    % This is a bit of a cluge to know if the user is on the SNS filer
    % If so, then the MML user probably wants to be online
    MMLROOT = getmmlroot;
    if isempty(findstr(lower(MMLROOT),'SomeDirectoryAtSNS'))
        switch2sim;
    else
        switch2online;
    end
    switch2hw;

elseif ModeNumber == 101
    % Model mode
    AD.OperationalMode = 'SNS 1.78 GeV - Model';
    ModeName = 'Model';
    OpsFileExtension = '_Model';

    % AT lattice
    AD.ATModel = 'snslattice';
    %snslattice;

    % Golden TUNE is with the TUNE family
    AO = getao;
    AO.TUNE.Monitor.Golden = [
        0.4133
        0.3633
        NaN];
    setao(AO);

    % Golden chromaticity is in the AD (must be in Physics units!)
    AD.Chromaticity.Golden = [.5; .5];  % ???

    switch2sim;
    switch2hw;

else
    error('Operational mode unknown');
end



% Set the AD directory path
setad(AD);
MMLROOT = setmmldirectories(AD.Machine, AD.SubMachine, ModeName, OpsFileExtension);
AD = getad;


% Circumference
AD.Circumference = findspos(THERING,length(THERING)+1);


% Updates the AT indices in the MiddleLayer with the present AT lattice
updateatindex;


% Set the model energy
setenergymodel(AD.Energy);


% Cavity and radiation
setcavity off;  
setradiation off;
fprintf('   Radiation and cavities are off. Use setradiation / setcavity to modify.\n'); 


% Momentum compaction factor
MCF = getmcf('Model');
if isnan(MCF)
    AD.MCF = 0.034134124729649;
    fprintf('   Model alpha calculation failed, middlelayer alpha set to  %f\n', AD.MCF);
else
    AD.MCF = MCF;
    fprintf('   Middlelayer alpha set to %f (AT model).\n', AD.MCF);
end

AD.OpsData.LOCOFile = [getfamilydata('Directory','OpsData'),'GoldenLOCO', OpsFileExtension, '.mat'];
setad(AD);


%%%%%%%%%%%%%%%%%%%%%%
% Final mode changes %
%%%%%%%%%%%%%%%%%%%%%%
if ModeNumber == 1
    setlocodata('Nominal');
    %setlocodata('LOCO2Model', AD.OpsData.LOCOFile);
elseif ModeNumber == 101
    setlocodata('Nominal');
    setfamilydata(0,'BPMx','Offset');
    setfamilydata(0,'BPMy','Offset');
    setfamilydata(0,'BPMx','Golden');
    setfamilydata(0,'BPMy','Golden');
    setfamilydata(0,'TuneDelay');
else
    setlocodata('Nominal');
end


fprintf('   Middlelayer setup for operational mode: %s\n', AD.OperationalMode);


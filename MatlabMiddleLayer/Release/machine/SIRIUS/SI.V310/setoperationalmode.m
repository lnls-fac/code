function setoperationalmode(ModeNumber)
%SETOPERATIONALMODE - Switches between the various operational modes
%  setoperationalmode(ModeNumber)
%
%  ModeNumber = 1.  3 GeV, AC20 {Default}
%               2.  3 GeV, AC10
%
% History
%
% 2012-08-29 Ximenes



% Check if the AO exists
checkforao;

% MODES
ModeCell = { ...
    '3 GeV - AC20', ...
    '3 GeV - AC10', ...
    };

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Accelerator Dependent Modes %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if nargin < 1
    [ModeNumber, OKFlag] = listdlg('Name','SIRIUS','PromptString','Select the Operational Mode:', 'SelectionMode','single', 'ListString', ModeCell);
    if OKFlag ~= 1
        fprintf('   Operational mode not changed\n');
        return
    end
end

if (ModeNumber == 1)
    set_operationalmode_AC20;
elseif (ModeNumber == 2)
    set_operationalmode_AC10;
else
    error('Operational mode unknown');
end

% Set the AD directory path
AD = getad;
setmmldirectories(AD.Machine, AD.SubMachine, AD.ModeName, AD.OpsFileExtension);
% Updates the AT indices in the MiddleLayer with the present AT lattice
updateatindex;
% Set the model energy
setenergymodel(AD.Energy);
% Cavity and radiation
setcavity off;
setradiation off;
fprintf('   Radiation and cavities are off. Use setradiation / setcavity to modify.\n');




%%%%%%%%%%%%%%%%%%%%%%
% Final mode changes %
%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Add LOCO Parameters to AO and AT-Model %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  'Nominal'    - Sets nominal gains (1) / rolls (0) to the model.
%  'SetGains'   - Set gains/coupling from a LOCO file.
%  'SetModel'   - Set the model from a LOCO file.  But it only changes
%                 the part of the model that does not get corrected
%                 in 'Symmetrize' (also does a SetGains).
%  'LOCO2Model' - Set the model from a LOCO file (also does a SetGains).
%                 This uses the LOCO AT model!!! And sets all lattice
%                 machines fit in the LOCO run to the model.
%
%   Basically, use 'SetGains' or 'SetModel' if the LOCO run was applied to the accelerator
%              use 'LOCO2Model' if the LOCO run was made after the final setup.  Of couse,
%              setlocodata must be written properly for all this to work correctly.

try
    % I typically place to store the calibration LOCO file in the StorageRingOpsData directory
    %LOCOFile = [getfamilydata('Directory','OpsData'),'LOCO_User'];
    setlocodata('Nominal');
    %setlocodata('SetGains',   LOCOFile);
    %setlocodata('SetModel',   LOCOFile);
    %setlocodata('LOCO2Model', LOCOFile);
catch
    fprintf('   Problem with setting the LOCO calibration.\n');
end


fprintf('   Middlelayer setup for operational mode: %s\n', AD.OperationalMode);
atsummary;

function set_operationalmode_AC20

global THERING;

AD = getad;
AD.Machine             = 'SIRIUS_V310';  % Will already be defined if setpathmml was used
AD.SubMachine          = 'StorageRing';  % Will already be defined if setpathmml was used
AD.OperationalMode     = 'V310_AC20';
AD.Energy              = 3.0;
AD.InjectionEnergy     = 3.0;
AD.ModeName            = 'AC20';
AD.OpsFileExtension    = '';

sirius_si_lattice(AD.Energy, AD.ModeName);

AD.Circumference       = findspos(THERING,length(THERING)+1);
AD.HarmonicNumber      = 864;
AD.DeltaRFDisp         = 2000e-6;
AD.DeltaRFChro         = 1e-6 * linspace(-3000,3000,11);

AD.TuneDelay           = 0;
AD.ATModel             = 'sirius_si_lattice';
AD.Chromaticity.Golden = [1; 1];
AD.MCF                 = getmcf('Model');

AD.BeamCurrent         = 0.500; % [A]
AD.NrBunches           = AD.HarmonicNumber;
AD.Coupling            = 0.010;
AD.OpsData.PrsProfFile = 'sirius_v300_pressure_profile.txt';

setad(AD);
switch2sim;
switch2hw;


function set_operationalmode_AC10

global THERING;

AD = getad;
AD.Machine             = 'SIRIUS_V310';           % Will already be defined if setpathmml was used
AD.SubMachine          = 'StorageRing';  % Will already be defined if setpathmml was used
AD.OperationalMode     = 'V310_AC10';
AD.Energy              = 3.0;
AD.InjectionEnergy     = 3.0;
AD.ModeName            = 'AC10';
AD.OpsFileExtension    = '';

sirius_si_lattice(AD.Energy, AD.ModeName);

AD.Circumference       = findspos(THERING,length(THERING)+1);
AD.HarmonicNumber      = 864;
AD.DeltaRFDisp         = 2000e-6;
AD.DeltaRFChro         = 1e-6 * linspace(-3000,3000,11);

AD.TuneDelay           = 0;
AD.ATModel             = 'sirius_si_lattice';
AD.Chromaticity.Golden = [1; 1];
AD.MCF                 = getmcf('Model');

AD.BeamCurrent         = 0.500; % [A]
AD.NrBunches           = AD.HarmonicNumber;
AD.Coupling            = 0.010;
AD.OpsData.PrsProfFile = 'sirius_v300_pressure_profile.txt';

setad(AD);
switch2sim;
switch2hw;

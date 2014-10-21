function sirius_init(OperationalMode)
%LNLSINIT - MML initialization file for the VUV ring at sirius3
%  lnlsinit(OperationalMode)
%
%  See also setoperationalmode

% 2012-07-10 Modificado para sirius3_lattice_e025 - Afonso




if nargin < 1
    OperationalMode = 1;
end

setao([]);
setad([]);



% Base on the location of this file
[SIRIUS_ROOT, FileName, ExtentionName] = fileparts(mfilename('fullpath'));
AD.Directory.ExcDataDir = [SIRIUS_ROOT, filesep, 'excitation_curves'];
AD.Directory.LatticesDef = [SIRIUS_ROOT, filesep, 'lattices_def'];
setad(AD);

% Add additional directories with SIRIUS_V03 specific stuff.
MMLROOT = getmmlroot('IgnoreTheAD');
%addpath(fullfile(MMLROOT,'machine','SIRIUS_V03','StorageRing','scripts'), '-begin');

% Get the device lists (local function)
%[OnePerSector, TwoPerSector, ThreePerSector, FourPerSector, FivePerSector, SixPerSector, EightPerSector, TenPerSector, TwelvePerSector, FifteenPerSector, SixteenPerSector, EighteenPerSector, TwentyFourPerSector] = buildthedevicelists;


% BENDS

AO.b1.FamilyName  = 'b1';
AO.b1.MemberOf    = {'PlotFamily'; 'b1'; 'BEND'; 'Magnet';};
AO.b1.DeviceList  = getDeviceList(10,4);
AO.b1.ElementList = (1:size(AO.b1.DeviceList,1))';
AO.b1.Status      = ones(size(AO.b1.DeviceList,1),1);
AO.b1.Position    = [];

AO.b1.Monitor.MemberOf = {};
AO.b1.Monitor.Mode = 'Simulator';
AO.b1.Monitor.DataType = 'Scalar';
AO.b1.Monitor.ChannelNames = sirius_getname(AO.b1.FamilyName, 'Monitor', AO.b1.DeviceList);
AO.b1.Monitor.HW2PhysicsParams = 1;
AO.b1.Monitor.Physics2HWParams = 1;
AO.b1.Monitor.Units        = 'Hardware';
AO.b1.Monitor.HWUnits      = 'Ampere';
AO.b1.Monitor.PhysicsUnits = 'GeV';

AO.b1.Setpoint.MemberOf = {'MachineConfig';};
AO.b1.Setpoint.Mode = 'Simulator';
AO.b1.Setpoint.DataType = 'Scalar';
AO.b1.Setpoint.ChannelNames = sirius_getname(AO.b1.FamilyName, 'Setpoint', AO.b1.DeviceList);
AO.b1.Setpoint.HW2PhysicsParams = 1;
AO.b1.Setpoint.Physics2HWParams = 1;
AO.b1.Setpoint.Units        = 'Hardware';
AO.b1.Setpoint.HWUnits      = 'Ampere';
AO.b1.Setpoint.PhysicsUnits = 'GeV';
AO.b1.Setpoint.Range        = [0 300];
AO.b1.Setpoint.Tolerance    = .1;
AO.b1.Setpoint.DeltaRespMat = .01;


AO.b2.FamilyName  = 'b2';
AO.b2.MemberOf    = {'PlotFamily'; 'b2'; 'BEND'; 'Magnet';};
AO.b2.DeviceList  = getDeviceList(10,4);
AO.b2.ElementList = (1:size(AO.b2.DeviceList,1))';
AO.b2.Status      = ones(size(AO.b2.DeviceList,1),1);
AO.b2.Position    = [];

AO.b2.Monitor.MemberOf = {};
AO.b2.Monitor.Mode = 'Simulator';
AO.b2.Monitor.DataType = 'Scalar';
AO.b2.Monitor.ChannelNames = sirius_getname(AO.b2.FamilyName, 'Monitor', AO.b2.DeviceList);
AO.b2.Monitor.HW2PhysicsParams = 1;
AO.b2.Monitor.Physics2HWParams = 1;
AO.b2.Monitor.Units        = 'Hardware';
AO.b2.Monitor.HWUnits      = 'Ampere';
AO.b2.Monitor.PhysicsUnits = 'GeV';

AO.b2.Setpoint.MemberOf = {'MachineConfig';};
AO.b2.Setpoint.Mode = 'Simulator';
AO.b2.Setpoint.DataType = 'Scalar';
AO.b2.Setpoint.ChannelNames = sirius_getname(AO.b2.FamilyName, 'Setpoint', AO.b2.DeviceList);
AO.b2.Setpoint.HW2PhysicsParams = 1;
AO.b2.Setpoint.Physics2HWParams = 1;
AO.b2.Setpoint.Units        = 'Hardware';
AO.b2.Setpoint.HWUnits      = 'Ampere';
AO.b2.Setpoint.PhysicsUnits = 'GeV';
AO.b2.Setpoint.Range        = [0 300];
AO.b2.Setpoint.Tolerance    = .1;
AO.b2.Setpoint.DeltaRespMat = .01;


AO.b3.FamilyName  = 'b3';
AO.b3.MemberOf    = {'PlotFamily'; 'b3'; 'BEND'; 'Magnet';};
AO.b3.DeviceList  = getDeviceList(10,4);
AO.b3.ElementList = (1:size(AO.b3.DeviceList,1))';
AO.b3.Status      = ones(size(AO.b3.DeviceList,1),1);
AO.b3.Position    = [];

AO.b3.Monitor.MemberOf = {};
AO.b3.Monitor.Mode = 'Simulator';
AO.b3.Monitor.DataType = 'Scalar';
AO.b3.Monitor.ChannelNames = sirius_getname(AO.b3.FamilyName, 'Monitor', AO.b3.DeviceList);
AO.b3.Monitor.HW2PhysicsParams = 1;
AO.b3.Monitor.Physics2HWParams = 1;
AO.b3.Monitor.Units        = 'Hardware';
AO.b3.Monitor.HWUnits      = 'Ampere';
AO.b3.Monitor.PhysicsUnits = 'GeV';

AO.b3.Setpoint.MemberOf = {'MachineConfig';};
AO.b3.Setpoint.Mode = 'Simulator';
AO.b3.Setpoint.DataType = 'Scalar';
AO.b3.Setpoint.ChannelNames = sirius_getname(AO.b3.FamilyName, 'Setpoint', AO.b3.DeviceList);
AO.b3.Setpoint.HW2PhysicsParams = 1;
AO.b3.Setpoint.Physics2HWParams = 1;
AO.b3.Setpoint.Units        = 'Hardware';
AO.b3.Setpoint.HWUnits      = 'Ampere';
AO.b3.Setpoint.PhysicsUnits = 'GeV';
AO.b3.Setpoint.Range        = [0 300];
AO.b3.Setpoint.Tolerance    = .1;
AO.b3.Setpoint.DeltaRespMat = .01;


AO.bc.FamilyName  = 'bc';
AO.bc.MemberOf    = {'PlotFamily'; 'bc'; 'BEND'; 'Magnet';};
AO.bc.DeviceList  = getDeviceList(10,2);
AO.bc.ElementList = (1:size(AO.bc.DeviceList,1))';
AO.bc.Status      = ones(size(AO.bc.DeviceList,1),1);
AO.bc.Position    = [];

AO.bc.Monitor.MemberOf = {};
AO.bc.Monitor.Mode = 'Simulator';
AO.bc.Monitor.DataType = 'Scalar';
AO.bc.Monitor.ChannelNames = sirius_getname(AO.bc.FamilyName, 'Monitor', AO.bc.DeviceList);
AO.bc.Monitor.HW2PhysicsParams = 1;
AO.bc.Monitor.Physics2HWParams = 1;
AO.bc.Monitor.Units        = 'Hardware';
AO.bc.Monitor.HWUnits      = 'Ampere';
AO.bc.Monitor.PhysicsUnits = 'GeV';

AO.bc.Setpoint.MemberOf = {'MachineConfig';};
AO.bc.Setpoint.Mode = 'Simulator';
AO.bc.Setpoint.DataType = 'Scalar';
AO.bc.Setpoint.ChannelNames = sirius_getname(AO.bc.FamilyName, 'Setpoint', AO.bc.DeviceList);
AO.bc.Setpoint.HW2PhysicsParams = 1;
AO.bc.Setpoint.Physics2HWParams = 1;
AO.bc.Setpoint.Units        = 'Hardware';
AO.bc.Setpoint.HWUnits      = 'Ampere';
AO.bc.Setpoint.PhysicsUnits = 'GeV';
AO.bc.Setpoint.Range        = [0 300];
AO.bc.Setpoint.Tolerance    = .1;
AO.bc.Setpoint.DeltaRespMat = .01;


AO.qfa.FamilyName = 'qfa';
AO.qfa.MemberOf    = {'PlotFamily'; 'qfa'; 'QUAD'; 'Magnet';};
AO.qfa.DeviceList  = getDeviceList(10,2);
AO.qfa.ElementList = (1:size(AO.qfa.DeviceList,1))';
AO.qfa.Status      = ones(size(AO.qfa.DeviceList,1),1);
AO.qfa.Position    = [];
AO.qfa.Monitor.MemberOf = {};
AO.qfa.Monitor.Mode = 'Simulator';
AO.qfa.Monitor.DataType = 'Scalar';
AO.qfa.Monitor.Units        = 'Hardware';
AO.qfa.Monitor.HWUnits      = 'Ampere';
AO.qfa.Monitor.PhysicsUnits = 'meter^-2';
AO.qfa.Setpoint.MemberOf      = {'MachineConfig'};
AO.qfa.Setpoint.Mode          = 'Simulator';
AO.qfa.Setpoint.DataType      = 'Scalar';
AO.qfa.Setpoint.Units         = 'Hardware';
AO.qfa.Setpoint.HWUnits       = 'Ampere';
AO.qfa.Setpoint.PhysicsUnits  = 'meter^-2';
AO.qfa.Setpoint.Range         = [0 225];
AO.qfa.Setpoint.Tolerance     = 0.2;
AO.qfa.Setpoint.DeltaRespMat  = 0.5; 

AO.qdb2.FamilyName = 'qdb2';
AO.qdb2.MemberOf    = {'PlotFamily'; 'qdb2'; 'QUAD'; 'Magnet';};
AO.qdb2.DeviceList  = getDeviceList(10,2);
AO.qdb2.ElementList = (1:size(AO.qdb2.DeviceList,1))';
AO.qdb2.Status      = ones(size(AO.qdb2.DeviceList,1),1);
AO.qdb2.Position    = [];
AO.qdb2.Monitor.MemberOf = {};
AO.qdb2.Monitor.Mode = 'Simulator';
AO.qdb2.Monitor.DataType = 'Scalar';
AO.qdb2.Monitor.Units        = 'Hardware';
AO.qdb2.Monitor.HWUnits      = 'Ampere';
AO.qdb2.Monitor.PhysicsUnits = 'meter^-2';
AO.qdb2.Setpoint.MemberOf      = {'MachineConfig'};
AO.qdb2.Setpoint.Mode          = 'Simulator';
AO.qdb2.Setpoint.DataType      = 'Scalar';
AO.qdb2.Setpoint.Units         = 'Hardware';
AO.qdb2.Setpoint.HWUnits       = 'Ampere';
AO.qdb2.Setpoint.PhysicsUnits  = 'meter^-2';
AO.qdb2.Setpoint.Range         = [0 225];
AO.qdb2.Setpoint.Tolerance     = 0.2;
AO.qdb2.Setpoint.DeltaRespMat  = 0.5; 

AO.qfb.FamilyName = 'qfb';
AO.qfb.MemberOf    = {'PlotFamily'; 'qfb'; 'QUAD'; 'Magnet';};
AO.qfb.DeviceList  = getDeviceList(10,2);
AO.qfb.ElementList = (1:size(AO.qfb.DeviceList,1))';
AO.qfb.Status      = ones(size(AO.qfb.DeviceList,1),1);
AO.qfb.Position    = [];
AO.qfb.Monitor.MemberOf = {};
AO.qfb.Monitor.Mode = 'Simulator';
AO.qfb.Monitor.DataType = 'Scalar';
AO.qfb.Monitor.Units        = 'Hardware';
AO.qfb.Monitor.HWUnits      = 'Ampere';
AO.qfb.Monitor.PhysicsUnits = 'meter^-2';
AO.qfb.Setpoint.MemberOf      = {'MachineConfig'};
AO.qfb.Setpoint.Mode          = 'Simulator';
AO.qfb.Setpoint.DataType      = 'Scalar';
AO.qfb.Setpoint.Units         = 'Hardware';
AO.qfb.Setpoint.HWUnits       = 'Ampere';
AO.qfb.Setpoint.PhysicsUnits  = 'meter^-2';
AO.qfb.Setpoint.Range         = [0 225];
AO.qfb.Setpoint.Tolerance     = 0.2;
AO.qfb.Setpoint.DeltaRespMat  = 0.5; 

AO.qdb1.FamilyName = 'qdb1';
AO.qdb1.MemberOf    = {'PlotFamily'; 'qdb1'; 'QUAD'; 'Magnet';};
AO.qdb1.DeviceList  = getDeviceList(10,2);
AO.qdb1.ElementList = (1:size(AO.qdb1.DeviceList,1))';
AO.qdb1.Status      = ones(size(AO.qdb1.DeviceList,1),1);
AO.qdb1.Position    = [];
AO.qdb1.Monitor.MemberOf = {};
AO.qdb1.Monitor.Mode = 'Simulator';
AO.qdb1.Monitor.DataType = 'Scalar';
AO.qdb1.Monitor.Units        = 'Hardware';
AO.qdb1.Monitor.HWUnits      = 'Ampere';
AO.qdb1.Monitor.PhysicsUnits = 'meter^-2';
AO.qdb1.Setpoint.MemberOf      = {'MachineConfig'};
AO.qdb1.Setpoint.Mode          = 'Simulator';
AO.qdb1.Setpoint.DataType      = 'Scalar';
AO.qdb1.Setpoint.Units         = 'Hardware';
AO.qdb1.Setpoint.HWUnits       = 'Ampere';
AO.qdb1.Setpoint.PhysicsUnits  = 'meter^-2';
AO.qdb1.Setpoint.Range         = [0 225];
AO.qdb1.Setpoint.Tolerance     = 0.2;
AO.qdb1.Setpoint.DeltaRespMat  = 0.5; 

AO.qda1.FamilyName = 'qda1';
AO.qda1.MemberOf    = {'PlotFamily'; 'qda1'; 'QUAD'; 'Magnet';};
AO.qda1.DeviceList  = getDeviceList(10,2);
AO.qda1.ElementList = (1:size(AO.qda1.DeviceList,1))';
AO.qda1.Status      = ones(size(AO.qda1.DeviceList,1),1);
AO.qda1.Position    = [];
AO.qda1.Monitor.MemberOf = {};
AO.qda1.Monitor.Mode = 'Simulator';
AO.qda1.Monitor.DataType = 'Scalar';
AO.qda1.Monitor.Units        = 'Hardware';
AO.qda1.Monitor.HWUnits      = 'Ampere';
AO.qda1.Monitor.PhysicsUnits = 'meter^-2';
AO.qda1.Setpoint.MemberOf      = {'MachineConfig'};
AO.qda1.Setpoint.Mode          = 'Simulator';
AO.qda1.Setpoint.DataType      = 'Scalar';
AO.qda1.Setpoint.Units         = 'Hardware';
AO.qda1.Setpoint.HWUnits       = 'Ampere';
AO.qda1.Setpoint.PhysicsUnits  = 'meter^-2';
AO.qda1.Setpoint.Range         = [0 225];
AO.qda1.Setpoint.Tolerance     = 0.2;
AO.qda1.Setpoint.DeltaRespMat  = 0.5;


AO.qf1.FamilyName = 'qf1';
AO.qf1.MemberOf    = {'PlotFamily'; 'qf1'; 'QUAD'; 'Magnet';};
AO.qf1.DeviceList  = getDeviceList(10,4);
AO.qf1.ElementList = (1:size(AO.qf1.DeviceList,1))';
AO.qf1.Status      = ones(size(AO.qf1.DeviceList,1),1);
AO.qf1.Position    = [];
AO.qf1.Monitor.MemberOf = {};
AO.qf1.Monitor.Mode = 'Simulator';
AO.qf1.Monitor.DataType = 'Scalar';
AO.qf1.Monitor.Units        = 'Hardware';
AO.qf1.Monitor.HWUnits      = 'Ampere';
AO.qf1.Monitor.PhysicsUnits = 'meter^-2';
AO.qf1.Setpoint.MemberOf      = {'MachineConfig'};
AO.qf1.Setpoint.Mode          = 'Simulator';
AO.qf1.Setpoint.DataType      = 'Scalar';
AO.qf1.Setpoint.Units         = 'Hardware';
AO.qf1.Setpoint.HWUnits       = 'Ampere';
AO.qf1.Setpoint.PhysicsUnits  = 'meter^-2';
AO.qf1.Setpoint.Range         = [0 225];
AO.qf1.Setpoint.Tolerance     = 0.2;
AO.qf1.Setpoint.DeltaRespMat  = 0.5;

AO.qf2.FamilyName = 'qf2';
AO.qf2.MemberOf    = {'PlotFamily'; 'qf2'; 'QUAD'; 'Magnet';};
AO.qf2.DeviceList  = getDeviceList(10,4);
AO.qf2.ElementList = (1:size(AO.qf2.DeviceList,1))';
AO.qf2.Status      = ones(size(AO.qf2.DeviceList,1),1);
AO.qf2.Position    = [];
AO.qf2.Monitor.MemberOf = {};
AO.qf2.Monitor.Mode = 'Simulator';
AO.qf2.Monitor.DataType = 'Scalar';
AO.qf2.Monitor.Units        = 'Hardware';
AO.qf2.Monitor.HWUnits      = 'Ampere';
AO.qf2.Monitor.PhysicsUnits = 'meter^-2';
AO.qf2.Setpoint.MemberOf      = {'MachineConfig'};
AO.qf2.Setpoint.Mode          = 'Simulator';
AO.qf2.Setpoint.DataType      = 'Scalar';
AO.qf2.Setpoint.Units         = 'Hardware';
AO.qf2.Setpoint.HWUnits       = 'Ampere';
AO.qf2.Setpoint.PhysicsUnits  = 'meter^-2';
AO.qf2.Setpoint.Range         = [0 225];
AO.qf2.Setpoint.Tolerance     = 0.2;
AO.qf2.Setpoint.DeltaRespMat  = 0.5;

AO.qf3.FamilyName = 'qf3';
AO.qf3.MemberOf    = {'PlotFamily'; 'qf3'; 'QUAD'; 'Magnet';};
AO.qf3.DeviceList  = getDeviceList(10,4);
AO.qf3.ElementList = (1:size(AO.qf3.DeviceList,1))';
AO.qf3.Status      = ones(size(AO.qf3.DeviceList,1),1);
AO.qf3.Position    = [];
AO.qf3.Monitor.MemberOf = {};
AO.qf3.Monitor.Mode = 'Simulator';
AO.qf3.Monitor.DataType = 'Scalar';
AO.qf3.Monitor.Units        = 'Hardware';
AO.qf3.Monitor.HWUnits      = 'Ampere';
AO.qf3.Monitor.PhysicsUnits = 'meter^-2';
AO.qf3.Setpoint.MemberOf      = {'MachineConfig'};
AO.qf3.Setpoint.Mode          = 'Simulator';
AO.qf3.Setpoint.DataType      = 'Scalar';
AO.qf3.Setpoint.Units         = 'Hardware';
AO.qf3.Setpoint.HWUnits       = 'Ampere';
AO.qf3.Setpoint.PhysicsUnits  = 'meter^-2';
AO.qf3.Setpoint.Range         = [0 225];
AO.qf3.Setpoint.Tolerance     = 0.2;
AO.qf3.Setpoint.DeltaRespMat  = 0.5;

AO.qf4.FamilyName = 'qf4';
AO.qf4.MemberOf    = {'PlotFamily'; 'qf4'; 'QUAD'; 'Magnet';};
AO.qf4.DeviceList  = getDeviceList(10,4);
AO.qf4.ElementList = (1:size(AO.qf4.DeviceList,1))';
AO.qf4.Status      = ones(size(AO.qf4.DeviceList,1),1);
AO.qf4.Position    = [];
AO.qf4.Monitor.MemberOf = {};
AO.qf4.Monitor.Mode = 'Simulator';
AO.qf4.Monitor.DataType = 'Scalar';
AO.qf4.Monitor.Units        = 'Hardware';
AO.qf4.Monitor.HWUnits      = 'Ampere';
AO.qf4.Monitor.PhysicsUnits = 'meter^-2';
AO.qf4.Setpoint.MemberOf      = {'MachineConfig'};
AO.qf4.Setpoint.Mode          = 'Simulator';
AO.qf4.Setpoint.DataType      = 'Scalar';
AO.qf4.Setpoint.Units         = 'Hardware';
AO.qf4.Setpoint.HWUnits       = 'Ampere';
AO.qf4.Setpoint.PhysicsUnits  = 'meter^-2';
AO.qf4.Setpoint.Range         = [0 225];
AO.qf4.Setpoint.Tolerance     = 0.2;
AO.qf4.Setpoint.DeltaRespMat  = 0.5;
%%

AO.sda.FamilyName = 'sda';
AO.sda.MemberOf    = {'PlotFamily'; 'sda'; 'SEXT'; 'Magnet'; 'Coupling Corrector'; 'Chromaticity Corrector'};
AO.sda.DeviceList  = getDeviceList(10,2);
AO.sda.ElementList = (1:size(AO.sda.DeviceList,1))';
AO.sda.Status      = ones(size(AO.sda.DeviceList,1),1);
AO.sda.Position    = [];
AO.sda.Monitor.MemberOf = {};
AO.sda.Monitor.Mode = 'Simulator';
AO.sda.Monitor.DataType = 'Scalar';
AO.sda.Monitor.Units        = 'Hardware';
AO.sda.Monitor.HWUnits      = 'Ampere';
AO.sda.Monitor.PhysicsUnits = 'meter^-3';
AO.sda.Setpoint.MemberOf      = {'MachineConfig'};
AO.sda.Setpoint.Mode          = 'Simulator';
AO.sda.Setpoint.DataType      = 'Scalar';
AO.sda.Setpoint.Units         = 'Hardware';
AO.sda.Setpoint.HWUnits       = 'Ampere';
AO.sda.Setpoint.PhysicsUnits  = 'meter^-3';
AO.sda.Setpoint.Range         = [0 225];
AO.sda.Setpoint.Tolerance     = 0.2;
AO.sda.Setpoint.DeltaRespMat  = 0.5; 

AO.sfa.FamilyName = 'sfa';
AO.sfa.MemberOf    = {'PlotFamily'; 'sfa'; 'SEXT'; 'Magnet'; 'Coupling Corrector'; 'Chromaticity Corrector'};
AO.sfa.DeviceList  = getDeviceList(10,2);
AO.sfa.ElementList = (1:size(AO.sfa.DeviceList,1))';
AO.sfa.Status      = ones(size(AO.sfa.DeviceList,1),1);
AO.sfa.Position    = [];
AO.sfa.Monitor.MemberOf = {};
AO.sfa.Monitor.Mode = 'Simulator';
AO.sfa.Monitor.DataType = 'Scalar';
AO.sfa.Monitor.Units        = 'Hardware';
AO.sfa.Monitor.HWUnits      = 'Ampere';
AO.sfa.Monitor.PhysicsUnits = 'meter^-3';
AO.sfa.Setpoint.MemberOf      = {'MachineConfig'};
AO.sfa.Setpoint.Mode          = 'Simulator';
AO.sfa.Setpoint.DataType      = 'Scalar';
AO.sfa.Setpoint.Units         = 'Hardware';
AO.sfa.Setpoint.HWUnits       = 'Ampere';
AO.sfa.Setpoint.PhysicsUnits  = 'meter^-3';
AO.sfa.Setpoint.Range         = [0 225];
AO.sfa.Setpoint.Tolerance     = 0.2;
AO.sfa.Setpoint.DeltaRespMat  = 0.5; 

AO.sd1a.FamilyName = 'sd1a';
AO.sd1a.MemberOf    = {'PlotFamily'; 'sd1a'; 'SEXT'; 'Magnet'; 'Coupling Corrector'; 'Chromaticity Corrector'};
AO.sd1a.DeviceList  = getDeviceList(10,2);
AO.sd1a.ElementList = (1:size(AO.sd1a.DeviceList,1))';
AO.sd1a.Status      = ones(size(AO.sd1a.DeviceList,1),1);
AO.sd1a.Position    = [];
AO.sd1a.Monitor.MemberOf = {};
AO.sd1a.Monitor.Mode = 'Simulator';
AO.sd1a.Monitor.DataType = 'Scalar';
AO.sd1a.Monitor.Units        = 'Hardware';
AO.sd1a.Monitor.HWUnits      = 'Ampere';
AO.sd1a.Monitor.PhysicsUnits = 'meter^-3';
AO.sd1a.Setpoint.MemberOf      = {'MachineConfig'};
AO.sd1a.Setpoint.Mode          = 'Simulator';
AO.sd1a.Setpoint.DataType      = 'Scalar';
AO.sd1a.Setpoint.Units         = 'Hardware';
AO.sd1a.Setpoint.HWUnits       = 'Ampere';
AO.sd1a.Setpoint.PhysicsUnits  = 'meter^-3';
AO.sd1a.Setpoint.Range         = [0 225];
AO.sd1a.Setpoint.Tolerance     = 0.2;
AO.sd1a.Setpoint.DeltaRespMat  = 0.5;

AO.sf1a.FamilyName = 'sf1a';
AO.sf1a.MemberOf    = {'PlotFamily'; 'sf1a'; 'SEXT'; 'Magnet'; 'Coupling Corrector'; 'Chromaticity Corrector'};
AO.sf1a.DeviceList  = getDeviceList(10,2);
AO.sf1a.ElementList = (1:size(AO.sf1a.DeviceList,1))';
AO.sf1a.Status      = ones(size(AO.sf1a.DeviceList,1),1);
AO.sf1a.Position    = [];
AO.sf1a.Monitor.MemberOf = {};
AO.sf1a.Monitor.Mode = 'Simulator';
AO.sf1a.Monitor.DataType = 'Scalar';
AO.sf1a.Monitor.Units        = 'Hardware';
AO.sf1a.Monitor.HWUnits      = 'Ampere';
AO.sf1a.Monitor.PhysicsUnits = 'meter^-3';
AO.sf1a.Setpoint.MemberOf      = {'MachineConfig'};
AO.sf1a.Setpoint.Mode          = 'Simulator';
AO.sf1a.Setpoint.DataType      = 'Scalar';
AO.sf1a.Setpoint.Units         = 'Hardware';
AO.sf1a.Setpoint.HWUnits       = 'Ampere';
AO.sf1a.Setpoint.PhysicsUnits  = 'meter^-3';
AO.sf1a.Setpoint.Range         = [0 225];
AO.sf1a.Setpoint.Tolerance     = 0.2;
AO.sf1a.Setpoint.DeltaRespMat  = 0.5; 

AO.sd2a.FamilyName = 'sd2a';
AO.sd2a.MemberOf    = {'PlotFamily'; 'sd2a'; 'SEXT'; 'Magnet'; 'Coupling Corrector'; 'Chromaticity Corrector'};
AO.sd2a.DeviceList  = getDeviceList(10,2);
AO.sd2a.ElementList = (1:size(AO.sd2a.DeviceList,1))';
AO.sd2a.Status      = ones(size(AO.sd2a.DeviceList,1),1);
AO.sd2a.Position    = [];
AO.sd2a.Monitor.MemberOf = {};
AO.sd2a.Monitor.Mode = 'Simulator';
AO.sd2a.Monitor.DataType = 'Scalar';
AO.sd2a.Monitor.Units        = 'Hardware';
AO.sd2a.Monitor.HWUnits      = 'Ampere';
AO.sd2a.Monitor.PhysicsUnits = 'meter^-3';
AO.sd2a.Setpoint.MemberOf      = {'MachineConfig'};
AO.sd2a.Setpoint.Mode          = 'Simulator';
AO.sd2a.Setpoint.DataType      = 'Scalar';
AO.sd2a.Setpoint.Units         = 'Hardware';
AO.sd2a.Setpoint.HWUnits       = 'Ampere';
AO.sd2a.Setpoint.PhysicsUnits  = 'meter^-3';
AO.sd2a.Setpoint.Range         = [0 225];
AO.sd2a.Setpoint.Tolerance     = 0.2;
AO.sd2a.Setpoint.DeltaRespMat  = 0.5; 

AO.sd3a.FamilyName = 'sd3a';
AO.sd3a.MemberOf    = {'PlotFamily'; 'sd3a'; 'SEXT'; 'Magnet'; 'Coupling Corrector'; 'Chromaticity Corrector'};
AO.sd3a.DeviceList  = getDeviceList(10,2);
AO.sd3a.ElementList = (1:size(AO.sd3a.DeviceList,1))';
AO.sd3a.Status      = ones(size(AO.sd3a.DeviceList,1),1);
AO.sd3a.Position    = [];
AO.sd3a.Monitor.MemberOf = {};
AO.sd3a.Monitor.Mode = 'Simulator';
AO.sd3a.Monitor.DataType = 'Scalar';
AO.sd3a.Monitor.Units        = 'Hardware';
AO.sd3a.Monitor.HWUnits      = 'Ampere';
AO.sd3a.Monitor.PhysicsUnits = 'meter^-3';
AO.sd3a.Setpoint.MemberOf      = {'MachineConfig'};
AO.sd3a.Setpoint.Mode          = 'Simulator';
AO.sd3a.Setpoint.DataType      = 'Scalar';
AO.sd3a.Setpoint.Units         = 'Hardware';
AO.sd3a.Setpoint.HWUnits       = 'Ampere';
AO.sd3a.Setpoint.PhysicsUnits  = 'meter^-3';
AO.sd3a.Setpoint.Range         = [0 225];
AO.sd3a.Setpoint.Tolerance     = 0.2;
AO.sd3a.Setpoint.DeltaRespMat  = 0.5; 

AO.sf2a.FamilyName = 'sf2a';
AO.sf2a.MemberOf    = {'PlotFamily'; 'sf2a'; 'SEXT'; 'Magnet'; 'Coupling Corrector'; 'Chromaticity Corrector'};
AO.sf2a.DeviceList  = getDeviceList(10,2);
AO.sf2a.ElementList = (1:size(AO.sf2a.DeviceList,1))';
AO.sf2a.Status      = ones(size(AO.sf2a.DeviceList,1),1);
AO.sf2a.Position    = [];
AO.sf2a.Monitor.MemberOf = {};
AO.sf2a.Monitor.Mode = 'Simulator';
AO.sf2a.Monitor.DataType = 'Scalar';
AO.sf2a.Monitor.Units        = 'Hardware';
AO.sf2a.Monitor.HWUnits      = 'Ampere';
AO.sf2a.Monitor.PhysicsUnits = 'meter^-3';
AO.sf2a.Setpoint.MemberOf      = {'MachineConfig'};
AO.sf2a.Setpoint.Mode          = 'Simulator';
AO.sf2a.Setpoint.DataType      = 'Scalar';
AO.sf2a.Setpoint.Units         = 'Hardware';
AO.sf2a.Setpoint.HWUnits       = 'Ampere';
AO.sf2a.Setpoint.PhysicsUnits  = 'meter^-3';
AO.sf2a.Setpoint.Range         = [0 225];
AO.sf2a.Setpoint.Tolerance     = 0.2;
AO.sf2a.Setpoint.DeltaRespMat  = 0.5; 

AO.sd1b.FamilyName = 'sd1b';
AO.sd1b.MemberOf    = {'PlotFamily'; 'sd1b'; 'SEXT'; 'Magnet'; 'Coupling Corrector'; 'Chromaticity Corrector'};
AO.sd1b.DeviceList  = getDeviceList(10,2);
AO.sd1b.ElementList = (1:size(AO.sd1b.DeviceList,1))';
AO.sd1b.Status      = ones(size(AO.sd1b.DeviceList,1),1);
AO.sd1b.Position    = [];
AO.sd1b.Monitor.MemberOf = {};
AO.sd1b.Monitor.Mode = 'Simulator';
AO.sd1b.Monitor.DataType = 'Scalar';
AO.sd1b.Monitor.Units        = 'Hardware';
AO.sd1b.Monitor.HWUnits      = 'Ampere';
AO.sd1b.Monitor.PhysicsUnits = 'meter^-3';
AO.sd1b.Setpoint.MemberOf      = {'MachineConfig'};
AO.sd1b.Setpoint.Mode          = 'Simulator';
AO.sd1b.Setpoint.DataType      = 'Scalar';
AO.sd1b.Setpoint.Units         = 'Hardware';
AO.sd1b.Setpoint.HWUnits       = 'Ampere';
AO.sd1b.Setpoint.PhysicsUnits  = 'meter^-3';
AO.sd1b.Setpoint.Range         = [0 225];
AO.sd1b.Setpoint.Tolerance     = 0.2;
AO.sd1b.Setpoint.DeltaRespMat  = 0.5;

AO.sf1b.FamilyName = 'sf1b';
AO.sf1b.MemberOf    = {'PlotFamily'; 'sf1b'; 'SEXT'; 'Magnet'; 'Coupling Corrector'; 'Chromaticity Corrector'};
AO.sf1b.DeviceList  = getDeviceList(10,2);
AO.sf1b.ElementList = (1:size(AO.sf1b.DeviceList,1))';
AO.sf1b.Status      = ones(size(AO.sf1b.DeviceList,1),1);
AO.sf1b.Position    = [];
AO.sf1b.Monitor.MemberOf = {};
AO.sf1b.Monitor.Mode = 'Simulator';
AO.sf1b.Monitor.DataType = 'Scalar';
AO.sf1b.Monitor.Units        = 'Hardware';
AO.sf1b.Monitor.HWUnits      = 'Ampere';
AO.sf1b.Monitor.PhysicsUnits = 'meter^-3';
AO.sf1b.Setpoint.MemberOf      = {'MachineConfig'};
AO.sf1b.Setpoint.Mode          = 'Simulator';
AO.sf1b.Setpoint.DataType      = 'Scalar';
AO.sf1b.Setpoint.Units         = 'Hardware';
AO.sf1b.Setpoint.HWUnits       = 'Ampere';
AO.sf1b.Setpoint.PhysicsUnits  = 'meter^-3';
AO.sf1b.Setpoint.Range         = [0 225];
AO.sf1b.Setpoint.Tolerance     = 0.2;
AO.sf1b.Setpoint.DeltaRespMat  = 0.5; 

AO.sd2b.FamilyName = 'sd2b';
AO.sd2b.MemberOf    = {'PlotFamily'; 'sd2b'; 'SEXT'; 'Magnet'; 'Coupling Corrector'; 'Chromaticity Corrector'};
AO.sd2b.DeviceList  = getDeviceList(10,2);
AO.sd2b.ElementList = (1:size(AO.sd2b.DeviceList,1))';
AO.sd2b.Status      = ones(size(AO.sd2b.DeviceList,1),1);
AO.sd2b.Position    = [];
AO.sd2b.Monitor.MemberOf = {};
AO.sd2b.Monitor.Mode = 'Simulator';
AO.sd2b.Monitor.DataType = 'Scalar';
AO.sd2b.Monitor.Units        = 'Hardware';
AO.sd2b.Monitor.HWUnits      = 'Ampere';
AO.sd2b.Monitor.PhysicsUnits = 'meter^-3';
AO.sd2b.Setpoint.MemberOf      = {'MachineConfig'};
AO.sd2b.Setpoint.Mode          = 'Simulator';
AO.sd2b.Setpoint.DataType      = 'Scalar';
AO.sd2b.Setpoint.Units         = 'Hardware';
AO.sd2b.Setpoint.HWUnits       = 'Ampere';
AO.sd2b.Setpoint.PhysicsUnits  = 'meter^-3';
AO.sd2b.Setpoint.Range         = [0 225];
AO.sd2b.Setpoint.Tolerance     = 0.2;
AO.sd2b.Setpoint.DeltaRespMat  = 0.5; 

AO.sd3b.FamilyName = 'sd3b';
AO.sd3b.MemberOf    = {'PlotFamily'; 'sd3b'; 'SEXT'; 'Magnet'; 'Coupling Corrector'; 'Chromaticity Corrector'};
AO.sd3b.DeviceList  = getDeviceList(10,2);
AO.sd3b.ElementList = (1:size(AO.sd3b.DeviceList,1))';
AO.sd3b.Status      = ones(size(AO.sd3b.DeviceList,1),1);
AO.sd3b.Position    = [];
AO.sd3b.Monitor.MemberOf = {};
AO.sd3b.Monitor.Mode = 'Simulator';
AO.sd3b.Monitor.DataType = 'Scalar';
AO.sd3b.Monitor.Units        = 'Hardware';
AO.sd3b.Monitor.HWUnits      = 'Ampere';
AO.sd3b.Monitor.PhysicsUnits = 'meter^-3';
AO.sd3b.Setpoint.MemberOf      = {'MachineConfig'};
AO.sd3b.Setpoint.Mode          = 'Simulator';
AO.sd3b.Setpoint.DataType      = 'Scalar';
AO.sd3b.Setpoint.Units         = 'Hardware';
AO.sd3b.Setpoint.HWUnits       = 'Ampere';
AO.sd3b.Setpoint.PhysicsUnits  = 'meter^-3';
AO.sd3b.Setpoint.Range         = [0 225];
AO.sd3b.Setpoint.Tolerance     = 0.2;
AO.sd3b.Setpoint.DeltaRespMat  = 0.5; 

AO.sf2b.FamilyName = 'sf2b';
AO.sf2b.MemberOf    = {'PlotFamily'; 'sf2b'; 'SEXT'; 'Magnet'; 'Coupling Corrector'; 'Chromaticity Corrector'};
AO.sf2b.DeviceList  = getDeviceList(10,2);
AO.sf2b.ElementList = (1:size(AO.sf2b.DeviceList,1))';
AO.sf2b.Status      = ones(size(AO.sf2b.DeviceList,1),1);
AO.sf2b.Position    = [];
AO.sf2b.Monitor.MemberOf = {};
AO.sf2b.Monitor.Mode = 'Simulator';
AO.sf2b.Monitor.DataType = 'Scalar';
AO.sf2b.Monitor.Units        = 'Hardware';
AO.sf2b.Monitor.HWUnits      = 'Ampere';
AO.sf2b.Monitor.PhysicsUnits = 'meter^-3';
AO.sf2b.Setpoint.MemberOf      = {'MachineConfig'};
AO.sf2b.Setpoint.Mode          = 'Simulator';
AO.sf2b.Setpoint.DataType      = 'Scalar';
AO.sf2b.Setpoint.Units         = 'Hardware';
AO.sf2b.Setpoint.HWUnits       = 'Ampere';
AO.sf2b.Setpoint.PhysicsUnits  = 'meter^-3';
AO.sf2b.Setpoint.Range         = [0 225];
AO.sf2b.Setpoint.Tolerance     = 0.2;
AO.sf2b.Setpoint.DeltaRespMat  = 0.5; 

AO.sfb.FamilyName = 'sfb';
AO.sfb.MemberOf    = {'PlotFamily'; 'sfb'; 'SEXT'; 'Magnet'; 'Coupling Corrector'; 'Chromaticity Corrector'};
AO.sfb.DeviceList  = getDeviceList(10,2);
AO.sfb.ElementList = (1:size(AO.sfb.DeviceList,1))';
AO.sfb.Status      = ones(size(AO.sfb.DeviceList,1),1);
AO.sfb.Position    = [];
AO.sfb.Monitor.MemberOf = {};
AO.sfb.Monitor.Mode = 'Simulator';
AO.sfb.Monitor.DataType = 'Scalar';
AO.sfb.Monitor.Units        = 'Hardware';
AO.sfb.Monitor.HWUnits      = 'Ampere';
AO.sfb.Monitor.PhysicsUnits = 'meter^-3';
AO.sfb.Setpoint.MemberOf      = {'MachineConfig'};
AO.sfb.Setpoint.Mode          = 'Simulator';
AO.sfb.Setpoint.DataType      = 'Scalar';
AO.sfb.Setpoint.Units         = 'Hardware';
AO.sfb.Setpoint.HWUnits       = 'Ampere';
AO.sfb.Setpoint.PhysicsUnits  = 'meter^-3';
AO.sfb.Setpoint.Range         = [0 225];
AO.sfb.Setpoint.Tolerance     = 0.2;
AO.sfb.Setpoint.DeltaRespMat  = 0.5; 

AO.sdb.FamilyName = 'sdb';
AO.sdb.MemberOf    = {'PlotFamily'; 'sdb'; 'SEXT'; 'Magnet'; 'Coupling Corrector'; 'Chromaticity Corrector'};
AO.sdb.DeviceList  = getDeviceList(10,2);
AO.sdb.ElementList = (1:size(AO.sdb.DeviceList,1))';
AO.sdb.Status      = ones(size(AO.sdb.DeviceList,1),1);
AO.sdb.Position    = [];
AO.sdb.Monitor.MemberOf = {};
AO.sdb.Monitor.Mode = 'Simulator';
AO.sdb.Monitor.DataType = 'Scalar';
AO.sdb.Monitor.Units        = 'Hardware';
AO.sdb.Monitor.HWUnits      = 'Ampere';
AO.sdb.Monitor.PhysicsUnits = 'meter^-3';
AO.sdb.Setpoint.MemberOf      = {'MachineConfig'};
AO.sdb.Setpoint.Mode          = 'Simulator';
AO.sdb.Setpoint.DataType      = 'Scalar';
AO.sdb.Setpoint.Units         = 'Hardware';
AO.sdb.Setpoint.HWUnits       = 'Ampere';
AO.sdb.Setpoint.PhysicsUnits  = 'meter^-3';
AO.sdb.Setpoint.Range         = [0 225];
AO.sdb.Setpoint.Tolerance     = 0.2;
AO.sdb.Setpoint.DeltaRespMat  = 0.5; 


%%
%%%%%%%%%%%%%%%%%%%%%
% Corrector Magnets %
%%%%%%%%%%%%%%%%%%%%%

% hcm
AO.hcm.FamilyName  = 'hcm';
AO.hcm.MemberOf    = {'PlotFamily'; 'COR'; 'hcm'; 'Magnet'};
AO.hcm.DeviceList  = getDeviceList(10,16);
AO.hcm.ElementList = (1:size(AO.hcm.DeviceList,1))';
AO.hcm.Status      = ones(size(AO.hcm.DeviceList,1),1);
%AO.hcm.Status      = repmat([0 1 0 1 1 0 1 0]',20,1);
AO.hcm.Position    = [];

AO.hcm.Monitor.MemberOf = {'Horizontal'; 'COR'; 'hcm'; 'Magnet';};
AO.hcm.Monitor.Mode = 'Simulator';
AO.hcm.Monitor.DataType = 'Scalar';
AO.hcm.Monitor.Units        = 'Physics';
AO.hcm.Monitor.HWUnits      = 'Ampere';
AO.hcm.Monitor.PhysicsUnits = 'Radian';

AO.hcm.Setpoint.MemberOf = {'MachineConfig'; 'Horizontal'; 'COR'; 'hcm'; 'Magnet'; 'Setpoint'; 'measbpmresp';};
AO.hcm.Setpoint.Mode = 'Simulator';
AO.hcm.Setpoint.DataType = 'Scalar';
AO.hcm.Setpoint.Units        = 'Physics';
AO.hcm.Setpoint.HWUnits      = 'Ampere';
AO.hcm.Setpoint.PhysicsUnits = 'Radian';
AO.hcm.Setpoint.Range        = [-10 10];
AO.hcm.Setpoint.Tolerance    = 0.00001;
AO.hcm.Setpoint.DeltaRespMat = 0.0005; 

% vcm
AO.vcm.FamilyName  = 'vcm';
AO.vcm.MemberOf    = {'PlotFamily'; 'COR'; 'vcm'; 'Magnet'};
AO.vcm.DeviceList  = getDeviceList(10,12);
AO.vcm.ElementList = (1:size(AO.vcm.DeviceList,1))';
AO.vcm.Status      = ones(size(AO.vcm.DeviceList,1),1);
%AO.vcm.Status      = repmat([1 0 1 0 0 1 0 1]',20,1);
AO.vcm.Position    = [];
AO.vcm.Monitor.MemberOf = {'Vertical'; 'COR'; 'vcm'; 'Magnet';};
AO.vcm.Monitor.Mode = 'Simulator';
AO.vcm.Monitor.DataType = 'Scalar';
AO.vcm.Monitor.Units        = 'Physics';
AO.vcm.Monitor.HWUnits      = 'Ampere';
AO.vcm.Monitor.PhysicsUnits = 'Radian';

AO.vcm.Setpoint.MemberOf = {'MachineConfig'; 'Horizontal'; 'COR'; 'vcm'; 'Magnet'; 'Setpoint'; 'measbpmresp';};
AO.vcm.Setpoint.Mode = 'Simulator';
AO.vcm.Setpoint.DataType = 'Scalar';
AO.vcm.Setpoint.Units        = 'Physics';
AO.vcm.Setpoint.HWUnits      = 'Ampere';
AO.vcm.Setpoint.PhysicsUnits = 'Radian';
AO.vcm.Setpoint.Range        = [-10 10];
AO.vcm.Setpoint.Tolerance    = 0.00001;
AO.vcm.Setpoint.DeltaRespMat = 0.0005; 


% skewcm

AO.skewcm.FamilyName  = 'skewcm';
AO.skewcm.MemberOf    = {'PlotFamily'; 'COR'; 'skewcm'; 'Magnet'};
AO.skewcm.DeviceList  = getDeviceList(10,28);
AO.skewcm.ElementList = (1:size(AO.skewcm.DeviceList,1))';
AO.skewcm.Status      = ones(size(AO.skewcm.DeviceList,1),1);

AO.skewcm.Position    = [];

AO.skewcm.Monitor.MemberOf = {'COR'; 'skewcm'; 'Magnet';};
AO.skewcm.Monitor.Mode = 'Simulator';
AO.skewcm.Monitor.DataType = 'Scalar';
AO.skewcm.Monitor.Units        = 'Physics';
AO.skewcm.Monitor.HWUnits      = 'Ampere';
AO.skewcm.Monitor.PhysicsUnits = 'Radian';

AO.skewcm.Setpoint.MemberOf = {'MachineConfig'; 'COR'; 'skewcm'; 'Magnet'; 'Setpoint';};
AO.skewcm.Setpoint.Mode = 'Simulator';
AO.skewcm.Setpoint.DataType = 'Scalar';
AO.skewcm.Setpoint.Units        = 'Physics';
AO.skewcm.Setpoint.HWUnits      = 'Ampere';
AO.skewcm.Setpoint.PhysicsUnits = 'm^-2';
AO.skewcm.Setpoint.Range        = [-10 10];
AO.skewcm.Setpoint.Tolerance    = 0.00001;


% bpmx
AO.bpmx.FamilyName  = 'bpmx';
AO.bpmx.MemberOf    = {'PlotFamily'; 'bpm'; 'bpmx'; 'Diagnostics'};
AO.bpmx.DeviceList  = getDeviceList(10,18);
AO.bpmx.ElementList = (1:size(AO.bpmx.DeviceList,1))';
AO.bpmx.Status      = ones(size(AO.bpmx.DeviceList,1),1);
AO.bpmx.Position    = [];
AO.bpmx.Golden      = zeros(length(AO.bpmx.ElementList),1);
AO.bpmx.Offset      = zeros(length(AO.bpmx.ElementList),1);

AO.bpmx.Monitor.MemberOf = {'bpmx'; 'Monitor';};
AO.bpmx.Monitor.Mode = 'Simulator';
AO.bpmx.Monitor.DataType = 'Scalar';
AO.bpmx.Monitor.HW2PhysicsParams = 1e-3;  % HW [mm], Simulator [Meters]
AO.bpmx.Monitor.Physics2HWParams = 1000;
AO.bpmx.Monitor.Units        = 'Hardware';
AO.bpmx.Monitor.HWUnits      = 'mm';
AO.bpmx.Monitor.PhysicsUnits = 'meter';



% bpmy
AO.bpmy.FamilyName  = 'bpmy';
AO.bpmy.MemberOf    = {'PlotFamily'; 'bpm'; 'bpmy'; 'Diagnostics'};
AO.bpmy.DeviceList  = getDeviceList(10,18);
AO.bpmy.ElementList = (1:size(AO.bpmy.DeviceList,1))';
AO.bpmy.Status      = ones(size(AO.bpmy.DeviceList,1),1);
AO.bpmy.Position    = [];
AO.bpmy.Golden      = zeros(length(AO.bpmy.ElementList),1);
AO.bpmy.Offset      = zeros(length(AO.bpmy.ElementList),1);


AO.bpmy.Monitor.MemberOf = {'bpmy'; 'Monitor';};
AO.bpmy.Monitor.Mode = 'Simulator';
AO.bpmy.Monitor.DataType = 'Scalar';
AO.bpmy.Monitor.HW2PhysicsParams = 1e-3;  % HW [mm], Simulator [Meters]
AO.bpmy.Monitor.Physics2HWParams = 1000;
AO.bpmy.Monitor.Units        = 'Hardware';
AO.bpmy.Monitor.HWUnits      = 'mm';
AO.bpmy.Monitor.PhysicsUnits = 'meter';

%%%%%%%%
% Tune %
%%%%%%%%
AO.TUNE.FamilyName = 'TUNE';
AO.TUNE.MemberOf = {'TUNE';};
AO.TUNE.DeviceList = [1 1;1 2;1 3];
AO.TUNE.ElementList = [1;2;3];
AO.TUNE.Status = [1; 1; 0];
AO.TUNE.CommonNames = ['TuneX'; 'TuneY'; 'TuneS'];

AO.TUNE.Monitor.MemberOf   = {'TUNE'};
AO.TUNE.Monitor.Mode = 'Simulator'; 
AO.TUNE.Monitor.DataType = 'Scalar';
AO.TUNE.Monitor.HW2PhysicsParams = 1;
AO.TUNE.Monitor.Physics2HWParams = 1;
AO.TUNE.Monitor.Units        = 'Hardware';
AO.TUNE.Monitor.HWUnits      = 'kHz';
AO.TUNE.Monitor.PhysicsUnits = 'Tune';
AO.TUNE.Monitor.SpecialFunctionGet = @bfreq2tune;


%%%%%%%%%%
%   RF   %
%%%%%%%%%%
AO.RF.FamilyName                = 'RF';
AO.RF.MemberOf                  = {'RF'; 'RFSystem'};
AO.RF.DeviceList                = [ 1 1 ];
AO.RF.ElementList               = 1;
AO.RF.Status                    = 1;
AO.RF.Position                  = 0;

AO.RF.Monitor.MemberOf          = {};
AO.RF.Monitor.Mode              = 'Simulator';
AO.RF.Monitor.DataType          = 'Scalar';
AO.RF.Monitor.HW2PhysicsParams  = 1e+6;
AO.RF.Monitor.Physics2HWParams  = 1e-6;
AO.RF.Monitor.Units             = 'Hardware';
AO.RF.Monitor.HWUnits           = 'MHz';
AO.RF.Monitor.PhysicsUnits      = 'Hz';

AO.RF.Setpoint.MemberOf         = {'MachineConfig';};
AO.RF.Setpoint.Mode             = 'Simulator';
AO.RF.Setpoint.DataType         = 'Scalar';
AO.RF.Setpoint.HW2PhysicsParams = 1e+6;
AO.RF.Setpoint.Physics2HWParams = 1e-6;
AO.RF.Setpoint.Units            = 'Hardware';
AO.RF.Setpoint.HWUnits          = 'MHz';
AO.RF.Setpoint.PhysicsUnits     = 'Hz';
AO.RF.Setpoint.Range            = [400.0 600.0];
AO.RF.Setpoint.Tolerance        = 1.0;

AO.RF.VoltageCtrl.MemberOf          = {};
AO.RF.VoltageCtrl.Mode              = 'Simulator';
AO.RF.VoltageCtrl.DataType          = 'Scalar';
AO.RF.VoltageCtrl.ChannelNames      = '';
AO.RF.VoltageCtrl.HW2PhysicsParams  = 1;
AO.RF.VoltageCtrl.Physics2HWParams  = 1;
AO.RF.VoltageCtrl.Units             = 'Hardware';
AO.RF.VoltageCtrl.HWUnits           = 'Volts';
AO.RF.VoltageCtrl.PhysicsUnits      = 'Volts';

AO.RF.Voltage.MemberOf          = {};
AO.RF.Voltage.Mode              = 'Simulator';
AO.RF.Voltage.DataType          = 'Scalar';
AO.RF.Voltage.ChannelNames      = '';
AO.RF.Voltage.HW2PhysicsParams  = 1;
AO.RF.Voltage.Physics2HWParams  = 1;
AO.RF.Voltage.Units             = 'Hardware';
AO.RF.Voltage.HWUnits           = 'Volts';
AO.RF.Voltage.PhysicsUnits      = 'Volts';

AO.RF.Power.MemberOf          = {};
AO.RF.Power.Mode              = 'Simulator';
AO.RF.Power.DataType          = 'Scalar';
AO.RF.Power.ChannelNames      = '';          % ???
AO.RF.Power.HW2PhysicsParams  = 1;         
AO.RF.Power.Physics2HWParams  = 1;
AO.RF.Power.Units             = 'Hardware';
AO.RF.Power.HWUnits           = 'MWatts';           
AO.RF.Power.PhysicsUnits      = 'MWatts';
AO.RF.Power.Range             = [-inf inf];  % ???  
AO.RF.Power.Tolerance         = inf;  % ???  

AO.RF.Phase.MemberOf          = {'RF'; 'Phase'};
AO.RF.Phase.Mode              = 'Simulator';
AO.RF.Phase.DataType          = 'Scalar';
AO.RF.Phase.ChannelNames      = 'SRF1:STN:PHASE:CALC';    % ???  
AO.RF.Phase.Units             = 'Hardware';
AO.RF.Phase.HW2PhysicsParams  = 1; 
AO.RF.Phase.Physics2HWParams  = 1;
AO.RF.Phase.HWUnits           = 'Degrees';  
AO.RF.Phase.PhysicsUnits      = 'Degrees';

AO.RF.PhaseCtrl.MemberOf      = {'RF; Phase'; 'Control'};  % 'MachineConfig';
AO.RF.PhaseCtrl.Mode              = 'Simulator';
AO.RF.PhaseCtrl.DataType          = 'Scalar';
AO.RF.PhaseCtrl.ChannelNames      = 'SRF1:STN:PHASE';    % ???     
AO.RF.PhaseCtrl.Units             = 'Hardware';
AO.RF.PhaseCtrl.HW2PhysicsParams  = 1;         
AO.RF.PhaseCtrl.Physics2HWParams  = 1;
AO.RF.PhaseCtrl.HWUnits           = 'Degrees';  
AO.RF.PhaseCtrl.PhysicsUnits      = 'Degrees'; 
AO.RF.PhaseCtrl.Range             = [-200 200];    % ??? 
AO.RF.PhaseCtrl.Tolerance         = 10;    % ??? 



% %%%%%%%%%%%%%%
% %    DCCT    %
% %%%%%%%%%%%%%%
% AO.DCCT.FamilyName               = 'DCCT';
% AO.DCCT.MemberOf                 = {'Diagnostics'; 'DCCT'};
% AO.DCCT.DeviceList               = [1 1];
% AO.DCCT.ElementList              = 1;
% AO.DCCT.Status                   = 1;
% AO.DCCT.Position                 = 23.2555;
% 
% AO.DCCT.Monitor.MemberOf         = {};
% AO.DCCT.Monitor.Mode             = 'Simulator';
% AO.DCCT.Monitor.DataType         = 'Scalar';
% AO.DCCT.Monitor.ChannelNames     = 'AMC03';    
% AO.DCCT.Monitor.HW2PhysicsParams = 1;    
% AO.DCCT.Monitor.Physics2HWParams = 1;
% AO.DCCT.Monitor.Units            = 'Hardware';
% AO.DCCT.Monitor.HWUnits          = 'Ampere';     
% AO.DCCT.Monitor.PhysicsUnits     = 'Ampere';






% The operational mode sets the path, filenames, and other important parameters
% Run setoperationalmode after most of the AO is built so that the Units and Mode fields
% can be set in setoperationalmode
setao(AO);
%setoperationalmode(OperationalMode);





% Convert the response matrix delta to hardware units (if it's not already)
% 'NoEnergyScaling' is needed so that the qmf is not read to get the energy (this is a setup file)  

%AO = getao;
%AO.hcm.Setpoint.DeltaRespMat  = physics2hw('hcm', 'Setpoint', AO.hcm.Setpoint.DeltaRespMat, AO.hcm.DeviceList, 'NoEnergyScaling');
%AO.vcm.Setpoint.DeltaRespMat  = physics2hw('vcm', 'Setpoint', AO.vcm.Setpoint.DeltaRespMat, AO.vcm.DeviceList, 'NoEnergyScaling');
%AO.QF.Setpoint.DeltaRespMat   = physics2hw('QF',  'Setpoint', AO.QF.Setpoint.DeltaRespMat,  AO.QF.DeviceList,  'NoEnergyScaling');
%AO.QD.Setpoint.DeltaRespMat   = physics2hw('QD',  'Setpoint', AO.QD.Setpoint.DeltaRespMat,  AO.QD.DeviceList,  'NoEnergyScaling');
%AO.QFC.Setpoint.DeltaRespMat  = physics2hw('QFC', 'Setpoint', AO.QFC.Setpoint.DeltaRespMat, AO.QFC.DeviceList, 'NoEnergyScaling');
%AO.sf1a.Setpoint.DeltaRespMat   = physics2hw('SF',  'Setpoint', AO.sf1a.Setpoint.DeltaRespMat,  AO.sf1a.DeviceList,  'NoEnergyScaling');
%AO.sd1a.Setpoint.DeltaRespMat   = physics2hw('SD',  'Setpoint', AO.sd1a.Setpoint.DeltaRespMat,  AO.sd1a.DeviceList,  'NoEnergyScaling');
%AO.sf1b.Setpoint.DeltaRespMat   = physics2hw('SF',  'Setpoint', AO.sf1b.Setpoint.DeltaRespMat,  AO.sf1b.DeviceList,  'NoEnergyScaling');
%AO.sd1b.Setpoint.DeltaRespMat   = physics2hw('SD',  'Setpoint', AO.sd1b.Setpoint.DeltaRespMat,  AO.sd1b.DeviceList,  'NoEnergyScaling');
%setao(AO);

%sirius_comm_connect_inputdlg;
 
function DList = getDeviceList(NSector,NDevices)

DList = [];
DL = ones(NDevices,2);
DL(:,2) = (1:NDevices)';
for i=1:NSector
    DL(:,1) = i;
    DList = [DList; DL];
end

function [OnePerSector, TwoPerSector, ThreePerSector, FourPerSector, FivePerSector, SixPerSector, EightPerSector, TenPerSector, TwelvePerSector, FifteenPerSector, SixteenPerSector, EighteenPerSector, TwentyFourPerSector] = buildthedevicelists

NSector = 4;

OnePerSector=[];
TwoPerSector=[];
ThreePerSector=[];
FourPerSector=[];
FivePerSector=[];
SixPerSector=[];
EightPerSector=[];
TenPerSector=[];
TwelvePerSector=[];
FifteenPerSector=[];
SixteenPerSector=[];
EighteenPerSector=[];
TwentyFourPerSector=[];

for Sector =1:NSector  
    
    OnePerSector = [OnePerSector;
        Sector 1;];
    
    TwoPerSector = [TwoPerSector;
        Sector 1;
        Sector 2;];
    
    ThreePerSector = [ThreePerSector;
        Sector 1;
        Sector 2;
        Sector 3;];

    FourPerSector = [FourPerSector;
        Sector 1;
        Sector 2;
        Sector 3;
        Sector 4;];	
    
    FivePerSector = [FivePerSector;
        Sector 1;
        Sector 2;
        Sector 3;
        Sector 4;
        Sector 5;];	

    SixPerSector = [SixPerSector;
        Sector 1;
        Sector 2;
        Sector 3;
        Sector 4;
        Sector 5;
        Sector 6;];	
    
    EightPerSector = [EightPerSector;
        Sector 1;
        Sector 2;
        Sector 3;
        Sector 4;
        Sector 5;
        Sector 6;
        Sector 7;
        Sector 8;];	
    
   TenPerSector = [TenPerSector;
        Sector 1;
        Sector 2;
        Sector 3;
        Sector 4;
        Sector 5;
        Sector 6;
        Sector 7;
        Sector 8;
        Sector 9;
        Sector 10;];	
    
    TwelvePerSector = [TwelvePerSector;
        Sector 1;
        Sector 2;
        Sector 3;
        Sector 4;
        Sector 5;
        Sector 6;
        Sector 7;
        Sector 8;
        Sector 9;
        Sector 10;
        Sector 11;
        Sector 12;
        ];	
    
     FifteenPerSector = [FifteenPerSector;
        Sector 1;
        Sector 2;
        Sector 3;
        Sector 4;
        Sector 5;
        Sector 6;
        Sector 7;
        Sector 8;
        Sector 9;
        Sector 10;
        Sector 11;
        Sector 12;
        Sector 13;
        Sector 14;
        Sector 15;
        ];
    
    SixteenPerSector = [SixteenPerSector;
        Sector 1;
        Sector 2;
        Sector 3;
        Sector 4;
        Sector 5;
        Sector 6;
        Sector 7;
        Sector 8;
        Sector 9;
        Sector 10;
        Sector 11;
        Sector 12;
        Sector 13;
        Sector 14;
        Sector 15;
        Sector 16;
        ];
    
     EighteenPerSector = [EighteenPerSector;
        Sector 1;
        Sector 2;
        Sector 3;
        Sector 4;
        Sector 5;
        Sector 6;
        Sector 7;
        Sector 8;
        Sector 9;
        Sector 10;
        Sector 11;
        Sector 12;
        Sector 13;
        Sector 14;
        Sector 15;
        Sector 16;
        Sector 17;
        Sector 18;
        ];
     TwentyFourPerSector = [TwentyFourPerSector;
        Sector 1;
        Sector 2;
        Sector 3;
        Sector 4;
        Sector 5;
        Sector 6;
        Sector 7;
        Sector 8;
        Sector 9;
        Sector 10;
        Sector 11;
        Sector 12;
        Sector 13;
        Sector 14;
        Sector 15;
        Sector 16;
        Sector 17;
        Sector 18;
        Sector 19;
        Sector 20;
        Sector 21;
        Sector 22;
        Sector 23;
        Sector 24;
        ];
end

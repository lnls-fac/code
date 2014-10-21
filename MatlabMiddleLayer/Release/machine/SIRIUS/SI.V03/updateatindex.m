function updateatindex
%UPDATEATINDEX - Updates the AT indices in the MiddleLayer with the present AT lattice (THERING)
% 2012-07-10 Modificado para sirius3_lattice_e025 - Afonso


global THERING


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Append Accelerator Toolbox information %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Since changes in the AT model could change the AT indexes, etc,
% It's best to regenerate all the model indices whenever a model is loaded

% Sort by family first (findcells is linear and slow)
Indices = atindex(THERING);

AO = getao;




try
    % B1
    AO.b1.AT.ATType = 'BEND';
    AO.b1.AT.ATIndex = buildatindex(AO.b1.FamilyName, Indices.b1);
    AO.b1.Position = findspos(THERING, AO.b1.AT.ATIndex(:,1+floor(size(AO.b1.AT.ATIndex,2)/2)))';
      
catch
    warning('b1 family not found in the model.');
end

try
    % B2
    AO.b2.AT.ATType = 'BEND';
    AO.b2.AT.ATIndex = buildatindex(AO.b2.FamilyName, Indices.b2);
    AO.b2.Position = findspos(THERING, AO.b2.AT.ATIndex(:,1+floor(size(AO.b2.AT.ATIndex,2)/2)))';
      
catch
    warning('b2 family not found in the model.');
end

try
    % B3
    AO.b3.AT.ATType = 'BEND';
    AO.b3.AT.ATIndex = buildatindex(AO.b3.FamilyName, Indices.b3);
    AO.b3.Position = findspos(THERING, AO.b3.AT.ATIndex(:,1+floor(size(AO.b3.AT.ATIndex,2)/2)))';
      
catch
    warning('b3 family not found in the model.');
end

try
    % BC
    AO.bc.AT.ATType = 'BEND';
    AO.bc.AT.ATIndex = buildatindex(AO.bc.FamilyName, Indices.bc);
    AO.bc.Position = findspos(THERING, AO.bc.AT.ATIndex(:,1+floor(size(AO.bc.AT.ATIndex,2)/2)))';
      
catch
    warning('bc family not found in the model.');
end


try
    % qfa
    AO.qfa.AT.ATType = 'Quad';
    AO.qfa.AT.ATIndex = buildatindex(AO.qfa.FamilyName, Indices.qfa);
    AO.qfa.Position = findspos(THERING, AO.qfa.AT.ATIndex(:,1))';
catch
    warning('qfa family not found in the model.');
end

try
    % qda1
    AO.qda1.AT.ATType = 'Quad';
    AO.qda1.AT.ATIndex = buildatindex(AO.qda1.FamilyName, Indices.qda1);
    AO.qda1.Position = findspos(THERING, AO.qda1.AT.ATIndex(:,1))';
catch
    warning('qda1 family not found in the model.');
end

try
    % qfb
    AO.qfb.AT.ATType = 'Quad';
    AO.qfb.AT.ATIndex = buildatindex(AO.qfb.FamilyName, Indices.qfb);
    AO.qfb.Position = findspos(THERING, AO.qfb.AT.ATIndex(:,1))';
catch
    warning('qfb family not found in the model.');
end

try
    % qdb2
    AO.qdb2.AT.ATType = 'Quad';
    AO.qdb2.AT.ATIndex = buildatindex(AO.qdb2.FamilyName, Indices.qdb2);
    AO.qdb2.Position = findspos(THERING, AO.qdb2.AT.ATIndex(:,1))';
catch
    warning('qdb2 family not found in the model.');
end

try
    % qdb1
    AO.qdb1.AT.ATType = 'Quad';
    AO.qdb1.AT.ATIndex = buildatindex(AO.qdb1.FamilyName, Indices.qdb1);
    AO.qdb1.Position = findspos(THERING, AO.qdb1.AT.ATIndex(:,1))';
catch
    warning('qdb1 family not found in the model.');
end

try
    % QF1
    AO.qf1.AT.ATType = 'Quad';
    AO.qf1.AT.ATIndex = buildatindex(AO.qf1.FamilyName, Indices.qf1);
    AO.qf1.Position = findspos(THERING, AO.qf1.AT.ATIndex(:,1))';
    % QF2
    AO.qf2.AT.ATType = 'Quad';
    AO.qf2.AT.ATIndex = buildatindex(AO.qf2.FamilyName, Indices.qf2);
    AO.qf2.Position = findspos(THERING, AO.qf2.AT.ATIndex(:,1))';
    % QF3
    AO.qf3.AT.ATType = 'Quad';
    AO.qf3.AT.ATIndex = buildatindex(AO.qf3.FamilyName, Indices.qf3);
    AO.qf3.Position = findspos(THERING, AO.qf3.AT.ATIndex(:,1))';
    % QF4
    AO.qf4.AT.ATType = 'Quad';
    AO.qf4.AT.ATIndex = buildatindex(AO.qf4.FamilyName, Indices.qf4);
    AO.qf4.Position = findspos(THERING, AO.qf4.AT.ATIndex(:,1))';
catch
    warning('qf1 qf2 qf3 qf4 families not found in the model.');
end

try
    % sda
    AO.sda.AT.ATType = 'Sext';
    AO.sda.AT.ATIndex = buildatindex(AO.sda.FamilyName, Indices.sda);
    AO.sda.Position = findspos(THERING, AO.sda.AT.ATIndex(:,1))';
catch
    warning('sda family not found in the model.');
end

try
    % sfa
    AO.sfa.AT.ATType = 'Sext';
    AO.sfa.AT.ATIndex = buildatindex(AO.sfa.FamilyName, Indices.sfa);
    AO.sfa.Position = findspos(THERING, AO.sfa.AT.ATIndex(:,1))';
catch
    warning('sfa family not found in the model.');
end


try
    % SD1A
    AO.sd1a.AT.ATType = 'Sext';
    AO.sd1a.AT.ATIndex = buildatindex(AO.sd1a.FamilyName, Indices.sd1a);
    AO.sd1a.Position = findspos(THERING, AO.sd1a.AT.ATIndex(:,1))';
catch
    warning('sd1a family not found in the model.');
end

try
    % SF1A
    AO.sf1a.AT.ATType = 'Sext';
    AO.sf1a.AT.ATIndex = buildatindex(AO.sf1a.FamilyName, Indices.sf1a);
    AO.sf1a.Position = findspos(THERING, AO.sf1a.AT.ATIndex(:,1))';
catch
    warning('sf1a family not found in the model.');
end

try
    % SD2A
    AO.sd2a.AT.ATType = 'Sext';
    AO.sd2a.AT.ATIndex = buildatindex(AO.sd2a.FamilyName, Indices.sd2a);
    AO.sd2a.Position = findspos(THERING, AO.sd2a.AT.ATIndex(:,1))';
catch
    warning('sd2a family not found in the model.');
end

try
    % SD3A
    AO.sd3a.AT.ATType = 'Sext';
    AO.sd3a.AT.ATIndex = buildatindex(AO.sd3a.FamilyName, Indices.sd3a);
    AO.sd3a.Position = findspos(THERING, AO.sd3a.AT.ATIndex(:,1))';
catch
    warning('sd3a family not found in the model.');
end


try
    % SF2A
    AO.sf2a.AT.ATType = 'Sext';
    AO.sf2a.AT.ATIndex = buildatindex(AO.sf2a.FamilyName, Indices.sf2a);
    AO.sf2a.Position = findspos(THERING, AO.sf2a.AT.ATIndex(:,1))';
catch
    warning('sf2a family not found in the model.');
end

try
    % SD1B
    AO.sd1b.AT.ATType = 'Sext';
    AO.sd1b.AT.ATIndex = buildatindex(AO.sd1b.FamilyName, Indices.sd1b);
    AO.sd1b.Position = findspos(THERING, AO.sd1b.AT.ATIndex(:,1))';
catch
    warning('sd1b family not found in the model.');
end

try
    % SF1B
    AO.sf1b.AT.ATType = 'Sext';
    AO.sf1b.AT.ATIndex = buildatindex(AO.sf1b.FamilyName, Indices.sf1b);
    AO.sf1b.Position = findspos(THERING, AO.sf1b.AT.ATIndex(:,1))';
catch
    warning('sf1b family not found in the model.');
end

try
    % SD2B
    AO.sd2b.AT.ATType = 'Sext';
    AO.sd2b.AT.ATIndex = buildatindex(AO.sd2b.FamilyName, Indices.sd2b);
    AO.sd2b.Position = findspos(THERING, AO.sd2b.AT.ATIndex(:,1))';
catch
    warning('sd2b family not found in the model.');
end

try
    % SD3B
    AO.sd3b.AT.ATType = 'Sext';
    AO.sd3b.AT.ATIndex = buildatindex(AO.sd3b.FamilyName, Indices.sd3b);
    AO.sd3b.Position = findspos(THERING, AO.sd3b.AT.ATIndex(:,1))';
catch
    warning('sd3b family not found in the model.');
end


try
    % SF2B
    AO.sf2b.AT.ATType = 'Sext';
    AO.sf2b.AT.ATIndex = buildatindex(AO.sf2b.FamilyName, Indices.sf2b);
    AO.sf2b.Position = findspos(THERING, AO.sf2b.AT.ATIndex(:,1))';
catch
    warning('sf2b family not found in the model.');
end

try
    % sfb
    AO.sfb.AT.ATType = 'Sext';
    AO.sfb.AT.ATIndex = buildatindex(AO.sfb.FamilyName, Indices.sfb);
    AO.sfb.Position = findspos(THERING, AO.sfb.AT.ATIndex(:,1))';
catch
    warning('sfb family not found in the model.');
end

try
    % sdb
    AO.sdb.AT.ATType = 'Sext';
    AO.sdb.AT.ATIndex = buildatindex(AO.sdb.FamilyName, Indices.sdb);
    AO.sdb.Position = findspos(THERING, AO.sdb.AT.ATIndex(:,1))';
catch
    warning('sdb family not found in the model.');
end

try
    % BPMx
    AO.bpmx.AT.ATType = 'X';
    AO.bpmx.AT.ATIndex = buildatindex(AO.bpmx.FamilyName, Indices.bpm);
    AO.bpmx.Position = findspos(THERING, AO.bpmx.AT.ATIndex(:,1))';   
catch
    warning('bpmx family not found in the model.');
end

try
    % BPMy
    AO.bpmy.AT.ATType = 'Y';
    AO.bpmy.AT.ATIndex = buildatindex(AO.bpmy.FamilyName, Indices.bpm);
    AO.bpmy.Position = findspos(THERING, AO.bpmy.AT.ATIndex(:,1))';   
catch
    warning('bpmy family not found in the model.');
end

try
    % HCM
    AO.hcm.AT.ATType = 'HCM';
    li = [];
    if isfield(Indices, 'cm'), li = [li Indices.cm]; end;
    if isfield(Indices, 'hcm'), li = [li Indices.hcm]; end;
    AO.hcm.AT.ATIndex = buildatindex(AO.hcm.FamilyName, sort(li));
    AO.hcm.Position = findspos(THERING, AO.hcm.AT.ATIndex(:,1))';   
catch
    warning('hcm family not found in the model.');
end


try
    % VCM
    AO.vcm.AT.ATType = 'VCM';
    li = [];
    if isfield(Indices, 'cm'), li = [li Indices.cm]; end;
    if isfield(Indices, 'vcm'), li = [li Indices.vcm]; end;
    AO.vcm.AT.ATIndex = buildatindex(AO.vcm.FamilyName, sort(li));
    AO.vcm.Position = findspos(THERING, AO.vcm.AT.ATIndex(:,1))';   
catch
    warning('vcm family not found in the model.');
end



% RF Cavity
try
    AO.RF.AT.ATType = 'RF Cavity';
    AO.RF.AT.ATIndex = findcells(THERING,'Frequency')';
    AO.RF.Position = findspos(THERING, AO.RF.AT.ATIndex(:,1))';
catch
    warning('RF cavity not found in the model.');
end

try
    % SKEWCM
    AO.skewcm.AT.ATType = 'SkewCorrector';
    
    
    AO.skewcm.AT.ATIndex = [ ...
         AO.sd1a.AT.ATIndex; ...
         AO.sf1a.AT.ATIndex; ...
         AO.sd1b.AT.ATIndex; ...
         AO.sf1b.AT.ATIndex; ...
         AO.sfa.AT.ATIndex; ...
         AO.sda.AT.ATIndex; ...
         AO.sd3a.AT.ATIndex; ...
         AO.sd2a.AT.ATIndex; ...
         AO.sf2a.AT.ATIndex; ...
         AO.sd3b.AT.ATIndex; ...
         AO.sd2b.AT.ATIndex; ...
         AO.sf2b.AT.ATIndex; ...
        ];
    [tmp idx] = sort(AO.skewcm.AT.ATIndex(:,1));
    AO.skewcm.AT.ATIndex = AO.skewcm.AT.ATIndex(idx,:);
    AO.skewcm.Position = findspos(THERING, AO.skewcm.AT.ATIndex(:,1))';   
    
catch
    warning('SKEWCM family not found in the model.');
end


setao(AO);



% Set TwissData at the start of the storage ring
% try
%     % BTS twiss parameters at the input
%     TwissData.alpha = [0 0]';
%     TwissData.beta  = [15.6475 0.7037]';
%     TwissData.mu    = [0 0]';
%     TwissData.ClosedOrbit = [0 0 0 0]';
%     TwissData.dP = 0;
%     TwissData.dL = 0;
%     TwissData.Dispersion  = [0 0 0 0]';
%     
%     setpvmodel('TwissData', '', TwissData);  % Same as, THERING{1}.TwissData = TwissData;
% catch
%      warning('Setting the twiss data parameters in the MML failed.');
% end

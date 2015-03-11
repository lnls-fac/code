function data = sirius_si_family_data(the_ring)

data.b1.nr_segs   = 2;
data.b2.nr_segs   = 3;
data.b3.nr_segs   = 2;
data.bc.nr_segs   = 12;

data.qfa.nr_segs  = 1;
data.qda.nr_segs  = 1;
data.qdb2.nr_segs = 1;
data.qfb.nr_segs  = 1;
data.qdb1.nr_segs = 1;
data.qf1.nr_segs  = 1;
data.qf2.nr_segs  = 1;
data.qf3.nr_segs  = 1;
data.qf4.nr_segs  = 1;

data.sda.nr_segs = 1;
data.sfa.nr_segs = 1;
data.sdb.nr_segs = 1;
data.sfb.nr_segs = 1;
data.sd1.nr_segs = 1;
data.sf1.nr_segs = 1;
data.sd2.nr_segs = 1;
data.sd3.nr_segs = 1;
data.sf2.nr_segs = 1;
data.sd6.nr_segs = 1;
data.sf4.nr_segs = 1;
data.sd5.nr_segs = 1;
data.sd4.nr_segs = 1;
data.sf3.nr_segs = 1;

data.bpm.nr_segs = 1;
data.cf.nr_segs  = 1;
data.chf.nr_segs = 1;
data.cvf.nr_segs = 1;
data.qs.nr_segs  = 1;
data.chs.nr_segs = 1;
data.cvs.nr_segs = 1;
data.qn.nr_segs  = 1;

fams = fields(data);
for i=1:length(fams)
    idx = sort(findcells(the_ring, 'FamName', fams{i}));
    if ~isempty(idx)
        idx = reshape(idx, data.(fams{i}).nr_segs, []);
        data.(fams{i}).ATIndex = idx';
    end
end

% chs - slow horizontal correctors
idx = [];
idx = [idx findcells(the_ring, 'FamName', 'sfa')];
idx = [idx findcells(the_ring, 'FamName', 'sd1')];
idx = [idx findcells(the_ring, 'FamName', 'sd2')];
idx = [idx findcells(the_ring, 'FamName', 'sf2')];
idx = [idx findcells(the_ring, 'FamName', 'sf3')];
idx = [idx findcells(the_ring, 'FamName', 'sd5')];
idx = [idx findcells(the_ring, 'FamName', 'sd6')];
idx = [idx findcells(the_ring, 'FamName', 'sfb')];
idx = sort(idx);
data.chs.ATIndex = reshape(idx,data.chs.nr_segs,[]);
data.chs.ATIndex = data.chs.ATIndex';

% cvs - slow horizontal correctors
idx = [];
idx = [idx findcells(the_ring, 'FamName', 'sfa')];
idx = [idx findcells(the_ring, 'FamName', 'sd1')];
idx = [idx findcells(the_ring, 'FamName', 'sd3')];
idx = [idx findcells(the_ring, 'FamName', 'sd4')];
idx = [idx findcells(the_ring, 'FamName', 'sd6')];
idx = [idx findcells(the_ring, 'FamName', 'sfb')];
idx = sort(idx);
data.cvs.ATIndex = reshape(idx,data.chs.nr_segs,[]);
data.cvs.ATIndex = data.cvs.ATIndex';

% chf - fast horizontal correctors
idx = [];
idx = [idx findcells(the_ring, 'FamName', 'cf')];
idx = sort(idx);
data.chf.ATIndex = reshape(idx,data.chf.nr_segs,[]);
data.chf.ATIndex = data.chf.ATIndex';

% cvf - fast vertical correctors
idx = [];
idx = [idx findcells(the_ring, 'FamName', 'cf')];
idx = sort(idx);
data.cvf.ATIndex = reshape(idx,data.cvf.nr_segs,[]);
data.cvf.ATIndex = data.cvf.ATIndex';

% qs - skew quad correctors
idx = [];
idx = [idx findcells(the_ring, 'FamName', 'cf')];
idx = sort(idx);
data.qs.ATIndex = reshape(idx,data.qs.nr_segs,[]);
data.qs.ATIndex = data.qs.ATIndex';

% kbs - quadrupoles knobs for optics correction
idx = [];
idx = [idx findcells(the_ring, 'FamName', 'qfa')];
idx = [idx findcells(the_ring, 'FamName', 'qda')];
idx = [idx findcells(the_ring, 'FamName', 'qf1')];
idx = [idx findcells(the_ring, 'FamName', 'qf2')];
idx = [idx findcells(the_ring, 'FamName', 'qf3')];
idx = [idx findcells(the_ring, 'FamName', 'qf4')];
idx = [idx findcells(the_ring, 'FamName', 'qdb1')];
idx = [idx findcells(the_ring, 'FamName', 'qfb')];
idx = [idx findcells(the_ring, 'FamName', 'qdb2')];
idx = sort(idx);
data.qn.ATIndex = reshape(idx,data.qn.nr_segs,[]);
data.qn.ATIndex = data.qn.ATIndex';

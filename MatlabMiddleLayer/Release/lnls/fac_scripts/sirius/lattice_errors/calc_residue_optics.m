function v = calc_residue_optics(the_ring, the_ring0)

scale_beta = 1;      % m
scale_eta  = 0.05;   % m
scale_tune = 0.0005; % tune

twiss0 = getappdata(0, 'TwissTheRing0');
if isempty(twiss0)
    twiss0 = calctwiss(the_ring0);
    setappdata(0, 'TwissTheRing0', twiss0);
end
twiss1 = calctwiss(the_ring);


% v = [twiss1.mux(end) - twiss0.mux(end); twiss1.muy(end) - twiss0.muy(end)] / 2 / pi / scale_tune;
% v = [v; (twiss1.betax - twiss0.betax)/scale_beta];
% v = [v; (twiss1.betay - twiss0.betay)/scale_beta];
% v = [v; (twiss1.etax - twiss0.etax)/scale_eta];
% v = [v; (twiss1.etay - twiss0.etay)/scale_eta];


% mudança para considerar ótica somente em pontos onde pode ser medida

idx1 = findcells(the_ring, 'K');
idx2 = findcells(the_ring, 'BendingAngle');
quad = setdiff(idx1,idx2);
bpms = findcells(the_ring, 'FamName', 'BPM');
v = [twiss1.mux(end) - twiss0.mux(end); twiss1.muy(end) - twiss0.muy(end)] / 2 / pi / scale_tune;
v = [v; (twiss1.betax(quad) - twiss0.betax(quad))/scale_beta];
v = [v; (twiss1.betay(quad) - twiss0.betay(quad))/scale_beta];
v = [v; (twiss1.etax(bpms) - twiss0.etax(bpms))/scale_eta];
v = [v; (twiss1.etay(bpms) - twiss0.etay(bpms))/scale_eta];



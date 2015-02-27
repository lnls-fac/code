function v = calc_residue_optics(the_ring, tune0, bpms, hcms, vcms, nper)

DISPWEIGHT = 1e4;   % m
TUNEWEIGHT = 1e8; % tune

% twiss0 = getappdata(0, 'TwissTheRing0');
% if isempty(twiss0)
%     twiss0 = calctwiss(the_ring0);
%     setappdata(0, 'TwissTheRing0', twiss0);
% end
% twiss1 = calctwiss(the_ring);
% 
% 
% % v = [twiss1.mux(end) - twiss0.mux(end); twiss1.muy(end) - twiss0.muy(end)] / 2 / pi / scale_tune;
% % v = [v; (twiss1.betax - twiss0.betax)/scale_beta];
% % v = [v; (twiss1.betay - twiss0.betay)/scale_beta];
% % v = [v; (twiss1.etax - twiss0.etax)/scale_eta];
% % v = [v; (twiss1.etay - twiss0.etay)/scale_eta];
% 
% 
% % mudança para considerar ótica somente em pontos onde pode ser medida
% 
% idx1 = findcells(the_ring, 'K');
% idx2 = findcells(the_ring, 'BendingAngle');
% quad = setdiff(idx1,idx2);
% bpms = findcells(the_ring, 'FamName', 'BPM');
% v = [twiss1.mux(end) - twiss0.mux(end); twiss1.muy(end) - twiss0.muy(end)] / 2 / pi / scale_tune;
% v = [v; (twiss1.betax(quad) - twiss0.betax(quad))/scale_beta];
% v = [v; (twiss1.betay(quad) - twiss0.betay(quad))/scale_beta];
% v = [v; (twiss1.etax(bpms) - twiss0.etax(bpms))/scale_eta];
% v = [v; (twiss1.etay(bpms) - twiss0.etay(bpms))/scale_eta];

if ~exist('nper','var'), nper = 1; end

nr_bpms = length(bpms);
nr_hcms = length(hcms);
nr_vcms = length(vcms);

len_bpm = nr_bpms/nper;
len_hcm = nr_hcms/nper;
len_vcm = nr_vcms/nper;

%[TD, ~, ~] = twissring(the_ring, 0, 1:length(the_ring)+1, 'chrom', 1e-8);
Dispersion  = calc_dispersion(the_ring,0,bpms)';
Dispersion = Dispersion(:,1);
M = get_response_matrix(the_ring, bpms, hcms, vcms);
M = mat2cell(M, [nr_bpms,nr_bpms],[nr_hcms, nr_vcms]);
Mxx = M{1,1}; % orbit x kick y
Myy = M{2,2}; % orbit y kick x


%% for optics matrix calculation purposes:
for i1=2:(nper)
    Mxx(:,:,i1) = circshift(Mxx(:,:,1),[len_bpm, len_hcm]*(i1-1));
    
    Myy(:,:,i1) = circshift(Myy(:,:,1),[len_bpm, len_vcm]*(i1-1)); %the last bpm turns into the first
    Dispersion(:,i1) = circshift(Dispersion(:,1),len_bpm*(i1-1));
end
Dispersion = reshape(Dispersion,[nr_bpms,1,nper]);

%% Calculation of the residue
v = [];

%Values imposed by the model:
%Dispersion in the straights must be 0
indcs = logical(repmat([1,0,0,0,0,0,0,0,1],1,20));
A = DISPWEIGHT * reshape(Dispersion(indcs,:,:),sum(indcs),nper);
v = [v; A];
%Tunes must be the ones specified
[~, tune]  =  twissring(the_ring, 0, 1:length(the_ring));
A = TUNEWEIGHT * repmat(tune(:)-tune0(:),[1,nper]);
v = [v;A];


%Translational Symmetries:
sym = 10;
A = circshift(Mxx,[nr_bpms, nr_hcms]/sym);
v = [v; reshape(A-Mxx,nr_bpms*nr_hcms,nper)];
A = circshift(Myy,[len_bpm, len_vcm]); %the last bpm turns into the first
v = [v; reshape(A-Myy,nr_bpms*nr_vcms,nper)];
indcs = ~indcs;
A = circshift(Dispersion(indcs,:,:),sum(indcs)/sym);
v = [v; DISPWEIGHT * reshape(A-Dispersion(indcs,:,:),sum(indcs),nper)];


% Mirror Symetries:
Psym = sort([findcells(the_ring,'FamName','mia'), findcells(the_ring,'FamName','mib')]);
Psym = Psym(1:length(Psym)/2);
bpm_idx = logical(repmat([1,1,0,1,0,1,1,0,1],1,20));
hcm_idx = logical(repmat([1,1,1,1,1,1,1,1],1,20));
vcm_idx = logical(repmat([1,1,1,1,1,1],1,20));
Mxx = Mxx(bpm_idx,hcm_idx,:);
Myy = Myy(bpm_idx,vcm_idx,:);
Disp = Dispersion(bpm_idx,:,:);
bpm_idx = bpms(bpm_idx); lenB = length(bpm_idx);
hcm_idx = hcms(hcm_idx); lenH = length(hcm_idx);
vcm_idx = vcms(vcm_idx); lenV = length(vcm_idx);
for i1=Psym
    shift_bpm = sum(bpm_idx < i1);
    shift_hcm = sum(hcm_idx < i1);
    shift_vcm = sum(vcm_idx < i1);
    Ax = circshift(Mxx,-[shift_bpm,shift_hcm]);
    Ay = circshift(Myy,-[shift_bpm,shift_vcm]);
    D  = circshift(Disp,-shift_bpm);
    for n=1:nper
        Ax1 = Ax(:,:,n);
        Ay1 = Ay(:,:,n);
        D1 = D(:,:,n);
        Ax1 = mat2cell(Ax1,lenB/2*[1 1], lenH/2*[1 1]);
        Ay1 = mat2cell(Ay1,lenB/2*[1 1], lenV/2*[1 1]);
        D1 = mat2cell(D1,lenB/2*[1 1]);
        Ax2(:,:,n) = (Ax1{1,1} - rot90(Ax1{2,2},2))';
        Ay2(:,:,n) = (Ay1{1,1} - rot90(Ay1{2,2},2))';
        D2(:,:,n) = DISPWEIGHT * (D1{1} - fliplr(D1{2}))';
    end
    v = [v;reshape([Ax2;Ay2;D2],lenB/2*((lenH + lenV)/2+1),nper)];
end






function dispersion = calc_dispersion(the_ring,dp, idx)

ddp = 1e-8;

orbn = findorbit4(the_ring,dp-ddp,idx);
orbp = findorbit4(the_ring,dp+ddp,idx);
dispersion = (orbp - orbn) / (2*ddp);

function v = calc_residue_coupling(the_ring, bpms, hcms, vcms, nper)

if ~exist('nper','var'), nper = 1; end

nr_bpms = length(bpms);
nr_hcms = length(hcms);
nr_vcms = length(vcms);

len_bpm = nr_bpms/nper;
len_hcm = nr_hcms/nper;
len_vcm = nr_vcms/nper;

%[TD, ~, ~] = twissring(the_ring, 0, 1:length(the_ring)+1, 'chrom', 1e-8);
Dispersion  = calc_dispersion(the_ring,0,bpms)';
Dispersion = Dispersion(:,3);
M = get_response_matrix(the_ring, bpms, hcms, vcms);
M = mat2cell(M, [nr_bpms,nr_bpms],[nr_hcms, nr_vcms]);
Mxy = M{1,2}; % orbit x kick y
Myx = M{2,1}; % orbit y kick x


%% for coupling matrix calculation purposes:
for i1=2:(nper)
    Myx(:,:,i1) = circshift(Myx(:,:,1),[len_bpm, len_hcm]*(i1-1));
    
    Mxy(:,:,i1) = circshift(Mxy(:,:,1),[len_bpm, len_vcm]*(i1-1)); %the last bpm turns into the first
    Dispersion(:,i1) = circshift(Dispersion(:,1),len_bpm*(i1-1));
end
Dispersion = reshape(Dispersion,[nr_bpms,1,nper]);
%% Calculation of the residue

%v = [Mxy(:); Myx(:)];
disp_weight = (nr_hcms + nr_vcms)*10;
v = permute([Myx, Mxy, disp_weight * Dispersion],[2 1 3]); % para ficar ordenado por bpm
v = reshape(v,(nr_hcms + nr_vcms + 1)*nr_bpms,nper);
% v = [10*dispersion_weight * Dispersion(bpms,3); Mxy(:); Myx(:)];


function dispersion = calc_dispersion(the_ring,dp, idx)

ddp = 1e-8;

orbn = findorbit4(the_ring,dp-ddp,idx);
orbp = findorbit4(the_ring,dp+ddp,idx);
dispersion = (orbp - orbn) / (2*ddp);
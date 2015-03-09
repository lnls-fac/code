function [Mxx,Mxy,Myx, Myy, Dispx, Dispy] = prepare_data_for_symm(the_ring, optics, M, Disp)

len_bpms = length(optics.bpm_idx);
if optics.simul_bpm_corr_err
    bpm_gains = getcellstruct(the_ring,'Gains',optics.bpm_idx);
    hcm_gains = getcellstruct(the_ring,'Gain',optics.hcm_idx)';
    vcm_gains = getcellstruct(the_ring,'Gain',optics.vcm_idx)';
    M = repmat([hcm_gains,vcm_gains],size(M,1),1).*M;
    for i=1:length(bpm_gains)
        M(i+[0,len_bpms],:) = bpm_gains{i}*M(i+[0,len_bpms],:);
        Disp([1,3],i) = bpm_gains{i}*Disp([1,3],i);
    end
end

M = mat2cell(M,len_bpms*[1,1],[length(optics.hcm_idx), length(optics.vcm_idx)]);
Mxx = M{1,1};
Mxy = M{1,2};
Myx = M{2,1};
Myy = M{2,2};

Dispx = Disp(1,:);
Dispy = Disp(3,:);
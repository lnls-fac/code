function [the_ring hkicks vkicks] = sirius_lattice_errors_correct_orbit_coupling(the_ring0, r)

the_ring = the_ring0;

max_iterations = r.config.cod.max_iterations;
eig_cutoff     = r.config.cod.eig_cutoff;

%HKicks = zeros(length(r.params.cod.hcms_idx),1);
%VKicks = zeros(length(r.params.cod.vcms_idx),1);

HKicks = getcellstruct(the_ring0, 'KickAngle', r.params.cod.hcms_idx(logical(r.params.cod.hcm_selection)), 1, 1);
VKicks = getcellstruct(the_ring0, 'KickAngle', r.params.cod.vcms_idx(logical(r.params.cod.vcm_selection)), 1, 2);


co0_rx = r.optics0.cox(r.params.cod.bpms_idx(logical(r.params.cod.bpm_selection)))';
co0_ry = r.optics0.coy(r.params.cod.bpms_idx(logical(r.params.cod.bpm_selection)))';
MXX = r.params.cod.respm.MXX(r.params.cod.bpms_idx(logical(r.params.cod.bpm_selection)),logical(r.params.cod.hcm_selection));
MYX = r.params.cod.respm.MYX(r.params.cod.bpms_idx(logical(r.params.cod.bpm_selection)),logical(r.params.cod.hcm_selection));
MYY = r.params.cod.respm.MYY(r.params.cod.bpms_idx(logical(r.params.cod.bpm_selection)),logical(r.params.cod.vcm_selection));
MXY = r.params.cod.respm.MXY(r.params.cod.bpms_idx(logical(r.params.cod.bpm_selection)),logical(r.params.cod.vcm_selection));

M = [MXX MXY; MYX MYY];
[U,S,V] = svd(M, 'econ');
Si = diag(1./diag(S));
Ut = U';

rr = length(find(diag(S) / S(1) > eig_cutoff)); 
Si(((rr(1)+1)*(rr(1)+1)):end) = 0;


max_delta_residue = 1;

GUESS = [0 0 0 0 0 0]';
%co = sirius_lattice_errors_findsyncorbit(the_ring,0,r.params.cod.bpms_idx, GUESS);
co = sirius_lattice_errors_findorbit4(the_ring,0,r.params.cod.bpms_idx(logical(r.params.cod.bpm_selection)), GUESS);
%co = sirius_lattice_errors_findorbit6(the_ring,r.params.cod.bpms_idx, GUESS);
co1_rx = co(1,:)';
co1_ry = co(3,:)';

residueX = co1_rx - co0_rx;
residueY = co1_ry - co0_ry;

%plot(1000*residueX);

str = 1;


for c=1:max_iterations
%while (max_delta_residue > 1e-8)
    
    pause(0.1);
    drawnow;
    
    UtR = Ut * [residueX; residueY];
    
    % se necess�rio elimina menores valores singulares, um por um, at� que m�ximo kick
    % seja menor que tolerancia.
    for i=length(diag(Si)):-1:1
        if i<length(diag(Si)), Si(i+1,i+1) = 0; end;
        Kicks = -(V * Si * UtR);
        KicksX = Kicks(1:length(HKicks));
        KicksY = Kicks(length(HKicks)+1:end);
        MaxKickX = max(abs(HKicks(:) + KicksX(:)));
        if (MaxKickX <= r.config.cod.max_hkick), break; end
        MaxKickY = max(abs(VKicks(:) + KicksY(:)));
        if (MaxKickY <= r.config.cod.max_vkick), break; end
    end
    HKicks = HKicks + str * KicksX;
    VKicks = VKicks + str * KicksY;
    
    the_ring = lattice_errors_set_correctors(r, the_ring, HKicks, VKicks);
    
    %co = sirius_lattice_errors_findsyncorbit(the_ring,0,r.params.cod.bpms_idx, GUESS);
    co = sirius_lattice_errors_findorbit4(the_ring,0,r.params.cod.bpms_idx(logical(r.params.cod.bpm_selection)), GUESS);
    %co = sirius_lattice_errors_findorbit6(the_ring,r.params.cod.bpms_idx, GUESS);
    co1_rx = co(1,:)';
    co1_ry = co(3,:)';
    
    %GUESS = [co(:,1); 0];
   GUESS = [co(:,1); 0; 0];
    
    GUESS = GUESS(1:6,:);
    
    new_residueX = co1_rx - co0_rx;
    new_residueY = co1_ry - co0_ry;
    
    max_delta_residue = max(abs([new_residueX - residueX; new_residueY - residueY]));
    residueX = new_residueX;
    residueY = new_residueY;  
    
    % residue
    HKicksAll(:,c) = HKicks;
    VKicksAll(:,c) = VKicks;
    ResidueXAll(:,c) = residueX;
    ResidueYAll(:,c) = residueY;
    
    %disp([norm(residueX) norm(residueY)]);
    %hold all; plot(1000*residueX);
    
end

% selects best iteration
[tmp idx] = min(max(abs(ResidueXAll)));
HKicks = HKicksAll(:,idx);
VKicks = VKicksAll(:,idx);
the_ring = lattice_errors_set_correctors(r, the_ring, HKicks, VKicks);

hkicks = zeros(size(r.params.cod.hcms_idx));
hkicks(logical(r.params.cod.hcm_selection)) = HKicks;
vkicks = zeros(size(r.params.cod.vcms_idx));
vkicks(logical(r.params.cod.vcm_selection)) = VKicks;


% if any(isnan(co))
%     hkicks = nan * hkicks;
%     vkicks = nan * vkicks;
% end







function ring1 = lattice_errors_set_correctors(r, ring0, HKicks, VKicks)

ring1 = ring0;
hkik_idxselection = r.params.cod.hcms_idx(logical(r.params.cod.hcm_selection));
for i=1:length(hkik_idxselection)
    ring1{hkik_idxselection(i)}.KickAngle(1) = HKicks(i);
end
vkik_idxselection = r.params.cod.vcms_idx(logical(r.params.cod.vcm_selection));
for i=1:length(vkik_idxselection)
    ring1{vkik_idxselection(i)}.KickAngle(2) = VKicks(i);
end


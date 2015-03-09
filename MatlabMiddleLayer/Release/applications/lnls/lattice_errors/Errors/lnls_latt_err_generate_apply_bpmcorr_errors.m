function the_ring = generate_apply_bpmcorr_errors(name, the_ring, control, cutoff, rndtype)

if ~exist('cutoff','var'), cutoff = inf; end
if ~exist('rndtype','var'), rndtype = 'gaussian'; end;


save([name,'_bpmcorr_errors_input.mat'],'control','cutoff','rndtype');

if ~iscell(the_ring{1}), the_ring = {the_ring};end

if isfield(control,'bpm')
    bpm = control.bpm;
    for i = 1:length(the_ring)
        if isfield(bpm,'sigma_offsetx') && any(bpm.sigma_offsetx) && ...
           isfield(bpm,'sigma_offsety') && any(bpm.sigma_offsety)
            % Set offsets Additively to old ones
            errorsx = get_random_numbers(bpm.sigma_offsetx,length(bpm.idx),cutoff,rndtype);
            errorsy = get_random_numbers(bpm.sigma_offsety,length(bpm.idx),cutoff,rndtype);
            offsets = [errorsx,errorsy];
            if isfield(the_ring{i}{bpm.idx(1)},'Offsets')
                offsets_old = getcellstruct(the_ring{i},'Offsets',bpm.idx);
                offsets_old = cell2mat(offsets_old);
                offsets = offsets + offsets_old;
            end
            errors = mat2cell(offsets,ones(1,length(offsets)),2);
            the_ring{i} = setcellstruct(the_ring{i},'Offsets',bpm.idx,errors);
        end
        
        % Set gain-matrix replacing old values
        if isfield(bpm,'sigma_matrix') && any(any(bpm.sigma_matrix))
            bxx = get_random_numbers(bpm.sigma_matrix(1,1),length(bpm.idx),cutoff,rndtype);
            bxy = get_random_numbers(bpm.sigma_matrix(1,2),length(bpm.idx),cutoff,rndtype);
            byx = get_random_numbers(bpm.sigma_matrix(2,1),length(bpm.idx),cutoff,rndtype);
            byy = get_random_numbers(bpm.sigma_matrix(2,2),length(bpm.idx),cutoff,rndtype);
            mats = mat2cell(reshape([1+bxx,byx,bxy,1+byy]',2,2*length(bxx)),2,(2+0*bxx));
            the_ring{i} = setcellstruct(the_ring{i},'Gains',bpm.idx,mats);
        end
    end
end

if isfield(control,'hcm') && isfield(control.hcm,'sigma_gain') && any(control.hcm.sigma_gain)
    hcm = control.hcm;
    for i = 1:length(the_ring)
        % Set gains replacing old values
        if any(hcm.sigma_gain)
            errors = get_random_numbers(hcm.sigma_gain,length(hcm.idx),cutoff,rndtype);
            the_ring{i} = setcellstruct(the_ring{i},'Gain', hcm.idx, 1 + errors);
        end
    end
end

if isfield(control,'vcm') && isfield(control.vcm,'sigma_gain') && any(control.vcm.sigma_gain)
    vcm = control.vcm;
    for i = 1:length(the_ring)
        % Set gains replacing old values
        if any(vcm.sigma_gain)
            errors = get_random_numbers(vcm.sigma_gain,length(vcm.idx),cutoff,rndtype);
            the_ring{i} = setcellstruct(the_ring{i},'Gain', vcm.idx, 1 + errors);
        end
    end
end

if length(the_ring) == 1, the_ring = the_ring{1}; end


function rndnr = get_random_numbers(sigma, nrels, cutoff, type)
max_value = cutoff;
rndnr = zeros(nrels,1);
sel = 1:nrels;
if any(strcmpi(type, {'gaussian','gauss','norm', 'normal'}))
    while ~isempty(sel)
        rndnr(sel) = randn(1,length(sel));
        sel = find(abs(rndnr) > max_value);
    end
elseif any(strcmpi(type, {'sin','vibration','ripple', 'cos','time-average'}))
    rndnr(sel) = sin(2*pi*rand(1,length(sel)));
end
rndnr = sigma * rndnr;
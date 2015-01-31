function girder = lnls_girder_amp_factors(res)

the_ring = res.the_ring;
twi = calctwiss(the_ring);
mis_err = res.mis_err;

mia = findcells(the_ring,'FamName','mia');
mib = findcells(the_ring,'FamName','mib');
mc  = findcells(the_ring,'FamName','mc');
indcs = 1:mia(2);
indcs = findcells(the_ring(indcs),'Girder');
[girders,in,~] = unique(getcellstruct(the_ring,'Girder',indcs));
[~,in2,~] = unique(getcellstruct(the_ring,'Girder',indcs),'first');
in = ceil((in+in2)/2);

for pla = {'x','y'}
    pl = pla{1};
    misalign = str2func(['lnls_set_misalignment' upper(pl)]);
    mis = ['mis' pl];
    girder.before.(mis).orb = zeros(8,length(girders));%1,2=all 3,4=mia 5,6=mib 7,8=mc
    girder.before.(mis).opt = zeros(3,length(girders));
    for ong = {'bpm_on','bpm_off'}
        on = ong{1};
        girder.(on).slow.(mis).orb = zeros(2,length(girders));
        girder.(on).slow.(mis).opt = zeros(3,length(girders));
        girder.(on).slow.(mis).cor = zeros(2,length(girders));
        girder.(on).fast.(mis).orb = zeros(6,length(girders));%1,2=mia 3,4=mib 5,6=mc
        girder.(on).fast.(mis).opt = zeros(3,length(girders));
        girder.(on).fast.(mis).cor = zeros(2,length(girders));
    end
    for i = 1:length(girders)
        %apply alignment errors
        gir = girders{i};
        fprintf([gir ', ']);
        ind = findcells(the_ring,'Girder',gir);
        err = repmat(mis_err,1,length(ind));
        the_ring_err = misalign(err,ind,the_ring);
        
        % get values before correction
        boba = findorbit4(the_ring_err,0,1:length(the_ring));
        girder.before.(mis).orb([1,2],i) = sqrt(lnls_meansqr(boba([1 3],:),2))/mis_err;
        girder.before.(mis).orb([3,4],i) = sqrt(lnls_meansqr(boba([1 3],mia),2))/mis_err;
        girder.before.(mis).orb([5,6],i) = sqrt(lnls_meansqr(boba([1 3],mib),2))/mis_err;
        girder.before.(mis).orb([7,8],i) = sqrt(lnls_meansqr(boba([1 3],mc),2))/mis_err;
        twi_err = calctwiss(the_ring_err);
        girder.before.(mis).opt([1,2],i) = sqrt(lnls_meansqr([(twi.betax-twi_err.betax)./twi.betax,...
                                         (twi.betay-twi_err.betay)./twi.betay]))'/mis_err;
        girder.before.(mis).opt(3,i) = lnls_calc_emittance_coupling(the_ring_err,1e-3);
        
        % perform slow and fast correction
        ibpm = findcells(the_ring(ind),'FamName','bpm');
        for ong = {'bpm_on','bpm_off'}
            on = ong{1};
            for mod = {'slow','fast'}
                mo = mod{1};
                par = res.params.(mo);
                goal_codx = zeros(size(par.bpm_idx));
                goal_cody = zeros(size(par.bpm_idx));
                ref = zeros(4,length(the_ring));
                if strcmp(pl,'x'), ref(1,ind) = mis_err; else ref(3,ind) = mis_err; end
                if strcmp(on, 'bpm_on') && ~isempty(ibpm)
                    if strcmp(pl,'x')
                        for ii = ibpm, goal_codx(par.bpm_idx == ind(ii)) = mis_err; end
                    else
                        for ii = ibpm, goal_cody(par.bpm_idx == ind(ii)) = mis_err; end
                    end
                end
                [the_ring_corr, hkicks, vkicks] = correct_orbit(the_ring_err,par,goal_codx,goal_cody);
                if strcmp(mo,'slow')
                    boba = sqrt(lnls_meansqr(findorbit4(the_ring_corr,0,1:length(the_ring))-ref,2))/mis_err;
                    girder.(on).(mo).(mis).orb(:,i) = boba([1 3]);
                    twi_err = calctwiss(the_ring_corr);
                    girder.(on).(mo).(mis).opt([1,2],i) = sqrt(lnls_meansqr([(twi.betax-twi_err.betax)./twi.betax,...
                        (twi.betay-twi_err.betay)./twi.betay]))'/mis_err;
                else
                    boba = findorbit4(the_ring_corr,0,1:length(the_ring));
                    girder.(on).(mo).(mis).orb([1,2],i) = sqrt(lnls_meansqr(boba([1,3],mia),2))/mis_err;
                    girder.(on).(mo).(mis).orb([3,4],i) = sqrt(lnls_meansqr(boba([1,3],mib),2))/mis_err;
                    girder.(on).(mo).(mis).orb([5,6],i) = sqrt(lnls_meansqr(boba([1,3],mc),2))/mis_err;
                    mi = sort([mia mib mc]);
                    twi_err = calctwiss(the_ring_corr,mi);
                    girder.(on).(mo).(mis).opt([1,2],i) = sqrt(lnls_meansqr([(twi.betax(mi)-twi_err.betax)./twi.betax(mi),...
                        (twi.betay(mi)-twi_err.betay)./twi.betay(mi)]))'/mis_err;
                end
                girder.(on).(mo).(mis).opt(3,i) = lnls_calc_emittance_coupling(the_ring_corr,1e-3);
                girder.(on).(mo).(mis).cor(:,i) =  [sqrt(lnls_meansqr(hkicks)); sqrt(lnls_meansqr(vkicks))]/mis_err;
            end
        end
    end
    fprintf('\n');
    [girder.indcs,I] = sort(indcs(in));
    girder.pos = twi.pos(girder.indcs);
    girder.before.(mis).orb = girder.before.(mis).orb(:,I);
    girder.before.(mis).opt = girder.before.(mis).opt(:,I);
    for ong = {'bpm_on','bpm_off'}
        on = ong{1};
        for mod = {'slow','fast'}
            mo = mod{1};
            girder.(on).(mo).(mis).orb = girder.(on).(mo).(mis).orb(:,I);
            girder.(on).(mo).(mis).opt = girder.(on).(mo).(mis).opt(:,I);
            girder.(on).(mo).(mis).cor = girder.(on).(mo).(mis).cor(:,I);
        end
    end
end
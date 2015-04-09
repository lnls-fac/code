function [ave_bun, rms_bun, ave_kickx, fdbkx] = single_bunch_tracking(ring, bunch, wake)

ave_bun   = zeros(4,ring.nturns);
rms_bun   = zeros(4,ring.nturns);
ave_kickx = zeros(1,ring.nturns);
fdbkx     = zeros(1,ring.nturns);

RandStream.setGlobalStream(RandStream('mt19937ar','seed', 190488));
%definicao dos pacotes
%generate the longitudinal phase space;
cutoff = 9;
[tau, espread] = generate_longitudinal_bunch(bunch, ring, wake);

if abs(bunch.espread-espread)/bunch.espread > eps
    fprintf('Microwave Intability regime: energy spread = %7.4g\n',espread);
end

en  = lnls_generate_random_numbers(espread, bunch.num_part, 'norm', cutoff, 0);

betx = ring.beta;
alpx = ring.alpha;
etax = ring.eta;
etxp = ring.etap;
tune = ring.tune;
chrom= ring.dtunedp;
tu_sh= ring.dtunedj;

% generate transverse phase space;
emitx = lnls_generate_random_numbers(bunch.emit, bunch.num_part,'exponential',cutoff^2,0);
phasx = 2*pi*rand(1, bunch.num_part);
x  =  sqrt(emitx*betx).*cos(phasx)                     + etax*en;
xp = -sqrt(emitx/betx).*(alpx*cos(phasx) + sin(phasx)) + etxp*en;


ind = abs(tau) < 3e-11 & abs(en) < 7.6e-4;
figure;
ax = axes;
plot(ax,tau(ind),en(ind),'b.', 'MarkerSize',1);hold(ax,'on');
plot(ax,tau(~ind),en(~ind),'b.', 'MarkerSize',1);
hold(ax,'off'); drawnow;
for ii=1:ring.nturns;
    % First do single particle tracking:
    % define one phase advance per particle
    phi  =  2*pi*(tune + chrom*en + tu_sh*((x-etax*en).^2/betx + ...
                 ((xp-etxp*en).^2 + alpx/betx*(x-etax*en).^2)*betx));
    
    [x, xp] = transverse_tracking(x,xp,en,phi,betx,alpx,etax,etxp);
    % The longitudinal time evolution equations are not in the differential
    % form. Thus, any longitudinal potential can be taken into account.
    % I don't have to normalize the potential by the charge, because the
    % energy is already in electronVolts
    en  = en  + interp1(bunch.tau, bunch.potential, tau)/ring.E;
    % Remember, positive tau means particle ahead of synchronous particle.
    tau = tau - ring.rev_time.*(en*ring.mom_comp);
    
    
    % Now comes the impedance kicks:
    [kickt, kickx] = kick_from_wake(x, tau, wake);
    kickt  = kickt * (ring.rev_time  / ring.E) * (bunch.I_b / bunch.num_part);
    kickx  = kickx * (ring.rev_time  / ring.E) * (bunch.I_b / bunch.num_part);
    
    ave_kickx(ii) = mean(kickx);
   
    % Now we try to simulate a bunch by bunch feedback system acting on the
    % bunch centroid:
    fdbkx(ii) = bbb_feedback(ave_bun(1,:),wake,ii);
    
    % The impedance kick must be divided by beta, because the betatron
    % function were already taken into account in the wake field definition
    xp = xp + kickx/betx + fdbkx(ii);
    en = en + kickt;
    
    % At last the first and second moments of the beam are recorded:
    ave_bun(:,ii) = mean([x;xp;en;tau],2);
    rms_bun(:,ii) =  std([x;xp;en;tau],0,2);
    
    
    if mod(ii,1000)==0
        fprintf('%d\n',ii);
    end
    if mod(ii,10)==0
        curx = get(ax,'XLim');
        cury = get(ax,'YLim');
        nextx = [min([tau,curx(1)]), max([tau,curx(2)])];
        nexty = [min([en,  cury(1)]), max([en,  cury(2)])];
        plot(ax,tau(ind),en(ind),'b.', 'MarkerSize',1); hold on;
        plot(ax,tau(~ind),en(~ind),'b.', 'MarkerSize',1);
        hold(ax,'off');
        xlim(nextx);
        ylim(nexty);
        drawnow;
    end
end

function [x_new, xp_new] = transverse_tracking(x,xp,en,phix,betx,alpx,etax,etxp)

% The transverse single particle kick is just an one turn matrix at some
% position in the ring, with a tune dependent of particle energy and
% transverse action:
x_new  =         (x-etax*en).*cos(phix) + betx*(xp-etxp*en).*sin(phix) + etax*en;
xp_new = -1/betx*(x-etax*en).*sin(phix) +      (xp-etxp*en).*cos(phix) + etxp*en;


function [kickt, kickx] = kick_from_wake(x, tau, wake)

kickx  = zeros(size(x));
kickt = zeros(size(tau));
% Remember that tau is the position ahead of the synchronous particle.
% Thus, a positive tau passes through the impedance before a negative tau.

if wake.dipo.sim && isfield(wake.dipo,'wake')
    difft = bsxfun(@minus,tau,tau');
    kik = interp1(wake.dipo.tau,wake.dipo.wake,difft,'linear',0);
    kickx = kickx - (x*kik);
end
if wake.dipo.sim && isfield(wake.dipo,'wr')
    wr = wake.dipo.wr;
    Rs = wake.dipo.Rs;
    Q  = wake.dipo.Q;
    betax = wake.dipo.beta;
    Ql = sqrt(Q.^2 - 1/4);
    wrl = wr .* Ql ./ Q;
    
    [sortedTau, I] = sort(tau,'descend');
    W_pot = zeros(size(wr));
    for i=1:length(sortedTau),
        for ii=1:length(wr)
            kickx(I(i)) = kickx(I(i)) - betax(ii)*wr(ii)*Rs(ii)/Ql(ii)*...
                   imag(W_pot(ii) * exp( sortedTau(i)*(1i*wrl(ii)+wr(ii)/(2*Q(ii)))));
            W_pot(ii) = W_pot(ii) + exp(-sortedTau(i)*(1i*wrl(ii)+wr(ii)/(2*Q(ii))))*x(I(i));
        end
    end
end


if  wake.quad.sim && isfield(wake.quad,'wake')
    if ~exist('difft','var'), difft = bsxfun(@minus,tau,tau'); end
    kik = interp1(wake.quad.tau,wake.quad.wake,difft,'linear',0);
    kickx = kickx - (sum(kik).*x);
end
if wake.quad.sim && isfield(wake.quad,'wr')
    wr = wake.quad.wr;
    Rs = wake.quad.Rs;
    Q  = wake.quad.Q;
    betax = wake.quad.beta;
    
    Ql = sqrt(Q.^2 - 1/4);
    wrl = wr .* Ql ./ Q;
    
    if ~exist('sortedTau','var'), [sortedTau, I] = sort(tau,'descend');end
    W_pot = zeros(size(wr));
    for i=1:length(sortedTau),
        for ii=1:length(wr)
            kickx(I(i)) = kickx(I(i)) - x(I(i)) * betax(ii)*wr(ii)*Rs(ii)/Ql(ii)*...
                   imag(W_pot(ii) * exp( sortedTau(i)*(1i*wrl(ii)+wr(ii)/(2*Q(ii)))));
            W_pot(ii) = W_pot(ii) + exp(-sortedTau(i)*(1i*wrl(ii)+wr(ii)/(2*Q(ii))));
        end
    end
end


if wake.long.sim && isfield(wake.long,'wake')
    if ~exist('difft','var'), difft = bsxfun(@minus,tau,tau'); end
    kik = interp1(wake.long.tau,wake.long.wake,difft,'linear',0);
    kickt = kickt - sum(kik);
end
if wake.long.sim && isfield(wake.long,'wr')
    wr = wake.long.wr;
    Rs = wake.long.Rs;
    Q  = wake.long.Q;
    
    Ql = sqrt(Q.^2 - 1/4);
    wrl = wr .* Ql ./ Q;
    
    if ~exist('sortedTau','var'), [sortedTau, I] = sort(tau,'descend'); end
    W_pot = zeros(size(wr));
    for i=1:length(sortedTau),
        for ii=1:length(wr)
            kickt(I(i)) = kickt(I(i)) - wr(ii)*Rs(ii)/Q(ii)*(1/2 + ...
                   real(W_pot(ii) * exp( sortedTau(i)*(1i*wrl(ii)+wr(ii)/(2*Q(ii))))) + ... 
          1/(2*Ql)*imag(W_pot(ii) * exp( sortedTau(i)*(1i*wrl(ii)+wr(ii)/(2*Q(ii))))));
            W_pot(ii) = W_pot(ii) + exp(-sortedTau(i)*(1i*wrl(ii)+wr(ii)/(2*Q(ii))));
        end
    end
end


function kick = bbb_feedback(x_m,wake,ii)

kick = 0;
if ii<wake.feedback.npoints || ~wake.feedback.sim, return; end

npoints = wake.feedback.npoints;
phase   = wake.feedback.phase;
freq    = wake.feedback.freq;
gain    = wake.feedback.gain;

samp  = 1:npoints;
fil = cos(2*pi*freq*samp + phase).*sin(2*pi*samp/(2*npoints))./(samp*pi);
kick = gain*(x_m((ii-npoints+1):ii)*fil');



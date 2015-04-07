function [ave_bun, rms_bun, ave_kickx, fdbkx] = single_bunch_tracking(ring, bunch, wake)

ave_bun   = zeros(4,ring.nturns);
rms_bun   = zeros(4,ring.nturns);
ave_kickx = zeros(1,ring.nturns);
fdbkx     = zeros(1,ring.nturns);

RandStream.setGlobalStream(RandStream('mt19937ar','seed', 190488));
%definicao dos pacotes
%generate the longitudinal phase space;
cutoff = 9;
en  = lnls_generate_random_numbers(bunch.espread, bunch.num_part, 'norm', cutoff, 0);

tau = bunch.tau;
pot = bunch.potential;
ipot = zeros(size(pot));
idist = zeros(size(pot));
ipot(1) = 0;for i=2:length(pot),ipot(i) = ipot(i-1) + (pot(i)+pot(i-1))/2*(tau(i)-tau(i-1));end
ind = tau <= 0;
ipot = ipot - ipot(sum(ind));
dist = exp(1/(ring.mom_comp*ring.rev_time*ring.E)*(ipot/(2*bunch.espread^2)));
idist(1) = 0;for i=2:length(dist),idist(i) = idist(i-1) + (dist(i)+dist(i-1))/2*(tau(i)-tau(i-1));end
idist = idist/idist(end);
ind = idist==max(idist) | idist==min(idist);

tau = interp1(idist(~ind),tau(~ind),rand(1,bunch.num_part));

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

figure;
ax = axes;
plot(ax,tau,x,'.');
for ii=1:ring.nturns;
    phi  =  2*pi*(tune + chrom*en + tu_sh*((x-etax*en).^2/betx + ...
                 ((xp-etxp*en).^2 + alpx/betx*(x-etax*en).^2)*betx));
    
    [x, xp] = transverse_tracking(x,xp,en,phi,betx,alpx,etax,etxp);
    en  = en  - interp1(bunch.tau, bunch.potential, tau)/ring.E;
    tau = tau - ring.rev_time.*(en*ring.mom_comp);
    
    kickx = kickx_from_wake(x, tau, wake, ii, ring.E, bunch.I_b, ring.rev_time);
    ave_kickx(ii) = mean(kickx);
    kickt = kickt_from_wake(tau, wake, ii, ring.E, bunch.I_b, ring.rev_time);
    fdbkx(ii) = bbb_feedback(ave_bun(1,:),wake,ii,kickx)/betx;
    xp = xp + kickx/betx + fdbkx(ii);
    en = en + kickt;
    ave_bun(:,ii) = mean([x;xp;en;tau],2);
    rms_bun(:,ii) =  std([x;xp;en;tau],0,2);
    if mod(ii,100)==0
        fprintf('%d\n',ii);
    end
    if mod(ii,10)==0
        curx = get(ax,'XLim');
        cury = get(ax,'YLim');
        nextx = [min([tau,curx(1)]), max([tau,curx(2)])];
        nexty = [min([x,  cury(1)]), max([x,  cury(2)])];
        plot(ax,tau,x,'.');
        xlim(nextx);
        ylim(nexty);
        drawnow;
    end
end


function [x_new, xp_new] = transverse_tracking(x,xp,en,phix,betx,alpx,etax,etxp)

x_new  =         (x-etax*en).*cos(phix) + betx*(xp-etxp*en).*sin(phix) + etax*en;
xp_new = -1/betx*(x-etax*en).*sin(phix) +      (xp-etxp*en).*cos(phix) + etxp*en;


function kick = kickx_from_wake(x, tau, wake, volta, E, I_b, T0)

kick = zeros(size(x));
np   = length(tau);

difft = bsxfun(@minus,tau',tau);
if wake.sing.dipo.sim
    %     kik = interp1(wake.sing.dipo.tau,wake.sing.dipo.wake,difft,'linear',0);
    %     kick = kick + T0*I_b/E/np*(x*kik);
    Zovern = 0.2;
    radius = 12e-3;
    fr  = 2.4* c/(radius*2*pi);
    Rs = Zovern*fr*ring.rev_time;
    Q = 1;
    wr = fr*2*pi;
    Ql = sqrt(Q^2 - 1/4);
    wrl = wr * Ql / Q;
    for i=1:length(tau),
        
        beta_imp*wr*Rs/Ql*sin(wrl*tau).*exp(-wr*tau/(2*Q));
    end
end
if wake.sing.quad.sim
    kik = interp1(wake.sing.quad.tau,wake.sing.quad.wake,difft,'linear',0);
    kick = kick + T0*I_b/E/np*(sum(kik).*x);
end
if wake.mult.trans.sim
    kick = kick + wake.mult.trans.wake(volta);
end

function kick = bbb_feedback(x_m,wake,ii,kickx)

kick = 0;
if ii<wake.sing.feedback.npoints || ~wake.sing.feedback.sim, return; end

npoints = wake.sing.feedback.npoints;
phase   = wake.sing.feedback.phase;
freq    = wake.sing.feedback.freq;
gain    = wake.sing.feedback.gain;

samp  = 1:npoints;
fil = cos(2*pi*freq*samp + phase).*sin(2*pi*samp/(2*npoints))./(samp*pi);
kick = gain*(x_m((ii-npoints+1):ii)*fil');


% if wake.sing.feedback.sim
%     kick = -repmat(mean(kickx),size(x));
% end

function kick = kickt_from_wake(tau, wake, volta, E, I_b, T0)

kick = zeros(size(tau));
np   = length(tau);

if wake.sing.long.sim
    difft = bsxfun(@minus,tau',tau);
    kik = interp1(wake.sing.long.tau,wake.sing.long.wake,difft,'linear',0);
    kick = kick + T0*I_b/E/np*sum(kik);
end
if wake.mult.long.sim
    kick = kick + wake.mult.long.wake(volta);
end
const = lnls_constants;
c = const.c;
el_ch = const.q0;
% ring data
ring.nturns   = 10000;
ring.rev_time = 518.396/c;
ring.E        = 3e9;
ring.mom_comp = 1.7e-4;
ring.beta     = 11;
ring.alpha    = 0;
ring.eta      = 0.0;
ring.etap     = 0;
ring.har_num  = 864;
ring.tune     = 13.117;
ring.dtunedp  = 0.0;
ring.dtunedj  = 000000;

bunch.num_part = 800;
bunch.I_b      = 2.7e-3;

tau = (-1000:1000)*1e-12;
V = 3.0e6;
wrf = 2*pi*ring.har_num/ring.rev_time;
phi0 = 171.24/180*pi;
Vl = 1.0e6*1;
wl = wrf*3;
phil = 0.30/180*pi;
bunch.potential= V*(sin(wrf*tau-phi0)+sin(phi0)) + Vl*(sin(wl*tau-phil)+sin(phil));
bunch.tau      = tau;
bunch.espread  = 7.64e-4;
bunch.emit     = 271e-12;

% Resistive Wall Impedance
% b = 12e-3;
% sigma = 5.9e7;
% Z0 = c*4*pi*1e-7;
% a = 3/sqrt(2*pi)/4;
% p = 2.7;
% s0 = (2*b^2/Z0/sigma)^(1/3);
% L = 4800;
% W0 = c*Z0/4/pi * 2*s0*L/b^4;
%     kik = beta_imp*W0*(8/3*exp(-difft*c/s0).*sin(difft*c*sqrt(3)/s0-pi/6) ...
%     + 1/sqrt(2*pi)*1./(a^p + (difft*c/(4*s0)).^p).^(1/p));
Zovern = 0.2;
radius = 12e-3;
fr  = 2.4* c/(radius*2*pi); 
Rs = Zovern*fr*ring.rev_time;
Q = 1;
wr = fr*2*pi;


tau = (0:1000)*1e-12;
clear wake;
wake.long.sim  = true;
% wake.long.tau  = tau;
% wake.long.wake = wr*Rs/Q*(cos(wrl*tau) - 1/(2*Ql)*sin(wrl*tau)).*exp(-wr*tau/(2*Q));
wake.long.wr   = wr;
wake.long.Rs   = Rs;
wake.long.Q    = Q;

beta_imp = 11;
Rs = Zovern*fr*ring.rev_time/radius;

wake.dipo.sim  = false;
% wake.dipo.tau  = tau;
% wake.dipo.wake = beta_imp*wr*Rs/Ql*sin(wrl*tau).*exp(-wr*tau/(2*Q));
wake.dipo.wr   = wr;
wake.dipo.Rs   = Rs;
wake.dipo.Q    = Q;
wake.dipo.beta = beta_imp;


Rs = -Rs/2;
wake.quad.sim  = false;
% wake.quad.tau  = tau;
% wake.quad.wake = beta_imp*wr*Rs/Ql*sin(wrl*tau).*exp(-wr*tau/(2*Q));
wake.quad.wr   = wr;
wake.quad.Rs   = Rs;
wake.quad.Q    = Q;
wake.quad.beta = beta_imp;


wake.feedback.sim = false;
wake.feedback.npoints = 8;
wake.feedback.freq   = 0.11;
wake.feedback.phase  = 3/4*pi;
wake.feedback.gain   = 1;

[ave_bun,rms_bun, ave_kickx, fdbkx] = single_bunch_tracking(ring, bunch, wake);
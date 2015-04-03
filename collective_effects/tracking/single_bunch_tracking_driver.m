% ring data
ring.nturns   = 1000;
ring.rev_per  = 518.396/c;
ring.E        = 3e9;
ring.mom_comp = 1.7e-4;
ring.beta     = 11;
ring.disp     = 0;
ring.har_num  = 864;
ring.tune     = 13.117;
ring.dtunedp  = 0.0;
ring.dtunedj  = 0.0;

bunch.num_part = 200;
bunch.I_b      = 1.5e-3;
bunch.syn_tune = 4.36e-3;
bunch.shape    = 'gauss';
bunch.espread  = 2e-4;

wake.sing.dipo.sim  = true;
wake.sing.dipo.Rs   = 2;
wake.sing.dipo.wr   = 3;
wake.sing.dipo.Q    = 1;
wake.sing.quad.sim  = true;
wake.sing.quad.Rs   = 2;
wake.sing.quad.wr   = 3;
wake.sing.quad.Q    = 1;
wake.sing.long.sim  = true;
wake.sing.long.Rs   = 2;
wake.sing.long.wr   = 3;
wake.sing.long.Q    = 1;

wake.mult.trans.sim  = true;
wake.mult.trans.wake = zeros(1,nturns);
wake.mult.long.sim   = true;
wake.mult.long.wake  = zeros(1,nturns);

[ave_bun,rms_bun] = sigle_bunch_tracking(ring, bunch, wake);
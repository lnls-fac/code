function [M, corr_steps] = farespmsin(fadata, freqs, npts_discard)

bpmdata = detrend(double(fadata.bpm_readings(npts_discard+1:end,:)),0);
corrdata = detrend(double(fadata.corr_setpoints(npts_discard+1:end,:)),0);
Ts = fadata.period*1e-6;
npts_total = size(bpmdata,1);
npts = npts_total - npts_discard;

window = flattopwin(npts);
Abpm = fourierseries(bpmdata.*repmat(window,1,size(bpmdata,2)), 1/Ts);
Acorr = fourierseries(corrdata.*repmat(window,1,size(corrdata,2)), 1/Ts);
PG = sum(window)/npts;

idx = round(npts*freqs+1);
M = (Acorr(idx,:)\Abpm(idx,:))';
corr_steps = diag(Acorr(idx,:))/PG;
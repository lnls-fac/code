% global THERING;
% 
% dips = findcells(THERING,'FamName','B');
% HALF_DIP = THERING(dips(2));
% rin = zeros(6,80);
% rin(1,:)=linspace(-10,10,80)*1e-3;
% rout = linepass(HALF_DIP,rin);
% plot(rin(1,:),rout(2,:))
% polyfit(rin(1,:),rout(2,:),2)

%% multipolos
% n = repmat([1 2 3 4 5 6],100,1);
% %x = repmat(linspace(-10,10,100)'*1e-3,1,6);
% x = repmat(linspace(-17.5,17.5,100)'*1e-3,1,6);
% pol = pot*((x/17.5e-3).^n)';
% plot(x(:,1),pol*7.5/180*pi);
% 
% name = 'modelo4_fewsegments.mat';
% name = 'modelo4_segmentado.mat';
% name = 'modelo4.mat';
name = 'modelo4_4segments.mat';
at_model = load(['/home/fac_files/data/sirius_mml/magnet_modelling/CONFIGS/BOOSTER_B_MODELO2/' name]);
at_model = at_model.r.at_model;
comp_atmod = findspos(at_model, length(at_model)+1);

the_ring = sirius_booster_lattice();
atsummary(the_ring);
idx_dip = findcells(the_ring,'FamName','B');
n_dip = length(idx_dip);
comp_dip = the_ring{idx_dip(1)}.Length/2;

diff = comp_atmod - comp_dip;
for ii=1:n_dip
    comp_dr = getcellstruct(the_ring,'Length',idx_dip(1)+[-2 2]);
    comp_dr_new = comp_dr-diff;
    if any(comp_dr_new) < 0, error('comprimento negativo'); end;
    dr_menos = drift('dr_menos', comp_dr_new(1), 'DriftPass');
    dr_mais  = drift('dr_mais', comp_dr_new(2), 'DriftPass');
    drifts = buildlat([dr_menos dr_mais]);
    the_ring = [the_ring(1:idx_dip(1)-3) drifts(1) fliplr(at_model) ...
                at_model drifts(2) the_ring(idx_dip(1)+3:end)];
    idx_dip = findcells(the_ring,'FamName','B');
end
atsummary(the_ring);
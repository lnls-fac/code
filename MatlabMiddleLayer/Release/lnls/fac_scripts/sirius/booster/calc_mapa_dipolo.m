bend_pass_method = 'BndMPoleSymplectic4Pass';

B_length = 1.1520/2;
B_angle  = 360 / 50/2;
B_gap    = 0.028;
B_fint1  = 0.0;
B_fint2  = 0.0;
B_edge   = (B_angle)*(pi/180)*1;

B_strength = -0.2037;
B_sext     = -2.2685; 


HALF_DIP = rbend_sirius('B', B_length, B_angle*(pi/180), 0, B_edge, ...
    B_gap, B_fint1, B_fint2, [0 0 0 0], [0, B_strength, B_sext, 0], bend_pass_method);
HALF_DIP = buildlat(HALF_DIP);

rin = zeros(6,80);
rin(1,:)=linspace(-10,10,80)*1e-3;
rout = linepass(HALF_DIP,rin);
plot(rin(1,:),rout(2,:))
polyfit(rin(1,:),rout(2,:),4)

%% multipolos
% n = repmat([1 2 3 4 5 6],100,1);
% %x = repmat(linspace(-10,10,100)'*1e-3,1,6);
% x = repmat(linspace(-17.5,17.5,100)'*1e-3,1,6);
% pol = pot*((x/17.5e-3).^n)';
% plot(x(:,1),pol*7.5/180*pi);
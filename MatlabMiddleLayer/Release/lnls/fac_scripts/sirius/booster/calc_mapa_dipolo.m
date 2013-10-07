global THERING;

dips = findcells(THERING,'FamName','B');
HALF_DIP = THERING(dips(2));
rin = zeros(6,80);
rin(1,:)=linspace(-10,10,80)*1e-3;
rout = linepass(HALF_DIP,rin);
plot(rin(1,:),rout(2,:))
polyfit(rin(1,:),rout(2,:),2)

%% multipolos
% n = repmat([1 2 3 4 5 6],100,1);
% %x = repmat(linspace(-10,10,100)'*1e-3,1,6);
% x = repmat(linspace(-17.5,17.5,100)'*1e-3,1,6);
% pol = pot*((x/17.5e-3).^n)';
% plot(x(:,1),pol*7.5/180*pi);
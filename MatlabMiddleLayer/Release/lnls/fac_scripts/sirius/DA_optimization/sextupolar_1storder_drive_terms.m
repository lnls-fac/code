function [geom chrom] = sextupolar_1storder_drive_terms(beta,eta,mu,SPos,plota)

betax = beta(:,1);
etax  = eta(:,1);
betay = beta(:,2);

geom(:,1) = (1/24)*betax.^(3/2).*(exp(1i*mu*[1 0]')); %h21000
geom(:,2) = (1/24)*betax.^(3/2).*(exp(1i*mu*[3 0]')); %h30000
geom(:,3) = -(1/4)*betax.^(1/2).*betay.*(exp(1i*mu*[1 0]')); %h10110
geom(:,4) = -(1/8)*betax.^(1/2).*betay.*(exp(1i*mu*[1 2]')); %h10200
geom(:,5) = -(1/8)*betax.^(1/2).*betay.*(exp(1i*mu*[1 -2]')); %h10020

geom(:,6) = conj(geom(:,1)); %h12000
geom(:,7) = conj(geom(:,2)); %h03000
geom(:,8) = conj(geom(:,3)); %h01110
geom(:,9) = conj(geom(:,4)); %h01020
geom(:,10) = conj(geom(:,5)); %h01200


chrom(:,1) = (1/2)*betax.*etax; %h11001
chrom(:,2) =-(1/2)*betay.*etax; %h00111
chrom(:,3) = (1/2)*betax.^(1/2).*etax.^2.*(exp(1i*mu*[1 0]')); %h10002
chrom(:,4) = (1/4)*betax.*etax.*(exp(1i*mu*[2 0]')); %h20001
chrom(:,5) = -(1/4)*etax.*betay.*(exp(1i*mu*[0 2]')); %h00201

chrom(:,6) = conj(chrom(:,3)); %h01002
chrom(:,7) = conj(chrom(:,4)); %h02001
chrom(:,8) = conj(chrom(:,5)); %h00021

if plota
    figure
    subplot(4,1,1);
    plot(SPos,2*real(chrom(:,1:2)));
    xlim([0 SPos(end)]);
    grid on
    
    subplot(4,1,2);
    plot(SPos,2*real(geom(:,1:5)));
    xlim([0 SPos(end)]);
    grid on
    legend('h21000','h30000','h10110','h10200','h10020');
    
    
    subplot(4,1,3);
    plot(SPos,2*real(chrom(:,3:5)));
    xlim([0 SPos(end)]);
    grid on
    legend('h10002','h20001','h00201');
    
    subplot(4,1,4);
    drawlattice(0, 1, gca, SPos(end));
    xlabel('Position [m]');
    % axis off;
    grid on
end

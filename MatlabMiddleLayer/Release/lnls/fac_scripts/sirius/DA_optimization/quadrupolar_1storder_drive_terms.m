function chrom = quadrupolar_1storder_drive_terms(beta,eta,mu,SPos)

betax = beta(:,1);
etax  = eta(:,1);
betay = beta(:,2);

chrom(:,1) = -(1/4)*betax; %h11001
chrom(:,2) =  (1/4)*betay; %h00111
chrom(:,3) = -(1/2)*betax.^(1/2).*etax.*(exp(1i*mu*[2 0]')); %h10002
chrom(:,4) = -(1/8)*betax.*(exp(1i*mu*[4 0]')); %h20001
chrom(:,5) = (1/8)*betay.*(exp(1i*mu*[0 4]')); %h00201

chrom(:,6) = conj(chrom(:,3)); %h01002
chrom(:,7) = conj(chrom(:,4)); %h02001
chrom(:,8) = conj(chrom(:,5)); %h00021
[ltba, tit, Twiss0] = ltba_lattice;

um = 1e-6;
mm = 1e-3;
mrad = 1e-3;
pc = 1e-2;

% Errors
rms_alix = 0.3 * mm;
rms_aliy = 0.3 * mm;
rms_ex   = 0.1 * pc;
rms_x0   = 0.1 * mm;
rms_xp0  = 0.1 * mrad;
rms_y0   = 0.1 * mm;
rms_yp0  = 0.1 * mrad;
n_maquinas = 100;


t=twissline(ltba,0,Twiss0,1:length(ltba)+1,'chrom',0);
 
beta=cat(1,t.beta);
s=cat(1,t.SPos);
%d=cat(1,t.Dispersion);
%plot(s,beta(:,1),'b',s,beta(:,2),'r',s,d(:,1),'g');
plot(s,beta(:,1),'b',s,beta(:,2),'r');

ind_BPM = findcells(ltba, 'FamName', 'BPM');
ind_ch = findcells(ltba, 'FamName', 'hcm');
ind_cv = findcells(ltba, 'FamName', 'vcm');

sBPM = s(ind_BPM);

nBPM = length(ind_BPM);
nch = length(ind_ch);
ncv = length(ind_cv);

%inicializa matrizes
dteta_ch = zeros(nch,n_maquinas);
dteta_cv = zeros(ncv,n_maquinas);
MH = zeros(nBPM,nch);
MV = zeros(nBPM,ncv);
orbx = zeros(length(ltba)+1,n_maquinas);
orby = orbx;
orbcx = orbx;
orbcy = orbx;
x_BPM = zeros(nBPM,n_maquinas);
y_BPM = x_BPM;
xc_BPM = x_BPM;
yc_BPM = x_BPM;


% Matriz resposta horizontal
for i=1:nch
    for j=1:nBPM
        %sub-linha de corretor a BPM
        if (ind_ch(i) < ind_BPM(j));
            line = ltba(ind_ch(i):ind_BPM(j));
            t1=twissline(line,0,Twiss0,1:length(line));
            M=cat(1,t1.M44);
            MH(j,i)=M(end-3,2);
        end
    end
end

% Matriz resposta vertical
for i=1:ncv
    for j=1:nBPM
        %sublinha de corretor a BPM
        if (ind_cv(i)<ind_BPM(j))
            line = ltba(ind_cv(i):ind_BPM(j));
            t1=twissline(line,0,Twiss0,1:length(line));
            M=cat(1,t1.M44);
            MV(j,i)=M(end-1,4);
        end
    end
end

% Matrizes de corre??o
[UH,SH,VH] = svd(MH);
MCH = -VH*inv(SH)*UH';

[UV,SV,VV] = svd(MV);
MCV = -VV*inv(SV)*UV';

% Erros de alinhamento e excita??o em dipolos e quadrupolos
idx = findcells(ltba,'K');
ltba_Ori = ltba;

% Loop nas m?quinas aleatorias
for nmaq=1:n_maquinas
    ltba = ltba_Ori;
    % Distribui??o uniforme de erros
    errox = (-1+2*rand(1,length(idx))) * rms_alix;
    erroy = (-1+2*rand(1,length(idx))) * rms_aliy;
    erroex = (-1+2*rand(1,length(idx))) * rms_ex;

    ltba = lnls_set_misalignmentX(errox, idx, ltba);
    ltba = lnls_set_misalignmentY(erroy, idx, ltba);
    erroex = lnls_set_excitation(erroex, idx, ltba);
    
%    for i=1:length(idx)
%        erro = [errox(i), 0, erroy(i), 0, 0, 0]; 
%        ltba{idx(i)}.T1 = ltba_Ori{idx(i)}.T1 + erro;
%        ltba{idx(i)}.T2 = ltba_Ori{idx(i)}.T2 - erro;
%    end

% Orbit without correction
    % Error in lauching conditions
    ex0 = (-1+2*rand(1)) * rms_x0;
    exp0 = (-1+2*rand(1)) * rms_xp0;
    ey0 = (-1+2*rand(1)) * rms_y0;
    eyp0 = (-1+2*rand(1)) * rms_yp0;
    Twiss0.ClosedOrbit=[ex0; exp0; ey0; eyp0];
    
    t=twissline(ltba,0,Twiss0,1:length(ltba)+1);
    for i=1:length(t)
        orbx(i,nmaq)=t(i).ClosedOrbit(1);
        orby(i,nmaq)=t(i).ClosedOrbit(3);
    end

% Orbita nos BPMs
    x_BPM(:,nmaq) = orbx(ind_BPM,nmaq);
    y_BPM(:,nmaq) = orby(ind_BPM,nmaq);
    
    xc_BPM(:,nmaq) = x_BPM(:,nmaq);
    yc_BPM(:,nmaq) = y_BPM(:,nmaq);
    
    %Itera
    
    for iter=1:1
% Corre??o
        dteta_ch(:,nmaq) = MCH * xc_BPM(:,nmaq);
        dteta_cv(:,nmaq) = MCV * yc_BPM(:,nmaq);

        for i=1:nch
            tetaori=ltba{ind_ch(i)}.KickAngle(1);
            ltba{ind_ch(i)}.KickAngle = [tetaori+dteta_ch(i,nmaq) 0];
        end

        for i=1:ncv
            tetaori=ltba{ind_cv(i)}.KickAngle(2);
            ltba{ind_cv(i)}.KickAngle = [0 dteta_cv(i,nmaq)+tetaori];
        end

% Orbita corrigida
        t=twissline(ltba,0,Twiss0,1:length(ltba)+1);
        for i=1:length(t)
            orbcx(i,nmaq)=t(i).ClosedOrbit(1);
            orbcy(i,nmaq)=t(i).ClosedOrbit(3);
        end

% Orbita corrigida nos BPMs
        xc_BPM(:,nmaq) = orbcx(ind_BPM,nmaq);
        yc_BPM(:,nmaq) = orbcy(ind_BPM,nmaq);
    end
        
end

for i=1:n_maquinas
    orbx_ptp(i) = max(orbx(:,i)) - min(orbx(:,i));
    orby_ptp(i) = max(orby(:,i)) - min(orby(:,i));
    orbcx_ptp(i) = max(orbcx(:,i)) - min(orbcx(:,i));
    orbcy_ptp(i) = max(orbcy(:,i)) - min(orbcy(:,i));
end

orbx_rms = std(orbx,0,2);
orby_rms = std(orby,0,2);
orbcx_rms = std(orbcx,0,2);
orbcy_rms = std(orbcy,0,2);
x_BPM_rms = std(x_BPM,0,2);
y_BPM_rms = std(y_BPM,0,2);
xc_BPM_rms = std(xc_BPM,0,2);
yc_BPM_rms = std(yc_BPM,0,2);
teta_ch_rms = std(dteta_ch(:));
teta_cv_rms = std(dteta_cv(:));
teta_ch_max = max(abs(dteta_ch(:)));
teta_cv_max = max(abs(dteta_cv(:)));

% Correction summary
% Before correction
Xmax = max(orbx_rms);
Ymax = max(orby_rms);
XBPMmax = max(x_BPM_rms);
YBPMmax = max(y_BPM_rms);
Xptp_mean = mean(orbx_ptp);
Yptp_mean = mean(orby_ptp);
Xptp_max = max(orbx_ptp);
Yptp_max = max(orby_ptp);

%After correction
Xcmax = max(orbcx_rms);
Ycmax = max(orbcy_rms);
XcBPMmax = max(xc_BPM_rms);
YcBPMmax = max(yc_BPM_rms);
Xcptp_mean = mean(orbcx_ptp);
Ycptp_mean = mean(orbcy_ptp);
Xcptp_max = max(orbcx_ptp);
Ycptp_max = max(orbcy_ptp);

fout = fopen('/Users/fac_files/estudo_LTBA/Correction_summary.out', 'w');
fprintf(fout,'Correction_summary\n');
fprintf(fout,['BTS Transfer Line - ' tit '\n']);
fprintf(fout,'Uniform random errors for all dipoles, septa and quadrupoles\n');
fmt = 'X alignment = +-%g mm\n'; fprintf(fout,fmt,rms_alix/mm);
fmt = 'y alignment = +-%g mm\n'; fprintf(fout,fmt,rms_aliy/mm);
fmt = 'relative excitation = +-%g %%\n'; fprintf(fout,fmt,rms_ex/pc);
fmt = 'x launch condition = +-%g mm\n'; fprintf(fout,fmt,rms_x0/mm);
fmt = 'xp launch condition = +-%g mrad\n'; fprintf(fout,fmt,rms_xp0/mrad);
fmt = 'y launch condition = +-%g mm\n'; fprintf(fout,fmt,rms_y0/mm);
fmt = 'yp launch condition = +-%g mrad\n'; fprintf(fout,fmt,rms_yp0/mrad);
fmt = 'number of machines = %i\n\n'; fprintf(fout,fmt,n_maquinas);

fmt = '                          before   after \n'; fprintf(fout,fmt);
fmt = '                          (mm)     (mm)  \n'; fprintf(fout,fmt);
fmt = 'Max. rms H orbit          %5.3f    %5.3f \n'; fprintf(fout,fmt,Xmax/mm,Xcmax/mm);
fmt = 'Max. rms V orbit          %5.3f    %5.3f \n'; fprintf(fout,fmt,Ymax/mm,Ycmax/mm);
fmt = 'Max. rms H orbit @ BPMs   %5.3f    %5.3f \n'; fprintf(fout,fmt,XBPMmax/mm,XcBPMmax/mm);
fmt = 'Max. rms V orbit @ BPMs   %5.3f    %5.3f \n'; fprintf(fout,fmt,YBPMmax/mm,YcBPMmax/mm);
fmt = 'Average H peak-to-peak    %5.3f    %5.3f \n'; fprintf(fout,fmt,Xptp_mean/mm,Xcptp_mean/mm);
fmt = 'Average V peak-to-peak    %5.3f    %5.3f \n'; fprintf(fout,fmt,Yptp_mean/mm,Ycptp_mean/mm);
fmt = 'Max. H peak-to-peak       %5.3f    %5.3f \n'; fprintf(fout,fmt,Xptp_max/mm,Xcptp_max/mm);
fmt = 'Max. V peak-to-peak       %5.3f    %5.3f \n\n'; fprintf(fout,fmt,Yptp_max/mm,Ycptp_max/mm);

fmt = '                          H       V \n'; fprintf(fout,fmt);
fmt = '                        (mrad)  (mrad) \n'; fprintf(fout,fmt);
fmt = 'rms corrector strength  %5.3f   %5.3f  \n'; fprintf(fout,fmt,teta_ch_rms/mrad,teta_cv_rms/mrad);
fmt = 'Max corrector strength  %5.3f   %5.3f  \n\n'; fprintf(fout,fmt,teta_ch_max/mrad,teta_cv_max/mrad);

tetai_ch_rms = std(dteta_ch,0,2);
tetai_cv_rms = std(dteta_cv,0,2);
tetai_ch_max = max(abs(dteta_ch),[],2);
tetai_cv_max = max(abs(dteta_cv),[],2);
fmt = '      rms     max \n'; fprintf(fout,fmt);
fmt = '     (mrad)  (mrad) \n'; fprintf(fout,fmt);
for i=1:nch
    fmt = 'CH%i  %5.3f   %5.3f  \n'; fprintf(fout,fmt,i,tetai_ch_rms(i)/mrad,tetai_ch_max(i)/mrad);
end
for i=1:ncv
    fmt = 'CV%i  %5.3f   %5.3f  \n'; fprintf(fout,fmt,i,tetai_cv_rms(i)/mrad,tetai_cv_max(i)/mrad);
end
    
fclose(fout);


%Create Figure Horizontal correction
figure1 = figure('Color',[1 1 1]);
annotation('textbox', [0.3,0.88,0.1,0.1],...
           'FontSize',14,...
           'FontWeight','bold',...
           'LineStyle','none',...
           'String', ['BTS Tansfer Line - ' tit]);
       
%Plot before correction
%subplot(5,1,[1,2],'FontSize',14);
subplot('position',[0.1 0.59 0.85 0.32],'FontSize',14);
hold all;
for i=1:n_maquinas
    plot(s,1e3*orbx(:,i),'Color',[0.8 0.8 1]);
end
plot(s,1e3*orbx_rms,'b','LineWidth',1.5);
plot(s,-1e3*orbx_rms,'b','LineWidth',1.5);
ylabel('x [mm]', 'FontSize',14);
ylimit=ylim;
xlimit=xlim;
text(1,0.8*ylimit(2),'X before correction', 'FontSize',14);
grid on;
box on;

%Plot lattice
%subplot(5,1,3);
subplot('position',[0.1 0.45 0.85 0.12]);
lnls_drawlattice(ltba, 1, 0, 1, 1);
xlim(xlimit);
axis off;

%Plot after correction
%subplot(5,1,[4,5],'FontSize',14);
subplot('position',[0.1 0.12 0.85 0.32],'FontSize',14);
hold all;
for i=1:n_maquinas
    plot(s,1e3*orbcx(:,i),'Color',[0.8 0.8 1]);
end
plot(s,1e3*orbcx_rms,'b','LineWidth',1.5);
plot(s,-1e3*orbcx_rms,'b','LineWidth',1.5);
xlabel('s [m]', 'FontSize',14);
ylabel('x [mm]', 'FontSize',14);
ylim(ylimit);
text(1,0.8*ylimit(2),'X after correction', 'FontSize',14);
grid on;
box on;


%Create Figure Vertical correction
figure2 = figure('Color',[1 1 1]);
annotation('textbox', [0.3,0.88,0.1,0.1],...
           'FontSize',14,...
           'FontWeight','bold',...
           'LineStyle','none',...
           'String', ['BTS Tansfer Line - ' tit]);

%Plot before correction
%subplot(5,1,[1,2],'FontSize',14);
subplot('position',[0.1 0.59 0.85 0.32],'FontSize',14);
hold all;
for i=1:n_maquinas
    plot(s,1e3*orby(:,i),'Color',[1 0.8 0.8]);
end
plot(s,1e3*orby_rms,'r','LineWidth',1.5);
plot(s,-1e3*orby_rms,'r','LineWidth',1.5);
ylabel('y [mm]', 'FontSize',14);
ylimit=ylim;
text(1,0.8*ylimit(2),'Y before correction', 'FontSize',14);
grid on;
box on;

%Plot lattice
%subplot(5,1,3);
subplot('position',[0.1 0.45 0.85 0.12]);
lnls_drawlattice(ltba, 1, 0, 1, 1);
xlim(xlimit);
axis off;

%Plot after correction
%subplot(5,1,[4,5],'FontSize',14);
subplot('position',[0.1 0.12 0.85 0.32],'FontSize',14);
hold all;
for i=1:n_maquinas
    plot(s,1e3*orbcy(:,i),'Color',[1 0.8 0.8]);
end
plot(s,1e3*orbcy_rms,'r','LineWidth',1.5);
plot(s,-1e3*orbcy_rms,'r','LineWidth',1.5);
xlabel('s [m]', 'FontSize',14);
ylabel('y [mm]', 'FontSize',14);
ylim(ylimit);
text(1,0.8*ylimit(2),'Y after correction', 'FontSize',14);
grid on;
box on;



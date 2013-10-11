%   [W,Wm,V] = LNLS_TAU_TOUSCHEK_INVERSO(E_n,gamma,N,sigma_E,sigma_s,d_acc,r,Bx,
%   By,alpha,eta,eta_diff,K) calcula o inverso do tempo de vida Touschek W
%   [1/s] a cada ponto, o valor médio Wm [1/s] e o volume do bunch V [m^3].
%
%   As entradas são a emitância natural E_n [m rad], gamma, o número de
%   elétrons por bunch N, a dispersão de energia relativa sigma_E, o
%   comprimento do bunch sigma_s [m], a aceitância em energia d_acc, um
%   vetor de posições r [m] ao longo do qual W é calculado, as funções
%   betatron horizontal e vertical Bx e By [m], alpha = -B'/2 [m], a
%   dispersão e sua derivada eta e eta_diff [m] ao longo de r e o fator de
%   acoplamento K (Ey = K*Ex). Para aceitância nula, negativa ou complexa,
%   o tempo de vida calculado é nulo.

function [W,Wm,V] = lnls_tau_touschek_inverso(E_n,gamma,N,sigma_E,sigma_s,d_acc,r,Bx,By,alpha,eta,eta_diff,K)

% Tabela para interpolar d_touschek
dinttable = getappdata(0, 'TouschekDIntegralTable');
if isempty(dinttable)
    load('lnls_tabela_d_touschek.mat');
    dinttable.x_tabela = x_tabela;
    dinttable.y_tabela = y_tabela;
    setappdata(0, 'TouschekDIntegralTable', dinttable);
else
    x_tabela = dinttable.x_tabela;
    y_tabela = dinttable.y_tabela;
end
    

% Volume do bunch
V = sigma_s * sqrt(By*(K/(1+K))*E_n) .* sqrt(Bx*(1/(1+K))*E_n + eta.^2*sigma_E^2);

if(isreal(d_acc) && d_acc > 0)
    % Tamanho horizontal do bunch
    Sx2 = 1/(1+K) * E_n * Bx;
    
    fator = Bx.*eta_diff + alpha.*eta;
    A1 = 1/(4*sigma_E^2) + (eta.^2 + fator.^2)./(4*Sx2);
    B1 = Bx.*fator./(2*Sx2);
    C1 = Bx.^2./(4*Sx2) - B1.^2./(4*A1);
    
    % Limite de integração inferior
    ksi = (2*sqrt(C1)/gamma * d_acc).^2;
    
    % Interpola d_touschek
    D = interp1(x_tabela,y_tabela,ksi);
    
    % Tempo de vida touschek inverso
    W = 9.4718e-23*N/gamma^2 / d_acc^3 * D ./ V;
    
    % Tempo de vida touschek inverso médio
    Wm = trapz(r,W) / ( r(length(r)) - r(1) );
else
    W = Inf(length(r),1);
    Wm = Inf;
end
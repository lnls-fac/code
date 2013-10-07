function lnls1_meastuneresp
%Mede sintonias do anel.
%
%História: 
%
%2010-09-13: comentários iniciais no código.
%

if ~strcmpi(getmode('BEND'), 'Online'), switch2online; end

lnls1_auto_orb_corr_on;
meastuneresp;

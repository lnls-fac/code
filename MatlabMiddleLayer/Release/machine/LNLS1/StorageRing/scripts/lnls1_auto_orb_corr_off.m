function lnls1_auto_orb_corr_off
%Desliga correção automática de órbita no OPR1
%
%History: 
% 
%2010-09-13: comentários iniciais no código.

if strcmpi(getmode('BEND'), 'online')
    msg.AORBCOR_ON = 0;
    lnls1_comm_write(msg);
else
    fprintf('lnls1_auto_orb_corr_off: simulation mode!\n');
end
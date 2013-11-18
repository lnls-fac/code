% lnls1_booster: carrega estrutura MML do booster do LNLS1

dr = pwd;

% desconecta com servidor se conexao existir
if any(strcmpi(computer, {'PCWIN', 'PCWIN64'}))
    addpath('C:\Arq\MatlabMiddleLayer\Release\mml\');
    cd('C:\Arq\MatlabMiddleLayer\Release\links\lnls_link\lnls1_link\');
    lnls1_comm_disconnect;
    rmpath('C:\Arq\MatlabMiddleLayer\Release\mml\');
else
    addpath('/home/fac_files/code/MatlabMiddleLayer/Release/mml/');
    cd('/home/fac_files/code/MatlabMiddleLayer/Release/links/lnls_link/lnls1_link/');
    lnls1_comm_disconnect;
    rmpath('/home/fac_files/code/MatlabMiddleLayer/Release/mml/');
end


% carrega paths do LNLS1
if any(strcmpi(computer, {'PCWIN', 'PCWIN64'}))
    cd('C:\Arq\MatlabMiddleLayer\Release\mml\');
else
    cd('/home/fac_files/code/MatlabMiddleLayer/Release/mml/');
end

setpathlnls('LNLS1', 'Booster', 'lnls1_link');

% volta ao working dir inicial
cd(dr);
clear dr;

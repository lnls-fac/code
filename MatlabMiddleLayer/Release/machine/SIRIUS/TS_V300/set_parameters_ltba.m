if strcmpi(caso,'default')
    
% forcas baseadas no arquivo LTBA_V300.opa com extracao do booster
% alterada para antes do QF. Utiliza dipolos do booster [2014-09-25]
    
    qa1_strength      = 0.843487;
    qa2_strength      = 1.009714;
    qb1_strength      = -0.328651;
    qb2_strength      = 2.190787;
    qc1_strength      = -1.879466;
    qc2_strength      = 1.805734;
    qc3_strength      = 1.805734;
    qc4_strength      = -1.328187;

%elseif strcmpi(caso,'mismatched_pmm')
    
else
    error('caso nao implementado');
end
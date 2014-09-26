if strcmpi(caso,'default')
    
% for?as baseadas no arquivo LTBA_V300.opa com extra??o do booster
% alterada para ates do QF e utiliza dipolos do booster [2014-09-25]
    
    qa1_strength      = 0.843500;
    qa2_strength      = 1.009718;
    qb1_strength      = -0.328663;
    qb2_strength      = 2.190774;
    qc1_strength      = -1.879477;
    qc2_strength      = 1.805730;
    qc3_strength      = 1.805730;
    qc4_strength      = -1.328159;

%elseif strcmpi(caso,'mismatched_pmm')
    
else
    error('caso nao implementado');
end


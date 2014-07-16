
dQF  = QF - QF0;
dQD  = QD - QD0;
dQFC = QFC - QFC0;

switch2online;
nrpts = 10;
for i=1:nrpts
    steppv('QF',  dQF/nrpts);
    steppv('QD',  dQD/nrpts);
    steppv('QFC', dQFC/nrpts);
    pause(1);
end

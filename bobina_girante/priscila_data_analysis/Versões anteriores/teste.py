import numpy as np


############ IMPORTAÇÃO DE DADOS DO TXT DA MEDIDA ############

n_multi = np.array([])
multi_norm_rot = np.array([])
multi_norm_std_rot = np.array([])
multi_skew_rot = np.array([])
multi_skew_std_rot = np.array([])
ang_col = np.array([])
ang_col_std = np.array([])

linha_ref = 4

arq = open('C:\\Users\\priscila.sanchez\\Desktop\\BQF03_Q_BOB_+0070A_140519_092909.dat')

#pula até linha_ref
for i in range(linha_ref):
    dados_l = arq.readline()

#armazena última posição do array: nome do arquivo
nome_arq = dados_l.split('\\')[-1]
nome_arq = nome_arq.replace('\n','')

#pula até linha da corrente principal
for i in range(16-linha_ref):
    dados_l = arq.readline()
    linha_ref = linha_ref+1

#armazena corrente principal
corr_alim_princ = dados_l.split('\t')[1]
corr_alim_princ = corr_alim_princ.replace(' ','')
corr_alim_princ = corr_alim_princ.replace('\n','')
corr_alim_princ = float(corr_alim_princ)

dados_l = arq.readline()
linha_ref = linha_ref+1

#armazena std corrente principal
corr_alim_princ_std = dados_l.split('\t')[1]
corr_alim_princ_std = corr_alim_princ_std.replace(' ','')
corr_alim_princ_std = corr_alim_princ_std.replace('\n','')
corr_alim_princ_std = float(corr_alim_princ_std)

dados_l = arq.readline()
linha_ref = linha_ref+1

#se corrente secundária diferente de zero, armazena corrente secundária e seu std
if dados_l.split('\t')[1]!=0:
    corr_alim_sec = dados_l.split('\t')[1]
    corr_alim_sec = corr_alim_sec.replace(' ','')
    corr_alim_sec  = corr_alim_sec.replace('\n','')
    corr_alim_sec = float(corr_alim_sec)

    dados_l = arq.readline()
    linha_ref = linha_ref+1

    corr_alim_sec_std  = dados_l.split('\t')[1]
    corr_alim_sec_std  = corr_alim_sec_std.replace(' ','')
    corr_alim_sec_std  = corr_alim_sec_std.replace('\n','')
    corr_alim_sec_std = float(corr_alim_sec_std)

#pula linhas até o início dos dados
for i in range(40-linha_ref):
    dados_l = arq.readline()

for i in range(15):
    dados_l = arq.readline()

    #armazena coluna dos n multipolos
    y = dados_l.split('\t')[0]
    y = y.replace(' ','')
    n_multi = np.append(n_multi,int(y))

    #armazena coluna do ângulo  
    x = dados_l.split('\t')[7]
    x = x.replace(' ','')
    ang_col = np.append(ang_col,float(x))
    
    #armazena coluna do std ângulo 
    x = dados_l.split('\t')[8]
    x = x.replace(' ','')
    ang_col_std = np.append(ang_col_std,float(x))

    #armazena coluna dos multipolos normais rotacionados
    y = dados_l.split('\t')[9]
    y = y.replace(' ','')
    multi_norm_rot = np.append(multi_norm_rot,float(y))

    #armazena coluna do std dos multipolos normais rotacionados
    y = dados_l.split('\t')[10]
    y = y.replace(' ','')
    multi_norm_std_rot = np.append(multi_norm_std_rot,float(y))

    #armazena coluna dos multipolos skew rotacionados
    y = dados_l.split('\t')[11]
    y = y.replace(' ','')
    multi_skew_rot = np.append(multi_skew_rot,float(y))

    #armazena coluna do std dos multipolos skew rotacionados
    y = dados_l.split('\t')[12]
    y = y.replace(' ','')
    multi_skew_std_rot = np.append(multi_skew_std_rot,float(y))

#verifica qual posição da coluna do ângulo é não nula (qual ímã foi medido) e armazena ângulo e std do ângulo
ima = np.nonzero(ang_col)[0][0]
ang = ang_col[ima]
ang_std = ang_col_std[ima]

############ FIM DA IMPORTAÇÃO DE DADOS DO TXT DA MEDIDA ############
B_resid_norm=0
for x in range(12):
    if ima==1:
        for m in range (14):
            x=x/1000
            B_resid_norm+=n_multi[m]*(x+1)**(m)
        B_resid_norm=(B_resid_norm-n_multi[ima]*(x+1)**(m))/(n_multi[ima]*(x+1)**(m))



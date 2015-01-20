import numpy as np
import matplotlib.pyplot as plt


n_multi = np.array([])
n_multi_str=np.array([])
multi_norm = np.array([])
multi_norm_std = np.array([])
multi_skew = np.array([])
multi_skew_std = np.array([])
ang_col = np.array([])
ang_col_std = np.array([])

rcb=12
r0=17.5
B_resid_norm=np.array([])
pos = np.array([])
multi_norm_normalized=np.array([])
multi_norm_normalized_std=np.array([])

############ IMPORTACAO DE DADOS DO TXT DA MEDIDA ############

arq = open('C:\\Users\\priscila.sanchez\\Desktop\\BQF03_Q_BOB_+0070A_140519_092909.dat')

linha_ref = 4

#pula até linha_ref
for i in range(linha_ref):
    dados_l = arq.readline()

#armazena ultima posição do array: nome do arquivo
nome_arq = dados_l.split('\\')[-1]
nome_arq = nome_arq.replace('\n','')

#pula ate linha da corrente principal
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

#se corrente secundaria diferente de zero, armazena corrente secundaria e seu std
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

#pula linhas ate o início dos dados
for i in range(40-linha_ref):
    dados_l = arq.readline()

for i in range(15):
    dados_l = arq.readline()

    #armazena coluna dos n multipolos
    y = dados_l.split('\t')[0]
    y = y.replace(' ','')
    n_multi = np.append(n_multi,float(y))
    n_multi=n_multi.astype(int)
    
    #armazena coluna do angulo  
    x = dados_l.split('\t')[7]
    x = x.replace(' ','')
    ang_col = np.append(ang_col,float(x))
    
    #armazena coluna do std angulo 
    x = dados_l.split('\t')[8]
    x = x.replace(' ','')
    ang_col_std = np.append(ang_col_std,float(x))

    #armazena coluna dos multipolos normais
    y = dados_l.split('\t')[1]
    y = y.replace(' ','')
    multi_norm = np.append(multi_norm,float(y))

    #armazena coluna do std dos multipolos normais
    y = dados_l.split('\t')[2]
    y = y.replace(' ','')
    multi_norm_std = np.append(multi_norm_std,float(y))

    #armazena coluna dos multipolos skew
    y = dados_l.split('\t')[3]
    y = y.replace(' ','')
    multi_skew = np.append(multi_skew,float(y))

    #armazena coluna do std dos multipolos skew
    y = dados_l.split('\t')[4]
    y = y.replace(' ','')
    multi_skew_std = np.append(multi_skew_std,float(y))

#verifica qual posicao da coluna do angulo é não nula (qual ima foi medido) e armazena angulo e std do angulo
ima = np.nonzero(ang_col)[0][0]
ang = ang_col[ima]
ang_std = ang_col_std[ima]

############ FIM DA IMPORTACAO DE DADOS DO TXT DA MEDIDA ############


#calculo do campo residual normalizado e grafico
for i in range(rcb):
    B_resid = 0
    y = (i + 1) / 1000
    pos=np.append(pos, float(y))

    for m in n_multi:
        B_resid += multi_norm[m-1] * pos[i] ** (m-1)
        y = (B_resid - multi_norm[ima] * pos[i] ** ima) / (multi_norm[ima] * pos[i] ** ima)
    B_resid_norm = np.append(B_resid_norm, float(y))
    
plt.plot(pos,B_resid_norm)
plt.show()

#calculo dos multipolos normalizados
multi_normalized = 0
multi_normalized_std = 0
r0 = r0 / 1000
bar_color = []

for m in n_multi:
    multi_normalized = multi_norm[m-1] * r0 ** (m-1) / (multi_norm[ima] * r0 ** ima)
    multi_norm_normalized = np.append(multi_norm_normalized, float(multi_normalized))

    multi_normalized_std = multi_norm_std[m-1] * r0 ** (m-1) / (multi_norm[ima] * r0 ** ima)
    multi_norm_normalized_std = np.append(multi_norm_normalized_std, float(multi_normalized_std))
    n_multi_str = np.append(n_multi_str, str(n_multi[m-1]))

    if multi_norm_normalized[m-1] > 0:
        bar_color.append('r')
    else:
        bar_color.append('g')

#grafico de barras dos multipolos normalizados
ind = np.arange(m)+ 1  # posicao x
width = 0.2
    
fig, ax = plt.subplots()
rects1 = ax.bar(ind, abs(multi_norm_normalized), width, bottom=10**(-6), color=bar_color, yerr=abs(multi_norm_normalized_std), log=y)

ax.set_xlabel('$n$', fontsize=20)
ax.set_ylabel('$B_n/B_2(@17.5mm)$', fontsize=20)
ax.set_title('Normal multipoles normalized', fontsize=20)
ax.set_xticks(ind+width/2)
ax.set_xticklabels(n_multi_str, fontsize=14)

for label in ax.get_yticklabels():
    label.set_fontsize(14) 

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 2.2*height,'M', ha='center', va='bottom', fontsize=14)

autolabel(rects1)

plt.show()




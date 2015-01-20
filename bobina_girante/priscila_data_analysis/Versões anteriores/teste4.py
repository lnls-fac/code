import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.optimize as sp_opt


def directory(path,extension):
  list_dir = []
  list_dir = os.listdir(path)
  count = 0
  for file in list_dir:
    if file.endswith(extension): # eg: '.txt'
      count += 1
  return count,list_dir


############ IMPORTACAO DE DADOS DO TXT DA MEDIDA ############
def import_data(path_abs):
    
    global n_multi, multi_norm, multi_norm_std, multi_skew, multi_skew_std, ang, ang_std, corr_alim_princ, corr_alim_princ_std, corr_alim_sec, corr_alim_sec_std, ima
    
    n_multi = np.array([])
    multi_norm = np.array([])
    multi_norm_std = np.array([])
    multi_skew = np.array([])
    multi_skew_std = np.array([])
    ang_col = np.array([])
    ang_col_std = np.array([])

    arq = open(path_abs)

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


############ CALCULO DOS MULTIPOLOS NORMAIS NORMALIZADOS E GRAFICO ###########
def multi_norm_calc():
  global multi_norm_normalized, multi_norm_normalized_std, bar_color, m, ax1, bottom_limit, n_multi, sim_data, sim_spec, spec_data_std
 
  multi_norm_normalized=np.array([])
  multi_norm_normalized_std=np.array([])
  n_multi_str=np.array([])

  bar_color = []
  y_lower = []
  
  multi_normalized = 0
  multi_normalized_std = 0

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


  # posicao x da barra de especificacao e simulacao
  ind_spec=np.arange(m) + 1
  ind_sim=ind_spec+width

  # barras de especificacao e simulacao
  if count_file == 0:
    rects_spec = ax1.bar(ind_spec, np.absolute(spec_data), width, color=bar_color, log='y', yerr=(bottom_limit_array,spec_data_std), ecolor='b')
    rects_sim = ax1.bar(ind_sim, np.absolute(sim_data), width, color=bar_color, log='y')
   
    ind = np.arange(m) + 1 + width * 2  # posicao x das barras de medicao
  else:
    ind = ind + width

  # corrigindo o limite inferior das barras de erro da medicao
  for i in n_multi: 
    if bottom_limit>(abs(multi_norm_normalized[i-1])-abs(multi_norm_normalized_std[i-1])):
      bottom_limit_=abs(multi_norm_normalized[i-1])
      y_lower = np.append(y_lower, bottom_limit_)
    else:
      y_lower = np.append(y_lower, abs(multi_norm_normalized_std[i-1]))

  # barras de medicao 
  rects1 = ax1.bar(ind, abs(multi_norm_normalized), width, bottom=bottom_limit, color=bar_color, log='y', yerr=[y_lower, abs(multi_norm_normalized_std)], ecolor='b')

  # nomeando o topo da barra de medicao central
  def autolabel(rects,multi_norm_normalized_stds):
      i=0
      for rect in rects:
          height = rect.get_height()
          ax1.text(rect.get_x()+rect.get_width()/2., 1.1*(height+multi_norm_normalized_stds[i]),'M', ha='center', va='bottom', fontsize=13)
          i+=1
          
  # nomeando o topo da barra de especificacao e simulacao
  def autolabel_spec_sim(rects_spec_sim, spec_data_stds, labels):
      i=0
      for rect_spec_sim in rects_spec_sim:
          height = rect_spec_sim.get_height()
          if height != 0:
            ax1.text(rect_spec_sim.get_x()+rect_spec_sim.get_width()/2., 1.1*(height+spec_data_stds[i]), labels, ha='center', va='bottom', fontsize=13)
          i+=1
          
  ax1.set_xlabel('$n$', fontsize=20)
  ax1.set_ylabel(r'$\frac{B_n}{B_'+str(ima+1)+'}(@'+str(r0*1000)+'mm)$', fontsize=30)
  ax1.set_title('Normal multipoles normalized', fontsize=20)

  if count_file == 0:
    ax1.set_xticks(ind+width*(n_file)/2) # posicao x dos ticks no centro do conjunto de barras
    autolabel_spec_sim(rects_spec, spec_data_std, 'E')
    autolabel_spec_sim(rects_sim, sim_data_std, 'S')
    
  if count_file == (n_file/2 - 1):
    autolabel(rects1,multi_norm_normalized_std)

  ax1.set_xticklabels(n_multi_str, fontsize=14)
  
  for label in ax1.get_yticklabels():
      label.set_fontsize(14)
############# FIM DO CALCULO DOS MULTIPOLOS NORMAIS NORMALIZADOS E GRAFICO #############


############ FIM DA IMPORTACAO DE DADOS DO TXT DA MEDIDA ############


############ CALCULO DOS MULTIPOLOS SKEW NORMALIZADOS E GRAFICO ###########
def multi_norm_calc():
  global multi_norm_normalized, multi_skew_normalized, multi_skew_normalized_std, bar_color, m, ax1, bottom_limit, n_multi, spec_data_skew_std
 
  multi_skew_normalized=np.array([])
  multi_skew_normalized_std=np.array([])

  bar_color = []
  y_lower = []
  
  multi_normalized = 0
  multi_normalized_std = 0

  for m in n_multi:
      multi_normalized = multi_skew[m-1] * r0 ** (m-1) / (multi_norm[ima] * r0 ** ima)
      multi_skew_normalized = np.append(multi_skew_normalized, float(multi_normalized))

      multi_normalized_std = multi_skew_std[m-1] * r0 ** (m-1) / (multi_norm[ima] * r0 ** ima)
      multi_skew_normalized_std = np.append(multi_skew_normalized_std, float(multi_normalized_std))

      if multi_norm_normalized[m-1] > 0:
          bar_color.append('r')
      else:
          bar_color.append('g')


  # posicao x da barra de especificacao e simulacao
  ind_spec=np.arange(m) + 1
  ind_sim=ind_spec+width

  # barras de especificacao e simulacao
  if count_file == 0:
    rects_spec = ax1.bar(ind_spec, np.absolute(spec_data), width, color=bar_color, log='y', yerr=(bottom_limit_array,spec_data_std), ecolor='b')
    rects_sim = ax1.bar(ind_sim, np.absolute(sim_data), width, color=bar_color, log='y')
   
    ind = np.arange(m) + 1 + width * 2  # posicao x das barras de medicao
  else:
    ind = ind + width

  # corrigindo o limite inferior das barras de erro da medicao
  for i in n_multi: 
    if bottom_limit>(abs(multi_norm_normalized[i-1])-abs(multi_norm_normalized_std[i-1])):
      bottom_limit_=abs(multi_norm_normalized[i-1])
      y_lower = np.append(y_lower, bottom_limit_)
    else:
      y_lower = np.append(y_lower, abs(multi_norm_normalized_std[i-1]))

  # barras de medicao 
  rects1 = ax1.bar(ind, abs(multi_norm_normalized), width, bottom=bottom_limit, color=bar_color, log='y', yerr=[y_lower, abs(multi_norm_normalized_std)], ecolor='b')

  # nomeando o topo da barra de medicao central
  def autolabel(rects,multi_norm_normalized_stds):
      i=0
      for rect in rects:
          height = rect.get_height()
          ax1.text(rect.get_x()+rect.get_width()/2., 1.1*(height+multi_norm_normalized_stds[i]),'M', ha='center', va='bottom', fontsize=13)
          i+=1
          
  # nomeando o topo da barra de especificacao e simulacao
  def autolabel_spec_sim(rects_spec_sim, spec_data_stds, labels):
      i=0
      for rect_spec_sim in rects_spec_sim:
          height = rect_spec_sim.get_height()
          if height != 0:
            ax1.text(rect_spec_sim.get_x()+rect_spec_sim.get_width()/2., 1.1*(height+spec_data_stds[i]), labels, ha='center', va='bottom', fontsize=13)
          i+=1
          
  ax1.set_xlabel('$n$', fontsize=20)
  ax1.set_ylabel(r'$\frac{B_n}{B_'+str(ima+1)+'}(@'+str(r0*1000)+'mm)$', fontsize=30)
  ax1.set_title('Normal multipoles normalized', fontsize=20)

  if count_file == 0:
    ax1.set_xticks(ind+width*(n_file)/2) # posicao x dos ticks no centro do conjunto de barras
    autolabel_spec_sim(rects_spec, spec_data_std, 'E')
    autolabel_spec_sim(rects_sim, sim_data_std, 'S')
    
  if count_file == (n_file/2 - 1):
    autolabel(rects1,multi_norm_normalized_std)

  ax1.set_xticklabels(n_multi_str, fontsize=14)
  
  for label in ax1.get_yticklabels():
      label.set_fontsize(14)
############# FIM DO CALCULO DOS MULTIPOLOS SKEW NORMALIZADOS E GRAFICO #############


############# CALCULO DO CAMPO RESIDUAL NORMALIZADO E GRAFICO #############
def resid_norm_calc():
  global pos, B_resid_norm, fig, ax3, q

  B_resid_norm = np.array([])
  B_resid_sim_norm = np.array([])
  B_spec_resid_norm = np.array([])
  pos = np.array([])

  for i in range(rcb * 2 + 1):
      B_resid = 0
      B_resid_sim = 0
      B_spec_resid = 0
      
      y = (i - rcb) / 1000
      pos = np.append(pos, y)

      for m in n_multi:
        if y != 0:
          B_resid += multi_norm[m-1] * pos[i] ** (m-1)
          z = (B_resid - multi_norm[ima] * pos[i] ** ima - multi_norm[0]) / (multi_norm[ima] * pos[i] ** ima)
          
          B_resid_sim += sim_data_multi[m-1] * pos[i] ** (m-1)
          w = (B_resid_sim - sim_data_multi[ima] * pos[i] ** ima) / (sim_data_multi[ima] * pos[i] ** ima)

          B_spec_resid += spec_data[m-1] / r0 ** (m - ima + 1) * pos[i] ** (m - ima + 1)
        else:
          z = 0
          w = 0
          B_espec_resid = 0
          
      B_resid_norm = np.append(B_resid_norm, float(z))
      B_resid_sim_norm = np.append(B_resid_sim_norm, float(w))
      B_spec_resid_norm = np.append(B_spec_resid_norm, B_spec_resid)

  if count_file == 0:
    plt.plot(pos, B_resid_sim_norm, label = 'Simulation')
    plt.plot(pos, B_spec_resid_norm, label = 'Specification')
    
  plt.plot(pos, B_resid_norm, label = 'I = %.2f A'% corr_alim_princ)
 
  plt.xlabel('Transversal Position x [m]', fontsize=20)
  plt.ylabel(r'$\frac{\sum_{n=1-[n='+str(ima+1)+']}^{'+n_multi_str[-1]+'}B_n}'+'{B_'+str(ima+1)+'}$', fontsize=30)
  plt.title('Residual Normal Integrated Field Normalized', fontsize=20)

  plt.ticklabel_format(axis='both',style='sci',scilimits=(0,0))
  plt.rc('font', **{'size':'14'})
  
  for label in ax3.get_yticklabels():
    label.set_fontsize(14)

  for label in ax3.get_xticklabels():
    label.set_fontsize(14) 
    
  plt.legend(loc='upper center')
  

############# FIM DO CALCULO DO CAMPO RESIDUAL NORMALIZADO E GRAFICO #############


############# CURVA DE EXCITACAO E SATURACAO #############
def excit_calc():

  global ax3, B_excit, B_excit_std, corr_alim_princ_arr, corr_alim_princ_arr_std, count_file

  B_excit = np.append(B_excit, multi_norm[ima])
  B_excit_std = np.append(B_excit_std, multi_norm_std[ima])
  corr_alim_princ_arr = np.append(corr_alim_princ_arr, corr_alim_princ)
  corr_alim_princ_arr_std = np.append(corr_alim_princ_arr_std, corr_alim_princ_std)

  if count_file == n_file - 1:
    fig4, ax4 = plt.subplots()
    plt.grid()
    
    ax3.errorbar(corr_alim_princ_arr, B_excit, xerr=corr_alim_princ_arr_std, yerr=B_excit_std)

    params = np.polyfit(corr_alim_princ_arr, B_excit, 1)
    [a, b] = params
    B_excit_ajust = a * corr_alim_princ_arr + b
    plt.plot(corr_alim_princ_arr, B_excit_ajust)

    if ima == 1:
      ax4.text(1.5, 2.3, ' Curve Fitting Line \n Integrated Gradient = A * Excitation Current + B \n\n A = %.7f\n B = %.7f' % (a, b), color='black', 
          bbox=dict(facecolor='none', edgecolor='black'))
    elif ima == 2:
      ax4.text(1.5, 2.3, ' Curve Fitting Line \n Integrated Gradient = A * Excitation Current + B \n\n A = %.7f\n B = %.7f' % (a, b), color='black', 
          bbox=dict(facecolor='none', edgecolor='black'))
    else:
      ax4.text(1.5, 2.3, ' Curve Fitting Line \n Integrated Field = A * Excitation Current + B \n\n A = %.7f\n B = %.7f' % (a, b), color='black', 
          bbox=dict(facecolor='none', edgecolor='black'))
    
    plt.xlabel('Excitation Current [A]', fontsize=20)
    if ima == 1:
      plt.ylabel('Integrated Gradient Measured [T]', fontsize=20)
    elif ima == 2:
      plt.ylabel('Integrated Gradient Measured [T/m]', fontsize=20)
    else:
      plt.ylabel('Integrated Field Measured [T]', fontsize=20)
    plt.title('Excitation Curve', fontsize=20)

    for label in ax4.get_yticklabels():
      label.set_fontsize(14)

    for label in ax4.get_xticklabels():
      label.set_fontsize(14)

    fig5, ax5 = plt.subplots()
    plt.grid()
    
    B_excit_resid = (B_excit - B_excit_ajust) / B_excit * 100
    corr_alim_princ_arr_sat = np.delete(corr_alim_princ_arr,0)
    B_excit_resid_sat = np.delete(B_excit_resid,0)
    plt.plot(corr_alim_princ_arr_sat, B_excit_resid_sat)

    plt.xlabel('Excitation Current [A]', fontsize=20)
    if ima == 1:
      plt.ylabel('Integrated Gradient (Measured - Adjusted) / Adjusted [%]', fontsize=20)
    elif ima == 2:
      plt.ylabel('Integrated Gradient (Measured - Adjusted) / Adjusted [%]', fontsize=20)
    else:
      plt.ylabel('Integrated Field (Measured - Adjusted) / Adjusted [%]', fontsize=20)
    plt.title('Saturation Curve', fontsize=20)
   
    for label in ax5.get_yticklabels():
      label.set_fontsize(14)

    for label in ax5.get_xticklabels():
      label.set_fontsize(14) 

    plt.show()


############# FIM DA CURVA DE EXCITACAO E SATURACAO #############
    

global n_file, count_file, r0, rcb, ax1, ax2, sim_data, spec_data, spec_data_std, width, B_excit, B_excit_std, corr_alim_princ_arr, corr_alim_princ_arr_std, sim_data_multi

rcb = 18
r0 = 17.5
bottom_limit = 10**(-6)
width = 0.07

path1="C:\\Users\\priscila.sanchez\\Desktop\\TESTES-BOBINA\\BQF03 - Curva Excitacao\\Fonte 130A\\Ligacao_Defocalizador\\01_Sequencia\\"

files_info = directory(path1, '.dat')
n_file = files_info[0]
path_abs1_all = files_info[1]

r0 = r0 / 1000

fig1, ax1 = plt.subplots()
plt.grid()
fig2, ax2 = plt.subplots()
plt.grid()
fig3, ax3 = plt.subplots()
plt.grid()

B_excit = []
B_excit_std = []
corr_alim_princ_arr = []
corr_alim_princ_arr_std = []

for count_file in range(n_file):
  import_data (path1 + path_abs1_all[count_file])
  if ima == 1:
    sim_data =            [0, 0,         0,              0,              0,              -1.0431*10**(-3), 0,              0,              0,              1.18022*10**(-3), 0,              0,              0,              2.76057*10**(-5), 0]
    spec_data =           [0, 0,         0,              0,              0,              -1.0000*10**(-3), 0,              0,              0,              1.10*10**(-3),    0,              0,              0,              8.00*10**(-5),    0]
    spec_data_skew_std =  [0, 0,         1.00*10**(-4),  5.00*10**(-4),  1.00*10**(-4),  1.00*10**(-4),    1.00*10**(-4),  1.00*10**(-4),  1.00*10**(-4),  1.00*10**(-4),    1.00*10**(-4),  1.00*10**(-4),  1.00*10**(-4),  1.00*10**(-4),    0]
    spec_data_std =       [0, 0,         7.00*10**(-4),  4.00*10**(-4),  4.00*10**(-4),  4.00*10**(-4),    4.00*10**(-4),  4.00*10**(-4),  4.00*10**(-4),  4.00*10**(-4),    4.00*10**(-4),  4.00*10**(-4),  4.00*10**(-4),  4.00*10**(-4),    0]
    sim_data_multi =      [0, 4.695788,  0,              0,              0,              -5.22255*10**(4), 0,              0,              0,              6.30039*10**(11), 0,              0,              0,              1.57127*10**(17), 0]

    
  sim_data_std = np.zeros(n_multi[-1])
  bottom_limit_array = np.absolute(spec_data) - bottom_limit

  multi_norm_calc()
  resid_norm_calc()
  excit_calc()

plt.show()










  


      
  

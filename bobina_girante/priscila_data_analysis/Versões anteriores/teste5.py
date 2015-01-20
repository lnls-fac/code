import numpy as np
import matplotlib.pyplot as plt
import os

plt.rcParams['figure.figsize'] = 22, 12

def directory(path,extension):

  list_dir = []
  list_dir = os.listdir(path)
  count = 0
  count_total = 0
  for file in list_dir:
    if file.endswith(extension): # eg: '.dat'
      count += 1
  for files in list_dir:
    if not files.endswith(extension):
      list_dir = np.delete(list_dir, count_total)
    else:
      count_total +=1
  return count,list_dir


############ IMPORTACAO DE DADOS DO TXT DA MEDIDA ############
def import_data(path_abs):
    
    global n_multi, multi_norm, multi_norm_std, multi_skew, multi_skew_std, ang, ang_std, corr_alim_princ, corr_alim_princ_std, corr_alim_sec, corr_alim_sec_std, ima, nome_ima, data
    
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
    nome_str = nome_arq.split("_")
    nome_ima = nome_str[0]
    data = nome_str[-2]

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
  global multi_norm_normalized, multi_norm_normalized_std, bar_color, ax1, bottom_limit, n_multi, sim_data, sim_spec, spec_data_std, n_multi_str, fig1,ind, name_fig
 
  multi_norm_normalized=np.array([])
  multi_norm_normalized_std=np.array([])
  n_multi_str=np.array([])

  bar_color = []
  y_lower = []
  y_lower_spec = []
  
  multi_normalized = 0
  multi_normalized_std = 0

  if count_file == 0:
    fig1, ax1 = plt.subplots()
    plt.grid()

  for m in n_multi:
      multi_normalized = multi_norm[m - 1] * r0 ** (m - 1) / (multi_norm[ima] * r0 ** ima)
      multi_norm_normalized = np.append(multi_norm_normalized, float(multi_normalized))

      multi_normalized_std = multi_norm_std[m - 1] * r0 ** (m-1) / (multi_norm[ima] * r0 ** ima)
      multi_norm_normalized_std = np.append(multi_norm_normalized_std, float(multi_normalized_std))
      n_multi_str = np.append(n_multi_str, str(n_multi[m - 1]))

      if multi_norm_normalized[m - 1] > 0:
        bar_color.append('r')
      else:
        bar_color.append('g')

      if spec_data[m - 1] == 0:
        spec_data[m - 1] = bottom_limit * 10 ** (-3)
        
      if sim_data[m - 1] == 0:
        sim_data[m - 1] = bottom_limit * 10 ** (-3)


  # posicao x da barra de especificacao e simulacao
  ind_spec=np.arange(m) + 1
  ind_sim=ind_spec+width

  # corrigindo o limite inferior das barras de erro da especificacao
  for i in n_multi: 
    if bottom_limit>(np.absolute(spec_data[i-1])-np.absolute(spec_data_std[i-1])):
      bottom_limit_= np.absolute(spec_data[i-1])
      y_lower_spec = np.append(y_lower_spec, bottom_limit_)
    else:
      y_lower_spec = np.append(y_lower_spec, np.absolute(spec_data_std[i-1]))
  
  # barras de especificacao e simulacao
  if count_file == 0:
    rects_spec = ax1.bar(ind_spec, np.absolute(spec_data), width, bottom=bottom_limit, color=bar_color, log='y', yerr=[y_lower_spec,spec_data_std], ecolor='b')
    rects_sim = ax1.bar(ind_sim, np.absolute(sim_data), width, bottom=bottom_limit, color=bar_color, log='y')
   
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
          ax1.text(rect_spec_sim.get_x()+rect_spec_sim.get_width()/2., 1.1*(height+spec_data_stds[i]), labels, ha='center', va='bottom', fontsize=13)
          i+=1
          
  ax1.set_xlabel('$n$', fontsize=20)
  ax1.set_ylabel(r'$\frac{B_{N_n}}{B_{N_'+str(ima+1)+'}}(@'+str(r0*1000)+'$ ''$ mm)$', fontsize=30)
  ax1.set_title(nome_ima +' - '+data+' - Normal Integrated Multipoles Normalized', fontsize=20)
  
  if count_file == 0:
    ax1.set_xticks(ind+width*(n_file)/2) # posicao x dos ticks no centro do conjunto de barras
    autolabel_spec_sim(rects_spec, spec_data_std, 'E')
    autolabel_spec_sim(rects_sim, sim_data_std, 'S')
    
  if count_file == (n_file/2 - 1):
    autolabel(rects1,multi_norm_normalized_std)

  ax1.set_xticklabels(n_multi_str, fontsize=14)
  
  for label in ax1.get_yticklabels():
      label.set_fontsize(14)

  if count_file == n_file - 1:
    name_fig = np.append(name_fig, ax1.get_title())

  
############# FIM DO CALCULO DOS MULTIPOLOS NORMAIS NORMALIZADOS E GRAFICO #############



############ CALCULO DOS MULTIPOLOS SKEW NORMALIZADOS E GRAFICO ###########
def multi_skew_calc():
  global multi_norm_normalized, multi_skew_normalized, multi_skew_normalized_std, bar_color, ax2, bottom_limit, n_multi, spec_data_skew_std, fig2, ind2, name_fig
 
  multi_skew_normalized=np.array([])
  multi_skew_normalized_std=np.array([])

  bar_color = []
  y_lower = []
  y_lower_spec = []

  spec_data_skew = np.ones(n_multi[-1]) * bottom_limit * 10 ** (-3)
  
  multi_normalized = 0
  multi_normalized_std = 0

  if count_file == 0:
    fig2, ax2 = plt.subplots()
    plt.grid()
    
  for m in n_multi:
      multi_normalized = multi_skew[m-1] * r0 ** (m-1) / (multi_norm[ima] * r0 ** ima)
      multi_skew_normalized = np.append(multi_skew_normalized, float(multi_normalized))

      multi_normalized_std = multi_skew_std[m-1] * r0 ** (m-1) / (multi_norm[ima] * r0 ** ima)
      multi_skew_normalized_std = np.append(multi_skew_normalized_std, float(multi_normalized_std))

      if multi_norm_normalized[m-1] > 0:
          bar_color.append('r')
      else:
          bar_color.append('g')


  # posicao x da barra de especificacao
  ind_spec=np.arange(m) + 1

  # corrigindo o limite inferior das barras de erro da especificacao
  for i in n_multi: 
    if bottom_limit>(np.absolute(spec_data_skew[i-1])-np.absolute(spec_data_skew_std[i-1])):
      bottom_limit_= np.absolute(spec_data_skew[i-1])
      y_lower_spec = np.append(y_lower_spec, bottom_limit_)
    else:
      y_lower_spec = np.append(y_lower_spec, np.absolute(spec_data_skew_std[i-1]))

  # barras de erro da especificacao
  if count_file == 0:
    rects_spec_skew = ax2.bar(ind_spec, spec_data_skew, width, bottom=bottom_limit, yerr= [y_lower_spec, np.absolute(spec_data_skew_std)], color=bar_color, log='y')
   
    ind2 = np.arange(m) + 1 + width  # posicao x das barras de medicao
  else:
    ind2 = ind2 + width

  # corrigindo o limite inferior das barras de erro da medicao
  for i in n_multi: 
    if bottom_limit>(abs(multi_skew_normalized[i-1])-abs(multi_skew_normalized_std[i-1])):
      bottom_limit_=abs(multi_skew_normalized[i-1])
      y_lower = np.append(y_lower, bottom_limit_)
    else:
      y_lower = np.append(y_lower, abs(multi_skew_normalized_std[i-1]))

  # barras de medicao 
  rects2 = ax2.bar(ind2, abs(multi_skew_normalized), width, bottom=bottom_limit, color=bar_color, log='y', yerr=[y_lower, abs(multi_skew_normalized_std)], ecolor='b')

  # nomeando o topo da barra de medicao central
  def autolabel(rects,multi_skew_normalized_stds):
      i = 0
      for rect in rects:
          height = rect.get_height()
          ax2.text(rect.get_x()+rect.get_width()/2., 1.1*(height+multi_skew_normalized_stds[i]),'M', ha='center', va='bottom', fontsize=13)
          i += 1
          
  # nomeando o topo da barra de especificacao
  def autolabel_spec_sim(rects_spec_skew, spec_data_skew_stds, labels):
      i = 0
      for rect_spec_skew in rects_spec_skew:
          height = rect_spec_skew.get_height()
          if height != 0:
            ax2.text(rect_spec_skew.get_x()+rect_spec_skew.get_width()/2., 1.1*(height+spec_data_skew_stds[i]), labels, ha='center', va='bottom', fontsize=13)
          i += 1
          
  ax2.set_xlabel('$n$', fontsize=20)
  ax2.set_ylabel(r'$\frac{B_{S_n}}{B_{N_'+str(ima+1)+'}}(@'+str(r0*1000)+'$ ''$mm)$', fontsize=30)
  ax2.set_title(nome_ima +' - '+data+' - Skew Integrated Multipoles Normalized', fontsize=20)

  if count_file == 0:
    ax2.set_xticks(ind2+width*(n_file)/2) # posicao x dos ticks no centro do conjunto de barras
    autolabel_spec_sim(rects_spec_skew, spec_data_skew_std, 'E')
    
  if count_file == (n_file/2 - 1):
    autolabel(rects2, multi_skew_normalized_std)

  ax2.set_xticklabels(n_multi_str, fontsize=14)
  
  for label in ax2.get_yticklabels():
      label.set_fontsize(14)

  if count_file == n_file - 1:
    name_fig = np.append(name_fig, ax2.get_title())

############# FIM DO CALCULO DOS MULTIPOLOS SKEW NORMALIZADOS E GRAFICO #############


############# CALCULO DO CAMPO RESIDUAL NORMALIZADO E GRAFICO #############
def resid_norm_calc():
  global pos, B_resid_norm, fig3, ax3, name_fig

  B_resid_norm = np.array([])
  B_resid_sim_norm = np.array([])
  B_spec_resid_norm = np.array([])
  pos = np.array([])

  if count_file == 0:
    fig3, ax3 = plt.subplots()
    plt.grid()
    
  for i in range(rcb * 2 + 1):
      B_resid = 0
      B_resid_sim = 0
      B_spec_resid = 0
      
      y = (i - rcb) / 1000
      pos = np.append(pos, y)

      for m in n_multi:
        if y != 0:
          B_resid += multi_norm[m - 1] * pos[i] ** (m - 1)
          z = (B_resid - multi_norm[ima] * pos[i] ** ima - multi_norm[0]) / (multi_norm[ima] * pos[i] ** ima)
          
          B_resid_sim += sim_data_multi[m - 1] * pos[i] ** (m - 1)
          w = (B_resid_sim - sim_data_multi[ima] * pos[i] ** ima) / (sim_data_multi[ima] * pos[i] ** ima)

          B_spec_resid += spec_data[m - 1] / r0 ** (m - ima + 1) * pos[i] ** (m - ima + 1) # calculo do campo residual a partir dos multipolos normalizados
        else:
          z = 0
          w = 0
          B_espec_resid = 0
          
      B_resid_norm = np.append(B_resid_norm, float(z))
      B_resid_sim_norm = np.append(B_resid_sim_norm, float(w))
      B_spec_resid_norm = np.append(B_spec_resid_norm, B_spec_resid)

  if count_file == 0:
    plt.plot(pos, B_resid_sim_norm, label = 'Simulation', linewidth=2.0)
    plt.plot(pos, B_spec_resid_norm, label = 'Specification', linewidth=2.0)
    
  plt.plot(pos, B_resid_norm, label = 'I = %.2f A'% corr_alim_princ, linewidth=2.0)
 
  plt.xlabel('Transversal Position x [m]', fontsize=20)
  if ima == 1:
    plt.ylabel(r'$\frac{\sum_{n=3}^{'+n_multi_str[-1]+'}B_{N_n}}'+'{B_{N_'+str(ima+1)+'}}$', fontsize=30)
  else:
    plt.ylabel(r'$\frac{\sum_{n=2-[n='+str(ima+1)+']}^{'+n_multi_str[-1]+'}B_{N_n}}'+'{B_{N_'+str(ima+1)+'}}$', fontsize=30)
  plt.title(nome_ima +' - '+data+' - Residual Normal Integrated Field Normalized', fontsize=20)

  plt.ticklabel_format(axis='both',style='sci',scilimits=(0,0))
  plt.rc('font', **{'size':'14'})
  
  for label in ax3.get_yticklabels():
    label.set_fontsize(14)

  for label in ax3.get_xticklabels():
    label.set_fontsize(14) 
    
  plt.legend(loc='upper center')

  if count_file == n_file - 1:
    name_fig = np.append(name_fig, ax3.get_title())  

############# FIM DO CALCULO DO CAMPO RESIDUAL NORMALIZADO E GRAFICO #############


############# CURVA DE EXCITACAO E SATURACAO #############
def excit_calc():

  global B_excit, B_excit_std, corr_alim_princ_arr, corr_alim_princ_arr_std, count_file, B_excit_ajust, fig4, fig5, name_fig

  # pegando apenas a componente principal
  B_excit = np.append(B_excit, multi_norm[ima])
  B_excit_std = np.append(B_excit_std, multi_norm_std[ima])
  corr_alim_princ_arr = np.append(corr_alim_princ_arr, corr_alim_princ)
  corr_alim_princ_arr_std = np.append(corr_alim_princ_arr_std, corr_alim_princ_std)

  if count_file == n_file - 1:
    fig4, ax4 = plt.subplots()
    plt.grid()

    # criando curva de excitacao
    ax4.errorbar(corr_alim_princ_arr, B_excit, xerr=corr_alim_princ_arr_std, yerr=B_excit_std, marker ='o',markersize=3, linewidth=2.0)

    # calculando ajuste linear
    params = np.polyfit(corr_alim_princ_arr, B_excit, 1)
    [a, b] = params
    B_excit_ajust = a * corr_alim_princ_arr + b
    plt.plot(corr_alim_princ_arr, B_excit_ajust, '-g', linewidth=2.0)

    # colocando dados do ajuste no grafico
    if ima == 1:
      ax4.text(1.5, 2.5, ' Curve Fitting Line \n Integrated Gradient = A * Excitation Current + B \n\n A = %.7f\n B = %.7f' % (a, b), color='black', fontsize=20,
          bbox=dict(facecolor='white', edgecolor='black'))
    elif ima == 2:
      ax4.text(1.5, 2.5, ' Curve Fitting Line \n Integrated Gradient = A * Excitation Current + B \n\n A = %.7f\n B = %.7f' % (a, b), color='black', fontsize=20,
          bbox=dict(facecolor='white', edgecolor='black'))
    else:
      ax4.text(1.5, 2.5, ' Curve Fitting Line \n Integrated Field = A * Excitation Current + B \n\n A = %.7f\n B = %.7f' % (a, b), color='black', fontsize=20,
          bbox=dict(facecolor='white', edgecolor='black'))
    
    plt.xlabel('Excitation Current [A]', fontsize=20)
    
    if ima == 1:
      plt.ylabel('$N_{'+str(ima+1)+'_{Measured}}$ [T]', fontsize=30)
    elif ima == 2:
      plt.ylabel('$N_{'+str(ima+1)+'_{Measured}}$ [T/m]', fontsize=30)
    else:
      plt.ylabel('$N_{'+str(ima+1)+'_{Measured}}$ [T.m]', fontsize=30)
    plt.title(nome_ima +' - '+data+' - Excitation Curve', fontsize=20)

    for label in ax4.get_yticklabels():
      label.set_fontsize(14)

    for label in ax4.get_xticklabels():
      label.set_fontsize(14)

    fig5, ax5 = plt.subplots()
    plt.grid()

    # calculando curva de saturacao
    B_excit_resid = (B_excit - B_excit_ajust) / B_excit * 100
    corr_alim_princ_arr_sat = np.delete(corr_alim_princ_arr,0)
    
    # eliminando primeiro ponto da curva de saturacao
    B_excit_resid_sat = np.delete(B_excit_resid,0)
    plt.plot(corr_alim_princ_arr_sat, B_excit_resid_sat, marker='o', color='r', linewidth=2.0)

    plt.xlabel('Excitation Current [A]', fontsize=20)

    plt.ylabel(r'$\frac{N_{'+str(ima+1)+'_{Measured}} - N_{'+str(ima+1)+'_{Adjusted}}}{N_{'+str(ima+1)+'_{Adjusted}}}$'' [%]', fontsize=30)

    plt.title(nome_ima +' - '+data+' - Saturation Curve', fontsize=20)
   
    for label in ax5.get_yticklabels():
      label.set_fontsize(14)

    for label in ax5.get_xticklabels():
      label.set_fontsize(14)

    if count_file == n_file - 1:
      name_fig = np.append(name_fig, ax4.get_title())
      name_fig = np.append(name_fig, ax5.get_title())

############# FIM DA CURVA DE EXCITACAO E SATURACAO #############



############# CURVA DE ANGULO #############
def ang_calc():

  global ang, ang_std, ang_arr, ang_arr_std, corr_alim_princ_arr, corr_alim_princ_arr_std, count_file, fig6, name_fig
 
  # pegando o angulo
  ang_arr = np.append(ang_arr, ang * 1000)
  ang_arr_std = np.append(ang_arr_std, ang_std * 1000)

  if count_file == n_file - 1:
    fig6, ax6 = plt.subplots()
    plt.grid()
  
    # criando curva de excitacao
    ax6.errorbar(corr_alim_princ_arr, ang_arr, marker='o', color='r', linewidth=2.0, xerr=corr_alim_princ_arr_std, yerr=ang_arr_std, ecolor='b', elinewidth=1.0)
  
    plt.xlabel('Excitation Current [A]', fontsize=20)
    plt.ylabel('$n^{-1} * atan(S_'+str(ima+1)+'/N_'+str(ima+1)+')$'' [mrad]', fontsize=20)
    plt.title(nome_ima +' - '+data+' - Angle', fontsize=20)

    for label in ax6.get_yticklabels():
      label.set_fontsize(14)

    for label in ax6.get_xticklabels():
      label.set_fontsize(14)

    if count_file == n_file - 1:
      name_fig = np.append(name_fig, ax6.get_title())

############# FIM DA CURVA DE ANGULO #############


############# TABELA #############
def tabela():

  global fig7, name_fig,table_matrix
  table_matrix=[]

  colLabels = (r'$n$', '$N_n$'' $[T.m^{(2-n)}]$', '$Err - N_n$'' $[T.m^{(2-n)}]$', '$S_n$'' $[T.m^{(2-n)})]$', '$Err - S_n$'' $[T.m^{(2-n)}]$')
  
  for i in range(n_multi[-1]+1):
    if i == 0:
      table = np.zeros(5)
    else:
      table = ['%d' % n_multi[i-1], '%.4e' % multi_norm[i-1], '%.4e' % multi_norm_std[i-1], '%.4e' % multi_skew[i-1], '%.4e' % multi_skew_std[i-1]]
    table_matrix.append(table)

  scale_h=2.7
  colWidths=[.1,.2,.2,.2,.2]

  nrows, ncols = len(table_matrix)+1, len(colLabels)
  hcell, wcell = 0.2, 3.5
  hpad, wpad = 0, 0    
  fig7 = plt.figure(figsize=(ncols*wcell+wpad, (nrows*hcell+hpad)*scale_h))
  ax7 = fig7.add_subplot(111)
  ax7.axis('off')

  the_table = ax7.table(cellText=table_matrix , colWidths=colWidths, colLabels=colLabels, colColours=['w', 'w', 'w', 'w', 'w'], loc='center', cellLoc='center')
  
  the_table.auto_set_font_size(False)
  the_table.set_fontsize(20)
  
  # ajustando escala  da figura e tabela
  the_table.scale(1, scale_h)
  ax7.set_title(nome_ima +' - '+data+'- Normal and Skew Multipoles - Current - %.2f A' % corr_alim_princ, fontsize=20)

  if count_file == n_file - 1:
      name_fig = np.append(name_fig, ax7.get_title())

############# FIM DA TABELA #############
  

global n_file, count_file, r0, rcb, fig1, fig2, fig3, fig4, fig5, fig6, sim_data, spec_data, spec_data_std, width, B_excit, B_excit_std, B_excit_ajust,\
       corr_alim_princ_arr, corr_alim_princ_arr_std, sim_data_multi, ind, ind2, bottom_limit_array, bottom_limit, B_excit_ajust, name_fig, fig7

if ima == 0:
  rcb = 15
  r0 = 15
  
if ima == 1:
  rcb = 18
  r0 = 17.5

if ima == 2:
  rcb = 18
  r0 = 17.5

bottom_limit = 10**(-6)
width = 0.07

path1="C:\\Users\\priscila.sanchez\\Desktop\\TESTES-BOBINA\\BQF03 - Curva Excitacao\\Fonte 130A\\Ligacao_Defocalizador\\01_Sequencia\\"

files_info = directory(path1, '.dat')
n_file = files_info[0]
path_abs1_all = files_info[1]

r0 = r0 / 1000

B_excit = []
B_excit_std = []
corr_alim_princ_arr = []
corr_alim_princ_arr_std = []
ang_arr = []
ang_arr_std = []
name_fig = []


for count_file in range(n_file):
  import_data (path1 + path_abs1_all[count_file])

  if ima == 0: # corretora horizontal sobre retas
    sim_data =            [0,                0,  3.06401*10**(-3),  0,  -1.27331*10**(-3),  0,  -1.70843*10**(-3),  0,  -1.14341*10**(-4),  0,  2.32739*10**(-4),  0,  -7.11864*10**(-5),  0,  8.59749*10**(-6)]
    spec_data =           [0,                0,  0,                 0,  0,                  0,  0,                  0,  0,                  0,  0,                 0,  0,                  0,  0               ]
    spec_data_skew_std =  [0,                0,  0,                 0,  0,                  0,  0,                  0,  0,                  0,  0,                 0,  0,                  0,  0               ]
    spec_data_std =       [0,                0,  0,                 0,  0,                  0,  0,                  0,  0,                  0,  0,                 0,  0,                  0,  0               ]
    sim_data_multi =      [3.02946*10**(-3), 0,  4.12547*10**(-2),  0,  -7.61962*10**(1),   0,  -4.54377*10**(5),   0,  -1.35157*10**(8),   0,  1.22271*10**(12),  0,  -1.66214*10**(15),  0,  8.92194*10**(17)]

  if ima == 1: # quadrupolo defocalizador
    sim_data =            [0, 0,         0,              0,              0,              -1.0431*10**(-3), 0,              0,              0,              1.18022*10**(-3), 0,              0,              0,              2.76057*10**(-5), 0]
    spec_data =           [0, 0,         0,              0,              0,              -1.0000*10**(-3), 0,              0,              0,              1.10*10**(-3),    0,              0,              0,              8.00*10**(-5),    0]
    spec_data_skew_std =  [0, 0,         1.00*10**(-4),  5.00*10**(-4),  1.00*10**(-4),  1.00*10**(-4),    1.00*10**(-4),  1.00*10**(-4),  1.00*10**(-4),  1.00*10**(-4),    1.00*10**(-4),  1.00*10**(-4),  1.00*10**(-4),  1.00*10**(-4),    0]
    spec_data_std =       [0, 0,         7.00*10**(-4),  4.00*10**(-4),  4.00*10**(-4),  4.00*10**(-4),    4.00*10**(-4),  4.00*10**(-4),  4.00*10**(-4),  4.00*10**(-4),    4.00*10**(-4),  4.00*10**(-4),  4.00*10**(-4),  4.00*10**(-4),    0]
    sim_data_multi =      [0, 4.695788,  0,              0,              0,              -5.22255*10**(4), 0,              0,              0,              6.30039*10**(11), 0,              0,              0,              1.57127*10**(17), 0]

  if ima == 2: # sextupolo focalizador
    sim_data =            [0, 0, 0,              0,              0,              0,                 0,              0,                -3.35214*10**(-2),    0,                  0,                0,                0,                0,                -9.11223*10**(-3)]
    spec_data =           [0, 0, 0,              0,              0,              0,                 0,              0,                -2.40*10**(-2),       0,                  0,                0,                0,                0,                -1.70*10**(-2)   ]
    spec_data_skew_std =  [0, 0, 0,              1.00*10**(-4),  1.00*10**(-4),  1.00*10**(-4),     1.00*10**(-4),  1.00*10**(-4),    1.00*10**(-4),        1.00*10**(-4),      1.00*10**(-4),    1.00*10**(-4),    1.00*10**(-4),    1.00*10**(-4),    0                ]
    spec_data_std =       [0, 0, 0,              4.00*10**(-4),  4.00*10**(-4),  4.00*10**(-4),     4.00*10**(-4),  4.00*10**(-4),    4.00*10**(-4),        4.00*10**(-4),      4.00*10**(-4),    4.00*10**(-4),    4.00*10**(-4),    4.00*10**(-4),    0                ]
    sim_data_multi =      [0, 0, -23.10300,      0,              0,              0,                 0,              0,                2.69627*10**(10),     0,                  0,                0,                0,                0,                2.55174*10**(20) ]
   
  sim_data_std = np.zeros(n_multi[-1])

  multi_norm_calc()
  multi_skew_calc()
  resid_norm_calc()
  excit_calc()
  ang_calc()
  
tabela()

fig = [fig1, fig2, fig3, fig4, fig5, fig6, fig7]

for k in range (7):
  fig[k].savefig(path1+name_fig[k]+'.png')

plt.show()











  


      
  

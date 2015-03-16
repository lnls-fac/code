import numpy as np
import matplotlib.pyplot as plt
import threading
import os
import sys
import glob
from PyQt4 import QtCore, QtGui

from interface_data_analysis_vs_1 import * # nome do meu arquivo.py de interface



############# INTERFACE #############   
class interface(threading.Thread):
    def __init__(self): # init nao necessita ser chamada, roda automaticamente
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        # inicia interface grafica
        self.App = QtGui.QApplication(sys.argv)
        self.myapp = MyForm()
        self.myapp.show()
        self.App.exec_()

##class interface(object):
##    def __init__(self):
##        # inicia interface grafica
##        self.App = QtGui.QApplication(sys.argv)
##        self.myapp = MyForm()
##        self.myapp.show()
##        self.App.exec_()

############# FIM DA INTERFACE #############


#####
class MyForm(QtGui.QMainWindow):
  
  def __init__(self, parent=None):
    # inicializa interface
    QtGui.QWidget.__init__(self, parent)
    self.ui = Ui_Form() # tipo da minha funcao de interface
    self.ui.setupUi(self)

    #formata tamanho das figuras diferente do padrao
    plt.rcParams['figure.figsize'] = 22, 12 

    #botoes
    self.ui.pBproc_pasta.clicked.connect(self.load_path)
    self.ui.pBrodar_prog.clicked.connect(self.main)

  #configura o caminho para a leitura do arquivo .dat
  def load_path(self):
    self.path1 = QtGui.QFileDialog.getOpenFileName(self,'Load File','.','Data files (*.dat);;Text files (*.txt)')
    self.path1 = os.path.abspath(os.path.dirname(self.path1))+'\\'

  #conta os arquivos com extensao .dat no caminho se houver outros que nao sejam .dat sao desconsiderados
  def directory(self,extension):

    list_dir = []
    list_dir = os.listdir(self.path1)
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
  def import_data(self,path_abs):
      
      self.n_multi = np.array([])
      self.multi_norm = np.array([])
      self.multi_norm_std = np.array([])
      self.multi_skew = np.array([])
      self.multi_skew_std = np.array([])
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
      self.nome_ima = nome_str[0]
      self.date = nome_str[-2]

      #pula ate linha da corrente principal
      for i in range(16-linha_ref):
          dados_l = arq.readline()
          linha_ref = linha_ref+1

      #armazena corrente principal
      self.corr_alim_princ = dados_l.split('\t')[1]
      self.corr_alim_princ = self.corr_alim_princ.replace(' ','')
      self.corr_alim_princ = self.corr_alim_princ.replace('\n','')
      self.corr_alim_princ = float(self.corr_alim_princ)

      dados_l = arq.readline()
      linha_ref = linha_ref+1

      #armazena std corrente principal
      self.corr_alim_princ_std = dados_l.split('\t')[1]
      self.corr_alim_princ_std = self.corr_alim_princ_std.replace(' ','')
      self.corr_alim_princ_std = self.corr_alim_princ_std.replace('\n','')
      self.corr_alim_princ_std = float(self.corr_alim_princ_std)

      dados_l = arq.readline()
      linha_ref = linha_ref+1

      #se corrente secundaria diferente de zero, armazena corrente secundaria e seu std
      if dados_l.split('\t')[1]!=0:
          self.corr_alim_sec = dados_l.split('\t')[1]
          self.corr_alim_sec = self.corr_alim_sec.replace(' ','')
          self.corr_alim_sec  = self.corr_alim_sec.replace('\n','')
          self.corr_alim_sec = float(self.corr_alim_sec)

          dados_l = arq.readline()
          linha_ref = linha_ref+1

          self.corr_alim_sec_std  = dados_l.split('\t')[1]
          self.corr_alim_sec_std  = self.corr_alim_sec_std.replace(' ','')
          self.corr_alim_sec_std  = self.corr_alim_sec_std.replace('\n','')
          self.corr_alim_sec_std = float(self.corr_alim_sec_std)

      #pula linhas ate o início dos dados
      for i in range(40-linha_ref):
          dados_l = arq.readline()

      for i in range(15):
          dados_l = arq.readline()

          #armazena coluna dos n multipolos
          y = dados_l.split('\t')[0]
          y = y.replace(' ','')
          self.n_multi = np.append(self.n_multi,float(y))
          self.n_multi=self.n_multi.astype(int)
          
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
          self.multi_norm = np.append(self.multi_norm,float(y))

          #armazena coluna do std dos multipolos normais
          y = dados_l.split('\t')[2]
          y = y.replace(' ','')
          self.multi_norm_std = np.append(self.multi_norm_std,float(y))

          #armazena coluna dos multipolos skew
          y = dados_l.split('\t')[3]
          y = y.replace(' ','')
          self.multi_skew = np.append(self.multi_skew,float(y))

          #armazena coluna do std dos multipolos skew
          y = dados_l.split('\t')[4]
          y = y.replace(' ','')
          self.multi_skew_std = np.append(self.multi_skew_std,float(y))

      #verifica qual posicao da coluna do angulo é não nula (qual ima foi medido) e armazena angulo e std do angulo
      self.ima = np.nonzero(ang_col)[0][0]
      self.ang = ang_col[self.ima]
      self.ang_std = ang_col_std[self.ima]
      
  ############ FIM DA IMPORTACAO DE DADOS DO TXT DA MEDIDA ############


  ############ CALCULO DOS MULTIPOLOS NORMAIS NORMALIZADOS E GRAFICO ###########
  def multi_norm_calc(self):
   
    self.multi_norm_normalized=np.array([])
    self.multi_norm_normalized_std=np.array([])
    self.n_multi_str=np.array([])

    self.bar_color = []
    y_lower = []
    y_lower_spec = []
    
    self.multi_normalized = 0
    self.multi_normalized_std = 0

    if self.count_file == 0:
      self.fig1, self.ax1 = plt.subplots()
      plt.grid()

    for m in self.n_multi:
        self.multi_normalized = self.multi_norm[m - 1] * self.r0 ** (m - 1) / (self.multi_norm[self.ima] * self.r0 ** self.ima)
        self.multi_norm_normalized = np.append(self.multi_norm_normalized, float(self.multi_normalized))

        self.multi_normalized_std = self.multi_norm_std[m - 1] * self.r0 ** (m-1) / (self.multi_norm[self.ima] * self.r0 ** self.ima)
        self.multi_norm_normalized_std = np.append(self.multi_norm_normalized_std, float(self.multi_normalized_std))
        self.n_multi_str = np.append(self.n_multi_str, str(self.n_multi[m - 1]))

        if self.multi_norm_normalized[m - 1] > 0: #positivo vermelho
          self.bar_color.append('r')
        else:
          self.bar_color.append('g')

        if self.spec_data[m - 1] == 0:
          self.spec_data[m - 1] = self.bottom_limit * 10 ** (-3)
          
        if self.sim_data[m - 1] == 0:
          self.sim_data[m - 1] = self.bottom_limit * 10 ** (-3)


    # posicao x da barra de especificacao e simulacao
    ind_spec=np.arange(m) + 1
    ind_sim=ind_spec+self.width

    # corrigindo o limite inferior das barras de erro da especificacao
    for i in self.n_multi: 
      if self.bottom_limit>(np.absolute(self.spec_data[i-1])-np.absolute(self.spec_data_std[i-1])):
        bottom_limit_= np.absolute(self.spec_data[i-1])
        y_lower_spec = np.append(y_lower_spec, bottom_limit_)
      else:
        y_lower_spec = np.append(y_lower_spec, np.absolute(self.spec_data_std[i-1]))
    
    # barras de especificacao e simulacao
    if self.count_file == 0:
      rects_spec = self.ax1.bar(ind_spec, np.absolute(self.spec_data), self.width, bottom=self.bottom_limit, color=self.bar_color, log='y', yerr=[y_lower_spec,self.spec_data_std], ecolor='b')
      rects_sim = self.ax1.bar(ind_sim, np.absolute(self.sim_data), self.width, bottom=self.bottom_limit, color=self.bar_color, log='y')
     
      self.ind = np.arange(m) + 1 + self.width * 2  # posicao x das barras de medicao
    else:
      self.ind = self.ind + self.width

    # corrigindo o limite inferior das barras de erro da medicao
    for i in self.n_multi: 
      if self.bottom_limit>(abs(self.multi_norm_normalized[i-1])-abs(self.multi_norm_normalized_std[i-1])):
        bottom_limit_=abs(self.multi_norm_normalized[i-1])
        y_lower = np.append(y_lower, bottom_limit_)
      else:
        y_lower = np.append(y_lower, abs(self.multi_norm_normalized_std[i-1]))

    # barras de medicao 
    self.rects1 = self.ax1.bar(self.ind, abs(self.multi_norm_normalized), self.width, bottom=self.bottom_limit, color=self.bar_color, log='y', yerr=[y_lower, abs(self.multi_norm_normalized_std)], ecolor='b')
           
    self.ax1.set_xlabel('$n$', fontsize=20)
    self.ax1.set_ylabel(r'$\frac{B_{N_n}}{B_{N_'+str(self.ima+1)+'}}(@'+str(self.r0*1000)+'$ ''$ mm)$', fontsize=30)
    self.ax1.set_title(self.nome_ima +' - '+self.date+' - Normal Integrated Multipoles Normalized', fontsize=20)
    
    if self.count_file == 0:
      self.ax1.set_xticks(self.ind+self.width*(self.n_file)/2) # posicao x dos ticks no centro do conjunto de barras
      self.autolabel_spec_sim(rects_spec, self.spec_data_std, 'E')
      self.autolabel_spec_sim(rects_sim, self.sim_data_std, 'S')

    if self.count_file == (round(self.n_file/2)):
      self.autolabel()

    self.ax1.set_xticklabels(self.n_multi_str, fontsize=14)
    
    for label in self.ax1.get_yticklabels():
        label.set_fontsize(14)

    if self.count_file == self.n_file - 1:
      self.name_fig = np.append(self.name_fig, self.ax1.get_title())

    self.ax1.text(0.8, 0.97, '\n E - Specification\n S - Simulation\n M - Measurement\n\n Red - Positive value\n Green - Negative value', verticalalignment='top', horizontalalignment='left',
        transform=self.ax1.transAxes, color='black', fontsize=20, bbox=dict(facecolor='white', edgecolor='black'))
      
  # nomeando o topo da barra de medicao central
  def autolabel(self):
      i=0
      for rect in self.rects1:
          height = rect.get_height()
          self.ax1.text(rect.get_x()+rect.get_width()/2., 1.1*(height+abs(self.multi_norm_normalized_std[i])),'M', ha='center', va='bottom', fontsize=13)
          i+=1
          
  # nomeando o topo da barra de especificacao e simulacao
  def autolabel_spec_sim(self,rects_spec_sim, spec_data_stds, labels):
      i=0
      for rect_spec_sim in rects_spec_sim:
          height = rect_spec_sim.get_height()
          self.ax1.text(rect_spec_sim.get_x()+rect_spec_sim.get_width()/2., 1.1*(height+abs(spec_data_stds[i])), labels, ha='center', va='bottom', fontsize=13)
          i+=1

    
  ############# FIM DO CALCULO DOS MULTIPOLOS NORMAIS NORMALIZADOS E GRAFICO #############


  ############ CALCULO DOS MULTIPOLOS SKEW NORMALIZADOS E GRAFICO ###########
  def multi_skew_calc(self):
   
    self.multi_skew_normalized=np.array([])
    self.multi_skew_normalized_std=np.array([])

    self.bar_color = []
    y_lower = []
    y_lower_spec = []

    spec_data_skew = np.ones(self.n_multi[-1]) * self.bottom_limit * 10 ** (-3)
    
    self.multi_normalized = 0
    self.multi_normalized_std = 0

    if self.count_file == 0:
      self.fig2, self.ax2 = plt.subplots()
      plt.grid()
      
    for m in self.n_multi:
        self.multi_normalized = self.multi_skew[m-1] * self.r0 ** (m-1) / (self.multi_norm[self.ima] * self.r0 ** self.ima)
        self.multi_skew_normalized = np.append(self.multi_skew_normalized, float(self.multi_normalized))

        self.multi_normalized_std = self.multi_skew_std[m-1] * self.r0 ** (m-1) / (self.multi_norm[self.ima] * self.r0 ** self.ima)
        self.multi_skew_normalized_std = np.append(self.multi_skew_normalized_std, float(self.multi_normalized_std))

        if self.multi_norm_normalized[m-1] > 0:
            self.bar_color.append('r')
        else:
            self.bar_color.append('g')


    # posicao x da barra de especificacao
    ind_spec=np.arange(m) + 1

    # corrigindo o limite inferior das barras de erro da especificacao
    for i in self.n_multi: 
      if self.bottom_limit>(np.absolute(spec_data_skew[i-1])-np.absolute(self.spec_data_skew_std[i-1])):
        bottom_limit_= np.absolute(spec_data_skew[i-1])
        y_lower_spec = np.append(y_lower_spec, bottom_limit_)
      else:
        y_lower_spec = np.append(y_lower_spec, np.absolute(self.spec_data_skew_std[i-1]))

    # barras de erro da especificacao
    if self.count_file == 0:
      rects_spec_skew = self.ax2.bar(ind_spec, spec_data_skew, self.width, bottom=self.bottom_limit, yerr= [y_lower_spec, np.absolute(self.spec_data_skew_std)], color=self.bar_color, log='y')
     
      self.ind2 = np.arange(m) + 1 + self.width  # posicao x das barras de medicao
    else:
      self.ind2 = self.ind2 + self.width

    # corrigindo o limite inferior das barras de erro da medicao
    for i in self.n_multi: 
      if self.bottom_limit>(abs(self.multi_skew_normalized[i-1])-abs(self.multi_skew_normalized_std[i-1])):
        bottom_limit_=abs(self.multi_skew_normalized[i-1])
        y_lower = np.append(y_lower, bottom_limit_)
      else:
        y_lower = np.append(y_lower, abs(self.multi_skew_normalized_std[i-1]))

    # barras de medicao 
    self.rects2 = self.ax2.bar(self.ind2, abs(self.multi_skew_normalized), self.width, bottom=self.bottom_limit, color=self.bar_color, log='y', yerr=[y_lower, abs(self.multi_skew_normalized_std)], ecolor='b')
            
    self.ax2.set_xlabel('$n$', fontsize=20)
    self.ax2.set_ylabel(r'$\frac{B_{S_n}}{B_{N_'+str(self.ima+1)+'}}(@'+str(self.r0*1000)+'$ ''$mm)$', fontsize=30)
    self.ax2.set_title(self.nome_ima +' - '+self.date+' - Skew Integrated Multipoles Normalized', fontsize=20)

    if self.count_file == 0:
      self.ax2.set_xticks(self.ind2+self.width*(self.n_file)/2) # posicao x dos ticks no centro do conjunto de barras
      self.autolabel_spec_sim_skew(rects_spec_skew, self.spec_data_skew_std, 'E')

    if self.count_file == (round(self.n_file/2)):
      self.autolabel_skew()

    self.ax2.set_xticklabels(self.n_multi_str, fontsize=14)
    
    for label in self.ax2.get_yticklabels():
        label.set_fontsize(14)

    if self.count_file == self.n_file - 1:
      self.name_fig = np.append(self.name_fig, self.ax2.get_title())

    self.ax2.text(0.8, 0.97, '\n E - Specification\n M - Measurement\n\n Red - Positive value\n Green - Negative value', verticalalignment='top', horizontalalignment='left',
        transform=self.ax1.transAxes, color='black', fontsize=20, bbox=dict(facecolor='white', edgecolor='black'))

  # nomeando o topo da barra de medicao central
  def autolabel_skew(self):
      i = 0
      for rect in self.rects2:
          height = rect.get_height()
          self.ax2.text(rect.get_x()+rect.get_width()/2., 1.1*(height+abs(self.multi_skew_normalized_std[i])),'M', ha='center', va='bottom', fontsize=13)
          i += 1
          
  # nomeando o topo da barra de especificacao
  def autolabel_spec_sim_skew(self,rects_spec_skew, spec_data_skew_stds, labels):
      i = 0
      for rect_spec_skew in rects_spec_skew:
          height = rect_spec_skew.get_height()
          if height != 0:
            self.ax2.text(rect_spec_skew.get_x()+rect_spec_skew.get_width()/2., 1.1*(height+abs(spec_data_skew_stds[i])), labels, ha='center', va='bottom', fontsize=13)
          i += 1

  ############# FIM DO CALCULO DOS MULTIPOLOS SKEW NORMALIZADOS E GRAFICO #############


  ############# CALCULO DO CAMPO RESIDUAL NORMALIZADO E GRAFICO #############
  def resid_norm_calc(self):

    B_resid_norm = np.array([])
    B_resid_sim_norm = np.array([])
    B_spec_resid_norm = np.array([])
    self.pos = np.array([])

    if self.count_file == 0:
      self.fig3, self.ax3 = plt.subplots()
      plt.grid()
      
    for i in range(int(self.rcb * 4) + 1):
        B_resid = 0
        B_resid_sim = 0
        B_spec_resid = 0
        
        y = (i/2 - self.rcb) / 1000
        self.pos = np.append(self.pos, y)

        for m in self.n_multi:
          if y != 0:
            B_resid += self.multi_norm[m - 1] * self.pos[i] ** (m - 1)
            z = (B_resid - self.multi_norm[self.ima] * self.pos[i] ** self.ima - self.multi_norm[0]) / (self.multi_norm[self.ima] * self.pos[i] ** self.ima)
            
            B_resid_sim += self.sim_data_multi[m - 1] * self.pos[i] ** (m - 1)
            w = (B_resid_sim - self.sim_data_multi[self.ima] * self.pos[i] ** self.ima) / (self.sim_data_multi[self.ima] * self.pos[i] ** self.ima)

            B_spec_resid += self.spec_data[m - 1] / self.r0 ** (m - self.ima + 1) * self.pos[i] ** (m - self.ima + 1) # calculo do campo residual a partir dos multipolos normalizados
          else:
            z = 0
            w = 0
            B_espec_resid = 0
            
        B_resid_norm = np.append(B_resid_norm, float(z))
        B_resid_sim_norm = np.append(B_resid_sim_norm, float(w))
        B_spec_resid_norm = np.append(B_spec_resid_norm, B_spec_resid)

    if self.count_file == 0:
      plt.plot(self.pos, B_resid_sim_norm, label = 'Simulation', linewidth=2.0)
      plt.plot(self.pos, B_spec_resid_norm, label = 'Specification', linewidth=2.0)
      
    plt.plot(self.pos, B_resid_norm, label = 'I = %.2f A'% self.corr_alim_princ, linewidth=2.0)
   
    plt.xlabel('Transversal self.position x [m]', fontsize=20)

    if self.ima == 0:
      plt.ylabel(r'$\frac{\sum_{n=1}^{'+self.n_multi_str[-1]+'}B_{N_n}}'+'{B_{N_'+str(self.ima+1)+'}}$', fontsize=30)
      plt.title(self.nome_ima +' - '+self.date+' - Homogeneity of the Normal Integrated Field', fontsize=20)
      
    if self.ima == 1:
      plt.ylabel(r'$\frac{\Delta B}{B} = \frac{\sum_{n=3}^{'+self.n_multi_str[-1]+'}B_{N_n}}'+'{B_{N_'+str(self.ima+1)+'}}$', fontsize=30)
      plt.title(self.nome_ima +' - '+self.date+' - Residual Normal Integrated Field Normalized', fontsize=20)
      
    if self.ima ==2:
      plt.ylabel(r'$\frac{\Delta B}{B} = \frac{\sum_{n=2-[n='+str(self.ima+1)+']}^{'+self.n_multi_str[-1]+'}B_{N_n}}'+'{B_{N_'+str(self.ima+1)+'}}$', fontsize=30)
      plt.title(self.nome_ima +' - '+self.date+' - Residual Normal Integrated Field Normalized', fontsize=20)

    plt.ticklabel_format(axis='both',style='sci',scilimits=(0,0))
    plt.rc('font', **{'size':'14'})
    
    for label in self.ax3.get_yticklabels():
      label.set_fontsize(14)

    for label in self.ax3.get_xticklabels():
      label.set_fontsize(14) 
      
    plt.legend(loc='upper center')

    if self.count_file == self.n_file - 1:
      self.name_fig = np.append(self.name_fig, self.ax3.get_title())  

  ############# FIM DO CALCULO DO CAMPO RESIDUAL NORMALIZADO E GRAFICO #############


  ############# CURVA DE EXCITACAO E SATURACAO #############
  def excit_calc(self):

    # pegando apenas a componente principal
    self.B_excit = np.append(self.B_excit, self.multi_norm[self.ima])
    self.B_excit_std = np.append(self.B_excit_std, self.multi_norm_std[self.ima])
    self.corr_alim_princ_arr = np.append(self.corr_alim_princ_arr, self.corr_alim_princ)
    self.corr_alim_princ_arr_std = np.append(self.corr_alim_princ_arr_std, self.corr_alim_princ_std)

    if self.count_file == self.n_file - 1:
      self.fig4, ax4 = plt.subplots()
      plt.grid()

      # criando curva de excitacao
      p1, = plt.plot(self.sim_corr_sat, self.sim_data_sat, marker ='^',markersize=3, linewidth=2.0)
      p2 = ax4.errorbar(self.corr_alim_princ_arr, self.B_excit, xerr=self.corr_alim_princ_arr_std, yerr=self.B_excit_std, marker ='o',markersize=3, linewidth=2.0)

      # calculando ajuste linear
      params_sim = np.polyfit(self.sim_corr_sat, self.sim_data_sat, 1)
      [a_sim, b_sim] = params_sim
      self.B_excit_ajust_sim = a_sim * self.sim_corr_sat + b_sim
      p3, = plt.plot(self.sim_corr_sat, self.B_excit_ajust_sim, '-y', linewidth=1.0)
      
      params = np.polyfit(self.corr_alim_princ_arr, self.B_excit, 1)
      [a, b] = params
      self.B_excit_ajust = a * self.corr_alim_princ_arr + b
      p4, = plt.plot(self.corr_alim_princ_arr, self.B_excit_ajust, '-r', linewidth=1.0)
     
      # colocando dados do ajuste no grafico
      if self.ima == 0:
        ax4.text(0.02, 0.97, '\n Integrated Field = A * Excitation Current + B \n\n Curve Fitting Line - Simulation \n A = %.4e\n B = %.4e\n\n Curve Fitting Line - Measurement \n A = %.4e\n B = %.4e\n' % (a_sim, b_sim, a, b), verticalalignment='top', horizontalalignment='left',
        transform=ax4.transAxes, color='black', fontsize=20, bbox=dict(facecolor='white', edgecolor='black'))
      if self.ima == 1:
        ax4.text(0.02,.97,'\n Integrated Gradient = A * Excitation Current + B \n\n Curve Fitting Line - Simulation \n A = %.4e\n B = %.4e\n\n Curve Fitting Line - Measurement \n A = %.4e\n B = %.4e\n' % (a_sim, b_sim, a, b), verticalalignment='top', horizontalalignment='left',
        transform=ax4.transAxes, color='black', fontsize=20, bbox=dict(facecolor='white', edgecolor='black'))
      if self.ima == 2:
        ax4.text(0.02, 0.97, '\n Integrated Gradient = A * Excitation Current + B \n\n Curve Fitting Line - Simulation \n A = %.4e\n B = %.4e\n\n Curve Fitting Line - Measurement \n A = %.4e\n B = %.4e\n' % (a_sim, b_sim, a, b), verticalalignment='top', horizontalalignment='left',
        transform=ax4.transAxes, color='black', fontsize=20, bbox=dict(facecolor='white', edgecolor='black'))
       
      plt.xlabel('Excitation Current [A]', fontsize=20)
      
      if self.ima == 1:
        plt.ylabel('$N_{'+str(self.ima+1)+'}$ [T]', fontsize=30)
      elif self.ima == 2:
        plt.ylabel('$N_{'+str(self.ima+1)+'}$ [T/m]', fontsize=30)
      else:
        plt.ylabel('$N_{'+str(self.ima+1)+'}$ [T.m]', fontsize=30)

      plt.title(self.nome_ima +' - '+self.date+' - Excitation Curve', fontsize=20)

      plt.legend([p1, p2, p3, p4],['Simulation', 'Measurement', 'Simulation Adjust', 'Measurement Adjust'], loc='lower right')

      for label in ax4.get_yticklabels():
        label.set_fontsize(14)

      for label in ax4.get_xticklabels():
        label.set_fontsize(14)

      self.fig5, ax5 = plt.subplots()
      plt.grid()

      # calculando curva de saturacao
      self.B_excit_resid_sim = (self.sim_data_sat - self.B_excit_ajust_sim) / self.sim_data_sat * 100
      sim_corr_sat_ = self.sim_corr_sat
      
      self.B_excit_resid = (self.B_excit - self.B_excit_ajust) / self.B_excit * 100
      self.corr_alim_princ_arr_sat = np.delete(self.corr_alim_princ_arr,0)
      
      # eliminando primeiro ponto da curva de saturacao
      self.B_excit_resid_sim_sat = self.B_excit_resid_sim
      plt.plot(sim_corr_sat_, self.B_excit_resid_sim_sat, marker='^', color='b', label = 'Simulation', linewidth=2.0)
      
      self.B_excit_resid_sat = np.delete(self.B_excit_resid,0)
      plt.plot(self.corr_alim_princ_arr_sat, self.B_excit_resid_sat, marker='o', color='r',  label = 'Measurement', linewidth=2.0)

      plt.xlabel('Excitation Current [A]', fontsize=20)

      plt.ylabel(r'$\frac{N_{'+str(self.ima+1)+'} - N_{'+str(self.ima+1)+'_{Adjusted}}}{N_{'+str(self.ima+1)+'_{Adjusted}}}$'' [%]', fontsize=30)

      plt.title(self.nome_ima +' - '+self.date+' - Saturation Curve', fontsize=20)
     
      for label in ax5.get_yticklabels():
        label.set_fontsize(14)

      for label in ax5.get_xticklabels():
        label.set_fontsize(14)

      plt.legend(loc='upper right')
      
      if self.count_file == self.n_file - 1:
        self.name_fig = np.append(self.name_fig, ax4.get_title())
        self.name_fig = np.append(self.name_fig, ax5.get_title())

  ############# FIM DA CURVA DE EXCITACAO E SATURACAO #############


  ############# CURVA DE ANGULO #############
  def ang_calc(self):
   
    # pegando o angulo
    self.ang_arr = np.append(self.ang_arr, self.ang * 1000)
    self.ang_arr_std = np.append(self.ang_arr_std, self.ang_std * 1000)

    if self.count_file == self.n_file - 1:
      self.fig6, ax6 = plt.subplots()
      plt.grid()
    
      # criando curva de excitacao
      ax6.errorbar(self.corr_alim_princ_arr, self.ang_arr, marker='o', color='r', linewidth=2.0, xerr=self.corr_alim_princ_arr_std, yerr=self.ang_arr_std, ecolor='b', elinewidth=1.0)
    
      plt.xlabel('Excitation Current [A]', fontsize=20)
      plt.ylabel('$n^{-1} * atan(S_'+str(self.ima+1)+'/N_'+str(self.ima+1)+')$'' [mrad]', fontsize=20)
      plt.title(self.nome_ima +' - '+self.date+' - Angle', fontsize=20)

      for label in ax6.get_yticklabels():
        label.set_fontsize(14)

      for label in ax6.get_xticklabels():
        label.set_fontsize(14)

      if self.count_file == self.n_file - 1:
        self.name_fig = np.append(self.name_fig, ax6.get_title())

  ############# FIM DA CURVA DE ANGULO #############


  ############# TABELA #############
  def tabela(self):

    table_matrix=[]

    colLabels = (r'$n$', '$N_n$'' $[T.m^{(2-n)}]$', '$Err - N_n$'' $[T.m^{(2-n)}]$', '$S_n$'' $[T.m^{(2-n)})]$', '$Err - S_n$'' $[T.m^{(2-n)}]$')
    
    for i in range(self.n_multi[-1]+1):
      if i == 0:
        table = np.zeros(5)
      else:
        table = ['%d' % self.n_multi[i-1], '%.4e' % self.multi_norm[i-1], '%.4e' % self.multi_norm_std[i-1], '%.4e' % self.multi_skew[i-1], '%.4e' % self.multi_skew_std[i-1]]
      table_matrix.append(table)

    scale_h=2.7
    colWidths=[.1,.2,.2,.2,.2]

    nrows, ncols = len(table_matrix)+1, len(colLabels)
    hcell, wcell = 0.2, 3.5
    hpad, wpad = 0, 0    
    self.fig7 = plt.figure(figsize=(ncols*wcell+wpad, (nrows*hcell+hpad)*scale_h))
    ax7 = self.fig7.add_subplot(111)
    ax7.axis('off')

    the_table = ax7.table(cellText=table_matrix , colWidths=colWidths, colLabels=colLabels, colColours=['w', 'w', 'w', 'w', 'w'], loc='center', cellLoc='center')
    
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(20)
    
    # ajustando escala  da figura e tabela
    the_table.scale(1, scale_h)
    ax7.set_title(self.nome_ima +' - '+self.date+'- Normal and Skew Integrated Multipoles - Current - %.2f A' % self.corr_alim_princ, fontsize=20)

    if self.count_file == self.n_file - 1:
        self.name_fig = np.append(self.name_fig, ax7.get_title())

  ############# FIM DA TABELA #############


  ############# FUNCAO PRINCIPAL #############
  def main(self):

    self.bottom_limit = 10**(-6)
    self.width = 0.07 # largura das barras dos grafico

    files_info = self.directory('.dat')
    self.n_file = files_info[0] # numero de arquivos .dat
    path_abs1_all = files_info[1] # nome dos arquivos .dat

    self.B_excit = []
    self.B_excit_std = [] 
    self.corr_alim_princ_arr = []
    self.corr_alim_princ_arr_std = []
    self.ang_arr = []
    self.ang_arr_std = []
    self.name_fig = []


    for self.count_file in range(self.n_file):
      self.import_data (self.path1 + path_abs1_all[self.count_file])

      if self.ima == 0: # corretora horizontal sobre retas, especificacao homogeneidade 1/300 em +/- 15 mm (sobre trajetorias)
        self.rcb = 15
        self.r0 = 15
        self.r0 = self.r0 / 1000
        
        self.sim_data =            [0,                0,  3.06401*10**(-3),  0,  -1.27331*10**(-3),  0,  -1.70843*10**(-3),  0,  -1.14341*10**(-4),  0,  2.32739*10**(-4),  0,  -7.11864*10**(-5),  0,  8.59749*10**(-6)]
        self.spec_data =           [0,                0,  0,                 0,  0,                  0,  0,                  0,  0,                  0,  0,                 0,  0,                  0,  0               ]
        self.spec_data_skew_std =  [0,                0,  0,                 0,  0,                  0,  0,                  0,  0,                  0,  0,                 0,  0,                  0,  0               ]
        self.spec_data_std =       [0,                0,  0,                 0,  0,                  0,  0,                  0,  0,                  0,  0,                 0,  0,                  0,  0               ]
        self.sim_data_multi =      [3.02946*10**(-3), 0,  4.12547*10**(-2),  0,  -7.61962*10**(1),   0,  -4.54377*10**(5),   0,  -1.35157*10**(8),   0,  1.22271*10**(12),  0,  -1.66214*10**(15),  0,  8.92194*10**(17)]

        self.sim_data_sat =                 [1.50754*10**(-3), 3.02946*10**(-3)]
        self.sim_corr_sat =        np.array([4.5,              9               ])

      if self.ima == 1: # quadrupolo defocalizador
        self.rcb = 17.5
        self.r0 = 17.5
        self.r0 = self.r0 / 1000
        
        self.sim_data =            [0, 0,         0,              0,              0,              -1.0431*10**(-3), 0,              0,              0,              1.18022*10**(-3), 0,              0,              0,              2.76057*10**(-5), 0]
        self.spec_data =           [0, 0,         0,              0,              0,              -1.0000*10**(-3), 0,              0,              0,              1.10*10**(-3),    0,              0,              0,              8.00*10**(-5),    0]
        self.spec_data_skew_std =  [0, 0,         1.00*10**(-4),  5.00*10**(-4),  1.00*10**(-4),  1.00*10**(-4),    1.00*10**(-4),  1.00*10**(-4),  1.00*10**(-4),  1.00*10**(-4),    1.00*10**(-4),  1.00*10**(-4),  1.00*10**(-4),  1.00*10**(-4),    0]
        self.spec_data_std =       [0, 0,         7.00*10**(-4),  4.00*10**(-4),  4.00*10**(-4),  4.00*10**(-4),    4.00*10**(-4),  4.00*10**(-4),  4.00*10**(-4),  4.00*10**(-4),    4.00*10**(-4),  4.00*10**(-4),  4.00*10**(-4),  4.00*10**(-4),    0]
        self.sim_data_multi =      [0, 4.69579,  0,              0,              0,              -5.22255*10**(4), 0,              0,              0,              6.30039*10**(11), 0,              0,              0,              1.57127*10**(17), 0]

        self.sim_data_sat =                 [7.40767*10**(-1), 2.03711, 2.35045, 2.96292, 4.07253, 4.69579]
        self.sim_corr_sat =        np.array([20,               55,      63.46,   80,      110,     126.92 ])
        
      if self.ima == 2: # sextupolo focalizador
        self.rcb = 17.5
        self.r0 = 17.5
        self.r0 = self.r0 / 1000
        
        self.sim_data =            [0, 0, 0,              0,              0,              0,                 0,              0,                -3.35214*10**(-2),    0,                  0,                0,                0,                0,                -9.11223*10**(-3)]
        self.spec_data =           [0, 0, 0,              0,              0,              0,                 0,              0,                -2.40*10**(-2),       0,                  0,                0,                0,                0,                -1.70*10**(-2)   ]
        self.spec_data_skew_std =  [0, 0, 0,              1.00*10**(-4),  1.00*10**(-4),  1.00*10**(-4),     1.00*10**(-4),  1.00*10**(-4),    1.00*10**(-4),        1.00*10**(-4),      1.00*10**(-4),    1.00*10**(-4),    1.00*10**(-4),    1.00*10**(-4),    0                ]
        self.spec_data_std =       [0, 0, 0,              4.00*10**(-4),  4.00*10**(-4),  4.00*10**(-4),     4.00*10**(-4),  4.00*10**(-4),    4.00*10**(-4),        4.00*10**(-4),      4.00*10**(-4),    4.00*10**(-4),    4.00*10**(-4),    4.00*10**(-4),    0                ]
        self.sim_data_multi =      [0, 0, -23.10300,      0,              0,              0,                 0,              0,                2.69627*10**(10),     0,                  0,                0,                0,                0,                2.55174*10**(20) ]

        self.sim_data_sat =                 [-9.95802, -11.5278, -19.9160]
        self.sim_corr_sat =        np.array([4.06,     4.7,      8.12    ])
        
      self.sim_data_std = np.zeros(self.n_multi[-1]) # nenhum erro para dados simulados

      self.multi_norm_calc()
      self.multi_skew_calc()
      self.resid_norm_calc()
      self.excit_calc()
      self.ang_calc()
      
    self.tabela()

    # salva figuras na mesma pasta dos arquivos .dat
    fig = [self.fig1, self.fig2, self.fig3, self.fig4, self.fig5, self.fig6, self.fig7]

    for k in range (7):
      fig[k].savefig(self.path1+self.name_fig[k]+'.png')


    plt.show()

 ############# FIM DA FUNCAO PRINCIPAL #############   

a=interface()










    


        
    

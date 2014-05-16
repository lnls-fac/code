# Lembretes: 

# Bobina girante v2.0

import sys
import time
import threading
import numpy
import matplotlib.pyplot as plt
import Display_Heidenhain
import Parker_Drivers
import FDI2056
import PUC_2v5
from PyQt4 import QtCore, QtGui
from interface import Ui_InterfaceBobina



# ____________________________________________
# Biblioteca de variaveis globais utilizadas
class lib(object):
    def __init__(self):
        self.display = 0            # Display Heidenhain
        self.motor = 0              # Driver do motor
        self.integrador = 0         # Integrador
        self.Janela = 0
        self.endereco = 2
        self.stop = 0
        self.posicao = [0,0]
        self.kill = 0
        self.pontos = []
        self.pontos_recebidos = []
        self.parartudo = 0
        self.media = 0
        self.F = 0
        self.ganho = 0
        self.pontos_integracao = 0
        self.pulsos_encoder = 0
        self.pulsos_trigger = 0
        self.voltas_offset = 0
        self.volta_filtro = 0
        self.SJN = numpy.zeros(21)
        self.SKN = numpy.zeros(21)
        self.SNn = numpy.zeros(21)
        self.SNn2 = numpy.zeros(21)
        self.SSJN2 = numpy.zeros(21)
        self.SSKN2 = numpy.zeros(21)
        self.SdbdXN = numpy.zeros(21)
        self.SdbdXN2 = numpy.zeros(21)
        self.Nn = numpy.zeros(21)
        self.Sn = numpy.zeros(21)
        self.Nnl = numpy.zeros(21)
        self.Snl = numpy.zeros(21)
        self.sDesv = numpy.zeros(21)
        self.sDesvNn = numpy.zeros(21)
        self.sDesvSn = numpy.zeros(21)
        self.angulo = numpy.zeros(21)
        self.SMod = numpy.zeros(21)
        self.AnguloVolta = []
        self.procura_indice_flag = 1
        self.velocidade = 0
        self.acaleracao = 0
        self.sentido = 0
        self.passos_volta = 50000
        self.alpha = 0
        self.Bucked = 0
        self.PUC = 0
        self.Ciclos_Puc = 0
        self.LeituraCorrente = 0
        self.FileName = 0
        self.Motor_Posicao = 0
        
        
lib = lib()
# ____________________________________________



# ____________________________________________
# Biblioteca de constantes utilizadas
class constantes(object):
    def __init__(self):
        self.numero_de_abas = 9                                 # Numero de abas da janela grafica
        self.ganhos = [1, 2, 5, 10, 20, 50, 100]                # Ganhos disponiveis para o integrador
        self.p_integracao = [16, 32, 64, 128, 256, 512]         # Numero de pontos de integracao disponiveis
        self.passos_mmA = 25000                                 # Numero de passos por mm
        self.passos_mmB = 25000                                 # Numero de passos por mm
        self.motorA_endereco = 3                                # Endereco do motor A
        self.motorB_endereco = 4                                # Endereco do motor B
        self.motorC_endereco = 2
        self.avancoA = 0
        self.avancoB = 0
        self.avancoC = 0
        self.zeroA = -108.310
        self.zeroB = -107.270
        self.pos_ang = 0
        self.pos_long = 0
        self.pos_ver = 0
        self.pos_trac = 0
        self.Clock_Puc = 4000                                   #Clock interno da PUC
        self.Pontos_Puc = 32768                                 #Número de pontos da Memória PUC

const = constantes()
# ____________________________________________



# ____________________________________________
# Definicao de todas as funcionalidades do programa ordenadas por abas
class JanelaGrafica(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(JanelaGrafica,self).__init__(parent)
        self.ui = Ui_InterfaceBobina()
        self.ui.setupUi(self)
        self.sinais()

    def sinais(self):
        for i in range(1,const.numero_de_abas):
            self.ui.tabWidget.setTabEnabled(i,False)
        self.ui.conectar.clicked.connect(self.CONECTAR)
        self.ui.zerar.clicked.connect(self.ZERAR)
        self.ui.ligar.clicked.connect(self.LIGARMOTOR)
        self.ui.parar.clicked.connect(self.PARARMOTOR)
        self.ui.configurar_integrador.clicked.connect(self.Start_Config)
        self.ui.ler_encoder.clicked.connect(self.LERENCODER)
        self.ui.MoverA.clicked.connect(self.MOVER_A)
        self.ui.MoverB.clicked.connect(self.MOVER_B)
        self.ui.Mover_2.clicked.connect(self.MOVER2)
        self.ui.Kill.clicked.connect(self.KILL)
        self.ui.Ref.clicked.connect(self.ENCONTRA_REF)
        self.ui.bobinadesmontada.toggled.connect(self.BOBINADESMONTADA)
        self.ui.ProcuraIndice.clicked.connect(self.ProcuraIndiceEncoder)
        self.ui.coletar.clicked.connect(self.COLETA_INTEGRADOR)
        self.ui.PararTudo.clicked.connect(self.PARAR_TUDO)
        self.ui.salvar_harmonico.clicked.connect(self.Salvar_Coletas)
        self.ui.posicionar.clicked.connect(self.POSICIONAR)
        self.ui.salvar_config.clicked.connect(self.SALVAR_DEFAULT)
        self.ui.ConfGeral.clicked.connect(self.CONFGERAL)
        self.ui.salvar_config_2.clicked.connect(self.SALVAR_DEFAULT)
        self.ui.Ciclar.clicked.connect(self.Ciclagem)
        self.ui.Plota.clicked.connect(self.Plotar_Curva)
        self.ui.EnviaCurva.clicked.connect(self.Enviar_Curva)
        self.ui.BobinaL.clicked.connect(self.CARREGABOBINA)
        self.ui.BobinaS.clicked.connect(self.SALVABOBINA)
        self.ui.montar.clicked.connect(self.MONTAR)
        self.ui.desmontar.clicked.connect(self.DESMONTAR)
        self.ui.ligar_fonte.clicked.connect(self.Start_Fonte)
        self.ui.Corrente_Atual.clicked.connect(self.Corrente_Fonte)
        self.ui.Enviar_Linear.clicked.connect(self.Rampa_Corrente_Manual)
        self.ui.Carregar_Config_Fonte.clicked.connect(self.Carregar_Fonte)
        self.ui.Salvar_Config_Fonte.clicked.connect(self.Salvar_Fonte)
        self.ui.Chk_Auto.toggled.connect(self.Hab_Auto)
        self.ui.Chk_Senoidal_Ponto.toggled.connect(self.Hab_Ponto)
        self.ui.C_Sucessivas.toggled.connect(self.Coleta_Suc_Manual)
        self.ui.posicaoA.setText('0')
        self.ui.posicaoB.setText('0')
        self.ui.velocidade_2.setText('3')
        self.ui.velocidade_2.editingFinished.connect(self.velocidade_2_Change)
        self.ui.groupBox_6.setEnabled(False)
        self.ui.velocidade.setText('1')
        self.ui.aceleracao.setText('1')
        self.ui.voltas.setText('1')
        self.ui.status.setText('Pronto')
        self.load_default()

    def load_default(self):
        try:
            f = open('default_settings.dat','r')
        except:
            print('arquivo inexistente')
            return
        config = f.read().split('\n\n')
        f.close()
        for i in range(len(config)):
            config[i]=config[i].split('\n')
            for j in range(len(config[i])):
                config[i][j]=config[i][j].split('\t')
        self.ui.Porta.setCurrentIndex(int(config[1][0][1])-1)
        self.ui.Porta_2.setCurrentIndex(int(config[1][1][1])-1)
        self.ui.Porta_3.setCurrentIndex(int(config[1][2][1])-1)
        self.ui.Porta_4.setCurrentIndex(int(config[1][3][1])-1)
        self.ui.Enderac_PUC.setValue(int(config[1][4][1]))
        self.ui.EndDriver.setCurrentIndex(int(config[2][0][1])-1)
        self.ui.ganho.setCurrentIndex(int(config[2][1][1]))
        self.ui.pontos_integracao.setCurrentIndex(int(config[2][2][1]))
        self.ui.pulsos_encoder.setText(config[2][3][1])
        self.ui.pulsos_trigger.setText(config[2][4][1])
        self.ui.velocidade_int.setText(config[2][5][1])
        self.ui.aceleracao_int.setText(config[2][6][1])
        self.ui.voltas_offset.setText(config[2][7][1])
        self.ui.filtro_voltas.setText(config[2][8][1])
        lib.passos_volta = int(config[2][9][1])
        self.ui.EndDriver_A.setCurrentIndex(int(config[4][0][1])-1)
        self.ui.EndDriver_B.setCurrentIndex(int(config[4][1][1])-1)
        self.ui.EndDriver_C.setCurrentIndex(int(config[4][2][1])-1)
        self.ui.sentido_A.setCurrentIndex(int(config[4][3][1]))
        self.ui.sentido_B.setCurrentIndex(int(config[4][4][1]))
        self.ui.sentido_C.setCurrentIndex(int(config[4][5][1]))
        self.ui.indice_A.setText(config[4][6][1])
        self.ui.indice_B.setText(config[4][7][1])
        self.ui.pos_ang.setText(config[4][8][1])
        self.ui.pos_long.setText(config[4][9][1])
        self.ui.pos_ver.setText(config[4][10][1])
        self.ui.pos_trac.setText(config[4][11][1])
        lib.endereco = config[2][0][1]
        self.CONFGERAL()

    ########### ABA 1: Conexao ###########

    def CONECTAR(self):        
        if (self.ui.conectar.text() == 'Conectar'):

            lib.stop = 0
            try:            
                lib.display = Display_Heidenhain.SerialCom(self.ui.Porta.currentIndex() + 1)
                lib.display.Conectar()
            except:
                QtGui.QMessageBox.critical(self,'Erro.','Porta serial ocupada ou inexistente.',QtGui.QMessageBox.Ok)
                return
            try:
                lib.motor = Parker_Drivers.SerialCom(self.ui.Porta_2.currentIndex() + 1)
                lib.motor.Conectar()
            except:
                QtGui.QMessageBox.critical(self,'Erro.','Porta serial ocupada ou inexistente.',QtGui.QMessageBox.Ok)
                lib.display.Desconectar()
                return
            try:
                lib.integrador = FDI2056.SerialCom(self.ui.Porta_3.currentIndex() + 1)
                lib.integrador.Conectar()
            except:
                QtGui.QMessageBox.critical(self,'Erro.','Porta serial ocupada ou inexistente.',QtGui.QMessageBox.Ok)
                lib.display.Desconectar()
                lib.motor.Desconectar()
                return
            try:
                Address = self.ui.Enderac_PUC.text()
                lib.PUC = PUC_2v5.SerialCom(Address)

                if (lib.PUC.Conectar(self.ui.Porta_4.currentIndex() + 1) == False):
                    QtGui.QMessageBox.critical(self,'Erro.','Porta serial ocupada/inexistente ou\nPUC não Conectada.',QtGui.QMessageBox.Ok)
                    for i in range(1,const.numero_de_abas-1):
                        self.ui.tabWidget.setTabEnabled(i,True)
                    self.ui.tabWidget.setTabEnabled(3,False)
                    self.ui.conectar.setText('Desconectar')
                    self.ui.Porta.setEnabled(False)
                    self.ui.Porta_2.setEnabled(False)
                    self.ui.Porta_3.setEnabled(False)
                    return
            except:
                return
            
            for i in range(1,const.numero_de_abas-1):
                self.ui.tabWidget.setTabEnabled(i,True)
            
            self.ui.conectar.setText('Desconectar')
            self.ui.Porta.setEnabled(False)
            self.ui.Porta_2.setEnabled(False)
            self.ui.Porta_3.setEnabled(False)
            self.ui.Porta_4.setEnabled(False)
            self.ui.Enderac_PUC.setEnabled(False)
                        
        else:
            lib.stop = 1
            lib.display.Desconectar()
            lib.motor.Desconectar()
            lib.integrador.Desconectar()
            
            for i in range(1,const.numero_de_abas):
                self.ui.tabWidget.setTabEnabled(i,False)

            self.ui.Porta.setEnabled(True)
            self.ui.Porta_2.setEnabled(True)
            self.ui.Porta_3.setEnabled(True)
            self.ui.Porta_4.setEnabled(True)
            self.ui.Enderac_PUC.setEnabled(True)
            self.ui.conectar.setText('Conectar')

            try:
                lib.PUC.Desconectar()
            except:
                return

            
    ########### ABA 2: Configuracoes Gerais ###########

    def CONFGERAL(self):
        const.motorA_endereco = self.ui.EndDriver_A.currentIndex() + 1
        const.motorB_endereco = self.ui.EndDriver_B.currentIndex() + 1
        const.motorC_endereco = self.ui.EndDriver_C.currentIndex() + 1
        const.avancoA = self.ui.sentido_A.currentIndex()
        const.avancoB = self.ui.sentido_B.currentIndex()
        const.avancoC = self.ui.sentido_C.currentIndex()
        const.zeroA = float(self.ui.indice_A.text())
        const.zeroB = float(self.ui.indice_B.text())
        const.pos_ang = int(self.ui.pos_ang.text())
        const.pos_long = float(self.ui.pos_long.text())
        const.pos_ver = int(self.ui.pos_ver.text())
        const.pos_trac = float(self.ui.pos_trac.text())

    ########### ABA 3: Mesas Transversais ###########

    def velocidade_2_Change(self):
        try:
            aux = float(self.ui.velocidade_2.text())
            if aux > 5:
                QtGui.QMessageBox.warning(self,'Atenção.','Velocidade muito alta.',QtGui.QMessageBox.Ok)
                self.ui.velocidade_2.setText('5')
            if aux < 0:
                QtGui.QMessageBox.warning(self,'Atenção.','Velocidade muito baixa.',QtGui.QMessageBox.Ok)
                self.ui.velocidade_2.setText('1')
        except:
            QtGui.QMessageBox.warning(self,'Atenção.','Valor não Numérico.',QtGui.QMessageBox.Ok)
            self.ui.velocidade_2.setText('3')

    def BOBINADESMONTADA(self):
        if self.ui.bobinadesmontada.isChecked():
            self.ui.groupBox_6.setEnabled(True)
            self.ui.groupBox_4.setEnabled(False)
            QtGui.QMessageBox.warning(self,'Atenção.','Verifique se a bobina está desmontada.',QtGui.QMessageBox.Ok)
        else:
            self.ui.groupBox_6.setEnabled(False)
            self.ui.groupBox_4.setEnabled(True)

    def ENCONTRA_REF(self):
        ret = QtGui.QMessageBox.question(self,'Referência.','Deseja Referenciar o Sistema?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if ret == QtGui.QMessageBox.Yes:
            self.ui.zerar.setEnabled(False)
            EncontraRef()
        else:
            return
  

    def MOVER_A(self):
        try:
            posicaoA = float(self.ui.posicaoA.text())
        except:
            QtGui.QMessageBox.critical(self,'Atenção.','Valor não é um número.',QtGui.QMessageBox.Ok)
            return
        self.ui.groupBox_6.setEnabled(False)
        self.ui.zerar.setEnabled(False)
        self.ui.bobinadesmontada.setEnabled(False)
        self.Mover_Motor_A(posicaoA,float(self.ui.velocidade_2.text()))

    def Mover_Motor_A(self,posicaoA,velocidade):
        lib.display.LerDisplay()
        lib.posicao = lib.display.DisplayPos
        posicaoB = float(lib.posicao[1])
        motortransversal(posicaoA, posicaoB, velocidade)       

    def MOVER_B(self):
        try:
            posicaoB = float(self.ui.posicaoB.text())
        except:
            QtGui.QMessageBox.critical(self,'Atenção.','Valor não é um número.',QtGui.QMessageBox.Ok)
            return
        self.ui.groupBox_6.setEnabled(False)
        self.ui.zerar.setEnabled(False)
        self.ui.bobinadesmontada.setEnabled(False)
        self.Mover_Motor_B(posicaoB,float(self.ui.velocidade_2.text()))

    def Mover_Motor_B(self,posicaoB,velocidade):
        lib.display.LerDisplay()
        lib.posicao = lib.display.DisplayPos
        posicaoA = float(lib.posicao[0])
        motortransversal(posicaoA, posicaoB, velocidade)

    

    def MOVER2(self):
        try:
            posicao = float(self.ui.posicao_bobina_montada.text())
        except:
            QtGui.QMessageBox.critical(self,'Atenção.','Valor não é um número.',QtGui.QMessageBox.Ok)
            return
        self.ui.groupBox_4.setEnabled(False)
        self.ui.zerar.setEnabled(False)
        self.ui.bobinadesmontada.setEnabled(False)
        if posicao > 1:
            posicao = 1
            self.ui.posicao_bobina_montada.setText('1')
        elif posicao < -1:
            posicao = -1
            self.ui.posicao_bobina_montada.setText('-1')
        motortransversal(posicao, posicao)
        
    def KILL(self):
        lib.parartudo = 1
        time.sleep(0.5)
        lib.motor.Kill()
        time.sleep(5)
        lib.parartudo = 0
    
    def ZERAR(self):
        lib.stop = 1
        time.sleep(1)
        lib.display.EscreveValorDisplay(0, 0)
        lib.display.EscreveValorDisplay(1, 0)
        lib.stop = 0
##        self.xyx = eixos()


    ########### ABA 4: Fonte (PUC_2v5) ###########

    def Start_Fonte(self):
        if (self.ui.ligar_fonte.text() == 'Ligar'):
            status = lib.PUC.ReadDigIn()
            if dec_bin(status,6) == 1:
                QtGui.QMessageBox.critical(self,'Atenção.','Interlock Externo da Fonte Acionado.',QtGui.QMessageBox.Ok)
                return
            if dec_bin(status,5) == 1:
                QtGui.QMessageBox.critical(self,'Atenção.','Interlock Interno da Fonte Acionado.',QtGui.QMessageBox.Ok)
                return
            status = lib.PUC.WriteDigBit(0,1)
            if status == True:
                time.sleep(0.5)
                status = lib.PUC.ReadDigIn()
                if dec_bin(status,7) == 1:
                    self.ui.ligar_fonte.setText('Desligar')
                    self.ui.status_fonte.setText('Ligada')
                    self.ui.Corrente_Atual.setEnabled(True)
                    self.ui.groupBox_5.setEnabled(True)
                else:
                    status = lib.PUC.WriteDigBit(0,1)
                    time.sleep(0.5)
                    status = lib.PUC.ReadDigIn()
                    if dec_bin(status,7) == 1:
                        self.ui.ligar_fonte.setText('Desligar')
                        self.ui.status_fonte.setText('Ligada')
                        self.ui.Corrente_Atual.setEnabled(True)
                        self.ui.groupBox_5.setEnabled(True)
                    else:
                        QtGui.QMessageBox.critical(self,'Atenção.','Fonte Não Ligou.',QtGui.QMessageBox.Ok)
                        return
            else:
                QtGui.QMessageBox.critical(self,'Atenção.','PUC Não recebeu o comando.',QtGui.QMessageBox.Ok)
                return
        else:
            status = lib.PUC.WriteDigBit(0,0)
            if status == True:
                self.ui.ligar_fonte.setText('Ligar')
                self.ui.status_fonte.setText('Desligada')
                self.ui.Corrente_Atual.setEnabled(False)
                self.ui.groupBox_5.setEnabled(False)
            else:
                QtGui.QMessageBox.critical(self,'Atenção.','PUC Não recebeu o comando.',QtGui.QMessageBox.Ok)
                return
            

    def Salvar_Fonte(self):
        try:
            arquivo = QtGui.QFileDialog.getSaveFileName(self, 'Save File', '.','Data files (*.dat);;Text files (*.txt)')
        except:
            return

        try:
            nome = str(self.ui.Nome_Fonte.text())
            C_Linear = str(float(self.ui.Corrente_Linear.text()))
            Amp_Linear = str(float(self.ui.Amplitude_Linear.text()))
            T_Linear = str(float(self.ui.Tempo_Linear.text()))
            C_Inicial = str(float(self.ui.Corrente_Auto_Inicial.text()))
            C_Final = str(float(self.ui.Corrente_Auto_Final.text()))
            N_Corrente = str(int(self.ui.N_Correntes_Auto.text()))
##            Amp_Auto = str(float(self.ui.Amplitude_Auto.text()))
##            T_Auto = str(float(self.ui.Tempo_Auto.text()))
            Amp_Sen = str(float(self.ui.Amplitude_Senoidal.text()))
            Off_Sen = str(float(self.ui.Offset_Senoidal.text()))
            P_I_Sen = str(float(self.ui.Pico_Inferior_Senoidal.text()))
            P_S_Sen = str(float(self.ui.Pico_Superior_Senoidal.text()))
            C_F_Sen = str(float(self.ui.Corrente_Final_Senoidal.text()))
            Freq_Sen = str(float(self.ui.Frequencia_Senoidal.text()))
            Ciclo_Sen = str(int(self.ui.N_Ciclos_Senoidal.text()))
            Ponto_Sen = str(int(self.ui.N_Pontos_Senoidal.text()))          
            F_Ent = str(float(self.ui.Fator_Entrada.text()))
            F_Saida = str(float(self.ui.Fator_Saida.text()))
            C_Max = str(float(self.ui.Corrente_Maxima_Fonte.text()))
            C_Min = C_Max = str(float(self.ui.Corrente_Minima_Fonte.text()))
        except:
            QtGui.QMessageBox.warning(self,'Atenção.','Valor não Numérico.',QtGui.QMessageBox.Ok)
            return
        try:    
            f = open(arquivo, 'w')
        except:
            return
        f.write('1\n')
        f.write('Nome da Fonte:\t' + nome + '\n')
        f.write('Corrente Linear:\t' + C_Linear +'\n')
        f.write('Amplitude Linear:\t' + Amp_Linear + '\n')
        f.write('Tempo Linear:\t' + T_Linear + '\n')
        f.write('Corrente Inicial Auto:\t' + C_Inicial + '\n')
        f.write('Corrente Final Auto:\t' + C_Final + '\n')
        f.write('Numero Correntes:\t' + N_Corrente + '\n')
##        f.write('Amplitude Auto:\t' + Amp_Auto + '\n')
##        f.write('Tempo Auto:\t' + T_Auto + '\n')
        f.write('Amplitude Senoidal:\t' + Amp_Sen + '\n')
        f.write('Offset Senoidal:\t' + Off_Sen + '\n')
        f.write('Pico Inferior:\t' + P_I_Sen + '\n')
        f.write('Pico Superior:\t' + P_S_Sen + '\n')
        f.write('Corrente Final Senoidal:\t' + C_F_Sen + '\n')
        f.write('Frequencia Senoidal:\t' + Freq_Sen + '\n')
        f.write('N Ciclos Senoidal:\t' + Ciclo_Sen + '\n')
        f.write('N Pontos Senoidal:\t' + Ponto_Sen + '\n')
        f.write('Fator Entrada:\t' + F_Ent + '\n')
        f.write('Fator Saida:\t' + F_Saida + '\n')
        f.write('Corrente Máxima da Fonte:\t' + C_Max + '\n')
        f.write('Corrente Mínima da Fonte:\t' + C_Min )
        f.close()
        

    def Carregar_Fonte(self):
        try:
            arquivo = QtGui.QFileDialog.getOpenFileName(self, 'Load File', '.','Data files (*.dat);;Text files (*.txt)')
            f = open(arquivo, 'r')
        except:
            QtGui.QMessageBox.warning(self,'Atenção.','Arquivo não foi Aberto.',QtGui.QMessageBox.Ok)
            return
        leitura = f.read().strip()
        f.close()
        dados = leitura.split('\n')
        leitura = dados
        if leitura[0] == '1':
            leitura.pop(0)
        else:
            QtGui.QMessageBox.warning(self,'Atenção.','Arquivo Incorreto.',QtGui.QMessageBox.Ok)
            return
        for i in range(len(leitura)):
            c = leitura[i].split('\t')
            dados[i] = c[1]
        try:    
            self.ui.Nome_Fonte.setText(dados[0])
            self.ui.Corrente_Linear.setText(dados[1])
            self.ui.Amplitude_Linear.setText(dados[2])
            self.ui.Tempo_Linear.setText(dados[3])
            self.ui.Corrente_Auto_Inicial.setText(dados[4])
            self.ui.Corrente_Auto_Final.setText(dados[5])
            self.ui.N_Correntes_Auto.setText(dados[6])
##            self.ui.Amplitude_Auto.setText(dados[7])
##            self.ui.Tempo_Auto.setText(dados[8])
            self.ui.Amplitude_Senoidal.setText(dados[7])
            self.ui.Offset_Senoidal.setText(dados[8])
            self.ui.Pico_Inferior_Senoidal.setText(dados[9])
            self.ui.Pico_Superior_Senoidal.setText(dados[10])
            self.ui.Corrente_Final_Senoidal.setText(dados[11])
            self.ui.Frequencia_Senoidal.setText(dados[12])
            self.ui.N_Ciclos_Senoidal.setText(dados[13])
            self.ui.N_Pontos_Senoidal.setText(dados[14])
            self.ui.Fator_Entrada.setText(dados[15])
            self.ui.Fator_Saida.setText(dados[16])
            self.ui.Corrente_Maxima_Fonte.setText(dados[17])
            self.ui.Corrente_Minima_Fonte.setText(dados[18])
            self.ui.label_135.setText('OK')
            QtGui.QApplication.processEvents()
        except:
            QtGui.QMessageBox.warning(self,'Atenção.','Dados da Fonte Incompletos.',QtGui.QMessageBox.Ok)
            return


        ########### ABA 4.1: Curva Linear ###########
    def Corrente_Fonte(self):
        try:
            corrente = round(lib.PUC.ReadAD(),3)
            entrada = float(self.ui.Fator_Entrada.text())
            self.ui.lcd_Corrente.display((corrente*entrada))
        except:
            QtGui.QMessageBox.warning(self,'Atenção.','Carregue Dados da Fonte.',QtGui.QMessageBox.Ok)
            return

    def Rampa(self,final,atual,passo,tempo):
        try:
            if final > atual:
                faixa = numpy.arange(atual+passo,final+passo,passo)
            else:
                faixa = numpy.arange(final+passo,atual+passo,passo)
                faixa = faixa[::-1]
            faixa[-1] = final
            for i in faixa:
                time.sleep(tempo)
                lib.PUC.WriteDA(i)
            return True
        except:
            return False
        

    def Rampa_Corrente_Manual(self):
        atual = round(lib.PUC.ReadDA(),3)
        try:
            f_saida = float(self.ui.Fator_Saida.text())
            final = float(self.ui.Corrente_Linear.text())
            final = (final/f_saida)
            if final > 10:
                final = atual
                QtGui.QMessageBox.warning(self,'Atenção.','Valor fora dos Limites da Fonte.',QtGui.QMessageBox.Ok)
            elif final < -10:
                final = atual
                QtGui.QMessageBox.warning(self,'Atenção.','Valor fora dos Limites da Fonte.',QtGui.QMessageBox.Ok)
            
            passo = float(self.ui.Amplitude_Linear.text())
            passo = (passo/f_saida)
            tempo = float(self.ui.Tempo_Linear.text())
        except:
            QtGui.QMessageBox.warning(self,'Atenção.','Valor Incorretos ou não Numérico.',QtGui.QMessageBox.Ok)
            return
        ramp = self.Rampa(final,atual,passo,tempo)
        if ramp == True:
            QtGui.QMessageBox.information(lib.Janela,'Aviso.','Corrente atingida com Sucesso.',QtGui.QMessageBox.Ok)
        else:
            QtGui.QMessageBox.critical(self,'Atenção.','Fonte no Valor Desejado.',QtGui.QMessageBox.Ok)
            return

    def Rampa_Corrente_Automatico(self):
        try:
            valor_inicial = float(self.ui.Corrente_Auto_Inicial.text())
            valor_final = float(self.ui.Corrente_Auto_Final.text())
            n_corrente = int(self.ui.N_Correntes_Auto.text())
            f_saida = float(self.ui.Fator_Saida.text())
            passo = float(self.ui.Amplitude_Linear.text())
            tempo = float(self.ui.Tempo_Linear.text())
            valor_inicial = valor_inicial/f_saida
            valor_final = valor_final/f_saida
            passo = (passo/f_saida)
        except:
            QtGui.QMessageBox.warning(self,'Atenção.','Valor não Numérico.',QtGui.QMessageBox.Ok)
            return

        passo_corrente = (valor_final - valor_inicial)/(n_corrente-1)
        faixa_corrente = numpy.arange(valor_inicial,valor_final+passo_corrente,passo_corrente)
        medida = 1
        for i in range(len(faixa_corrente)):
            atual = round(lib.PUC.ReadDA(),3)
            try:
                if faixa_corrente[i] > atual:
                    faixa = numpy.arange(atual+passo,faixa_corrente[i]+passo,passo)
                else:
                    faixa = numpy.arange(faixa_corrente[i]+passo,atual+passo,passo)
                    faixa = faixa[::-1]
                faixa[-1] = faixa_corrente[i]
            except:
                time.sleep(.1)
            for j in faixa:
                time.sleep(tempo)
                lib.PUC.WriteDA(j)
            time.sleep(2)
            self.Correcao_Posicao()
            ColetaDados(len(faixa_corrente))
            time.sleep(.1)
            self.SALVAR_HARMONICO(1,medida)
            self.ui.label_138.setText(str(i+1))
            QtGui.QApplication.processEvents()
            medida+=1
  
        QtGui.QMessageBox.information(lib.Janela,'Atenção.','Processo de Coleta Automática Concluído.',QtGui.QMessageBox.Ok)
         
    
    def Hab_Auto(self):
        if self.ui.Chk_Auto.isChecked():
##            self.ui.Configuracao_Auto.setEnabled(True)
##            self.ui.Configuracao_Manual.setEnabled(False)
            self.ui.C_Sucessivas.setEnabled(False)
        else:
##            self.ui.Configuracao_Auto.setEnabled(False)
##            self.ui.Configuracao_Manual.setEnabled(True)
            self.ui.C_Sucessivas.setEnabled(True)

        

        ########### ABA 4.2: Curva Senoidal ###########

    def Hab_Ponto(self):
        if self.ui.Chk_Senoidal_Ponto.isChecked():
            self.ui.N_Pontos_Senoidal.setEnabled(True)
            self.ui.label_122.setEnabled(True)
            self.ui.label_120.setEnabled(True)
            self.ui.N_Ciclos_Senoidal.setEnabled(False)
            self.ui.label_117.setEnabled(False)
            self.ui.label_123.setEnabled(False)
        else:
            self.ui.N_Pontos_Senoidal.setEnabled(False)
            self.ui.label_122.setEnabled(False)
            self.ui.label_120.setEnabled(False)
            self.ui.N_Ciclos_Senoidal.setEnabled(True)
            self.ui.label_117.setEnabled(True)
            self.ui.label_123.setEnabled(True)

    def Plotar_Curva(self, pontos):
        curva, checksum, pontos, ciclos = self.Gerar_Curva_Senoidal()
        pontos = pontos[:ciclos]
        plt.plot(pontos)
        plt.show()

    def Enviar_Curva(self):
        curva, checksum, pontos, ciclos = self.Gerar_Curva_Senoidal()
        check = lib.PUC.SendCurve(curva)
        if check == checksum:
            QtGui.QMessageBox.warning(self,'Atenção.','Envio da Curva com Sucesso.',QtGui.QMessageBox.Ok)
            self.ui.Ciclar.setEnabled(True)
            return True
        else:
            QtGui.QMessageBox.warning(self,'Atenção.','Falha no envio da Curva.',QtGui.QMessageBox.Ok)
            return False

    def Gerar_Curva_Senoidal(self):
        try:
            f_saida = float(self.ui.Fator_Saida.text())
            Amp = (float(self.ui.Amplitude_Senoidal.text()))/f_saida
            freq = float(self.ui.Frequencia_Senoidal.text())
            offset = (float(self.ui.Offset_Senoidal.text()))/f_saida
        except:
            QtGui.QMessageBox.warning(self,'Atenção.','Carregue Dados da Fonte.',QtGui.QMessageBox.Ok)
            return 
        ciclos = (int(const.Pontos_Puc/const.Clock_Puc)*const.Clock_Puc)
        Amp = Amp/2
        w = (2*numpy.pi*freq)/const.Clock_Puc
        pontos = list(map(lambda x: Amp*numpy.sin(w*x)+offset,range(const.Pontos_Puc)))  # gera a lista de pontos
        curva = lib.PUC.ConverteCurva(pontos)   # converte para complemento de 2 com 4 bytes
        checksum = lib.PUC.CalculateGeneratedCsum(curva)     # calcula o checksum da curva gerada
        lib.Ciclos_Puc = ciclos
        return curva, checksum, pontos, ciclos

    def Ciclagem(self):
        self.ui.EnviaCurva.setEnabled(False)
        self.ui.Ciclar.setEnabled(False)
        atual = round(lib.PUC.ReadDA(),3)
        f_saida = float(self.ui.Fator_Saida.text())
        final = (float(self.ui.Offset_Senoidal.text()))/f_saida
        passo = (float(self.ui.Amplitude_Linear.text()))/f_saida
        tempo = float(self.ui.Tempo_Linear.text())
        self.Rampa(final,atual,passo,tempo)
        

        lib.PUC.ExecuteCurve(lib.Ciclos_Puc, 0, 0, 1, 0, 0, 0)


        self.ui.EnviaCurva.setEnabled(True)
        self.ui.Ciclar.setEnabled(True)
                

        
    ########### ABA 5: Motores ###########

    def LIGARMOTOR(self):
        endereco = int(self.ui.EndDriver_2.currentIndex() + 1)
        velocidade = float(self.ui.velocidade.text())
        if velocidade > 5:
            velocidade = 5
            self.ui.velocidade.setText('5')
        aceleracao = float(self.ui.aceleracao.text())
        if aceleracao > 5:
            aceleracao = 5
            self.ui.aceleracao.setText('5')
        voltas = float(self.ui.voltas.text())
        sentido = self.ui.sentido.currentIndex()
        modo = self.ui.modo.currentIndex()
        self.Motor_Manual(endereco, velocidade, aceleracao, voltas, sentido, modo)

    def Motor_Manual(self,endereco, velocidade, aceleracao, voltas, sentido, modo):
##    Endereco(1-Giro;2-Mesa longitudinal) sentido(0-Horario;1-Antihorario) modo(0-manual;1-continuo)
        voltas = int(voltas * lib.passos_volta)
        lib.motor.SetResolucao(endereco,lib.passos_volta)
        lib.motor.ConfMotor(endereco,velocidade,aceleracao,voltas)
        lib.motor.ConfModo(endereco,modo,sentido)
        if lib.motor.ready(endereco):
            lib.motor.MoverMotor(endereco)
            
    def PARARMOTOR(self):
        endereco = int(self.ui.EndDriver_2.currentIndex() + 1)
        lib.motor.PararMotor(endereco)


    ########### ABA 6: Bobina ###########

    def CARREGABOBINA(self):
        try:
            arquivo = QtGui.QFileDialog.getOpenFileName(self, 'Load File', '.','Data files (*.dat);;Text files (*.txt)')
            f = open(arquivo, 'r')
        except:
            return
        leitura = f.read().strip()
        f.close()
        a = leitura.split('\n\n')
        leitura = a[0].split('\n')
        if leitura[0] == '2':
            leitura.pop(0)
        else:
            QtGui.QMessageBox.warning(self,'Atenção.','Arquivo Incorreto.',QtGui.QMessageBox.Ok)
            return
        b = a[1].split('\n')
        c = a[2].split('\n')
        a = a[0].split('\t')
        self.ui.BobinaNome.setText(a[1])
        for i in range(len(b)):
            b[i]=b[i].split('\t')
            c[i]=c[i].split('\t')
        c[len(c)-1]=c[len(c)-1].split('\t')
        self.ui.nespiras.setText(b[1][1])
        self.ui.raio1.setText(b[2][1])
        self.ui.raio2.setText(b[3][1])
        self.ui.nespirasb.setText(c[1][1])
        self.ui.raio1b.setText(c[2][1])
        self.ui.raio2b.setText(c[3][1])
        self.ui.sentido_2.setCurrentIndex(int(c[4][1])-1)
        self.ui.label_136.setText('OK')
        QtGui.QApplication.processEvents()

    def SALVABOBINA(self):
        try:
            arquivo = QtGui.QFileDialog.getSaveFileName(self, 'Save File', '.','Data files (*.dat);;Text files (*.txt)')
        except:
            return
        nome = str(self.ui.BobinaNome.text())
        Ne = str(self.ui.nespiras.text())
        Neb = str(self.ui.nespirasb.text())
        r1 = str(self.ui.raio1.text())
        r2 = str(self.ui.raio2.text())
        r1b = str(self.ui.raio1b.text())
        r2b = str(self.ui.raio2b.text())
        sentido = str(self.ui.sentido_2.currentIndex()+1)
        try:
            f = open(arquivo, 'w')
        except:
            return
        f.write('2\n')
        f.write('Nome da bobina:\t' + nome + '\n\n')
        f.write('Normal:\n')
        f.write('Numero de espiras:\t' + Ne + '\n')
        f.write('Raio 1:\t' + r1 + '\n')
        f.write('Raio 2:\t' + r2 + '\n\n')
        f.write('Bucked:\n')
        f.write('Numero de espiras:\t' + Neb + '\n')
        f.write('Raio 1:\t' + r1b + '\n')
        f.write('Raio 2:\t' + r2b + '\n')
        f.write('Sentido Giro:\t' + sentido)
        f.close()

    def MONTAR(self):
        ret = QtGui.QMessageBox.question(self,'Montar Bobina.','Rotina de montagem da bobina será inicializada.\nDeseja continuar?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if ret == QtGui.QMessageBox.No:
            return
        if lib.procura_indice_flag == 1:
            QtGui.QMessageBox.critical(self,'Montar Bobina.','Encoder Angular está sem referência.',QtGui.QMessageBox.Ok)
            return
        ret = QtGui.QMessageBox.question(self,'Montar Bobina.','Enviar Mesa Longitudinal para Referência.\nDeseja continuar?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if ret == QtGui.QMessageBox.Yes:
            lib.motor.MoverMotorFimdeCursoNeg(const.motorC_endereco,3,5)        
            while not lib.motor.ready(const.motorC_endereco) and lib.parartudo == 0:
                time.sleep(0.5)
        else:
            return
        ret = QtGui.QMessageBox.question(self,'Montar Bobina.','Enviar Mesa A para Posição Livre.\nDeseja continuar?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if ret == QtGui.QMessageBox.Yes:
            self.Mover_Motor_A(20,5)
        else:
            return
        while lib.Motor_Posicao == 0:
            time.sleep(.5)
        ret = QtGui.QMessageBox.question(self,'Montar Bobina.','Enviar Mesa B para Posição Livre.\nDeseja continuar?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if ret == QtGui.QMessageBox.Yes:
            self.Mover_Motor_B(20,5)
        else:
            return
        while lib.Motor_Posicao == 0:
            time.sleep(.5)
        ret = QtGui.QMessageBox.question(self,'Montar Bobina.','Posicionar o Giro da Bobina.\nDeseja continuar?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if ret == QtGui.QMessageBox.Yes:
            self.posicao_angular(const.pos_ang, 1)
        else:
            return     
        ret = QtGui.QMessageBox.question(self,'Montar Bobina.','Posicionar a Bobina Dentro do Ima.\nDeseja continuar?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if ret == QtGui.QMessageBox.No:
            return
        ret = QtGui.QMessageBox.question(self,'Montar Bobina.','Enviar Mesa A para Posição de Pré Montagem.\nDeseja continuar?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if ret == QtGui.QMessageBox.Yes:
            self.Mover_Motor_A(10,5)
        else:
            return    
        while lib.Motor_Posicao == 0:
            time.sleep(.5)          
        ret = QtGui.QMessageBox.question(self,'Montar Bobina.','Enviar Mesa A para Posição Zero.\nDeseja continuar?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if ret == QtGui.QMessageBox.Yes:
            self.Mover_Motor_A(0,1)
        else:
            return
        while lib.Motor_Posicao == 0:
            time.sleep(.5)
        ret = QtGui.QMessageBox.question(self,'Montar Bobina.','Enviar Mesa B para Posição de Pré Montagem.\nDeseja continuar?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if ret == QtGui.QMessageBox.Yes:
            self.Mover_Motor_B(10,5)
        else:
            return        
        while lib.Motor_Posicao == 0:
            time.sleep(.5)
        ret = QtGui.QMessageBox.question(self,'Montar Bobina.','Enviar Mesa B para Posição Zero.\nDeseja continuar?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if ret == QtGui.QMessageBox.Yes:
            self.Mover_Motor_B(0,1)
        else:
            return
        while lib.Motor_Posicao == 0:
            time.sleep(.5)
        ret = QtGui.QMessageBox.question(self,'Montar Bobina.','Travar a Bobina Manualmente.\nDeseja continuar?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if ret == QtGui.QMessageBox.No:
            return
        ret = QtGui.QMessageBox.question(self,'Montar Bobina.','Realizar a pré-tração da Bobina.\nDeseja continuar?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if ret == QtGui.QMessageBox.Yes:
            lib.motor.ConfMotor(const.motorC_endereco,3,5,const.pos_long*lib.passos_volta)
            lib.motor.ConfModo(const.motorC_endereco,0,const.avancoC)
            lib.motor.MoverMotor(const.motorC_endereco)            
            while not lib.motor.ready(const.motorC_endereco) and lib.parartudo == 0:
                time.sleep(0.5)
        else:
            return
        ret = QtGui.QMessageBox.question(self,'Montar Bobina.','Finalizar a tração da Bobina.\nDeseja continuar?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if ret == QtGui.QMessageBox.Yes:
            lib.motor.ConfMotor(const.motorC_endereco,3,5,(const.pos_trac - const.pos_long)*lib.passos_volta)
            lib.motor.ConfModo(const.motorC_endereco,0,const.avancoC)
            lib.motor.MoverMotor(const.motorC_endereco)
            while not lib.motor.ready(const.motorC_endereco) and lib.parartudo == 0:
                time.sleep(0.5)
        else:
            return
        QtGui.QMessageBox.critical(self,'Montar Bobina.','Processo de montagem da Bobina Finalizado.',QtGui.QMessageBox.Ok)        
       
    def DESMONTAR(self):
        ret = QtGui.QMessageBox.question(self,'Desmontar Bobina.','Rotina de desmontagem da bobina será inicializada.\nDeseja continuar?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if ret == QtGui.QMessageBox.No:
            return
        if lib.procura_indice_flag == 1:
            QtGui.QMessageBox.critical(self,'Desmontar Bobina.','Encoder Angular está sem referência.',QtGui.QMessageBox.Ok)
            return
        ret = QtGui.QMessageBox.question(self,'Desmontar Bobina.','Posicionar o Giro da Bobina.\nDeseja continuar?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if ret == QtGui.QMessageBox.Yes:
            self.posicao_angular(const.pos_ang, 1)
        else:
            return
        ret = QtGui.QMessageBox.question(self,'Desmontar Bobina.','Destravar a Bobina Manualmente.\nDeseja continuar?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if ret == QtGui.QMessageBox.No:
            return
        ret = QtGui.QMessageBox.question(self,'Desmontar Bobina.','Retirar a tração da Bobina.\nDeseja continuar?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if ret == QtGui.QMessageBox.Yes:
            lib.motor.ConfMotor(const.motorC_endereco,3,5,(const.pos_trac - const.pos_long)*lib.passos_volta)
            lib.motor.ConfModo(const.motorC_endereco,0,const.avancoC^1)
            lib.motor.MoverMotor(const.motorC_endereco)
            while not lib.motor.ready(const.motorC_endereco) and lib.parartudo == 0:
                time.sleep(0.5)
        else:
            return
        ret = QtGui.QMessageBox.question(self,'Desmontar Bobina.','Enviar Mesa B para Posição de Pré Desmontagem.\nDeseja continuar?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if ret == QtGui.QMessageBox.Yes:
            self.Mover_Motor_B(10,1)
        else:
            return    
        while lib.Motor_Posicao == 0:
            time.sleep(.5)         
        ret = QtGui.QMessageBox.question(self,'Desmontar Bobina.','Enviar Mesa B para Posição Final.\nDeseja continuar?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if ret == QtGui.QMessageBox.Yes:
            self.Mover_Motor_B(20,5)
        else:
            return    
        while lib.Motor_Posicao == 0:
            time.sleep(.5)  
        ret = QtGui.QMessageBox.question(self,'Desmontar Bobina.','Enviar Mesa A para Posição de Pré Desmontagem.\nDeseja continuar?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if ret == QtGui.QMessageBox.Yes:
            self.Mover_Motor_A(10,1)
        else:
            return    
        while lib.Motor_Posicao == 0:
            time.sleep(.5)         
        ret = QtGui.QMessageBox.question(self,'Desmontar Bobina.','Enviar Mesa A para Posição Final.\nDeseja continuar?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if ret == QtGui.QMessageBox.Yes:
            self.Mover_Motor_A(20,5)
        else:
            return    
        while lib.Motor_Posicao == 0:
            time.sleep(.5)
        ret = QtGui.QMessageBox.question(self,'Desmontar Bobina.','Retirar a Bobina de Dentro do Ima.\nDeseja continuar?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if ret == QtGui.QMessageBox.No:
            return
        QtGui.QMessageBox.critical(self,'Desmontar Bobina.','Processo de desmontagem da Bobina Finalizado.',QtGui.QMessageBox.Ok)
        

    ########### ABA 7: Integrador ###########

    def SALVAR_DEFAULT(self):
        port1 = str(self.ui.Porta.currentIndex()+1)
        port2 = str(self.ui.Porta_2.currentIndex()+1)
        port3 = str(self.ui.Porta_3.currentIndex()+1)
        port4 = str(self.ui.Porta_4.currentIndex()+1)
        enderec = str(self.ui.Enderac_PUC.text())
        ganho = str(self.ui.ganho.currentIndex())
        pontos_integracao = str(self.ui.pontos_integracao.currentIndex())
        pulsos_encoder = self.ui.pulsos_encoder.text()
        pulsos_trigger = self.ui.pulsos_trigger.text()
        velocidade = self.ui.velocidade_int.text()
        aceleracao = self.ui.aceleracao_int.text()
        voltas_offset = self.ui.voltas_offset.text()
        volta_filtro = self.ui.filtro_voltas.text()
        N = self.ui.nespiras.text()
        raio1 = self.ui.raio1.text()
        raio2 = self.ui.raio2.text()
        f = open('default_settings.dat','w')
        f.write('0\n')
        f.write('Configurações da bobina girante\n\n')
        f.write('Porta Display\t' + port1 + '\n')
        f.write('Porta Driver\t' + port2 + '\n')
        f.write('Porta Integrador\t' + port3 + '\n')
        f.write('Porta PUC\t' + port4 + '\n')
        f.write('Enderecamento PUC\t' + enderec + '\n\n')
        f.write('Endereco Driver\t' + str(lib.endereco) + '\n')
        f.write('Ganho\t' + ganho + '\n')
        f.write('Pontos Integracao\t' + pontos_integracao + '\n')
        f.write('Pulsos Encoder\t' + pulsos_encoder + '\n')
        f.write('Pulsos para Trigger\t' + pulsos_trigger + '\n')
        f.write('Velocidade Medida\t' + velocidade + '\n')
        f.write('Aceleracao Medida\t' + aceleracao + '\n')
        f.write('Voltas offset\t' + voltas_offset + '\n')
        f.write('Volta filtro\t' + volta_filtro + '\n')
        f.write('Passos Motor\t' + str(lib.passos_volta) + '\n\n')
        f.write('\n\nEndereco Driver A\t' + str(const.motorA_endereco) + '\n')
        f.write('Endereco Driver B\t' + str(const.motorB_endereco) + '\n')
        f.write('Endereco Driver C\t' + str(const.motorC_endereco) + '\n')
        f.write('Avanco do motor A\t' + str(const.avancoA) + '\n')
        f.write('Avanco do motor B\t' + str(const.avancoB) + '\n')
        f.write('Avanco do motor C\t' + str(const.avancoC) + '\n')
        f.write('Posicao de indice A\t' + str(const.zeroA) + '\n')
        f.write('Posicao de indice B\t' + str(const.zeroB) + '\n')
        f.write('Posicao angular montagem\t' + str(const.pos_ang) + '\n')
        f.write('Posicao longitudinal montagem\t' + str(const.pos_long) + '\n')
        f.write('Posicao vertical\t' + str(const.pos_ver) + '\n')
        f.write('Posicao tracao\t' + str(const.pos_trac))
        f.close()
                
    def POSICIONAR(self):
        try:
            posicao = int(self.ui.posicao_angular.text())
        except:
            return
        if posicao > (lib.pulsos_encoder - 1):
            posicao = (lib.pulsos_encoder - 1)
            self.ui.posicao_angular.setText(str((lib.pulsos_encoder - 1)))
        if posicao < 0:
            posicao = 0
            self.ui.posicao_angular.setText('0')
        self.posicao_angular(posicao, lib.endereco,(1/1),(1/1))

    def posicao_angular(self, posicao, endereco, velocidade=1, aceleracao=1):
        tempoespera = 0.1
        lib.integrador.LimpaTxRx()
        lib.integrador.Enviar(lib.integrador.PDILerEncoder)
        time.sleep(tempoespera)
        valor = lib.integrador.ser.readall().strip()
        valor = str(valor).strip('b').strip("'")
        valor = int(valor)
        erro = posicao - valor
        if erro < 0:
            sentido = 0
        else:
            sentido = 1
        passos = int(lib.passos_volta*abs(erro)/lib.pulsos_encoder)  #/10000
        lib.motor.ConfMotor(endereco,velocidade,aceleracao,passos)
        lib.motor.ConfModo(endereco,0,sentido)
        lib.motor.MoverMotor(endereco)

    def Correcao_Posicao(self):
        posicao = lib.pulsos_trigger + (lib.pulsos_encoder / 2)
        if posicao > lib.pulsos_encoder:
            posicao = posicao - lib.pulsos_encoder
        self.posicao_angular(posicao, lib.endereco,(1/1),(1/1))
        time.sleep(1)

    def PARAR_TUDO(self):
        lib.parartudo = 1
        self.KILL()
        lib.parartudo = 0

            
    def Tabela(self):
##        self.ui.tabela.clear()
        TipoIma = lib.Janela.ui.TipoIma.currentIndex()
        if len(lib.F[0])>16:
            nmax = 16
        else:
            nmax = 8
        for i in range(1,nmax,1):
            self.set_item(i-1,0,str(lib.Nn[i]))
            self.set_item(i-1,1,str(lib.Sn[i]))
            self.set_item(i-1,2,str(lib.SMod[i]))
            self.set_item(i-1,3,str(lib.sDesvNn[i]))
            self.set_item(i-1,4,str(lib.sDesvSn[i]))
            self.set_item(i-1,5,str(lib.sDesv[i]))
            if i == TipoIma or TipoIma == 0:
                self.set_item(i-1,6,str(lib.angulo[i]))
            else:
                self.set_item(i-1,6,str('0.00'))
            self.set_item(i-1,7,str(lib.Nnl[i]))
            self.set_item(i-1,8,str(lib.Snl[i]))

    def set_item(self,lin,col,Text):
        item = QtGui.QTableWidgetItem()
        self.ui.tabela.setItem(lin, col, item)
        item.setText(Text)
    
    def ProcuraIndiceEncoder(self):
        tempoespera = 0.1
        lib.integrador.Enviar(lib.integrador.PDIZerarContador)
        time.sleep(tempoespera)
        lib.integrador.Enviar(lib.integrador.PDIProcuraIndice)
        time.sleep(tempoespera)
        lib.motor.SetResolucao(lib.endereco,lib.passos_volta)
        lib.motor.ConfMotor(lib.endereco,1,1,lib.passos_volta*2)  #(lib.endereco,1,1,100000
        lib.motor.ConfModo(lib.endereco,0,1)
        lib.motor.MoverMotor(lib.endereco)
        while not lib.motor.ready(lib.endereco) and not lib.parartudo:
            continue
        lib.motor.ConfModo(lib.endereco,0,0)
        lib.motor.MoverMotor(lib.endereco)
        while not lib.motor.ready(lib.endereco) and not lib.parartudo:
            continue
        if not lib.parartudo:
            lib.integrador.LimpaTxRx()
            lib.integrador.Enviar(lib.integrador.PDILerEncoder)
            time.sleep(tempoespera)
            valor = lib.integrador.ser.readall().strip()
            valor = str(valor).strip('b').strip("'")
            valor = int(valor)
            passos = int(lib.passos_volta*valor/lib.pulsos_encoder)  #/10000
            lib.motor.ConfMotor(lib.endereco,1,1,passos)
            lib.motor.ConfModo(lib.endereco,0,0)
            lib.motor.MoverMotor(lib.endereco)
            
    def Start_Config(self):
        bit = 0
        self.CONFIGURARINTEGRADOR(bit)
        
    def CONFIGURARINTEGRADOR(self,bit):
        lib.ganho = self.ui.ganho.currentIndex()
        lib.ganho = const.ganhos[lib.ganho]
        pontos_integracao = self.ui.pontos_integracao.currentIndex()
        lib.pontos_integracao = const.p_integracao[pontos_integracao]
        lib.endereco = self.ui.EndDriver.currentIndex()+1
        try:
            lib.velocidade = float(self.ui.velocidade_int.text())
            lib.aceleracao = float(self.ui.aceleracao_int.text())
        except:
            QtGui.QMessageBox.critical(self,'Erro.','Não foi possível converter os valores de velocidade e aceleração.',QtGui.QMessageBox.Ok)
            return        
        try:
            lib.pulsos_encoder = (int(self.ui.pulsos_encoder.text())) * 4
            lib.pulsos_trigger = int(self.ui.pulsos_trigger.text())
            lib.voltas_offset = int(self.ui.voltas_offset.text()) + 2  # 1 descarte aceleracao; 1 filtro de erro transmissão de dados            
        except:
            QtGui.QMessageBox.critical(self,'Erro.','Parâmetros de configuração do integrador devem ser números inteiros.',QtGui.QMessageBox.Ok)
            return
        if lib.velocidade > 3:
            QtGui.QMessageBox.warning(self,'Atenção.','Velocidade muito alta.',QtGui.QMessageBox.Ok)
            lib.velocidade = 3
            self.ui.velocidade_int.setText('3')
        if lib.aceleracao > 10:
            QtGui.QMessageBox.warning(self,'Atenção.','Aceleracao muito alta.',QtGui.QMessageBox.Ok)
            lib.aceleracao = 10
            self.ui.aceleracao_int.setText('10')
        if lib.pulsos_trigger > int(lib.pulsos_encoder-1):
            QtGui.QMessageBox.critical(self,'Atenção.','Pulso de Início Maior que permitido.\nTente novamente.',QtGui.QMessageBox.Ok)
            return
        lib.sentido = lib.Janela.ui.sentido_2.currentIndex()
        self.ui.label_69.setText('Máx: ' + str(int(lib.pulsos_encoder-1)))
        if lib.sentido == 0:
            lib.integrador.Configurar_Integrador('-',lib.ganho, lib.pontos_integracao, lib.pulsos_encoder, lib.pulsos_trigger, lib.voltas_offset)
        elif lib.sentido == 1:
            lib.integrador.Configurar_Integrador('+',lib.ganho, lib.pontos_integracao, lib.pulsos_encoder, lib.pulsos_trigger, lib.voltas_offset)
        if lib.procura_indice_flag == 1:
            lib.procura_indice_flag = 0
            self.ProcuraIndiceEncoder()
            time.sleep(2)
##            self.Motor_Manual(lib.endereco, lib.velocidade, lib.aceleracao, 10, lib.sentido, 0)   #Voltas de acomodamento
            if lib.sentido == 0:
                lib.integrador.Configurar_Integrador('-',lib.ganho, lib.pontos_integracao, lib.pulsos_encoder, lib.pulsos_trigger, lib.voltas_offset)
            elif lib.sentido == 1:
                lib.integrador.Configurar_Integrador('+',lib.ganho, lib.pontos_integracao, lib.pulsos_encoder, lib.pulsos_trigger, lib.voltas_offset)
            self.ui.configurar_integrador.setText('Configurar')
            self.ui.posicionar.setEnabled(True)
            self.ui.label_137.setText('OK')
            QtGui.QApplication.processEvents()
        if self.ui.TipoIma.currentIndex() == 0:
            self.ui.filtro_voltas.setEnabled(False)
        else:
            self.ui.filtro_voltas.setEnabled(True)
        if bit == 0:
            QtGui.QMessageBox.information(self,'Aviso.','Integrador configurado com sucesso.',QtGui.QMessageBox.Ok)

    def LERENCODER(self):
        lib.integrador.LimpaTxRx()
        lib.integrador.Enviar(lib.integrador.PDILerEncoder)
        time.sleep(0.05)
        valor = lib.integrador.ser.readall().strip()
        valor = str(valor).strip('b').strip("'")
        valor = int(valor)
        self.ui.lcdNumber.display(valor)

    def ZERAROFFSET(self):
        lib.integrador.Enviar(lib.integrador.PDICurtoCircuito)



     ########### ABA 8: Coletas ###########

    def Coleta_Suc_Manual(self):
        if self.ui.C_Sucessivas.isChecked():
            self.ui.N_Coletas_Manual.setEnabled(True)
            self.ui.label_22.setEnabled(True)
            self.ui.Chk_Auto.setEnabled(False)
        else:
            self.ui.N_Coletas_Manual.setEnabled(False)
            self.ui.label_22.setEnabled(False)
            self.ui.Chk_Auto.setEnabled(True)

    def COLETA_INTEGRADOR(self):
        if (self.ui.tabWidget.isTabEnabled(3) == True) and (self.ui.Nome_Fonte.text() == ''):
            QtGui.QMessageBox.warning(self,'Atenção.','Carregue dados da fonte.\nTente Novamente.',QtGui.QMessageBox.Ok)
            return
        if (self.ui.tabWidget.isTabEnabled(3) == True) and (self.ui.Chk_Auto.isChecked()):
            try:
                quantidade = float(self.ui.N_Correntes_Auto.text())
            except:
                QtGui.QMessageBox.warning(self,'Atenção.','Número de Correntes Não Inteiro ou Numérico.\nTente Novamente.',QtGui.QMessageBox.Ok)
                return
            if quantidade <= 1:
                QtGui.QMessageBox.warning(self,'Atenção.','Número de Correntes deve ser Inteiro e Maior que 1.\nTente Novamente.',QtGui.QMessageBox.Ok)
                return
        elif (self.ui.C_Sucessivas.isChecked()):
            quantidade = 1
        else:
            quantidade = 0            
        if self.ui.BobinaNome.text() == '':
            QtGui.QMessageBox.warning(self,'Atenção.','Carregue dados da bobina.\nTente Novamente.',QtGui.QMessageBox.Ok)
            return
        if (lib.procura_indice_flag == 1):
            QtGui.QMessageBox.warning(self,'Atenção.','Configurar Integrador.\nTente Novamente.',QtGui.QMessageBox.Ok)
            return
        if self.ui.Nome_Ima.text() =='':
            QtGui.QMessageBox.warning(self,'Atenção.','Informe o Nome do Ima.\nTente Novamente.',QtGui.QMessageBox.Ok)
            return
        
        nome = str(self.ui.Nome_Ima.text())
        self.CONFIGURARINTEGRADOR(1)
        self.ui.label_138.setText('0')
        QtGui.QApplication.processEvents()
        
        if quantidade == 0: #Rotina de Coleta de corrente manual para coleta unica
            self.ui.groupBox_2.setEnabled(False)
            self.ui.coletar.setEnabled(False)
            self.Correcao_Posicao()
            ColetaDados(1)
            self.Tabela()
            self.ui.label_138.setText('1')
            QtGui.QApplication.processEvents()

        if quantidade == 1: #Rotina de Coleta de corrente manual com coletas Sucessivas
            try:
                Rep = int(self.ui.N_Coletas_Manual.text())
                if Rep <= 1:
                    QtGui.QMessageBox.warning(self,'Atenção.','Número de Coletas deve ser Maior que 1.\nTente Novamente.',QtGui.QMessageBox.Ok)
                    return
            except:
                QtGui.QMessageBox.warning(self,'Atenção.','Número de Coletas Sucessivas Não Inteiro.\nTente Novamente.',QtGui.QMessageBox.Ok)
                return

            lib.FileName = QtGui.QFileDialog.getSaveFileName(self, 'Save File', nome)
            
            self.ui.coletar.setEnabled(False)
            self.ui.Nome_Ima.setEnabled(False)
            self.ui.N_Coletas_Manual.setEnabled(False)
            for i in range(0,Rep,1):
                self.Correcao_Posicao()
                ColetaDados(Rep)
                time.sleep(1)
                self.SALVAR_HARMONICO(1,(i+1))
                self.ui.label_138.setText(str(i+1))
                QtGui.QApplication.processEvents()  #Atualizar tela
            QtGui.QMessageBox.information(lib.Janela,'Atenção.','Processo de Coleta Automática Concluído.',QtGui.QMessageBox.Ok)
            self.ui.coletar.setEnabled(True)
            self.ui.Nome_Ima.setEnabled(True)
            self.ui.N_Coletas_Manual.setEnabled(True)     
            
        if quantidade > 1:  #Rotina de Coleta com corrente em automatico
            lib.FileName = QtGui.QFileDialog.getSaveFileName(self, 'Save File', nome)
            self.ui.groupBox_2.setEnabled(False)
            self.ui.coletar.setEnabled(False)
            self.ui.Nome_Ima.setEnabled(False)
            self.Rampa_Corrente_Automatico()
            self.ui.groupBox_2.setEnabled(True)
            self.ui.coletar.setEnabled(True)
            self.ui.Nome_Ima.setEnabled(True)



    ########### ABA 9: Resultados ###########

    def Salvar_Coletas(self):
        self.SALVAR_HARMONICO(0,1)

    def SALVAR_HARMONICO(self,Auto,Coleta):
##        if lib.pontos != []:
            data = time.strftime("%d/%m/%Y", time.localtime())
            hora = time.strftime("%H:%M:%S", time.localtime())
            if Auto == 0:
                nome = str(self.ui.Nome_Ima.text())
                arquivo = QtGui.QFileDialog.getSaveFileName(self, 'Save File', nome,'Data files (*.dat);;Text files (*.txt)')
            else:
                arquivo = lib.FileName + '_Medida_' + str(Coleta) + '.dat'
            arquivo_nome = arquivo.replace('/','\\')
            try:
                f = open(arquivo,'w')
            except:
                return

            iNumeroColetas = len(lib.F)
            TipoIma = lib.Janela.ui.TipoIma.currentIndex()
            
            # Cabecalho do arquivo
            f.write('\nCurva de Excitação - Bobina Girante\n\n')
            f.write('.........Dados de Configuração.........\n')
            f.write('Arquivo................: ' + str(arquivo_nome) + '\n')
            f.write('Data...................: ' + str(data) + '\n')
            f.write('Hora...................: ' + str(hora) + '\n')
            f.write('Ganho..................: ' + str(lib.ganho) + '\n')
            f.write('N. Pontos Integração...: ' + str(lib.pontos_integracao) + '\n')
            f.write('Velocidade.............: ' + str(lib.velocidade) + '\n')
            f.write('Aceleracao.............: ' + str(lib.aceleracao) + '\n')
            f.write('N. de Coletas..........: ' + str(Coleta) + '\n')
            f.write('N. de Voltas...........: ' + str(lib.voltas_offset + 2) + '\n')
            f.write('Intervalo de Análise...: ' + str(2) + '-' + str(lib.voltas_offset + 1) + '\n')
            f.write('Sentido de rotação.....: ' + str(lib.sentido) + '\n')
##            f.write('Deslocamento em Y(mm)..: ' + str(lib.deslY) + '\n')
            f.write('Corrente Alimentação(A): ' + str('{0:0.5e}'.format(numpy.mean(lib.LeituraCorrente.saida))) + ' Erro(S): ' + str('{0:0.5e}'.format(numpy.std(lib.LeituraCorrente.saida))) + '\n\n\n\n\n')
            
            f.write('.........Dados de Leitura.........\n')
            f.write("N\tL.Nn     \tL.Sn     \tL.Bn(T/m^n-2)\tEr_Nn(T/m^n-2)\tEr_Sn(T/m^n-2)\tErro(T/m^n-2)\tÂngulo(rad)\tL.Nn'   \tL.Sn'\n\n")
            
            if len(lib.F[0])>16:
                Nfinal = 16
            else:
                Nfinal = 8
                
            if iNumeroColetas >= 1:
                for i in range(1,Nfinal,1):
                    f.write(str(i) + '\t')
                    f.write(str('{0:0.5e}'.format(lib.Nn[i])) + '\t')
                    f.write(str('{0:0.5e}'.format(lib.Sn[i])) + '\t')
                    f.write(str('{0:0.5e}'.format(lib.SMod[i])) + '\t')
                    f.write(str('{0:0.5e}'.format(abs(lib.sDesvNn[i]))) + '\t')
                    f.write(str('{0:0.5e}'.format(abs(lib.sDesvSn[i]))) + '\t')
                    f.write(str('{0:0.5e}'.format(abs(lib.sDesv[i]))) + '\t')
                    if i == TipoIma or TipoIma == 0:
                        f.write(str('{0:0.5e}'.format(lib.angulo[i])) + '\t')
                    else:
                        f.write(str('      000.00') + '\t')                       
                    f.write(str('{0:0.5e}'.format(lib.Nnl[i])) + '\t')
                    f.write(str('{0:0.5e}'.format(lib.Snl[i])) + '\n')
            
            f.write('\n\n\n')
            f.write('.........Dados Armazenados:.........\n\n')
##            f.write('Brutos  \t\tMédios\n\n')                 #Cabeçalho de Dados Brutos e Dados Médios
            f.write('Brutos\n\n')                               #Cabeçalho de Dados Brutos

            for i in range(len(lib.pontos)):
                for j in range(len(lib.pontos[i])):
##                    if i == 0:
##                        f.write(str(lib.pontos[i][j]) + ' \t\t' + str(lib.media[j]) + '\n')       #Rotina para salvar dados brutos e médios
##                    else:
                        f.write(str(lib.pontos[i][j]) + '\n')
                f.write('\n')

            f.write('\n\n\n')
            f.write('.........Angulo Volta:.........\n\n')
            for i in range(0,len(lib.pontos),1):
                f.write(str(lib.AnguloVolta[i]) + '\n')
            
            f.close()
##        else:
##            QtGui.QMessageBox.critical(self,'Erro.','Dados inexistentas.',QtGui.QMessageBox.Ok)

    def PlotFunc1(self,x,y):
        self.ui.widget.canvas.ax1.clear()
        self.ui.widget.canvas.ax1.plot(x,y)
        self.ui.widget.canvas.ax1.set_xlabel('Volta')
        self.ui.widget.canvas.ax1.set_ylabel('Amplitude (V.s)')
        self.ui.widget.canvas.fig.tight_layout()
        self.ui.widget.canvas.draw()

    def PlotFunc2(self,x,y):
        self.ui.widget.canvas.ax2.clear()
        self.ui.widget.canvas.ax2.plot(x,y)
##        self.ui.widget.canvas.ax.set_xlabel('Frequência')
##        self.ui.widget.canvas.ax.set_ylabel('Amplitude')
        self.ui.widget.canvas.draw()

    def PlotFunc3(self,x,y):
        self.ui.widget.canvas.ax2.clear()
        for i in range(len(y)):
            if i % 2 == 0:
                self.ui.widget.canvas.ax2.plot(x[i*lib.pontos_integracao:(i+1)*lib.pontos_integracao],y[i],'b')
            else:
                self.ui.widget.canvas.ax2.plot(x[i*lib.pontos_integracao:(i+1)*lib.pontos_integracao],y[i],'r')
        self.ui.widget.canvas.ax2.set_xlabel('Voltas')
        self.ui.widget.canvas.ax2.set_ylabel('Amplitude (V.s)')
        self.ui.widget.canvas.fig.tight_layout()
        self.ui.widget.canvas.draw()
# ____________________________________________


# ____________________________________________
# Move os motores transversais para a posicao desejada
class motortransversal(threading.Thread):
    def __init__(self, posicaoA, posicaoB, velocidade = 0.2):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.posicaoA = posicaoA
        self.posicaoB = posicaoB
        self.velocidade = velocidade
        self.start()
    def callback(self):
        self._stop()
    def run(self):
        lib.Motor_Posicao = 0
        lib.Janela.ui.status.setText('Movendo')
        if self.velocidade >= 1:
            aceleracao = 5
        else:
            aceleracao = 0.2
        lib.display.LerDisplay()
        posicao = lib.display.DisplayPos
        erroX = self.posicaoA-float(posicao[0])
        passosX = int(const.passos_mmA*abs(erroX))
        erroY = self.posicaoB-float(posicao[1])
        passosY = int(const.passos_mmB*abs(erroY))
        while (passosX > const.passos_mmA/500 or passosY > const.passos_mmB/500) and lib.parartudo == 0:
            if(erroX > 0):
                sentidoA = const.avancoA^1
            else:
                sentidoA = const.avancoA
            if(erroY > 0):
                sentidoB = const.avancoA^1
            else:
                sentidoB = const.avancoB
            lib.motor.ConfMotor(const.motorA_endereco,self.velocidade,aceleracao,passosX)
            lib.motor.ConfModo(const.motorA_endereco,0,sentidoA)
            lib.motor.ConfMotor(const.motorB_endereco,self.velocidade,aceleracao,passosY)
            lib.motor.ConfModo(const.motorB_endereco,0,sentidoB)
            if lib.motor.ready(const.motorA_endereco) and lib.motor.ready(const.motorB_endereco) and lib.parartudo == 0:
                lib.motor.MoverMotor(const.motorA_endereco)
                lib.motor.MoverMotor(const.motorB_endereco)
            while (not lib.motor.ready(const.motorA_endereco) or not lib.motor.ready(const.motorB_endereco)) and lib.parartudo == 0:
                QtGui.QApplication.processEvents()
            time.sleep(1)
            lib.display.LerDisplay()
            posicao = lib.display.DisplayPos
            erroX = self.posicaoA-float(posicao[0])
            passosX = int(const.passos_mmA*abs(erroX))
            erroY = self.posicaoB-float(posicao[1])
            passosY = int(const.passos_mmB*abs(erroY))
        if lib.Janela.ui.bobinadesmontada.isChecked():
            lib.Janela.ui.groupBox_6.setEnabled(True)
        else:
            lib.Janela.ui.groupBox_4.setEnabled(True)
        lib.Janela.ui.zerar.setEnabled(True)
        lib.Janela.ui.bobinadesmontada.setEnabled(True)
        lib.Janela.ui.status.setText('Pronto')
        QtGui.QApplication.processEvents()
        lib.Motor_Posicao = 1
# ____________________________________________



# ____________________________________________
# Encontra referencia dos motores transversais
class EncontraRef(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.start()
    def callback(self):
        self._stop()
    def run(self):
        lib.Janela.ui.status.setText('Movendo')
        lib.Janela.ui.groupBox_6.setEnabled(False)
        lib.motor.MoverMotorFimdeCursoNeg(const.motorA_endereco,3,5)
        lib.motor.MoverMotorFimdeCursoNeg(const.motorB_endereco,3,5)
        while (not lib.motor.ready(const.motorA_endereco) or not lib.motor.ready(const.motorB_endereco)) and lib.parartudo == 0:
            QtGui.QApplication.processEvents()
        if lib.parartudo == 0:
            lib.stop = 1
            time.sleep(0.5)
            lib.display.Reset_SetRef_Display()
            lib.display.EscreveValorDisplay(0, const.zeroA)
            lib.display.EscreveValorDisplay(1, const.zeroB)
            lib.stop = 0
            lib.motor.ConfMotor(const.motorA_endereco,3,5,0)
            lib.motor.ConfModo(const.motorA_endereco,1,1)
            lib.motor.ConfMotor(const.motorB_endereco,3,5,0)
            lib.motor.ConfModo(const.motorB_endereco,1,1)
            lib.motor.MoverMotor(const.motorA_endereco)
            lib.motor.MoverMotor(const.motorB_endereco)
            lib.posicao = [const.zeroA,const.zeroB]
        while (lib.posicao[0] == const.zeroA or lib.posicao[1] == const.zeroB) and lib.parartudo == 0:
            lib.display.LerDisplay()
            lib.posicao = lib.display.DisplayPos
            continue
        lib.motor.PararMotor(const.motorA_endereco)
        lib.motor.PararMotor(const.motorB_endereco)
        lib.Janela.ui.groupBox_6.setEnabled(True)
        lib.Janela.ui.zerar.setEnabled(True)
        lib.Janela.ui.status.setText('Pronto')
# ____________________________________________



# ____________________________________________
# Recebe os dados coletados pelo Integrador

##def Filtro(dados, valor_filtro):        ## Filtro de dados pelo desvio padrao elevado
##    valor_total = len(dados)
##    while (valor_total > valor_filtro):
##        dados_std = numpy.std(dados,axis=0) # redefines std values
##        locsj = numpy.argmax(dados_std) # searches for max std
##        avg_std = numpy.mean(dados_std) #average of rms values
##        locsi = numpy.argmax(abs(numpy.mean(dados[::,locsj])-dados[::,locsj])) #searches in which column is the max values
##        dados = numpy.delete(dados,locsi,0) #deletes the data set with max std
##        valor_total = valor_total-1
##    return dados

def dec_bin(Num,bit):
    valor = bin(Num)
    valor = list(valor)
    valor.pop(0)
    valor.pop(0)
    final=['0']
    if (len(valor))<8:
        for i in range(len(valor),8,1):
            valor = final + valor
    for i in range(0,8,1):
        valor[i] = int(valor[i])
    valor = valor[::-1]
    return valor[bit]


def ColetaDados(Repeticao):
    lib.LeituraCorrente = leitura_corrente(lib.voltas_offset,lib.velocidade,lib.Janela.ui.Fator_Entrada.text())
    lib.pontos_recebidos = ColetaDados_Leitura(Repeticao)
    if not lib.pontos_recebidos == [] and not lib.parartudo:
        ColetaDados_Calculos(Repeticao)
    else:
        QtGui.QMessageBox.warning(lib.Janela,'Aviso.','Dados vazios.',QtGui.QMessageBox.Ok)
    

def ColetaDados_Leitura(Repeticao):
    lib.integrador.Enviar('ISC,A,0')
    lib.integrador.Enviar(lib.integrador.PDIIniciaColeta)               # inicia a coleta de dados
    voltas = lib.voltas_offset + 2                                      
    lib.motor.SetResolucao(lib.endereco,lib.passos_volta)
    lib.motor.ConfMotor(lib.endereco,lib.velocidade,lib.aceleracao,lib.passos_volta*voltas)
    sentido = lib.Janela.ui.sentido_2.currentIndex()
    if sentido == 0:
        lib.sentido = 'Horário'
    else:
        lib.sentido = 'Anti-horário'
    lib.motor.ConfModo(lib.endereco,0,sentido)
    lib.motor.MoverMotor(lib.endereco)
    while (not lib.motor.ready(lib.endereco)) and lib.parartudo == 0:
        QtGui.QApplication.processEvents()
    
    bitstatus = 0
    while (bitstatus != 1) and lib.parartudo == 0:
        QtGui.QApplication.processEvents()
        status = lib.integrador.Status('1')
        try:
            bitstatus = int(status[-3])
        except:
            pass
    valor = ''
    status = -1
    lib.integrador.LimpaTxRx()
    time.sleep(0.1)
    lib.integrador.Enviar('ENQ')
    time.sleep(0.2)
    while (status == -1) and not lib.parartudo:
        tmp = lib.integrador.ser.readall()
        tmp = tmp.decode('utf-8')
        valor = valor + tmp
        status = tmp.find('\x1a')

    valor = valor.strip(' A\r\n\x1a')
    pontos = valor.split(' A\r\n')
    lib.integrador.Enviar('ISC,A,1')
    try:
        for i in range(len(pontos)):
            pontos[i] = int(pontos[i])
    except:
        return ColetaDados_Leitura(Repeticao)
        
    if lib.parartudo == 1:
        lib.Janela.ui.groupBox_2.setEnabled(True)
        lib.Janela.ui.coletar.setEnabled(True)
    return pontos


def ColetaDados_Calculos(Repeticao):
    ### Variaveis
    pontos = lib.pontos_recebidos
    lib.Bucked = lib.Janela.ui.Bucked.isChecked()
    Ne = int(lib.Janela.ui.nespiras.text())
    Neb = int(lib.Janela.ui.nespirasb.text())
    r1 = float(lib.Janela.ui.raio1.text())
    r2 = float(lib.Janela.ui.raio2.text())
    r1b = float(lib.Janela.ui.raio1b.text())
    r2b = float(lib.Janela.ui.raio2b.text())
    TipoIma = lib.Janela.ui.TipoIma.currentIndex()
    volta_filtro = int(lib.Janela.ui.filtro_voltas.text())
    aux = []
    
    ### Organiza dados para cálculos
    for i in range(int(lib.voltas_offset)):
        aux.append(pontos[i*lib.pontos_integracao:(i+1)*lib.pontos_integracao])
    aux.pop(0)  ### despreza primeira volta de aceleração
    lib.pontos = aux
    dados = numpy.array(aux)*10**(-12)  ##Converte dados.

############### Filtro Erro de Transmissão ###############
    volta_total = len(dados)
    filtro = len(dados)-1
    while (volta_total > filtro):
        dados_std = numpy.std(dados,axis=0) # redefines std values
        locsj = numpy.argmax(dados_std) # searches for max std
        avg_std = numpy.mean(dados_std) #average of rms values
        locsi = numpy.argmax(abs(numpy.mean(dados[::,locsj])-dados[::,locsj])) #searches in which column is the max values
        dados = numpy.delete(dados,locsi,0) #deletes the data set with max std
        lib.pontos = numpy.delete(lib.pontos,locsi,0)
        volta_total = volta_total-1
############### Filtro Erro de Transmissão ###############


##### Dados finais apos filtro de erro de leitura #####
    F = numpy.zeros(len(dados)).tolist()
    for i in range(len(dados)):
        F[i] = (numpy.fft.fft(dados[i]))/(len(dados[i])/2)
    lib.F = numpy.array(F)                              # F contem as transformadas de fourier de cada volta

    iNumeroColetas = len(lib.F)
    dtheta = 2*numpy.pi/len(lib.F[0])
    
    if len(lib.F[0])>16:
        nmax = 21
    else:
        nmax = 9

    if TipoIma != 0:
        volta_total = len(lib.F)
        while volta_total > volta_filtro:
            lib.AnguloVolta = numpy.zeros(len(lib.F))
            for i in range(len(lib.F)):
                n = TipoIma
                if lib.Bucked:
                    R = Ne*(r2**n-r1**n)-Neb*(r2b**n-r1b**n)
                else:
                    R = Ne*(r2**n-r1**n)

                An = lib.F[i][n].real
                Bn = -lib.F[i][n].imag
                Jn = (An*numpy.sin(n*dtheta) + Bn*(numpy.cos(n*dtheta)-1))/(2*R*(numpy.cos(n*dtheta)-1))
                Kn = (Bn*numpy.sin(n*dtheta)-An*(numpy.cos(n*dtheta)-1))/(2*R*(numpy.cos(n*dtheta)-1))
                lib.AnguloVolta[i] = (1/TipoIma)*numpy.arctan(Jn/Kn)
                
            maior = numpy.argmax(abs(numpy.mean(lib.AnguloVolta) - lib.AnguloVolta),0)
            lib.AnguloVolta = numpy.delete(lib.AnguloVolta,maior,0)
            lib.F = numpy.delete(lib.F,maior,0)
            dados = numpy.delete(dados,maior,0)
            lib.pontos = numpy.delete(lib.pontos,maior,0)
            volta_total-=1

    iNumeroColetas = len(lib.F)
    dtheta = 2*numpy.pi/len(lib.F[0])
    lib.AnguloVolta = numpy.zeros(len(lib.F))
    lib.SJN = numpy.zeros(21)
    lib.SKN = numpy.zeros(21)
    lib.SNn = numpy.zeros(21)
    lib.SNn2 = numpy.zeros(21)
    lib.SSJN2 = numpy.zeros(21)
    lib.SSKN2 = numpy.zeros(21)
    lib.SdbdXN = numpy.zeros(21)
    lib.SdbdXN2 = numpy.zeros(21)
    for i in range(len(lib.F)):
        for n in range(1,nmax,1):
            if lib.Bucked and n==2:
                n+=1
                continue
            if lib.Bucked:
                R = Ne*(r2**n-r1**n)-Neb*(r2b**n-r1b**n)
            else:
                R = Ne*(r2**n-r1**n)

            An = lib.F[i][n].real
            Bn = -lib.F[i][n].imag
            Jn = (An*numpy.sin(n*dtheta) + Bn*(numpy.cos(n*dtheta)-1))/(2*R*(numpy.cos(n*dtheta)-1))
            Kn = (Bn*numpy.sin(n*dtheta)-An*(numpy.cos(n*dtheta)-1))/(2*R*(numpy.cos(n*dtheta)-1))

            dbdXN = n*(Jn**2+Kn**2)**(1/2)
            lib.SJN[n] = lib.SJN[n] + Jn
            lib.SKN[n] = lib.SKN[n] + Kn
            lib.SSJN2[n] = lib.SSJN2[n] + Jn**2
            lib.SSKN2[n] = lib.SSKN2[n] + Kn**2
            lib.SdbdXN[n] = lib.SdbdXN[n] + dbdXN
            lib.SdbdXN2[n] = lib.SdbdXN2[n] + dbdXN**2
            if n == TipoIma:
                lib.AnguloVolta[i] = (1/TipoIma)*numpy.arctan(Jn/Kn)
        
##### Calculo Desvio Padrao das Medidas #####
    lib.sDesv = numpy.zeros(21)
    lib.sDesvSn = numpy.zeros(21)
    lib.sDesvNn = numpy.zeros(21)
    lib.Nn = numpy.zeros(21)
    lib.Sn = numpy.zeros(21)
    lib.angulo = numpy.zeros(21)
    lib.SMod = numpy.zeros(21)
    for i in range(1,nmax,1):
        lib.sDesv[i] = ((lib.SdbdXN2[i] - lib.SdbdXN[i]**2/iNumeroColetas)/(iNumeroColetas-1))**(1/2)
        lib.sDesvSn[i] = ((((i**2)*lib.SSJN2[i]) - (i*lib.SJN[i])**2/iNumeroColetas)/(iNumeroColetas-1))**(1/2)
        lib.sDesvNn[i] = ((((i**2)*lib.SSKN2[i]) - (i*lib.SKN[i])**2/iNumeroColetas)/(iNumeroColetas-1))**(1/2)
        lib.Nn[i] = (lib.SKN[i]/iNumeroColetas)*i
        lib.Sn[i] = (lib.SJN[i]/iNumeroColetas)*i
        lib.SMod[i] = ((lib.Nn[i]**2)+(lib.Sn[i]**2))**0.5              #Modulo dos valores finais de Nn e Sn
        lib.angulo[i] = (1/i)*numpy.arctan(lib.Sn[i]/lib.Nn[i])

##### Calculo da Correçao para Tipo de Ima #####
    lib.Nnl = numpy.zeros(21)
    lib.Snl = numpy.zeros(21)
    for i in range(1,nmax,1):
        if TipoIma == 0:
            lib.Nnl[i] = lib.Nn[i]
            lib.Snl[i] = lib.Sn[i]
        else:
            lib.Nnl[i] = lib.Nn[i]*numpy.cos(i*lib.angulo[TipoIma])+lib.Sn[i]*numpy.sin(i*lib.angulo[TipoIma])
            lib.Snl[i] = lib.Sn[i]*numpy.cos(i*lib.angulo[TipoIma])-lib.Nn[i]*numpy.sin(i*lib.angulo[TipoIma])

##    for i in range(1,nmax,1):
##        if lib.sDesv[TipoIma] > 0.0001:
##            QtGui.QMessageBox.information(lib.Janela,'Aviso.','Desvio Padrão acima do esperado.\nRefazer medição.',QtGui.QMessageBox.Ok) # Provisório: verificação de erro de leitura.
##            lib.Janela.ui.tabWidget.setTabEnabled(const.numero_de_abas-1,True)
##            lib.Janela.ui.groupBox_2.setEnabled(True)
##            lib.Janela.ui.coletar.setEnabled(True)
##            return
    
                                                                                                 
    # Plota os graficos na aba de resultados e habilita botoes de coleta                                                                                             
    lib.media = numpy.mean(dados, axis =0)
    if Repeticao == 1:
        x = numpy.linspace(0,1,len(lib.media))
        x2 = numpy.linspace(0,1,(len(dados[0])*len(dados)+10))  ## substituido pontos por dados
        lib.Janela.PlotFunc1(x,lib.media)
        lib.Janela.PlotFunc3(x2,dados)
        lib.Janela.ui.tabWidget.setTabEnabled(const.numero_de_abas-1,True)
        lib.Janela.ui.groupBox_2.setEnabled(True)
        lib.Janela.ui.coletar.setEnabled(True)
        QtGui.QMessageBox.warning(lib.Janela,'Aviso.','Dados transferidos com sucesso.',QtGui.QMessageBox.Ok)







# ____________________________________________

class leitura_corrente(threading.Thread):
    def __init__(self, nVoltas, velocidade,fator_fonte):
        threading.Thread.__init__(self)
        self.nVoltas = int(nVoltas)
        self.velocidade = float(velocidade)
        if (lib.Janela.ui.tabWidget.isTabEnabled(3) == True): 
            self.fator = float(fator_fonte)
        else:
            self.fator = 1
        self.start()
        
    def run(self):
        saida = []
        if (lib.Janela.ui.tabWidget.isTabEnabled(3) == True): 
            for i in range(self.nVoltas):
                saida.append((lib.PUC.ReadAD()*self.fator))
                time.sleep(1/self.velocidade)
        else:
            for i in range(self.nVoltas):
                saida.append(0)
        self.saida = saida



# ____________________________________________
# Objeto da janela de programa
class screen(object):
    def __init__(self):
        app = QtGui.QApplication(sys.argv)
        lib.Janela = JanelaGrafica()
        lib.Janela.show()
        time.sleep(0.5)
        app.exec_()
# ____________________________________________



# ____________________________________________
if __name__ == '__main__':
    tela = screen()
    lib.parartudo = 1
    print(threading.activeCount())

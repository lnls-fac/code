# -*- coding: utf-8 -*-
"""
Created on 11/01/2013
Versão 1.0
@author: James Citadini
"""
# Importa bibliotecas
import serial
import time
import threading
# ******************************************

class SerialCom(threading.Thread):
    def __init__(self,porta):
        threading.Thread.__init__(self)
        self.porta = porta
        self.ser = serial.Serial(self.porta-1)
        self.start()

    def callback(self):
        self._stop()

    def run(self):
        self.Comandos()
        
    def Comandos(self):
        CR = '\r'

        #Biblioteca Integrador
        self.PDIProcuraIndice    = 'IND'         #Habilita a procura de indice do integrador
        self.PDIIniciaColeta     = 'RUN'         #Inicia coleta com o integrador
        self.PDIParaColeta       = 'BRK'         #Para coleta com o integrador
        self.PDILerStatus        = 'STB,'        #Le status do integrador
        self.PDIBuscaResultados  = 'ENQ'         #Busca Resultados do integrador
        self.PDIEscolheCanal     = 'CHA,A'       #Escolha de Canal
        self.PDIConfiguraGanho   = 'SGA,A,'      #Configura ganho integrador
        self.PDIClearStatus      = 'CRV,A'       #Limpa Saturacao
        self.PDITipodeTrigger    = 'TRS,E,'      #Tipo de Trigger
        self.PDISequenciaTrigger0= 'TRI,-,'      #Sequencia Trigger -
        self.PDISequenciaTrigger1= 'TRI,+,'      #Sequencia Trigger +
        self.PDIArmazenaBloco    = 'IMD,0'       #Configura Dados para serem armazenados em blocos
        self.PDIArmazena         = 'CUM,0'       #Configura Dados para serem armazenados
        self.PDIZerarContador    = 'ZCT'         #Zerar contador de pulsos
        self.PDIEndofData        = 'EOD'         #End of Data
        self.PDISincroniza       = 'SYN,1'       #Sincroniza
        self.PDICurtoCircuito    = 'ADJ,A,1'     #Curto Integrador
        self.PDILerEncoder       = 'RCT'         #Leitura Pulso Encoder
        self.PDIEnquiry          = 'ENQ'         #Requisitar Resultados
        
    def Conectar(self):
        self.ser.baudrate = 9600
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.parity = serial.PARITY_NONE
        self.ser.timeout = 0.01
        if not self.ser.isOpen():
            self.ser.open()
            
    def Desconectar(self):
        self.ser.close()
        
    def LimpaTxRx(self):
        self.ser.flushInput()
        self.ser.flushOutput()

    def Enviar(self,comando):
        self.LimpaTxRx()
        ajuste = comando + '\r'
        self.ser.write(ajuste.encode('utf-8'))

    def Ler(self,n):
        try:
            leitura = self.ser.read(n)
            leitura = leitura.decode('utf-8')
            leitura = leitura.replace('\r\n','')
        except:
            leitura = ''

        return leitura

    def Status(self,registrador):
        self.Enviar(self.PDILerStatus + registrador)
        time.sleep(0.1)
        leitura = self.Ler(10)
        return leitura

    def Configurar_Integrador(self, sentido, ganho, pontos_integracao, pulsos_encoder, pulsos_trigger, voltas_offset):
        tempoespera = 0.1
        # Cálculo do intervalo de integração
        IntervaloIntegrador = int(int(pulsos_encoder) / int(pontos_integracao))

        # Parar todas as coletas e preparar integrador
        self.Enviar(self.PDIParaColeta)
        time.sleep(tempoespera)

##        # Configurar Canal a ser utilizado - Fixo no canal A
##        self.Enviar(self.PDIEscolheCanal)
##        time.sleep(tempoespera)

        # Configurar Tipo de encoder e n pulsos
        self.Enviar(self.PDITipodeTrigger + str(int(int(pulsos_encoder)/4)))
        time.sleep(tempoespera)

        # Configurar intervalo e direção do trigger
        if sentido == '-':
            ajuste = self.PDISequenciaTrigger0 + \
                                   str(pulsos_trigger) + '/' + \
                                   str(int(pontos_integracao)*int(voltas_offset)) + ',' + \
                                   str(IntervaloIntegrador)

            self.Enviar(ajuste)
            time.sleep(tempoespera)
        else:
            ajuste = self.PDISequenciaTrigger1 + \
                                   str(pulsos_trigger) + '/' + \
                                   str(int(pontos_integracao)*int(voltas_offset)) + ',' + \
                                   str(IntervaloIntegrador)

            self.Enviar(ajuste)
            time.sleep(tempoespera)

        # Configurar para armazenamento em bloco
        self.Enviar(self.PDIArmazenaBloco)
        time.sleep(tempoespera)

        # Preparar para armazenamento
        self.Enviar(self.PDIArmazena)
        time.sleep(tempoespera)

        # Configurar End of Data
        self.Enviar(self.PDIEndofData)
        time.sleep(tempoespera)

##        # Sincronismo GPIB - not in use
##        self.Enviar(self.PDISincroniza)
##        time.sleep(tempoespera)

        # Parar todas as coletas e preparar integrador
        self.Enviar(self.PDIConfiguraGanho + str(ganho))
        time.sleep(tempoespera)

        # Aumentar a resolução
        self.Enviar('FCT,1E12')
        time.sleep(tempoespera)


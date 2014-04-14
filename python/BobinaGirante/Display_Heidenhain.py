# -*- coding: utf-8 -*-
"""
Created on 28/08/2012
Versão 1.0
@author: James Citadini
"""
# Importa bibliotecas
import time
import serial
import ctypes
import threading
# ******************************************
MessageBox = ctypes.windll.user32.MessageBoxW

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
         #Constantes de comandos da Régua Digital
        self.Converte_metros_mm   = 1000 #

        self.Zero0      = '\x1bT0000\r' # {Tecla 0}
        self.Um1        = '\x1bT0001\r' # {Tecla 1}
        self.Dois2      = '\x1bT0002\r' # {Tecla 2}
        self.Tres3      = '\x1bT0003\r' # {Tecla 3}
        self.Quatro4    = '\x1bT0004\r' # {Tecla 4}
        self.Cinco5     = '\x1bT0005\r' # {Tecla 5}
        self.Seis6      = '\x1bT0006\r' # {Tecla 6}
        self.Sete7      = '\x1bT0007\r' # {Tecla 7}
        self.Oito8      = '\x1bT0008\r' # {Tecla 8}
        self.Nove9      = '\x1bT0009\r' # {Tecla 9}
        self.CL         = '\x1bT0100\r' # {Tecla CL}
        self.Menos      = '\x1bT0101\r' # {Tecla -}
        self.Ponto      = '\x1bT0102\r' # {Tecla .}
        self.Ent        = '\x1bT0104\r' # {Tecla Ent}
        self.Eixo12     = '\x1bT0107\r' # {Tecla 1/2}
        self.EixoX      = '\x1bT0109\r' # {Tecla X}
        self.EixoY      = '\x1bT0110\r' # {Tecla Y}
        self.EixoZ      = '\x1bT0111\r' # {Tecla Z}
        self.Spec       = '\x1bT0129\r' # {Tecla Spec Fct}
        self.Rpn        = '\x1bT0142\r' # {Tecla R+/-}

        self.CEZero0    = '\x1bT1000\r' # {Tecla CE+0}
        self.CEUm1      = '\x1bT1001\r' # {Tecla CE+1}
        self.CEDois2    = '\x1bT1002\r' # {Tecla CE+2}
        self.CETres3    = '\x1bT1003\r' # {Tecla CE+3}
        self.CEQuatro4  = '\x1bT1004\r' # {Tecla CE+4}
        self.CECinco5   = '\x1bT1005\r' # {Tecla CE+5}
        self.CESeis6    = '\x1bT1006\r' # {Tecla CE+6}
        self.CESete7    = '\x1bT1007\r' # {Tecla CE+7}
        self.CEOito8    = '\x1bT1008\r' # {Tecla CE+8}
        self.CENove9    = '\x1bT1009\r' # {Tecla CE+9}

        self.Modelo     = '\x1bA0000\r' # {Output of model designation}
        self.Segm       = '\x1bA0100\r' # {Output of 14-segment display}
        self.Valor      = '\x1bA0200\r' # {Output of current value}
        self.Error      = '\x1bA0301\r' # {Output of error text}
        self.Soft       = '\x1bA0400\r' # {Output of software number}
        self.Ind        = '\x1bA0900\r' # {Output of indicators}

        self.ResetRegua = '\x1bS0000\r' # {Counter RESET}
        self.Lock       = '\x1bS0001\r' # {Lock keyboard}
        self.Unlock     = '\x1bS0002\r' # {Unlock keyboard}

        # Variável de leitura
        self.DisplayPos = (0,0,0)

    def Conectar(self):
        self.ser.baudrate = 9600
        self.ser.bytesize = serial.SEVENBITS
        self.ser.stopbits = serial.STOPBITS_TWO
        self.ser.parity = serial.PARITY_EVEN#PARITY_NONE
        self.ser.timeout = 0.5
        if not self.ser.isOpen():
            self.ser.open()

    def Desconectar(self):
        self.ser.close()

    def LimpaTxRx(self):
        self.ser.flushInput()
        self.ser.flushOutput()

    def LimpaString(self,leitura):
        leitura = leitura.replace('\'','')
        leitura = leitura.replace('\\x82','')
        leitura = leitura.replace('\\x8d','')
        leitura = leitura.replace('\\','')
        leitura = leitura.replace('xb','')
        leitura = leitura.replace('b','')
        return leitura

    def EscreveValorDisplay(self,Eixo,Valor):
        # Converte para string
        aux = str(abs(Valor))
        nchar = len(aux)

        self.LimpaTxRx()
        time.sleep(0.2)
        self.ser.write(self.CL.encode('utf-8'))
        time.sleep(0.2)

        if Eixo == 0:
            self.ser.write(self.EixoX.encode('utf-8'))
        elif Eixo == 1:
            self.ser.write(self.EixoY.encode('utf-8'))
        elif Eixo == 2:
            self.ser.write(self.EixoZ.encode('utf-8'))

        time.sleep(0.2)

        # Identifica e escreve
        for i in range(nchar):
            self.LimpaTxRx()
            tmp = aux[i]
            if (tmp == '0'):
                ajuste = self.Zero0
            elif (tmp == '1'):
                ajuste = self.Um1
            elif (tmp == '2'):
                ajuste = self.Dois2
            elif (tmp == '3'):
                ajuste = self.Tres3
            elif (tmp == '4'):
                ajuste = self.Quatro4
            elif (tmp == '5'):
                ajuste = self.Cinco5
            elif (tmp == '6'):
                ajuste = self.Seis6
            elif (tmp == '7'):
                ajuste = self.Sete7
            elif (tmp == '8'):
                ajuste = self.Oito8
            elif (tmp == '9'):
                ajuste = self.Nove9
            elif (tmp == '.'):
                ajuste = self.Ponto
            self.ser.write(ajuste.encode('utf-8'))
            time.sleep(0.2)

        if Valor < 0:
            self.ser.write(self.Menos.encode('utf-8'))
            time.sleep(0.2)

        # Enter
        self.ser.write(self.Ent.encode('utf-8'))

    def LerDisplay(self):
        try:
            ajuste = self.Valor
            self.LimpaTxRx()
            self.ser.write(ajuste.encode('utf-8'))
            time.sleep(0.1)
            leitura = str(self.ser.read(40))

            #Converte para string e limpa lixo
            leitura = self.LimpaString(leitura)
##            print(leitura)

            #Converte para float
            p1 = leitura.find('rn')
            leitura1 = float(leitura[p1-10:p1])/1000
            leitura = leitura[p1+1:]

            p2 = leitura.find('rn')
            leitura2 = float(leitura[p2-10:p2])/1000
            leitura = leitura[p2+1:]

            p3 = leitura.find('rn')
            leitura3 = float(leitura[p3-10:p3])/1000
        except:
            leitura1 = 0
            leitura2 = 0
            leitura3 = 0

        self.DisplayPos = (leitura1,leitura2,leitura3)

    def Reset_SetRef_Display(self):
        # Envia comando de reset
        self.LimpaTxRx()
        time.sleep(0.2)
        self.ser.write(self.ResetRegua.encode('utf-8'))

        # Aguarda 3 segundos o processo de reset to display
        time.sleep(4)

        # Envia enter para buscar referência
        self.LimpaTxRx()
        time.sleep(0.2)
        self.ser.write(self.Ent.encode('utf-8'))
        time.sleep(0.2)

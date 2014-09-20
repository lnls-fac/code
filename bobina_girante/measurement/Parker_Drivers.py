# -*- coding: utf-8 -*-
"""
Created on 28/08/2012
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
        self.Mover  = 'G' # {Comando para mover motor}
        self.Parar  = 'S' # {Comando para parar motor}
        self.Dist   = 'D' # {Comando para parar motor}
        self.Vel    = 'V' # {Velocidade motor}
        self.Ace    = 'A' # {Aceleração motor}
        self.status = 'R' # {Aceleração motor}
        self.modocont = 'MC' # {Aceleração motor}
        self.modomanual = 'MN' # {Aceleração motor}
        self.sentido = 'H' # {Aceleração motor}
        self.FimdeCurso_Off = 'LD3' # {Desabilita Fim de Curso}
        self.FimdeCurso_On = 'LD0' # {Habilita Fim de Curso}
        self.kill = 'K' # {Parada de emergencia}
        self.setResolucao = 'MR' # {setar resolução do motor}
        
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
    def ConfModo(self,EndDriver,Modo,Sentido):
        self.LimpaTxRx()
        # Ajusta Modo Manual ou Cotinuo
        if ((Modo == 0) or (Modo == 'Manual')):
            ajuste = str(EndDriver) + self.modomanual + '\r'
        elif ((Modo == 1) or (Modo == 'Continuo')):
            ajuste = str(EndDriver) + self.modocont + '\r'

        self.ser.write(ajuste.encode('utf-8'))
        leitura = self.ser.read(100)

        # Ajusta Sentido
        if ((Sentido == 0) or (Sentido == 'Horario')):
            ajuste = str(EndDriver) + self.sentido + '+\r'
        elif ((Sentido == 1) or (Sentido == 'AntiHorario')):
            ajuste = str(EndDriver) + self.sentido + '-\r'

        self.ser.write(ajuste.encode('utf-8'))
        leitura = self.ser.read(100)
            
    def ConfMotor(self,EndDriver,Vel,Ace,Passos):
        self.LimpaTxRx()

        # Habilita Fim de Curso
        ajuste = str(EndDriver) + self.FimdeCurso_On + '\r'
        self.ser.write(ajuste.encode('utf-8'))
        leitura = self.ser.read(100)

        # Configura Driver
        ajuste = str(EndDriver) + self.modomanual + '\r'
        self.ser.write(ajuste.encode('utf-8'))
        leitura = self.ser.read(100)
        
        ajuste = str(EndDriver) + self.Vel + str(Vel) + '\r'
        self.ser.write(ajuste.encode('utf-8'))
        leitura = self.ser.read(100)
        
        ajuste = str(EndDriver) + self.Ace + str(Ace) + '\r'
        self.ser.write(ajuste.encode('utf-8'))
        leitura = self.ser.read(100)

        ajuste = str(EndDriver) + self.Dist + str(Passos) + '\r'
        self.ser.write(ajuste.encode('utf-8'))
        leitura = self.ser.read(100)

    def MoverMotorFimdeCursoPos(self,EndDriver,Vel=1,Ace=1):
        # Move Fim de Curso Positivo
        self.LimpaTxRx()        
        ajuste = str(EndDriver) + self.Vel + str(Vel) + '\r'
        self.ser.write(ajuste.encode('utf-8'))
        leitura = self.ser.read(100)
        
        ajuste = str(EndDriver) + self.Ace + str(Ace) + '\r'
        self.ser.write(ajuste.encode('utf-8'))
        leitura = self.ser.read(100)

        ajuste = str(EndDriver) + self.modocont + '\r'
        self.ser.write(ajuste.encode('utf-8'))
        leitura = self.ser.read(100)

        ajuste = str(EndDriver) + self.sentido + '-\r'
        self.ser.write(ajuste.encode('utf-8'))
        leitura = self.ser.read(100)

        self.MoverMotor(EndDriver)

    def MoverMotorFimdeCursoNeg(self,EndDriver,Vel=1,Ace=1):
        # Move Fim de Curso Nagativo
        self.LimpaTxRx()        
        ajuste = str(EndDriver) + self.Vel + str(Vel) + '\r'
        self.ser.write(ajuste.encode('utf-8'))
        leitura = self.ser.read(100)
        
        ajuste = str(EndDriver) + self.Ace + str(Ace) + '\r'
        self.ser.write(ajuste.encode('utf-8'))
        leitura = self.ser.read(100)

        ajuste = str(EndDriver) + self.modocont + '\r'
        self.ser.write(ajuste.encode('utf-8'))
        leitura = self.ser.read(100)

        ajuste = str(EndDriver) + self.sentido + '+\r'
        self.ser.write(ajuste.encode('utf-8'))
        leitura = self.ser.read(100)

        self.MoverMotor(EndDriver)

    def PararMotor(self,EndDriver):
        self.LimpaTxRx()
        # Para o motor
        ajuste = str(EndDriver) + self.Parar + '\r'
        self.ser.write(ajuste.encode('utf-8'))
        leitura = self.ser.read(100)

    def MoverMotor(self,EndDriver):
        self.LimpaTxRx()
        # Mover o motor n passos
        ajuste = str(EndDriver) + self.Mover + '\r'
        self.ser.write(ajuste.encode('utf-8'))
        leitura = self.ser.read(100)

    def ready(self,EndDriver):
        self.LimpaTxRx()
        ajuste = str(EndDriver) + self.status + '\r'
        self.ser.write(ajuste.encode('utf-8'))
        time.sleep(0.01)
        leitura = str(self.ser.read(100))
        if ( (leitura.find('*R') >= 0) or (leitura.find('*S') >= 0)):
            return True
        else:
            return False

    def Kill(self):
        ajuste = self.kill + '\r'
        self.ser.write(ajuste.encode('utf-8'))
        leitura = self.ser.read(100)

    def SetResolucao(self,EndDriver,Resolucao):
        ajuste = str(EndDriver) + self.setResolucao + str(int(Resolucao)) + '\r'
        self.ser.write(ajuste.encode('utf-8'))
        time.sleep(0.01)
        leitura = str(self.ser.read(100))
        

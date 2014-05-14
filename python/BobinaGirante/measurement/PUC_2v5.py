#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 06/12/2013
Versão 2.5
@author: Ariane Taffarello
Python 3.2.3 32 bits
PUC 1DA/1AD + 1I8bits/1O8bits
Firmware PUC Mag v2.2 1 Mbps
"""
# Importa bibliotecas
import serial, time, sys, math
from hashlib import md5
# ******************************************

class SerialCom(object):
    
    def __init__(self,PUCaddr):
        # Endereço da PUC
        self.PUCaddress = PUCaddr
        self.Status = ''
        self.SYNC_CONFIG_id = None
        self.SYNC_ENABLE_id = None
        self.SYNC_STATUS_id = None
        self.AD_id = None
        self.DA_id = None
        self.DIGIN_id = None
        self.DIGOUT_id = None
        self.FLASH_id = None
        self.RAM_id = None
        self.FLASH_maxPoints = None
        self.RAM_maxPoints = None
        self.Comandos()
        self.Var_type()

    def Comandos(self):
        # Constamntes de comando da PUC
        self.QUERY_STATUS                    = 0x00
        self.STATUS                          = 0x01
        self.QUERY_VARS_LIST                 = 0x02
        self.VARS_LIST                       = 0x03
        self.QUERY_GROUPS_LIST               = 0x04
        self.GROUPS_LIST                     = 0x05
        self.QUERY_GROUP                     = 0x06
        self.GROUP                           = 0x07
        self.QUERY_CURVES_LIST               = 0x08
        self.CURVES_LIST                     = 0x09
        self.QUERY_CHECKSUM                  = 0x0A
        self.CHECKSUM                        = 0x0B

        self.READ_VAR                        = 0x10
        self.VAR_READING                     = 0x11
        self.READ_GROUP                      = 0x12
        self.GROUP_READING                   = 0x13

        self.WRITE_VAR                       = 0x20
        self.WRITE_GROUP                     = 0x22

        self.CREATE_GROUP                    = 0x30
        self.GROUP_CREATED                   = 0x31
        self.REMOVE_ALL_GROUPS               = 0x32

        self.CURVE_TRANSMIT                  = 0x40
        self.CURVE_BLOCK                     = 0x41
        self.CURVE_RECALC_CSUM               = 0x42

        self.OK                              = 0xE0
        self.ERR_MALFORMED_MESSAGE           = 0xE1
        self.ERR_OP_NOT_SUPPORTED            = 0xE2
        self.ERR_INVALID_ID                  = 0xE3
        self.ERR_INVALID_VALUE               = 0xE4
        self.ERR_INVALID_PAYLOAD_SIZE        = 0xE5
        self.ERR_READ_ONLY                   = 0xE6
        self.ERR_INSUFFICIENT_MEMORY         = 0xE7
        self.ERR_INTERNAL                    = 0xE8

    def Var_type(self):
        self.CONFIG_SYNC     = 0x85
        self.DIGIN           = 0x01
        self.ADC             = 0x03
        self.DIGOUT          = 0x81
        self.DAC             = 0x83
    
    def Conectar(self, port,baud=1000000,tout=2.0):
        try:
            port = 'COM'+str(port)
            self.serial = serial.Serial(port, baud, timeout=tout)
            if not self.serial.isOpen():
                self.serial.open()
        
            self.Status = 'Conectado'
            if not self.CheckVariables(): return False
            if not self.CheckCurves(): return False
            return True
        except:
            return False

    def Desconectar(self):
        self.serial.close()

    def Command(self, cmd_code, payload=[]):
        # Monta o pacote envia e recebe a resposta
        pkt = self.SimplePacket(cmd_code)
        pkt[3] = 0xFF if cmd_code == self.CURVE_BLOCK else len(payload)
        pkt = pkt + payload
        self.SendPacket(pkt)
        pkt = self.RecvPacket()
        if pkt==[]: return False
        return pkt[4:]

    def ReadDA(self):
        # Lê o DA
        raw_value = self.Command(self.READ_VAR, [self.DA_id])
        value = self.From_2s_complement(raw_value)
        return value

    def ReadDigOut(self):
        # Lê a Saída Digital
        value = self.Command(self.READ_VAR, [self.DIGOUT_id])[0]
        return value

    def ReadAD(self):
        # Lê o AD
        raw_value = self.Command(self.READ_VAR, [self.AD_id])
        raw_value = (raw_value[0] << 16) + (raw_value[1] << 8) + raw_value[2]
        value = raw_value*20 / 262143-10
        return value

    def ReadDigIn(self):
        # Lê a Entrada Digital
        value = self.Command(self.READ_VAR, [self.DIGIN_id])[0]
        return value

    def WriteDigBit(self,port,value):
        # Escreve em um bit digital
        # Lê a saída atual
        outnow = self.ReadDigOut()
        if port == 0:
            if value == 0:
                outnew = 0b11111110 & outnow
            else:
                outnew = 0b00000001 | outnow
        elif port == 1:
            if value == 0:
                outnew = 0b11111101 & outnow
            else:
                outnew = 0b00000010 | outnow
        elif port == 2:
            if value == 0:
                outnew = 0b11111011 & outnow
            else:
                outnew = 0b00000100 | outnow
        elif port == 3:
            if value == 0:
                outnew = 0b11110111 & outnow
            else:
                outnew = 0b00001000 | outnow
        elif port == 4:
            if value == 0:
                outnew = 0b11101111 & outnow
            else:
                outnew = 0b00010000 | outnow
        elif port == 5:
            if value == 0:
                outnew = 0b11011111 & outnow
            else:
                outnew = 0b00100000 | outnow
        elif port == 6:
            if value == 0:
                outnew = 0b10111111 & outnow
            else:
                outnew = 0b01000000 | outnow
        elif port == 7:
            if value == 0:
                outnew = 0b01111111 & outnow
            else:
                outnew = 0b10000000 | outnow
        else:
            return False
        self.WriteDig(outnew)
        return True
        

    def WriteDig(self,value):
        # Escreve na Saída Digital
        # Garante um máximo de 8 bits
        value = value & 0xFF
        self.Command(self.WRITE_VAR, [self.DIGOUT_id, value])

    def WriteDA(self,value):
        # Escreve no DA
        raw_value = self.To_2s_complement(float(value))
        self.Command(self.WRITE_VAR, [self.DA_id]+raw_value[1:])  #envia 3 bytes

    def SendCurve(self, curva=None):
        # Envia curva - DA
        if not curva:
            return

        # Monta os pacotes - máx de 8 blocos = 65536 pontos de 2 bytes
        blockSize = 16384
        nblocks = len(curva)/blockSize
        for i in range(int(nblocks)):
            payload = [self.FLASH_id, 0, i] + curva[i*blockSize:(i+1)*blockSize]
            self.Command(self.CURVE_BLOCK, payload)

        # Retorna o Checksum da curva recebida
        return self.UpdateChecksumsCurves()

    def ExecuteCurve(self, points=None, CLK_IN_EXT=1, CLK_OUT=1, Flash=1, RAM=1, Dout_bit=0, Loop=0):
        # Executa a curva
        # (nº de pontos, CLK int0/ext1, ..., Dout de 0 a 7)
        if not points:
            return
        if points > 32768: points = 32768
        
        points = [(points >> 24) & 0xFF, (points >> 16) & 0xFF, (points >> 8) & 0xFF, points & 0xFF]

        config = 0
        # Monta a configuração
        if Loop:
            config = config | 0x80
            
        if CLK_IN_EXT:
            config = config | 0x40

        if CLK_OUT:
            config = config | 0x20

        if Flash:
            config = config | 0x10

        if RAM:
            config = config | 0x08

        config = config | Dout_bit

        # Configura
        self.Command(self.WRITE_VAR, [self.SYNC_CONFIG_id, config] + points)
        # Executa
        self.Command(self.WRITE_VAR, [self.SYNC_ENABLE_id, 1])

    def ReadStatusCurve(self):
        status = self.Command(self.READ_VAR, [self.SYNC_STATUS_id])
        st = status[0] != 0
        point = (status[1] << 24) + (status[2] << 16) + (status[3] << 8) + status[4]
        return st, point

    def StopCurve(self):
        # Para a execução de uma curva
        self.Command(self.WRITE_VAR, [self.SYNC_ENABLE_id, 0])

    def ReadCaptured(self):
        # Lê a curva capturada
        capturedCurve = []
        capturedBytes = []

        # Recebe os 8 blocos
        for i in range(8):
            capturedBytes.extend(self.Command(self.CURVE_TRANSMIT, [self.RAM_id, 0, i])[3:])

        if not capturedBytes:
            return

        # Converte de 4 bytes para o valor em tensão
        for i in range(0,len(capturedBytes),4):
            value = ((capturedBytes[i+1]*65536 + capturedBytes[i+2]*256 + capturedBytes[i+3])*20 / 262143) - 10.0
            capturedCurve.append(value)

        return capturedCurve

    def ReadFirstPoint(self):
        # Lê o primeiro ponto da curva a ser executada
        bloco = self.Command(self.CURVE_TRANSMIT, [self.FLASH_id, 0, 0])
        FirstPoint = ((bloco[4]*65536 + bloco[5]*256 + bloco[6])*20/262143)
        return FirstPoint
        
    
    def CalculateGeneratedCsum(self,curva):
        # Calcula o Checksum de uma curva (Alto nível)
        # Cada ponto da curva deve ter 2 bytes = 16 bits
        m=md5()
        aux = list(map(int, curva))
        aux = ''.join(list(map(chr,aux)))
        m.update(aux.encode('latin1'))
        genCsum = m.hexdigest()
        return genCsum

    def UpdateChecksumsCurves(self, curves = []):
        # Lê o Checksum da curva DA da PUC
        # Flash DA
        if self.FLASH_id != None:
            flashChecksum = self.Command(self.CURVE_RECALC_CSUM, [self.FLASH_id])
            flashChecksum = ''.join(list(map(lambda x: '%02x' % x,flashChecksum)))
            return flashChecksum

    def SimplePacket(self, cmd):
        # Forma o pacote mínimo
        # Destino|Origem=0|Comando|Tamanho=0
        try:
            return [int(self.PUCaddress), 0, cmd, 0]
        except ValueError:
            self.Status = 'Endereço da PUC '+str(self.PUCaddress)+' inválido'
            return []

    def SendPacket(self, packet):
        # Adiciona o checksum e envia
        # soma o pacote e pega o byte menos significativo
        csum = int(sum(packet)) & 0xFF
        #calcula o checksum
        csum = 0x100 - csum
        csum = csum & 0xFF
        aux = list(map(int, packet+[csum]))
        aux = bytes(aux)
        self.serial.write(aux)

    def RecvPacket(self):
        # Recebe o cabeçalho |Destino|Origem|Comando|Tamanho|
        header = list(map(int, self.serial.read(4)))

        if not header:
            self.Status = 'Check packet: EMPTY ANSWER'
            print(self.Status)
            return []

        body = []
        # Se o |Tamanho| != 0
        if header[3]:
            if header[3] == 255:
                body = list(map(int, self.serial.read(16387)))
            else:
                body = list(map(int, self.serial.read(header[3])))

        # checksum
        csum = list(map(int, self.serial.read(1)))

        #verifica checksum
        if not self.CheckPacket(header+body+csum):
            return []
        
        return header+body

    def CheckPacket(self, packet):
        return_value = True
        message = ''

        # Testa possíveis erro e verifica checksum
        if len(packet) == 0:
            message = 'Check packet: EMPTY ANSWER'
            return_value = False
        elif len(packet) < 4:
            message = 'Check packet: MALFORMED MESSAGE'
            return_value = False
        elif sum(packet) & 0xFF != 0x00:
            message = 'Check packet: CHECKSUM MISMATCH'
            return_value = False
        else:
            pkt_len = 0
            raw_len = packet[3]

            if raw_len == 255:
                pkt_len = 16387
            else:
                pkt_len = raw_len

            pkt_len = pkt_len + 5 # src dst cmd size csum

            if pkt_len != len(packet):
                message = 'Check packet: LENGTH MISMATCH'
                return_value = False
            #elif packet[2] > self.OK:
                #message = "Check packet: ERR:"+error_message[packet[2]]
                #return_value = False

        # Se encontrar falha
        if message:
##            print (message)
            self.Status = message
            
        return return_value

    def CheckVariables(self):
        # Verifica a lista de variáveis
        vars_list = self.Command(self.QUERY_VARS_LIST)

        if not vars_list:
            self.Status = 'A PUC não contém variáveis!'
            return False

        # Indexa as variáveis
        self.SYNC_CONFIG_id = 0
        self.SYNC_ENABLE_id = 1
        self.SYNC_STATUS_id = 2

        for i, var in enumerate(vars_list[3:]):
            i = i + 3
            if not self.AD_id and var == self.ADC:
                self.AD_id = i
            if not self.DA_id and var == self.DAC:
                self.DA_id = i
            if not self.DIGIN_id and var == self.DIGIN:
                self.DIGIN_id = i
            if not self.DIGOUT_id and var == self.DIGOUT:
                self.DIGOUT_id = i
        return True

    def CheckCurves(self):
        # Verifica a lista de curvas
        # |Tipo|Blocos-1|     Checksum da curva    | = 18 bytes
        curves = self.Command(self.QUERY_CURVES_LIST)

        if not curves:
            self.Status = 'A PUC não contém curvas!'
            return False
        
        # Indexa as curvas
        for i in range(0, len(curves), 3):
            # Flash DA
            if curves[i] != 0 and self.FLASH_id == None:
                self.FLASH_id = int(i/3)
            # RAM AD
            elif curves[i] == 0 and self.RAM_id == None:
                self.RAM_id = int(i/3)
        return True


    def From_2s_complement(self, raw_value):
        # Converte de complemento de 2
        if not raw_value:
            return 0.0

        # Monta o valor decimal de 18 bits
        twos_complement = (raw_value[0] << 16) + (raw_value[1] << 8) + raw_value[2]

        # Limites
        if twos_complement > 262143 or twos_complement < 0:
            return 0.0
        
        # Tensão Negativa/Positiva
        if twos_complement >= 131072:
            twos_complement = twos_complement - 131072
            value = (twos_complement*10.0/131071.0)-10
        else:
            value = twos_complement*10.0/131071.0

        return value

    def To_2s_complement(self, value):
        # Converte para complemento de dois
        # Limites
        if value < -10.0:
            value = -10.0
        elif value > 10.0:
            value = 10.0

        if value < 0.0:
            value = value + 20.0
            twos_complement = int(value*131071.0/10.0)+1
        else:
            twos_complement = int(value*131071.0/10.0)

        # Gera 3 bytes
        return [0, (twos_complement >> 16) & 0xFF, (twos_complement >> 8) & 0xFF, twos_complement & 0xFF]

    def ConverteCurva(self, listapontos):
        curva=[]
        # Converte uma lista de pontos em complemento de 2 com 4 bytes
        for i in listapontos:
            curva.extend(self.To_2s_complement(i))
        return curva

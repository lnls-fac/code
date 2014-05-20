import time

class Lib:
    def __init__(self):
        self.F = [[1,2,3]]
        self.ganho = 100
        self.pontos_integracao = 128
        self.velocidade = 1.0
        self.aceleracao = 0.5

class Test():
    
    def __init__(self):
        pass
    
    def SALVAR_HARMONICO(self):
        
        Auto = 0
        lib = Lib()
        
        data = time.strftime("%d/%m/%Y", time.localtime())
        hora = time.strftime("%H:%M:%S", time.localtime())
        
        if Auto == 0:
            #nome = str(self.ui.Nome_Ima.text())
            #arquivo = QtGui.QFileDialog.getSaveFileName(self, 'Save File', nome,'Data files (*.dat);;Text files (*.txt)')
            arquivo = 'test.txt'
        else:
            arquivo = lib.FileName + '_Medida_' + str(Coleta) + '.dat'
        arquivo_nome = arquivo.replace('/','\\')
        
        try:
            f = open(arquivo,'w')
        except:
            return
        
        # numero de multipolos a serem listados
        if len(lib.F[0])>16:
            Nfinal = 16
        else:
            Nfinal = 8
    
                        
        iNumeroColetas = len(lib.F)
        TipoIma = 0
        
        nome_ima = 'nome_ima'    
        
        # Cabecalho do arquivo
        f.write('### MEDIDA DE BOBINA GIRANTE ###\n')
        f.write('\n')
        f.write('### DADOS DE CONFIGURACAO ###\n')
        f.write('nome_ima                 ' + str(nome_ima) + '\n')
        f.write('arquivo                  ' + str(arquivo_nome) + '\n')
        f.write('data                     ' + str(data) + '\n')
        f.write('hora                     ' + str(hora) + '\n')
        f.write('ganho                    ' + str(lib.ganho) + '\n')
        f.write('nr_pontos_integracao     ' + str(lib.pontos_integracao) + '\n')
        f.write('velocidade               ' + str(lib.velocidade) + '\n')
        f.write('aceleracao               ' + str(lib.aceleracao) + '\n')
        f.write('nr_coletas               ' + str(Coleta) + '\n')
        f.write('nr_voltas                ' + str(lib.voltas_offset + 2) + '\n')
        f.write('intervalo_analise        ' + str(2) + ' ' + str(lib.voltas_offset + 1) + '\n')
        f.write('sentido_rotacao          ' + str(lib.sentido) + '\n')
        f.write('corrente_avg             ' + str('{0:0.5e}'.format(numpy.mean(lib.LeituraCorrente.saida))) + ' [Ampere]\n')
        f.write('corrente_std             ' + str('{0:0.5e}'.format(numpy.mean(lib.LeituraCorrente.saida))) + ' [Ampere]\n')
        f.write('comentarios              ' + str(comentarios) + '\n')
        f.write('\n')
        f.write('### DADOS DE LEITURA ###\n')
        f.write('\n')
        f.write('n   avg_Nn.L[T/m^n-2]  avg_Sn.L[T/m^n-2]  std_Nn.L[T/m^n-2]  std_Sn.L[T/m^n-2]\n') 
              
        if iNumeroColetas >= 1:
            for i in range(1,Nfinal,1):
                f.write(str('{0: <4d}'.format(i)))
                f.write(str('{0: <+19.5e}'.format(lib.Nn[i])))
                f.write(str('{0: <+19.5e}'.format(lib.Sn[i])))
                f.write(str('{0: <+19.5e}'.format(lib.sDesvNn[i])))
                f.write(str('{0: <+19.5e}'.format(lib.sDesvSn[i])))
                f.write('\n')
        f.write('\n')
        
        f.write('### DADOS BRUTOS ARMAZENADOS ###\n')
        for j in range(len(lib.pontos[1])):
            for i in range(len(lib.pontos)):
                f.write(str('{0:+15.8e} '.format(lib.pontos[i][j])))
            f.write('\n')
        f.write('\n') 
    
        f.close()
    
t = Test();
t.SALVAR_HARMONICO()
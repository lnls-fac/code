import numpy
import math
import matplotlib.pyplot as plt
import os

''' color patterns for multipole plots '''
colors_happy   = [(0,0,0), (1,0,0),(0,0,1),(0,0.8,0),(1,0,1),(0,1,1),(1,1,0)]
colors_redline = [(0,0,0), (128,0,0),(165,42,42),(220,20,60),(255,99,71),(205,92,92),(233,150,122),(255,160,122)]
colors_redline = [(1.0*c[0]/255.0,1.0*c[1]/255.0,1.0*c[2]/255.0) for c in colors_redline]
        
        
class multipoles:
    
    def __init__(self, 
                 measurement = None, 
                 harmonics = None, 
                 r0 = None, 
                 main_multipole = None, 
                 absolute_LN_avg = None,
                 absolute_LS_avg = None,
                 absolute_LN_std = None,
                 absolute_LS_std = None,
                 relative_LN_avg = None,
                 relative_LS_avg = None,
                 relative_LN_std = None,
                 relative_LS_std = None,
                 ):
        
        self.measurement     = measurement
        self.harmonics       = harmonics
        self.r0              = r0
        self.main_multipole  = main_multipole
        self.absolute_LN     = None
        self.absolute_LS     = None
        self.skew_angle      = None
        self.absolute_LN_avg = absolute_LN_avg
        self.absolute_LS_avg = absolute_LS_avg
        self.absolute_LN_std = absolute_LN_std
        self.absolute_LS_std = absolute_LS_std
        self.relative_LN_avg = relative_LN_avg
        self.relative_LS_avg = relative_LS_avg
        self.relative_LN_std = relative_LN_std
        self.relative_LS_std = relative_LS_std
        self.skew_angle_avg  = None
        self.skew_angle_std  = None

        
    def __str__(self):
        r = ''
        if self.measurement is not None:
            r += str(self.measurement)
        if self.harmonics is not None:
            r += '{0:30s}: '.format('harmonics') +  str(self.harmonics) + '\n'
        if self.absolute_LN_avg is not None:
            for i in range(len(self.harmonics)):
                n = self.harmonics[i]
                r += '{0:30s}: '.format('abs_mpole  (n={0:02d}) [{1:s}]'.format(n, self.calc_multipole_units(n))) + u'{0:+10.4e} \u00B1 {1:10.4e}'.format(self.absolute_LN_avg[i], self.absolute_LN_std[i]) + ', ' + u'{0:+10.4e} \u00B1 {1:10.4e}'.format(self.absolute_LS_avg[i], self.absolute_LS_std[i]) + '\n'
        if self.skew_angle_avg is not None:
            for i in range(len(self.harmonics)):
                n = self.harmonics[i]
                r += '{0:30s}: '.format('skew_angle (n={0:02d}) [rad]'.format(n)) + u'{0:+10.4e} \u00B1 {1:10.4e}'.format(self.skew_angle_avg[i], self.skew_angle_std[i]) + '\n'     
        if self.r0 is not None:
            r += '{0:30s}: '.format('r0[m]') +  str(self.r0) + '\n'
        if self.main_multipole is not None:
            n = self.main_multipole[0]
            r += '{0:30s}: '.format('main_multipole [{0:s}]'.format(self.calc_multipole_units(n))) +  str(self.main_multipole[1]) + '\n'
        if self.relative_LN_avg is not None:
            for i in range(len(self.harmonics)):
                n = self.harmonics[i]
                r += '{0:30s}: '.format('rel_mpole  (n={0:02d})'.format(n)) + u'{0:+10.4e} \u00B1 {1:10.4e}'.format(self.relative_LN_avg[i], self.relative_LN_std[i]) + ', ' + u'{0:+10.4e} \u00B1 {1:10.4e}'.format(self.relative_LS_avg[i], self.relative_LS_std[i]) + '\n'
        return r
    
    @staticmethod
    def calc_multipole_units(n):
        if (n == 1):
            units = 'T.m'
        elif (n == 2):
            units = 'T'
        elif (n == 3):
            units = 'T/m'
        else:
            units = 'T/m^' + str(n-2)
        return units

    def set_harmonics(self, harmonics):
        self.harmonics = harmonics
        self.calc_absolute_multipoles()
        self.calc_relative_multipoles()
        
    def set_main_multipole(self, order, value):
        self.main_multipole = (order, value)
        self.calc_relative_multipoles()
        
    def set_r0(self, r0):
        self.r0 = r0
        self.calc_relative_multipoles()
            
    def select_main_multipole(self, h):
        
        idx  = self.harmonics.index(h)
        return (h,self.absolute_LN_avg[idx])  
        
    def calc_relative_multipoles(self, r0 = None, main_multipole = None):
        
        if r0 is not None:
            self.r0 = r0
        if main_multipole is not None:
            self.main_multipole = main_multipole    
        if (self.main_multipole is None) or (self.r0 is None):
            return
        if self.absolute_LN_avg is None:
            self.calc_absolute_multipoles()
        
        nr_turns  = self.measurement.nr_turns
        main = self.main_multipole[1] * (self.r0 ** self.main_multipole[0])
        self.relative_LN = numpy.zeros((len(self.harmonics), nr_turns))
        self.relative_LS = numpy.zeros((len(self.harmonics), nr_turns))
        for j in range(len(self.harmonics)):
            n = self.harmonics[j]
            for i in range(nr_turns):
                self.relative_LN[j,i] = self.absolute_LN[j,i] * (self.r0 ** n) / main
                self.relative_LS[j,i] = self.absolute_LS[j,i] * (self.r0 ** n) / main
        
        ''' Calculates average and std of the Normal and Skew relative multipoles '''  
        self.relative_LN_avg  = numpy.mean(self.relative_LN,axis=1)   
        self.relative_LS_avg  = numpy.mean(self.relative_LS,axis=1)
        self.relative_LN_std  = numpy.std(self.relative_LN,axis=1, ddof=1) / numpy.sqrt(nr_turns)
        self.relative_LS_std  = numpy.std(self.relative_LS,axis=1, ddof=1) / numpy.sqrt(nr_turns)
                
    def calc_absolute_multipoles(self):
    
        if self.harmonics is None or self.measurement is None:
            return
        
        Ne = self.measurement.rcoil_Ne # Numero de Espiras
        r1 = self.measurement.rcoil_r1 # Raio interno [m]
        r2 = self.measurement.rcoil_r2 # Raio externo [m]
        nr_points = self.measurement.nr_points
        nr_turns  = self.measurement.nr_turns
        
        ''' Fourier transform of integrated voltage '''
        F = [0] * nr_turns
        for i in range(nr_turns):
            F[i] = (numpy.fft.fft(self.measurement.raw[:,i]))/(nr_points/2)
            
        ''' calcs Jn (skew multipole), Kn (normal multipole) and An (skew angle) from FFT of integrated voltage '''
        dtheta = 2*numpy.pi/nr_points
        self.absolute_LN = numpy.zeros((len(self.harmonics),nr_turns))
        self.absolute_LS = numpy.zeros((len(self.harmonics),nr_turns))
        self.skew_angle = numpy.zeros((len(self.harmonics),nr_turns))
        for j in range(len(self.harmonics)):
            n = self.harmonics[j]
            R = Ne * (r2 ** n - r1 ** n)
            s = numpy.sin(n*dtheta)
            c = numpy.cos(n*dtheta)
            for i in range(nr_turns):    
                An =  F[i][n].real
                Bn = -F[i][n].imag
                Jn = (An * s + Bn*(c-1.0))/(2*R*(c-1.0))
                Kn = (Bn * s - An*(c-1.0))/(2*R*(c-1.0))
                self.absolute_LS[j,i] = Jn*n
                self.absolute_LN[j,i] = Kn*n
                self.skew_angle[j,i] = math.atan(self.absolute_LS[j,i] / self.absolute_LN[j,i]) / n
        
        ''' Calculates average and std of the Normal and Skew multipoles '''  
        self.absolute_LN_avg  = numpy.mean(self.absolute_LN,axis=1)   
        self.absolute_LS_avg  = numpy.mean(self.absolute_LS,axis=1)
        self.skew_angle_avg   = numpy.mean(self.skew_angle,axis=1)
        self.absolute_LN_std  = numpy.std(self.absolute_LN,axis=1, ddof=1) / numpy.sqrt(nr_turns - 1)
        self.absolute_LS_std  = numpy.std(self.absolute_LS,axis=1, ddof=1) / numpy.sqrt(nr_turns - 1)
        self.skew_angle_std   = numpy.std(self.skew_angle,axis=1,  ddof=1) / numpy.sqrt(nr_turns - 1)
        
        
class measurement:
    
    def __init__(self, fname):
        
        self.fname = fname
        self.config = {}
        self.read_file()
        self.nr_points = len(self.raw)
        self.nr_turns  = len(self.raw[0])
        self.rcoil_Ne = self.config['n_espiras_bobina_principal']     # Numero de Espiras
        self.rcoil_r1 = self.config['raio_interno_bobina_princip(m)'] # Raio interno [m]
        self.rcoil_r2 = self.config['raio_externo_bobina_princip(m)'] # Raio externo [m]
        
        
    def __str__(self):
        r = ''
        r += '{0:30s}: '.format('fname') +  self.fname + '\n'
        r += '{0:30s}: '.format('timestamp') +  self.config['data'] + '_' + self.config['hora'] + '\n'
        r += '{0:30s}: '.format('current[A]') + str(self.config['corrente_alim_principal_avg(A)']) + '\n'
        r += '{0:30s}: '.format('nr_turns') +  str(self.nr_turns) + '\n'
        r += '{0:30s}: '.format('nr_points') + str(self.nr_points) + '\n'
        r += '{0:30s}: '.format('rcoil_Ne') + str(int(self.rcoil_Ne)) + '\n'    
        r += '{0:30s}: '.format('rcoil_r1[m]') + str(self.rcoil_r1) + '\n'
        r += '{0:30s}: '.format('rcoil_r2[m]') + str(self.rcoil_r2) + '\n'
        return r
        
    def read_file(self):
        
        ''' reads raw data into list '''
        fp = open(self.fname)
        lines = fp.readlines()
        fp.close()
        
        section = None
        ''' parses header file '''
        for i in range(len(lines)):
            line = lines[i].strip()
            if not len(line):
                continue
            if '### DADOS DE CONFIG' in line.upper(): 
                section = 'CONFIG'
                continue
            if '### DADOS DE LEITURA' in line.upper():
                section = 'MULTIPOLES'
                continue
            if '### DADOS DA BOBINA' in line.upper():
                section = 'BOBINA'
                continue
            #if '### DADOS ARMAZENADOS' in line.upper():
            if '### DADOS BRUTOS' in line.upper():
                section = 'RAW'
                raw = []
                continue
            if line[0] == '#':
                continue
            if section == 'CONFIG':
                words = line.split()
                self.config[words[0]] = ' '.join(words[1:])
                try:
                    self.config[words[0]] = float(self.config[words[0]])
                except:
                    pass
                continue
            if section == 'BOBINA':
                words = line.split()
                self.config[words[0]] = ' '.join(words[1:])
                try:
                    self.config[words[0]] = float(self.config[words[0]])
                except:
                    pass
                continue
            if section == 'MULTIPOLES':
                words = line.split()
                if words[0].upper() == 'N':
                    continue
                continue
            if section == 'RAW':
                words = line.split()
                for k in range(len(words)):
                    words[k] = float(words[k])
                raw.append(words)
        self.raw = 1e-12 * numpy.array(raw)  # unidade em V.s
        

def calc_alpha_blending(fg, alpha, bg=(1,1,1)):
    return (alpha*fg[0]+(1-alpha)*bg[0],alpha*fg[1]+(1-alpha)*bg[1],alpha*fg[2]+(1-alpha)*bg[2])
        
def plot_normal_multipoles(data,  
                           plot_label = '', 
                           harmonics = None, 
                           directory = None,
                           filename = None, 
                           ymin = 1e-6,
                           colors = None,
                           alpha_blending = 0.6,
                           legend = None,
                           display_plot = True
                           ):  
    
    if colors == None:
        colors = colors_redline
    if harmonics is None:
        harmonics = data[0].harmonics
    
    r0 = data[0].r0
    nr_bars = len(data)
    
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(1,1,1)
    ax.set_yscale('log')
    dx = 1.0
    xticks = []
    for j in range(nr_bars):
        x, y, n = [], [], 1
        for i in range(len(harmonics)):
            try:
                idx          = data[j].harmonics.index(harmonics[i])      
                error        = data[j].relative_LN_std[idx]
                multipole_0  = abs(data[j].relative_LN_avg[idx]) 
                multipole_p  = multipole_0 + error
                multipole_n  = multipole_0 - error 
                if multipole_n < ymin:
                    multipole_n = ymin 
                x0 = n * (nr_bars+2) + j
                if j == nr_bars/2:
                    xticks.append(x0)
                    #xticks.append(harmonics[i])
                x.append(x0-0.5*dx), y.append(ymin)
                x.append(x0-0.5*dx), y.append(multipole_0)
                x.append(x0+0.5*dx), y.append(multipole_0)
                x.append(x0+0.5*dx), y.append(ymin)
                if (multipole_n != 0) or (multipole_p != 0):  
                    plt.plot([x0, x0], [multipole_n, multipole_p], color = (0,0,0)) #colors[j])
                    plt.plot([x0-0.25*dx, x0+0.25*dx], [multipole_n, multipole_n], color = (0,0,0)) #colors[j])
                    plt.plot([x0-0.25*dx, x0+0.25*dx], [multipole_p, multipole_p], color = (0,0,0)) #colors[j])
            except ValueError:
                pass
            finally:
                n += 1
        c = calc_alpha_blending(colors[j%len(colors)],alpha_blending)
        plt.fill(x,y, color=calc_alpha_blending(colors[j%len(colors)],alpha_blending))
    ax.grid(True)
    ax.xaxis.set_ticks(xticks)
    ax.xaxis.set_ticklabels(['{0:d}'.format(i) for i in harmonics])
    plt.xlabel('harmonic order')
    plt.ylabel('relative normal multipole strengths (r$_0$ = ' + str(r0*1000) + ' mm)')
    if legend is not None:
        plt.legend(legend)
    plt.title(plot_label + ': normal components')
#     if directory is not None:
#         fname = os.path.join(directory,filename + '_skew.ps')
#     else:
#         fname = filename + '_skew.ps'
#     plt.savefig(fname)
    if display_plot:
        plt.show()
    plt.close()
    
    
def read_folder(folder):
    
    fnames = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    data = []
    for fname in fnames:
        m = measurement(fname)
        data.append(m)
    return data
    
    
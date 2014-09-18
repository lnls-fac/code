import numpy
import math
import matplotlib.pyplot as plt
import os

''' color patterns for multipole plots '''
# colors_redline   = [(1.0,0,0),(0.5,0,0)]
# colors_blueline  = [(0,0,1.0),(0,0,0.5)]
# colors_greenline = [(0,0.5,0),(0,1,0)]

colors_redline   = [(1,0,0),]
colors_greenline = [(0,1,0),]
colors_blueline  = [(0,0,1),]


  
default_ymin = 1e-6
        
class multipoles:
    """ class which represents multipole analysis from a rotating coil measurement """
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
                r += '{0:30s}: '.format('abs_mpole  (n={0:02d}) [{1:s}]'.format(n, self.calc_multipole_units(n))) + '{0:+10.4e} \u00B1 {1:10.4e}'.format(self.absolute_LN_avg[i], self.absolute_LN_std[i]) + ', ' + '{0:+10.4e} \u00B1 {1:10.4e}'.format(self.absolute_LS_avg[i], self.absolute_LS_std[i]) + '\n'
        if self.skew_angle_avg is not None:
            for i in range(len(self.harmonics)):
                n = self.harmonics[i]
                r += '{0:30s}: '.format('skew_angle (n={0:02d}) [rad]'.format(n)) + '{0:+10.4e} \u00B1 {1:10.4e}'.format(self.skew_angle_avg[i], self.skew_angle_std[i]) + '\n'     
        if self.r0 is not None:
            r += '{0:30s}: '.format('r0[m]') +  str(self.r0) + '\n'
        if self.main_multipole is not None:
            n = self.main_multipole[0]
            r += '{0:30s}: '.format('main_multipole [{0:s}]'.format(self.calc_multipole_units(n))) +  str(self.main_multipole[1]) + '\n'
        if self.relative_LN_avg is not None:
            for i in range(len(self.harmonics)):
                n = self.harmonics[i]
                r += '{0:30s}: '.format('rel_mpole  (n={0:02d})'.format(n)) + '{0:+10.4e} \u00B1 {1:10.4e}'.format(self.relative_LN_avg[i], self.relative_LN_std[i]) + ', ' + '{0:+10.4e} \u00B1 {1:10.4e}'.format(self.relative_LS_avg[i], self.relative_LS_std[i]) + '\n'
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
        if self.absolute_LN_avg is None:
            self.calc_absolute_multipoles()
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
        
        main = self.main_multipole[1] * (self.r0 ** (self.main_multipole[0]-1))
        
        if self.absolute_LN is None:
            self.relative_LN_avg = [0] * len(self.harmonics)
            self.relative_LS_avg = [0] * len(self.harmonics)
            self.relative_LN_std = [0] * len(self.harmonics)
            self.relative_LS_std = [0] * len(self.harmonics)
            for j in range(len(self.harmonics)):
                n = self.harmonics[j]
                self.relative_LN_avg[j]  = self.absolute_LN_avg[j] * (self.r0 ** (n-1)) / main
                self.relative_LS_avg[j]  = self.absolute_LS_avg[j] * (self.r0 ** (n-1)) / main
                self.relative_LN_std[j]  = self.absolute_LN_std[j] * (self.r0 ** (n-1)) / main
                self.relative_LS_std[j]  = self.absolute_LS_std[j] * (self.r0 ** (n-1)) / main
        else:
            nr_turns  = self.measurement.nr_turns
            self.relative_LN = numpy.zeros((len(self.harmonics), nr_turns))
            self.relative_LS = numpy.zeros((len(self.harmonics), nr_turns))
            for j in range(len(self.harmonics)):
                n = self.harmonics[j]
                for i in range(nr_turns):
                    self.relative_LN[j,i] = self.absolute_LN[j,i] * (self.r0 ** (n-1)) / main
                    self.relative_LS[j,i] = self.absolute_LS[j,i] * (self.r0 ** (n-1)) / main
        
            ''' Calculates average and std of the Normal and Skew relative multipoles '''  
            self.relative_LN_avg  = numpy.mean(self.relative_LN,axis=1)   
            self.relative_LS_avg  = numpy.mean(self.relative_LS,axis=1)
            self.relative_LN_std  = numpy.std(self.relative_LN,axis=1, ddof=1) / numpy.sqrt(nr_turns)
            self.relative_LS_std  = numpy.std(self.relative_LS,axis=1, ddof=1) / numpy.sqrt(nr_turns)
                
    def calc_absolute_multipoles(self):
    
        if self.harmonics is None:
            return
        
        if self.measurement is None:
            if (self.main_multipole is None) or (self.r0 is None):
                return
            main = self.main_multipole[1] * (self.r0 ** self.main_multipole[0])
            self.absolute_LN_avg = [0] * len(self.harmonics)
            self.absolute_LS_avg = [0] * len(self.harmonics)
            self.absolute_LN_std = [0] * len(self.harmonics)
            self.absolute_LS_std = [0] * len(self.harmonics)
            for j in range(len(self.harmonics)):
                n = self.harmonics[j]
                self.absolute_LN_avg[j] = main * self.relative_LN_avg[j] / (self.r0 ** (n-1))
                self.absolute_LS_avg[j] = main * self.relative_LS_avg[j] / (self.r0 ** (n-1))
                self.absolute_LN_std[j] = main * self.relative_LN_std[j] / (self.r0 ** (n-1))
                self.absolute_LS_std[j] = main * self.relative_LS_std[j] / (self.r0 ** (n-1))
            return  
            
        Ne = self.measurement.rcoil_Ne # Numero de Espiras
        r1 = self.measurement.rcoil_r1 # Raio interno [m]
        r2 = self.measurement.rcoil_r2 # Raio externo [m]
        nr_points = self.measurement.nr_points
        nr_turns  = self.measurement.nr_turns
        
        ''' Fourier transform of integrated voltage '''
        F = [0] * nr_turns
        for i in range(nr_turns):
            F[i] = (numpy.fft.fft(self.measurement.raw[:,i]))/(nr_points/2.0)
            
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
    """ class which represents rotating coil measurement """
    
    def __init__(self, fname):
        
        self.fname = fname
        self.config = {}
        self.read_file()
        #self.read_file_old_format()
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
        
    
    def read_file_old_format(self):
        
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
            if 'Dados de Configura' in line: 
                section = 'CONFIG'
                continue
            if 'Dados de Leitura' in line:
                section = 'MULTIPOLES'
                continue
            #if '### DADOS ARMAZENADOS' in line.upper():
            if 'Dados Armazenados' in line:
                section = 'RAW'
                raw = []
                continue
            if 'Angulo Volta' in line:
                section = 'ANGULO'
            if line[0] == '#':
                continue
            if section is None:
                continue
            if section is 'ANGULO':
                continue
            if section == 'CONFIG':
                words = line.split()
                words[0] = words[0].strip(':\.')
                words[0] = words[0].lower()
                if words[0] == 'corrente':
                    words[0] = 'corrente_alim_principal_avg(A)'
                    del words[3:]
                    del words[1:2]
                if words[0] == 'ganho': words[0] = 'ganho_integrador'
                if words[0] == 'n' and words[1] == 'Pontos': 
                    words[0] = 'nr_pontos_integracao'
                    del words[1:3]
                if words[0] == 'n' and words[2] == 'Coletas..........:': 
                    words[0] = 'nr_voltas'
                    del words[1:3]
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
                if line == 'Brutos':
                    continue
                raw.append(float(line))
        
        #print(self.config)
        self.config['nr_voltas'] = int(self.config['nr_voltas'])
        self.raw = 1e-12 * numpy.array(raw)  # unidade em V.s
        self.raw = numpy.reshape(self.raw, (self.config['nr_voltas'],-1))
        self.raw = numpy.transpose(self.raw)
        
        self.config['n_espiras_bobina_principal']     = 10
        self.config['raio_interno_bobina_princip(m)'] = 0.001
        self.config['raio_externo_bobina_princip(m)'] = 0.01803
        
        
def calc_alpha_blending(fg, alpha, bg=(1,1,1)):
    """ does color linear combination for alpha-blending (ps figures loose alpha-blending props unless it is hard-coded in colors) """
    return (alpha*fg[0]+(1-alpha)*bg[0],alpha*fg[1]+(1-alpha)*bg[1],alpha*fg[2]+(1-alpha)*bg[2])
    
def excitation_print_summary(data, base_bar = False):
    pass

def bar_print_summary(data, base_bar = False):
    
    if base_bar:
        idx = 1
    else:
        idx = 0
        
    nrpts = len(data[idx:])
    main_multipole = data[idx].main_multipole
    harmonics = data[idx].harmonics
    
    print('main multipole         : {0:+11.4e} {1:s}'.format(main_multipole[1], multipoles.calc_multipole_units(main_multipole[0])))
    print('number of measurements : {0:d}'.format(nrpts))
    avg_relative_LN_avg = [0] * len(data[idx].relative_LN_avg)
    std_relative_LN_avg = [0] * len(data[idx].relative_LN_avg)
    max_relative_LN_std = None
    avg_relative_LS_avg = [0] * len(data[idx].relative_LS_avg)
    std_relative_LS_avg = [0] * len(data[idx].relative_LS_avg)
    max_relative_LS_std = None
    print('{0:s}  [{1:s},  {2:s},  {3:s}]'.format('harmonic','avg_relative_LN_avg','std_relative_LN_avg', 'max_relative_LN_std'))
    print('          [{0:s},  {1:s},  {2:s}]'.format('avg_relative_LS_avg','std_relative_LS_avg', 'max_relative_LS_std'))
    for h in range(len(avg_relative_LN_avg)):
        for i in range(idx,nrpts):
            avg_relative_LN_avg[h] += data[i].relative_LN_avg[h]
            std_relative_LN_avg[h] += data[i].relative_LN_avg[h] ** 2
            avg_relative_LS_avg[h] += data[i].relative_LS_avg[h]
            std_relative_LS_avg[h] += data[i].relative_LS_avg[h] ** 2
            if (max_relative_LN_std is None) or (data[i].relative_LN_std[h] > max_relative_LN_std) or (data[i].relative_LN_std[h] is None):
                max_relative_LN_std = data[i].relative_LN_std[h]
            if (max_relative_LS_std is None) or (data[i].relative_LS_std[h] > max_relative_LS_std) or (data[i].relative_LS_std[h] is None):
                max_relative_LS_std = data[i].relative_LS_std[h]
        avg_relative_LN_avg[h] /= nrpts
        std_relative_LN_avg[h] = math.sqrt(std_relative_LN_avg[h]/nrpts - avg_relative_LN_avg[h] ** 2)
        avg_relative_LS_avg[h] /= nrpts
        std_relative_LS_avg[h] = math.sqrt(std_relative_LS_avg[h]/nrpts - avg_relative_LS_avg[h] ** 2)
        print('{0:<8d}: [{1:<+11.4e} {2:<10.4e} {3:<10.4e}]   [{4:<+11.4e} {5:<10.4e} {6:<10.4e}]'.format(harmonics[h], avg_relative_LN_avg[h], std_relative_LN_avg[h], max_relative_LN_std, avg_relative_LS_avg[h], std_relative_LS_avg[h], max_relative_LS_std))
    

def current_plot_multipoles(data,  
                            harmonic_order,
                            plot_label = '', 
                            legend = None,
                            plot_type = 'normal_multipoles',
                            plot_excitation_flag = True,
                            plot_nonlinearity_flag = True,
                            current_range = None,
                            ):  
    try:
        r0 = data[0].r0
    except:
        r0 = 0
        
    idx_attr_avg, idx_attr_std, idx_ylabel, idx_title = 0, 1, 2, 3
    options = {'skew_multipoles'            : ('relative_LS_avg', 'relative_LS_std', 'relative skew multipole strength (r$_0$ = ' + str(r0*1000) + ' mm)', plot_label),
               'normal_multipoles'          : ('relative_LN_avg', 'relative_LN_std', 'relative normal multipole strength (r$_0$ = ' + str(r0*1000) + ' mm)', plot_label),
               'skew_angle'                 : ('skew_angle_avg',  'skew_angle_std',  'skew angle [mrad]', 'teste'),
               'absolute_skew_multipoles'   : ('absolute_LS_avg', 'absolute_LS_std', 'absolute skew multipole strength [' + data[0].calc_multipole_units(harmonic_order) + ']', plot_label), 
               'absolute_normal_multipoles' : ('absolute_LN_avg', 'absolute_LN_std', 'absolute normal multipole strength [' + data[0].calc_multipole_units(harmonic_order) + ']', plot_label),
               }
    
    ''' builds lists with current and multipoles values (and error bars) '''
    currents, multipoles_avg, multipoles_std = [], [], []
    for d in data:
        curr  = d.measurement.config['corrente_alim_principal_avg(A)']
        tmp = getattr(d, options[plot_type][idx_attr_avg])
        m_avg = tmp[harmonic_order]
        tmp = getattr(d, options[plot_type][idx_attr_std])
        m_std = tmp[harmonic_order]
        #m_avg = tmp[harmonic_order]
        #m_std = getattr(d, options[plot_type][idx_attr_std])
        if (current_range is None) or (current_range[0] <= curr <= current_range[1]):
            currents.append(curr)
            multipoles_avg.append(m_avg)
            multipoles_std.append(m_std)
         
    ''' plots excitation curve '''
    if plot_excitation_flag:
        plt.errorbar(currents, multipoles_avg, yerr = multipoles_std, marker='o')         
        plt.xlabel('current [A]'), plt.ylabel(options[plot_type][idx_ylabel])
        plt.title(options[plot_type][idx_title])
        plt.show()
        plt.close()
    
    ''' plots excitation non-linearity '''
    if plot_nonlinearity_flag:
        p = numpy.poly1d(numpy.polyfit(currents, multipoles_avg, deg = 1))
        fitted_error = [0] * len(currents)
        fitted_error_std = [0] * len(currents)
        for i in range(len(currents)):
            fitted_error[i]     = 100 * (p(currents[i]) - multipoles_avg[i]) / multipoles_avg[i]
            fitted_error_std[i] = 100 * multipoles_std[i] / multipoles_avg[i]
        plt.errorbar(currents, fitted_error, yerr = fitted_error_std, marker='o')         
        plt.xlabel('current [A]'), plt.ylabel('non-linearity [%]')
        plt.title(options[plot_type][idx_title])
        plt.show()
        plt.close()    
    
        
def bar_plot_multipoles(data,  
                        plot_label = '', 
                        harmonics = None, 
                        ymin = default_ymin,
                        legend = None,
                        plot_type = 'normal_multipoles',
                        base_bar = 0,
                        ):  
    """ generic drive routine that plots multipole (and skew angle) comparisons """
    if harmonics is None:
        harmonics = data[0].harmonics
    
    r0 = data[0].r0
    nr_bars = len(data)
    ylabels = {'skew_multipoles'   : 'relative skew multipole strengths (r$_0$ = ' + str(r0*1000) + ' mm)',
               'normal_multipoles' : 'relative normal multipole strengths (r$_0$ = ' + str(r0*1000) + ' mm)',
               'skew_angle'        : 'skew angle [mrad]',
               }
    titles  = {'skew_multipoles'   : plot_label + ': skew multipoles',
               'normal_multipoles' : plot_label + ': normal multipoles',
               'skew_angle'        : plot_label + ': skew angle',
               }
    
    black = (0,0,0)
    
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(1,1,1)
    ax.set_yscale('log')
    dx = 1.0
    xticks = []
    for j in range(nr_bars):
        x, y, n = [], [], 1
        for i in range(len(harmonics)):
            x, y = [], []
            try:
                ''' selects data to plot and errorbars '''
                idx          = data[j].harmonics.index(harmonics[i]) 
                if plot_type == 'skew_multipoles':
                    error        = data[j].relative_LS_std[idx]
                    multipole_0  = data[j].relative_LS_avg[idx]
                elif plot_type == 'normal_multipoles':
                    error        = data[j].relative_LN_std[idx]
                    multipole_0  = data[j].relative_LN_avg[idx]
                elif plot_type == 'skew_angle':
                    try:
                        error        = 1000 * data[j].skew_angle_std[idx]
                        multipole_0  = 1000 * data[j].skew_angle_avg[idx]
                    except:
                        error        = 0
                        multipole_0  = 0
                else:
                    raise Exception('Invalid plot type')  
    
                ''' checks bars sign acts accordingly (color settings) '''
                if multipole_0 < 0:
                    ''' negative multipoles get painted represented with red bars '''
                    c = colors_redline[j%len(colors_redline)]    
                    ''' bars are plotted with absolute values '''
                    multipole_0 = abs(multipole_0) 
                else:
                    ''' positive multipoles get painted represented with blue bars '''
                    c = colors_blueline[j%len(colors_blueline)]
                    
                if (j < base_bar):
                    factor  = 0.5
                    #c = colors_greenline[0]
                else:
                    factor = 1.0 
                    

                multipole_p  = multipole_0 + error
                multipole_n  = multipole_0 - error
                
                if multipole_0 < ymin:
                    multipole_0 = ymin    
                if multipole_n < ymin:
                    multipole_n = ymin
                if multipole_p < ymin:
                    multipole_p = ymin 
                x0 = n * (nr_bars+2) + j
                if j == nr_bars//2:
                    xticks.append(x0)
                x.append(x0-0.5*dx), y.append(ymin)
                x.append(x0-0.5*dx), y.append(multipole_0)
                x.append(x0+0.5*dx), y.append(multipole_0)
                x.append(x0+0.5*dx), y.append(ymin)
                if (multipole_n != 0) or (multipole_p != 0):
                    ''' error bars '''  
                    plt.plot([x0, x0], [multipole_n, multipole_p], color = black)
                    plt.plot([x0-0.25*dx, x0+0.25*dx], [multipole_n, multipole_n], color = black)
                    plt.plot([x0-0.25*dx, x0+0.25*dx], [multipole_p, multipole_p], color = black)
                    ''' plots bars '''
                    c = (factor*c[0],factor*c[1],factor*c[2])
                    plt.fill(x,y, color = c)
                    plt.plot(x,y, color = black)
            except ValueError:
                pass
            finally:
                n += 1
        ''' plots bars '''
        #plt.fill(x,y, color = c)
        #plt.plot(x,y, color = black)
    ax.grid(True)
    ax.xaxis.set_ticks(xticks)
    ax.xaxis.set_ticklabels(['{0:d}'.format(i) for i in harmonics])
    plt.xlabel('harmonic order'), plt.ylabel(ylabels[plot_type])
    if legend is not None:
        plt.legend(legend)
    plt.title(titles[plot_type])
    plt.show()
    plt.close()
    
def bar_plot_normal_multipoles(data,  
                               plot_label = '', 
                               harmonics = None,  
                               ymin = default_ymin,
                               legend = None,
                               base_bar = False
                               ):  
    """ comparison plot of normal multipoles from a list with multipole objects """
    bar_plot_multipoles(data,  
                        plot_label = plot_label, 
                        harmonics = harmonics,  
                        ymin = ymin,
                        legend = legend,
                        plot_type = 'normal_multipoles',
                        base_bar = base_bar
                        )  
    
def bar_plot_skew_multipoles(data,  
                             plot_label = '', 
                             harmonics = None,  
                             ymin = default_ymin,
                             legend = None,
                             base_bar = False
                             ):  
    """ comparison plot of skew multipoles from a list with multipole objects """
    bar_plot_multipoles(data,  
                        plot_label = plot_label, 
                        harmonics = harmonics, 
                        ymin = ymin,
                        legend = legend,
                        plot_type = 'skew_multipoles',
                        base_bar = base_bar,
                        )   
     
def bar_plot_skew_angle(data,  
                        plot_label = '', 
                        harmonics = None, 
                        ymin = default_ymin,
                        legend = None,
                        base_bar = False
                        ):
    """ comparison plot of skew angle from a list with multipole objects """ 
    bar_plot_multipoles(data,  
                        plot_label = plot_label, 
                        harmonics = harmonics, 
                        ymin = ymin,
                        legend = legend,
                        plot_type = 'skew_angle',
                        base_bar = base_bar,
                        )   

def bar_plot_multipoles_repetibility(multipoles,
                                     harmonics,
                                     r0,                                  
                                     plot_label = 'PLOT_LABEL',
                                     ymin = default_ymin,
                                     colors = None,
                                     legend = None,
                                     plot_normal_multipoles_flag = True, 
                                     plot_skew_multipoles_flag = True,
                                     plot_skew_angle_flag = True,
                                     base_bar = False):

    if plot_normal_multipoles_flag:
        bar_plot_normal_multipoles(multipoles, plot_label = plot_label, harmonics = harmonics, 
                                   ymin = ymin, legend = legend, base_bar = base_bar)
    if plot_skew_multipoles_flag:
        bar_plot_skew_multipoles(multipoles, plot_label = plot_label, harmonics = harmonics, 
                                 ymin = ymin, legend = legend, base_bar = base_bar)
    if plot_skew_angle_flag:
        bar_plot_skew_angle(multipoles, plot_label = plot_label, harmonics = harmonics, 
                            ymin = ymin, legend = legend, base_bar = base_bar)
                                      
def read_measurements_from_folder(folder):
    """ reads all data files within a folder and stores measurement objects in a list which is then returned """
    fnames = sorted([os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))])
    data = []
    for fname in fnames:
        print(fname)
        m = measurement(fname)
        data.append(m)
    return data

def calc_multipoles_from_measurements(measurements, harmonics, r0, main_multipole = None, main_harmonic = None):
    """ calcs absolute and relative multipoles for a list of measurements """
    
    multip = []
    for d in measurements:
        m = multipoles(measurement = d, harmonics = harmonics)
        m.calc_absolute_multipoles()
        if main_harmonic is not None:
            main_multipole  = m.select_main_multipole(main_harmonic)
        m.calc_relative_multipoles(r0 = r0, main_multipole = main_multipole)
        multip.append(m)
    return multip
    
    
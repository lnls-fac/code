import math
import numpy
import matplotlib.pyplot as plt
import os

''' color patterns for multipole plots '''
colors_happy   = [(0,0,0), (1,0,0),(0,0,1),(0,0.8,0),(1,0,1),(0,1,1),(1,1,0)]
colors_redline = [(0,0,0), (128,0,0),(165,42,42),(220,20,60),(255,99,71),(205,92,92),(233,150,122),(255,160,122)]
colors_redline = [(1.0*c[0]/255.0,1.0*c[1]/255.0,1.0*c[2]/255.0) for c in colors_redline]
        
            
class RotatingCoilMeasurement:
    
    def __init__(self, 
                 fname = None, 
                 label = None, 
                 max_harmonic_order = 15, 
                 harmonics = None, 
                 LNn_avg = None, 
                 LNn_std = None, 
                 LSn_avg = None, 
                 LSn_std = None):
        self.label       = label
        self.fname       = fname
        self.config      = {}
        self.harmonics   = []
        self.max_harmonic_order = max_harmonic_order
        self.LNn_avg = []
        self.LNn_std = []
        self.LSn_avg = []
        self.LSn_std = []
        self.Ang_avg = []
        self.Ang_std = []
        self.raw         = None
        if fname is not None:
            self.read_file()
            self.calc_multipoles()
        else:
            self.harmonics = harmonics
            self.LNn_avg = LNn_avg
            self.LNn_std = LNn_std
            self.LSn_avg = LSn_avg
            self.LSn_std = LSn_std
        
            

    def calc_multipoles(self):
        """ Calculates multipoles from rotating coil integrated signal"""
        
        max_harmonic_order = self.max_harmonic_order
        nTurns  = self.raw.shape[1]
        nPoints = self.raw.shape[0] 
        dados = self.raw*(10**(-12))
        F = [0] * nTurns
        for i in range(nTurns):
            F[i] = (numpy.fft.fft(dados[:,i]))/(nPoints/2)
            
        F = numpy.array(F)
        Ne = 10                        # Numero de Espiras
        r1 = 1.0/1000                  # Raio interno [m]
        r2 = 18.03/1000                # Raio externo [m]
        dtheta = 2*numpy.pi/nPoints
        SJN = numpy.zeros((max_harmonic_order,nTurns))
        SKN = numpy.zeros((max_harmonic_order,nTurns))
        AGN = numpy.zeros((max_harmonic_order,nTurns))
        Nn  = numpy.zeros(max_harmonic_order)
        Sn  = numpy.zeros(max_harmonic_order)
        sNn = numpy.zeros(max_harmonic_order)
        sSn = numpy.zeros(max_harmonic_order)
        #ang = numpy.zeros(21)
        #sang = numpy.zeros(21)
        for i in range(nTurns):
            for n in range(1,max_harmonic_order+1,1):
                R = Ne * (r2 ** n - r1 ** n)
                An =  F[i][n].real
                Bn = -F[i][n].imag
                Jn = (An * numpy.sin(n*dtheta) + Bn*(numpy.cos(n*dtheta)-1))/(2*R*(numpy.cos(n*dtheta)-1))
                Kn = (Bn * numpy.sin(n*dtheta) - An*(numpy.cos(n*dtheta)-1))/(2*R*(numpy.cos(n*dtheta)-1))
                #Calculate the terms K and J from the Fourier Series
                SJN[n-1,i] = Jn*n
                SKN[n-1,i] = Kn*n
                AGN[n-1,i] = math.atan(SJN[n-1,i] / SKN[n-1,i]) / n  
                if i == 0:
                    self.harmonics.append(n)

        #Calulate average and rms of the Normal and Skew multipoles  
        Nn  = numpy.mean(SKN,axis=1)   
        Sn  = numpy.mean(SJN,axis=1)
        An  = numpy.mean(AGN,axis=1)
        sNn = numpy.std(SKN,axis=1,ddof=1)/numpy.sqrt(nTurns)   
        sSn = numpy.std(SJN,axis=1,ddof=1)/numpy.sqrt(nTurns)
        sAn = numpy.std(AGN,axis=1,ddof=1)/numpy.sqrt(nTurns)
        self.LNn_avg = Nn
        self.LSn_avg = Sn
        self.LNn_std = sNn
        self.LSn_std = sSn
        self.Ang_avg = An
        self.Ang_std = sAn
            

    def print_multipoles(self):
        
        print('--- measured multipoles ---')
        for i in range(len(self.harmonics)):
            try:
                ppm_n = int(1e6*abs(self.LNn_std[i]/self.LNn_avg[i]))
            except:
                ppm_n = 0
            try:
                ppm_s = int(1e6*abs(self.LSn_std[i]/self.LSn_avg[i]))
            except:
                ppm_s = 0
            unit = calc_multipole_units(i+1)
            print('{0:02d} [{5:6s}]  n:{1:+22.16E} (+/- {3:8d} ppm), s:{2:+22.16E} (+/- {4:8d} ppm)'.format(self.harmonics[i], self.LNn_avg[i], self.LSn_avg[i], ppm_n, ppm_s, unit))


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
            if '### DADOS ARMAZENADOS' in line.upper():
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
            if section == 'MULTIPOLES':
                words = line.split()
                if words[0].upper() == 'N':
                    continue
#                 self.harms.append(float(words[0]))
#                 self.LNn_avg_original.append(float(words[1]))
#                 self.LSn_avg_original.append(float(words[2]))
#                 self.LBn_avg_original.append(float(words[3]))
#                 self.LNn_std_original.append(float(words[4]))
#                 self.LSn_std_original.append(float(words[5]))
#                 self.LBn_std_original.append(float(words[6]))
                continue
            if section == 'RAW':
                words = line.split()
                for k in range(len(words)):
                    words[k] = float(words[k])
                raw.append(words)
        self.raw = numpy.array(raw)
                
    @staticmethod
    def alpha_blending(fg, alpha, bg=(1,1,1)):
        return (alpha*fg[0]+(1-alpha)*bg[0],alpha*fg[1]+(1-alpha)*bg[1],alpha*fg[2]+(1-alpha)*bg[2])
        
def calc_multipole_units(n = 2):
    if (n == 1):
        units = 'T.m'
    elif (n == 2):
        units = 'T'
    elif (n == 3):
        units = 'T/m'
    else:
        units = 'T/m^' + str(n+1-1)
    return units
   
def plot_skew_angle(data,
                    main_harmonic_order = 2,
                    plot_label = '',
                    directory  = None,
                    filename   = None,
                    display_plot = True,
                    ymin = None,
                    ymax = None):
    
    current_avg    = [0] * len(data)
    current_std    = [0] * len(data)
    angle_avg      = [0] * len(data)
    angle_std      = [0] * len(data)
    for i in range(len(data)):
        mu_m, mu2_m = 0, 0
        mu_c, mu2_c = 0, 0
        nr_points = len(data[i])
        for j in range(nr_points):
            d = data[i][j]
            mu_c  += d.config['corrente_alimentacao_avg(A)']
            mu2_c += d.config['corrente_alimentacao_std(A)']**2
            mu_m  += data[i][j].Ang_avg[main_harmonic_order-1]
            mu2_m += data[i][j].Ang_std[main_harmonic_order-1]**2
        current_avg[i] = mu_c / nr_points
        current_std[i] = math.sqrt(mu2_c) / nr_points
        angle_avg[i] = 1000 * mu_m / nr_points
        angle_std[i] = 1000 * math.sqrt(mu2_m) / nr_points
        
    ''' skew angle '''
    fig = plt.figure()
    plt.plot(current_avg, angle_avg, color='b')
    plt.errorbar(current_avg, angle_avg, yerr = angle_std, xerr = current_std, fmt = 'o', color='b')
    plt.xlabel('current [A]')
    plt.ylabel('Skew angle [mrad]')
    plt.title(plot_label)
    #plt.yscale('log')
    plt.ylim(ymax = ymax, ymin = ymin)
    if filename == None:
        fn = 'skew_angle.ps'
    else:
        fn = filename
    if directory is not None:
        fname = os.path.join(directory,fn + '_skew_angle.ps')
    else:
        fname = fn + '_skew_angle.ps'
    plt.gcf().subplots_adjust(left=0.15)
    plt.grid()
    plt.savefig(fname)
    if display_plot:
        plt.show()
    plt.close()
          
def plot_excitation_curve(data,
                          main_harmonic_order = 2,
                          plot_label = '',
                          directory  = None,
                          filename   = None,
                          points_fit = [2,3,4],
                          display_plot = True
                          ): 
    """ plots excitation curve """
    
    
    current_avg    = [0] * len(data)
    current_std    = [0] * len(data)
    multipoles_avg = [0] * len(data)
    multipoles_std = [0] * len(data)
    for i in range(len(data)):
        mu_m, mu2_m = 0, 0
        mu_c, mu2_c = 0, 0
        nr_points = len(data[i])
        for j in range(nr_points):
            d = data[i][j]
            mu_c  += d.config['corrente_alimentacao_avg(A)']
            mu2_c += d.config['corrente_alimentacao_std(A)']**2
            mu_m  += data[i][j].LNn_avg[main_harmonic_order-1]
            mu2_m += data[i][j].LNn_std[main_harmonic_order-1]**2
        current_avg[i] = mu_c / nr_points
        current_std[i] = math.sqrt(mu2_c) / nr_points
        multipoles_avg[i] = mu_m / nr_points
        multipoles_std[i] = math.sqrt(mu2_m) / nr_points
    
    ''' excitation '''
    fig = plt.figure()
    plt.plot(current_avg, multipoles_avg, color='b')
    plt.errorbar(current_avg, multipoles_avg, yerr = multipoles_std, xerr = current_std, fmt = 'o', color='b')
    plt.xlabel('current [A]')
    plt.ylabel('Integrated multipole [' + calc_multipole_units(n = main_harmonic_order) + ']')
    plt.title(plot_label)
    if filename == None:
        fn = 'excitation.ps'
    else:
        fn = filename
    if directory is not None:
        fname = os.path.join(directory,fn + '_excitation.ps')
    else:
        fname = fn + '_excitation.ps'
    plt.gcf().subplots_adjust(left=0.15)
    plt.grid()
    plt.savefig(fname)
    if display_plot:
        plt.show()
    plt.close()
    
    ''' nonlinearity '''
    I, M = current_avg[:], multipoles_avg[:]
    coeffs = numpy.polyfit(I, M, 1)
    polynomial = numpy.poly1d(coeffs)
    M_fitted = polynomial(current_avg)
    #plt.plot(current_avg, M_fitted)
    #plt.plot(current_avg, multipoles_avg)
    #plt.show()
    #M_nonlinearity = [(multipoles_avg[i] - M_fitted[i]) for i in range(len(current_avg))]
    M_nonlinearity = [(100*(multipoles_avg[i] - M_fitted[i])/M_fitted[i]) for i in range(len(current_avg))]
    M_error = [(100*(multipoles_std[i])/M_fitted[i]) for i in range(len(current_avg))]
    plt.plot(current_avg, M_nonlinearity, color='b')
    plt.errorbar(current_avg, M_nonlinearity, yerr = M_error, fmt = 'o', color='b')
    plt.ylim(ymin = -0.5, ymax = 0.5)
    plt.xlabel('current [A]')
    plt.ylabel('Nonlinearity [%]') #Integrated multipole [' + calc_multipole_units(n = main_multipole_order) + ']')
    plt.title(plot_label)
    if filename == None:
        fn = 'nonlinearity.ps'
    else:
        fn = filename
    if directory is not None:
        fname = os.path.join(directory,fn + '_nonlinearity.ps')
    else:
        fname = fn + '_nonlinearity.ps'
    plt.gcf().subplots_adjust(left=0.15)
    plt.grid()
    plt.savefig(fname)
    if display_plot:
        plt.show()
    plt.close()
            
def plot_multipoles(data, 
                    main_harmonic_order = 2, 
                    r0 = 17.5/1000, 
                    plot_label = '', 
                    harmonics = None, 
                    directory = None,
                    filename = None,
                    max_multipole = None, 
                    ymin = 1e-6,
                    colors = None,
                    alpha_blending = 0.6,
                    legend = None,
                    reference_data_idx = 0,
                    display_plot = True
                    ):
    """ plots mutipole data comparisons """
    
    ''' processes input parameters '''
    if colors == None:
        colors = colors_redline
    if filename == None:
        filename = 'multipoles.ps'
    if max_multipole is None:
        max_multipole = max(data[reference_data_idx].harmonics)
    if harmonics is None:
        harmonics = []
        for i in data[reference_data_idx].harmonics:
            if i <= max_multipole:
                harmonics.append(i)
    
    
    
    ''' defines main multipole '''
    nr_bars = len(data)
    #main_idx = data[reference_data_idx].harmonics.index(main_multipole_order)
    #main_multipole = abs(data[reference_data_idx].LNn_avg[main_idx]*(r0**(data[reference_data_idx].harmonics[main_idx]-1)))
    
    ''' main loop for normal component '''
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(1,1,1)
    ax.set_yscale('log')
    dx = 1 #0.4/nr_bars
    xticks = []
    for j in range(nr_bars):
        main_idx = data[j].harmonics.index(main_harmonic_order)
        main_multipole       = abs(data[j].LNn_avg[main_idx]*(r0**(data[j].harmonics[main_idx]-1)))
        main_multipole_error = abs(data[j].LNn_std[main_idx]*(r0**(data[j].harmonics[main_idx]-1)))
        x, y, n = [], [], 1
        for i in range(len(harmonics)):
            
            idx = data[j].harmonics.index(harmonics[i])
            #multipole_0     = abs(data[j].LNn_avg[idx])*(r0**(data[j].harmonics[idx]-1)) / main_multipole
            #multipole_p     = (abs(data[j].LNn_avg[idx])+data[j].LNn_std[idx])*(r0**(data[j].harmonics[idx]-1)) / main_multipole
            #multipole_n     = (abs(data[j].LNn_avg[idx])-data[j].LNn_std[idx])*(r0**(data[j].harmonics[idx]-1)) / main_multipole
            
            alpha           = r0**(data[j].harmonics[idx]-1) / (r0**(data[j].harmonics[main_idx]-1))
            error           = alpha * math.sqrt((data[j].LNn_std[idx]/data[j].LNn_avg[main_idx])**2 + (data[j].LNn_avg[idx]*data[j].LNn_std[main_idx]/data[j].LNn_avg[main_idx])**2)
            multipole_0     = alpha * abs(data[j].LNn_avg[idx] / data[j].LNn_avg[main_idx]) 
            multipole_p     = multipole_0 + error
            multipole_n     = multipole_0 - error 
            
            
            if multipole_n < 0:
                multipole_n = ymin
            x0 = n * (nr_bars+2) + j
            if j == nr_bars/2:
                xticks.append(x0)
            x.append(x0-0.5*dx), y.append(ymin)
            x.append(x0-0.5*dx), y.append(multipole_0)
            x.append(x0+0.5*dx), y.append(multipole_0)
            x.append(x0+0.5*dx), y.append(ymin)
            if (multipole_n != 0) or (multipole_p != 0):  
                plt.plot([x0, x0], [multipole_n, multipole_p], color = (0,0,0)) #colors[j])
                plt.plot([x0-0.25*dx, x0+0.25*dx], [multipole_n, multipole_n], color = (0,0,0)) #colors[j])
                plt.plot([x0-0.25*dx, x0+0.25*dx], [multipole_p, multipole_p], color = (0,0,0)) #colors[j])
            n += 1
        plt.fill(x,y, color=RotatingCoilMeasurement.alpha_blending(colors[j%len(colors)],alpha_blending))
        
    ''' creates plots '''
    ax.grid(True)
    ax.xaxis.set_ticks(xticks)
    ax.xaxis.set_ticklabels(['{0:d}'.format(i) for i in harmonics])
    plt.ylim(ymin = ymin)
    plt.xlabel('harmonic order')
    plt.ylabel('relative normal multipole strengths (r$_0$ = ' + str(r0*1000) + ' mm)')
    if legend is not None:
        plt.legend(legend)
    plt.title(plot_label + ': normal components')
    if directory is not None:
        fname = os.path.join(directory,filename + '_normal.ps')
    else:
        fname = filename + '_normal.ps'
    plt.savefig(fname)
    if display_plot:
        plt.show()
    plt.close()
    
    
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(1,1,1)
    ax.set_yscale('log')
    dx = 1 #0.4/nr_bars
    xticks = []
    
    for j in range(nr_bars):
        x, y, n = [], [], 1
        for i in range(len(harmonics)):
            idx = data[j].harmonics.index(harmonics[i])
            multipole_0     = abs(data[j].LSn_avg[idx])*(r0**(data[j].harmonics[idx]-1)) / main_multipole
            multipole_p     = (abs(data[j].LSn_avg[idx])+data[j].LSn_std[idx])*(r0**(data[j].harmonics[idx]-1)) / main_multipole
            multipole_n     = (abs(data[j].LSn_avg[idx])-data[j].LSn_std[idx])*(r0**(data[j].harmonics[idx]-1)) / main_multipole
            if multipole_n < 0:
                multipole_n = ymin
            x0 = n * (nr_bars+2) + j
            if j == nr_bars/2:
                xticks.append(x0)
            x.append(x0-0.5*dx), y.append(ymin)
            x.append(x0-0.5*dx), y.append(multipole_0)
            x.append(x0+0.5*dx), y.append(multipole_0)
            x.append(x0+0.5*dx), y.append(ymin)
            if (multipole_n != 0) or (multipole_p != 0):
                plt.plot([x0, x0], [multipole_n, multipole_p], color = (0,0,0)) #colors[j])
                plt.plot([x0-0.25*dx, x0+0.25*dx], [multipole_n, multipole_n], color = (0,0,0)) #colors[j])
                plt.plot([x0-0.25*dx, x0+0.25*dx], [multipole_p, multipole_p], color = (0,0,0)) #colors[j])
            n += 1
        plt.fill(x,y, color=RotatingCoilMeasurement.alpha_blending(colors[j%len(colors)],alpha_blending))
        
    ax.grid(True)
    ax.xaxis.set_ticks(xticks)
    ax.xaxis.set_ticklabels(['{0:d}'.format(i) for i in harmonics])
    plt.xlabel('harmonic order')
    plt.ylabel('relative skew multipole strengths (r$_0$ = ' + str(r0*1000) + ' mm)')
    if legend is not None:
        plt.legend(legend)
    plt.title(plot_label + ': skew components')
    if directory is not None:
        fname = os.path.join(directory,filename + '_skew.ps')
    else:
        fname = filename + '_skew.ps'
    plt.savefig(fname)
    if display_plot:
        plt.show()
    plt.close()

def calc_normalized_multipoles(harmonics, LNn_avg, LNn_std, LSn_avg, LSn_std, main_harmonic_order = 2, r0 = 17.5/1000):
        
        main_idx = harmonics.index(main_harmonic_order)
        main_multipole = LNn_avg[main_idx]*(r0**(harmonics[main_idx]-1))
        LNn_norm_avg, LNn_norm_std = [], []
        LSn_norm_avg, LSn_norm_std = [], []
        for i in range(len(harmonics)):
            n = harmonics[i]
            LNn_norm_avg.append(LNn_avg[i]*(r0**(n-1)) / main_multipole)
            LNn_norm_std.append(LNn_std[i]*(r0**(n-1)) / main_multipole)
            LSn_norm_avg.append(LSn_avg[i]*(r0**(n-1)) / main_multipole)
            LSn_norm_std.append(LSn_std[i]*(r0**(n-1)) / main_multipole)
        return (LNn_norm_avg, LNn_norm_std, LSn_norm_avg, LSn_norm_std)
      
def calc_absolute_multipoles(harmonics, LNn_norm_avg, LNn_norm_std, LSn_norm_avg, LSn_norm_std, main_harmonic_order = 2, r0 = 17.5/1000):
    
    main_idx  = harmonics.index(main_harmonic_order)
    LNn_avg, LNn_std = [], []
    LSn_avg, LSn_std = [], []
    for i in range(len(harmonics)):
        n = harmonics[i]
        LNn_avg.append(LNn_norm_avg[i] * main_multipole * (r0 ** (n-1)) / (r0 ** (n-1))) 
        LNn_std.append(LNn_norm_std[i] * main_multipole * (r0 ** (n-1)) / (r0 ** (n-1)))
        LSn_avg.append(LSn_norm_avg[i] * main_multipole * (r0 ** (n-1)) / (r0 ** (n-1))) 
        LSn_std.append(LSn_norm_std[i] * main_multipole * (r0 ** (n-1)) / (r0 ** (n-1)))
    return (LNn_avg, LNn_std, LSn_avg, LSn_std)

def load_data_set(directory, magnet_names):
    
    data = []
    for magnet_name in magnet_names:
        idx = 1
        magnet_data = []
        while True:
            fname = os.path.join(directory, magnet_name, magnet_name + '_Medida_' + str(idx) + '_FAC.dat')
            try:
                m = RotatingCoilMeasurement(fname, label = magnet_name)
                magnet_data.append(m)
                idx += 1
            except IOError:
                break
        data.append(magnet_data)
    return data
            
def print_data_set_information(data, main_harmonic_order = 2):
    
    print('{0:<12s}  '.format('')),
    idx = 0
    for sm in data[0]:
        print('{0:<10d}'.format(idx)),
        idx += 1
    print('')
    print('--- current [A] ---')
    for m in data:
        print('{0:<12s}: '.format(m[0].label)),
        for sm in m:
            print('{0:+10.3E}'.format(sm.config['corrente_alimentacao_avg(A)'])),
        print('')
        
    main_idx = data[0][0].harmonics.index(main_harmonic_order)
    
    units = calc_multipole_units(main_harmonic_order) 
    label = '--- main normal multipole: n = ' + str(data[0][0].harmonics[main_idx]) + ', units = [' + units + '] --- '
    print(label)
    for m in data:
        print('{0:<12s}: '.format(m[0].label)),
        for sm in m:
            print('{0:+10.3E}'.format(sm.LNn_avg[main_idx])),
        print('')
    


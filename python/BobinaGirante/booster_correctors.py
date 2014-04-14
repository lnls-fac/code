import datetime
import math
import analysis
import matplotlib.pyplot as plt

def analysis_at_single_current(data, current_idx, harmonics = [1,2,3], r0 = 17.5/1000, display_plot = False):
    
    n = len(data)
    
    ''' selects only at specific current'''
    selection = []
    for m in data:
        selection.append(m[current_idx])
            
    ''' does stats on current and calcs normalized multipoles ''' 
    current_avg, current_std = 0, 0
    LNn_norm_avg_tmp, LNn_norm_std_tmp = [], []
    LSn_norm_avg_tmp, LSn_norm_std_tmp = [], []
    for i in range(len(selection)):
        current_avg += selection[i].config['corrente_alimentacao_avg(A)']
        current_std += selection[i].config['corrente_alimentacao_std(A)']**2
        d = selection[i]
        p = analysis.calc_normalized_multipoles(d.harmonics, d.LNn_avg, d.LNn_std, d.LSn_avg, d.LSn_std, r0 = r0, main_harmonic_order = 1)
        LNn_norm_avg_tmp.append(p[0])
        LNn_norm_std_tmp.append(p[1])
        LSn_norm_avg_tmp.append(p[2])
        LSn_norm_std_tmp.append(p[3])
    current_avg /= n
    current_std = math.sqrt(current_std) / n
        
    ''' calcs multipole statistics over prototypes set '''
    LNn_avg = [0] * len(selection[0].LNn_avg)
    LNn_std = [0] * len(selection[0].LNn_std)
    LSn_avg = [0] * len(selection[0].LSn_avg)
    LSn_std = [0] * len(selection[0].LSn_std)
    LNn_norm_avg = [0] * len(LNn_norm_avg_tmp[0])
    LNn_norm_std = [0] * len(LNn_norm_std_tmp[0])
    LSn_norm_avg = [0] * len(LSn_norm_avg_tmp[0])
    LSn_norm_std = [0] * len(LSn_norm_std_tmp[0])
    for j in range(len(LNn_avg)):
        smu1, smu2, ssigma2 = 0.0, 0.0, 0.0
        smu1_norm, smu2_norm, ssigma2_norm = 0.0, 0.0, 0.0 
        for i in range(n):
            ssigma2      += selection[i].LNn_std[j]**2
            smu1         += selection[i].LNn_avg[j]
            smu2         += selection[i].LNn_avg[j]**2
            ssigma2_norm += LNn_norm_std_tmp[i][j]**2
            smu1_norm    += LNn_norm_avg_tmp[i][j]
            smu2_norm    += LNn_norm_avg_tmp[i][j]**2
        LNn_avg[j] = smu1 / n
        LNn_std[j] = math.sqrt(((n-1.0)/n) * (ssigma2/n) + smu2 / n - (LNn_avg[j])**2)
        LNn_norm_avg[j] = smu1_norm / n
        LNn_norm_std[j] = math.sqrt(((n-1.0)/n) * (ssigma2_norm/n) + smu2_norm / n - (LNn_norm_avg[j])**2)
     
    for j in range(len(LSn_avg)):
        smu1, smu2, ssigma2 = 0.0, 0.0, 0.0
        smu1_norm, smu2_norm, ssigma2_norm = 0.0, 0.0, 0.0 
        for i in range(n):
            ssigma2      += selection[i].LSn_std[j]**2
            smu1         += selection[i].LSn_avg[j]
            smu2         += selection[i].LSn_avg[j]**2
            ssigma2_norm += LSn_norm_std_tmp[i][j]**2
            smu1_norm    += LSn_norm_avg_tmp[i][j]
            smu2_norm    += LSn_norm_avg_tmp[i][j]**2
        LSn_avg[j] = smu1 / n
        LSn_std[j] = math.sqrt(((n-1.0)/n) * (ssigma2/n) + smu2 / n - (LSn_avg[j])**2)
        LSn_norm_avg[j] = smu1_norm / n
        LSn_norm_std[j] = math.sqrt(((n-1.0)/n) * (ssigma2_norm/n) + smu2_norm / n - (LSn_norm_avg[j])**2)    
   
            
    
    ''' prints summary of data analysis '''
        
    print('')
    print('Data set analysis at specific current')
    print('-------------------------------------')
    print('index of selected corrent : {0:<2d}'.format(current_idx))
    print('avg current [mA]          : {0:<+7.1f}'.format(1000*current_avg))
    print('std current [ppm]         : {0:<d}'.format(int(1e6*current_std/current_avg)))
    print('--- normal and skew multipoles ---')
    print('n   avg(LNn)[T/m^(n-2)] std(LNn)[T/m^(n-2)] std/avg[%] avg(LSn)[T/m^(n-2)] std(LSn)[T/m^(n-2)] std/avg[%]')
    for j in range(len(LNn_avg)):
        print('{0:02d}  {1:+11.4E}         {2:+11.4E}         {3:<6.2f}     {4:+11.4E}         {5:+11.4E}         {6:<6.2f}'.format(selection[0].harmonics[j], LNn_avg[j], LNn_std[j], abs(100*LNn_std[j]/LNn_avg[j]), LSn_avg[j], LSn_std[j], abs(100*LSn_std[j]/LSn_avg[j])))
    print('--- normalized normal and skew multipoles (r0 = ' + str(r0*1000) + ' mm) ---')
    print('n   avg(NBn/B0)  std(NBn/B0)  avg(SBn/B0)  std(dSBn/B0)')
    for j in range(len(LNn_avg)):
        print('{0:02d}  {1:+11.4E}  {2:+11.4E}  {3:+11.4E}  {4:+11.4E}'.format(selection[0].harmonics[j], LNn_norm_avg[j], LNn_norm_std[j], LSn_norm_avg[j], LSn_norm_std[j]))    
        
        
    ''' plots multipole comparison for the prototypes set '''
    #plt.xkcd()
    current_label = '{0:03d}'.format(current_idx) + '_I='+str(current_avg)+'A'
    analysis.plot_multipoles(selection, 
                             main_harmonic_order = 1, 
                             harmonics = [1,2,3,4,5], 
                             plot_label = current_label, 
                             alpha_blending = 0.4, 
                             colors = analysis.colors_happy, 
                             ymin = 1e-6,
                             directory = '/home/fac_files/data/sirius_python/bobina_girante/booster_corretoras/2014-04-01_8prototypes/',
                             filename  = current_label,
                             display_plot = display_plot
                             )
    
def analysis_at_single_corrector(data, reference_data_idx = 0, directory = None, display_plot = True):
    
    data1, data2 = data, []
    for i in range(len(data)):
        data2.append([data[i]])
    corrector = data1[0].label
    

    legend = None
    analysis.plot_multipoles(data1, 
                              main_harmonic_order = 1, 
                              reference_data_idx = reference_data_idx,
                              harmonics = [2,3,4,5], 
                              plot_label = corrector, 
                              alpha_blending = 0.4, 
                              colors = analysis.colors_happy, 
                              ymin = 1e-6, 
                              directory = directory,
                              filename  = corrector,
                              legend = legend,
                              display_plot = display_plot
                              ) 
        
    analysis.plot_excitation_curve(data2[:7],
                          main_harmonic_order = 1,
                          plot_label = corrector,
                          directory = directory,
                          filename = corrector,
                          points_fit = [0,1,2,3],
                          display_plot = display_plot
                          )   
    
    analysis.plot_skew_angle(data2,
                             main_harmonic_order = 1,
                             plot_label = corrector,
                             directory = directory,
                             filename = corrector,
                             display_plot = display_plot,
                             ymin = -10,
                             ymax = +10
                             )
       
    
                                

if __name__ == '__main__':
    
    directory = '/home/fac_files/data/sirius_python/bobina_girante/booster_corretoras/2014-04-01_8prototypes/'
    magnet_names = ['BC-0001','BC-0002','BC-0003','BC-0004','BC-0005','BC-0006','BC-0007','BC-0008']
    data = analysis.load_data_set(directory, magnet_names)
    
    today = datetime.date.today()
    
    print('ANALYSIS OF ROTATING COIL MEASUREMENTS FOR THE BOOSTER CORRECTOR PROTOTYPES')
    print('===========================================================================')
    print('Timestamp: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    analysis.print_data_set_information(data, main_harmonic_order = 1)
    
    ''' analysis for each corrector '''
    for i in range(len(data)):
        analysis_at_single_corrector(data[i], reference_data_idx = 6, directory = directory, display_plot = False)
        
    ''' analysis for each current '''
    for i in range(len(data[0])):
        analysis_at_single_current(data, current_idx = i, harmonics = [1,2,3], display_plot = False)
        
    


        

import numpy as np    
import mathphys
import fieldmaptrack
    
class Multipoles:

    def __init__(self, 
                 trajectory = None, 
                 perpendicular_grid = None, 
                 fitting_monomials = None):
        self.trajectory = trajectory
        self.perpendicular_grid = perpendicular_grid
        self.fitting_monomials  = fitting_monomials
      
    def get_multipole_labels(self, type, i):
        
        n = self.fitting_monomials[i]
        if n == 0:
            title  = type.title() + ' dipolar field'
            ylabel = title + ' [T]'
        elif n == 1:
            title  = type.title() + ' quadrupolar field'
            ylabel = title + ' [T/m]'
        elif n == 2:
            title  = type.title() + ' sextupolar field'
            ylabel = title + ' [T/m$^\mathrm{2}$]'
        elif n == 3:
            title  = type.title() + ' octupolar field'
            ylabel = title + ' [T/m$^\mathrm{3}$]'
        elif n == 4:
            title  = type.title() + ' decapolar field'
            ylabel = title + ' [T/m$^\mathrm{4}$]'
        elif n == 5:
            title  = type.title() + ' duodecapolar field'
            ylabel = title + ' [T/m$^\mathrm{5}$]'
        else:
            title  = type.title() + ' 2*({0}+1)-polar field'.format(n)
            pot = '{0}'.format(n)
            ylabel = title + ' [T/m$^\mathrm{'+pot+'}$]'
            
        fname = type + '_' + 'b{0}rx{0}'.format(n)
        return ylabel, title, fname       
         
    def calc_multipoles(self, is_ref_trajectory_flag = False):
        """ calculates multipoles ([T] and [m] units) around given trajectory
            
            inputs 
            
            - is_ref_trajectory: True or False 
            
            if trajectory is a reference trajectory then, for the dipolar
            term, the algorithm fits only the difference between the fieldmap
            and the field on the ref. trajectory (dipolar error fit)
            
            if not a reference trajectory the algorithm does not fit the dipolar
            term at all. It is set explicitly according to the field on the trajectory"""
            
        
        # checks if x == 0 is in the perpendicular grid. gets its index
        grid = list(self.perpendicular_grid)            
        try:
            grid_zero = grid.index(0)
        except ValueError:
            print('perpendicular grid needs to contain origin point')
            raise ValueError
        
        s = self.trajectory.s
        grid_meter = np.array(grid) * mathphys.units.mm_2_meter
        monomials = list(self.fitting_monomials)
        self.normal_multipoles = np.zeros((len(monomials), len(s)))
        self.skew_multipoles   = np.zeros((len(monomials), len(s)))
        #self._polynom_b_amethod = np.zeros((len(monomials), len(s)))
        #self._polynom_a_amethod = np.zeros((len(monomials), len(s)))
        
        if is_ref_trajectory_flag:
            reference_field = np.zeros((3,len(s)))
            reference_field[0,:] = self.trajectory.bx
            reference_field[1,:] = self.trajectory.by
            reference_field[2,:] = self.trajectory.bz
        else:
            #monomials.remove(0) 
            pass
        
        self.max_fit_error = (0,0)
        for i in range(len(s)):
            #print(str(i) + '/' + str(len(s)))
            sf = fieldmaptrack.SerretFrenetCoordSystem(self.trajectory, i)
            points = sf.get_transverse_line(grid)
            fieldmap_field = self.trajectory.fieldmap.interpolate_set(points)
            if is_ref_trajectory_flag:
                # trajectory is a reference trajectory
                field = fieldmap_field - np.tile(reference_field[:,i].reshape((3,1)), (1, len(grid)))
                self.skew_multipoles[:,i], max_error = mathphys.functions.polyfit(grid_meter, field[0,:], monomials)
                self.max_fit_error = max_error if max_error[0] > self.max_fit_error[0] else self.max_fit_error
                self.normal_multipoles[:,i], max_error = mathphys.functions.polyfit(grid_meter, field[1,:], monomials)
                self.max_fit_error = max_error if max_error[0] > self.max_fit_error[0] else self.max_fit_error
            else:
                # trajectory is not a reference trajectory
                #field = fieldmap_field - np.tile(fieldmap_field[:,grid_zero].reshape((3,1)), (1, len(grid)))
#                 self.polynom_a[1:,i] = mathphys.functions.polyfit(grid_meter, field[0,:], monomials)
#                 self.polynom_b[1:,i] = mathphys.functions.polyfit(grid_meter, field[1,:], monomials)
#                 self.polynom_a[0,i] = fieldmap_field[0,grid_zero]
#                 self.polynom_b[0,i] = fieldmap_field[1,grid_zero]
                field = fieldmap_field
                self.skew_multipoles[:,i], max_error = mathphys.functions.polyfit(grid_meter, field[0,:], monomials, algorithm='*lstsq')
                self.max_fit_error = max_error if max_error[0] > self.max_fit_error[0] else self.max_fit_error
                self.normal_multipoles[:,i], max_error = mathphys.functions.polyfit(grid_meter, field[1,:], monomials, algorithm='*lstsq')
                self.max_fit_error = max_error if max_error[0] > self.max_fit_error[0] else self.max_fit_error              
            
                
    def calc_multipoles_integrals(self):
        monomials = self.fitting_monomials
        self.skew_multipoles_integral = np.zeros(self.skew_multipoles.shape[0])
        self.normal_multipoles_integral = np.zeros(self.normal_multipoles.shape[0])
        x = self.trajectory.s * mathphys.units.mm_2_meter
        for i in range(len(monomials)):
            ya, yb = self.skew_multipoles[i,:], self.normal_multipoles[i,:]
            self.skew_multipoles_integral[i] = np.trapz(y = ya, x = x)
            self.normal_multipoles_integral[i] = np.trapz(y = yb, x = x)               
    
    def calc_multipoles_integrals_relative(self, main_polynom, main_monomial, r0):
        
        self.r0 = r0
        r0 = self.r0 * mathphys.units.mm_2_meter
        main_idx = list(self.fitting_monomials).index(main_monomial)
        main_multipole = main_polynom[main_idx] * r0 ** main_monomial
        self.skew_multipoles_integral_relative = np.zeros(self.skew_multipoles_integral.shape)
        self.normal_multipoles_integral_relative = np.zeros(self.normal_multipoles_integral.shape)
        for i in range(len(self.fitting_monomials)):
            n = self.fitting_monomials[i]
            self.skew_multipoles_integral_relative[i]   = self.skew_multipoles_integral[i]   * (r0 ** n) / main_multipole
            self.normal_multipoles_integral_relative[i] = self.normal_multipoles_integral[i] * (r0 ** n) / main_multipole
                   
#     def cccalc_hardedge_polynomials(self,model_hardedge_length):
#         
#         beam = self.trajectory.beam
#         half_hedge_len = 0.5 * model_hardedge_length * mathphys.units.mm_2_meter
#         signed_brho = - 1.0 * beam.brho
#         self.polynom_a_hardedge = (self.skew_multipoles_integral / signed_brho) / half_hedge_len    
#         self.polynom_b_hardedge = (self.normal_multipoles_integral / signed_brho) / half_hedge_len
        
                           
    def __str__(self):
        
        nrpts = len(self.perpendicular_grid)
        grid_min = min(self.perpendicular_grid)
        grid_max = max(self.perpendicular_grid)
        monomials = self.fitting_monomials
        
        r = ''
        r += '{0:<35s} {1}'.format('perpendicular_grid:', '{0} points in [{1:+f},{2:+f}] mm'.format(nrpts, grid_min, grid_max))
        r += '\n{0:<35s} {1:.3f}/{2:.3f} G/G'.format('max_fitting_error', 1e4*self.max_fit_error[0], 1e4*abs(self.max_fit_error[1]))
        r += '\n{0:<35s} {1} mm'.format('r0_for_relative_multipoles', self.r0) 
        r += '\n{0:<35s} {1:^12s} {2:^12s} {5:^12s} | {3:^12s} {4:^12s} {6:^12s}'.format('                   ', 'MaxAbs_Nn', 'Integ_Nn', 'MaxAbs_Sn', 'Integ_Sn', 'Nn/N0(@r0)', 'Sn/S0(@r0)')
        r += '\n{0:<35s} {1:^12s} {2:^12s} {5:^12s} | {3:^12s} {4:^12s} {6:^12s}'.format('<multipole_order n>', '[T/m^n]', '[T.m/m^n]', '[T/m^n]', '[T.m/m^n]', '[]', '[]')
        for i in range(len(monomials)):
            n = monomials[i]
            max_poly_a = max(np.abs(self.skew_multipoles[i,:]))
            max_poly_b = max(np.abs(self.normal_multipoles[i,:]))
            integ_poly_a = self.skew_multipoles_integral[i]
            integ_poly_b = self.normal_multipoles_integral[i]
            integ_poly_a_relative = self.skew_multipoles_integral_relative[i]
            integ_poly_b_relative = self.normal_multipoles_integral_relative[i]        
            r += '\n{0:35s} {1:^12.3e} {2:^+12.3e} {5:^+12.4e} | {3:^12.3e} {4:^+12.3e} {6:^+12.3e}'.format('n={0:02d}:'.format(n), max_poly_b, integ_poly_b, max_poly_a, integ_poly_a, integ_poly_b_relative, integ_poly_a_relative) 
        return r

    def save(self, filename):
        
        with open(filename, 'w') as fp:
            fp.write('# multipoles\n')
            fp.write('# s[mm] ')
            for j in range(len(self.fitting_monomials)):
                fp.write('polynom_b[n={0}][T/m^n] '.format(self.fitting_monomials[j]))
            fp.write('\n') 
            traj = self.trajectory
            for i in range(len(traj.s)):
                fp.write('{0:+.16e} '.format(traj.s[i]))
                for j in range(len(self.fitting_monomials)):
                    fp.write('{0:+.16e} '.format(self.normal_multipoles[j, i]))
                fp.write('\n')
                
        
        
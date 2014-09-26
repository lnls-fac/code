import math
from fieldmaptrack import fieldmap
import numpy as np
import mathphys
import mathphys.units as units


class SerretFrenetCoordSystem:
    
    def __init__(self, trajectory, point_idx = 0):
        
        t,i = trajectory,point_idx # syntactic-sugars
        self.s = t.s[i]                      # s position
        self.p = np.array((t.rx[i], t.ry[i], t.rz[i])) # (rx,ry,rz) position of point
        self.t = np.array((t.px[i], t.py[i], t.pz[i])) # (px,py,pz) position of point
        self.t /= math.sqrt(np.sum(self.t**2))
        self.n = np.array((t.pz[i], t.py[i],-t.px[i])) # (px,py,pz) position of point
        tx,ty,tz = self.t # syntactic-sugars
        nx,ny,nz = self.n # syntactic-sugars
        self.k = np.array((ty*nz-tz*ny, tz*nx-tx*nz, tx*ny-ty*nx))  ## k = t x n
        
    def get_transverse_line(self, grid):
        
        points = np.zeros((3,len(grid)))
        for i in range(len(grid)):
            points[:,i] = self.p + grid[i] * self.n
        return points    
    
class Trajectory:
    
    def __init__(self,
                 beam,
                 fieldmap):
        self.beam     = beam
        self.fieldmap = fieldmap
        
    def calc_trajectory(self, 
                        init_rx, init_ry, init_rz,
                        init_px, init_py, init_pz,
                        s_length = None, 
                        s_nrpts = None,
                        s_step = None,
                        min_rz = None,
                        force_midplane = False):
        """ Numerical integration (1st-order simple RK lagorithm) of the beam trajectory"""
        
        
        if s_length is None:
            s_length = 0
            s_nrpts = 0
        else:
            s_step = s_length / (s_nrpts - 1.0)
                
        self.s_step = s_step
        self.force_midplane = force_midplane
        self.init_rx, self.init_ry, self.init_rz = init_rx, init_ry, init_rz
        self.init_px, self.init_py, self.init_pz = init_px, init_py, init_pz
        self.s = []
        self.rx, self.ry, self.rz = [], [], []
        self.px, self.py, self.pz = [], [], []
        self.bx, self.by, self.bz = [], [], []
        
        alpha = 1.0/(1000.0*self.beam.brho)/self.beam.beta
    
        s, i = 0.0, 0    
        rx,ry,rz = init_rx, init_ry, init_rz
        px,py,pz = init_px, init_py, init_pz
        
        while True:
           
            # forces midplane, if the case
            if self.force_midplane:
                ry, py = 0.0,0.0
            
            # calcs magnetic field on current position
            try:
                bx,by,bz = self.fieldmap.interpolate(rx,ry,rz)
            except fieldmap.OutOfRangeRy:
                    bx,by,bz = 0.0,0.0,0.0
                    print('extrapolation at ' + str((rx,ry,rz)))
            
            # stores current position
            self.s.append(s)
            self.rx.append(rx), self.ry.append(ry), self.rz.append(rz) 
            self.px.append(px), self.py.append(py), self.pz.append(pz)
            self.bx.append(bx), self.by.append(by), self.bz.append(bz)
            
            # calcs derivatives of the eqs. of motion
            drx_ds = px
            dry_ds = py
            drz_ds = pz
            dpx_ds = - alpha * (py * bz - pz * by)
            dpy_ds = - alpha * (pz * bx - px * bz)
            dpz_ds = - alpha * (px * by - py * bx)
            # propagates to next point
            rx += drx_ds * self.s_step
            ry += dry_ds * self.s_step
            rz += drz_ds * self.s_step
            px += dpx_ds * self.s_step
            py += dpy_ds * self.s_step
            pz += dpz_ds * self.s_step
            s  += self.s_step
            i  += 1 
            
            # tests if end of integration is reached
            if not s_nrpts:
                if rz > min_rz:
                    # is integrating until min_rz is reached
                    break
            else:
                if i == s_nrpts:
                    # is integrating until s_nrpts is reached
                    break
            
        # converts python native lists into numpy arrays
        # (appending in native lists is faster than in nympy arrays)
        self.s = np.array(self.s)
        self.rx, self.ry, self.rz = np.array(self.rx), np.array(self.ry), np.array(self.rz)   
        self.px, self.py, self.pz = np.array(self.px), np.array(self.py), np.array(self.pz)
        self.bx, self.by, self.bz = np.array(self.bx), np.array(self.by), np.array(self.bz)
        
        # calcs deflection angle along trajectory
        self.theta_x = np.arctan(self.px/self.pz)
                         
    def __str__(self):
        
        bx,by,bz = [abs(x) for x in self.bx], [abs(x) for x in self.by], [abs(x) for x in self.bz]
        max_bx, max_by, max_bz = max(bx), max(by), max(bz)
        s_max_bx, s_max_by, s_max_bz = self.s[bx.index(max_bx)], self.s[by.index(max_by)], self.s[bz.index(max_bz)] 
        
        r  = ''
        r += '{0:<35s} {1} deg.'.format('deflection_angle:', abs((180.0/math.pi)*self.theta_x[-1]))
        r += '\n{0:<35s} {1} mm'.format('trajectory_length:', self.s[-1]-self.s[0])
        r += '\n{0:<35s} {1}'.format('trajectory_nrpts:', len(self.s))
        r += '\n{0:<35s} {1} mm'.format('trajectory_s_step:', self.s_step) 
        r += '\n{0:35s} {1:+f} Tesla at rz = {2} mm'.format('max_abs_by@trajectory:', self.by[max_by], s_max_by)
        r += '\n{0:35s} {1:+f} Tesla at rz = {2} mm'.format('max_abs_bx@trajectory:', self.bx[max_bx], s_max_bx)
        r += '\n{0:35s} {1:+f} Tesla at rz = {2} mm'.format('max_abs_bz@trajectory:', self.bz[max_bz], s_max_bz)
    
        return r
       
class Multipoles:

    def __init__(self, 
                 trajectory = None, 
                 perpendicular_grid = None, 
                 fitting_monomials = None):
        self.trajectory = trajectory
        self.perpendicular_grid = perpendicular_grid
        self.fitting_monomials = fitting_monomials
      
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
            
        fname = type + '_' + 'b{0}bx{0}'.format(n)
        return ylabel, title, fname       
         
    def calc_multipoles(self, is_ref_trajectory_flag = False):
        """ calculates multipoles ([T] and [m] units) around given trajectory
            
            inputs 
            
            - is_ref_trajectory: True or False 
            
            if trajectory is a reference trajectory than, for the dipolar
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
        self.polynom_b = np.zeros((len(monomials), len(s)))
        self.polynom_a = np.zeros((len(monomials), len(s)))
        
        if is_ref_trajectory_flag:
            reference_field = np.zeros((3,len(s)))
            reference_field[0,:] = self.trajectory.bx
            reference_field[1,:] = self.trajectory.by
            reference_field[2,:] = self.trajectory.bz
        else:
            monomials.remove(0) 
        
        for i in range(len(s)):
            #print(str(i) + '/' + str(len(s)))
            sf = SerretFrenetCoordSystem(self.trajectory, i)
            points = sf.get_transverse_line(grid)
            fieldmap_field = self.trajectory.fieldmap.interpolate_set(points)
            if is_ref_trajectory_flag:
                # trajectory is a reference trajectory
                
                field = fieldmap_field - np.tile(reference_field[:,i].reshape((3,1)), (1, len(grid)))
                self.polynom_a[:,i] = mathphys.functions.polyfit(grid_meter, field[0,:], monomials)
                self.polynom_b[:,i] = mathphys.functions.polyfit(grid_meter, field[1,:], monomials)
            else:
                # trajectory is not a reference trajectory
                field = fieldmap_field - np.tile(fieldmap_field[:,grid_zero].reshape((3,1)), (1, len(grid)))
                self.polynom_a[1:,i] = mathphys.functions.polyfit(grid_meter, field[0,:], monomials)
                self.polynom_b[1:,i] = mathphys.functions.polyfit(grid_meter, field[1,:], monomials)
                self.polynom_a[0,i] = fieldmap_field[0,grid_zero]
                self.polynom_b[0,i] = fieldmap_field[1,grid_zero]
            
             
    def calc_multipoles_integrals(self):
        monomials = self.fitting_monomials
        self.polynom_a_integral = np.zeros(self.polynom_a.shape[0])
        self.polynom_b_integral = np.zeros(self.polynom_b.shape[0])
        x = self.trajectory.s * units.mm_2_meter
        for i in range(len(monomials)):
            ya, yb = self.polynom_a[i,:], self.polynom_b[i,:]
            self.polynom_a_integral[i] = np.trapz(y = ya, x = x)
            self.polynom_b_integral[i] = np.trapz(y = yb, x = x)               
    
    def __str__(self):
        
        nrpts = len(self.perpendicular_grid)
        grid_min = min(self.perpendicular_grid)
        grid_max = max(self.perpendicular_grid)
        monomials = self.fitting_monomials
        
        r = ''
        r += '{0:<35s} {1}'.format('perpendicular_grid:', '{0} points in [{1:+f},{2:+f}] mm'.format(nrpts, grid_min, grid_max)) 
        r += '\n{0:<35s} {1:^17s} {2:^17s} | {3:^17s} {4:^17s}'.format('<multipole_order n>', 'MaxAbs_Nn_[T/m^n]', 'Integ_Nn[T.m/m^n]', 'MaxAbs_Sn_[T/m^n]', 'Integ_Sn[T.m/m^n]')
        for i in range(len(monomials)):
            n = monomials[i]
            max_poly_a = max(np.abs(self.polynom_a[i,:]))
            max_poly_b = max(np.abs(self.polynom_b[i,:]))
            integ_poly_a = self.polynom_a_integral[i]
            integ_poly_b = self.polynom_b_integral[i]
            r += '\n{0:35s} {1:^17.4e} {2:^+17.4e} | {3:^17.4e} {4:^+17.4e}'.format('n={0:02d}:'.format(n), max_poly_b, integ_poly_b, max_poly_a, integ_poly_a)
        return r

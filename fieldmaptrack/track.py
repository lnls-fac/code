import math
from fieldmaptrack import fieldmap
import numpy as np
import mathphys


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
                        s_length, 
                        s_nrpts,
                        force_midplane = False):
    
        # numerical integration (1st-order simple RK lagorithm) of the beam trajectory
        # (no approximation of the eqs of motion)
        #
        
        self.init_rx, self.init_ry, self.init_rz = init_rx, init_ry, init_rz
        self.init_px, self.init_py, self.init_pz = init_px, init_py, init_pz
        self.s_length = s_length
        self.s_nrpts = s_nrpts
        self.force_midplane = force_midplane
        self.rx, self.ry, self.rz = np.zeros(s_nrpts), np.zeros(s_nrpts), np.zeros(s_nrpts)
        self.px, self.py, self.pz = np.zeros(s_nrpts), np.zeros(s_nrpts), np.zeros(s_nrpts)
        self.bx, self.by, self.bz = np.zeros(s_nrpts), np.zeros(s_nrpts), np.zeros(s_nrpts)
        self.s = np.linspace(0.0, self.s_length, self.s_nrpts)
        
        alpha = 1.0/(1000.0*self.beam.brho)/self.beam.beta
        
        rx,ry,rz = init_rx, init_ry, init_rz
        px,py,pz = init_px, init_py, init_pz
        s_step = s_length / (self.s_nrpts - 1.0)
        
        for i in range(self.s_nrpts):
            
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
            self.rx[i], self.ry[i], self.rz[i] = rx, ry, rz
            self.px[i], self.py[i], self.pz[i] = px, py, pz
            self.bx[i], self.by[i], self.bz[i] = bx, by, bz
            
            # propagates to next point
            drx_ds = px
            dry_ds = py
            drz_ds = pz
            dpx_ds = - alpha * (py * bz - pz * by)
            dpy_ds = - alpha * (pz * bx - px * bz)
            dpz_ds = - alpha * (px * by - py * bx)
            rx += drx_ds * s_step
            ry += dry_ds * s_step
            rz += drz_ds * s_step
            px += dpx_ds * s_step
            py += dpy_ds * s_step
            pz += dpz_ds * s_step
            
        # calcs deflection angle along trajectory
        self.theta_x = np.arctan(self.px/self.pz)
                         
    def __str__(self):
        
        bx,by,bz = [abs(x) for x in self.bx], [abs(x) for x in self.by], [abs(x) for x in self.bz]
        max_bx, max_by, max_bz = max(bx), max(by), max(bz)
        s_max_bx, s_max_by, s_max_bz = self.s[bx.index(max_bx)], self.s[by.index(max_by)], self.s[bz.index(max_bz)] 
        
        r  = ''
        r += '{0:<35s} {1} deg.'.format('deflection_angle:', abs((180.0/math.pi)*self.theta_x[-1]))
        r += '\n{0:<35s} {1} mm'.format('trajectory_length:', self.s_length)
        r += '\n{0:<35s} {1}'.format('trajectory_nrpts:', self.s_nrpts)
        r += '\n{0:<35s} {1} mm'.format('trajectory_s_step:', self.s_length/(self.s_nrpts-1)) 
        r += '\n{0:35s} {1:+f} Tesla at rz = {2} mm'.format('max_abs_bx@trajectory:', self.bx[max_bx], s_max_bx)
        r += '\n{0:35s} {1:+f} Tesla at rz = {2} mm'.format('max_abs_by@trajectory:', self.by[max_by], s_max_by)
        r += '\n{0:35s} {1:+f} Tesla at rz = {2} mm'.format('max_abs_bz@trajectory:', self.bz[max_bz], s_max_bz)
    
        return r
       
class Multipoles:

    def __init__(self, 
                 trajectory = None, 
                 multipoles_perpendicular_grid = None, 
                 multipoles_fitting_monomials = None):
        self.trajectory = trajectory
        self.multipoles_perpendicular_grid = multipoles_perpendicular_grid
        self.multipoles_fitting_monomials = multipoles_fitting_monomials
        
    def calc_multipoles(self):
        ''' calcs multipoles ([T] and [m] units) around given trajectory '''
        s = self.trajectory.s
        grid = self.multipoles_perpendicular_grid
        grid_meter = grid * mathphys.units.mm_2_meter
        monomials = self.multipoles_fitting_monomials
        
        self.polynom_b = np.zeros((len(monomials), len(s)))
        self.polynom_a = np.zeros((len(monomials), len(s)))
        for i in range(len(s)):
            #print(str(i) + '/' + str(len(self.s)))
            sf = SerretFrenetCoordSystem(self.trajectory, i)
            points = sf.get_transverse_line(grid)
            field = self.trajectory.fieldmap.interpolate_set(points)
            self.polynom_a[:,i] = mathphys.functions.polyfit(grid_meter, field[0,:], monomials)
            self.polynom_b[:,i] = mathphys.functions.polyfit(grid_meter, field[1,:], monomials)
             

    def calc_multipoles_integrals():
        monomials = self.multipoles_fitting_monomials
        for i in range(len(monomials)):
            y = self.polynom_a[i,:]
            x = self.trajectory.s
               
    def __str__(self):
        
        nrpts = len(self.multipoles_perpendicular_grid)
        grid_min = min(self.multipoles_perpendicular_grid)
        grid_max = max(self.multipoles_perpendicular_grid)
        monomials = self.multipoles_fitting_monomials
        
        r = ''
        r += '{0:<35s} {1}'.format('perpendicular_grid:', '{0} points in ({1:+f} .. {2:+f})'.format(nrpts, grid_min, grid_max)) 
        r += '\n{0:<35s} {1}'.format('fitting_monomials:', 'x^{0}'.format(monomials))
        for i in range(len(monomials)):
            n = monomials[i]
            poly_a = self.polynom_a_integral[i]
            poly_a = self.polynom_b_integral[i]
            r += '\n{0:35s} {1:+.4e} {2:+.4e}'.format('integrated_multipole(n={0}):'.format(n), poly_a, poly_b)
        return r

import mathphysicslibs.functions as mfuncs
import mathphysicslibs.constants as consts

''' These passmethod indices have to be consistent with corresponding indices from trackc++ passmethods '''
pm_identity_pass              = 0
pm_drift_pass                 = 1
pm_str_mpole_symplectic4_pass = 2
pm_bnd_mpole_symplectic4_pass = 3
pm_corrector_pass             = 4
pm_cavity_pass                = 5
pm_thinquad_pass              = 6
pm_thinsext_pass              = 7
pm_kicktable_pass             = 8

pm_dict = { pm_identity_pass              : ('identity_pass',              PassMethods.identity_pass) ,
            pm_drift_pass                 : ('drift_pass',                 PassMethods.drift_pass),
            pm_str_mpole_symplectic4_pass : ('str_mpole_symplectic4_pass', PassMethods.str_mpole_symplectic4_pass),
            pm_bnd_mpole_symplectic4_pass : ('bnd_mpole_symplectic4_pass', PassMethods.bnd_mpole_symplectic4_pass),
            pm_corrector_pass             : ('corrector_pass',             PassMethods.corrector_pass),
            pm_cavity_pass                : ('cavity_pass',                PassMethods.cavity_pass),
            pm_thinquad_pass              : ('thinquad_pass',              PassMethods.thinquad_pass),
            pm_thinsext_pass              : ('thinsext_pass',              PassMethods.thinsext_pass),
            pm_kicktable_pass             : ('kicktable_pass',             PassMethods.kicktable_pass),
       }
  
  
class PassMethods:

    _DRIFT1 =  6.756035959798286638e-01
    _DRIFT2 = -1.756035959798286639e-01
    _KICK1  =  1.351207191959657328e+00
    _KICK2  = -1.702414383919314656e+00

    # Auxiliary functions
    # -------------------
    
    @staticmethod
    def _drift(pos, length):
        pnorm = 1.0 / (1.0 + pos.de)
        norml = length * pnorm
        pos.rx += norml * pos.px
        pos.ry += norml * pos.py
        pos.dl += 0.5 * norml * pnorm * (pos.px**2 + pos.py**2)    
        
    @staticmethod
    def _fastdrift(pos, norml):
        dx = norml * pos.px
        dy = norml * pos.py
        pos.rx += dx
        pos.ry += dy
        pos.dl += 0.5 * norml * (pos.px**2 + pos.py**2) / (1.0 + pos.de)
    
    @staticmethod
    def _strthinkick(pos, length, polynom_a, polynom_b):    
        (real_sum,imag_sum) = PassMethods._calcpolykick(pos, polynom_a, polynom_b)
        pos.px -= length * real_sum
        pos.py += length * imag_sum
    
    @staticmethod
    def _bndthinkick(pos, length, polynom_a, polynom_b, irho):
        (real_sum,imag_sum) = PassMethods._calcpolykick(pos, polynom_a, polynom_b)
        pos.px -= length * (real_sum - (pos.de - pos.rx * irho) * irho)
        pos.py += length * imag_sum
        pos.dl += length * irho * pos.rx 

    @staticmethod
    def _calcpolykick(pos, polynom_a, polynom_b):
        n = len(polynom_b)
        real_sum = polynom_b[n-1]
        imag_sum = polynom_a[n-1]
        for i in range(n-2, -1, -1):
            real_sum_tmp = real_sum * pos.rx - imag_sum * pos.ry + polynom_b[i]
            imag_sum = imag_sum * pos.rx + real_sum * pos.ry + polynom_a[i]
            real_sum = real_sum_tmp
        return (real_sum,imag_sum)

    @staticmethod    
    def _edge(pos, inv_rho, edge_angle):
        psi = inv_rho * mfuncs.tan(edge_angle)/(1.0 + pos.de);
        pos.px += psi * pos.rx
        pos.py -= psi * pos.ry 
    
    @staticmethod
    def _edge_fringe(pos, inv_rho, edge_angle, fint, gap):
        fx      = inv_rho * mfuncs.tan(edge_angle)/(1.0 + pos.de)
        psi_bar = edge_angle - inv_rho * gap * fint * (1.0 + mfuncs.sin(edge_angle) * mfuncs.sin(edge_angle)) / mfuncs.cos(edge_angle) / (1.0 + pos.de)
        fy      = inv_rho * mfuncs.tan(psi_bar) / (1.0 + pos.de)
        pos.px += pos.rx * fx
        pos.py -= pos.ry * fy


    @staticmethod
    def _translate_pos(pos, t):
        pos.rx += t[0]; pos.px += t[1]
        pos.ry += t[2]; pos.py += t[3]
        pos.de += t[4]; pos.dl += t[5]
        
    @staticmethod
    def _rotate_pos(pos, r):
        (pos.rx, pos.px, pos.ry, pos.py, pos.de, pos.dl) = (
            r[0][0] * pos.rx + r[0][1] * pos.px + r[0][2] * pos.ry + r[0][3] * pos.py + r[0][4] * pos.de + r[0][5] * pos.dl,
            r[1][0] * pos.rx + r[1][1] * pos.px + r[1][2] * pos.ry + r[1][3] * pos.py + r[1][4] * pos.de + r[1][5] * pos.dl,
            r[2][0] * pos.rx + r[2][1] * pos.px + r[2][2] * pos.ry + r[2][3] * pos.py + r[2][4] * pos.de + r[2][5] * pos.dl,
            r[3][0] * pos.rx + r[3][1] * pos.px + r[3][2] * pos.ry + r[3][3] * pos.py + r[3][4] * pos.de + r[3][5] * pos.dl,
            r[4][0] * pos.rx + r[4][1] * pos.px + r[4][2] * pos.ry + r[4][3] * pos.py + r[4][4] * pos.de + r[4][5] * pos.dl,
            r[5][0] * pos.rx + r[5][1] * pos.px + r[5][2] * pos.ry + r[5][3] * pos.py + r[5][4] * pos.de + r[5][5] * pos.dl,
        )

    @staticmethod
    def _global_2_local(pos, element):
        try:
            PassMethods._translate_pos(pos, element.t_in)
        except:
            pass
        try:
            PassMethods._rotate_pos(pos, element.r_in)
        except:
            pass

    @staticmethod
    def _local_2_global(pos, element):
        try:
            PassMethods._rotate_pos(pos, element.r_out)
        except:
            pass
        try:
            PassMethods._translate_pos(pos, element.t_out)
        except:
            pass
        

    # pass_methods
    # ------------
    
    @staticmethod
    def identity_pass(pos, element):
        pass
    
    @staticmethod
    def drift_pass(pos, element):
        PassMethods._drift(pos, element.length)
       
    @staticmethod
    def str_mpole_symplectic4_pass(pos, element):
        sl = element.length / float(element.nr_steps)
        l1 = sl * PassMethods._DRIFT1
        l2 = sl * PassMethods._DRIFT2;
        k1 = sl * PassMethods._KICK1;
        k2 = sl * PassMethods._KICK2;
    
        (polynom_a,polynom_b) = (element.polynom_a, element.polynom_b)
        n = max([len(polynom_a), len(polynom_b)])
        polynom_a.extend((n-len(polynom_a))*[0])
        polynom_b.extend((n-len(polynom_b))*[0])

        PassMethods._global_2_local(pos, element)
    
        for _ in range(element.nr_steps):
            norm   = 1.0/(1.0 + pos.de)
            norml1 = l1 * norm
            norml2 = l2 * norm
            PassMethods._fastdrift(pos, norml1)
            PassMethods._strthinkick(pos, k1, polynom_a, polynom_b) 
            PassMethods._fastdrift(pos, norml2)
            PassMethods._strthinkick(pos, k2, polynom_a, polynom_b)
            PassMethods._fastdrift(pos, norml2)
            PassMethods._strthinkick(pos, k1, polynom_a, polynom_b)
            PassMethods._fastdrift(pos, norml1)

        PassMethods._local_2_global(pos, element)
            
    @staticmethod
    def bnd_mpole_symplectic4_pass(pos, element):            
          
        sl = element.length / float(element.nr_steps)    
        l1 = sl * PassMethods._DRIFT1
        l2 = sl * PassMethods._DRIFT2
        k1 = sl * PassMethods._KICK1
        k2 = sl * PassMethods._KICK2
        
        (polynom_a,polynom_b) = (element.polynom_a, element.polynom_b)
        n = max([len(polynom_a), len(polynom_b)])
        polynom_a.extend((n-len(polynom_a))*[0])
        polynom_b.extend((n-len(polynom_b))*[0])
    
        irho = element.angle / element.length

        PassMethods._global_2_local(pos, element)

        # fringe field - entrance
        try:
            PassMethods._edge_fringe(pos, irho, element.angle_in, element.fint_in, element.gap)
        except: 
            PassMethods._edge(pos, irho, element.angle_in)

        # sector dipole
        for _ in range(element.nr_steps):
            PassMethods._drift(pos, l1)
            PassMethods._bndthinkick(pos, k1, polynom_a, polynom_b, irho)
            PassMethods._drift(pos, l2)
            PassMethods._bndthinkick(pos, k2, polynom_a, polynom_b, irho)
            PassMethods._drift(pos, l2)
            PassMethods._bndthinkick(pos, k1, polynom_a, polynom_b, irho)
            PassMethods._drift(pos, l1)

        # fringe field - exit
        try:
            PassMethods._edge_fringe(pos, irho, element.angle_out, element.fint_out, element.gap)
        except:
            PassMethods._edge(pos, irho, element.angle_out)   

        PassMethods._local_2_global(pos, element)


    @staticmethod
    def corrector_pass(pos, element):

        PassMethods._global_2_local(pos, element)
        
        (xkick,ykick) = element.kick_angle
        if element.length == 0:
            pos.px += xkick
            pos.py += ykick
        else:
            pnorm   = 1.0 / (1.0 + pos.de)
            norml   = element.length * pnorm
            pos.dl += norml * pnorm * 0.5 * ( \
                        xkick * xkick/3.0 + ykick * ykick/3.0 + \
                        pos.px**2 + pos.py**2 + \
                        pos.px * xkick + pos.py * ykick \
                      )
            pos.rx += norml * (pos.px + 0.5 * xkick)
            pos.px += xkick
            pos.ry += norml * (pos.py + 0.5 * ykick)
            pos.py += ykick

        PassMethods._local_2_global(pos, element)
        
    @staticmethod
    def cavity_pass(pos, element):            

        PassMethods._global_2_local(pos, element)

        nv = element.voltage / element.energy
        if element.length == 0:
            pos.de +=  -nv * mfuncs.sin(2*mfuncs.pi*element.frequency*pos.dl/consts.light_speed)
        else:
            # drift half length
            pnorm   = 1.0 / (1.0 + pos.de)
            norml   = (0.5 * element.length) * pnorm
            pos.rx += norml * pos.px
            pos.ry += norml * pos.py
            pos.dl += 0.5 * norml * pnorm * (pos.px**2 + pos.py**2)
            # longitudinal momentum kick 
            pos.de += -nv * mfuncs.sin(2*mfuncs.pi*element.frequency*pos.dl/consts.light_speed)
            # drift half length
            pnorm   = 1.0 / (1.0 + pos.de)
            norml   = (0.5 * element.length) * pnorm                
            pos.rx += norml * pos.px
            pos.ry += norml * pos.py
            pos.dl += 0.5 * norml * pnorm * (pos.px**2 + pos.py**2)

        PassMethods._local_2_global(pos, element)
        
    @staticmethod
    def thinquad_pass(pos, element):
        raise Exception('pass method not implemented!')
    
    @staticmethod
    def thinsext_pass(pos, element):
        raise Exception('pass method not implemented!')
        
    

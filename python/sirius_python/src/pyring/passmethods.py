import mathphysicslibs.functions as mfuncs

class PassMethods:
    
    pm_identity_pass = 0
    pm_drift_pass = 1
    pm_str_mpole_symplectic4_pass = 2
    pm_bnd_mpole_symplectic4_pass = 3
    pm_corrector_pass = 4
    pm_cavity_pass = 5
    pm_thinquad_pass = 6
    pm_thinsext_pass = 7
        
    class _Aux:
        
        DRIFT1 =  6.756035959798286638e-01
        DRIFT2 = -1.756035959798286639e-01
        KICK1  =  1.351207191959657328e+00
        KICK2  = -1.702414383919314656e+00
    
        @staticmethod
        def drift(pos, length):
            pnorm = 1.0 / (1.0 + pos.de)
            norml = length * pnorm
            pos.rx += norml * pos.px
            pos.ry += norml * pos.py
            pos.dl += 0.5 * norml * pnorm * (pos.px**2 + pos.py**2)    
        
        @staticmethod
        def fastdrift(pos, norml):
            dx = norml * pos.px
            dy = norml * pos.py
            pos.rx += dx
            pos.ry += dy
            pos.dl += 0.5 * norml * (pos.px**2 + pos.py**2) / (1.0 + pos.de)
        
        @staticmethod
        def strthinkick(pos, length, polynom_a, polynom_b):    
            (real_sum,imag_sum) = PassMethods._Aux.calcpolykick(pos, polynom_a, polynom_b)
            pos.px -= length * real_sum
            pos.py += length * imag_sum
        
        @staticmethod
        def calcpolykick(pos, polynom_a, polynom_b):
            n = len(polynom_b)
            real_sum = polynom_b[n-1]
            imag_sum = polynom_a[n-1]
            for i in range(n-2, -1, -1):
                real_sum_tmp = real_sum * pos.rx - imag_sum * pos.ry + polynom_b[i]
                imag_sum = imag_sum * pos.rx + real_sum * pos.ry + polynom_a[i]
                real_sum = real_sum_tmp
            return (real_sum,imag_sum)
        
        @staticmethod
        def translate_pos(pos, t):
            pos.rx += t[0]; pos.px += t[1]
            pos.ry += t[2]; pos.py += t[3]
            pos.de += t[4]; pos.dl += t[5]
            
        @staticmethod
        def rotate_pos(pos, r):
            (pos.rx, pos.px, pos.ry, pos.py, pos.de, pos.dl) = (
                r[0][0] * pos.rx + r[0][1] * pos.px + r[0][2] * pos.ry + r[0][3] * pos.py + r[0][4] * pos.de + r[0][5] * pos.dl,
                r[1][0] * pos.rx + r[1][1] * pos.px + r[1][2] * pos.ry + r[1][3] * pos.py + r[1][4] * pos.de + r[1][5] * pos.dl,
                r[2][0] * pos.rx + r[2][1] * pos.px + r[2][2] * pos.ry + r[2][3] * pos.py + r[2][4] * pos.de + r[2][5] * pos.dl,
                r[3][0] * pos.rx + r[3][1] * pos.px + r[3][2] * pos.ry + r[3][3] * pos.py + r[3][4] * pos.de + r[3][5] * pos.dl,
                r[4][0] * pos.rx + r[4][1] * pos.px + r[4][2] * pos.ry + r[4][3] * pos.py + r[4][4] * pos.de + r[4][5] * pos.dl,
                r[5][0] * pos.rx + r[5][1] * pos.px + r[5][2] * pos.ry + r[5][3] * pos.py + r[5][4] * pos.de + r[5][5] * pos.dl,
            )
    
        @staticmethod
        def map_identity_pass(pos, element):
            pass
        
        @staticmethod
        def map_drift_pass(pos, element):
            PassMethods.Aux.drift(pos, element.length)
           
        @staticmethod
        def map_str_mpole_symplectic4_pass(pos, element):
            sl = element.length / float(element.nr_steps)
            l1 = sl * PassMethods._Aux.DRIFT1
            l2 = sl * PassMethods._Aux.DRIFT2;
            k1 = sl * PassMethods._Aux.KICK1;
            k2 = sl * PassMethods._Aux.KICK2;
        
            (polynom_a,polynom_b) = (element.polynom_a, element.polynom_b)
            n = max([len(polynom_a), len(polynom_b)])
            polynom_a.extend((n-len(polynom_a))*[0])
            polynom_b.extend((n-len(polynom_b))*[0])
          
            if element.t_in is not None:
                PassMethods._Aux.translate_pos(pos, element.t_in)
            if element.r_in is not None:
                PassMethods._Aux.rotate_pos(pos, element.r_in)
            for _ in range(element.nr_steps):
                norm   = 1.0/(1.0 + pos.de)
                norml1 = l1 * norm
                norml2 = l2 * norm
                PassMethods._Aux.fastdrift(pos, norml1)
                PassMethods._Aux.strthinkick(pos, k1, polynom_a, polynom_b) 
                PassMethods._Aux.fastdrift(pos, norml2)
                PassMethods._Aux.strthinkick(pos, k2, polynom_a, polynom_b)
                PassMethods._Aux.fastdrift(pos, norml2)
                PassMethods._Aux.strthinkick(pos, k1, polynom_a, polynom_b)
                PassMethods._Aux.fastdrift(pos, norml1)  
            if element.r_out is not None:
                PassMethods._Aux.rotate_pos(pos, element.r_out)
            if element.t_out is not None:
                PassMethods._Aux.translate_pos(pos, element.t_out)
                
        @staticmethod
        def map_bnd_mpole_symplectic4_pass(pos, element):            
              
            sl = element.length / float(element.nr_slices)    
            l1 = sl * PassMethods._Aux.DRIFT1
            l2 = sl * PassMethods._Aux.DRIFT2
            k1 = sl * PassMethods._Aux.KICK1
            k2 = sl * PassMethods._Aux.KICK2
            
            (polynom_a,polynom_b) = (element.polynom_a, element.polynom_b)
            n = max([len(polynom_a), len(polynom_b)])
            polynom_a.extend((n-len(polynom_a))*[0])
            polynom_b.extend((n-len(polynom_b))*[0])
        
            irho = element.angle / element.length
            
            if element.t_in is not None:
                PassMethods._Aux.translate_pos(pos, element.t_in)
            if element.r_in is not None:
                PassMethods._Aux.rotate_pos(pos, element.r_in)
            if element.fint_in is not None:
                PassMethods._Aux.edge_fringe(pos, irho, element.angle_in, element.fint_in, element.gap)
            else:
                PassMethods._Aux.edge(pos, irho, element.angle_in)
                
            for _ in range(element.nr_slices):
                PassMethods._Aux.drift(pos, l1)
                PassMethods._Aux.bndthinkick(pos, k1, polynom_a, polynom_b, irho)
                PassMethods._Aux.drift(pos, l2)
                PassMethods._Aux.bndthinkick(pos, k2, polynom_a, polynom_b, irho)
                PassMethods._Aux.drift(pos, l2)
                PassMethods._Aux.bndthinkick(pos, k1, polynom_a, polynom_b, irho)
                PassMethods._Aux.drift(pos, l1)
             
            if element.fint_out is not None:
                PassMethods._Aux.edge_fringe(pos, irho, element.angle_out, element.fint_out, element.gap)
            else:
                PassMethods._Aux.edge(pos, irho, element.angle_out)   
            if element.r_out is not None:
                PassMethods._Aux.rotate_pos(pos, element.r_out)
            if element.t_out is not None:
                PassMethods._Aux.translate_pos(pos, element.t_out)
         
        @staticmethod
        def map_corrector_pass(pos, element):
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
            
        @staticmethod
        def map_cavity_pass(pos, element):            
            nv = element.voltage / element.energy
            
            if element.length == 0:
                pos.de +=  -nv * mfuncs.sin(2*math.pi*element.frequency*pos.dl/constants.c)
            else:
                # drift half length
                pnorm   = 1.0 / (1.0 + pos.de)
                norml   = (0.5 * element.length) * pnorm
                pos.rx += norml * pos.px
                pos.ry += norml * pos.py
                pos.dl += 0.5 * norml * pnorm * (pos.px**2 + pos.py**2)
                # longitudinal momentum kick 
                pos.de += -nv * mfuncs.sin(2*math.pi*element.frequency*pos.dl/constants.c)
                # drift half length
                pnorm   = 1.0 / (1.0 + pos.de)
                norml   = (0.5 * element.length) * pnorm                
                pos.rx += norml * pos.px
                pos.ry += norml * pos.py
                pos.dl += 0.5 * norml * pnorm * (pos.px**2 + pos.py**2)
        
        @staticmethod
        def map_thinquad_pass(pos, element):
            raise Exception('pass method not implemented!')
        
        @staticmethod
        def map_thinsext_pass(pos, element):
            raise Exception('pass method not implemented!')
        
     
        
    maps  = {  pm_identity_pass              : _Aux.map_identity_pass,
               pm_drift_pass                 : _Aux.map_drift_pass,
               pm_str_mpole_symplectic4_pass : _Aux.map_str_mpole_symplectic4_pass,
               pm_bnd_mpole_symplectic4_pass : _Aux.map_bnd_mpole_symplectic4_pass,
               pm_corrector_pass             : _Aux.map_corrector_pass,
               pm_cavity_pass                : _Aux.map_cavity_pass,
               pm_thinquad_pass              : _Aux.map_thinquad_pass,
               pm_thinsext_pass              : _Aux.map_thinsext_pass,               
            }
    

import passmethods

class marker(object):
    def __init__(self,     
         fam_name, 
         pass_method = passmethods.pm_drift_pass,
         length      = 0.0,
         nr_steps    = 1,
         hkick       = None,
         vkick       = None,
         angle       = None,
         angle_in    = None,
         angle_out   = None,
         gap         = None,
         fint_in     = None,
         fint_out    = None,
         thin_KL     = None,
         thin_SL     = None,
         frequency   = None,
         voltage     = None,
         polynom_a   = None,
         polynom_b   = None,
         kicktable   = None,
         hmax        = None,
         vmax        = None,
         t_in        = None, 
         t_out       = None,
         r_in        = None,
         r_out       = None,     
         **kwargs
         ):
        
        if angle       is not None: self.angle       = angle
        if angle_in    is not None: self.angle_in    = angle_in
        if angle_out   is not None: self.angle_out   = angle_out
        if gap         is not None: self.gap         = gap
        if fint_in     is not None: self.fint_in     = fint_in
        if fint_out    is not None: self.fint_out    = fint_out
        if thin_KL     is not None: self.thin_KL     = thin_KL
        if thin_SL     is not None: self.thin_SL     = thin_SL
        if frequency   is not None: self.frequency   = frequency
        if voltage     is not None: self.voltage     = voltage
        if polynom_a   is not None: self.polynom_a   = polynom_a
        if polynom_b   is not None: self.polynom_b   = polynom_b
        if kicktable   is not None: self.kicktable   = kicktable
        if hmax        is not None: self.hmax        = hmax
        if vmax        is not None: self.vmax        = vmax
        if t_in        is not None: self.t_in        = t_in
        if t_out       is not None: self.t_out       = t_out
        if r_in        is not None: self.r_in        = r_in
        if r_out       is not None: self.r_out       = r_out
        
    def __str__(self):
        
        r  = ''
        r +=   '{0:<15s} {1}'.format('fam_name',    self.fam_name)
        r += '\n{0:<15s} {1}'.format('pass_method', self.pass_method)
        r += '\n{0:<15s} {1}'.format('length[m]',   str(self.length))
        r += '\n{0:<15s} {1}'.format('nr_steps',    str(self.nr_steps))
        try: r += '\n{0:<15s} {1}'.format('hkick[rad]',     str(self.hkick))
        except: pass
        try: r += '\n{0:<15s} {1}'.format('vkick[rad]',     str(self.vkick))
        except: pass
        try: r += '\n{0:<15s} {1}'.format('angle[rad]',     str(self.angle))
        except: pass
        try: r += '\n{0:<15s} {1}'.format('angle_in[rad]',  str(self.angle_in))
        except: pass
        try: r += '\n{0:<15s} {1}'.format('angle_out[rad]', str(self.angle_out))
        except: pass  
        try: r += '\n{0:<15s} {1}'.format('gap[m]',         str(self.gap))
        except: pass
        try: r += '\n{0:<15s} {1}'.format('fint_in',        str(self.fint_in))
        except: pass
        try: r += '\n{0:<15s} {1}'.format('fint_out',       str(self.fint_out))
        except: pass
        
        
        try: r += '  polynom_a: ' + str(self.polynom_a) + '\n'
        except: pass
        try: r += '  polynom_b: ' + str(self.polynom_b) + '\n'
        except: pass
        try: r += '          k: ' + str(self.k) + '\n'
        except: pass
        try: r += '         kl: ' + str(self.kl) + '\n'
        except: pass
        try: r += '         sl: ' + str(self.sl) + '\n'
        except: pass
        try: r += ' kick_angle: ' + str(self.kick_angle) + '\n'
        except: pass
        try: r += '    voltage: ' + str(self.voltage) + '\n'
        except: pass
        try: r += '  frequency: ' + str(self.frequency) + '\n'
        except: pass
        try: r += '     energy: ' + str(self.energy) + '\n'
        except: pass
        try: r += '    hnumber: ' + str(self.hnumber) + '\n'
        except: pass
        try: r += '       t_in: ' + str(self.t_in) + '\n'
        except: pass
        try: r += '       r_in: ' + str(self.r_in) + '\n'
        except: pass
        try: r += '    fint_in: ' + str(self.fint_in) + '\n'
        except: pass
        try: r += '      t_out: ' + str(self.t_out) + '\n'
        except: pass
        try: r += '      r_out: ' + str(self.r_out) + '\n'
        except: pass
        try: r += '   fint_out: ' + str(self.fint_out) + '\n'
        except: pass
        return r    
    
    
class drift(marker):
    def __init__(self, pass_method = passmethods.drift_pass, **kwargs):
        marker.__init__(self, pass_method = pass_method, **kwargs)

class corrector(marker):
    def __init__(self, pass_method = passmethods.corrector_pass, kick_angle  = None, **kwargs):
        if kick_angle == None: kick_angle = [0,0]
        marker.__init__(self, pass_method = pass_method, kick_angle = kick_angle, **kwargs)
        
class rfcavity(marker):
    def __init__(self, voltage, frequency, energy, hnumber, pass_method = passmethods.cavity_pass, **kwargs):
        marker.__init__(self, pass_method = pass_method, voltage = voltage, frequency = frequency, energy = energy, hnumber = hnumber, **kwargs)

class quadrupole(marker):
    def __init__(self, pass_method = passmethods.str_mpole_symplectic4_pass, nr_steps = 10, polynom_a = None, polynom_b = None, **kwargs): 
        if polynom_a == None: polynom_a = [0,0]
        if polynom_b == None: polynom_b = [0,0] 
        if 'k' in kwargs: 
            if ('kl' in kwargs) or (pass_method == passmethods.thinquad_pass):
                raise Exception('Inconsistent marker parameters!')
            polynom_b[1] = kwargs['k']
            del kwargs['k']
        if 'kl' in kwargs:
            if ('k' in kwargs) or (pass_method != passmethods.thinquad_pass):
                raise Exception('Inconsistent marker parameters!')
        marker.__init__(self, pass_method = pass_method, nr_steps = nr_steps, polynom_a = polynom_a, polynom_b = polynom_b, **kwargs)

class sextupole(marker):
    def __init__(self, pass_method = passmethods.str_mpole_symplectic4_pass, nr_steps = 5, polynom_a = None, polynom_b = None, **kwargs): 
        if polynom_a == None: polynom_a = [0,0,0]
        if polynom_b == None: polynom_b = [0,0,0] 
        if 's' in kwargs: 
            if ('sl' in kwargs) or (pass_method == 'thinsext_pass'):
                raise Exception('Inconsistent marker parameters!')
            polynom_b[2] = kwargs['s']
            del kwargs['s']
        if 'sl' in kwargs:
            if ('s' in kwargs) or (pass_method != 'thinsext_pass'):
                raise Exception('Inconsistent marker parameters!')
        marker.__init__(self, pass_method = pass_method, nr_steps = nr_steps, polynom_a = polynom_a, polynom_b = polynom_b, **kwargs)

class rbend(marker):
    def __init__(self, length, angle, pass_method = passmethods.bnd_mpole_symplectic4_pass, nr_steps = 10, polynom_a = None, polynom_b = None, gap = 0, **kwargs):
        if polynom_a == None: polynom_a = [0,0,0]
        if polynom_b == None: polynom_b = [0,0,0]
        if 'k' in kwargs:
            polynom_b[1] = kwargs['k']
            del kwargs['k']
        if 's' in kwargs:
            polynom_b[2] = kwargs['s']
            del kwargs['s']
        if 'angle_in' not in kwargs:
            kwargs['angle_in'] = 0.5 * angle
        if 'angle_out' not in kwargs:
            kwargs['angle_out'] = 0.5 * angle
        marker.__init__(self, pass_method = pass_method, length = length, angle = angle, gap = gap, nr_steps = nr_steps, polynom_a = polynom_a, polynom_b = polynom_b, **kwargs)



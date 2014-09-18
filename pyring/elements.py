import passmethods


class marker(object):
    def __init__(self,     
         fam_name, 
         length      = 0,
         nr_steps    = 1,
         pass_method = passmethods.identity_pass,
         angle       = None,
         gap         = None,
         polynom_a   = None,
         polynom_b   = None,
         k           = None,
         kl          = None,
         s           = None,
         sl          = None,
         kick_angle  = None,
         frequency   = None,
         voltage     = None,
         energy      = None,
         hnumber     = None,
         t_in        = None,
         r_in        = None,
         angle_in    = None,
         fint_in     = None,
         t_out       = None,
         r_out       = None,
         angle_out   = None,
         fint_out    = None,
         **kwargs
         ):
        
        if fam_name    is not None: self.fam_name    = fam_name
        if length      is not None: self.length      = length
        if nr_steps    is not None: self.nr_steps    = nr_steps
        if pass_method is not None: self.pass_method = pass_method
        
        if angle       is not None: self.angle       = angle
        if gap         is not None: self.gap         = gap
        if polynom_a   is not None: self.polynom_a   = polynom_a
        if polynom_b   is not None: self.polynom_b   = polynom_b
        
        if k           is not None: self.k           = k
        if kl          is not None: self.kl          = kl
        if sl          is not None: self.sl          = sl
        if kick_angle  is not None: self.kick_angle  = kick_angle
        if voltage     is not None: self.voltage     = voltage
        if frequency   is not None: self.frequency   = frequency
        if energy      is not None: self.energy      = energy
        if hnumber     is not None: self.hnumber     = hnumber
        
        if t_in        is not None: self.t_in        = t_in
        if r_in        is not None: self.r_in        = r_in
        if angle_in    is not None: self.angle_in    = angle_in
        if fint_in     is not None: self.fint_in     = fint_in
        
        if t_out       is not None: self.t_out       = t_out
        if r_out       is not None: self.r_out       = r_out
        if angle_out   is not None: self.angle_out   = angle_out 
        if fint_out    is not None: self.fint_out    = fint_out
        
    def __str__(self):
        r  = ''
        try: r += '   fam_name: ' + self.fam_name + '\n' 
        except: pass
        try: r += '     length: ' + str(self.length) + '\n'
        except: pass
        try:
            pm = passmethods.pm_dict[self.pass_method] 
            r +=  'pass_method: ' + str(pm[0]) + '\n'
        except: pass
        try: r += '      angle: ' + str(self.angle) + '\n'
        except: pass
        try: r += '   angle_in: ' + str(self.angle_in) + '\n'
        except: pass
        try: r += '  angle_out: ' + str(self.angle_out) + '\n'
        except: pass
        try: r += '        gap: ' + str(self.gap) + '\n'
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



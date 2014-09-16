class FieldMapException(Exception):
    pass


class FieldMap:
    def __init__(self, fname):
        self.read_fieldmap(fname)


    def read_fieldmap(self, fname):

        
        with open(fname, 'r') as fp:
            content = fp.read()
        
        ''' finds index of data section start '''
        idx = content.find('Z[mm]')
        idx = content.find('\n', idx+1)
        idx = content.find('\n', idx+1)
            
        ''' data section '''
        import numpy as np
        raw_data = np.fromstring(content[idx+1:], dtype=float, sep=' ')
        data = raw_data.view()
        data.shape = (-1,6)
        # position data
        rx = sorted(list(set(data[:,0])))
        ry = sorted(list(set(data[:,1])))
        rz = sorted(list(set(data[:,2])))
        self.rx_min, self.rx_max, self.rx_nrpts = min(rx), max(rx), len(rx)
        self.ry_min, self.ry_max, self.ry_nrpts = min(ry), max(ry), len(ry)
        self.rz_min, self.rz_max, self.rz_nrpts = min(rz), max(rz), len(rz)
        if self.rx_nrpts * self.ry_nrpts * self.rz_nrpts != data.shape[0]:
            raise FieldMapException('not a rectangular grid')
        self.rx_step = (self.rx_max - self.rx_min) / (self.rx_nrpts - 1.0) if self.rx_nrpts > 1 else 0.0            
        self.ry_step = (self.ry_max - self.ry_min) / (self.ry_nrpts - 1.0) if self.ry_nrpts > 1 else 0.0
        self.rz_step = (self.rz_max - self.rz_min) / (self.rz_nrpts - 1.0) if self.rz_nrpts > 1 else 0.0
        try:
            self.rx_zero = rx.index(0)
        except ValueError:
            self.rx_zero = None
        try:
            self.ry_zero = ry.index(0)
        except ValueError:
            self.ry_zero = None
        try:
            self.rz_zero = rz.index(0)
        except ValueError:
            self.rz_zero = None
            
        # field data
        self.bx, self.by, self.bz = data[:,3].view(), data[:,4].view(), data[:,5].view()
        self.bx.shape, self.by.shape, self.bz.shape = (-1,self.rx_nrpts), (-1,self.rx_nrpts), (-1,self.rx_nrpts)
        self.bx = [np.transpose(self.bx)]
        self.by = [np.transpose(self.by)]
        self.bz = [np.transpose(self.bz)]
        
        
        ''' header section '''
        lines = content[:idx].split('\n')
        for line in lines:
            
            # empty line or comment
            if line[0] == '#':
                continue
            words = line.split()
            if not words:
                continue
            
            cmd = words[0].lower()
            if cmd == 'nome_do_mapa:':
                self.fieldmap_label = ' '.join(words[1:])
                continue
            if cmd == 'data_hora:':
                self.timestamp = ' '.join(words[1:])
                continue
            if cmd == 'nome_do_arquivo:':
                self.filename = ' '.join(words[1:])
                continue
            if cmd == 'numero_de_imas:':
                self.nr_magnets = int(words[1])
                continue
            if cmd == 'nome_do_ima:':
                self.magnet_label = ' '.join(words[1:])
                continue
            if cmd == 'gap[mm]:':
                self.gap = float(words[1]) #[mm]
                continue
            if cmd == 'gap_controle[mm]:':
                self.control_gap = float(words[1]) #[mm]
                continue
            if cmd == 'comprimento[mm]:':
                self.length = float(words[1]) #[mm]
                continue
            if cmd == 'corrente[a]:':
                try:
                    self.current = float(words[1])#[A]
                except ValueError:
                    self.current = None
                continue
            
    def index2indices(self, i):
        raise NotImplementedError

    def pos2indices(self, rx,ry,rz):
        iy = int(round((ry - self.ry_min) / self.ry_step)) if self.ry_nrpts > 1 else 0
        ix = int(round((rx - self.rx_min) / self.rx_step)) if self.rx_nrpts > 1 else 0
        iz = int(round((rz - self.rz_min) / self.rz_step)) if self.rz_nrpts > 1 else 0
        return ix,iy,iz


    def __str__(self):
        r = ''
        r += '{0:<15s} {1}\n'.format('filename:', self.filename)
        r += '{0:<15s} {1}\n'.format('timestamp:', self.timestamp)
        if self.ry_nrpts == 1: 
            r += '{0:<15s} {3} point in [{1},{2}] (step of {4:f})\n'.format('ry[mm]:', self.ry_min, self.ry_max, self.ry_nrpts, self.ry_step)
        else:
            r += '{0:<15s} {3} points in [{1},{2}] (step of {4:f})\n'.format('ry[mm]:', self.ry_min, self.ry_max, self.ry_nrpts, self.ry_step)
        if self.rx_nrpts == 1: 
            r += '{0:<15s} {3} point in [{1},{2}] (step of {4:f})\n'.format('rx[mm]:', self.rx_min, self.rx_max, self.rx_nrpts, self.rx_step)
        else:
            r += '{0:<15s} {3} points in [{1},{2}] (step of {4:f})\n'.format('rx[mm]:', self.rx_min, self.rx_max, self.rx_nrpts, self.rx_step)
        if self.rz_nrpts == 1: 
            r += '{0:<15s} {3} point in [{1},{2}] (step of {4:f})\n'.format('rz[mm]:', self.rz_min, self.rz_max, self.rz_nrpts, self.rz_step)
        else:
            r += '{0:<15s} {3} points in [{1},{2}] (step of {4:f})\n'.format('rz[mm]:', self.rz_min, self.rz_max, self.rz_nrpts, self.rz_step)    
        r += '{0:<15s} min:{1:+8.5f} max:{2:+8.5f}\n'.format('by[T]@axis:', 
        min(self.by[self.ry_zero][self.rx_zero]), max(self.by[self.ry_zero][self.rx_zero])) 
        r += '{0:<15s} min:{1:+8.5f} max:{2:+8.5f}\n'.format('bx[T]@axis:', 
        min(self.bx[self.ry_zero][self.rx_zero]), max(self.bx[self.ry_zero][self.rx_zero])) 
        r += '{0:<15s} min:{1:+8.5f} max:{2:+8.5f}\n'.format('bz[T]@axis:', 
        min(self.bz[self.ry_zero][self.rx_zero]), max(self.bz[self.ry_zero][self.rx_zero])) 
        return r

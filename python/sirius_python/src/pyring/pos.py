

class Pos(object):

    #(rx,px,ry,py,de,dl) = (0,1,2,3,4,5)
    
    def __init__(self, rx=0.0, px=0.0, ry=0.0, py=0.0, de=0.0, dl=0.0):
        self._data = [rx,px,ry,py,de,dl]     
    @property 
    def rx(self): return  self._data[0]
    @rx.setter
    def rx(self, value): self._data[0] = value; return self._data[0]
    @property 
    def px(self): return  self._data[1]
    @px.setter
    def px(self, value): self._data[1] = value; return self._data[1]
    @property 
    def ry(self): return  self._data[2]
    @ry.setter
    def ry(self, value): self._data[2] = value; return self._data[2]
    @property 
    def py(self): return  self._data[3]
    @py.setter
    def py(self, value): self._data[3] = value; return self._data[3]
    @property 
    def de(self): return  self._data[4]
    @de.setter
    def de(self, value): self._data[4] = value; return self._data[4]
    @property 
    def dl(self): return  self._data[5]
    @dl.setter
    def dl(self, value): self._data[5] = value; return self._data[5]
    def data(self):
        return self._data
    def __str__(self):
        return '('+str(self._data[0])+','+str(self._data[1])+','+str(self._data[2])+','+str(self._data[3])+','+str(self._data[4])+','+str(self._data[5])+')'
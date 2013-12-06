"""
DateTimeLine
    Keep a matplotlib (date,y) line and related methods.

Afonso Haruo Carnielli Mukai (FAC - LNLS)

2013-11-27: v0.1
"""

import datetime
import numpy
import CustomLine


class DateTimeLengthError(Exception):
    pass


class DateTimeLine(CustomLine.CustomLine):
    
    """
    Keep a matplotlib line for datetime data and the maximum array length.
    """
    
    def __init__(self, line, max_data_length=1000):
        """        
        line -- matplotlib Line2D
        max_data_length -- the maximum array length (default 1000)        
        """
        super(DateTimeLine, self).__init__(line)
        self._max_data_length = max_data_length
        self.set_line_style('-')
        self.set_marker('None')
        
    def get_length(self):
        x = self.get_x()
        y = self.get_y()
        if not len(x) == len(y):
            raise DateTimeLengthError
        else:
            return len(x)
    
    def get_max_length(self):
        return self._max_data_length
    
    def set_x(self, array):
        self._check_array_length(array)
        super(DateTimeLine, self).set_x(array)
    
    def set_y(self, array):
        self._check_array_length(array)
        super(DateTimeLine, self).set_y(array)
        
    def clear(self):
        self.set_x([])
        self.set_y([])
        
    def add_y(self, y):
        x = datetime.datetime.now()
        self.add_xy(x, y)
    
    def add_xy(self, x, y):        
        current_x = self.get_x()
        current_y = self.get_y()
        length = self.get_length()
        if length < self._max_data_length:
            new_x = self._append(current_x, x)
            new_y = self._append(current_y, y)            
        else:
            new_x = self._remove_first_and_append(current_x, x)
            new_y = self._remove_first_and_append(current_y, y)
        self.set_x(new_x)
        self.set_y(new_y)
    
    def _append(self, array, element):
        return numpy.append(array, element)
    
    def _remove_first_and_append(self, array, element):
        return numpy.append(array[1:], element)
        
    def _check_array_length(self, array):
        if len(array) > self._max_data_length:
            raise DateTimeLengthError

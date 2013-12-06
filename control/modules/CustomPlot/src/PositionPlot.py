"""
PositionPlot
    Class for embedding matplotlib position plots in PyQt GUI. 

Afonso Haruo Carnielli Mukai (FAC - LNLS)

2013-12-04: v0.1
"""

import CustomPlot
import ColorConversion


DEFAULT_BACKGROUND_COLOR = ColorConversion.DEFAULT_BACKGROUND_COLOR
DEFAULT_AXIS_BACKGROUND_COLOR = ColorConversion.DEFAULT_AXIS_BACKGROUND_COLOR
DEFAULT_AXIS_ELEMENTS_COLOR = ColorConversion.DEFAULT_AXIS_ELEMENTS_COLOR


class IntervalBoundsError(Exception):
    pass


class LengthError(Exception):
    pass


class PositionPlot(CustomPlot.CustomPlot):
    
    """Embed a position plot in PyQt."""
    
    def __init__(self,
                 background_color=DEFAULT_BACKGROUND_COLOR,
                 axis_background_color=DEFAULT_AXIS_BACKGROUND_COLOR,
                 axis_elements_color=DEFAULT_AXIS_ELEMENTS_COLOR,
                 autoscale=True,
                 axis_extra_spacing=0,
                 interval_min=0,
                 interval_max=1,
                 interpolate=False):
        
        if not interval_min <= interval_max:
            raise IntervalBoundsError
        
        self.super = super(PositionPlot, self)
        self.super.__init__(background_color=background_color,
                            axis_background_color=axis_background_color,
                            axis_elements_color=axis_elements_color,
                            autoscale=autoscale,
                            axes_extra_spacing=axis_extra_spacing)
                
        self._interval_min = interval_min
        self._interval_max = interval_max
        self._interpolate = interpolate
        
        self.x_axis = (self._interval_min, self._interval_max)
        
        self._ticks = {}
        self._selected_ticks = []
       
    @property 
    def interpolate(self):
        return self._interpolate
    
    @interpolate.setter
    def interpolate(self, value):
        self._interpolate = value
    
    @property
    def ticks(self):
        return self._ticks
    
    @property
    def selected_ticks(self):
        return self._selected_ticks
        
    def define_ticks(self, names, pos):
        if len(names) != len(pos):
            raise LengthError
        name_pos_pairs = zip(names, pos)
        self._ticks = dict(name_pos_pairs)
    
    def select_ticks(self, names):
        for name in names:
            if not self._ticks.has_key(name):
                raise KeyError
        self._selected_ticks = names
    
    def _find_axis_min_and_max(self, axis):
        if axis == 'y':
            result = self.super._find_axis_min_and_max(axis)
        else:
            new_min = self._interval_min
            new_max = self._interval_max
            result = (new_min, new_max)
        return result

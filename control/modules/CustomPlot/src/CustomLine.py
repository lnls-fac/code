"""
CustomLine
    Keep a matplotlib line and related methods.

Afonso Haruo Carnielli Mukai (FAC - LNLS)

2013-11-22: v0.1
"""

import ColorConversion


class CustomLine(object):

    """
    Keep a matplotlib line and allow access to data and options.

    Public methods (prefix with get_ or set_):
    x: array
    y: array
    color: RGBA tuple [0,255] or 'red', 'green', 'blue' ... 
    marker_fill: 'full', 'none'
    line_style: '-', '--', '-.', ':', 'None'
    line_width: value in points
    marker: '.', 'o', '^', 's', 'x', 'None'
    marker_face_color: RGBA tuple [0,255] or 'red', 'green', 'blue' ...
    marker_size: value in points 
    """
    
    def __init__(self, line):
        """line -- a matplotlib Line2D"""
        self.line = line
    
    def get_x(self):
        return self.line.get_xdata()

    def set_x(self, array):
        self.line.set_xdata(array)

    def get_y(self): 
        return self.line.get_ydata()

    def set_y(self, array):
        self.line.set_ydata(array)
        
    def get_color(self):
        color = self.line.get_color()
        return ColorConversion.denormalize_color(color)
    
    def set_color(self, color):
        new_color = ColorConversion.normalize_color(color)
        self.line.set_color(new_color)
        
    def get_marker_fill(self):
        return self.line.get_fillstyle()
        
    def set_marker_fill(self, style):
        self.line.get_fillstyle(style)
    
    def get_line_style(self):
        return self.line.get_linestyle()
    
    def set_line_style(self, style):
        self.line.set_linestyle(style)
        
    def get_line_width(self):
        return self.line.get_linewidth()
        
    def set_line_width(self, style):
        self.line.set_linewidth(style)
    
    def get_marker(self):
        return self.line.get_marker()
    
    def set_marker(self, marker):
        self.line.set_marker(marker)
    
    def get_marker_face_color(self):
        color = self.line.get_markerfacecolor()
        return ColorConversion.denormalize_color(color)
    
    def set_marker_face_color(self, color):
        new_color = ColorConversion.normalize_color(color)
        self.line.set_markerfacecolor(new_color)

    def get_marker_size(self):
        return self.line.get_markersize()
    
    def set_marker_size(self, size):
        self.line.set_markersize(size)

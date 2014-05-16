from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.fig.patch.set_facecolor('1')
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class matplotlibWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.canvas.ax1.set_xlabel('Volta')
        self.canvas.ax1.set_ylabel('Amplitude (V.s)')
        self.canvas.ax2.set_xlabel('Voltas')
        self.canvas.ax2.set_ylabel('Amplitude (V.s)')
        self.canvas.fig.tight_layout()
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
##        self.toolbar = NavigationToolbar(self.canvas, self)
##        self.vbl.addWidget(self.toolbar)        
        self.setLayout(self.vbl)

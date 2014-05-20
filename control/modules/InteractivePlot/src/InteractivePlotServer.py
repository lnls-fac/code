"""
InteractivePlotServer
    Interactive plot window. 

Afonso Haruo Carnielli Mukai (FAC - LNLS)

2013-12-17: v0.1
"""

import sys
from PyQt4 import QtCore, QtGui
import CustomPlot
import CustomToolbar


class Window(QtGui.QWidget):
    def __init__(self, shm, conn, window_title, parent=None):
        super(Window, self).__init__(parent)
        
        self.plot = CustomPlot.CustomPlot()
        self.toolbar = CustomToolbar.CustomToolbar(self.plot, self)
        
        layout = QtGui.QVBoxLayout()        
        layout.addWidget(self.plot)
        layout.addWidget(self.toolbar)
                
        self.setLayout(layout)
        self.setWindowTitle(window_title)
        
        self.shm = shm
        self.conn = conn
        
        self.timer = QtCore.QTimer()
        self.timer.start(100)


def start(shm, conn, window_title):    
    app = QtGui.QApplication(sys.argv)
    window = Window(shm, conn, window_title)
    window.show()
    app.exec_()

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'teste.ui'
#
# Created: Wed Jun 18 14:44:24 2014
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(400, 111)
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.pBrodar_prog = QtGui.QPushButton(Form)
        self.pBrodar_prog.setGeometry(QtCore.QRect(160, 60, 101, 23))
        self.pBrodar_prog.setText(QtGui.QApplication.translate("Form", "Rodar programa", None, QtGui.QApplication.UnicodeUTF8))
        self.pBrodar_prog.setObjectName(_fromUtf8("pBrodar_prog"))
        self.pBproc_pasta = QtGui.QPushButton(Form)
        self.pBproc_pasta.setGeometry(QtCore.QRect(90, 20, 231, 23))
        self.pBproc_pasta.setText(QtGui.QApplication.translate("Form", "Procurar pasta com medidas", None, QtGui.QApplication.UnicodeUTF8))
        self.pBproc_pasta.setObjectName(_fromUtf8("pBproc_pasta"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass


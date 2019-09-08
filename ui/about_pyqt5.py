# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about_pyqt5.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_pyqt5_dialog(object):
    def setupUi(self, pyqt5_dialog):
        pyqt5_dialog.setObjectName("pyqt5_dialog")
        pyqt5_dialog.resize(409, 248)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/proPrefix/image/Qt_logo_2016.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        pyqt5_dialog.setWindowIcon(icon)
        pyqt5_dialog.setAutoFillBackground(True)
        self.textBrowser = QtWidgets.QTextBrowser(pyqt5_dialog)
        self.textBrowser.setGeometry(QtCore.QRect(100, 10, 300, 220))
        self.textBrowser.setMinimumSize(QtCore.QSize(300, 220))
        self.textBrowser.setMaximumSize(QtCore.QSize(300, 220))
        self.textBrowser.setStyleSheet("background: transparent;")
        self.textBrowser.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(pyqt5_dialog)
        self.label.setGeometry(QtCore.QRect(10, 50, 81, 91))
        self.label.setStyleSheet("image:url(:/proPrefix/image/Qt_logo_2016.png)")
        self.label.setText("")
        self.label.setObjectName("label")

        self.retranslateUi(pyqt5_dialog)
        QtCore.QMetaObject.connectSlotsByName(pyqt5_dialog)

    def retranslateUi(self, pyqt5_dialog):
        _translate = QtCore.QCoreApplication.translate
        pyqt5_dialog.setWindowTitle(_translate("pyqt5_dialog", "关于pyqt5"))
        self.textBrowser.setHtml(_translate("pyqt5_dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"                    <html><head><meta name=\"qrichtext\" content=\"1\" /><style\n"
"                    type=\"text/css\">\n"
"                    p, li { white-space: pre-wrap; }\n"
"                    </style></head><body style=\" font-family:\'SimSun\'; font-size:9pt;\n"
"                    font-weight:400; font-style:normal;\">\n"
"                    <p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px;\n"
"                    -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'宋体\';\n"
"                    font-size:12pt; font-weight:600;\">关于PyQt5</span><span style=\"\n"
"                    font-family:\'宋体\';\"> </span></p>\n"
"                    <p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px;\n"
"                    -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'宋体\';\">Qt是一套跨平台的C++库，它们实现了高级API，可以访问现代桌面和移动系统的许多方面。\n"
"                    </span></p>\n"
"                    <p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px;\n"
"                    -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'宋体\';\">PyQt5是Qtv5的一套全面的Python绑定。\n"
"                    它实现为超过35个扩展模块，并使Python能够在所有支持的平台（包括iOS和Android）上用作C++的替代应用程序开发语言。 </span></p>\n"
"                    <p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px;\n"
"                    -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'宋体\';\">请前往</span><a\n"
"                    href=\"http://qt.io/licensing/\"><span style=\" font-family:\'宋体\'; text-decoration:\n"
"                    underline; color:#0000ff;\">http://qt.io/licensing/</span></a><span style=\"\n"
"                    font-family:\'宋体\';\">查看相关授权。</span> </p></body></html>\n"
"                "))

import ResFiles_rc

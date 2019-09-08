# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about_proj.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_about_proj(object):
    def setupUi(self, about_proj):
        about_proj.setObjectName("about_proj")
        about_proj.setEnabled(True)
        about_proj.resize(440, 240)
        about_proj.setMinimumSize(QtCore.QSize(440, 240))
        about_proj.setMaximumSize(QtCore.QSize(440, 240))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/proPrefix/image/spider.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        about_proj.setWindowIcon(icon)
        self.label = QtWidgets.QLabel(about_proj)
        self.label.setGeometry(QtCore.QRect(10, 70, 91, 101))
        self.label.setStyleSheet("image: url(:/proPrefix/image/spider.ico)")
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setText("")
        self.label.setObjectName("label")
        self.readme = QtWidgets.QTextBrowser(about_proj)
        self.readme.setEnabled(True)
        self.readme.setGeometry(QtCore.QRect(110, 10, 321, 241))
        self.readme.setAutoFillBackground(False)
        self.readme.setStyleSheet("background: transparent;")
        self.readme.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.readme.setAutoFormatting(QtWidgets.QTextEdit.AutoNone)
        self.readme.setDocumentTitle("")
        self.readme.setOverwriteMode(False)
        self.readme.setAcceptRichText(True)
        self.readme.setSearchPaths([])
        self.readme.setOpenExternalLinks(True)
        self.readme.setOpenLinks(True)
        self.readme.setObjectName("readme")

        self.retranslateUi(about_proj)
        QtCore.QMetaObject.connectSlotsByName(about_proj)

    def retranslateUi(self, about_proj):
        _translate = QtCore.QCoreApplication.translate
        about_proj.setWindowTitle(_translate("about_proj", "关于项目"))
        self.readme.setHtml(_translate("about_proj", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"                    <html><head><meta name=\"qrichtext\" content=\"1\" /><style\n"
"                    type=\"text/css\">\n"
"                    p, li { white-space: pre-wrap; }\n"
"                    </style></head><body style=\" font-family:\'SimSun\'; font-size:9pt;\n"
"                    font-weight:400; font-style:normal;\">\n"
"                    <p align=\"center\" style=\" margin-top:0px; margin-bottom:16px; margin-left:0px;\n"
"                    margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\"\n"
"                    font-family:\'-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif,Apple Color\n"
"                    Emoji,Segoe UI Emoji,Segoe UI Symbol\'; font-size:16px; font-weight:600; color:#24292e;\">机电事业部能源数据爬取软件</span></p>\n"
"                    <p style=\" margin-top:0px; margin-bottom:16px; margin-left:0px; margin-right:0px;\n"
"                    -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#24292e;\">该软件能爬取</span><a\n"
"                    href=\"http://energy.easynx.com/Energy/\"><span style=\" text-decoration:\n"
"                    underline; color:#0000ff;\">http://energy.easynx.com/Energy/</span></a><span\n"
"                    style=\" color:#24292e;\"> 后台管理界面中，</span><span style=\" font-weight:600;\n"
"                    color:#24292e;\">统计分析</span><span style=\" color:#24292e;\">选项下所有数据，并</span><span\n"
"                    style=\" font-weight:600; color:#24292e;\">定期</span><span style=\"\n"
"                    color:#24292e;\">（一般为15min）上传到</span><span style=\" color:#24292e;\n"
"                    background-color:rgba(27,31,35,0.047059);\">oracle</span><span style=\"\n"
"                    color:#24292e;\">数据库。</span> </p>\n"
"                    <p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\n"
"                    -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#24292e;\">本软件遵守GPLv3协议。</span></p>\n"
"                    <p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:16px; margin-left:0px;\n"
"                    margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Microsoft\n"
"                    YaHei,Arial,Verdana,Helvetica,sans-serif\'; font-size:14px; color:#333333;\"><br /></p></body></html>\n"
"                "))

import ResFiles_rc

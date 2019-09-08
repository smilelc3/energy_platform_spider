# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'web_setting.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_webSettingDialog(object):
    def setupUi(self, webSettingDialog):
        webSettingDialog.setObjectName("webSettingDialog")
        webSettingDialog.resize(633, 501)
        webSettingDialog.setLocale(QtCore.QLocale(QtCore.QLocale.Chinese, QtCore.QLocale.China))
        self.gridLayout_2 = QtWidgets.QGridLayout(webSettingDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.loginUrlLabel = QtWidgets.QLabel(webSettingDialog)
        self.loginUrlLabel.setObjectName("loginUrlLabel")
        self.gridLayout_2.addWidget(self.loginUrlLabel, 5, 0, 1, 1)
        self.infoUrlInput = QtWidgets.QLineEdit(webSettingDialog)
        self.infoUrlInput.setObjectName("infoUrlInput")
        self.gridLayout_2.addWidget(self.infoUrlInput, 16, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(webSettingDialog)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_2.addWidget(self.line_2, 4, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pwdInput = QtWidgets.QLineEdit(webSettingDialog)
        self.pwdInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pwdInput.setObjectName("pwdInput")
        self.gridLayout.addWidget(self.pwdInput, 1, 2, 1, 1)
        self.pwdLabel = QtWidgets.QLabel(webSettingDialog)
        self.pwdLabel.setObjectName("pwdLabel")
        self.gridLayout.addWidget(self.pwdLabel, 1, 1, 1, 1)
        self.pwdCheckBox = QtWidgets.QCheckBox(webSettingDialog)
        self.pwdCheckBox.setObjectName("pwdCheckBox")
        self.gridLayout.addWidget(self.pwdCheckBox, 1, 3, 1, 1)
        self.userInpput = QtWidgets.QLineEdit(webSettingDialog)
        self.userInpput.setObjectName("userInpput")
        self.gridLayout.addWidget(self.userInpput, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 4, 1, 1)
        self.userLabel = QtWidgets.QLabel(webSettingDialog)
        self.userLabel.setObjectName("userLabel")
        self.gridLayout.addWidget(self.userLabel, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 7, 0, 1, 1)
        self.hostLabel = QtWidgets.QLabel(webSettingDialog)
        self.hostLabel.setObjectName("hostLabel")
        self.gridLayout_2.addWidget(self.hostLabel, 0, 0, 1, 1)
        self.parentTreeUrlInput = QtWidgets.QLineEdit(webSettingDialog)
        self.parentTreeUrlInput.setObjectName("parentTreeUrlInput")
        self.gridLayout_2.addWidget(self.parentTreeUrlInput, 12, 0, 1, 1)
        self.loginUrlInput = QtWidgets.QLineEdit(webSettingDialog)
        self.loginUrlInput.setObjectName("loginUrlInput")
        self.gridLayout_2.addWidget(self.loginUrlInput, 6, 0, 1, 1)
        self.homeUrlLabel = QtWidgets.QLabel(webSettingDialog)
        self.homeUrlLabel.setObjectName("homeUrlLabel")
        self.gridLayout_2.addWidget(self.homeUrlLabel, 2, 0, 1, 1)
        self.childTreeUrlInput = QtWidgets.QLineEdit(webSettingDialog)
        self.childTreeUrlInput.setObjectName("childTreeUrlInput")
        self.gridLayout_2.addWidget(self.childTreeUrlInput, 14, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.OK = QtWidgets.QPushButton(webSettingDialog)
        self.OK.setMouseTracking(True)
        self.OK.setAutoFillBackground(False)
        self.OK.setStyleSheet("")
        self.OK.setCheckable(False)
        self.OK.setDefault(True)
        self.OK.setFlat(False)
        self.OK.setObjectName("OK")
        self.horizontalLayout_2.addWidget(self.OK)
        self.cancel = QtWidgets.QPushButton(webSettingDialog)
        self.cancel.setObjectName("cancel")
        self.horizontalLayout_2.addWidget(self.cancel)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 18, 0, 1, 1)
        self.homeUrlInput = QtWidgets.QLineEdit(webSettingDialog)
        self.homeUrlInput.setObjectName("homeUrlInput")
        self.gridLayout_2.addWidget(self.homeUrlInput, 3, 0, 1, 1)
        self.line = QtWidgets.QFrame(webSettingDialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 8, 0, 1, 1)
        self.parentTreeUrlLabel = QtWidgets.QLabel(webSettingDialog)
        self.parentTreeUrlLabel.setObjectName("parentTreeUrlLabel")
        self.gridLayout_2.addWidget(self.parentTreeUrlLabel, 11, 0, 1, 1)
        self.childTreeUrlLabel = QtWidgets.QLabel(webSettingDialog)
        self.childTreeUrlLabel.setObjectName("childTreeUrlLabel")
        self.gridLayout_2.addWidget(self.childTreeUrlLabel, 13, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem2, 17, 0, 1, 1)
        self.infoUrlLabel = QtWidgets.QLabel(webSettingDialog)
        self.infoUrlLabel.setObjectName("infoUrlLabel")
        self.gridLayout_2.addWidget(self.infoUrlLabel, 15, 0, 1, 1)
        self.hostInput = QtWidgets.QLineEdit(webSettingDialog)
        self.hostInput.setObjectName("hostInput")
        self.gridLayout_2.addWidget(self.hostInput, 1, 0, 1, 1)
        self.showMainPageLabel = QtWidgets.QLabel(webSettingDialog)
        self.showMainPageLabel.setObjectName("showMainPageLabel")
        self.gridLayout_2.addWidget(self.showMainPageLabel, 9, 0, 1, 1)
        self.showMainPageInput = QtWidgets.QLineEdit(webSettingDialog)
        self.showMainPageInput.setObjectName("showMainPageInput")
        self.gridLayout_2.addWidget(self.showMainPageInput, 10, 0, 1, 1)

        self.retranslateUi(webSettingDialog)
        self.cancel.clicked.connect(webSettingDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(webSettingDialog)
        webSettingDialog.setTabOrder(self.homeUrlInput, self.loginUrlInput)
        webSettingDialog.setTabOrder(self.loginUrlInput, self.userInpput)
        webSettingDialog.setTabOrder(self.userInpput, self.pwdInput)
        webSettingDialog.setTabOrder(self.pwdInput, self.pwdCheckBox)
        webSettingDialog.setTabOrder(self.pwdCheckBox, self.parentTreeUrlInput)
        webSettingDialog.setTabOrder(self.parentTreeUrlInput, self.childTreeUrlInput)
        webSettingDialog.setTabOrder(self.childTreeUrlInput, self.infoUrlInput)
        webSettingDialog.setTabOrder(self.infoUrlInput, self.OK)
        webSettingDialog.setTabOrder(self.OK, self.cancel)

    def retranslateUi(self, webSettingDialog):
        _translate = QtCore.QCoreApplication.translate
        webSettingDialog.setWindowTitle(_translate("webSettingDialog", "网页设置"))
        self.loginUrlLabel.setText(_translate("webSettingDialog", "登陆网页："))
        self.pwdLabel.setText(_translate("webSettingDialog", "密码："))
        self.pwdCheckBox.setText(_translate("webSettingDialog", "可见"))
        self.userLabel.setText(_translate("webSettingDialog", "用户名："))
        self.hostLabel.setText(_translate("webSettingDialog", "主机地址："))
        self.homeUrlLabel.setText(_translate("webSettingDialog", "根网页："))
        self.OK.setText(_translate("webSettingDialog", "确认"))
        self.cancel.setText(_translate("webSettingDialog", "取消"))
        self.parentTreeUrlLabel.setText(_translate("webSettingDialog", "总结点信息网页："))
        self.childTreeUrlLabel.setText(_translate("webSettingDialog", "子结点信息网页："))
        self.infoUrlLabel.setText(_translate("webSettingDialog", "子结点数据网页："))
        self.showMainPageLabel.setText(_translate("webSettingDialog", "获取总结点网页："))

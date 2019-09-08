import cx_Oracle as oracle
from PyQt5 import QtWidgets, QtGui, QtCore

from ui import web_setting, server_setting


# 数据设置

class server:
    def __init__(self):
        # 服务器参数配置初始化
        self.Dialog = QtWidgets.QDialog()
        self.SevSetUI = server_setting.Ui_dialog()
        self.SevSetUI.setupUi(self.Dialog)

        self.SevSetUI.host_input.textChanged['QString'].connect(self.genSevUrl)
        self.SevSetUI.port_input.textChanged['QString'].connect(self.genSevUrl)
        self.SevSetUI.sid_input.textChanged['QString'].connect(self.genSevUrl)
        self.SevSetUI.user_input.textChanged['QString'].connect(self.genSevUrl)
        self.SevSetUI.pwd_input.textChanged['QString'].connect(self.genSevUrl)

        self.SevSetUI.visible_check.stateChanged['int'].connect(self.pwd_visible_state_change)
        self.SevSetUI.visible_check.stateChanged['int'].connect(self.genSevUrl)

        # 端口号输入限制（仅仅输入数字）
        self.SevSetUI.port_input.setValidator(QtGui.QIntValidator())
        self.SevSetUI.port_input.textChanged.connect(self.max_port_limit)

        # 测试按钮绑定
        self.SevSetUI.test_button.clicked.connect(lambda: self.test_db_conn(needShow=True))

        # 确认按钮绑定
        self.SevSetUI.OK.clicked.connect(self.saveSevMsg)

        # 配置文件初始化
        self.settings = QtCore.QSettings('res/config.ini', QtCore.QSettings.IniFormat)
        self.settings.setIniCodec('UTF-8')

        # 界面展示参数初始化
        self.initSevMsg()

    # 最小/最大端口号限制
    def max_port_limit(self):
        if self.SevSetUI.port_input.text() and int(self.SevSetUI.port_input.text()) > 65535:
            self.SevSetUI.port_input.setText('65535')

    # 初始化服务器参数文件
    def initSevMsg(self):
        SQL_DATABASE_NAME = self.settings.value("ORACLE/SQL_DATABASE_NAME")
        SQL_DATABASE_PASSWORD = self.settings.value("ORACLE/SQL_DATABASE_PASSWORD")
        SQL_SERVER_HOST = self.settings.value("ORACLE/SQL_SERVER_HOST")
        SQL_SERVER_PORT = self.settings.value("ORACLE/SQL_SERVER_PORT")
        SQL_DATABASE_SID = self.settings.value("ORACLE/SQL_DATABASE_SID")
        if SQL_SERVER_HOST != 'localhost':
            self.SevSetUI.host_input.setText(SQL_SERVER_HOST)
        if SQL_SERVER_PORT != 1521:
            self.SevSetUI.port_input.setText(SQL_SERVER_PORT)
        self.SevSetUI.sid_input.setText(SQL_DATABASE_SID)
        self.SevSetUI.user_input.setText(SQL_DATABASE_NAME)
        self.SevSetUI.pwd_input.setText(SQL_DATABASE_PASSWORD)

    # url生成事件绑定
    def genSevUrl(self):
        SQL_DATABASE_NAME, SQL_DATABASE_PASSWORD, SQL_SERVER_HOST, SQL_SERVER_PORT, SQL_DATABASE_SID = self.getSevInput()
        if self.SevSetUI.visible_check.isChecked():
            self.SevSetUI.URL_input.setText(
                f'{SQL_DATABASE_NAME}/{SQL_DATABASE_PASSWORD}@{SQL_SERVER_HOST}:{SQL_SERVER_PORT}/{SQL_DATABASE_SID}')
        else:
            self.SevSetUI.URL_input.setText(
                f'{SQL_DATABASE_NAME}/' + '*' * len(
                    SQL_DATABASE_PASSWORD) + f'@{SQL_SERVER_HOST}:{SQL_SERVER_PORT}/{SQL_DATABASE_SID}')

    # 获取输入的结果
    def getSevInput(self) -> tuple:
        if self.SevSetUI.host_input.text():
            SQL_SERVER_HOST = self.SevSetUI.host_input.text()
        else:
            SQL_SERVER_HOST = 'localhost'  # 默认host

        SQL_DATABASE_SID = self.SevSetUI.sid_input.text()

        if self.SevSetUI.port_input.text():
            SQL_SERVER_PORT = int(self.SevSetUI.port_input.text())
        else:
            SQL_SERVER_PORT = 1521  # oracle 默认端口

        SQL_DATABASE_NAME = self.SevSetUI.user_input.text()
        SQL_DATABASE_PASSWORD = self.SevSetUI.pwd_input.text()
        return SQL_DATABASE_NAME, SQL_DATABASE_PASSWORD, SQL_SERVER_HOST, SQL_SERVER_PORT, SQL_DATABASE_SID

    # 密码可见绑定
    def pwd_visible_state_change(self):
        if self.SevSetUI.visible_check.isChecked():
            self.SevSetUI.pwd_input.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.SevSetUI.pwd_input.setEchoMode(QtWidgets.QLineEdit.Password)

    # 服务器配置字段拼写完整性检查
    def sevSpellCheck(self) -> bool:
        # 非空限制
        if not self.SevSetUI.sid_input.text():
            QtWidgets.QMessageBox.warning(
                self.Dialog, "数据库连接", f'SID字段不可为空')
            return False
        elif not self.SevSetUI.user_input.text():
            QtWidgets.QMessageBox.warning(
                self.Dialog, "数据库连接", f'用户名字段不可为空')
            return False
        elif not self.SevSetUI.pwd_input.text():
            QtWidgets.QMessageBox.warning(
                self.Dialog, "数据库连接", f'密码字段不可为空')
            return False
        return True

    # 数据库连接测试
    def test_db_conn(self, needShow=True) -> bool:
        if not self.sevSpellCheck():
            return False

        # 测试数据库
        SQL_DATABASE_NAME, SQL_DATABASE_PASSWORD, SQL_SERVER_HOST, SQL_SERVER_PORT, SQL_DATABASE_SID = self.getSevInput()
        try:
            oracle.connect(SQL_DATABASE_NAME, SQL_DATABASE_PASSWORD,
                           f'{SQL_SERVER_HOST}:{SQL_SERVER_PORT}/{SQL_DATABASE_SID}')

        except oracle.DatabaseError as e:
            if e.args[0].code == 1017:
                QtWidgets.QMessageBox.warning(
                    self.Dialog, "数据库连接", '登陆错误，无效的用户名/密码')
            else:
                QtWidgets.QMessageBox.warning(
                    self.Dialog, "数据库连接", '错误' + e.__str__())
            return False
        else:
            if needShow:
                QtWidgets.QMessageBox.information(
                    self.Dialog, "数据库连接", '数据库连接成功！')
            return True

    # 保存数据库配置信息
    def saveSevMsg(self):
        if not self.sevSpellCheck():
            pass
        else:
            try:
                SQL_DATABASE_NAME, SQL_DATABASE_PASSWORD, SQL_SERVER_HOST, SQL_SERVER_PORT, SQL_DATABASE_SID = self.getSevInput()
                self.settings.setValue("ORACLE/SQL_DATABASE_NAME", SQL_DATABASE_NAME)
                self.settings.setValue("ORACLE/SQL_DATABASE_PASSWORD", SQL_DATABASE_PASSWORD)
                self.settings.setValue("ORACLE/SQL_SERVER_HOST", SQL_SERVER_HOST)
                self.settings.setValue("ORACLE/SQL_SERVER_PORT", SQL_SERVER_PORT)
                self.settings.setValue("ORACLE/SQL_DATABASE_SID", SQL_DATABASE_SID)
            except Exception as e:
                QtWidgets.QMessageBox.warning(
                    self.Dialog, "配置保存", '错误：' + e.__str__())
            self.Dialog.accept()


# 网页参数设置
class web:
    def __init__(self):
        # 服务器参数配置初始化
        self.Dialog = QtWidgets.QDialog()
        self.webSetUI = web_setting.Ui_webSettingDialog()
        self.webSetUI.setupUi(self.Dialog)
        self.webSetUI.hostInput.textChanged['QString'].connect(self.genHostUrl)
        self.webSetUI.homeUrlInput.textChanged['QString'].connect(self.genHomeUrl)

        # 确认按钮绑定
        self.webSetUI.OK.clicked.connect(self.saveWebMsg)

        # 密码可见性绑定
        self.webSetUI.pwdCheckBox.stateChanged['int'].connect(self.pwd_visible_state_change)

        self.settings = QtCore.QSettings('res/config.ini', QtCore.QSettings.IniFormat)
        self.settings.setIniCodec('UTF-8')

        self.initWebMsg()

    # server Host生成事件
    def genHostUrl(self):
        http_host = 'http://' + self.webSetUI.hostInput.text()
        self.webSetUI.homeUrlInput.setText(http_host)

    # home_url生成事件
    def genHomeUrl(self):
        homeUrl = self.webSetUI.homeUrlInput.text()
        self.webSetUI.showMainPageInput.setText(homeUrl)
        self.webSetUI.childTreeUrlInput.setText(homeUrl)
        self.webSetUI.loginUrlInput.setText(homeUrl)
        self.webSetUI.parentTreeUrlInput.setText(homeUrl)
        self.webSetUI.infoUrlInput.setText(homeUrl)

    # 初始化网页设置
    def initWebMsg(self):
        SERVER_HOST = self.settings.value("WEB/SERVER_HOST")
        HOME_URL = self.settings.value("WEB/HOME_URL")
        LOGIN_URL = self.settings.value("WEB/LOGIN_URL")
        LOGIN_USERNAME = self.settings.value("WEB/LOGIN_USERNAME")
        LOGIN_PASSWORD = self.settings.value("WEB/LOGIN_PASSWORD")
        PARENT_TREE_URL = self.settings.value("WEB/PARENT_TREE_URL")
        CHILD_TREE_URL = self.settings.value("WEB/CHILD_TREE_URL")
        QUERY_INFO_URL = self.settings.value("WEB/QUERY_INFO_URL")
        SHOW_MAIN_PAGE_URL = self.settings.value("WEB/SHOW_MAIN_PAGE_URL")
        self.webSetUI.hostInput.setText(SERVER_HOST)
        self.webSetUI.homeUrlInput.setText(HOME_URL)
        self.webSetUI.loginUrlInput.setText(LOGIN_URL)
        self.webSetUI.userInpput.setText(LOGIN_USERNAME)
        self.webSetUI.pwdInput.setText(LOGIN_PASSWORD)
        self.webSetUI.showMainPageInput.setText(SHOW_MAIN_PAGE_URL)
        self.webSetUI.parentTreeUrlInput.setText(PARENT_TREE_URL)
        self.webSetUI.childTreeUrlInput.setText(CHILD_TREE_URL)
        self.webSetUI.infoUrlInput.setText(QUERY_INFO_URL)

    # 保存网页设置
    def saveWebMsg(self):
        try:
            self.settings.setValue("WEB/SERVER_HOST", self.webSetUI.hostInput.text())
            self.settings.setValue("WEB/HOME_URL", self.webSetUI.homeUrlInput.text())
            self.settings.setValue("WEB/LOGIN_URL", self.webSetUI.loginUrlInput.text())
            self.settings.setValue("WEB/LOGIN_USERNAME", self.webSetUI.userInpput.text())
            self.settings.setValue("WEB/LOGIN_PASSWORD", self.webSetUI.pwdInput.text())
            self.settings.setValue("WEB/LOGIN_PASSWORD", self.webSetUI.pwdInput.text())
            self.settings.setValue("WEB/SHOW_MAIN_PAGE_URL", self.webSetUI.showMainPageInput.text())
            self.settings.setValue("WEB/PARENT_TREE_URL", self.webSetUI.parentTreeUrlInput.text())
            self.settings.setValue("WEB/CHILD_TREE_URL", self.webSetUI.childTreeUrlInput.text())
            self.settings.setValue("WEB/QUERY_INFO_URL", self.webSetUI.infoUrlInput.text())
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self.Dialog, "配置保存", e.__str__())
        self.Dialog.accept()  # 关闭界面

    # 密码可见绑定
    def pwd_visible_state_change(self):
        if self.webSetUI.pwdCheckBox.isChecked():
            self.webSetUI.pwdInput.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.webSetUI.pwdInput.setEchoMode(QtWidgets.QLineEdit.Password)

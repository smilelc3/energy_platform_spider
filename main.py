import os
import sys

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from src.display import Display
from ui import mainUI

if __name__ == '__main__':
    # 添加oracle client驱动环境变量(添加到首位，避免与已存在client冲突)
    os.environ['PATH'] = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'instantclient_19_3\\') + ';' + \
                         os.environ['PATH']
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'  # client使用utf-8编码

    # 高DPI
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)  # enable highdpi scaling
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)  # use highdpi icons

    app = QApplication(sys.argv)

    ui = mainUI.Ui_MainWindow()

    # 可以理解成将创建的 ui 绑定到新建的 mainWnd 上
    display = Display(ui)
    display.show()

    sys.exit(app.exec_())

import datetime
import math
import os
import sys
import time

from PyQt5 import QtWidgets, QtCore, QtSql, QtGui

from src import setting_build
from ui import about_pyqt5, about_proj, mainUI
from src.workerThread import StatusCheckThread, MainSpiderThread, AddNowThread, StatusMsg


class Display(QtWidgets.QMainWindow):
    statusCheckTimer = QtCore.QTimer()
    mainSpiderTimer = QtCore.QTimer()
    addNowTimer = QtCore.QTimer()

    def __init__(self, ui: mainUI.Ui_MainWindow):
        super().__init__()
        # 中文路径检测
        # 因为使用本地oracle client驱动，驱动路径最好不能包含非ASCII
        projFilePath = os.path.realpath(sys.argv[0])
        try:
            projFilePath.encode('ascii')
        except UnicodeEncodeError:
            QtWidgets.QMessageBox.critical(self, '严重错误', '因涉及调用该路径下Oracle客户端驱动，软件路径不能包含中文或其他非ASCII码字符，请切换路径')
            exit(0)

        self.ui = ui
        self.ui.setupUi(self)
        # 菜单绑定

        # 服务器参数配置初始化
        self.SevSet = setting_build.server()
        self.ui.server_setting.triggered.connect(self.SevSet.initSevMsg)  # 每次打开初始化参数
        self.ui.server_setting.triggered.connect(self.SevSet.Dialog.show)

        # 网页参数配置初始化
        self.webSet = setting_build.web()
        self.ui.web_setting.triggered.connect(self.webSet.initWebMsg)  # 每次打开初始化参数
        self.ui.web_setting.triggered.connect(self.webSet.Dialog.show)

        # 关于项目
        self.aboutProjDialog = QtWidgets.QDialog()
        self.aboutProjUI = about_proj.Ui_about_proj()
        self.aboutProjUI.setupUi(self.aboutProjDialog)
        self.ui.about_energy_platform_spider.triggered.connect(self.aboutProjDialog.show)

        # 关于pyqt5
        self.aboutPyQt5Dialog = QtWidgets.QDialog()
        self.aboutPyQt5UI = about_pyqt5.Ui_pyqt5_dialog()
        self.aboutPyQt5UI.setupUi(self.aboutPyQt5Dialog)
        self.ui.about_pyqt5.triggered.connect(self.aboutPyQt5Dialog.show)

        # 主界面初始化

        self.ui.progressBar.setHidden(True)
        self.spiderStatus = False  # 爬虫状态
        self.ui.startEndButton.clicked.connect(self.start_end_spider)

        self.settings = QtCore.QSettings("res/config.ini", QtCore.QSettings.IniFormat)
        self.settings.setIniCodec('UTF-8')  # 加载本地参数

        # 日期选择栏初始化
        self.ui.startTimeEdit.setCalendarPopup(True)
        self.ui.startTimeEdit.setDate(QtCore.QDate.currentDate())
        self.ui.endTimeEdit.setCalendarPopup(True)
        self.ui.endTimeEdit.setDate(QtCore.QDate.currentDate())
        self.ui.addTaskButton.clicked.connect(self.on_add_task_clicked)

        # 本地存储数据库初始化
        self.localDB = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.localDB.setDatabaseName('res/spiderView.db')
        self.localDB.open()
        if not self.localDB.isOpen():
            QtWidgets.QMessageBox.critical(self,
                                           '严重错误',
                                           '本地数据库启用失败，程序无法使用\n' + self.localDB.lastError().text()
                                           )
            exit(0)
        self.localDBModel = QtSql.QSqlQueryModel()
        self.on_change_page_clicked(pageNum=1)
        self.localDBModel.setHeaderData(0, QtCore.Qt.Horizontal, '')
        self.localDBModel.setHeaderData(1, QtCore.Qt.Horizontal, '任务名')
        self.localDBModel.setHeaderData(2, QtCore.Qt.Horizontal, '爬取时间')
        self.localDBModel.setHeaderData(3, QtCore.Qt.Horizontal, '状态')
        self.localDBModel.setHeaderData(4, QtCore.Qt.Horizontal, '有效数据/条')
        self.localDBModel.setHeaderData(5, QtCore.Qt.Horizontal, '入库')
        self.ui.spiderView.setModel(self.localDBModel)
        self.ui.spiderView.verticalHeader().setHidden(True)
        self.ui.spiderView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)  # 设置选择行为，以行为单位

        # Table 展示界面优化
        self.ui.spiderView.setColumnWidth(0, 55)
        self.ui.spiderView.setColumnWidth(1, 150)
        self.ui.spiderView.setColumnWidth(2, 155)
        self.ui.spiderView.setColumnWidth(3, 63)
        self.ui.spiderView.setColumnWidth(5, 50)

        # 日期选择限制
        self.ui.startTimeEdit.dateTimeChanged.connect(self.on_start_time_edit_change)
        self.ui.endTimeEdit.dateTimeChanged.connect(self.on_end_time_edit_change)

        # 翻页限制
        self.totalPageNum = self.get_total_num_page()
        self.pageNum = 1
        self.ui.totalPageLabel.setText('共' + str(self.totalPageNum) + '页')
        self.ui.numberPageInput.setText(str(self.pageNum))  # 当前第一页
        self.ui.nextPageButton.clicked.connect(lambda: self.on_change_page_clicked(pageNum=self.pageNum + 1))
        self.ui.prePageButton.clicked.connect(lambda: self.on_change_page_clicked(pageNum=self.pageNum - 1))
        self.ui.firstPageButton.clicked.connect(lambda: self.on_change_page_clicked(pageNum=1))
        self.ui.lastPageButton.clicked.connect(lambda: self.on_change_page_clicked(pageNum=self.totalPageNum))
        self.ui.numberPageInput.setValidator(QtGui.QIntValidator())
        self.ui.goPageButton.clicked.connect(
            lambda: self.on_change_page_clicked(pageNum=int(self.ui.numberPageInput.text())))
        self.page_num_check()

        # 任务线程初始化
        self.statusCheckThread = StatusCheckThread(settings=self.settings)
        # 状态检测四个信号连接到同一个槽
        self.statusCheckThread.dbCheck[StatusMsg].connect(self.on_check_status)
        self.statusCheckThread.webCheck[StatusMsg].connect(self.on_check_status)
        self.statusCheckThread.spiderLoginCheck[StatusMsg].connect(self.on_check_status)
        self.statusCheckThread.spiderDataCheck[StatusMsg].connect(self.on_check_status)

        self.mainSpiderThread = MainSpiderThread(settings=self.settings, localDB=self.localDB)
        self.mainSpiderThread.oneFinished.connect(lambda: self.on_change_page_clicked(pageNum=self.pageNum))

        self.statusCheckThread.cookiesUpdated.connect(self.mainSpiderThread.setCookies)  # cookies 更新信号与槽

        self.addNowThread = AddNowThread(localDB=self.localDB)
        self.addNowThread.addFinished.connect(lambda: self.on_change_page_clicked(pageNum=self.pageNum))

        self.statusCheckTimer.timeout.connect(self.statusCheckThread.start)
        self.mainSpiderTimer.timeout.connect(self.mainSpiderThread.start)
        self.addNowTimer.timeout.connect(self.addNowThread.start)

    # 翻页限制检查
    def page_num_check(self):
        '''
        当前页数=1  上一页/首页无效
        当前页数=最大页数，下一页/末页无效
        '''
        self.ui.prePageButton.setEnabled(False if self.pageNum is 1 else True)
        self.ui.firstPageButton.setEnabled(False if self.pageNum is 1 else True)
        self.ui.nextPageButton.setEnabled(False if self.pageNum == self.totalPageNum else True)
        self.ui.lastPageButton.setEnabled(False if self.pageNum == self.totalPageNum else True)

    # 页面翻页刷新绑定（带页面参数）
    def on_change_page_clicked(self, pageNum, showMsg=True):
        self.totalPageNum = self.get_total_num_page()
        self.ui.totalPageLabel.setText('共' + str(self.totalPageNum) + '页')
        if pageNum > self.totalPageNum:
            if showMsg:
                QtWidgets.QMessageBox.warning(self, '数据格式错误', f'当前最多{self.totalPageNum}页,无法翻页至{pageNum}页')
            pageNum = self.totalPageNum

        elif pageNum < 1:
            QtWidgets.QMessageBox.warning(self, '数据格式错误', f'页数不能小于1')
            pageNum = 1

        self.pageNum = pageNum
        self.ui.numberPageInput.setText(str(self.pageNum))
        querySql = 'SELECT  (select count(*) from MDB_ENERGY_COLLECT_LOCAL as T2  where T1.TASK_NAME <= T2.TASK_NAME) as ROW_NUM, * ' \
                   'FROM MDB_ENERGY_COLLECT_LOCAL as T1 ' \
                   'ORDER BY TASK_NAME DESC ' \
                   'LIMIT 500 ' \
                   f'OFFSET {(self.pageNum - 1) * 500}'
        self.localDBModel.setQuery(querySql)
        while self.localDBModel.canFetchMore():
            self.localDBModel.fetchMore()
        self.page_num_check()

    # 获取最大页数
    def get_total_num_page(self) -> int:
        totalPageNumQuery = QtSql.QSqlQuery(query="SELECT count(*) FROM MDB_ENERGY_COLLECT_LOCAL", db=self.localDB)
        totalPageNumQuery.next()
        return int(math.ceil(int(totalPageNumQuery.value(0)) / 500))

    # 开始时间限制
    def on_start_time_edit_change(self):
        '''
        1. 分钟数必须15分钟的整数
        2. 开始时间不能晚于结束时间
        3. 开始时间不能晚于当前时间最最近15分钟的时间 - 15min  (-15min是需要等待一定时间数据生效)
        '''
        startDateTime = self.ui.startTimeEdit.dateTime()
        datetimeNow15 = datetime.datetime.now()
        datetimeNow15 = datetimeNow15 - datetime.timedelta(
            minutes=datetimeNow15.minute % 15 + 15,
            seconds=datetimeNow15.second,
            microseconds=datetimeNow15.microsecond
        )
        if startDateTime.time().minute() not in (0, 15, 30, 45):
            QtWidgets.QMessageBox.warning(self,
                                          '配置错误',
                                          '开始时间中分钟数值必须为15倍数（0、15、30、45）'
                                          )
            self.ui.startTimeEdit.setTime(startDateTime.time().addSecs(0 - 60 * startDateTime.time().minute()))  # 分钟数归零

        elif startDateTime.toPyDateTime() > self.ui.endTimeEdit.dateTime().toPyDateTime():
            QtWidgets.QMessageBox.warning(self,
                                          '配置错误',
                                          '开始时间不能晚于结束时间'
                                          )
            self.ui.startTimeEdit.setDateTime(self.ui.endTimeEdit.dateTime())  # 输入错误

        elif startDateTime.toPyDateTime() > datetimeNow15:
            QtWidgets.QMessageBox.warning(self,
                                          '配置错误',
                                          '开始时间不能晚于%s' % (
                                              datetimeNow15.strftime("%Y/%m/%d %H:%M")) + '\n(当前时间最最近15分钟的时间 - 15min)'
                                          )
            self.ui.startTimeEdit.setDateTime(datetimeNow15)

    # 结束时间限制
    def on_end_time_edit_change(self):
        '''
        1. 分钟数必须15分钟的整数
        2. 结束时间不能早于开始时间
        3. 结束时间不能早于当前时间最最近15分钟的时间 - 15min  (-15min是结束时需要多15min等待数据)
        '''
        endDateTime = self.ui.endTimeEdit.dateTime()
        datetimeNow15 = datetime.datetime.now()
        datetimeNow15 = datetimeNow15 - datetime.timedelta(
            minutes=datetimeNow15.minute % 15 + 15,
            seconds=datetimeNow15.second,
            microseconds=datetimeNow15.microsecond
        )

        if endDateTime.time().minute() not in (0, 15, 30, 45):
            QtWidgets.QMessageBox.warning(self,
                                          '配置错误',
                                          '结束时间中分钟数值必须为15倍数（0、15、30、45）'
                                          )
            self.ui.startTimeEdit.setTime(endDateTime.time().addSecs(0 - 60 * endDateTime.time().minute()))  # 分钟数归零

        elif endDateTime.toPyDateTime() < self.ui.startTimeEdit.dateTime().toPyDateTime():
            QtWidgets.QMessageBox.warning(self,
                                          '配置错误',
                                          '结束时间不能早于开始时间'
                                          )
            self.ui.endTimeEdit.setDateTime(self.ui.startTimeEdit.dateTime())  # 输入错误
        elif endDateTime.toPyDateTime() > datetimeNow15:
            QtWidgets.QMessageBox.warning(self,
                                          '配置错误',
                                          '结束时间不能晚于%s' % (
                                              datetimeNow15.strftime("%Y-%m-%d %H:%M")) + '\n(当前时间最最近15分钟的时间 - 15min)'
                                          )
            self.ui.endTimeEdit.setDateTime(datetimeNow15)

    # 添加任务响应
    def on_add_task_clicked(self):
        '''
        直接和本地数据库对接，添加任务，无需检测数据数据格式正确，因为已被修正
        '''
        startTime = self.ui.startTimeEdit.dateTime().toPyDateTime()
        endTime = self.ui.endTimeEdit.dateTime().toPyDateTime()
        taskNum = 0
        insertSql = QtSql.QSqlQuery(db=self.localDB)
        self.localDB.transaction()  # 开启事务 加快插入速度
        while startTime <= endTime:
            sql = "REPLACE INTO " + \
                  "MDB_ENERGY_COLLECT_LOCAL(TASK_NAME, SPIDER_TIME, STATUS, DATA_NUM, STORAGE_IN_DB)" + \
                  f"VALUES ('{startTime.strftime('%Y-%m-%d %H:%M')} - {(startTime + datetime.timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M')}', null, '待获取', null, null)"
            insertSql.exec(sql)
            startTime = startTime + datetime.timedelta(minutes=15)  # 时间累加
            taskNum += 1
        # 提示信息
        self.localDB.commit()
        QtWidgets.QMessageBox.information(
            self,
            '数据修改',
            f'成功插入{taskNum}条任务'
        )
        self.on_change_page_clicked(pageNum=self.pageNum)

    # 键盘检测事件
    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == QtCore.Qt.Key_Delete or a0.key() == QtCore.Qt.Key_Backspace:
            self.del_select_task()  # 删除任务

    # 删除选中任务
    def del_select_task(self):
        selRows = self.ui.spiderView.selectionModel().selectedRows()
        # 判断是否有选中
        if selRows:
            isOK = QtWidgets.QMessageBox.question(
                self,
                '删除任务',
                f'是否删除选中的{len(selRows)}行任务？',
                QtWidgets.QMessageBox.Yes,
                QtWidgets.QMessageBox.No
            )
            if isOK == QtWidgets.QMessageBox.Yes:
                self.localDB.transaction()
                deleteSqlQuery = QtSql.QSqlQuery(db=self.localDB)
                for row in selRows:
                    data = self.localDBModel.record(row.data(0) - (self.pageNum - 1) * 500 - 1)
                    taskName = data.value(1)
                    deleteSql = f"DELETE FROM MDB_ENERGY_COLLECT_LOCAL WHERE TASK_NAME = '{taskName}'"
                    deleteSqlQuery.exec(deleteSql)
                self.localDB.commit()
        # 刷新页面
        self.on_change_page_clicked(pageNum=self.pageNum, showMsg=False)

    # 爬虫启动停止逻辑
    def start_end_spider(self):
        if self.spiderStatus is False:
            self.start_spider()
        else:
            self.cancel_spider()

    # 启动爬虫
    def start_spider(self):
        self.ui.startEndButton.setHidden(True)
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setHidden(False)
        self.ui.server_setting.setEnabled(False)
        self.ui.web_setting.setEnabled(False)
        self.ui.proxy_setting.setEnabled(False)
        self.statusCheckThread.start()
        self.mainSpiderThread.start()
        self.addNowThread.start()
        # 开始计时
        self.statusCheckTimer.start(9 * 10 * 1000)  # 定时任务，以秒为单位
        self.mainSpiderTimer.start(3 * 60 * 1000)  # 定时任务，以秒为单位
        self.addNowTimer.start(6 * 60 * 1000)  # 定时任务，以秒为单位
        self.spiderStatus = True

    # 连通信号检测触发函数
    def on_check_status(self, statusMsg: StatusMsg):
        if statusMsg.type == 'dbCheck':
            for progressBar_v in range(25):
                self.ui.progressBar.setValue(progressBar_v)
                time.sleep(0.01)
            if statusMsg.status:
                self.ui.dbStatusLED.setStyleSheet("image:url(:/proPrefix/image/led_correct.png)")
            else:
                self.ui.dbStatusLED.setStyleSheet("image:url(:/proPrefix/image/led_error.png)")

        elif statusMsg.type == 'webCheck':
            for progressBar_v in range(25, 50):
                self.ui.progressBar.setValue(progressBar_v)
                time.sleep(0.01)
            if statusMsg.status:
                self.ui.webStatusLED.setStyleSheet("image:url(:/proPrefix/image/led_correct.png)")
            else:
                self.ui.webStatusLED.setStyleSheet("image:url(:/proPrefix/image/led_error.png)")

        elif statusMsg.type == 'loginCheck':
            for progressBar_v in range(50, 75):
                self.ui.progressBar.setValue(progressBar_v)
                time.sleep(0.01)
            if statusMsg.status:
                self.ui.loginStatusLED.setStyleSheet("image:url(:/proPrefix/image/led_correct.png)")
            else:
                self.ui.loginStatusLED.setStyleSheet("image:url(:/proPrefix/image/led_error.png)")

        elif statusMsg.type == 'dataCheck':
            for progressBar_v in range(75, 101):
                self.ui.progressBar.setValue(progressBar_v)
                time.sleep(0.01)
            if statusMsg.status:
                self.ui.dataStatusLED.setStyleSheet("image:url(:/proPrefix/image/led_correct.png)")
            else:
                self.ui.dataStatusLED.setStyleSheet("image:url(:/proPrefix/image/led_error.png)")

            # 最后执行显示任务
            self.ui.startEndButton.setHidden(False)
            self.ui.startEndButton.setText('停止爬虫')
            self.ui.progressBar.setValue(0)
            self.ui.progressBar.setHidden(True)
            self.ui.server_setting.setEnabled(True)
            self.ui.web_setting.setEnabled(True)
            self.ui.proxy_setting.setEnabled(True)
            self.ui.addTaskButton.setEnabled(True)

        if not statusMsg.status:  # 检测到错误，自动关闭
            autoCloseDelayS = 5
            infoBox = QtWidgets.QMessageBox()
            infoBox.setIcon(QtWidgets.QMessageBox.Critical)
            infoBox.setWindowTitle(statusMsg.title)
            infoBox.setText(statusMsg.msg + f'\n {autoCloseDelayS}秒后，自动关闭')
            infoBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            infoBox.button(QtWidgets.QMessageBox.Ok).animateClick(autoCloseDelayS * 1000)  # 3秒自动关闭
            infoBox.exec_()

    # 取消启动任务
    def cancel_spider(self):
        self.ui.startEndButton.setHidden(False)
        self.ui.startEndButton.setText('启动爬虫')
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setHidden(True)
        self.ui.server_setting.setEnabled(True)
        self.ui.web_setting.setEnabled(True)
        self.ui.proxy_setting.setEnabled(True)
        self.ui.addTaskButton.setEnabled(False)
        self.ui.dbStatusLED.setStyleSheet("image:url(:/proPrefix/image/led_unknow.png)")
        self.ui.webStatusLED.setStyleSheet("image:url(:/proPrefix/image/led_unknow.png)")
        self.ui.loginStatusLED.setStyleSheet("image:url(:/proPrefix/image/led_unknow.png)")
        self.ui.dataStatusLED.setStyleSheet("image:url(:/proPrefix/image/led_unknow.png)")
        self.statusCheckTimer.stop()
        self.mainSpiderTimer.stop()
        self.addNowTimer.stop()
        self.statusCheckThread.quit()
        self.mainSpiderThread.quit()
        self.addNowThread.quit()
        self.spiderStatus = False

import copy
import datetime
import logging

import cx_Oracle as oracle
from PyQt5 import QtCore, QtSql
from requests.cookies import RequestsCookieJar

from src import spider_func

# logging 记录
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='res/running.log',
                    filemode='a')


# 状态记录类
class StatusMsg(object):
    status = False
    type = ''
    title = ''
    msg = ''


# 线程 AddNowThread: 每15分钟向数据库加入新需要爬取的数据
class AddNowThread(QtCore.QThread):
    addFinished = QtCore.pyqtSignal()

    def __init__(self, localDB):
        super(AddNowThread, self).__init__()
        self.localDB = localDB

    def run(self):
        logging.debug('run AddNowThread')
        # 获取到当前的时间节点，并判断是否在数据库中
        datetimeNow15 = datetime.datetime.now()
        datetimeNow15 = datetimeNow15 - datetime.timedelta(
            minutes=datetimeNow15.minute % 15 + 15,
            seconds=datetimeNow15.second,
            microseconds=datetimeNow15.microsecond
        )
        sqlQuery = QtSql.QSqlQuery(db=self.localDB)
        selectSql = f"SELECT * FROM MDB_ENERGY_COLLECT_LOCAL " \
                    f"WHERE START_TIME='{datetimeNow15.strftime('%Y-%m-%d %H:%M')}' AND  END_TIME='{(datetimeNow15 + datetime.timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M')}' " \
                    f"AND DATA_NUM"
        sqlQuery.exec(selectSql)
        if not sqlQuery.next():  # 保证无
            insertSql = "REPLACE INTO " \
                        "MDB_ENERGY_COLLECT_LOCAL(START_TIME, END_TIME, SPIDER_TIME, STATUS, DATA_NUM, STORAGE_IN_DB) " \
                        f"VALUES ('{datetimeNow15.strftime('%Y-%m-%d %H:%M')}',  '{(datetimeNow15 + datetime.timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M')}', null, '待获取', null, null)"
            sqlQuery.exec(insertSql)
            logging.debug('已插入新任务数据：' + datetimeNow15.strftime('%Y-%m-%d %H:%M'))
            self.addFinished.emit()
        else:
            logging.debug('数据库已有有效数据：' + datetimeNow15.strftime('%Y-%m-%d %H:%M'))
            pass


# 线程 StatusCheckThread：每?分钟检测所有状态连通性通信

class StatusCheckThread(QtCore.QThread):
    # 四个状态检测信号槽
    dbCheck = QtCore.pyqtSignal(StatusMsg)
    webCheck = QtCore.pyqtSignal(StatusMsg)
    spiderLoginCheck = QtCore.pyqtSignal(StatusMsg)
    spiderDataCheck = QtCore.pyqtSignal(StatusMsg)

    # 状态记录list
    statusMsg = StatusMsg()
    cookies = RequestsCookieJar()
    cookiesUpdated = QtCore.pyqtSignal(RequestsCookieJar)

    def __init__(self, settings: QtCore.QSettings):
        super(StatusCheckThread, self).__init__()  # 父类构造函数
        self.settings = settings  # 必须带配置参数构造

    def run(self):
        logging.debug('StatusCheckThread')
        # 第一步连接数据库
        self.statusMsg.type = 'dbCheck'
        try:
            oracle.connect(
                self.settings.value("ORACLE/SQL_DATABASE_NAME"),
                self.settings.value("ORACLE/SQL_DATABASE_PASSWORD"),
                f'{self.settings.value("ORACLE/SQL_SERVER_HOST")}:{self.settings.value("ORACLE/SQL_SERVER_PORT")}/{self.settings.value("ORACLE/SQL_DATABASE_SID")}')
        except oracle.DatabaseError as e:
            self.statusMsg.status = False
            if e.args[0].code == 1017:
                self.statusMsg.title = '数据库连接错误'
                self.statusMsg.msg = '无效的用户名/密码'
            else:
                self.statusMsg.title = '数据库连接错误'
                self.statusMsg.msg = e.__str__()
                logging.error('数据库未知错误：' + e.__str__())
        else:
            self.statusMsg.status = True
        self.dbCheck.emit(copy.deepcopy(self.statusMsg))  # 运行完成后，发射信号

        # 第二步获取cookies
        self.statusMsg.type = 'webCheck'
        try:
            login_header = spider_func.get_login_header(self.settings.value('WEB/SERVER_HOST'))
            self.cookies = spider_func.get_init_cookies(self.settings.value('WEB/HOME_URL'), login_header)
            if self.cookies:
                self.statusMsg.status = True

                self.cookiesUpdated.emit(copy.deepcopy(self.cookies))
            else:
                self.statusMsg.status = False
                self.statusMsg.title = '网络错误'
                self.statusMsg.msg = '网页不可达，请检查网络连接或确认URL地址状态' + self.settings.value('WEB/HOME_URL')
        except Exception as e:
            self.statusMsg.status = False
            self.statusMsg.title = '未知错误'
            logging.error('web未知错误：' + e.__str__())
            self.statusMsg.msg = e.__str__()
        self.webCheck.emit(copy.deepcopy(self.statusMsg))

        # 第三步获取用户登陆状态，尝试登陆
        self.statusMsg.type = 'loginCheck'
        try:
            responseJson = spider_func.login_as_admin(
                url=self.settings.value('WEB/LOGIN_URL'),
                cookies=self.cookies,
                login_header=spider_func.get_login_header(self.settings.value('WEB/SERVER_HOST')),
                user=self.settings.value('WEB/LOGIN_USERNAME'),
                password=self.settings.value('WEB/LOGIN_PASSWORD')
            )
            if responseJson['errorCode'] is 4:
                # 登陆成功
                self.statusMsg.status = True
            else:
                self.statusMsg.status = False
                if responseJson['errorCode'] is 1:
                    self.statusMsg.title = '账号错误'
                    self.statusMsg.msg = '账号密码输入错误'
                elif responseJson['errorCode'] is 2:
                    self.statusMsg.title = '账号错误'
                    self.statusMsg.msg = '账号被锁定，请联系平台管理员'
                elif responseJson['errorCode'] is 3:
                    self.statusMsg.title = '账号错误'
                    self.statusMsg.msg = '账号被禁用或删除'
                elif responseJson['errorCode'] is 10000:
                    self.statusMsg.title = '账号错误'
                    self.statusMsg.msg = '验证码错误，请稍后重试'
                else:
                    self.statusMsg.title = '登录错误'
                    self.statusMsg.msg = '状态码：' + str(responseJson['errorCode'])
        except Exception as e:
            self.statusMsg.title = '登录错误'
            self.statusMsg.status = False
            self.statusMsg.msg = e.__str__()
            logging.error('登录未知错误：' + e.__str__())
        self.spiderLoginCheck.emit(copy.deepcopy(self.statusMsg))

        # 第四步 获取目录
        self.statusMsg.type = 'dataCheck'
        try:
            result = spider_func.update_tree_info(
                parentTree_URL=self.settings.value('WEB/PARENT_TREE_URL'),
                showMainPage_URL=self.settings.value('WEB/SHOW_MAIN_PAGE_URL'),
                childTree_URL=self.settings.value('WEB/CHILD_TREE_URL'),
                cookies=self.cookies
            )
            # 数据连接成功
            self.statusMsg.status = True
        except Exception as e:
            self.statusMsg.status = False
            self.statusMsg.title = '网页错误'
            self.statusMsg.msg = e.__str__()
            logging.error('目录未知错误：' + e.__str__())
        self.spiderDataCheck.emit(copy.deepcopy(self.statusMsg))


# 线程 MainSpiderThread：在连接畅通的前提下，每n秒检测数据库需要爬取的数据，并爬取，爬取成功后，写入本地数据库
class MainSpiderThread(QtCore.QThread):
    oneFinished = QtCore.pyqtSignal()
    cookies = None

    def __init__(self, settings: QtCore.QSettings, localDB: QtSql.QSqlDatabase):
        super(MainSpiderThread, self).__init__()
        self.settings = settings
        self.localDB = localDB

    def setCookies(self, cookies):
        self.cookies = cookies

    def run(self):
        logging.debug('MainSpiderThread')
        try:
            self.oracle = oracle.connect(
                self.settings.value('ORACLE/SQL_DATABASE_NAME'), self.settings.value('ORACLE/SQL_DATABASE_PASSWORD'),
                f"{self.settings.value('ORACLE/SQL_SERVER_HOST')}:{self.settings.value('ORACLE/SQL_SERVER_PORT')}/{self.settings.value('ORACLE/SQL_DATABASE_SID')}"
            )
        except oracle.DatabaseError as e:
            self.oracle = None
            logging.critical('爬取线程数据库错误：' + e.__str__())
        else:
            sqlQuery = QtSql.QSqlQuery(db=self.localDB)
            sqlInsert = QtSql.QSqlQuery(db=self.localDB)
            sql = "SELECT START_TIME, END_TIME FROM MDB_ENERGY_COLLECT_LOCAL " \
                  "WHERE STATUS='待获取' " \
                  "ORDER BY START_TIME || ' - ' || END_TIME"
            sqlQuery.exec(sql)
            while not self.cookies and self.oracle:  # cookies 不存在时，线程sleep
                self.wait(5)
            while sqlQuery.next():
                startTime, endTime = sqlQuery.value(0), sqlQuery.value(1)
                logging.debug(f'正在爬取: {startTime} - {endTime}   cookies: {self.cookies}')
                try:
                    totUsefulNum = 0
                    node_list = spider_func.update_tree_info(
                        parentTree_URL=self.settings.value('WEB/PARENT_TREE_URL'),
                        cookies=self.cookies,
                        showMainPage_URL=self.settings.value('WEB/SHOW_MAIN_PAGE_URL'),
                        childTree_URL=self.settings.value('WEB/CHILD_TREE_URL')
                    )
                    logging.debug(node_list)
                    for node in node_list:
                        node_info = spider_func.query_indication_info(
                            query_info_url=self.settings.value('WEB/QUERY_INFO_URL'),
                            cookies=self.cookies,
                            begin_time=startTime,
                            end_time=endTime,
                            id=node['id'],
                            name=node['name']
                        )
                        totUsefulNum += spider_func.insert_or_update_many(self.oracle,
                                                                          data=node_info['tbData']['total1'],
                                                                          startTime=startTime)
                except Exception as e:
                    logging.error('爬取错误：' + e.__str__())


                else:  # 更新完毕
                    insertSql = "REPLACE INTO " \
                                "MDB_ENERGY_COLLECT_LOCAL(START_TIME, END_TIME, SPIDER_TIME, STATUS, DATA_NUM, STORAGE_IN_DB) " \
                                f"VALUES ('{startTime}', '{endTime}', '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}', '已获取', {totUsefulNum}, '是')"
                    sqlInsert.exec(insertSql)
                    self.oneFinished.emit()
                self.sleep(5)  # 避免高频访问被封

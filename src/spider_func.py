# coding = utf-8

import datetime
import hashlib
import json
import time
from urllib.parse import quote, urlencode

import requests

spider_header = {
    'Accept': 'text/plain, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}


# 获取所有根节点信息
def _get_parent_tree(url, cookies, showMainPage_URL) -> dict:
    spider_header_cookie = spider_header
    # 必须加入Referer信息才能正确获取到信息，不要问为什么，呵呵
    spider_header_cookie['Referer'] = showMainPage_URL
    spider_header_cookie['Content-Type'] = 'application/x-www-form-urlencoded'
    # print(spider_header_cookie)
    params = {
        'isEleTopo': 'false',
    }
    response = requests.post(url, headers=spider_header_cookie, params=params, cookies=cookies,
                             proxies=({ }))  # TODO 加入代理
    response_json = json.loads(response.text)
    return response_json


# 获取父节点下子节点信息
def _get_child_tree(url, cookies, parent_id) -> dict:
    spider_header_cookie = spider_header
    spider_header_cookie['Content-Type'] = 'application/x-www-form-urlencoded'
    params = {
        'parentLedgerId': parent_id,  # 添加u父节点Id
    }
    response = requests.post(url, headers=spider_header_cookie, params=params, cookies=cookies,
                             proxies=({ }))  # TODO 加入代理
    response_json = json.loads(response.text)
    return response_json


# 获取总结点信息(管理者)
def update_tree_info(parentTree_URL, cookies, showMainPage_URL, childTree_URL) -> list:
    result = []
    parent_tree = _get_parent_tree(parentTree_URL, cookies, showMainPage_URL)
    for parent in parent_tree:  # 获取每个根节点信息
        # print(parent)
        sub_parent_tree = _get_child_tree(childTree_URL, cookies, parent['id'])
        # print(parent['name'])
        for sub_parent in sub_parent_tree:  # 获取第二节点信息
            result.append({ 'name': sub_parent['name'], 'id': sub_parent['id'] })
            # print('\t', sub_parent['name'])

            # child_tree = _get_child_tree(childTree_URL, cookies, sub_parent['id'])      # 获取第三子节点信息
            # for child in child_tree:
            #     print('\t\t', child['name'])
    return result


# 将str格式化时间转换成以秒为单位的float
def strptime_to_second(str_time, format='%Y-%m-%d %H:%M'):
    return time.mktime(time.strptime(str_time, format))


# 获取节点数据
def query_indication_info(query_info_url, cookies, begin_time: str, end_time: str, id, name):
    param_info = {
        "beginTime": begin_time + ':00',  # 加上秒数
        "endTime": end_time + ':00',
        "id": id,
        'type': '1',
        'beweenDays': str((strptime_to_second(end_time) - strptime_to_second(begin_time)) / (24 * 60 * 60)),  # 计算时间间隔
        'name': quote(name),
        'sourceType': '2',  # 管理者
        'dataTypes': [1],
    }
    form_data = {
        'paramInfo': json.dumps(param_info)  # 二次url编码，网页编码十分混乱
    }
    spider_header_cookie = spider_header
    spider_header_cookie['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
    response = requests.post(query_info_url, headers=spider_header_cookie, data=form_data, cookies=cookies,
                             proxies=({ }))  # TODO 加入代理

    return json.loads(response.text)


def get_login_header(SERVER_HOST) -> dict:
    # 用于伪造登录cookies的首次header
    login_header = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Host': SERVER_HOST,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }
    return login_header


# 获取初始化的cookies 以便伪造用户长期在线
def get_init_cookies(HOME_URL: str, login_header):
    session = requests.session()
    cookiesGet = session.get(url=HOME_URL, headers=login_header, proxies=({ }))  # TODO 加入代理
    if cookiesGet.status_code == 200:
        return cookiesGet.cookies
    else:
        return None


# 以管理员身份模拟登录
def login_as_admin(url, user, password, cookies, login_header):
    crypto_pwd = crypto_sha256(password)
    # 伪造提交数据
    formData = {
        'username': user,
        'password': crypto_pwd,  # 密码加密
        'roleType': '2',  # 以管理员登录
        'code': '',
        'loginPath': 'login',
        'display': 'none'
    }
    urlencode_formData = urlencode(formData)
    urlencode_formData = urlencode_formData.replace(quote(user), user)
    # user必须使用非url编码，原因未知
    # 重新构建header
    login_header_cookies = login_header
    login_header_cookies['Content-Length'] = str(len(urlencode_formData.encode('utf-8')))
    login_header_cookies['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    login_header_cookies['X-Requested-With'] = 'XMLHttpRequest'  # 伪造Ajax异步请求

    response = requests.post(url=url, data=urlencode_formData.encode('utf-8'), cookies=cookies,
                             headers=login_header_cookies, proxies=({ }))  # 加入代理
    responseJson = json.loads(response.text)
    # if response_json['errorCode'] is 1:
    #     print('输入有误')
    # if response_json['errorCode'] is 2:
    #     print('账户被锁定')
    # if response_json['errorCode'] is 3:
    #     print('被禁用或则删除')
    # if response_json['errorCode'] is 10000:
    #     print('验证码错误')
    # if response_json['errorCode'] is 4:
    #     print('登陆成功')
    return responseJson


# 密码经过哈希/散列加密，加密方式为 SHA256
def crypto_sha256(plaintext: str):
    hash_256 = hashlib.sha256()
    hash_256.update(plaintext.encode('utf-8'))
    cryptogram = hash_256.hexdigest()
    return cryptogram


# 更新登录信息
def update_user_cookies(HOME_URL, LOGIN_URL, LOGIN_USERNAME, LOGIN_PASSWORD, login_header):
    # 获取cookies
    cookies = get_init_cookies(HOME_URL, login_header)
    # print(cookies.get('JSESSIONID'))

    # 自动登录获取user_code
    user_code = login_as_admin(LOGIN_URL, LOGIN_USERNAME, LOGIN_PASSWORD, cookies, login_header)
    # print(f'user_code = {user_code}')
    return cookies


# 插入 与 更新 多条 数据
def insert_or_update_many(db, data: list, startTime: str) -> int:
    usefulNum = 0
    startTime = datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M')
    cr = db.cursor()
    for item in data:
        name, value, times = item['meterName'], item['ratestart_new'], item['ptct']
        if value is not None:  # 值非空
            usefulNum += 1
            insertOrUpdateSql = \
                "MERGE INTO MDB_ENERGY_COLLECT " \
                "USING DUAL " \
                "ON ( NAME=:name AND TIME =:time ) " \
                "WHEN MATCHED THEN " \
                "UPDATE SET VALUE =:value " \
                "WHEN NOT MATCHED THEN " \
                "INSERT (NAME, VALUE, TIME) VALUES(:name, :value, :time)"
            cr.execute(insertOrUpdateSql, { 'name': name, 'value': float(value) * int(times), 'time': startTime })
    cr.close()
    db.commit()
    return usefulNum

import requests
from pswd_encrypt import encryptAES
from lxml import etree
from time import time as getTime
from requests.packages import urllib3
from log_setting import logger
from requests.exceptions import ConnectTimeout,Timeout

urllib3.disable_warnings()

class WJC:
    def __init__(self, account, pswd):
        self.headers = {
            #'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 (4714622976) cpdaily/9.4.0  wisedu/9.4.0'
            'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1'
        }

        self.account = account
        self.pswd = pswd

        self.s = requests.session()
        self.s.verify = False

        self.__login_form = {
            'salt': '',
            'cap': '',
            'execution': ''
        }
        self.__loginInfoGet()

    def __pswdGen(self, pswd=None, salt=None):
        # return self.__js.call('app.encryptAES', pswd, salt)
        pswd = pswd if pswd else self.pswd
        salt = salt if salt else self.__login_form.get('salt')
        return encryptAES(pswd, salt)

    def __timeGen(self) -> str:
        return str(getTime()).replace('.','')[:13]


    def __isNeedCap(self):
        pass

    def __loginInfoGet(self):
        try:
            res = self.s.get('https://ids.uwh.edu.cn/authserver/login?service=https://ehall.uwh.edu.cn/login', headers=self.headers,timeout=45)
        except ConnectTimeout or Timeout:
            logger.error('请求登录信息超时')
            return {'code':'fail','msg':'请求登录息超时'}
        
        if res.status_code == 200:
            html = etree.HTML(res.text)
            try:
                self.__login_form.update({
                    'salt': html.xpath('//input[@id="pwdEncryptSalt"][1]/@value')[0],
                    'execution': html.xpath('//input[@id="execution"][1]/@value')[0]
                })
                msg = {'code': 'ok', 'msg': '成功获取加密参数', 'info': {}}
                logger.info(f"[{msg['code']}] {msg['msg']}")
                return msg
            except Exception as e:
                msg = {'code': 'error', 'msg': '尝试获取加密参数出现错误，错误信息会被保存于info中', 'info': {'msg': e}}
                logger.error(f"[{msg['code']}] {msg['msg']}\n{msg['info']['msg']}")
                return msg
        else:
            msg = {'code': 'fail', 'msg': '请求登录界面失败，具体信息将会被保存在info中',
                    'info': {'code': res.status_code, 'content': res.text}}
            logger.error(f"[{msg['code']}] {msg['msg']}\n{msg['info']['code']}\n{msg['info']['content']}")
            return msg

    def login(self):
        logger.info(f"开始登录账号{self.account}")
        if not self.account or not self.pswd:
            msg = {'code': 'fail', 'msg': '账号或密码不能为空', 'info': {}}
            logger.error(f"[{msg['code']}] {msg['msg']}")
            return msg
        if not self.__login_form.get('salt') or not self.__login_form.get('execution'):
            msg = {'code': 'fail', 'msg': '无加密参数', 'info': {}}
            logger.error(f"[{msg['code']}] {msg['msg']}")
            return msg

        data_form = {
            'username': self.account,
            'password': self.__pswdGen(self.pswd, self.__login_form['salt']),
            'captcha': '',
            '_eventId': 'submit',
            'cllt': 'userNameLogin',
            'dllt': 'generalLogin',
            'lt': '',
            'execution': self.__login_form['execution']
        }
     

        headers = {
            'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
        }
        try:
            res = self.s.post('https://ids.uwh.edu.cn/authserver/login?service=https://ehall.uwh.edu.cn/login',headers=headers,data=data_form,verify=False,timeout=45)
            res_cas = self.s.post('https://ehall.uwh.edu.cn/student/cas',timeout=45)
        except ConnectTimeout or Timeout:
            logger.error('请求登录超时')
            return {'code':'fail','msg':'请求登录超时'}
        
        cookie = ''
        for k,v in self.s.cookies.get_dict().items():
            cookie += k+'='+v+';'
        msg = {'code':'ok','msg':f'({self.account})获取Cookies','info':{}}  # 不代表登录成功
        logger.info(f"[{msg['code']}] {msg['msg']}")
        return msg
    
    def getSignTask(self):
        api = 'https://ehall.uwh.edu.cn/student/content/tabledata/student/sign/stu/sign'
        params_load = {
            "bSortable_0": "false",
            "bSortable_1": "true",
            "iSortingCols": "1",
            "iDisplayStart": "0",
            "iDisplayLength": "12",
            "iSortCol_0": "3",
            "sSortDir_0": "desc",
            "_t_s_": self.__timeGen()
        }
        try:
            res = self.s.get(api, params=params_load,timeout=45)
        except ConnectTimeout or Timeout:
            logger.error('请求签到信息超时')
            return {'code':'fail','msg':'请求签到息超时'}
        
        if res.status_code == 200:
            try:
                msg = {'code': 'ok', 'msg': '成功获取签到任务', 'info': res.json()}
                logger.info(f"[{msg['code']}] {msg['msg']}")
                return msg
            except requests.exceptions.JSONDecodeError:
                msg = {'code': 'fail', 'msg': '获取签到任务失败', 'info': {'code': res.status_code, 'content': res.text}}
                logger.error(f"[{msg['code']}] {msg['msg']}\n{msg['info']}")
                return msg
        else:
            msg = {'code': 'fail', 'msg': '获取签到任务失败', 'info': {'code': res.status_code, 'content': res.text}}
            logger.error(f"[{msg['code']}] {msg['msg']}\n{msg['info']}")
            return msg

    def sign(self,coordinate:str,dm:str,sjdm:str):
        api = 'https://ehall.uwh.edu.cn/student/content/student/sign/stu/sign'
        params_load = {
            '_t_s_':self.__timeGen()
        }
        
        data_form = {
            "pathFile": "",
            "dm": dm,
            "sjdm": sjdm,
            "zb": coordinate,
            "wz": "安徽师范大学皖江学院（江北校区）附近",
            "ly": "lbs",
            "qdwzZt": "0",
            "fwwDistance": "0",    #距离签到位置距离
            "operationType": "Update"
        }

        try:
            res = self.s.post(api,params=params_load, data=data_form,headers=self.headers,timeout=45)
        except ConnectTimeout or Timeout:
            logger.error('请求签到超时')
            return {'code':'fail','msg':'请求签到超时'}
        if res.status_code == 200:
            msg = {'code': 'ok', 'msg': '成功签到', 'info': res.json()}
            logger.info(f"[{msg['code']}] {msg['msg']}")
            return msg
        else:
            msg = {'code': 'fail', 'msg': '签到失败', 'info': {'code': res.status_code, 'content': res.text}}
            logger.error(f"[{msg['code']}] {msg['msg']}\n{msg['info']}")
            return msg

    def isLoginSuccess(self) -> bool:
        if(self.getSignTask()['code'] == 'ok'):
            return True
        return False

async def wjcAccountSignTest(account:str,pswd:str) -> bool:
    wjc = WJC(account,pswd)
    wjc.login()
    return wjc.isLoginSuccess()
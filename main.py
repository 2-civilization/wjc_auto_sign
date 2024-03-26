import requests
from pswd_encrypt import encryptAES
from lxml import etree
from time import time as getTime


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
        res = self.s.get('https://ids.uwh.edu.cn/authserver/login?service=https://ehall.uwh.edu.cn/login', headers=self.headers)
        if res.status_code == 200:
            html = etree.HTML(res.text)
            try:
                self.__login_form.update({
                    'salt': html.xpath('//input[@id="pwdEncryptSalt"][1]/@value')[0],
                    'execution': html.xpath('//input[@id="execution"][1]/@value')[0]
                })
                return {'code': 1, 'msg': '成功获取加密参数出现错误', 'info': {}}
            except Exception as e:
                return {'code': 0, 'msg': '尝试获取加密参数出现错误，错误信息会被保存于info中', 'info': {'msg': e}}
        else:
            return {'code': 0, 'msg': '请求登录界面失败，具体信息将会被保存在info中',
                    'info': {'code': res.status_code, 'content': res.text}}

    def login(self):
        if not self.account or not self.pswd:
            return {'code': 0, 'msg': '账号或密码不能为空', 'info': {}}
        if not self.__login_form.get('salt') or not self.__login_form.get('execution'):
            return {'code': 0, 'msg': '无加密参数', 'info': {}}

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
        res = self.s.post('https://ids.uwh.edu.cn/authserver/login?service=https://ehall.uwh.edu.cn/login',headers=headers,data=data_form,verify=False)
        res_cas = self.s.post('https://ehall.uwh.edu.cn/student/cas')
        cookie = ''
        for k,v in self.s.cookies.get_dict().items():
            cookie += k+'='+v+';'
        
        print(cookie)
    
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
        print(params_load['_t_s_'])

        res = self.s.get(api, params=params_load)
        if res.status_code == 200:
            return {'code': 1, 'msg': '成功获取签到任务', 'info': res.json()}
        else:
            return {'code': 0, 'msg': '获取签到任务失败', 'info': {'code': res.status_code, 'content': res.text}}

        




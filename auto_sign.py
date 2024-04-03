from core import WJC
from setting import logger,db_get,DB_TABLE,REMOTE_API,TIME_SET,TIME_CHCECK_WAIT,DB_PATH,SIGN_MAX_TRY_TIMES,TIME_SLEEP_WAIT
from queue import Queue
from datetime import datetime,time
from db_control_sync import DBControl
import mail_control

class AutoSign:
    def __init__(self):
        self.q_user = Queue()
        self.q_fail_user = Queue()
        self.db = DBControl(DB_PATH)

    def sign(self,account, pswd,coordinate,email) -> bool:
        wjc = WJC(account, pswd)
        wjc.login()
        info = wjc.sign(coordinate,info['info']['aaData'][0]['DM'],info['info']['aaData'][0]['SJDM'])
        if info['code'] == 1:
            logger.info(f"{account} 签到成功")
            mail_content = mail_control.user_mail_gen(f"签到成功",f"{account} 签到成功",str(info['info']))
            mail_control.user_mail('签到成功',mail_content,email)
        
        else:
            logger.error(f"{account} 签到失败")
            self.q_fail_user.put({
                'account':account,
                'pswd':pswd,
                'coordinate':coordinate,
                'email':email,
                'info':str(info)
            })
        return info 

    def __sign_task_queue(self) -> None:
        data = self.db.get_users_info()
        logger.info(f"加载用户 {len(data)} 个")
        for u in data:
            u_info = {
                'account':u[0],
                'pswd':u[1],
                'coordinate':u[3],
                'email':u[2]
            }
            self.q_user.put(u_info)
    
    def sign_task(self):
        self.__sign_task_queue()
        while not self.q_user.empty():
            user = self.q_user.get()
            self.sign(user['account'],user['pswd'],user['coordinate'],user['email'])
            self.q_user.task_done()
        
    def __fail_user_sign(self) -> None:
        times_try = 0
        while not self.q_fail_user.empty() or times_try == SIGN_MAX_TRY_TIMES:
            user = self.q_fail_user.get()
            self.q_fail_user.task_done()
            self.db.user_sign(user['account'],user['pswd'],user['coordinate'],user['email'])
        
        while not self.q_fail_user.empty():
            user = self.q_fail_user.get()
            mail_content = mail_control.user_mail_gen('签到失败','签到失败',user['info'])
            mail_control.user_mail('签到失败',mail_content,user['email'])
            self.q_fail_user.task_done()
    

    def time_check(self):
        logger.info('时间检查开始')
        while True:
            while True:
                # 获取当前时间
                now = datetime.now()
                current_time = now.time()

                # 将时间区间转换为datetime.time对象
                start_time = time(hour=int(TIME_SET['start'].split(':')[0]), minute=int(TIME_SET['start'].split(':')[1]))
                end_time = time(hour=int(TIME_SET['end'].split(':')[0]), minute=int(TIME_SET['end'].split(':')[1]))

                if start_time <= current_time <= end_time:
                    logger.info('签到开始')
                    self.sign_task()
                    self.__fail_user_sign()
                    break
                else:
                    time.sleep(TIME_CHCECK_WAIT)
                users_info = self.db.get_users_info()
                info = []
                for user in users_info:
                    info.append({
                        'account':user[0],
                        'status':self.db.check_user(user[0])['msg'],
                        'success':user[6],
                        'total':user[7]
                    })
                mail_content = mail_control.admin_mail_gen(info)
                mail_control.user_mail('签到状态',mail_content)
            time.sleep(TIME_SLEEP_WAIT)



                

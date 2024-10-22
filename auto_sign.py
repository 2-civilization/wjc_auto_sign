from core import WJC
from setting import TIME_SET,TIME_CHCECK_WAIT,DB_PATH,SIGN_MAX_TRY_TIMES,TIME_SLEEP_WAIT
from queue import Queue
from datetime import datetime,time,date
from db_control import getDBControl
import mail_control
import asyncio
from log_setting import logger

class AutoSign:
    def __init__(self):
        self.q_user = Queue()
        self.q_fail_user = Queue()

    async def __error_msg_gen(self,content:str) -> str:
        if '请登录' in content or '需要登录才能进去系统' in content:
            return '账号密码可能错误'
        else:
            __info = content.split('body')
            if len(__info) == 3:
                return __info[1]
        return '未知错误'

    @logger.catch
    async def sign(self,account, pswd,coordinate,email,fail_try:bool=False):
        wjc = WJC(account, pswd)
        db = await getDBControl(DB_PATH)
        try:
            wjc.login()
            info = wjc.getSignTask()
            info = wjc.sign(coordinate,info['info']['aaData'][0]['DM'],info['info']['aaData'][0]['SJDM'])
            if info['code'] == 'ok':
                logger.info(f"{account} 签到成功")
                #mail_content = mail_control.user_mail_gen(f"签到成功",f"{account} 签到成功",str(info['info']))
                # mail_control.user_mail('签到成功',mail_content,email)
                #await mail_control.new_user_mail('签到成功',mail_content,email)

                await db.user_sign(account)
            else:
                logger.error(f"{account} 签到失败")
                self.q_fail_user.put({
                    'account':account,
                    'pswd':pswd,
                    'coordinate':coordinate,
                    'email':email,
                    'info':str(info)
                })
                await db.user_try_add(account)
        except Exception:
            logger.error(f"{account} 签到失败")
            if not fail_try:
                self.q_fail_user.put({
                    'account':account,
                    'pswd':pswd,
                    'coordinate':coordinate,
                    'email':email,
                    'info':str(info)
                })
            await db.user_try_add(account)
        
        return info 

    async def __sign_task_queue(self) -> None:
        db = await getDBControl(DB_PATH)
        data = await db.get_users_info()
        logger.info(f"加载用户 {len(data)} 个")
        for u in data:
            if not u[8]:
                # active 0 跳过该用户
                continue

            if (await db.check_user(u[0]))['code'] == 'ok':
                u_info = {
                    'account':u[0],
                    'pswd':u[1],
                    'coordinate':u[3],
                    'email':u[2]
                }

                self.q_user.put(u_info)
        logger.info(f"待签到用户数 {self.q_user.qsize()} 个")

    async def sign_task(self):
        await self.__sign_task_queue()
        while not self.q_user.empty():
            user = self.q_user.get()
            await self.sign(user['account'],user['pswd'],user['coordinate'],user['email'])
            self.q_user.task_done()
    
    @logger.catch
    async def __fail_user_sign(self) -> None:
        db = await getDBControl(DB_PATH)
        logger.info('重试队列开始')
        times_try = 1
        while not self.q_fail_user.empty() and times_try < SIGN_MAX_TRY_TIMES:
            logger.info(f"第 {times_try} 次重试开始")
            user = self.q_fail_user.get()
            self.q_fail_user.task_done()
            await self.sign(user['account'],user['pswd'],user['coordinate'],user['email'],fail_try=True)
            logger.info(f"第 {times_try} 次重试结束")
            times_try +=1
        
        logger.info('重试队列结束')
        while not self.q_fail_user.empty():
            user = self.q_fail_user.get()
            mail_content = mail_control.user_mail_gen('签到失败','请检查账号密码等信息是否正确',await self.__error_msg_gen(user['info']))
            mail_control.user_mail('签到失败',mail_content,user['email'])
            #await mail_control.new_user_mail('签到失败',mail_content,user['email'])

            self.q_fail_user.task_done()
            logger.info(f"向用户{user['account']}发送签到失败信息成功")

            # 添加失败天数
            await db.user_fail_day_add(user['account'])

            # 尝试封禁失败用户
            if await db.deactive_user(user['account']):
                mail_content = mail_control.ban_mail_gen(str(user['account']))
                mail_control.user_mail('自动签到停止',mail_content,user['email'])
                # await mail_control.new_user_mail('自动签到停止',mail_content,user['email'])
                
                logger.info(f"向用户{user['account']}发送账号禁用成功")
        
    async def time_check(self):
        logger.info('时间检查开始')
        while True:
            while True:
                # 获取当前时间
                now = datetime.now()
                current_time = now.time()

                # 将时间区间转换为datetime.time对象
                start_time = time(hour=int(TIME_SET['start'].split(':')[0]), minute=int(TIME_SET['start'].split(':')[1]))
                end_time = time(hour=int(TIME_SET['end'].split(':')[0]), minute=int(TIME_SET['end'].split(':')[1]))

                TIME_CHCECK_WAIT = int(datetime.combine(date.today(),start_time).timestamp()-now.timestamp())
                if TIME_CHCECK_WAIT <1:
                    TIME_CHCECK_WAIT = 1

                if start_time <= current_time <= end_time:
                    logger.info('签到开始')
                    await self.sign_task()
                    await self.__fail_user_sign()
                    logger.info('签到结束，开始发送管理员邮件')
                    db = await getDBControl(DB_PATH)
                    users_info = await db.get_users_info()
                    info = []
                    for user in users_info:
                        info.append({
                            'account':user[0],
                            'status':'是' if (await db.check_user(user[0]))['code'] == 'ok_signed' else '否',
                            'success':user[6],
                            'total':user[7],
                            'active':user[8],
                        })
                    mail_content = mail_control.admin_mail_gen(info)
                    mail_control.admin_mail('签到状态',mail_content)
                    break
                else:
                    logger.info(f'未到签到开始时间，等待{TIME_CHCECK_WAIT}秒后重新开始签到')
                    await asyncio.sleep(TIME_CHCECK_WAIT)
                    continue
                
            logger.info(f'签到结束，等待{TIME_SLEEP_WAIT}')
            await asyncio.sleep(TIME_SLEEP_WAIT)

    @logger.catch
    def run(self):
        asyncio.run(self.time_check())

if __name__ == '__main__':
    auto_sign = AutoSign()
    auto_sign.run()

                

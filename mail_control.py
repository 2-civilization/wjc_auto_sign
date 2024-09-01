import yagmail
import yagmail.error
from setting import MAIL_SET,CURRENT_PATH
from smtplib import SMTPDataError
from log_setting import logger
from queue import Queue
from time import sleep
from threading import Thread
import asyncio
import re

def html_get(target:str,info_list:list) -> str:
    def get_content():
        path = {
            'notice':CURRENT_PATH+'temp_doc/notice.html',
        }
        with open(path[target],'r',encoding='utf-8') as f:
            return f.read()
    


    # 使用正则表达式查找所有"WAIT_TO_REPLACE"位置
    origin_content = get_content(target)
    pattern = re.compile(r"WAIT_TO_REPLACE")
    matches = list(pattern.finditer(origin_content))

    # 替换每个"WAIT_TO_REPLACE"位置的内容
    replaced_str = ""
    last_index = 0
    for i, match in enumerate(matches):
        replaced_str += origin_content[last_index:match.start()] + info_list[i]
        last_index = match.end()
    replaced_str += origin_content[last_index:]

    print(replaced_str)


def admin_mail(subject:str, contents:str) -> None:
    try:
        yag = yagmail.SMTP(user=MAIL_SET['account'], password=MAIL_SET['token'], host=MAIL_SET['host'])
        yag.send(to=MAIL_SET['admin'], subject=subject, contents=contents)
        logger.info('管理员邮件发送成功！')
    except Exception as e:
        logger.error(f'管理员邮件发送失败！可能是由于是邮箱设置有误->{e}')


def user_mail(subject:str, contents:str, user:str) -> bool:
    try:
        yag = yagmail.SMTP(user=MAIL_SET['account'], password=MAIL_SET['token'], host=MAIL_SET['host'])
        yag.send(to=user, subject=subject, contents=contents)
        logger.info(f'用户邮件发送成功！->{user}')
        return True
    except SMTPDataError or yagmail.error.YagInvalidEmailAddress:
        logger.error(f'用户邮件发送失败！邮箱地址可能错误。->{user}')
        return False

def user_mail_gen(title:str,info:str,code:str):
    content = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
        }
        
        h1, p {
            text-align: center;
        }
    </style>
    <title>'''+title+'''-自动签到状态提醒</title>
</head>
<body>
    <h1>'''+title+'''</h1>
    <p>这是一封由程序自动生成的邮件，请勿回复！</p>
    <p>自动签到程序将会使用你注册时填写的信息为你自动签到，并会在签到失败时向你发送邮件提醒。</p>
    <p>自动签到程序启动时间约为20:30-21:00，此期间请注意是否收到签到失败的邮件或前往校芜优验证签到状态。</p>
    <p>签到状态如邮件中展示，如若签到失败请手动签到，多次失败请向此邮件发送反馈邮件，标题为 签到失败+你的签到问题，内容任意。</p>
    <p>以下为签到的信息</p>
    <p>签到：'''+info+'''</p>
    <p>响应信息：</p>
    <pre><code>'''+code+'''
    </code></pre>
</body>
</html>
    '''
    #return html_get(target='notice',info_list=[title,info,code])
    return content





def admin_mail_gen(info_list:list):
    def __active_str_gen(active:int)->str:
        return '启用' if info['active'] else '禁用'

    content = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
        }

        h1, p, table {
            text-align: center;
        }
        
        table {
            margin: auto;
            border-collapse: collapse;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
    </style>
    <title>签到日志</title>
</head>
<body>
    <h1>今日签到</h1>
    <p>以下为今日签到的状态</p>
    <table>
        <thead>
            <tr>
                <th>账号</th>
                <th>是否签到</th>
                <th>成功次数</th>
                <th>总次数</th>
                <th>状态</th>
            </tr>
        </thead>
        <tbody>
    '''
    for info in info_list:
        content += '''
            <tr>
                <td>'''+str(info['account'])+'''</td>
                <td>'''+info['status']+'''</td>
                <td>'''+str(info['success'])+'''</td>
                <td>'''+str(info['total'])+'''</td>
                <td>'''+__active_str_gen(info['active'])+'''</td></tr>
        '''
    content += '''
        </tbody>
    </table>
</body>
</html>
'''
    return content

def reg_mail_gen(info:dict):
    content = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
        }
        
        h1, p {
            text-align: center;
        }
    </style>
    <title>自动签到注册&更新成功！</title>
</head>
<body>
    <h1>自动签到注册&更新成功！</h1>
    <p>这是一封由程序自动生成的邮件，请勿回复！</p>
    <p>自动签到程序将会使用你注册时填写的信息为你自动签到，并会在签到失败时向你发送邮件提醒。</p>
    <p>自动签到程序启动时间约为20:30-21:00，此期间请注意是否收到签到失败的邮件或前往校芜优验证签到状态。</p>
    <p>注意！如果你在签到时间段内进行注册或更新，你将不会被自动签到，当日你仍然需要进行手动签到！</p>
    <p>你注册的信息如下，如若填写错误或需要更新请重新注册提交即可。</p>
    <p>账号：'''+info['account']+'''</p>
    <p>邮箱：'''+info['email']+'''</p>
    <p>坐标：'''+info['coordinate']+'''</p>
</body>
</html>
    '''
    return content

def ban_mail_gen(account:str):
    content = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
        }
        
        h1, p {
            text-align: center;
        }
    </style>
    <title>自动签到账户停用通知</title>
</head>
<body>
    <h1>你已无法继续使用自动签到</h1>
    <p>这是一封由程序自动生成的邮件，请勿回复！</p>
    <p>你选择了主动取消自动签到，或由于你提供的账号信息在3天内连续签到失败且你未能及时更新信息，现在已经停止为你自动签到。</p>
    <p>如果你希望继续使用，请回到注册页重新进行注册。</p>
    <p>你提供的账号信息：'''+account+'''</p>
</body>
</html>
'''
    return content

def email_validate_gen(code:str):
    content = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>自动签到注册验证码</title>
</head>
<body>
<p>你的验证码为：<b>'''+code+'''</b></p>
<p>验证码有效期为3分钟，请尽快填入！</p>
</body>
</html>
'''
    return content

async def new_user_mail(subject:str,contents:str,user:str):
    # 实际用处不大，废弃
    user_mail(subject,contents,user)
    await asyncio.sleep(2)

class MailQueue:
    def __init__(self,queue_wait_time:int=30):
        self.queue_wait_time = queue_wait_time
        self.mail_queue = Queue()
        self.mail_thread_flag = True
        self.mail_thread = None

    def add(self,subject:str,contents:str,user:str) -> None:
        self.mail_queue.put({
            'subject':subject,
            'contents':contents,
            'user':user,
            'try':0
        })
    
    def post(self) -> str:
        # while not self.mail_queue.empty() or not self.mail_thread_flag:
        while not self.mail_queue.empty():
            mail = self.mail_queue.get()
            logger.info(f'发送邮件至{mail["user"]}，第{mail["try"]+1}次尝试')
            res = user_mail(mail['subject'],mail['contents'],mail['user'])
            self.mail_queue.task_done()
            if not res and mail['try']<3:
                # 将会额外尝试发送3次
                mail.update({'try':mail['try']+1})
                self.mail_queue.put(mail)
            sleep(self.queue_wait_time)

        logger.info('邮件队列结束')
    def start(self) -> None:
        logger.info('邮件队列已启动')
        self.mail_thread = Thread(target=self.post)
        self.mail_thread.start()

    def stop(self) -> None:
        # 暂时弃用
        logger.info('邮件队列准备结束')
        self.mail_thread_flag = False
        
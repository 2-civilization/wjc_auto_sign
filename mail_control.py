import yagmail
from setting import MAIL_SET,logger

def admin_mail(subject:str, contents:str) -> None:
    yag = yagmail.SMTP(user=MAIL_SET['account'], password=MAIL_SET['token'], host=MAIL_SET['host'])
    yag.send(to=MAIL_SET['admin'], subject=subject, contents=contents)
    logger.info('管理员邮件发送成功！')


def user_mail(subject:str, contents:str, user:str) -> None:
    yag = yagmail.SMTP(user=MAIL_SET['account'], password=MAIL_SET['token'], host=MAIL_SET['host'])
    yag.send(to=user, subject=subject, contents=contents)
    logger.info(f'用户邮件发送成功！->{user}')

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
    <p>自动签到程序启动时间约为20:30-22:00，如若超出该时间仍未受到通知邮件请手动检查并签到！</p>
    <p>签到状态如邮件中展示，如若签到失败请手动签到，多次失败请向此邮件发送反馈邮件，标题为 签到失败+你的签到问题，内容任意。</p>
    <p>以下为签到的信息</p>
    <p>签到：'''+info+'''</p>
    <p>响应信息：</p>
    <pre><code>'''+code+'''
    </code></pre>
</body>
</html>
    '''
    return content

def admin_mail_gen(info_list:list):
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
            </tr>
        </thead>
        <tbody>
    '''
    for info in info_list:
        content += '''
            <tr>
                <td>'''+info['account']+'''</td>
                <td>'''+info['status']+'''</td>
                <td>'''+str(info['success'])+'''</td>
                <td>'''+str(info['total'])+'''</td>
            </tr>
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
    <p>自动签到程序将会使用你注册时填写的信息为你自动签到，并会向你邮寄一封电子邮件以供你确认状态信息。</p>
    <p>自动签到程序启动时间约为20:30-22:00，如若超出该时间仍未受到通知邮件请手动检查并签到！</p>
    <p>你注册的信息如下，如若填写错误或需要更新请重新注册提交即可。</p>
    <p>账号：'''+info['account']+'''</p>
    <p>邮箱：'''+info['email']+'''</p>
    <p>坐标：'''+info['coordinate']+'''</p>
</body>
</html>
    '''
    return content


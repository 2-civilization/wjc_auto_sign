from sanic import Sanic
from sanic.response import html,json,file
import os
from pathlib import Path
from db_control import DBControl
from setting import DB_PATH,REMOTE_API_TOKEN,TIME_SET,logger
from mail_control import user_mail,reg_mail_gen
from datetime import datetime,time,timedelta

NOW_FILE_PATH = os.path.dirname(os.path.abspath(__file__))

DB = DBControl(DB_PATH)

app = Sanic("webSubmitter")
# app.static("/template","D:\\REPOSITORY\\PROJECTS\\Project\\WJC_Sign\\WebSubmitter\\template")

async def is_db_locked() -> bool:
    # 获取当前时间
    now = datetime.now()
    # 增加1s的延迟
    now += timedelta(seconds=1)
    current_time = now.time()
    
    # 将时间区间转换为datetime.time对象
    start_time = time(hour=int(TIME_SET['start'].split(':')[0]), minute=int(TIME_SET['start'].split(':')[1]))
    end_time = time(hour=int(TIME_SET['end'].split(':')[0]), minute=int(TIME_SET['end'].split(':')[1]))

    if start_time <= current_time <= end_time:
        # 处于签到时间点，禁止数据库操作
        return True
    else:
        return False
    

@app.get('/')
async def index(request):
    # async with aiofiles.open('/template/submit_index.html', mode='r') as f:
    #     content = await f.read()
    #     return html(content)
    return await file(Path(NOW_FILE_PATH+"/template/submit_index.html"))


@app.get('/customLocalHelp')
async def customHelp(request):
    # async with aiofiles.open('/template/custom_readme.html', mode='r') as f:
    #     content = await f.read()
    #     return html(content)
    return await file(Path(NOW_FILE_PATH+"/template/custom_readme.html"))


@app.get('/file/local')
async def getLocal(request):
    # async with aiofiles.open('/local.json', mode='r') as f:
    #     content = await f.read()
    #     return json(content)
    return await file(Path(NOW_FILE_PATH+"/local.json"))


@app.post('/submit')
@logger.catch
async def submit(request):
    if await is_db_locked():
        logger.error(f'[WEB]用户{form["username"][0]} - {form["email"][0]}在脚本启动期内被拒绝注册')
        return json({"code":'fail','msg':f'当前时间段（{TIME_SET["start"]} - {TIME_SET["end"]}）无法注册，请在非此时间段再重试'})
    
    form = request.get_form()
    if user_mail('注册成功',reg_mail_gen({'account':form["username"][0],'email':form["email"][0],'coordinate':form["coordinates"][0]}),form["email"][0]):
        await DB.add_user(form["username"][0],form["password"][0],form["email"][0],form["coordinates"][0])
        logger.info(f'[WEB]用户{form["username"][0]} - {form["email"][0]}注册成功')
        return json({"code":'ok','msg':'提交成功，请检查你的邮箱！'})
    else:
        logger.error(f'[WEB]用户{form["username"][0]} - {form["email"][0]}注册失败')
        return json({"code":'fail','msg':'提交失败，请检查你的邮箱地址是否填写正确！'})
    

@app.get('/reg_success_page')
async def reg_success_page(request):
    return await file(Path(NOW_FILE_PATH+"/template/reg_success_page.html"))

@app.post('/getUsers')
@logger.catch
async def get_users_info(request):
    if await is_db_locked():
        return json({"code":'fail','msg':f'当前时间段（{TIME_SET["start"]} - {TIME_SET["end"]}）无法获取用户信息，请在非此时间段再重试'})
    

    form = request.get_form()
    if form["token"][0] == REMOTE_API_TOKEN:
        users = await DB.get_users_info()
        logger.info(f'获取用户信息成功')
        return json({"code":'ok',"msg":'验证成功','data':users})
    else:
        logger.error(f'获取用户信息失败，验证token ->{form["token"][0]}')
        return json({"code":'fail','msg':'验证失败'})

@app.get('/favicon.ico')
async def get_favicon(request):
    return await file(Path(NOW_FILE_PATH+"/template/favicon.ico"))

@logger.catch
def run():
    app.run('0.0.0.0', port=8081,debug=True)
    # app.run('::',443,ssl='/home/admin/certificate/')

if __name__ == '__main__':
    run()

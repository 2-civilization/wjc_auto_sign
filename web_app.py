from fastapi import FastAPI,Form
from fastapi.responses import HTMLResponse,JSONResponse,Response
from datetime import datetime,time,timedelta
from fastapi.staticfiles import StaticFiles
from setting import DB_PATH,TIME_SET
from mail_control import user_mail,reg_mail_gen,email_validate_gen
from db_control import getDBControl
import aiofiles
from pathlib import Path
import os
from core import wjcAccountSignTest
import uvicorn
from log_setting import logger
from web_regControl import RegControl

NOW_FILE_PATH = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()
app.mount("/static", StaticFiles(directory="web_app/build/static"), name="static")

eDB = RegControl()

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


@app.get('/',response_class=HTMLResponse)
async def index():
    async with aiofiles.open(Path(NOW_FILE_PATH+"/web_app/build/index.html"),encoding='utf-8') as f:
        return HTMLResponse(await f.read(),status_code=200)


@app.get('/favicon.ico')
async def get_favicon():
    async with aiofiles.open(Path(NOW_FILE_PATH+"/web_app/build/favicon.ico"),'rb') as f:
        return Response(await f.read(),media_type='image/x-icon')

@app.post('/checkAccount')
async def check_account(account:str=Form(),pswd:str=Form(),email:str=Form()):
    global eDB
    if(await is_db_locked()):
        logger.info(f'用户 {account} 尝试在非开放时间点注册')
        return JSONResponse({'code':'fail','msg':f'当前时间段 ({TIME_SET["start"]} - {TIME_SET["end"]}) 无法注册，请在非此时间段再重试'})
    
    await eDB.init_db()

    if(await eDB.check_user(account,pswd) or await wjcAccountSignTest(account,pswd)):
        emailVCode = await eDB.updata_user(account,pswd,email)

        res = user_mail('自动签到注册邮箱验证码',f'您的验证码为：{emailVCode}',email)
        if(res):
            return JSONResponse(content={'code':'ok','msg':'账号验证成功'})
        else:
            return JSONResponse(content={'code':'fail','msg':'邮箱不存在或格式错误'})
    else:
        return JSONResponse(content={'code':'fail','msg':'账号或密码错误'})

@app.post('/stopAccount')
async def cancel_reg(account:str=Form(),pswd:str=Form()):
    DB = await getDBControl(DB_PATH)
    if(await DB.is_user_exist(account,pswd) and await wjcAccountSignTest(account,pswd)):
        if await DB.deactive_user(account=account,ban_by_user=True):
            return JSONResponse(content={'code':'ok','msg':'取消注册成功'})
        else:
            return JSONResponse(content={'code':'fail','msg':'取消注册失败'})
    else:
        return JSONResponse(content={'code':'fail','msg':'未注册自动签到或账号密码错误'})
@app.post('/emailCheck')
async def emailCheck(account:str=Form(),emailVCode:str=Form()):
    global eDB
    if(await is_db_locked()):
        return JSONResponse({'code':'fail','msg':f'当前时间段 ({TIME_SET["start"]} - {TIME_SET["end"]}) 无法注册，请在非此时间段再重试'})
    
    await eDB.init_db()

    if await eDB.check_email(account,emailVCode):
        return JSONResponse(content={'code':'ok','msg':'邮箱验证成功！'})
    else:
        return JSONResponse(content={'code':'fail','msg':'验证码错误或已过期！'})


@app.post('/submit')
async def submit(account:str=Form(),coordinate:str=Form()):
    global eDB
    if(await is_db_locked()):
        return JSONResponse({'code':'fail','msg':f'当前时间段 ({TIME_SET["start"]} - {TIME_SET["end"]}) 无法注册，请在非此时间段再重试'})
    
    await eDB.init_db()

    if await eDB.is_user_pass(account):
        user_info = await eDB.finish_reg(account)
        DB = await getDBControl(DB_PATH)
        await DB.add_user(account,user_info['pswd'],user_info['email'],coordinate)
        user_mail('自动签到注册成功',reg_mail_gen({'account':account,'email':user_info['email'],'coordinate':coordinate}),user_info['email'])
        return JSONResponse(content={'code':'ok','msg':'注册成功'})
    else:
        return JSONResponse(content={'code':'fail','msg':'当前账号未通过验证'})
    

if __name__ == '__main__':
    uvicorn.run(app='web_app:app',host='0.0.0.0',port=8000,reload=True)
    #uvicorn.run(app='web_app:app',host='0.0.0.0',port=443,ssl_keyfile='/home/admin/certificate/certkey.key',ssl_certfile='/home/admin/certificate/certfile.cer')
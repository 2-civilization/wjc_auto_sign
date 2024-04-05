from sanic import Sanic
from sanic.response import html,json,file
import aiofiles
import os
from pathlib import Path
from db_control import DBControl
from setting import DB_PATH,REMOTE_API_TOKEN
from mail_control import user_mail,reg_mail_gen


NOW_FILE_PATH = os.path.dirname(os.path.abspath(__file__))

DB = DBControl(DB_PATH)

app = Sanic("webSubmitter")
# app.static("/template","D:\\REPOSITORY\\PROJECTS\\Project\\WJC_Sign\\WebSubmitter\\template")

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
async def submit(request):
    form = request.get_form()
    if user_mail('注册成功',reg_mail_gen({'account':form["username"][0],'email':form["email"][0],'coordinate':form["coordinates"][0]}),form["email"][0]):
        await DB.add_user(form["username"][0],form["password"][0],form["email"][0],form["coordinates"][0])
        return json({"code":'ok','msg':'提交成功，请检查你的邮箱！'})
    else:
        return json({"code":'fail','msg':'提交失败，请检查你的邮箱地址是否填写正确！'})

@app.get('/reg_success_page')
async def reg_success_page(request):
    return await file(Path(NOW_FILE_PATH+"/template/reg_success_page.html"))

@app.post('/getUsers')
async def get_users_info(request):
    form = request.get_form()
    if form["token"][0] == REMOTE_API_TOKEN:
        users = await DB.get_users_info()
        return json({"code":'ok',"msg":'验证成功','data':users})
    else:
        return json({"code":'fail','msg':'验证失败'})

@app.get('/favicon.ico')
async def get_favicon(request):
    return await file(Path(NOW_FILE_PATH+"/template/favicon.ico"))

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080,debug=True)
    # app.run('::',443,ssl='/home/admin/certificate/')

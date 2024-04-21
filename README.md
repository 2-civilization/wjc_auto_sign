# README

芜湖学院（原 安徽师范大学皖江学院） 签到自动化

目前实现：
- 签到端
  - 用于从数据库中提取用户数据并在规定时间内启动签到任务，完成后自动等待至下一次签到开始。
- 注册信息端
  - 提供Web页面向用户提供注册功能，将用户提交的信息保存至数据库供签到端使用

待实现：
- 两端分离，签到端自动同步数据库
- （Web）为用户提供取消签到功能，用户可自行选择是否启用自动签到（是否停用）
- 对于签到次数过多的账号，将会自动停用该账号
  - 签到失败天数达到3天
- （Web）简易的管理后台，方便对用户签到信息进行监控以及管理
- （Web）显示历史更新版本

## 使用说明

### 准备环境：
- Python3.8+

使用pip安装依赖：
```shell
pip install -r requirements_web.txt
```

> 如果你只用于本地使用且不需要Web页面提供注册功能，可选择手动向signinInfo.db中添加数据。同时选择安装以下依赖即可：
> ```shell
> pip install -r requirements.txt
> ```

### 配置（可选）

`setting.py`文件用于配置脚本运行，提供以下参数供修改：

- `DB_PATH`：数据库名。数据库使用Sqlite3，不存在会按此名词自动生成，如无需要不推荐修改
- `DB_TABLE`：用于保存用户信息的表名，同样无需要不推荐修改。
- `TIME_SET`：邮箱推送设置
  - `start`：签到任务开始时间
  - `end`：签到任务结束时间。**注意**：该时间应该小于实际签到结束时间，让脚本提前结束，避免签到失败的信息无法及时推送，以错过手动签到。
- `TIME_CHCECK_WAIT`：由于脚本难以精确地在签到开始时启动，所以会提前启动，并检测签到是否开始，首次检测时间间隔，默认为180秒。该值仅限第一次检测，后会根据响应的结果自动调整。
- `TIME_SLEEP_WAIT`：签到完成后等待下一次启动时间，不推荐修改。
- `MAIL_SET`：邮箱推送设置
  - `admin`：一天的签到任务结束后向该邮箱推送今日所有用户的签到情况。
  - `account`：推送信息将由此邮箱发送。
  - `host`：邮箱服务器
  - `token`：邮箱授权码

### 添加数据

#### 手动添加数据

推荐先启动`auto_sign.py`来初始化下数据库，然后再向`signInfo.db`中添加数据

> 你也可以参照`setting.py`中的`DB_INIT_SQL`来手动创建对应的表结构。

#### 使用Web端添加数据

启动Web端
```shell
python web_app.py
```

访问`http://127.0.0.1:8080`即可进行注册

### 开始自动签到

完成上面的准备步骤后，现在可以将`auto_sign.py`启动，它会自动从数据库中提取用户数据并在规定时间内启动签到任务，完成后自动等待至下一次签到开始。

每次完成签到任务，都会向每个用户发送邮件确认，并额外向管理员发送邮件汇报今日签到任务结果。

## 开发说明

2024年学校官网及统一认证平台功能逐步上线正常，网页中终于可通过一些手段进入，便于抓包逆向。

签到步骤：
- 根据设置的账号密码登录获取必要的Token或Cookies
- (额外)检测是否需要验证，如若需要则启动反验证码模块
- 携带必要信息查询签到任务
- 根据设置签到任务
- (额外)通知设置的账户信息签到状态

## 模块

### 登录

API:
- URL:`https://ids.uwh.edu.cn/authserver/login?service=https://ehall.uwh.edu.cn/login`
- METHOD: GET | POST
- PARAMS: NONE
- DATA: (FORM)
  - username:账号
  - password:密码（加密）
  - captcha:验证码
  - _eventId:`submit`
  - cllt:`userNameLogin`
  - dllt:`generalLogin`
  - lt: 保持为空
  - execution:来自前置页面

前置页：需要预先GET此页，包含了POST时所需的必要信息（data和cookie）

API:
- URL:`https://ehall.uwh.edu.cn/student/cas`
- METHOD: POST

上一个请求成功后携带Cookie直接访问即可，另有登录界面，需要额外密码（身份证号后六位），不推荐。

### 获取签到任务

API: 
- URL: 'https://ehall.uwh.edu.cn/student/content/tabledata/student/sign/stu/sign'
- METHOD: GET
- PARAMS: 见下
- RESPONSE-TYPE: (JSON)见下

Params:
```python
params_load = {
            "bSortable_0": "false",
            "bSortable_1": "true",
            "iSortingCols": "1",
            "iDisplayStart": "0",
            "iDisplayLength": "12",
            "iSortCol_0": "3",
            "sSortDir_0": "desc",
            "_t_s_": "1711441937310"
        }
```
其中`_t_s_`为13位时间戳

Response:
```json

{
	"sEcho": 1,
	"iDisplayStart": 0,
	"iDisplayLength": 12,
	"iSortColList": [2],
	"sSortDirList": ["desc"],
	"iTotalRecords": 1,
	"iTotalDisplayRecords": 1,
	"aaData": [{
		"UPDATE_COUNT": 2,
		"JSSJ": "2024-03-26 23:00:00",
		"QDFS": "1",
		"SJDM": "17112924123429681075",
		"QDCS": null,
		"VALID": "0",
		"DM": "17089192567824456997",
		"JLDM": null,
		"QDWZ_DZ": null,
		"QDLB": "晚间签到",
		"QDSJ": null,
		"UPDATE_IND": "1",
		"FBR": "张铮",
		"SUBJECT": "江北校区晚间签到",
		"KSSJ": "2024-03-26 20:30:00",
		"ISFZR": "0"
	}]
}

```

成功签到示例：
```json

{
    "code": 1,
    "msg": "成功获取签到任务",
    "info": {
        "sEcho": 1,
        "iDisplayStart": 0,
        "iDisplayLength": 12,
        "iSortColList": [2],
        "sSortDirList": ["desc"],
        "iTotalRecords": 1,
        "iTotalDisplayRecords": 1,
        "aaData": [
            {
                "UPDATE_COUNT": 2,
                "JSSJ": "2024-03-26 23:00:00",
                "QDFS": "1",
                "SJDM": "17112924123429681075",
                "QDCS": 1,
                "VALID": "1",
                "DM": "17089192567824456997",
                "JLDM": "17114572277777336296",
                "QDWZ_DZ": "中国安徽 省芜湖市鸠江区二坝镇通江大道辅路",
                "QDLB": "晚间签到",
                "QDSJ": "2024-03-26 20:47:07",
                "UPDATE_IND": "1",
                "FBR": "张铮",
                "SUBJECT": "江北 校区晚间签到",
                "KSSJ": "2024-03-26 20:30:00",
                "ISFZR": "0"
            }
        ]
    }
}

```


其中:
- `JSSJ`：签到结束时间
- `KSSJ`: 签到开始时间
- `SJDM`和`DM`: 后续签到需要用到的信息。
- `QDSJ`: 签到时间 时间格式：`YYYY-MM-DD H:M:S`
  - `null` 未签到
- `VALID`: 
  - `"0"`：未开始
  - `"1"`：已开始
- 



## 更新日志

- 2024-04-21_Ver1.0.0:
  - 正式版本

# README

芜湖学院 签到自动化

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

其中:
- `SJDM`和`DM`: 后续签到需要用到的信息。
- `QDSJ`: `null` 未签到
- `VALID`: `"0"`未开始










import os.path as os_path


CURRENT_PATH = os_path.dirname(os_path.abspath(__file__))

DB_PATH = 'signInfo.db'
DB_TABLE = 'users'

DB_PATH = os_path.join(CURRENT_PATH, DB_PATH)

REMOTE_API = {
    'update':''
}

REMOTE_API_TOKEN = '7aF9dPcE3bR2sW1xV6mG5tN8yH4qJ0lK'

TIME_SET = {
    'start': '20:30',  
    'end': '22:00' #'23:00'      # 提前结束预留时间
}

MAIL_SET = {
    'admin':'',
    'account':'',
    'host': '',
    'token':''
}

TIME_CHCECK_WAIT = 180  # 3分钟
TIME_SLEEP_WAIT = 60*60*22 # 22小时

SIGN_MAX_TRY_TIMES = 3 # 签到失败最多尝试次数
FAIL_MAX_TRY_DAYS = 3   # 最大连续失败签到天数，达到该天数后将会禁用用户自动签到

DB_INIT_SQL = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER NOT NULL PRIMARY KEY,
        pswd TEXT NOT NULL,
        email TEXT NOT NULL,
        coordinate TEXT NOT NULL,
        updateTime TEXT NOT NULL,
        signTime TEXT,
        success INTEGER DEFAULT 0,
        total INTEGER DEFAULT 0,
        active INTEGER DEFAULT 1,
        failDays INTEGER DEFAULT 0
    );
'''


import logging
import os.path as os_path
from os import mkdir as os_mkdir
from datetime import datetime

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
        id INTEGER NOT NULL PRIMARY KEY UNIQUE,
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


def __logger_set():
    # 日志设置
    __current_path = CURRENT_PATH
    __log_dir = os_path.join(__current_path, 'logs')

    if not os_path.exists(__log_dir):
        os_mkdir(__log_dir)


    # 创建一个logger实例
    logger = logging.getLogger('LOGGER')
    logger.setLevel(logging.DEBUG)  # 设置日志级别为DEBUG，可以根据需要调整为INFO、ERROR等
    __formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # 创建一个StreamHandler用于输出到控制台
    __console_handler = logging.StreamHandler()
    __console_handler.setLevel(logging.INFO)  # 控制台只显示INFO及更高级别的日志
    __console_handler.setFormatter(__formatter)
    logger.addHandler(__console_handler)

    # 创建一个FileHandler并设置其保存路径
    # 定义日志文件名，包含启动时刻的日期
    __log_file_path = os_path.join(__log_dir, f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    __file_handler = logging.FileHandler(__log_file_path,encoding='utf-8')
    __file_handler.setLevel(logging.DEBUG)  # 文件保存所有级别的日志
    __file_handler.setFormatter(__formatter)
    logger.addHandler(__file_handler)

    return logger

logger = __logger_set()

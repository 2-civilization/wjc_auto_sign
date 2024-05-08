from datetime import datetime
import loguru

def __logger_set(DEBUG_ENV:bool=False):
    logger = loguru.logger
    log_file_name = f"./logs/log_{datetime.now().strftime('%Y%m%d_%H-%M-%S')}.log"

    # 自动向屏幕输出日志，因此仅需添加文件Handler
    logger.add(
        sink=log_file_name,
        level='DEBUG',
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        backtrace=True,
        diagnose=DEBUG_ENV,     # 显示变量值，不推荐生产环境中设为True
        enqueue=True,
        catch=True,
        retention='1 week',
        delay=True
    )
    return logger

logger = __logger_set()

# import os.path as os_path
# import logging
# from os import mkdir as os_mkdir


# CURRENT_PATH = os_path.dirname(os_path.abspath(__file__))
# def __old_logger_set():
#     # 日志设置
#     __current_path = CURRENT_PATH
#     __log_dir = os_path.join(__current_path, 'logs')

#     if not os_path.exists(__log_dir):
#         os_mkdir(__log_dir)


#     # 创建一个logger实例
#     logger = logging.getLogger('LOGGER')
#     logger.setLevel(logging.DEBUG)  # 设置日志级别为DEBUG，可以根据需要调整为INFO、ERROR等
#     __formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

#     # 创建一个StreamHandler用于输出到控制台
#     __console_handler = logging.StreamHandler()
#     __console_handler.setLevel(logging.INFO)  # 控制台只显示INFO及更高级别的日志
#     __console_handler.setFormatter(__formatter)
#     logger.addHandler(__console_handler)

#     # 创建一个FileHandler并设置其保存路径
#     # 定义日志文件名，包含启动时刻的日期
#     __log_file_path = os_path.join(__log_dir, f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
#     __file_handler = logging.FileHandler(__log_file_path,encoding='utf-8')
#     __file_handler.setLevel(logging.DEBUG)  # 文件保存所有级别的日志
#     __file_handler.setFormatter(__formatter)
#     logger.addHandler(__file_handler)

#     return logger

# logger = __logger_set()


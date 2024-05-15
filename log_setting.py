from datetime import datetime
import loguru
import logging
from typing import Dict,Any
import sys
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

# S_LOGGING_CONFIG_DEFAULTS: Dict[str, Any] = dict(  # no cov
#     version=1,
#     disable_existing_loggers=False,
#     loggers={
#         "sanic.root": {"level": "INFO", "handlers": ["console"], "propagate": False},
#         "sanic.error": {
#             "level": "INFO",
#             "handlers": ["error_console"],
#             "propagate": False,
#             "qualname": "sanic.error",
#         },
#         "sanic.server": {
#             "level": "INFO",
#             "handlers": ["console"],
#             "propagate": False,
#             "qualname": "sanic.server",
#         },
#     },
#     handlers={
#         "console": {
#             "class": "logger.InterceptHandler",
#         },
#         "error_console": {
#             "class": "logger.InterceptHandler",
#         }
#     }
# )
 
# class InterceptHandler(logging.StreamHandler):
#     def emit(self, record):
#         # Get corresponding Loguru level if it exists
#         try:
#             level = logger.level(record.levelname).name
#         except ValueError:
#             level = record.levelno
#         # Find caller from where originated the logged message
#         frame, depth = logging.currentframe(), 2
#         while frame.f_code.co_filename == logging.__file__:
#             frame = frame.f_back
#             depth += 1

#         msg = self.format(record) # 官方实现中使用record.getMessage()来获取msg，但在sanic中会漏掉它配置过的日志模板，因此要用self.format(record)
#         logger.opt(depth=depth, exception=record.exc_info).log(level, msg)
 
 
# def setup_log():
#     logging.root.handlers = [InterceptHandler()]
#     logging.root.setLevel("DEBUG")
#     for name in logging.root.manager.loggerDict.keys():
#         logging.getLogger(name).handlers = []
#         logging.getLogger(name).propagate = True
#     logger.configure(handlers=[{"sink": sys.stdout, "serialize": False}])

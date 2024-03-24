from loguru import logger
import os
import sys

# 定义日志文件名和轮转时间
LOG_FILE = "translation.log"
ROTATION_TIME = "02:00"

class Logger:
    """
    日志类，用于初始化日志记录器并设置日志等级及输出方式。
    
    参数:
    - name: 日志记录器的名称，默认为"translation"。
    - log_dir: 存放日志文件的目录，默认为"logs"。
    - debug: 是否开启调试模式，默认为False。若为True，日志级别为DEBUG，否则为INFO。
    
    返回值:
    - 无
    """
    def __init__(self, name="translation", log_dir="logs", debug=False):
        # 创建日志目录，如果不存在的话
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file_path = os.path.join(log_dir, LOG_FILE)

        # 移除loguru的默认日志处理器
        logger.remove()

        # 添加控制台处理器，设置特定的日志级别
        level = "DEBUG" if debug else "INFO"
        logger.add(sys.stdout, level=level)
        # 添加文件处理器，设置特定日志级别和定时轮转
        logger.add(log_file_path, rotation=ROTATION_TIME, level="DEBUG")
        self.logger = logger

# 初始化一个调试模式下的日志记录器
LOG = Logger(debug=True).logger

if __name__ == "__main__":
    # 在主程序中初始化并使用日志记录器
    log = Logger().logger

    # 示例：使用不同级别的日志记录
    log.debug("This is a debug message.")
    log.info("This is an info message.")
    log.warning("This is a warning message.")
    log.error("This is an error message.")
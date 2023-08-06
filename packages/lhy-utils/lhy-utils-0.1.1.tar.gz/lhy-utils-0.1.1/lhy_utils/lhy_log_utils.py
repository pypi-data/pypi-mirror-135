# coding: utf-8
import logging
import os
from logging.handlers import RotatingFileHandler


class Logger:
    def __init__(self, log_file=None):
        self.logger = logging.getLogger(os.path.realpath(__file__))
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False
        self.fmt_str = "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d]: %(message)s"
        self.formatter = logging.Formatter(self.fmt_str)
        self.sh = logging.StreamHandler()
        self.sh.setLevel(logging.INFO)
        self.sh.setFormatter(self.formatter)
        self.logger.addHandler(self.sh)
        if log_file:
            self.fh = RotatingFileHandler(log_file, maxBytes=1024 * 1024 * 64, backupCount=10, encoding="utf-8")
            self.fh.setLevel(logging.INFO)
            self.fh.setFormatter(self.formatter)
            self.logger.addHandler(self.fh)

    def get_logger(self):
        return self.logger

    def font_color(self, color):
        # 不同的日志输出不同的颜色
        formatter = logging.Formatter(color % self.fmt_str)
        self.sh.setFormatter(formatter)
        self.logger.addHandler(self.sh)

    # 显示方式（0: 默认; 1: 高亮; 4: 下划线; 5: 闪烁; 7: 反白显示; 8: 隐藏）
    # 前景色（30: 黑色; 31: 红色; 32: 绿色; 33: 黄色; 34: 蓝色; 35: 紫红色; 36: 青蓝色; 37: 白色）
    # 背景色（40: 黑色; 41: 红色; 42: 绿色; 43: 黄色; 44: 蓝色; 45: 紫红色; 46: 青蓝色; 47: 白色）

    def debug(self, message):
        self.font_color('\033[0;32m%s\033[0m')
        self.logger.debug(message)

    def info(self, message):
        self.font_color('\033[0;37m%s\033[0m')
        self.logger.info(message)

    def warning(self, message):
        self.font_color('\033[1;33m%s\033[0m')
        self.logger.warning(message)

    def error(self, message):
        self.font_color('\033[1;31m%s\033[0m')
        self.logger.error(message)
        exit(-1)

    def critical(self, message):
        self.font_color('\033[1;35m%s\033[0m')
        self.logger.critical(message)

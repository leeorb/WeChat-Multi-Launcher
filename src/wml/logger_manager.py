"""
日志管理模块
负责初始化日志系统，提供日志记录功能
"""

import logging
from datetime import datetime
from pathlib import Path

from .constants import (
    LOGS_DIR,
    LOG_PREFIX,
    LOG_DATE_FORMAT,
    LOG_FORMAT,
)


class LoggerManager:
    """日志管理器"""

    def __init__(self, log_dir: Path = LOGS_DIR):
        """
        初始化日志管理器

        Args:
            log_dir: 日志目录路径
        """
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._setup_logger()

    def _setup_logger(self):
        """设置日志系统"""
        # 创建日志文件名，格式：wml_2026-01-27.log
        log_date = datetime.now().strftime(LOG_DATE_FORMAT)
        log_file = self.log_dir / f"{LOG_PREFIX}_{log_date}.log"

        # 配置日志处理器
        handlers = [
            logging.FileHandler(log_file, encoding='utf-8')
        ]

        # 只有在非冻结模式下才输出到控制台
        import sys
        if not hasattr(sys, 'frozen'):
            handlers.append(logging.StreamHandler())

        # 配置日志格式
        logging.basicConfig(
            level=logging.DEBUG,
            format=LOG_FORMAT,
            handlers=handlers
        )

        self.logger = logging.getLogger(__name__)

    def debug(self, message: str):
        """记录 DEBUG 级别日志"""
        self.logger.debug(message)

    def info(self, message: str):
        """记录 INFO 级别日志"""
        self.logger.info(message)

    def warning(self, message: str):
        """记录 WARNING 级别日志"""
        self.logger.warning(message)

    def error(self, message: str):
        """记录 ERROR 级别日志"""
        self.logger.error(message)

    def exception(self, message: str):
        """记录异常信息"""
        self.logger.exception(message)


# 创建全局日志管理器实例
logger = LoggerManager()

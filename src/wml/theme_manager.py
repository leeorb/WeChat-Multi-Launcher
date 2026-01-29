"""
主题管理模块
负责管理应用程序的主题（自动/手动黑白主题）
"""

import darkdetect
from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

from .constants import THEME_AUTO, THEME_LIGHT, THEME_DARK
from .logger_manager import logger


class ThemeManager:
    """主题管理器"""

    def __init__(self, app: QApplication, theme: str = THEME_AUTO):
        """
        初始化主题管理器

        Args:
            app: QApplication 实例
            theme: 主题模式 (auto/light/dark)
        """
        self.app = app
        self.theme = theme
        self.is_dark = False
        self._apply_theme()

    def _apply_theme(self):
        """应用主题"""
        if self.theme == THEME_AUTO:
            # 自动检测系统主题
            self.is_dark = darkdetect.isDark()
        elif self.theme == THEME_DARK:
            self.is_dark = True
        elif self.theme == THEME_LIGHT:
            self.is_dark = False
        else:
            logger.warning(f"未知主题模式: {self.theme}，使用默认主题")
            self.is_dark = False

        self._set_palette()
        logger.info(f"应用主题: {self.theme} (深色模式: {self.is_dark})")

    def _set_palette(self):
        """设置应用程序调色板"""
        palette = QPalette()

        if self.is_dark:
            # 深色主题
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
        else:
            # 浅色主题
            palette.setColor(QPalette.Window, QColor(240, 240, 240))
            palette.setColor(QPalette.WindowText, Qt.black)
            palette.setColor(QPalette.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.black)
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, QColor(240, 240, 240))
            palette.setColor(QPalette.ButtonText, Qt.black)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.white)

        self.app.setPalette(palette)

        # 设置 Fusion 风格
        self.app.setStyle(QStyleFactory.create("Fusion"))

    def set_theme(self, theme: str):
        """
        设置主题模式

        Args:
            theme: 主题模式 (auto/light/dark)
        """
        self.theme = theme
        self._apply_theme()

    def get_theme(self) -> str:
        """
        获取当前主题模式

        Returns:
            主题模式字符串
        """
        return self.theme

    def is_dark_theme(self) -> bool:
        """
        是否为深色主题

        Returns:
            是否为深色主题
        """
        return self.is_dark

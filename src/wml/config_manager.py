"""
配置管理模块
负责配置文件的读写、微信路径检测等
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any

from wml.constants import (
    CONFIG_FILE,
    WECHAT_DEFAULT_PATHS,
    THEME_AUTO,
)
from wml.logger_manager import logger
from wml.registry_utils import get_wechat_path_from_registry


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_file: Path = CONFIG_FILE):
        """
        初始化配置管理器

        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self.config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self):
        """加载配置文件"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                logger.info(f"配置文件加载成功: {self.config_file}")
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"加载配置文件失败: {e}")
                self.config = self._create_default_config()
                self._save_config()
        else:
            logger.info("配置文件不存在，创建默认配置")
            self.config = self._create_default_config()
            self._discover_wechat_path()
            self._save_config()

    def _create_default_config(self) -> Dict[str, Any]:
        """
        创建默认配置

        Returns:
            默认配置字典
        """
        return {
            "wechat_path": "",
            "launch_count": 2,
            "theme": THEME_AUTO,
            "last_launch_status": "",
            "last_error_message": ""
        }

    def _discover_wechat_path(self) -> Optional[str]:
        """
        自动发现微信安装路径

        Returns:
            发现的微信路径，如果未发现则返回 None
        """
        # 1. 尝试从注册表读取
        registry_path = get_wechat_path_from_registry()
        if registry_path:
            self.config["wechat_path"] = registry_path
            return registry_path

        # 2. 尝试默认路径
        for default_path in WECHAT_DEFAULT_PATHS:
            if Path(default_path).exists():
                logger.info(f"找到默认微信路径: {default_path}")
                self.config["wechat_path"] = default_path
                return default_path

        logger.warning("未能自动发现微信路径")
        return None

    def _save_config(self):
        """保存配置文件"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.debug(f"配置文件保存成功: {self.config_file}")
        except IOError as e:
            logger.error(f"保存配置文件失败: {e}")

    def get_wechat_path(self) -> str:
        """获取微信路径"""
        return self.config.get("wechat_path", "")

    def set_wechat_path(self, path: str):
        """设置微信路径"""
        self.config["wechat_path"] = path
        self._save_config()
        logger.info(f"微信路径已更新: {path}")

    def get_launch_count(self) -> int:
        """获取启动数量"""
        return self.config.get("launch_count", 2)

    def set_launch_count(self, count: int):
        """设置启动数量"""
        if count < 1:
            raise ValueError("启动数量必须大于 0")
        self.config["launch_count"] = count
        self._save_config()
        logger.info(f"启动数量已更新: {count}")

    def get_theme(self) -> str:
        """获取主题设置"""
        return self.config.get("theme", THEME_AUTO)

    def set_theme(self, theme: str):
        """设置主题"""
        self.config["theme"] = theme
        self._save_config()
        logger.info(f"主题已更新: {theme}")

    def get_last_launch_status(self) -> str:
        """获取上次启动状态"""
        return self.config.get("last_launch_status", "")

    def set_last_launch_status(self, status: str):
        """设置上次启动状态"""
        self.config["last_launch_status"] = status
        self._save_config()

    def get_last_error_message(self) -> str:
        """获取上次错误信息"""
        return self.config.get("last_error_message", "")

    def set_last_error_message(self, error: str):
        """设置上次错误信息"""
        self.config["last_error_message"] = error
        self._save_config()

    def validate_wechat_path(self, path: str) -> bool:
        """
        验证微信路径是否有效

        Args:
            path: 微信路径

        Returns:
            是否有效
        """
        wechat_path = Path(path)
        if not wechat_path.exists():
            logger.error(f"微信路径不存在: {path}")
            return False

        if not wechat_path.is_file():
            logger.error(f"微信路径不是文件: {path}")
            return False

        if wechat_path.name != "Weixin.exe":
            logger.error(f"微信路径不是 Weixin.exe: {path}")
            return False

        return True

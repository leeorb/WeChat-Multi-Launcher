"""
注册表工具模块
用于从 Windows 注册表中读取微信安装路径
"""

import winreg
from typing import Optional
from pathlib import Path

from .constants import (
    REGISTRY_KEY,
    REGISTRY_VALUE,
)
from .logger_manager import logger


def get_wechat_path_from_registry() -> Optional[str]:
    """
    从注册表中读取微信安装路径

    Returns:
        微信安装路径，如果读取失败则返回 None
    """
    try:
        # 打开注册表键
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_KEY) as key:
            # 读取安装路径值
            install_path, _ = winreg.QueryValueEx(key, REGISTRY_VALUE)

            # 构建完整的微信执行文件路径
            wechat_path = Path(install_path) / "Weixin.exe"

            if wechat_path.exists():
                logger.info(f"从注册表找到微信路径: {wechat_path}")
                return str(wechat_path)
            else:
                logger.warning(f"注册表路径存在但文件不存在: {wechat_path}")
                return None

    except FileNotFoundError:
        logger.debug(f"注册表键不存在: {REGISTRY_KEY}")
        return None
    except OSError as e:
        logger.error(f"读取注册表失败: {e}")
        return None
    except Exception as e:
        logger.error(f"获取微信路径时发生未知错误: {e}")
        return None

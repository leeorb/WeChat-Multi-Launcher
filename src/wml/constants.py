"""
常量定义模块
定义项目中使用的各种常量
"""

import os
from pathlib import Path

# 项目信息
PROJECT_NAME = "WeChat Multi Launcher"
PROJECT_VERSION = "1.0.0"
DEVELOPER = "Lee orb"
REPOSITORY_URL = "https://github.com/leeorb/WeChat-Multi-Launcher"
LICENSE = "MIT License"
LICENSE_URL = "https://github.com/leeorb/WeChat-Multi-Launcher/blob/main/LICENSE"

# 路径常量
import sys

def get_base_dir() -> Path:
    if hasattr(sys, "frozen"):
        return Path(sys._MEIPASS)
    else:
        return Path(__file__).resolve().parent.parent.parent

def get_user_data_dir() -> Path:
    """
    获取用户数据目录（用于配置和日志）
    在冻结模式下，使用用户文档目录
    在开发模式下，使用项目根目录
    """
    if hasattr(sys, "frozen"):
        # 使用用户文档目录
        from pathlib import Path
        import os
        user_dir = Path(os.path.expanduser("~")) / "Documents" / "WeChatMultiLauncher"
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir
    else:
        # 开发模式，使用项目根目录
        return get_base_dir()

BASE_DIR = get_base_dir()
USER_DATA_DIR = get_user_data_dir()

SRC_DIR = BASE_DIR / "src"
CONFIG_DIR = USER_DATA_DIR / "config"
LOGS_DIR = USER_DATA_DIR / "logs"
IMG_DIR = BASE_DIR / "img"

# 配置文件
CONFIG_FILE = CONFIG_DIR / "config.json"

# 图标文件
LOGO_ICON = IMG_DIR / "logo.ico"
WECHAT_ICON = IMG_DIR / "wechat.ico"

# 日志配置
LOG_PREFIX = "wml"
LOG_DATE_FORMAT = "%Y-%m-%d"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# 微信默认安装路径
WECHAT_DEFAULT_PATHS = [
    r"C:\Program Files\Tencent\Weixin\Weixin.exe",
    r"C:\Program Files (x86)\Tencent\Weixin\Weixin.exe",
]

# 注册表路径
REGISTRY_KEY = r"SOFTWARE\Tencent\Weixin"
REGISTRY_VALUE = "InstallPath"

# 进程配置
WECHAT_PROCESS_NAME = "Weixin.exe"
PROCESS_CHECK_DELAY = 2  # 秒

# 主题配置
THEME_AUTO = "auto"
THEME_LIGHT = "light"
THEME_DARK = "dark"

# GUI 配置
WINDOW_TITLE = "微信多开启动器"
WINDOW_MIN_WIDTH = 508
WINDOW_MIN_HEIGHT = 250
WINDOW_DEFAULT_WIDTH = 508
WINDOW_DEFAULT_HEIGHT = 280

# 等待确保配置和日志目录存在
# 注意：只在开发模式或用户数据目录可写时创建
# 在冻结模式下，目录在 get_user_data_dir() 中已经创建
import sys
if not hasattr(sys, "frozen"):
    # 开发模式：创建配置、日志和图片目录
    for directory in [CONFIG_DIR, LOGS_DIR, IMG_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

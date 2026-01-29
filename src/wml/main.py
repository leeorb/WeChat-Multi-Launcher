"""
程序入口
WeChat Multi Launcher 的主程序入口
"""

import sys
import os
import traceback


def find_project_root():
    """
    查找项目根目录
    支持两种环境：
    1. 开发环境：直接运行 Python 脚本
    2. 打包环境：PyInstaller 运行时
    """
    # 方法1: 如果已添加到 sys.path，直接使用
    for path in sys.path:
        if path and os.path.exists(os.path.join(path, 'src', 'wml', 'constants.py')):
            return path

    # 方法2: 从当前文件路径向上查找
    current_file = __file__
    current_dir = os.path.dirname(os.path.abspath(current_file))

    # 向上查找 src 目录
    while current_dir and not os.path.exists(os.path.join(current_dir, 'src')):
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:  # 已经到达根目录
            break
        current_dir = parent_dir

    # 如果找到 src 目录，返回其父目录（项目根目录）
    if os.path.exists(os.path.join(current_dir, 'src')):
        return current_dir

    # 方法3: 使用 os.getcwd() 作为后备
    current_dir = os.getcwd()
    return current_dir


# 初始化路径
project_root = find_project_root()

# 确保项目根目录在 sys.path 中（在导入 wml 模块之前）
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 添加当前目录（src/wml）到 sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from PySide6.QtWidgets import QApplication

# 添加路径到 sys.path
if hasattr(sys, 'frozen'):
    # PyInstaller 环境
    # _MEIPASS 是解压的临时目录
    base_dir = sys._MEIPASS
    sys.path.insert(0, os.path.join(base_dir, 'src'))
else:
    # 开发环境
    sys.path.insert(0, current_dir)
    sys.path.insert(0, os.path.dirname(current_dir))

import wml.constants as constants_module
import wml.logger_manager as logger_module
import wml.gui as gui_module

PROJECT_NAME = constants_module.PROJECT_NAME
PROJECT_VERSION = constants_module.PROJECT_VERSION
logger = logger_module.logger
MainWindow = gui_module.MainWindow


def main():
    """主函数"""
    try:
        logger.info(f"{PROJECT_NAME} v{PROJECT_VERSION} 启动")
        logger.info("=" * 50)

        # 创建 QApplication 实例
        app = QApplication(sys.argv)
        app.setApplicationName(PROJECT_NAME)
        app.setApplicationVersion(PROJECT_VERSION)

        # 创建并显示主窗口
        window = MainWindow(app)
        window.show()

        logger.info("主窗口已显示")

        # 运行应用程序
        exit_code = app.exec()
        logger.info(f"应用程序退出，退出码: {exit_code}")
        return exit_code
    except Exception as e:
        logger.error(f"程序发生未捕获的异常: {e}")
        logger.error(traceback.format_exc())
        return 1


if __name__ == "__main__":
    sys.exit(main())

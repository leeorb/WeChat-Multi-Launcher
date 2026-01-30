import sys
import os
import traceback
import ctypes


# 设置应用程序用户模型ID（AppUserModelID）
# 这对于Windows任务栏正确显示图标至关重要
# 必须在所有Qt导入和QApplication创建之前调用
try:
    app_user_model_id = "github.leeorb.WeChatMultiLauncher"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_user_model_id)
    _app_id_error = None
except Exception as e:
    # 记录错误但不中断程序，后续logger初始化后再输出
    _app_id_error = e


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


def main():
    """主函数"""
    # 延迟导入所有模块
    import wml.constants as constants_module
    import wml.logger_manager as logger_module
    import wml.gui as gui_module

    # 在创建QApplication之前导入Qt模块
    from PySide6.QtWidgets import QApplication
    from PySide6.QtGui import QIcon

    PROJECT_NAME = constants_module.PROJECT_NAME
    PROJECT_VERSION = constants_module.PROJECT_VERSION
    logger = logger_module.logger
    MainWindow = gui_module.MainWindow

    try:
        logger.info(f"{PROJECT_NAME} v{PROJECT_VERSION} 启动")
        logger.info("=" * 50)

        # 输出AppUserModelID设置结果
        if _app_id_error:
            logger.warning(f"设置AppUserModelID失败: {_app_id_error}")
        else:
            logger.info("AppUserModelID设置成功")

        # 创建 QApplication 实例
        app = QApplication(sys.argv)
        app.setApplicationName(PROJECT_NAME)
        app.setApplicationVersion(PROJECT_VERSION)

        # 设置应用程序图标（任务栏和窗口都使用APP_ICON）
        if constants_module.APP_ICON.exists():
            app.setWindowIcon(QIcon(str(constants_module.APP_ICON)))
            logger.info(f"应用程序图标已设置: {constants_module.APP_ICON}")

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

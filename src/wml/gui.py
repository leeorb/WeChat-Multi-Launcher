"""
GUI主界面模块
使用 PySide6 构建应用程序的图形用户界面
"""

# 安全导入webbrowser - 如果失败则使用fallback
try:
    import webbrowser
except ImportError:
    # Fallback: 如果PyInstaller没有正确打包webbrowser，创建一个简单的替代品
    import sys
    import os

    class WebBrowserFallback:
        def open(self, url, new=0):
            if os.name == 'nt':
                os.startfile(url)
            else:
                import subprocess
                if new == 1:
                    subprocess.Popen(['open', url], shell=True)
                else:
                    webbrowser.open(url)

    webbrowser = WebBrowserFallback()

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QSpinBox,
    QGroupBox, QMessageBox, QFileDialog, QApplication,
    QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPalette, QColor

from wml.constants import (
    PROJECT_NAME,
    DEVELOPER,
    REPOSITORY_URL,
    LICENSE_URL,
    LICENSE,
    WINDOW_TITLE,
    WINDOW_MIN_WIDTH,
    WINDOW_MIN_HEIGHT,
    WINDOW_DEFAULT_WIDTH,
    WINDOW_DEFAULT_HEIGHT,
    LOGO_ICON,
    THEME_AUTO,
    THEME_LIGHT,
    THEME_DARK,
)
from wml.logger_manager import logger
from wml.config_manager import ConfigManager
from wml.theme_manager import ThemeManager
from wml.wechat_launcher import WeChatLauncher


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self, app):
        """
        初始化主窗口

        Args:
            app: QApplication 实例
        """
        super().__init__()

        self.app = app
        self.config_manager = ConfigManager()
        self.theme_manager = ThemeManager(app, self.config_manager.get_theme())
        self.launcher = WeChatLauncher()
        self.wechat_launched = False  # 标记是否已成功启动微信

        self._setup_window()
        self._setup_ui()
        self._load_config()

    def _setup_window(self):
        """设置窗口属性"""
        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.resize(WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT)
        # 禁用窗口置顶，确保其他应用窗口可以显示在主窗口上方
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)

        # 设置窗口图标
        try:
            if LOGO_ICON.exists():
                from PySide6.QtGui import QIcon
                self.setWindowIcon(QIcon(str(LOGO_ICON)))
        except Exception as e:
            logger.warning(f"设置窗口图标失败: {e}")

    def _setup_ui(self):
        """设置用户界面"""
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 15, 20, 20)

        # 1. 主程序标题
        title_label = QLabel("微信多开启动器")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # 添加分隔线
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.Shape.HLine)
        separator1.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator1)

        # 2. 配置区域（横向布局，两列）
        config_layout = QHBoxLayout()
        config_layout.setSpacing(15)

        # 2.1 微信路径配置
        path_group = QGroupBox("微信路径")
        path_layout = QHBoxLayout()

        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("请选择微信安装路径...")
        path_layout.addWidget(self.path_edit)

        self.browse_button = QPushButton("浏览...")
        self.browse_button.setFixedWidth(80)
        self.browse_button.clicked.connect(self._on_browse_clicked)
        path_layout.addWidget(self.browse_button)

        path_group.setLayout(path_layout)
        config_layout.addWidget(path_group)

        # 2.2 启动数量配置
        count_group = QGroupBox("启动数量")
        count_layout = QVBoxLayout()

        self.count_spin = QSpinBox()
        self.count_spin.setMinimum(1)
        self.count_spin.setMaximum(100)
        self.count_spin.setValue(2)
        count_layout.addWidget(self.count_spin)

        count_group.setLayout(count_layout)
        config_layout.addWidget(count_group)

        main_layout.addLayout(config_layout)

        # 3. 启动按钮（紧贴配置区域下方）
        self.launch_button = QPushButton("启动微信")
        self.launch_button.setMinimumHeight(60)
        self.launch_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                background-color: #07c160;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 15px 25px;
            }
            QPushButton:hover {
                background-color: #06ad56;
            }
            QPushButton:pressed {
                background-color: #05a04d;
            }
        """)
        self.launch_button.clicked.connect(self._on_launch_clicked)
        main_layout.addWidget(self.launch_button)

        # 4. 按钮栏（主题按钮和关于按钮在启动按钮下方，右对齐）
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        # 主题按钮（固定宽度）
        self.theme_button = QPushButton("主题")
        self.theme_button.setFixedWidth(80)
        self.theme_button.clicked.connect(self._show_theme_menu)
        buttons_layout.addWidget(self.theme_button)

        # 关于按钮（固定宽度）
        self.about_button = QPushButton("关于")
        self.about_button.setFixedWidth(80)
        self.about_button.clicked.connect(self._on_about_clicked)
        buttons_layout.addWidget(self.about_button)

        main_layout.addLayout(buttons_layout)

        # 设置主窗口大小
        self.resize(508, 250)

    def _load_config(self):
        """加载配置到界面"""
        # 加载微信路径
        wechat_path = self.config_manager.get_wechat_path()
        if wechat_path:
            self.path_edit.setText(wechat_path)
        else:
            self.path_edit.setPlaceholderText("请选择微信安装路径...")

        # 加载启动数量
        launch_count = self.config_manager.get_launch_count()
        self.count_spin.setValue(launch_count)

        # 加载主题
        theme = self.config_manager.get_theme()
        self._update_theme_button_text(theme)

    def _on_browse_clicked(self):
        """浏览按钮点击事件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择微信可执行文件",
            "",
            "可执行文件 (*.exe);;所有文件 (*.*)"
        )

        if file_path:
            # 验证路径
            is_valid, error_msg = self.launcher.validate_path(file_path)
            if not is_valid:
                QMessageBox.warning(self, "路径错误", error_msg)
                return

            self.path_edit.setText(file_path)
            self.config_manager.set_wechat_path(file_path)
            logger.info(f"用户选择微信路径: {file_path}")

    def _show_theme_menu(self):
        """显示主题下拉菜单"""
        from PySide6.QtWidgets import QMenu
        from PySide6.QtCore import QPoint

        # 创建菜单
        menu = QMenu(self)

        # 添加菜单项
        auto_action = menu.addAction("自动")
        auto_action.setData(THEME_AUTO)
        light_action = menu.addAction("浅色")
        light_action.setData(THEME_LIGHT)
        dark_action = menu.addAction("深色")
        dark_action.setData(THEME_DARK)

        # 标记当前选中的主题
        current_theme = self.config_manager.get_theme()
        for action in menu.actions():
            if action.data() == current_theme:
                action.setCheckable(True)
                action.setChecked(True)

        # 连接点击事件
        menu.triggered.connect(self._on_theme_action_triggered)

        # 在按钮下方显示菜单
        button_rect = self.theme_button.geometry()
        menu_pos = self.theme_button.mapToGlobal(QPoint(0, button_rect.height()))
        menu.exec_(menu_pos)

    def _on_theme_action_triggered(self, action):
        """主题菜单项被触发"""
        theme = action.data()
        self.theme_manager.set_theme(theme)
        self.config_manager.set_theme(theme)
        self._update_theme_button_text(theme)
        logger.info(f"主题已切换为: {theme}")

    def _update_theme_button_text(self, theme: str):
        """更新主题按钮文本"""
        theme_names = {
            THEME_AUTO: "主题",
            THEME_LIGHT: "浅色",
            THEME_DARK: "深色"
        }
        self.theme_button.setText(theme_names.get(theme, "主题"))

    def _on_theme_changed(self, _index: int):
        """主题改变事件（已废弃，保留兼容性）"""
        pass

    def _on_launch_clicked(self):
        """启动按钮点击事件"""
        wechat_path = self.path_edit.text().strip()
        launch_count = self.count_spin.value()

        # 验证路径
        if not wechat_path:
            QMessageBox.warning(self, "错误", "请先选择微信安装路径！")
            return

        # 验证路径
        is_valid, error_msg = self.launcher.validate_path(wechat_path)
        if not is_valid:
            QMessageBox.warning(self, "路径错误", error_msg)
            return

        # 检查是否有正在运行的微信
        has_running, check_msg = self.launcher.check_running_wechat()
        if has_running:
            QMessageBox.warning(self, "已有微信运行", check_msg)
            return

        # 保存配置
        self.config_manager.set_wechat_path(wechat_path)
        self.config_manager.set_launch_count(launch_count)

        # 禁用启动按钮
        self.launch_button.setEnabled(False)
        self.launch_button.setText("启动中...")
        self.app.processEvents()

        # 启动微信
        success, message = self.launcher.launch(wechat_path, launch_count)

        # 保存启动状态
        self.config_manager.set_last_launch_status("success" if success else "failed")
        self.config_manager.set_last_error_message("" if success else message)

        # 显示结果
        if success:
            # 启动成功，标记为已启动
            self.wechat_launched = True
            # 将主窗口置于后台，让微信窗口显示在上方
            self.showMinimized()
            logger.info(f"启动成功，主窗口已最小化")
            # 给用户一点时间看到微信窗口
            import time
            time.sleep(3)
            self.close()
        else:
            QMessageBox.critical(self, "启动失败", message)
            logger.error(f"启动失败: {message}")
            self.launch_button.setEnabled(True)
            self.launch_button.setText("启动微信")

    def _on_about_clicked(self):
        """关于按钮点击事件"""
        about_text = f"""
        <h2>{PROJECT_NAME}</h2>
        <p><b>开发者:</b> {DEVELOPER}</p>
        <p><b>仓库地址:</b> <a href='{REPOSITORY_URL}'>{REPOSITORY_URL}</a></p>
        <p><b>开源许可:</b> <a href='{LICENSE_URL}'>{LICENSE}</a></p>
        """

        QMessageBox.about(self, "关于", about_text)

    def closeEvent(self, event):
        """窗口关闭事件"""
        # 如果已经成功启动了微信，直接关闭主程序
        # 不要关闭微信进程，因为它们是独立运行的
        if self.wechat_launched:
            logger.info("应用程序关闭（微信已独立运行）")
            event.accept()
        else:
            # 如果没有启动微信，正常关闭
            logger.info("应用程序关闭")
            event.accept()
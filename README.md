# WeChat Multi Launcher

微信多开启动器 - 一个简洁优雅的 Windows 微信多开工具。

## 功能特性

- **一键多开**: 同时启动多个微信实例（1-10个）
- **自动检测**: 自动从注册表和默认路径检测微信安装位置
- **主题切换**: 支持自动/浅色/深色三种主题模式
- **进程验证**: 启动后自动验证微信进程是否正常启动
- **日志记录**: 完整的操作日志，便于排查问题
- **配置持久化**: 配置自动保存，下次启动无需重复设置

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行程序

```bash
python -m src
```

### 打包为可执行文件

```bash
pyinstaller WeChatMultiLauncher.spec
```

打包后的文件位于 `dist/` 目录。

## 项目结构

```
wechat-multilauncher/
├── src/wml/              # 源代码
│   ├── main.py           # 程序入口
│   ├── gui.py            # 主界面
│   ├── wechat_launcher.py # 微信启动逻辑
│   ├── config_manager.py # 配置管理
│   ├── theme_manager.py  # 主题管理
│   ├── process_utils.py  # 进程工具
│   ├── registry_utils.py # 注册表工具
│   ├── logger_manager.py # 日志管理
│   └── constants.py      # 常量定义
├── img/                  # 图标资源
├── config/               # 配置文件（运行时生成）
├── logs/                 # 日志文件（运行时生成）
├── requirements.txt      # 项目依赖
└── README.md             # 项目说明
```

## 配置说明

配置文件位于 `~/Documents/WeChatMultiLauncher/config/config.json`：

```json
{
  "wechat_path": "C:\\Program Files\\Tencent\\Weixin\\Weixin.exe",
  "launch_count": 2,
  "theme": "auto"
}
```
## 日志说明

每次启动或操作都会生成日志，文件按日期命名，位于：

`~/Documents/WeChatMultiLauncher/logs/wml_{date}.log`

其中 `{date}` 表示日志生成日期。

## 依赖

- PySide6 >= 6.6.0 - GUI 框架
- darkdetect >= 0.8.0 - 系统主题检测
- psutil >= 5.9.0 - 进程管理

## 许可证

[MIT License](LICENSE)

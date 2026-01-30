# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 收集所有需要的模块
a = Analysis(
    ['src/wml/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/wml', 'src/wml'),
        ('img/WeChat-Multi-Launcher.ico', 'img'),
    ],
    hiddenimports=[
        'json', 'os', 'sys', 'subprocess', 'webbrowser',
        'darkdetect', 'psutil',
        'PySide6.QtWidgets', 'PySide6.QtCore', 'PySide6.QtGui',
        'wml', 'wml.constants', 'wml.logger_manager', 'wml.gui',
        'wml.theme_manager', 'wml.config_manager', 'wml.wechat_launcher',
        'wml.process_utils', 'wml.registry_utils',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WeChat Multi Launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='img/WeChat-Multi-Launcher.ico',
)

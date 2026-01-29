"""
PyInstaller runtime hook for wml module
"""
# 确保所有标准库模块在PyInstaller打包后可用
import json
import os
import subprocess
import webbrowser

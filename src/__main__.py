"""
包主入口
支持使用 `python -m src` 命令运行程序
"""

import sys
import os

def find_project_root():
    """
    查找项目根目录
    """
    # 方法1: 从当前文件位置向上查找 src 目录
    if __file__ and not __file__.startswith('<'):
        current_file = __file__
        current_dir = os.path.dirname(os.path.abspath(current_file))
        while current_dir and not os.path.exists(os.path.join(current_dir, 'src')):
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:
                break
            current_dir = parent_dir
        if os.path.exists(os.path.join(current_dir, 'src')):
            print(f"找到项目根目录: {current_dir}", file=sys.stderr)
            return current_dir

    # 方法2: 使用 sys.argv[0] 作为后备
    if sys.argv and sys.argv[0]:
        current_file = sys.argv[0]
        if not current_file.startswith('<'):
            current_dir = os.path.dirname(os.path.abspath(current_file))
            while current_dir and not os.path.exists(os.path.join(current_dir, 'src')):
                parent_dir = os.path.dirname(current_dir)
                if parent_dir == current_dir:
                    break
                current_dir = parent_dir
            if os.path.exists(os.path.join(current_dir, 'src')):
                print(f"从 sys.argv 找到项目根目录: {current_dir}", file=sys.stderr)
                return current_dir

    # 方法3: 检查当前工作目录及其父目录（多次）
    cwd = os.getcwd()
    for _ in range(3):  # 最多检查 3 级
        if os.path.exists(os.path.join(cwd, 'src', 'wml')):
            print(f"从 cwd 找到项目根目录: {cwd}", file=sys.stderr)
            return cwd
        parent = os.path.dirname(cwd)
        if parent == cwd:
            break
        cwd = parent

    # 方法4: 检查已知的常见项目结构位置
    known_paths = [
        os.path.abspath('..'),
        os.path.abspath('.'),
    ]

    for path in known_paths:
        if os.path.exists(os.path.join(path, 'src', 'wml')):
            print(f"从 known_paths 找到项目根目录: {path}", file=sys.stderr)
            return path

    # 方法5: 尝试从 PYTHONPATH 中查找
    if 'PYTHONPATH' in os.environ:
        for path in os.environ['PYTHONPATH'].split(os.pathsep):
            if os.path.exists(os.path.join(path, 'src', 'wml')):
                print(f"从 PYTHONPATH 找到项目根目录: {path}", file=sys.stderr)
                return path

    # 方法6: 使用 os.getcwd() 作为最后后备
    print(f"使用 cwd 作为项目根目录: {os.getcwd()}", file=sys.stderr)
    return os.getcwd()

# 添加项目根目录到 sys.path
project_root = find_project_root()
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 打印调试信息
print(f"项目根目录: {project_root}", file=sys.stderr)
print(f"sys.path 前5项: {sys.path[:5]}", file=sys.stderr)
print(f"wml 在 sys.path 中? {'wml' in sys.path}", file=sys.stderr)

# 尝试添加所有可能的路径
import os
for path in [project_root, os.path.join(project_root, 'src'), os.path.join(project_root, 'src', 'wml')]:
    if path and os.path.exists(path):
        if path not in sys.path:
            sys.path.insert(0, path)
            print(f"添加到 sys.path: {path}", file=sys.stderr)

print(f"sys.path 前5项: {sys.path[:5]}", file=sys.stderr)

# 导入主程序
from wml.main import main

if __name__ == "__main__":
    sys.exit(main())
"""
进程工具模块
用于检测系统中的微信进程数量
"""

import psutil
from typing import List

from .constants import WECHAT_PROCESS_NAME
from .logger_manager import logger


def get_wechat_processes() -> List[psutil.Process]:
    """
    获取所有微信进程

    Returns:
        微信进程列表
    """
    wechat_processes = []

    for proc in psutil.process_iter(['name', 'exe']):
        try:
            process_name = proc.info['name']
            if process_name == WECHAT_PROCESS_NAME:
                wechat_processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return wechat_processes


def get_wechat_process_count() -> int:
    """
    获取微信进程数量

    Returns:
        微信进程数量
    """
    count = len(get_wechat_processes())
    logger.debug(f"当前微信进程数量: {count}")
    return count


def kill_wechat_processes() -> bool:
    """
    关闭所有微信进程

    Returns:
        是否成功关闭
    """
    processes = get_wechat_processes()

    if not processes:
        logger.info("没有发现运行的微信进程")
        return True

    success = True
    for proc in processes:
        try:
            proc.kill()
            logger.debug(f"已关闭微信进程 (PID: {proc.pid})")
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            logger.error(f"关闭微信进程失败 (PID: {proc.pid}): {e}")
            success = False

    return success


def get_wechat_executable_paths() -> List[str]:
    """
    获取所有正在运行的微信进程的可执行文件路径

    Returns:
        微信可执行文件路径列表
    """
    paths = []
    for proc in get_wechat_processes():
        try:
            exe_path = proc.exe()
            if exe_path:
                paths.append(exe_path)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return paths

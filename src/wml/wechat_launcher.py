"""
微信启动器模块
负责启动多个微信实例并进行进程校验
"""

import subprocess
import time
from typing import Tuple

from .constants import PROCESS_CHECK_DELAY
from .logger_manager import logger
from .process_utils import get_wechat_process_count


class WeChatLauncher:
    """微信启动器"""

    def __init__(self):
        """初始化微信启动器"""
        pass

    def check_running_wechat(self) -> Tuple[bool, str]:
        """
        检查是否有正在运行的微信进程

        Returns:
            (是否已有微信运行, 提示信息)
        """
        process_count = get_wechat_process_count()

        if process_count > 0:
            msg = f"检测到系统中已有 {process_count} 个微信进程正在运行。\n\n"
            msg += "为了确保多开功能正常使用，请先关闭所有已运行的微信实例。"
            logger.info(f"检测到 {process_count} 个微信进程正在运行")
            return True, msg

        return False, ""

    def launch(self, wechat_path: str, count: int) -> Tuple[bool, str]:
        """
        启动指定数量的微信实例

        Args:
            wechat_path: 微信可执行文件路径
            count: 启动数量

        Returns:
            (是否成功, 错误信息)
        """
        # 首先检查是否有正在运行的微信
        has_running, msg = self.check_running_wechat()
        if has_running:
            return False, msg

        logger.info(f"准备同时启动 {count} 个微信实例，路径: {wechat_path}")

        # 记录启动前的进程数量
        before_count = get_wechat_process_count()
        logger.debug(f"启动前微信进程数量: {before_count}")

        # 启动微信实例
        try:
            self._start_wechat_instances(wechat_path, count)
        except Exception as e:
            error_msg = f"启动微信失败: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

        # 等待进程启动
        logger.info(f"等待 {PROCESS_CHECK_DELAY} 秒以检查进程状态...")
        time.sleep(PROCESS_CHECK_DELAY)

        # 验证进程数量
        after_count = get_wechat_process_count()
        logger.debug(f"启动后微信进程数量: {after_count}")

        expected_count = before_count + count
        if after_count == expected_count:
            success_msg = f"成功启动 {count} 个微信实例（当前总数: {after_count}）"
            logger.info(success_msg)
            return True, success_msg
        else:
            error_msg = (
                f"进程数量验证失败：预期 {expected_count} 个，实际 {after_count} 个。"
                f"可能启动失败或已有进程关闭。"
            )
            logger.error(error_msg)
            return False, error_msg

    def _start_wechat_instances(self, wechat_path: str, count: int):
        """
        同时启动所有微信实例（不延时）

        Args:
            wechat_path: 微信可执行文件路径
            count: 启动数量
        """
        # 使用 subprocess.Popen 创建独立进程
        # 使用 CREATE_NEW_PROCESS_GROUP 和 DETACHED_PROCESS 确保进程独立
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        DETACHED_PROCESS = 0x00000008

        processes = []
        for i in range(count):
            try:
                # 使用 Popen 启动微信，确保进程独立
                # shell=True 确保在 Windows 上正确启动 GUI 应用
                # creationflags 确保进程脱离父进程控制
                proc = subprocess.Popen(
                    [wechat_path],
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    creationflags=CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS,
                    close_fds=True
                )
                processes.append(proc)
                logger.debug(f"已启动第 {i+1}/{count} 个微信实例（使用 Popen，PID: {proc.pid}）")

            except Exception as e:
                logger.error(f"启动第 {i+1} 个微信实例失败: {e}")
                # 清理已启动的进程
                self._cleanup_processes(processes)
                raise Exception(f"启动第 {i+1} 个微信实例失败: {e}")

        logger.info(f"已同时启动 {count} 个微信实例，进程完全独立运行")
        logger.info("使用方法: subprocess.Popen（完全脱离父进程）")

    def _cleanup_processes(self, processes):
        """
        清理已启动的进程（启动失败时调用）

        Args:
            processes: 进程列表
        """
        for proc in processes:
            try:
                proc.kill()
                logger.debug(f"已关闭进程 (PID: {proc.pid})")
            except Exception as e:
                logger.warning(f"关闭进程失败 (PID: {proc.pid}): {e}")

    def validate_path(self, wechat_path: str) -> Tuple[bool, str]:
        """
        验证微信路径是否有效

        Args:
            wechat_path: 微信可执行文件路径

        Returns:
            (是否有效, 错误信息)
        """
        from pathlib import Path

        path = Path(wechat_path)

        if not path.exists():
            return False, "微信路径不存在"

        if not path.is_file():
            return False, "微信路径不是文件"

        if path.name != "Weixin.exe":
            return False, "文件名必须是 Weixin.exe"

        return True, ""

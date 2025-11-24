from clicknium import clicknium as cc
import time
import subprocess
import pyperclip as pc
from datetime import datetime, timedelta
from log import logger


class UI:

    @staticmethod
    def safe_input(locator, text, timeout=3, retry=3, sleep=1):
        """
        通用输入函数：
        - 等待控件出现
        - 自动重试 retry 次
        """
        for attempt in range(1, retry + 1):
            elem = cc.wait_appear(locator, wait_timeout=timeout)
            if elem:
                try:
                    elem.click()
                    time.sleep(0.2)
                    elem.send_hotkey("^a")
                    time.sleep(0.1)
                    elem.send_hotkey("{DEL}")
                    time.sleep(0.1)
                    pc.copy(text)
                    time.sleep(0.1)
                    elem.send_hotkey("^v")
                    time.sleep(0.3)
                    # 校验数据正确性
                    try:
                        val = elem.get_text()
                    except:
                        val = ""

                    if val and str(val).strip() == str(text).strip():
                        return True
                    else:
                        logger.warning(f"[safe_input] 输入校验失败，第{attempt}次，实际值：{val}，期望：{text}")
                        time.sleep(sleep)
                        continue
                except:
                    logger.warning(f"[safe_input] 第 {attempt}/{retry} 次输入失败：{locator}")
                    time.sleep(sleep)
            else:
                logger.warning(f"[safe_input] 第 {attempt}/{retry} 次等待控件失败：{locator}")
                time.sleep(sleep)
        raise Exception(f"[safe_input] 输入失败：无法找到或输入 {locator}，累计尝试 {retry} 次")


    @staticmethod
    def try_click(locator, timeout=3): 
        """ 
        通用：等待点击，出现点击不出现则跳过 
        """ 
        elem = cc.wait_appear(locator, wait_timeout=timeout) 
        if elem: 
            elem.click() 
            time.sleep(1) 
            return True 
        return False


    @staticmethod
    def safe_click(locator, timeout=5, retry=3, sleep=2):
        """
        通用等待点击：
        - 先等待元素出现 timeout 秒
        - 找不到则自动重试 retry 次，每次间隔 sleep 秒
        """
        for attempt in range(1, retry + 1):
            elem = cc.wait_appear(locator, wait_timeout=timeout)
            if elem:
                elem.click()
                time.sleep(1)
                return True
            logger.warning(f"[safe_click] 第 {attempt}/{retry} 次等待失败：未找到元素 {locator}")
            time.sleep(sleep)
        raise Exception(f"[safe_click] 点击失败：无法找到元素 {locator}，累计尝试 {retry} 次")



    @staticmethod
    def wait_loading(locator, timeout=60, interval=3):
        """
        每秒检查一次控件是否还存在
        - timeout：最大检测时间
        - Interval：日志打印等待间隔
        """
        logger.info(f"[wait_loading] 等待加载控件消失...")
        start = time.time()
        next_log_time = start + interval

        while True:
            now = time.time()
            elapsed = int(now - start)
            if elapsed >= timeout:
                logger.error(f"[wait_loading] 加载控件 {locator} 在 {timeout}s 内未消失")
                raise Exception(f"[wait_loading] 加载控件 {locator} 在 {timeout}s 内未消失")
            elem = cc.wait_appear(locator, wait_timeout=1)
            if not elem:
                logger.info("[wait_loading] 加载完成")
                return True
            if now >= next_log_time:
                logger.info(f"[wait_loading] 加载中... 已等待 {elapsed}s")
                next_log_time += interval

    @staticmethod
    def wait_appear_strict(locator, timeout=180, interval=15):
        """
        每秒检查一次控件是否出现
        - timeout：最大检测时间
        - Interval：日志打印等待间隔
        """
        logger.info(f"[wait_appear_strict] 开始等待控件出现...")
        start = time.time()
        next_log_time = start + interval

        while True:
            now = time.time()
            elapsed = int(now - start)
            if elapsed >= timeout:
                logger.error(f"[wait_appear_strict] 控件 {locator} 在 {timeout}s 内未出现")
                raise Exception(f"[wait_appear_strict] 控件 {locator} 在 {timeout}s 内未出现")
            elem = cc.wait_appear(locator, wait_timeout=1)
            if elem:
                logger.info("[wait_appear_strict] 控件已出现")
                return True
            if now >= next_log_time:
                logger.info(f"[wait_appear_strict] 等待中... 已等待 {elapsed}s")
                next_log_time += interval
    
    @staticmethod
    def click_and_wait(click_locator, appear_locator, timeout=10):
        """
        点击控件 + 等待目标控件出现，用于关键跳转动作。
        """
        UI.safe_click(click_locator)
        elem = cc.wait_appear(appear_locator, wait_timeout=timeout)
        if elem:
            return True
        raise Exception(f"[click_and_wait] 点击后未出现目标控件：{appear_locator}")
    
    @staticmethod
    def file_ready(path, retry=5, sleep=1):
        """
        检查文件是否存在/可读（用于下载/导出后）
        """
        import os

        for i in range(retry):
            if os.path.exists(path):
                try:
                    if os.path.getsize(path) > 0:
                        return True
                except:
                    pass
            time.sleep(sleep)
        raise Exception(f"[file_ready] 文件未成功生成：{path}")


    
class Utils:
    
    @staticmethod
    def retry(max_retry=3, delay=3):
        """
        通用重试装饰器：
        - 捕获异常，记录日志
        - 每次失败后强制关闭 Chrome，重新来一轮
        - 重试 max_retry 次后仍失败则抛出异常
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                for attempt in range(1, max_retry + 1):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        logger.error(f"[retry] 第 {attempt}/{max_retry} 次执行失败：{e}")
                        # --- 强制关闭所有 Chrome ---
                        try:
                            Utils.kill_chrome()
                            logger.info("[retry] 已强制关闭 Chrome 进程，准备重试...")
                        except:
                            pass

                        if attempt == max_retry:
                            raise
                        time.sleep(delay)
            return wrapper
        return decorator

    @staticmethod
    def kill_chrome():
        """
        强制关闭所有 Chrome 进程（用于自动化前清理环境）
        """
        try:
            subprocess.call("taskkill /F /IM chrome.exe", shell=True)
            time.sleep(1)
        except:
            pass

    @staticmethod
    def split_date_range():
        """
        返回日期区间列表：
        - 不跨年：[(start, end)]
        - 跨年：[(start, 当年12-31), (次年1-01, end)]
        """
        today = datetime.today()
        start = today - timedelta(days=60)
        start_date = start.date()
        end_date = today.date()
        if start_date.year == end_date.year:
            return [(start_date, end_date)]
        # 跨年（2025-11-11 ~ 2026-01-10：[(2025-11-11, 2025-12-31), (2026-01-01, 2026-01-10)]
        first_end = datetime(start_date.year, 12, 31).date()
        second_start = datetime(end_date.year, 1, 1).date()
        return [(start_date, first_end),(second_start, end_date)]
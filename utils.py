from clicknium import clicknium as cc
import time
import subprocess
import pyperclip as pc
from datetime import datetime, timedelta
from log import logger



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
                time.sleep(0.2)
                return True
            except:
                logger.warning(f"[safe_input] 第 {attempt}/{retry} 次输入失败：{locator}")
                time.sleep(sleep)
        else:
            logger.warning(f"[safe_input] 第 {attempt}/{retry} 次等待控件失败：{locator}")
            time.sleep(sleep)
    raise Exception(f"[safe_input] 输入失败：无法找到或输入 {locator}，累计尝试 {retry} 次")



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


def kill_chrome():
    """
    强制关闭所有 Chrome 进程（用于自动化前清理环境）
    """
    try:
        subprocess.call("taskkill /F /IM chrome.exe", shell=True)
        time.sleep(1)
    except:
        pass


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
    return [
        (start_date, first_end),
        (second_start, end_date)
    ]

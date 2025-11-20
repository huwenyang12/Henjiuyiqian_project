from clicknium import clicknium as cc
import time
import subprocess
import pyperclip as pc


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
                # 复制到剪贴板
                pc.copy(text)
                time.sleep(0.1)
                elem.send_hotkey("^v")
                time.sleep(0.2)
                return True
            except:
                print(f"[safe_input] 第 {attempt}/{retry} 次输入失败：{locator}")
                time.sleep(sleep)
        else:
            print(f"[safe_input] 第 {attempt}/{retry} 次等待控件失败：{locator}")
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
        print(f"[safe_click] 第 {attempt}/{retry} 次等待失败：未找到元素 {locator}")
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


def wait_loading(locator, max_timeout=60):
    """
    每秒检查一次加载控件是否存在
    """
    start = time.time()
    while True:
        elapsed = int(time.time() - start)
        if elapsed >= max_timeout:
            raise Exception(f"[wait_loading] 加载控件 {locator} 在 {max_timeout} 秒内未消失")
        # 每秒检测是否消失
        elem = cc.wait_appear(locator, wait_timeout=1)
        if not elem:
            print("\n[wait_loading] 加载完成")
            return True
        print(f"\r[wait_loading] 加载中... {elapsed}s", end="")



def wait_appear_strict(locator, timeout=180):
    """
    每秒检查一次控件是否出现
    """
    print(f"[wait_appear_strict] 开始等待控件出现：{locator}")
    start = time.time()
    while True:
        elapsed = int(time.time() - start)
        if elapsed >= timeout:
            raise Exception(f"[wait_appear_strict] 控件 {locator} 在 {timeout} 秒内未出现")
        # 检测是否出现
        elem = cc.wait_appear(locator, wait_timeout=1)
        if elem:
            print(f"\n[wait_appear_strict] 控件已出现")
            return elem
        print(f"\r[wait_appear_strict] 等待中... {elapsed}s", end="")


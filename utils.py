from clicknium import clicknium as cc
import time

def safe_input(locator, text, timeout=3, retry=3, sleep=1):
    """
    通用输入函数：
    - 等待控件出现
    - 清空后输入文字
    - 自动重试 retry 次
    - 重试仍失败则抛异常
    """
    for attempt in range(1, retry + 1):
        elem = cc.wait_appear(locator, wait_timeout=timeout)
        if elem:
            try:
                elem.set_text("") 
                time.sleep(0.3)
                elem.set_text(text)
                time.sleep(0.3)
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



def safe_click(locator, timeout=3, retry=3, sleep=1):
    """
    通用等待点击：
    - 先等待元素出现 timeout 秒
    - 找不到则自动重试 retry 次，每次间隔 sleep 秒
    - 每次失败打印attempt日志
    - 仍找不到则抛异常
    """
    for attempt in range(1, retry + 1):
        elem = cc.wait_appear(locator, wait_timeout=timeout)
        if elem:
            elem.click()
            time.sleep(0.5)
            return True
        print(f"[safe_click] 第 {attempt}/{retry} 次等待失败：未找到元素 {locator}")
        time.sleep(sleep)
    raise Exception(f"[safe_click] 点击失败：无法找到元素 {locator}，累计尝试 {retry} 次")

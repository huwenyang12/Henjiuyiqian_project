from clicknium import clicknium as cc, locator, ui
import yaml
import os
import time

from utils import safe_input, try_click, safe_click

# 读取 config.yaml 配置
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.yaml")

with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

class Browser:

    def __init__(self):
        # 打开系统主页面
        self.url = cfg["system"]["base_url"]
        self.downloads_dir = cfg["system"]["download_dir"]
        os.makedirs(self.downloads_dir, exist_ok=True)

    # ==================== 执行登录操作 ==================== 
    def login(self):
        try:
            # 打开浏览器
            print("正在打开控制台网页...")
            self.tab = cc.chrome.open(self.url)
            try_click(locator.login.button_接受,timeout=2)
            # 判断是否登录
            ele_logo = cc.wait_appear(locator.login.Logo, wait_timeout=3)
            if ele_logo:
                print("已在控制台页面，无需登录")
                return
            print("正在进行登录...")
            safe_input(locator.login.login_username, cfg["login"]["username"])
            safe_input(locator.login.login_password, cfg["login"]["password"])
            safe_click(locator.login.button_登录)
            time.sleep(2)
            ele_logo_after = cc.wait_appear(locator.login.Logo, wait_timeout=5)
            print("登录成功!" if ele_logo_after else "登录失败!")
        except Exception as e:
            print(f"进入登录失败：{e}")
            raise

    # ==================== 进入查询页面 ==================== 
    def goto_query(self):
        try:
            print("正在进入序时帐查询页面...")
            safe_click(locator.query.首页_全局导航)
            safe_click(locator.query.span_财务会计)
            safe_click(locator.query.span_序时账)
            time.sleep(3)
            return
        except Exception as e:
            print(f"进入序时账查询页面失败：{e}")
            raise

    # ==================== 执行查询序时账 ==================== 
    def run_query(self):
        try:
            print("正在筛选账簿列表...")
            safe_click(locator.query.button_查询)
            safe_click(locator.query.账簿勾选)
            time.sleep(1)
            cc.find_element(locator.query.tab_我的收藏).double_click()
            time.sleep(2)
            safe_click(locator.query.button_全部选择)
            safe_click(locator.query.button_确定)

            print("正在填写查找日期...")
            safe_input(locator.query.input_开始日期, "2025-11-19")
            safe_input(locator.query.input_结束日期, "2025-12-19")
            time.sleep(1)
            cc.send_hotkey("{ENTER}")

        except Exception as e:
            print(f"查询序时账失败：{e}")
            raise

    # ==================== 导出 Excel ==================== 
    def export_excel(self):
        selectors = cfg["query"]["selectors"]

        # 点击导出 Excel
        cc.find_element(selectors["export_button"]).click()

        # 等待文件下载（假设下载到系统默认目录）
        time.sleep(3)

        # ⚠️ Clicknium 没有 playwright 那种 download hook
        # 这里一般需要自己从默认 download 目录找最新文件
        # 这里先示例用 downloads_dir 不动

        # TODO: 你后续告诉我系统下载目录，我可以自动检测
        return None

    # ==================== 关闭浏览器 ==================== 
    def close(self):
        try:
            self.tab.close()
            print("浏览器已关闭!")
        except:
            pass

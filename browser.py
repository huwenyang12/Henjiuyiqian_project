from clicknium import clicknium as cc, locator, ui
from datetime import datetime, timedelta
import yaml
import os
import time

from utils import safe_input, try_click, safe_click, kill_chrome

# 读取配置
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
            # # 清理进程
            # kill_chrome()

            # 打开浏览器
            print("正在打开控制台网页...")
            self.tab = cc.chrome.open(self.url)
            try_click(locator.login.button_接受,timeout=2)

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
            print("正在进入序时账查询页面...")
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
            # TODO: 账簿少一个 00030-0005
            safe_click(locator.query.button_查询)
            safe_click(locator.query.账簿勾选)
            time.sleep(1)
            cc.find_element(locator.query.tab_我的收藏).double_click()
            time.sleep(2)
            safe_click(locator.query.button_全部选择)
            safe_click(locator.query.button_确定)

            print("正在填写查找日期...")
            # 开始日期：今天。结束日期：今天+60天
            # start_date = datetime.today().strftime("%Y-%m-%d")
            # TODO: 起止日期跨度不能跨年
            end_date = (datetime.today() + timedelta(days=30)).strftime("%Y-%m-%d")
            safe_click(locator.query.锚点_今天)
            # safe_input(locator.query.input_开始日期, start_date)
            safe_input(locator.query.input_结束日期, end_date)
            time.sleep(1)
            cc.send_hotkey("{ENTER}")

            print("正在筛选会计科目...")
            safe_click(locator.query.div_会计科目)
            safe_click(locator.query.div_会计科目_介于)
            safe_input(locator.query.会计科目_编码名称1,"主营业务收入")
            safe_input(locator.query.会计科目_编码名称2,"以前年度损益调整")
            cc.send_hotkey("{ENTER}")
            time.sleep(1)
            safe_click(locator.query.span_显示对方科目)
            safe_click(locator.query.span_全景查询)

            safe_click(locator.query.button_提交查询)
            return 

        except Exception as e:
            print(f"查询序时账失败：{e}")
            raise

    # ==================== 导出 Excel ==================== 
    def save_to_excel(self):
        try:
            print("正在进行导出序时账为Excel表...")
            safe_click(locator.download.button_导出)
            safe_click(locator.download.li_导出excel)
            safe_click(locator.download.span_原始数据导出)
            safe_click(locator.download.button_确定导出)

            filename = f"序时账_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            full_path = os.path.join(self.downloads_dir, filename)

            path_box = cc.wait_appear(locator.download.window_另存为, wait_timeout=15)
            if not path_box:
                print("路径输入框未找到")
                return
            safe_input(locator.download.win_input_文件名, full_path)
            time.sleep(1)
            safe_click(locator.download.win_button_保存)
            print(f"Excel 已成功保存到：{full_path}")
            return
        except Exception as e:
            print(f"导出序时账失败：{e}")
            raise

    # ==================== 关闭浏览器 ==================== 
    def close(self):
        try:
            num = 5
            for i in range(num, 0, -1):
                print(f"\r浏览器将在 {i} 秒后关闭...", end="", flush=True)
                time.sleep(1)
            print("\r正在关闭浏览器...        ")
            self.tab.close()
            print("浏览器已关闭!")
            return
        except Exception as e:
            print(f"\n关闭浏览器时发生异常：{e}")


from clicknium import clicknium as cc, locator, ui
from datetime import datetime, timedelta
import yaml
import os
import time

from utils import safe_input, try_click, safe_click, kill_chrome, wait_loading, wait_appear_strict, split_date_range

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.yaml")

with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

class Browser:

    def __init__(self):
        self.url = cfg["system"]["base_url"]
        self.downloads_dir = cfg["system"]["download_dir"]
        os.makedirs(self.downloads_dir, exist_ok=True)

    # ==================== 执行登录操作 ==================== 
    def login(self):
        try:
            # # 清理进程
            # kill_chrome()

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
        except Exception as e:
            print(f"进入序时账查询页面失败：{e}")
            raise

    # ==================== 执行查询序时账 ==================== 
    def run_query(self, start_date, end_date):
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

            safe_click(locator.query.锚点_今天)
            safe_input(locator.query.input_开始日期, start_date.strftime("%Y-%m-%d"))
            safe_input(locator.query.input_结束日期, end_date.strftime("%Y-%m-%d"))
            time.sleep(1)
            cc.send_hotkey("{ENTER}")
            safe_click(locator.query.锚点_期间)


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

        except Exception as e:
            print(f"查询序时账失败：{e}")
            raise

    # ==================== 导出 Excel ==================== 
    def save_to_excel(self):
        try:
            wait_loading(locator.download.div_加载中)
        
            print("正在进行导出序时账为Excel表...")
            safe_click(locator.download.button_导出)
            safe_click(locator.download.li_导出excel)
            safe_click(locator.download.span_原始数据导出)
            safe_click(locator.download.button_确定导出)

            filename = f"序时账_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            full_path = os.path.join(self.downloads_dir, filename)

            wait_appear_strict(locator.download.window_另存为)

            safe_input(locator.download.win_input_文件名, full_path)
            time.sleep(1)
            safe_click(locator.download.win_button_保存)
            print(f"Excel 已成功保存到：{full_path}")
            return full_path
        except Exception as e:
            print(f"导出序时账失败：{e}")
            raise
    
    # ==================== 条件执行查找 ==================== 
    def run_all_queries(self):
        date_ranges = split_date_range()
        # 测试
        # date_ranges = date_ranges = [(datetime(2024, 11, 11).date(), datetime(2024, 12, 31).date()),(datetime(2025, 1, 1).date(), datetime(2025, 1, 10).date())]
        total = len(date_ranges)

        print(f"\n本次需要执行 {total} 段查询\n")
        
        for idx, (start_date, end_date) in enumerate(date_ranges, start=1):
            if idx != 1:
                print("[刷新等待6s...]")
                elem = cc.find_element(locator.download.p_序时账)
                elem.click("right")
                safe_click(locator.download.div_刷新)
                time.sleep(6)

            print(f"--- 开始第 {idx} 段查询 ---")
            print(f"日期范围：{start_date} 至 {end_date}")
            # 执行查询
            self.run_query(start_date, end_date)
            print("查询完成，正在导出 Excel...")
            # 导出
            self.save_to_excel()
            print(f"第 {idx} 段导出完成\n")
            
        print("所有查询与导出已完成。")

    # ==================== 关闭浏览器 ==================== 
    def close(self):
        try:
            num = 5
            for i in range(num, 0, -1):
                print(f"\r浏览器将在 {i} 秒后关闭...", end="", flush=True)
                time.sleep(1)
            print("\r正在关闭浏览器...        ")
            self.tab.close()
            print("浏览器已关闭。")
        except Exception as e:
            print(f"\n关闭浏览器时发生异常：{e}")


from clicknium import clicknium as cc, locator, ui
from datetime import datetime
import yaml, os, time
from log import logger 
from utils import Utils, UI

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.yaml")
with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

class Browser:
    def __init__(self):
        self.url = cfg["system"]["base_url"]
        # 添加执行目录
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        self.task_folder = os.path.join(cfg["system"]["download_dir"], ts)
        os.makedirs(self.task_folder, exist_ok=True)

    # ==================== 执行登录操作 ==================== 
    def login(self):
        try:
            # # 清理进程
            # Utils.kill_chrome()

            logger.info("正在打开控制台网页...")
            self.tab = cc.chrome.open(self.url)
            UI.try_click(locator.login.button_接受,timeout=2)
            ele_logo = cc.wait_appear(locator.login.Logo, wait_timeout=1)
            if ele_logo:
                logger.info("已在控制台页面，无需登录")
                return
            logger.info("正在进行登录...")
            UI.safe_input(locator.login.login_username, cfg["login"]["username"])
            UI.safe_input(locator.login.login_password, cfg["login"]["password"])
            UI.click_and_wait(locator.login.button_登录, locator.login.Logo)
            UI.wait_loading(locator.download.div_加载中)
            logger.info("登录成功！")
        except Exception as e:
            logger.error(f"进入登录失败：{e}")
            raise

    # ==================== 进入查询页面 ==================== 
    def goto_query(self):
        try:
            logger.info("正在进入序时账查询页面...")
            UI.safe_click(locator.query.首页_全局导航)
            UI.safe_click(locator.query.span_财务会计)
            UI.click_and_wait(locator.query.span_序时账, locator.query.button_查询)
        except Exception as e:
            logger.error(f"进入序时账查询页面失败：{e}")
            raise
    
    # ==================== 条件执行查找 ==================== 
    def run_queries(self):
        date_ranges = Utils.split_date_range()
        # # test
        # date_ranges = date_ranges = [(datetime(2024, 12, 21).date(), datetime(2024, 12, 31).date()),(datetime(2025, 1, 1).date(), datetime(2025, 1, 10).date())]
        total = len(date_ranges)
        result_list = []

        logger.info(f"本次需要执行 {total} 段查询")
        
        for idx, (start_date, end_date) in enumerate(date_ranges, start=1):
            if idx != 1:
                logger.info("刷新等待 6 秒...")
                elem = cc.find_element(locator.download.p_序时账)
                elem.click("right")
                UI.safe_click(locator.download.div_刷新)
                time.sleep(6)

            logger.info(f"开始第 {idx} 段查询：{start_date} 至 {end_date}")
            self.run_query(start_date, end_date)

            logger.info("查询完成，正在导出 Excel...")
            file_path = self.save_to_excel()
            logger.info(f"第 {idx} 段导出完成")

            download_time = os.path.basename(file_path).replace(".xlsx", "")
            result_list.append({
                "data_folder": self.task_folder,
                "download_time": download_time,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d")
            })

        logger.info("所有查询与导出已完成。")
        return result_list
    
    # ==================== 导出 Excel ==================== 
    def save_to_excel(self):
        try:
            UI.wait_loading(locator.download.div_加载中)
            logger.info("正在导出序时账为 Excel ...")
            UI.safe_click(locator.download.button_导出)
            UI.safe_click(locator.download.li_导出excel)
            UI.safe_click(locator.download.span_原始数据导出)
            UI.safe_click(locator.download.button_确定导出)
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
            full_path = os.path.join(self.task_folder, filename)
            UI.wait_appear_strict(locator.download.window_另存为)
            UI.safe_input(locator.download.win_input_文件名, full_path)
            time.sleep(1)
            UI.safe_click(locator.download.win_button_保存)
            UI.file_ready(full_path)
            logger.info(f"Excel 已成功保存到：{full_path}")
            return full_path
        except Exception as e:
            logger.error(f"导出序时账失败：{e}")
            raise

    # ==================== 关闭浏览器 ==================== 
    def close(self):
        try:
            logger.info(f"浏览器将在 5 秒后关闭...")
            time.sleep(5)                
            self.tab.close()
            logger.info("浏览器已关闭。")
        except Exception as e:
            logger.error(f"关闭浏览器时发生异常：{e}")

    # ==================== 执行查询序时账 ==================== 
    def run_query(self, start_date, end_date):
        try:
            time.sleep(5)
            logger.info("正在筛选账簿列表...")
            self.select_ledgers()
            logger.info("正在填写查找日期范围...")
            self.fill_date_range(start_date, end_date)
            logger.info("正在筛选会计科目...")
            self.select_subjects()
            logger.info("正在选择币种...")
            self.select_currency()
            logger.info("正在提交查询...")
            self.submit_query()
        except Exception as e:
            logger.error(f"查询序时账失败：{e}")
            raise

    def select_ledgers(self):
        UI.safe_click(locator.query.button_查询)
        UI.safe_click(locator.query.账簿勾选)
        time.sleep(0.5)
        UI.click_and_wait(locator.query.tab_我的收藏, locator.query.button_全部选择)
        time.sleep(2)
        UI.safe_click(locator.query.button_全部选择)
        UI.safe_click(locator.query.button_确定)

    def fill_date_range(self, start_date, end_date):
        UI.safe_click(locator.query.锚点_今天)
        UI.safe_input(locator.query.input_开始日期, start_date.strftime("%Y-%m-%d"))
        UI.safe_input(locator.query.input_结束日期, end_date.strftime("%Y-%m-%d"))
        cc.send_hotkey("{ENTER}")
        UI.safe_click(locator.query.锚点_期间)

    def select_subjects(self):
        UI.safe_click(locator.query.div_会计科目)
        UI.safe_click(locator.query.div_会计科目_介于)
        UI.safe_input(locator.query.会计科目_编码名称1, "主营业务收入")
        UI.safe_input(locator.query.会计科目_编码名称2, "以前年度损益调整")
        cc.send_hotkey("{ENTER}")
        time.sleep(0.5)
        UI.safe_click(locator.query.span_显示对方科目)
        UI.safe_click(locator.query.span_全景查询)

    def select_currency(self):
        UI.safe_click(locator.query.div_币种范围)
        UI.safe_click(locator.query.li_人民币)
        UI.safe_click(locator.query.button_确定_币种)

    def submit_query(self):
        UI.click_and_wait(locator.query.button_提交查询, locator.download.button_导出)


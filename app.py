from browser import Browser
from log import logger
from utils import Utils
from db import main as insert_db

@Utils.retry
@Utils.task_log
def run():
    obj = Browser()

    obj.login()
    obj.goto_query()

    results  = obj.run_queries()

    obj.close()

    for item in results:
        print("开始入库...")
        insert_db(**item)
    logger.info("所有 Excel 已入库完成")

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        logger.error(f"【主流程运行失败】：{e}")

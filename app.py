from browser import Browser
from log import logger
from utils import Utils
from db import main as insert_db


@Utils.retry
def run_query():
    recorder = Utils.start_recorder()
    obj = Browser()
    try:
        obj.login()
        obj.goto_query()
        return obj.run_queries()
    except Exception as e:
        # 调用异常截图
        pass
    finally:
        Utils.stop_recorder(recorder)
        obj.close()
        
@Utils.task_log
def main():
    for item in run_query():
        insert_db(**item)
    logger.info("所有 Excel 已入库完成")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"【主流程运行失败】：{e}")

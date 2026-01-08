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
        Utils.take_screenshot()
        raise
    finally:
        Utils.stop_recorder(recorder)
        obj.close()
        
@Utils.task_log
def main():
    results = run_query()
    if not results:
        logger.info("没有数据需要入库")
        return

    # 合并两段的删除范围
    data_folder = results[0]["data_folder"]
    start_date = min(r["start_date"] for r in results)
    end_date   = max(r["end_date"] for r in results)

    insert_db(
        data_folder=data_folder,
        download_time=results[0]["download_time"],
        start_date=start_date,
        end_date=end_date,
    )
    logger.info("所有 Excel 已入库完成")



if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"【主流程运行失败】：{e}")

from browser import Browser
from log import logger
from utils import Utils

@Utils.retry()
def run():
    obj = Browser()

    obj.login()
    
    obj.goto_query()

    obj.run_queries()

    # # TODO: 解析入库

    obj.close()


if __name__ == "__main__":
    try:
        logger.info("")
        logger.info("【开始执行任务】")
        run()
        logger.info("【任务执行结束】")
    except Exception as e:
        logger.error(f"【任务执行失败】：{e}")

from browser import Browser
from log import logger
from utils import Utils

@Utils.retry
@Utils.task_log
def run():
    obj = Browser()

    obj.login()
    
    obj.goto_query()

    obj.run_queries()

    # # TODO: 解析入库

    obj.close()


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        logger.error(f"【主流程运行失败】：{e}")

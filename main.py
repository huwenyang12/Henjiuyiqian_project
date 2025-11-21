from browser import Browser
from log import logger

def run():
    obj = Browser()

    obj.login()
    
    obj.goto_query()

    obj.run_all_queries()

    obj.close()

if __name__ == "__main__":
    try:
        logger.info("")
        logger.info("开始执行任务")
        run()
        logger.info("任务执行完成！")
    except Exception as e:
        logger.error(f"任务失败：{e}")

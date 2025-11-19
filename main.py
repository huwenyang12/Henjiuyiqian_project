from browser import Browser
import time
def run():
    obj = Browser()

    # 登录
    obj.login()

    # 进入查找
    obj.goto_query()

    # 查找过程
    obj.run_query()
    
    # 关闭页面
    time.sleep(10)
    obj.close()

if __name__ == "__main__":
    run()

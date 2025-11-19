from browser import Browser
import time
def run():
    obj = Browser()

    obj.login()

    obj.goto_query_page()
    # obj.run_query()
    # file = obj.export_excel()
    # print("导出文件：", file)

    # obj.close()

if __name__ == "__main__":
    run()

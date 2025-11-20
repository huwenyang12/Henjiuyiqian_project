from browser import Browser
def run():
    obj = Browser()

    # 登录
    obj.login()
    # 进入查找
    obj.goto_query()
    # 查找过程
    obj.run_query()
    # 导出Excel表
    obj.save_to_excel()
    # # 关闭页面
    # obj.close()

if __name__ == "__main__":
    try:
        print("开始执行任务")
        run()
        print("任务执行完成！")
    except Exception as e:
        print(f"任务失败：{e}")

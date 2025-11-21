from browser import Browser

def run():
    obj = Browser()

    obj.login()

    obj.goto_query()

    obj.run_all_queries()

    obj.close()

if __name__ == "__main__":
    try:
        print("开始执行任务")
        run()
        print("任务执行完成！")
    except Exception as e:
        print(f"任务失败：{e}")
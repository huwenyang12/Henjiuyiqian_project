# Clicknium 操作常用指南

本文档提供 Clicknium 自动化操作的常用示例，涵盖浏览器操作、元素定位、输入输出、验证码处理等场景，适用于初学者和进阶用户。代码以京东登录为例，展示实际应用。

------

## 目录

- [1. 环境准备](https://grok.com/chat/d5db9aa9-301d-412b-a533-46a6c0b048ba#1-环境准备)
- [2. 浏览器操作](https://grok.com/chat/d5db9aa9-301d-412b-a533-46a6c0b048ba#2-浏览器操作)
- [3. 元素定位与基本操作](https://grok.com/chat/d5db9aa9-301d-412b-a533-46a6c0b048ba#3-元素定位与基本操作)
- [4. 点击操作](https://grok.com/chat/d5db9aa9-301d-412b-a533-46a6c0b048ba#4-点击操作)
- [5. 文本输入操作](https://grok.com/chat/d5db9aa9-301d-412b-a533-46a6c0b048ba#5-文本输入操作)
- [6. 下拉框操作](https://grok.com/chat/d5db9aa9-301d-412b-a533-46a6c0b048ba#6-下拉框操作)
- [7. 表格操作](https://grok.com/chat/d5db9aa9-301d-412b-a533-46a6c0b048ba#7-表格操作)
- [8. 文件操作](https://grok.com/chat/d5db9aa9-301d-412b-a533-46a6c0b048ba#8-文件操作)
- [9. 窗口与标签页操作](https://grok.com/chat/d5db9aa9-301d-412b-a533-46a6c0b048ba#9-窗口与标签页操作)
- [10. 等待与异常处理](https://grok.com/chat/d5db9aa9-301d-412b-a533-46a6c0b048ba#10-等待与异常处理)
- [11. 元素属性与状态](https://grok.com/chat/d5db9aa9-301d-412b-a533-46a6c0b048ba#11-元素属性与状态)
- [12. 截图与高亮](https://grok.com/chat/d5db9aa9-301d-412b-a533-46a6c0b048ba#12-截图与高亮)
- [13. JavaScript 执行](https://grok.com/chat/d5db9aa9-301d-412b-a533-46a6c0b048ba#13-javascript-执行)
- [14. 配置文件支持](https://grok.com/chat/d5db9aa9-301d-412b-a533-46a6c0b048ba#14-配置文件支持)
- [15. 日志记录](https://grok.com/chat/d5db9aa9-301d-412b-a533-46a6c0b048ba#15-日志记录)
- [16. 验证码处理](https://grok.com/chat/d5db9aa9-301d-412b-a533-46a6c0b048ba#16-验证码处理)
- [17. 完整登录示例（以京东为例）](https://grok.com/chat/d5db9aa9-301d-412b-a533-46a6c0b048ba#17-完整登录示例以京东为例)

------

## 1. 环境准备

确保已安装以下工具：

- Python 3.7+（建议 3.9 或 3.10）
- Clicknium：`pip install clicknium`
- VSCode 及 Clicknium 扩展
- 浏览器驱动（如 Chrome WebDriver，Clicknium 自动管理）

在 VSCode 中打开 Clicknium 扩展，点击 **Capture** 启动录制器，捕获控件并生成代码。

------

## 2. 浏览器操作

```python
import time
from clicknium import clicknium as cc, locator

def browser_operations():
    """浏览器基本操作"""
    # 打开浏览器
    tab = cc.chrome.open("https://www.example.com")
    # 支持其他浏览器
    # tab = cc.edge.open("https://www.example.com")
    # tab = cc.firefox.open("https://www.example.com")
    
    # 浏览器窗口操作
    tab.maximize()          # 最大化
    tab.minimize()          # 最小化
    tab.set_window_size(1920, 1080)  # 设置窗口大小
    
    # 页面导航
    tab.goto("https://www.baidu.com")
    tab.back()              # 后退
    tab.forward referencias

    # 获取页面信息
    title = tab.title       # 获取标题
    url = tab.url          # 获取当前URL
    
    # 关闭浏览器
    tab.close()
    
    print(f"页面标题: {title}")
    print(f"页面URL: {url}")
```

------

## 3. 元素定位与基本操作

```python
def element_operations():
    """元素定位和基本操作"""
    tab = cc.chrome.open("https://www.example.com")
    
    # 等待元素出现
    tab.wait_appear(locator.example.button_login, timeout=10)
    
    # 查找单个元素
    element = tab.find_element(locator.example.button_login)
    
    # 查找多个元素
    elements = tab.find_elements(locator.example.list_items)
    
    # 检查元素是否存在
    try:
        element = tab.find_element(locator.example.button_login)
        print("元素存在")
    except:
        print("元素不存在")
    
    # 等待元素消失
    tab.wait_disappear(locator.example.loading_spinner, timeout=10)
```

------

## 4. 点击操作

```python
def click_operations():
    """各种点击操作"""
    tab = cc.chrome.open("https://www.example.com")
    
    # 基本点击
    tab.click(locator.example.button_submit)
    
    # 通过元素对象点击
    element = tab.find_element(locator.example.button_submit)
    element.click()
    
    # 不同类型的点击
    element.click(by="center")      # 点击中心（默认）
    element.click(by="coordinate")  # 坐标点击
    element.click(by="js")          # JavaScript点击
    
    # 右键点击
    element.right_click()
    
    # 双击
    element.double_click()
    
    # 点击指定坐标
    element.click(offset_x=10, offset_y=20)
```

------

## 5. 文本输入操作

```python
from clicknium.common import Keys

def text_input_operations():
    """文本输入相关操作"""
    tab = cc.chrome.open("https://www.example.com")
    
    # 基本文本输入
    tab.find_element(locator.example.input_username).set_text("admin")
    
    # 清空后输入
    input_element = tab.find_element(locator.example.input_username)
    input_element.clear_text()
    input_element.set_text("new_username")
    
    # 获取输入框文本
    text = input_element.get_text()
    print(f"输入框内容: {text}")
    
    # 追加文本
    input_element.set_text("additional_text", clear=False)
    
    # 模拟键盘输入
    input_element.send_keys("Hello World")
    input_element.send_keys(Keys.ENTER)  # 按回车
    input_element.send_keys(Keys.TAB)    # 按Tab键
    
    # 组合键
    input_element.send_keys(Keys.CTRL + "a")  # Ctrl+A全选
    input_element.send_keys(Keys.CTRL + "c")  # Ctrl+C复制
```

------

## 6. 下拉框操作

```python
def dropdown_operations():
    """下拉框操作"""
    tab = cc.chrome.open("https://www.example.com")
    
    # 通过文本选择
    dropdown = tab.find_element(locator.example.select_country)
    dropdown.select_item("China")
    
    # 通过索引选择
    dropdown.select_item(2)
    
    # 通过值选择
    dropdown.select_item_by_value("cn")
    
    # 获取选中项
    selected_text = dropdown.get_selected_item()
    print(f"选中项: {selected_text}")
    
    # 获取所有选项
    options = dropdown.get_options()
    for option in options:
        print(f"选项: {option}")
```

------

## 7. 表格操作

```python
def table_operations():
    """表格操作"""
    tab = cc.chrome.open("https://www.example.com")
    
    # 获取表格
    table = tab.find_element(locator.example.table_data)
    
    # 获取表格行数
    rows = table.find_elements(locator.example.table_rows)
    print(f"表格行数: {len(rows)}")
    
    # 遍历表格数据
    for i, row in enumerate(rows):
        cells = row.find_elements(locator.example.table_cells)
        row_data = [cell.get_text() for cell in cells]
        print(f"第{i+1}行: {row_data}")
    
    # 点击特定单元格
    specific_cell = table.find_element(locator.example.cell_edit_button)
    specific_cell.click()
```

------

## 8. 文件操作

```python
def file_operations():
    """文件上传下载操作"""
    tab = cc.chrome.open("https://www.example.com")
    
    # 文件上传
    file_input = tab.find_element(locator.example.input_file)
    file_input.set_files(r"C:\path\to\your\file.txt")
    
    # 多文件上传
    file_input.set_files([
        r"C:\path\to\file1.txt",
        r"C:\path\to\file2.txt"
    ])
    
    # 文件下载（通过点击下载链接）
    tab.click(locator.example.link_download)
    
    # 等待下载完成
    time.sleep(5)
```

------

## 9. 窗口与标签页操作

```python
def window_tab_operations():
    """窗口和标签页操作"""
    # 打开多个标签页
    tab1 = cc.chrome.open("https://www.example1.com")
    tab2 = cc.chrome.open("https://www.example2.com")
    
    # 切换标签页
    tab1.activate()
    tab2.activate()
    
    # 获取所有标签页
    tabs = cc.chrome.get_tabs()
    print(f"打开的标签页数: {len(tabs)}")
    
    # 关闭特定标签页
    tab2.close()
    
    # 新建标签页
    new_tab = tab1.new_tab("https://www.example3.com")
    
    # 处理弹窗
    try:
        alert = tab1.get_alert()
        alert_text = alert.text
        alert.accept()  # 点击确定
    except:
        print("没有弹窗")
```

------

## 10. 等待与异常处理

```python
def wait_and_exception_handling():
    """等待和异常处理"""
    tab = cc.chrome.open("https://www.example.com")
    
    # 等待元素出现
    try:
        tab.wait_appear(locator.example.button_login, timeout=30)
        print("元素出现了")
    except Exception as e:
        print(f"等待超时: {e}")
    
    # 等待元素消失
    try:
        tab.wait_disappear(locator.example.loading_spinner, timeout=10)
        print("加载完成")
    except Exception as e:
        print(f"等待消失超时: {e}")
    
    # 等待页面加载完成
    tab.wait_page_load(timeout=30)
    
    # 自定义等待条件
    def custom_condition():
        try:
            element = tab.find_element(locator.example.result_text)
            return "Success" in element.get_text()
        except:
            return False
    
    start_time = time.time()
    while not custom_condition() and time.time() - start_time < 30:
        time.sleep(1)
```

------

## 11. 元素属性与状态

```python
def element_properties():
    """获取元素属性和状态"""
    tab = cc.chrome.open("https://www.example.com")
    element = tab.find_element(locator.example.input_username)
    
    # 获取元素文本
    text = element.get_text()
    
    # 获取元素属性
    class_name = element.get_property("class")
    id_value = element.get_property("id")
    
    # 检查元素状态
    is_enabled = element.is_enabled()
    is_visible = element.is_visible()
    is_selected = element.is_selected()  # 对于checkbox/radio
    
    # 获取元素位置和大小
    location = element.location
    size = element.size
    
    print(f"元素文本: {text}")
    print(f"元素类名: {class_name}")
    print(f"元素ID: {id_value}")
    print(f"是否启用: {is_enabled}")
    print(f"是否可见: {is_visible}")
    print(f"位置: {location}")
    print(f"大小: {size}")
```

------

## 12. 截图与高亮

```python
def screenshot_and_highlight():
    """截图和高亮显示"""
    tab = cc.chrome.open("https://www.example.com")
    
    # 页面截图
    tab.save_screenshot(r"C:\path\to\screenshot.png")
    
    # 元素截图
    element = tab.find_element(locator.example.button_login)
    element.save_screenshot(r"C:\path\to\element_screenshot.png")
    
    # 高亮显示元素
    element.highlight()
    time.sleep(2)  # 让用户看到高亮效果
```

------

## 13. JavaScript 执行

```python
def javascript_execution():
    """执行JavaScript代码"""
    tab = cc.chrome.open("https://www.example.com")
    
    # 执行JavaScript
    result = tab.execute_script("return document.title;")
    print(f"页面标题: {result}")
    
    # 执行复杂JavaScript
    script = """
    var element = document.getElementById('username');
    if (element) {
        element.value = 'test_user';
        element.style.backgroundColor = 'yellow';
        return element.value;
    }
    return null;
    """
    result = tab.execute_script(script)
    print(f"JavaScript执行结果: {result}")
    
    # 滚动页面
    tab.execute_script("window.scrollTo(0, document.body.scrollHeight);")
```

------

## 14. 配置文件支持

使用 JSON 文件存储敏感信息（如用户名和密码），提高安全性。

```python
import json

def load_config(file_path):
    """读取配置文件"""
    with open(file_path, 'r') as f:
        return json.load(f)

# 示例配置文件 config.json
# {
#   "username": "your_username",
#   "password": "your_password"
# }

config = load_config("config.json")
username = config["username"]
password = config["password"]
```

------

## 15. 日志记录

使用 Python 的 `logging` 模块记录操作日志，便于调试。

```python
import logging

def setup_logging():
    """设置日志记录"""
    logging.basicConfig(
        filename='clicknium.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("开始执行自动化脚本")
```

------

## 16. 验证码处理

京东登录可能涉及验证码，添加手动或自动处理逻辑。

```python
def handle_captcha(tab):
    """处理验证码"""
    try:
        captcha = tab.find_element(locator.jd.passport.captcha)
        if captcha.is_visible():
            logging.info("检测到验证码，请手动处理")
            time.sleep(10)  # 等待用户手动输入
            # 可选：调用第三方验证码识别服务
            # result = call_third_party_captcha_api(captcha)
            # captcha.set_text(result)
    except:
        logging.info("无验证码")
```

------

## 17. 完整登录示例（以京东为例）

以下是完整的京东登录自动化脚本，包含验证码处理、日志记录和配置文件支持。

```python
import time
import logging
import json
from clicknium import clicknium as cc, locator
from retry import retry

def setup_logging():
    logging.basicConfig(
        filename='jd_login.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def load_config(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

@retry(tries=3, delay=2)
def jd_login():
    """京东登录自动化"""
    setup_logging()
    logging.info("开始京东登录")
    
    try:
        # 读取配置文件
        config = load_config("config.json")
        username = config["username"]
        password = config["password"]
        
        # 打开登录页面
        tab = cc.chrome.open("https://passport.jd.com/new/login.aspx")
        logging.info("打开京东登录页面")
        
        # 等待页面加载
        tab.wait_appear(locator.jd.passport.text_loginname, timeout=10)
        
        # 输入用户名
        username_input = tab.find_element(locator.jd.passport.text_loginname)
        username_input.clear_text()
        username_input.set_text(username)
        logging.info("输入用户名")
        
        # 输入密码
        password_input = tab.find_element(locator.jd.passport.password_nloginpwd)
        password_input.clear_text()
        password_input.set_text(password)
        logging.info("输入密码")
        
        # 处理验证码
        handle_captcha(tab)
        
        # 点击登录按钮
        login_button = tab.find_element(locator.jd.passport.button_login)
        login_button.click()
        logging.info("点击登录按钮")
        
        # 等待登录结果
        try:
            tab.wait_appear(locator.jd.passport.login_success, timeout=10)
            logging.info("登录成功")
            print("登录成功")
        except:
            logging.error("登录失败，可能需要验证")
            print("登录失败，请检查验证码或账号信息")
        
        # 关闭浏览器
        tab.close()
        logging.info("关闭浏览器")
        
    except Exception as e:
        logging.error(f"登录异常: {e}")
        print(f"登录异常: {e}")
        raise

if __name__ == "__main__":
    jd_login()
```

**配置文件示例（config.json）**

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

------

## 注意事项

1. **控件定位**：确保 `locator.yaml` 中的定位信息准确，京东页面可能因更新而变化。
2. **验证码处理**：滑动验证码可能需要人工干预或第三方服务。
3. **重试机制**：使用 `retry` 装饰器处理网络不稳定或页面加载失败的情况。
4. **安全性**：避免硬编码敏感信息，推荐使用配置文件。
5. **浏览器兼容性**：脚本以 Chrome 为例，可根据需要切换为 Edge 或 Firefox。
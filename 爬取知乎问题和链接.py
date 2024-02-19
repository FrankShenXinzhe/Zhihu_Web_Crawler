import csv  # 用于字典转表格
import random  # 用于生成随机数
import pyautogui  # 用于模拟鼠标滚动操作
import subprocess  # 用于执行 cmd 命令
from time import sleep  # 用于强制等待
from selenium import webdriver  # 用于创建 webdriver 对象
from selenium.webdriver import Edge  # 使用 Edge 浏览器进行自动化操作
from selenium.webdriver.common.by import By  # 导入元素定位依据函数 By
from selenium.webdriver.common.keys import Keys  # 导入 send_keys 模块
from selenium.webdriver.edge.options import Options  # 导入 Options 类

# 打开 Edge 浏览器
# 指定 Edge 浏览器 目录
directory = r'C:\Program Files (x86)\Microsoft\Edge\Application'

# 执行cmd命令：打开 Edge 浏览器
subprocess.run('msedge.exe --remote-debugging-port=9222 --user-data-dir="D:\python\seleniumEdge"', shell=True,
               cwd=directory, capture_output=True, text=True)

# 执行 cmd 命令，关闭 cmd 窗口
subprocess.run('exit', shell=True, cwd=directory, capture_output=True, text=True)

# 配置浏览器并访问 https://www.zhihu.com/
# Options 类实例化
Edge_options = Options()

# 配置 Edge 浏览器参数
Edge_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# 创建 Webdriver 对象
wd = webdriver.Edge(options=Edge_options)

# 隐式等待
wd.implicitly_wait(5)

# 调用 Webdriver 对象的get方法，可以让浏览器打开指定网址
wd.get("https://www.zhihu.com/")

# 根据 QQ 登录按钮是否存在判断是否需要进行 QQ 登录
# 寻找 QQ 登录按钮
elements = wd.find_elements(By.CLASS_NAME, 'ZDI.ZDI--Qq24')

# 若存在 QQ 登录按钮
if len(elements) == 1:
    # 从 elements 中提取 QQ 登录按钮
    element = elements[0]

    # 点击QQ登录按钮
    element.click()

    # 切换到 QQ账号安全登录 - 个人 窗口
    for handle in wd.window_handles:
        # 先切换到该窗口
        wd.switch_to.window(handle)
        # 得到该窗口的标题栏字符串，判断是不是我们要操作的那个窗口
        if 'QQ' in wd.title:
            # 如果是，那么这时候WebDriver对象就是对应的该该窗口，正好，跳出循环，
            break

    # 切换到 ID = 'ptlogin_iframe' 的框架内
    wd.switch_to.frame('ptlogin_iframe')

    # 定位 uin="1210820710" 的元素（头像登录按钮）
    element = wd.find_element(By.CSS_SELECTOR, '[uin="1210820710"]')

    # 点击头像登录按钮，登录知乎
    element.click()

    # 等待页面跳转至 首页 - 知乎
    sleep(5)

    # 切换至 首页 - 知乎 窗口
    wd.switch_to.window(wd.window_handles[-1])
# QQ 登录操作完毕


# 搜索模块
# 定位搜索框
element = wd.find_element(By.ID, 'Popover1-toggle')

# 清除搜索框内已有内容
element.clear()

# 输入关键词
element.send_keys('老年大学')

# 点击搜索按钮
wd.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/header/div[1]/div[1]/div/form/div/div/label/button/span').click()

# 打开筛选功能
element = wd.find_element(By.CSS_SELECTOR, '.SearchTabs-customFilterEntry')
element.click()

# 只看回答
element = wd.find_element(By.XPATH, '//*[@id="root"]/div/main/div/div[1]/div[2]/ul[1]/li[2]/div')
element.click()

# 滚动至页面底端
elements = []
while len(elements) == 0:
    # 向下滚动50次
    for i in range(50):
        pyautogui.scroll(-random.randint(900, 1100))
        sleep(0.5)
    # 寻找 Class = 'css-7hmi9v' 的元素（该元素出现代表页面已滚动至最底端）
    elements = wd.find_elements(By.CSS_SELECTOR, '.css-7hmi9v')

# 定位至页面顶端（否则问题会被页面中其他元素遮挡，无法点击）
wd.execute_script('window.scrollTo(0,0)')

# 问题汇总模块
# 新建 Question_Dict 字典准备存储问题和相应链接
Question_Dict = {}

# 定位页面中所有 Class = 'Highlight' 的元素
elements = wd.find_elements(By.CSS_SELECTOR, '.Highlight')

# 循环用于遍历每个问题（由于一个问题对应两个 Class = 'Highlight' 的元素，因此设置步长为 2）
for i in range(0, len(elements), 2):

    # 点击问题
    elements[i].click()

    # 切换至新打开的问题页面
    wd.switch_to.window(wd.window_handles[-1])

    # 等待页面加载完毕
    sleep(2)

    # 定义字典的键 key 为问题
    key = wd.find_element(By.CSS_SELECTOR, '.QuestionHeader-title').get_attribute('innerText')

    # 定义 key 对应的值为当前页面的 url
    Question_Dict[key] = wd.current_url

    # 关闭问题页面
    wd.close()

    # 切换至搜索页面
    wd.switch_to.window(wd.window_handles[0])

# 数据保存模块
# 打开数据表
with open(r"C:\Users\86158\Desktop\原始问题.csv", 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=Question_Dict.keys())
    writer.writeheader()
    writer.writerow(Question_Dict)

# 关闭 Webdriver 对象
wd.quit()

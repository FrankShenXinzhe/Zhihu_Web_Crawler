import re                                            # 用于去除非中文字符
import random                                        # 用于生成随机数
import pyautogui                                     # 用于模拟鼠标滚动操作
import subprocess                                    # 用于执行 cmd 命令
import pandas as pd                                  # 用于处理 csv 文件
from time import sleep                               # 用于强制等待
from selenium import webdriver                       # 用于创建 webdriver 对象
from selenium.webdriver import Edge                  # 使用 Edge 浏览器进行自动化操作
from selenium.webdriver.common.by import By          # 导入元素定位依据函数 By
from selenium.webdriver.common.keys import Keys      # 导入 send_keys 模块
from selenium.webdriver.edge.options import Options  # 导入 Options 类


def remove_non_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    result = re.findall(pattern, text)
    result_str = ''.join(result)
    return result_str


# 打开 Edge 浏览器
# 指定 Edge 浏览器 目录
directory = r'C:\Program Files (x86)\Microsoft\Edge\Application'

# 执行cmd命令：打开 Edge 浏览器
subprocess.run('msedge.exe --remote-debugging-port=9222 --user-data-dir="D:\python\seleniumEdge"', shell=True, cwd=directory, capture_output=True, text=True)

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
wd.implicitly_wait(3)

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


# 提取问题链接
# 定义文件路径
path = r"C:\Users\86158\Desktop\筛选后问题.csv"

# 提取文件内容至 data
data = pd.read_csv(path, encoding='utf-8')

# 将文件第二列（列名为‘url’）写入列表
question_url_list = data['url'].values.tolist()


# 逐一访问 question_url_list 中的每个链接
for question_url in question_url_list:

    # 访问问题链接
    wd.get(question_url)

    # 切换窗口至问题页面
    wd.switch_to.window(wd.window_handles[-1])

    # 点击“查看全部回答”按钮
    elements = wd.find_elements(By.CSS_SELECTOR, '.Card.ViewAll')
    if len(elements) != 0:
        elements[0].click()

        # 滚动至页面底端
        # 列表 elements 用于存储Class = 'Zi.Zi--Edit.QuestionButton-icon' 的元素，该元素为 ”写回答“ 按钮
        elements = []

        #  ”写回答“ 按钮在页面顶端会出现两次，当页面滑动到底端时还会再出现一次。因此滑动到页面底端可以等价于 ”写回答“ 按钮在页面中的出现次数等于 3 。
        #  因此，只要 ”写回答“ 按钮在页面中的出现次数不等于 3 ，就向下滚动页面。
        while len(elements) != 3:

            # 向下滚动10次
            for i in range(10):
                pyautogui.scroll(-random.randint(900, 1100))

            # 向上滚动一次（滚动到页面底端后必须向上滚动一段，否则页面可能无法继续加载）
            pyautogui.scroll(random.randint(900, 1100))

            # 寻找 ”写回答“ 按钮
            elements = wd.find_elements(By.CSS_SELECTOR, '.Zi.Zi--Edit.QuestionButton-icon')

        # 等待页面全部加载完毕
        sleep(3)

        # 定义 回答内容列表
        text_list = []

        # 定位页面中所有的回答
        elements = wd.find_elements(By.CSS_SELECTOR, 'p')

        # 将所有回答添加到 回答内容列表
        for content in elements:
            text_list.append(content.get_attribute('innerText'))

        # 获取问题
        question = wd.find_element(By.CSS_SELECTOR, '.QuestionHeader-title').get_attribute('innerText')

        # 去除问题中的非中文字符
        question = remove_non_chinese(question)

        # 写入模块
        # 创建txt文件（以问题命名）
        f = open(fr'C:\Users\86158\Desktop\回答内容汇总\问题{question}.txt', 'w', encoding='utf-8')

        # 将 text_list 写入txt文件
        for line in text_list:
            f.write(line + '\n')
        f.close()

# 关闭 Webdriver 对象
wd.quit()

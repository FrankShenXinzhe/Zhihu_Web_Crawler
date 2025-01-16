from DrissionPage import ChromiumPage
from DrissionPage.common import By
from bs4 import BeautifulSoup

# 创建浏览器实例
from 知乎_问题id_答案_2 import get_text

page = ChromiumPage()

# 打开知乎首页
page.get('https://www.zhihu.com')
page.set.scroll.smooth(on_off=True)  # 启用平滑滚动

page.ele("#Popover1-toggle").clear().input('老年大学')

page.ele(".Button SearchBar-searchButton FEfUrdfMIKpQDJDqkjte Button--primary Button--blue epMJl0lFQuYbC7jrwr_o JmYzaky7MEPMFcJDLNMG").click()
page.ele(".SearchTabs-customFilterEntry").click()
# 只看问答
loc1 = (By.XPATH, '//*[@id="root"]/div/main/div/div[1]/div[2]/ul[1]/li[2]/div')
page.ele(loc1).click()
# 最多赞同
loc2 = (By.XPATH, '//*[@id="root"]/div/main/div/div[1]/div[2]/ul[2]/li[2]/div')
page.ele(loc2).click()

while not page.s_ele('@class=css-7hmi9v'):
    print(len(page.s_eles('@class=List-item')))
    page.actions.scroll(delta_y=100000)
    page.actions.scroll(delta_y=-10000)

href = (By.XPATH, f'//*[@id="SearchMain"]/div/div/div')
href_html = page.ele(href).html
# 解析HTML
soup = BeautifulSoup(href_html, 'html.parser')

# 查找所有a标签
for a_tag in soup.find_all('a', href=True):  # 确保有 href 属性

    # 获取 a 标签的父元素（div）
    parent_div = a_tag.find_parent('div')

    # 如果父 div 的 class 包含 "RelevantQuery"，则跳过该 a 标签
    if parent_div and 'RelevantQuery' in parent_div.get('class', []):
        continue

    # 如果 href 中不包含 "answer"，则跳过
    if 'answer' not in a_tag['href']:
        continue

    # 输出完整的 URL
    get_text("https://www.zhihu.com" + a_tag['href'])

# 关闭浏览器
page.quit()




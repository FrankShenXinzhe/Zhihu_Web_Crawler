import pandas as pd
from DrissionPage import ChromiumPage


def get_text(http):
    file_path = 'zhihu.txt'

    # 只保留text列
    df = pd.DataFrame(columns=['text'])

    page = ChromiumPage()
    page.get(http)
    page.set.scroll.smooth(on_off=True)

    if page.ele(".QuestionMainAction ViewAll-QuestionMainAction"):
        page.ele(".QuestionMainAction ViewAll-QuestionMainAction").click()

    while not page.s_ele('@class=Button QuestionAnswers-answerButton FEfUrdfMIKpQDJDqkjte Button--blue Button--spread JmYzaky7MEPMFcJDLNMG GMKy5J1UWc7y8NF_V8YA'):
        print(len(page.s_eles('@class=List-item')))
        page.actions.scroll(delta_y=100000)
        page.actions.scroll(delta_y=-10000)

    # 提取数据并保存到文本文件
    with open(file_path, 'a', encoding='utf-8') as file:  # 使用追加模式
        for ele in page.s_eles('@class=List-item'):
            text = "\n".join(map(str, [ele.text for ele in ele.s_eles('tag=p')]))
            file.write(text + "\n\n")  # 每个条目之间用空行分隔


if __name__ == '__main__':
    get_text("https://www.zhihu.com/question/493317162/answer/2178716019", 1)
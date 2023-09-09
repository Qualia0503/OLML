import requests
from bs4 import BeautifulSoup
import lxml
import random
import time
import csv
from time import strftime
from wordcloud import WordCloud
from PIL import Image, ImageDraw
#import Image
import numpy
import jieba.analyse
import jieba
import pandas as pd
import matplotlib.pyplot as plt

list_content = []

list_t = []


# list = ["name","type","value","date"]

# list_content.append(list)

def get_header():
    header1 = {

        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0"

    }

    header2 = {

        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"

    }

    header3 = {

        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"

    }

    header_list = [header1, header2, header3]

    index = random.randint(0, 1)

    return header_list[index]

    pass


# 从微博网站获取数据

def get_data(url, headers):
    time_sleep = random.randint(0, 1)

    req = requests.get(url=url, headers=headers)

    req.encoding = "utf-8"

    # print("响应码：", req.status_code)

    print("名次", "微博热搜话题", "微博热搜话题量", "当前时间")

    html = req.text

    # print(html)

    bf = BeautifulSoup(html, "lxml")

    # print(bf)

    div_content = bf.find_all("tr", class_="")

    t = 1

    for item in div_content:

        # 去掉第一条信息

        if (t == 1):
            t = 0

            continue

        time.sleep(time_sleep)

        # 获取当前热搜名次

        num_content = item.select("td")[0].string

        # 获取当前热搜主题

        content = item.select("td")[1].select("a")[0].string

        # 获取当前热搜主题讨论量

        num = item.select("td")[1].select("span")[0].string

        # 获取当前时间

        current_time = strftime("%Y-%m-%d %H:%M")

        # print(num)

        list_t = [content, num_content, num, current_time]

        list_content.append(list_t)

        print(num_content, content, num, current_time)

    # print(list_content)

    pass


# 存储数据

def store_Excel(list):
    with open("微博实时热搜.csv", "a", encoding="utf_8_sig", newline="")as file:
        csv_writer = csv.writer(file)

        for item in list:
            csv_writer.writerow(item)

        file.close()

    pass


# 生成词云

def get_cloud():
    str = ""

    with open("微博实时热搜test.csv", "r", encoding="utf_8_sig", newline="") as file:

        csv_reader = csv.reader(file)

        t = 1

        for item in csv_reader:

            # 去掉第一行无用信息

            if t == 1:
                t = 0

                continue

            str += item[0]

        # print(str)

        file.close()

    jieba_content = jieba.cut(str)

    # print(jieba_content)

    join_content = " ".join(jieba_content)

    # print(jieba_content)

    wei_bo = Image.open("logo.jpg")

    wei_bo_image = numpy.array(wei_bo)

    word_cloud = WordCloud(font_path="font1.TTF", background_color="white", mask=wei_bo_image).generate(join_content)

    word_cloud.to_file("微博热搜3.jpg")

    with open("1.txt", "w", encoding="utf-8") as file:

        file.write(str)

        file.close()

    pass


# 分析数据

def analysis_data():
    word_dic = {}

    with open(r"./1.txt", "r", encoding="utf-8") as file:

        txt = file.read()

        file.close()

    # jieba分词切分数据

    words = jieba.lcut(txt)

    # print(words)

    for word in words:

        # 如果关键字字数为1，不统计

        if len(word) == 1:

            continue

        # 否则增1

        else:

            word_dic[word] = word_dic.get(word, 0) + 1

    # print(word_dic)

    # 字典数据转换成元祖

    word_zip = zip(word_dic.values(), word_dic.keys())

    # 对元祖里面的元素按照value从大到小进行排序

    word_sort = list(sorted(word_zip, reverse=True))

    # print(word_sort)

    list_1 = ["name", "count_name"]

    list_2 = []

    list_2.append(list_1)

    for item in word_sort:
        # 词频数

        count = item[0]

        # 关键字

        name = item[1]

        list_1 = [name, count]

        list_2.append(list_1)

    # print(list_2)

    with open("微博热搜关键词词频统计.csv", "w", encoding="utf_8_sig", newline="")as file:

        csv_writer = csv.writer(file)

        for i in list_2:
            csv_writer.writerow(i)

        file.close()

    pass


# 数据绘图

def draw_data():
    # 绘图风格

    plt.style.use('ggplot')

    colors1 = '#6D6D6D'

    # 读取csv文件

    df = pd.read_csv(r"微博热搜关键词词频统计.csv", encoding="utf-8")

    print(df)

    df_data = df.sort_values('count_name',ascending=False)

    name1 = df.name[:20]

    count1 = df.count_name[:20]

    # print(name1,count1)

    # 绘制条形图，用range()能保持x轴正确顺序

    plt.bar(range(20), count1, tick_label=name1)

    # 设置纵坐标范围

    plt.ylim(0, 90)

    # 显示中文标签

    plt.rcParams['font.sans-serif'] = ['SimHei']

    # 标题

    plt.title('微博热搜关键词词频统计', color=colors1)

    # x轴标题

    plt.xlabel('关键词')

    # y轴标题

    plt.ylabel('词频')

    # 为每个条形图添加数值标签

    for x, y in enumerate(list(count1)):
        plt.text(x, y + 1, '%s' % round(y, 90), ha='center', color=colors1)

    # x轴关键字旋转300度

    plt.xticks(rotation=300)

    # 自动控制空白边缘，以全部显示x轴坐标

    plt.tight_layout()

    # plt.savefig('微博热搜关键词词频统计top20.png')

    plt.show()

    pass


if __name__ == '__main__':
    url = "https://s.weibo.com/top/summary?cate=realtimehot"

    print("*********************微博热搜榜*********************")

    # 获取微博热搜数据

    get_data(url, get_header())

    # 存储微博热搜数据

    # store_Excel(list_content)

    # 生成微博热搜词云

    # get_cloud()

    # 分析数据
    analysis_data()
    # 绘图描绘数据，生成微博热搜关键词频度top20
    draw_data()
    print("*********************微博热搜榜*********************")
#任务要求：使用requests库发送post或get请求，并返回其相应结果，以一定方式（GUI或界面方式展现出来）
# ，并以图表等进行展示


#任务描述，作微博数据挖掘，使用stopwords进行数据预处理，然后进行分类与情感研究。


import os
import requests
from bs4 import BeautifulSoup

#D:\Recent\homework\python与深度学习基础
def download_all_papers(name, save_path):
    # 创建目录
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # 访问 DBLP 搜索结果页面
    base_url = "https://dblp.org/search?q={name}&h=1000&f=0"
    url = base_url.format(name=name)
    response = requests.get(url)

    # 解析 HTML
    soup = BeautifulSoup(response.content, "html.parser")

    # 获取所有文章链接
    article_links = soup.find_all("a", class_="title")
    for i, link in enumerate(article_links):
        article_url = "https://dblp.org" + link["href"]
        print(article_url)
        article_response = requests.get(article_url)

        # 保存文章内容
        filename = f"{save_path}/paper_{i}.pdf"
        with open(filename, "wb") as f:
            f.write(article_response.content)
            print(f"Downloaded {filename}")

    print("All papers downloaded successfully!")
download_all_papers(name = "Xiangnan He", save_path = "D:/Recent/homework/python与深度学习基础/outputs")
import requests
from bs4 import BeautifulSoup

# 输入计算机科学家姓名
name = input("请输入计算机科学家姓名：")

# 构造 DBLP 的搜索链接
url = f"https://dblp.org/search?q={name}&h=1000&f=0"

# 发送 HTTP 请求并获取响应
response = requests.get(url)

# 解析 HTML
soup = BeautifulSoup(response.content, "html.parser")

# 查找所有文章链接
articles = soup.find_all("li", class_="entry")

flag = 0
# 打印所有文章标题和链接
for article in articles:
    title = article.find("span", class_="title").text
    link = article.find("a", href=True)["href"]
    flag = flag + 1
    print(flag,title,"\n")
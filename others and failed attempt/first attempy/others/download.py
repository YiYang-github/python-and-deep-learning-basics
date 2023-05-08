import requests
from bs4 import BeautifulSoup
name = [' The surprising power of graph neural networks with random node initialization'] 
#去掉所有\n,或者把 \n 用空格替代


def download_papers(titles):
    base_url = "https://dblp.org/search"
    results = {}
    for title in titles:
        query_params = {"q": title}
        response = requests.get(base_url, params=query_params)
        soup = BeautifulSoup(response.text, "html.parser")
        try:
            title = soup.select_one(".title").text
            authors = soup.select_one(".authors").text
            url = soup.select_one(".title a")["href"]
            results[title] = {"authors": authors, "url": url}
        except:
            results[title] = None
    return results
results = download_papers(name)
with open("results.txt", "w") as f:
    for title, info in results.items():
        if info is not None:
            f.write(f"Title: {title}\nAuthors: {info['authors']}\nURL: {info['url']}\n\n")
        else:
            f.write(f"No results found for {title}\n\n")
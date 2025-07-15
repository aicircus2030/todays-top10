import json
import requests
from bs4 import BeautifulSoup

news = []

def fetch_163_news():
    try:
        url = "https://news.163.com/"
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        for item in soup.select("div.news_title a"):
            title = item.get_text(strip=True)
            link = item.get("href", "")
            if title and link.startswith("http"):
                news.append({"title": title, "link": link, "source": "网易"})
    except Exception as e:
        print("❌ 网易新闻抓取失败：", e)

def fetch_bbc():
    try:
        url = "https://www.bbc.com/zhongwen/simp"
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        for item in soup.select("a.gs-c-promo-heading"):
            title = item.get_text(strip=True)
            link = "https://www.bbc.com" + item.get("href", "")
            if title and "/zhongwen" in link:
                news.append({"title": title, "link": link, "source": "BBC"})
    except Exception as e:
        print("❌ BBC 抓取失败：", e)

def fetch_dw():
    try:
        url = "https://www.dw.com/zh/zh%E6%96%B0%E9%97%BB/s-100827"
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        for item in soup.select("a[href^='/zh/']"):
            title = item.get_text(strip=True)
            link = "https://www.dw.com" + item.get("href", "")
            if title and "zh" in link:
                news.append({"title": title, "link": link, "source": "德国之声"})
    except Exception as e:
        print("❌ 德国之声抓取失败：", e)

def fetch_reuters():
    try:
        url = "https://cn.reuters.com/news/archive/worldNews"
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        for item in soup.select("article.story div.story-content a"):
            title = item.get_text(strip=True)
            link = "https://cn.reuters.com" + item.get("href", "")
            if title:
                news.append({"title": title, "link": link, "source": "Reuters"})
    except Exception as e:
        print("❌ Reuters 抓取失败：", e)

def fetch_lianhe():
    try:
        url = "https://www.zaobao.com.sg/news"
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        for item in soup.select("a"):
            title = item.get_text(strip=True)
            link = item.get("href", "")
            if title and "/news/" in link:
                if not link.startswith("http"):
                    link = "https://www.zaobao.com.sg" + link
                news.append({"title": title, "link": link, "source": "联合早报"})
    except Exception as e:
        print("❌ 联合早报抓取失败：", e)

# 抓取所有来源
fetch_163_news()
fetch_bbc()
fetch_dw()
fetch_reuters()
fetch_lianhe()

# 去重（title + source）
seen = set()
unique_news = []
for item in news:
    key = (item["title"], item["source"])
    if key not in seen:
        seen.add(key)
        unique_news.append(item)

# 截取前 50 条
final_news = unique_news[:50]

# 保存为 news.json
if final_news:
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(final_news, f, ensure_ascii=False, indent=2)
    print(f"✅ 成功抓取 {len(final_news)} 条新闻")
else:
    print("⚠️ 所有新闻抓取失败，保留原有 news.json 未作更改")

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# 模拟 headers
headers = {
    "User-Agent": "Mozilla/5.0"
}

# 新闻来源列表（可扩展）
sources = [
    {
        "name": "Reuters",
        "url": "https://www.reuters.com/news/archive/technologyNews",
        "base": "https://www.reuters.com",
        "selector": "article.story",
        "title_tag": "h3.story-title",
        "link_attr": "href"
    },
    {
        "name": "BBC",
        "url": "https://www.bbc.com/news/technology",
        "base": "https://www.bbc.com",
        "selector": "a.gs-c-promo-heading",
        "title_attr": "aria-label",
        "link_attr": "href"
    }
]

# 提取新闻函数
def fetch_news():
    news_items = []
    for source in sources:
        try:
            res = requests.get(source["url"], headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            articles = soup.select(source["selector"])
            for article in articles[:6]:  # 每站最多抓6条
                title = article.get(source.get("title_attr")) or article.text.strip()
                link = article.get(source.get("link_attr")) or article.get("href")
                if not link.startswith("http"):
                    link = source["base"] + link
                if len(title) > 10:
                    news_items.append({
                        "title_en": title.strip(),
                        "url": link.strip(),
                        "source": source["name"]
                    })
        except Exception as e:
            print(f"Error fetching {source['name']}: {e}")
    return news_items[:10]  # 最多10条

# 使用助手翻译为中文摘要（mock）
def generate_summary(news_list):
    translated_news = []
    all_titles = []
    for item in news_list:
        summary = f"这篇来自 {item['source']} 的文章讲述了：{item['title_en'][:50]}..."  # 占位翻译
        item["title"] = item["title_en"]
        item["summary"] = summary
        del item["title_en"]
        translated_news.append(item)
        all_titles.append(item["summary"])
    return translated_news, all_titles

# 输出文件
def save_json(news, summary):
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(news, f, ensure_ascii=False, indent=2)
    with open("summary.json", "w", encoding="utf-8") as f:
        date = datetime.today().strftime("%Y年%m月%d日")
        intro = f"**今日科技、教育与财经热点包括**：\n" + "、\n".join(summary[:5]) + f"。\n{date}。"
        json.dump({"summary": intro}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    news_raw = fetch_news()
    news_final, summary_list = generate_summary(news_raw)
    save_json(news_final, summary_list)

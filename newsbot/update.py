import feedparser
import requests
import json
from datetime import datetime

# === RSS 源列表（科技、教育、财经） ===
rss_feeds = {
    "BBC Technology": "http://feeds.bbci.co.uk/news/technology/rss.xml",
    "Reuters Education": "https://www.reutersagency.com/feed/?best-topics=education&r=feed",
    "CNN Business": "http://rss.cnn.com/rss/money_news_international.rss",
    "AP News Tech": "https://apnews.com/apf-technology?format=RSS"
}

# === 获取新闻摘要的函数（使用 ChatGPT） ===
def summarize(text):
    prompt = f"请用简洁中文总结下面的英文新闻，限40字以内：\n\n{text}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer sk-REPLACE_WITH_YOUR_OWN_KEY"
    }
    data = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5
    }
    try:
        res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data, timeout=10)
        return res.json()["choices"][0]["message"]["content"].strip()
    except:
        return "⚠️ 摘要生成失败"

# === 聚合新闻 ===
items = []
for source, url in rss_feeds.items():
    feed = feedparser.parse(url)
    for entry in feed.entries[:3]:
        title = entry.get("title", "").strip()
        summary = entry.get("summary", "").strip() or entry.get("description", "").strip()
        link = entry.get("link", "#")
        content = f"{title}\n\n{summary}"
        translated = summarize(content)
        items.append({
            "title": title,
            "summary": translated,
            "url": link,
            "source": source
        })

# === 添加免责声明 ===
items.append({
    "title": "免责声明",
    "summary": "本页面内容由程序自动抓取、生成与翻译，仅供参考。",
    "url": "#",
    "source": "系统"
})

# === 写入 news.json 文件 ===
with open("news.json", "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print(f"✅ {len(items)} 条新闻已生成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

import json
news = [
    {"title": "测试新闻一", "link": "https://example.com/a", "source": "网易"},
    {"title": "测试新闻二", "link": "https://example.com/b", "source": "BBC"}
]
with open("news.json", "w", encoding="utf-8") as f:
    json.dump(news * 25, f, ensure_ascii=False, indent=2)
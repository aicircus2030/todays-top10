import json
import feedparser

RSS_FEEDS = {
    '澎湃新闻': 'https://rsshub.app/thepaper/featured',
    'BBC 中文': 'https://rsshub.app/bbc/chinese',
    '新华网': 'https://rsshub.app/xinhuanet/news',
    'Reuters': 'http://feeds.reuters.com/reuters/topNews',
    'CNN': 'http://rss.cnn.com/rss/edition.rss',
    'NYTimes': 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'
}

def fetch_mixed_news(feeds, max_items=50):
    all_entries = []
    seen_titles = set()

    for source, url in feeds.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = entry.title.strip()
                if title in seen_titles:
                    continue
                seen_titles.add(title)
                all_entries.append({
                    'title': title,
                    'link': entry.link.strip(),
                    'summary': entry.get('summary', '').strip()[:100],
                    'source': source
                })
                if len(all_entries) >= max_items:
                    break
        except Exception as e:
            print(f"Error fetching from {source}: {e}")
    return all_entries

if __name__ == "__main__":
    news = fetch_mixed_news(RSS_FEEDS)
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(news, f, ensure_ascii=False, indent=2)
    print("✅ 新闻已更新到 news.json")

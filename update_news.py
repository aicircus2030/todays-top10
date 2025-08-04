
import json
import requests
from datetime import datetime

def fetch_netease_news():
    url = "https://3g.163.com/touch/reconstruct/article/list/BA10TA81wangning/0-10.html"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        text = response.text
        json_str = text[text.find("{"):text.rfind("}")+1]
        data = json.loads(json_str)
        items = list(data.values())[0]
        results = []
        for item in items[:10]:
            results.append({
                "title": item.get("title", "No Title"),
                "link": item.get("url", "#"),
                "source": "网易"
            })
        return results
    except Exception as e:
        return [{"title": "抓取失败", "link": "", "source": "系统"}]

def save_summary(news_list):
    # 本地使用助手端生成，站点不运行此步骤
    summary = {
        "summary": "📢 今日要闻自动摘要将在服务器端生成并每日更新。"
    }
    with open("summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

def main():
    news = fetch_netease_news()
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(news, f, ensure_ascii=False, indent=2)
    save_summary(news)

if __name__ == "__main__":
    main()

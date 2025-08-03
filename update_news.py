
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_zhihu():
    url = 'https://www.zhihu.com/billboard'
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    results = []
    for card in soup.select('.HotList-list > section.HotItem')[:5]:
        title = card.select_one('.HotItem-content .HotItem-title')
        link = card.find('a')
        if title and link:
            results.append({
                'title': title.text.strip(),
                'link': link['href'],
                'source': '知乎'
            })
    return results

def main():
    news = fetch_zhihu()
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(news, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()

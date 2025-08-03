
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
    for card in soup.select('.HotList-list li')[:5]:
        title = card.select_one('.HotList-itemTitle')
        link = card.find('a')
        if title and link:
            results.append({
                'title': title.text.strip(),
                'link': 'https://www.zhihu.com' + link['href'],
                'source': '知乎'
            })
    return results

def fetch_weibo():
    url = 'https://s.weibo.com/top/summary'
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    results = []
    for tr in soup.select('table tbody tr')[1:6]:
        a = tr.select_one('a')
        if a:
            results.append({
                'title': a.text.strip(),
                'link': 'https://s.weibo.com' + a['href'],
                'source': '微博'
            })
    return results

def fetch_baidu():
    url = 'https://top.baidu.com/board?tab=realtime'
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    scripts = soup.find_all('script')
    for script in scripts:
        if 'hotList' in script.text:
            json_text = script.text.split('=', 1)[-1].strip().rstrip(';')
            try:
                data = json.loads(json_text)
                items = data['data']['cards'][0]['content']
                return [{
                    'title': item['word'],
                    'link': item['url'],
                    'source': '百度'
                } for item in items[:5]]
            except:
                break
    return []

def main():
    news = fetch_zhihu() + fetch_weibo() + fetch_baidu()
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(news, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()

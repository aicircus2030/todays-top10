import json
import requests
from bs4 import BeautifulSoup

def fetch_bbc_chinese_top():
    url = "https://www.bbc.com/zhongwen/simp"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    items = []

    for link in soup.select("a.gs-c-promo-heading"):
        title = link.get_text(strip=True)
        href = link.get("href")
        if href and not href.startswith("http"):
            href = "https://www.bbc.com" + href
        if title and href and len(title) > 10:
            items.append({"title": title, "url": href, "source": "BBC 中文"})
        if len(items) >= 50:
            break

    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    fetch_bbc_chinese_top()

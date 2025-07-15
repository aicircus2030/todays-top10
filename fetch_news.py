import json
import requests
from bs4 import BeautifulSoup

def fetch_163_news():
    url = "https://news.163.com"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")
    items = []
    for a in soup.select("a[href^='https://www.163.com/']"):
        title = a.get_text(strip=True)
        href = a.get("href")
        if title and href and len(title) > 10:
            items.append({"title": title, "url": href, "source": "网易新闻"})
        if len(items) >= 15:
            break
    return items

def fetch_bbc_english_news():
    url = "https://www.bbc.com/news"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    items = []
    for a in soup.select("a"):
        title = a.get_text(strip=True)
        href = a.get("href")
        if href and not href.startswith("http"):
            href = url.rstrip("/") + "/" + href.lstrip("/")
        if title and href and len(title) > 10:
            items.append({"title": title, "url": href, "source": "BBC English"})
        if len(items) >= 15:
            break
    return items

def fetch_deutsche_welle_zh_news():
    url = "https://www.dw.com/zh/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    items = []
    for a in soup.select("a"):
        title = a.get_text(strip=True)
        href = a.get("href")
        if href and not href.startswith("http"):
            href = url.rstrip("/") + "/" + href.lstrip("/")
        if title and href and len(title) > 10:
            items.append({"title": title, "url": href, "source": "德国之声"})
        if len(items) >= 15:
            break
    return items

def fetch_reuters_zh_news():
    url = "https://cn.reuters.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    items = []
    for a in soup.select("a"):
        title = a.get_text(strip=True)
        href = a.get("href")
        if href and not href.startswith("http"):
            href = url.rstrip("/") + "/" + href.lstrip("/")
        if title and href and len(title) > 10:
            items.append({"title": title, "url": href, "source": "路透中文"})
        if len(items) >= 15:
            break
    return items

def fetch_zaobao_news():
    url = "https://www.zaobao.com/news/china"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    items = []
    for a in soup.select("a"):
        title = a.get_text(strip=True)
        href = a.get("href")
        if href and not href.startswith("http"):
            href = url.rstrip("/") + "/" + href.lstrip("/")
        if title and href and len(title) > 10:
            items.append({"title": title, "url": href, "source": "联合早报"})
        if len(items) >= 15:
            break
    return items

if __name__ == "__main__":
    all_news = []
    try: all_news += fetch_163_news()
    except Exception as e: print("❌ 网易新闻失败:", e)
    try: all_news += fetch_bbc_english_news()
    except Exception as e: print("❌ BBC失败:", e)
    try: all_news += fetch_deutsche_welle_zh_news()
    except Exception as e: print("❌ 德国之声失败:", e)
    try: all_news += fetch_reuters_zh_news()
    except Exception as e: print("❌ 路透失败:", e)
    try: all_news += fetch_zaobao_news()
    except Exception as e: print("❌ 联合早报失败:", e)

    seen = set()
    unique = []
    for item in all_news:
        if item["title"] not in seen:
            unique.append(item)
            seen.add(item["title"])

    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(unique[:50], f, indent=2, ensure_ascii=False)

    print(f"✅ 抓取成功，共 {len(unique[:50])} 条")
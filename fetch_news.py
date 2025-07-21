import requests
from bs4 import BeautifulSoup
import json
import random

news = []

def summarize_text(text, max_len=180):
    sentences = text.split('. ')
    return sentences[0].strip() if sentences else text.strip()

def fetch_bbc(max_items=13):
    url = "https://www.bbc.com/news"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    articles = soup.select("a.gs-c-promo-heading")
    count = 0
    for item in articles:
        title = item.get_text(strip=True)
        link = item.get("href")
        if not link.startswith("http"):
            link = "https://www.bbc.com" + link
        if title and link:
            news.append({
                "title": title,
                "link": link,
                "source": "BBC",
                "summary": summarize_text(title)
            })
            count += 1
        if count >= max_items:
            break

def fetch_reuters(max_items=13):
    url = "https://www.reuters.com/news/archive/worldNews"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    stories = soup.select("article.story")
    count = 0
    for s in stories:
        h3 = s.select_one("h3.story-title")
        if not h3:
            continue
        title = h3.get_text(strip=True)
        a_tag = s.find("a")
        link = "https://www.reuters.com" + a_tag.get("href") if a_tag else ""
        if title and link:
            news.append({
                "title": title,
                "link": link,
                "source": "Reuters",
                "summary": summarize_text(title)
            })
            count += 1
        if count >= max_items:
            break

def fetch_cnn(max_items=12):
    url = "https://edition.cnn.com/world"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    links = soup.select("h3.cd__headline a")
    count = 0
    for a in links:
        title = a.get_text(strip=True)
        link = a.get("href")
        if not link.startswith("http"):
            link = "https://edition.cnn.com" + link
        if title and link:
            news.append({
                "title": title,
                "link": link,
                "source": "CNN",
                "summary": summarize_text(title)
            })
            count += 1
        if count >= max_items:
            break

def fetch_ap(max_items=12):
    url = "https://apnews.com/hub/world-news"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    items = soup.select("a.Link")
    count = 0
    for item in items:
        title = item.get_text(strip=True)
        link = item.get("href")
        if not link.startswith("http"):
            link = "https://apnews.com" + link
        if title and link:
            news.append({
                "title": title,
                "link": link,
                "source": "AP News",
                "summary": summarize_text(title)
            })
            count += 1
        if count >= max_items:
            break

# --- Run all ---
fetch_bbc()
fetch_reuters()
fetch_cnn()
fetch_ap()

# Random shuffle & keep 50
random.shuffle(news)
news = news[:50]

with open("news.json", "w", encoding="utf-8") as f:
    json.dump(news, f, indent=2, ensure_ascii=False)

print("✅ news.json updated with", len(news), "items.")

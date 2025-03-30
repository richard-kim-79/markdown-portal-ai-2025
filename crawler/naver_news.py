# crawler/naver_news.py

import requests
from bs4 import BeautifulSoup
import trafilatura

def crawl_naver_news(query: str, max_articles: int = 5):
    print(f"⚡️ 네이버 뉴스 검색: '{query}'")
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    # 뉴스 검색 URL (네이버 뉴스 검색)
    search_url = f"https://search.naver.com/search.naver?where=news&query={query}"
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for link in soup.select("a.info"):
        url = link.get("href")
        if not url or "news.naver.com" not in url:
            continue

        # 본문 추출
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            continue

        content = trafilatura.extract(downloaded)
        if not content or len(content) < 300:
            continue

        title = link.find_previous("a").text.strip()
        results.append({"title": title, "url": url, "content": content})

        if len(results) >= max_articles:
            break

    print(f"✅ 총 {len(results)}개 기사 수집 완료")
    return results
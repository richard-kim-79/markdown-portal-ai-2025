# crawler/collector.py

import requests
from bs4 import BeautifulSoup
import re

def collect_news_from_naver(query: str = "AI", max_articles: int = 5) -> list:
    """
    네이버 뉴스 검색 결과에서 기사 제목, 링크, 본문 내용을 크롤링합니다.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    query_encoded = requests.utils.quote(query)
    search_url = f"https://search.naver.com/search.naver?where=news&query={query_encoded}&sm=tab_opt"

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    news_links = []
    for a_tag in soup.select("a.info"):
        href = a_tag.get("href")
        if href and "news.naver.com" in href:
            news_links.append(href)

    news_links = list(dict.fromkeys(news_links))[:max_articles]  # 중복 제거 + 최대 제한

    articles = []
    for url in news_links:
        try:
            article_html = requests.get(url, headers=headers).text
            article_soup = BeautifulSoup(article_html, "html.parser")

            title = article_soup.select_one("h2#title_area, h3#articleTitle")  # 예전/새 뉴스 구조
            title_text = title.text.strip() if title else "제목 없음"

            body = article_soup.select_one("article#dic_area, div#articleBodyContents")
            body_text = body.get_text(separator="\n").strip() if body else ""

            # 특수문자 제거
            body_cleaned = re.sub(r"\s+", " ", re.sub(r"[^\w가-힣 .,!?]", "", body_text))

            articles.append({
                "title": title_text,
                "url": url,
                "content": body_cleaned
            })
        except Exception as e:
            print(f"⚠️ 기사 수집 실패: {url} - {e}")

    return articles
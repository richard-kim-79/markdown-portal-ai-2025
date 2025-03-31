# crawler/collector.py

import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict


def collect_news_from_naver(query: str = "AI", max_articles: int = 5) -> List[Dict[str, str]]:
    """
    네이버 뉴스 검색 결과에서 기사 제목, 링크, 본문 내용을 크롤링합니다.

    Args:
        query (str): 검색어 (기본값: "AI")
        max_articles (int): 수집할 최대 기사 수

    Returns:
        List[Dict[str, str]]: 제목, URL, 본문이 담긴 기사 리스트
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    query_encoded = requests.utils.quote(query)
    search_url = f"https://search.naver.com/search.naver?where=news&query={query_encoded}&sm=tab_opt"

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # 검색 결과에서 뉴스 기사 링크 수집
    news_links = []
    for a_tag in soup.select("a.info"):
        href = a_tag.get("href")
        if href and "news.naver.com" in href:
            news_links.append(href)

    # 중복 제거 및 최대 기사 수 제한
    news_links = list(dict.fromkeys(news_links))[:max_articles]

    articles = []

    for url in news_links:
        try:
            article_html = requests.get(url, headers=headers).text
            article_soup = BeautifulSoup(article_html, "html.parser")

            # 제목 추출 (구버전/신버전 대응)
            title_el = article_soup.select_one("h2#title_area, h3#articleTitle")
            title_text = title_el.get_text(strip=True) if title_el else "제목 없음"

            # 본문 추출
            body_el = article_soup.select_one("article#dic_area, div#articleBodyContents")
            body_text = body_el.get_text(separator="\n", strip=True) if body_el else ""

            # 특수문자, 공백 정리
            body_cleaned = re.sub(r"\s+", " ", re.sub(r"[^\w가-힣 .,!?]", "", body_text))

            articles.append({
                "title": title_text,
                "url": url,
                "content": body_cleaned
            })

        except Exception as e:
            print(f"⚠️ 기사 수집 실패: {url} - {e}")

    return articles
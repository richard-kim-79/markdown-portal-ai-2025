# tasks/crawler_task.py

from crawler.naver_news import crawl_naver_news
from summarizer.summarizer import summarize_documents
from summarizer.tagger import generate_tags
from summarizer.markdown_generator import save_markdown
from db.models import insert_document
from datetime import datetime

def run_crawling_and_summarization():
    print("🚀 [START] 자동 크롤링 실행")
    results = crawl_naver_news("인공지능", max_articles=5)

    for doc in results:
        title = doc["title"]
        url = doc["url"]
        content = doc["content"]
        category = "뉴스"

        summary = summarize_documents(content)
        tags = generate_tags(summary)
        save_path = save_markdown(title, summary, tags, content)

        insert_document(
            title=title,
            content=content,
            summary=summary,
            tags=tags,
            category=category,
            url=url,
            saved_path=str(save_path)
        )

    print("✅ [END] 자동 크롤링 및 저장 완료")
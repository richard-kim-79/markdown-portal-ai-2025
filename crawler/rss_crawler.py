import feedparser
import requests
from trafilatura import extract
from summarizer.summarizer import summarize_documents
from summarizer.tagger import generate_tags
from summarizer.markdown_generator import save_markdown
from db.models import insert_document


def load_rss_feeds(path="crawler/rss_feeds.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def fetch_and_process_feed(feed_url):
    feed = feedparser.parse(feed_url)
    for entry in feed.entries[:3]:  # 각 피드당 최근 3개 기사만 수집
        title = entry.title
        url = entry.link

        print(f"🔗 {title} ({url})")

        try:
            html = requests.get(url, timeout=10).text
            content = extract(html)
            if not content:
                print("⚠️ 본문 추출 실패"); continue

            summary = summarize_documents(content)
            tags = generate_tags(summary)
            save_path = save_markdown(title, summary, tags, content)

            insert_document(title, content, summary, tags, category="뉴스", url=url, saved_path=str(save_path))
            print(f"✅ 저장 완료: {save_path}")
        except Exception as e:
            print(f"❌ 오류 발생: {e}")


def run_rss_crawler():
    feeds = load_rss_feeds()
    print(f"🌐 RSS 피드 {len(feeds)}개 수집 시작...")
    for feed_url in feeds:
        fetch_and_process_feed(feed_url)
    print("🎉 전체 수집 완료!")


if __name__ == "__main__":
    run_rss_crawler()

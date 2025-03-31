# app/main.py
import streamlit as st
from summarizer.summarizer import summarize_documents
from summarizer.tagger import generate_tags
from summarizer.markdown_generator import save_markdown
from db.models import (
    init_db,
    insert_document,
    get_all_documents,
    log_collection,
    get_recent_logs
)
from crawler.collector import collect_news_from_naver

# ✅ 페이지 설정
st.set_page_config(page_title="🧠 Markdown Portal for AI 2025", layout="wide")
st.title("📚 Markdown Portal for AI 2025")
st.markdown("뉴스, 블로그, 논문 등의 원문을 요약하고 태깅하며, 결과를 Markdown으로 저장하고 DB에 기록합니다.")

# ✅ DB 초기화
init_db()

# ✅ 수집 로그 렌더 함수
def render_log_entry(log):
    status_emoji = "✅" if log[3] == "success" else "❌"
    created = log[5][:19] if log[5] else "시간 없음"
    source = log[1]
    keyword = log[2]
    message = log[4]
    st.markdown(f"{status_emoji} `{created}` | {source} | `{keyword}` → {message}")

# ✅ 저장된 문서 필터링
def filter_documents(documents, title_filter, tag_filter, category_filter):
    results = []
    for doc in documents:
        title = doc[1] or ""
        tags = doc[4] or ""
        category = doc[5] or ""

        if (
            (not title_filter or title_filter.lower() in title.lower()) and
            (not tag_filter or tag_filter.lower() in tags.lower()) and
            (category_filter == "전체" or category_filter == category)
        ):
            results.append(doc)
    return results

# 📡 자동 뉴스 수집
if st.button("📡 자동 뉴스 수집"):
    with st.spinner("🌀 네이버 뉴스에서 'AI' 관련 문서 수집 중..."):
        results = collect_news_from_naver(query="AI", max_articles=3)
        for article in results:
            title = article.get("title", "제목 없음")
            try:
                url = article.get("url")
                content = article.get("content")
                summary = summarize_documents(content)
                tags = generate_tags(summary)
                save_path = save_markdown(title, summary, tags, content)

                insert_document(title, content, summary, tags, "뉴스", url, str(save_path))
                log_collection("naver_news", "AI", "success", title)
                st.toast(f"✅ 저장 완료: {title}")
            except Exception as e:
                log_collection("naver_news", "AI", "fail", f"{title} - {e}")
                st.error(f"❌ {title} 저장 중 오류 발생: {e}")
        st.success("✅ 자동 수집 완료!")

# ✍️ 수동 입력
with st.form("input_form"):
    url = st.text_input("🔗 원본 URL", "")
    title = st.text_input("📝 문서 제목", "")
    category = st.selectbox("📂 문서 유형 (카테고리)", ["뉴스", "블로그", "논문", "기타"])
    content = st.text_area("📄 원문 텍스트", height=300)
    submitted = st.form_submit_button("요약 및 저장")

if submitted and content.strip():
    with st.spinner("요약 중..."):
        try:
            summary = summarize_documents(content)
            tags = generate_tags(summary)
            save_path = save_markdown(title or "Untitled", summary, tags, content)
            insert_document(title, content, summary, tags, category, url, str(save_path))

            st.success("✅ 저장 완료!")
            st.markdown(f"📁 저장 경로: `{save_path}`")
            st.markdown("### ✨ 요약 결과")
            st.write(summary)
            st.markdown("### 🏗️ 태그")
            st.write(", ".join(tags))
        except Exception as e:
            st.error(f"❌ 오류 발생: {e}")
elif submitted:
    st.warning("⚠️ 원문 텍스트를 입력해주세요.")

# 🔍 필터 및 문서 목록
st.markdown("---")
st.subheader("🔎 문서 검색 필터")
search_title = st.text_input("🔤 제목 검색")
search_tag = st.text_input("🏷️ 태그 포함")
search_category = st.selectbox("🗂️ 카테고리 필터", ["전체", "뉴스", "블로그", "논문", "기타"])

st.subheader("📖 저장된 요약 목록")
documents = get_all_documents()
filtered_docs = filter_documents(documents, search_title, search_tag, search_category)

if filtered_docs:
    for doc in filtered_docs:
        title = doc[1] or "제목 없음"
        content = doc[2] or ""
        summary = doc[3] or ""
        tags = doc[4] or ""
        category = doc[5] or "카테고리 없음"
        url = doc[6] or "없음"
        path = doc[7] or ""
        created_at = doc[8][:19] if doc[8] else "날짜 없음"

        with st.expander(f"📌 {title} | 🗂️ {category} | 🍒 {created_at}"):
            st.markdown(f"**🔗 URL:** {url}")
            st.markdown(f"**📝 원문 내용:**\n\n{content}")
            st.markdown(f"**📌 요약 결과:**\n\n{summary}")
            st.markdown(f"**🏷️ 태그:** {tags}")
            st.markdown(f"📁 저장 경로: `{path}`")
else:
    st.info("🔍 조건에 맞는 문서가 없습니다.")

# 🪵 수집 로그
st.markdown("---")
st.subheader("🪵 수집 로그")
for log in get_recent_logs(limit=10):
    render_log_entry(log)
# 🧠 Markdown Portal for AI 2025

AI 시대를 위한 지식 요약/태깅/저장 허브.

Streamlit + SQLite + Markdown 기반으로, 뉴스/블로그/논문 등의 콘텐츠를 요약하고, 태그를 생성해 마크다운 파일로 저장하며, 검색 가능한 DB에 기록합니다.

## 🧩 주요 기능

- 📥 수동 입력 or 📡 자동 뉴스 수집 (네이버 뉴스)
- 🤖 Hugging Face BART 요약기 (선택 가능)
- 🏷️ 태그 생성기 (기본 내장 or 커스터마이즈 가능)
- 📁 Markdown 문서 저장 (docs/ 폴더에 자동 생성)
- 💾 SQLite DB 기록 및 Streamlit 검색 필터
- 🪵 수집 로그 추적
- ☁️ Hugging Face Spaces 배포 가능

---

## 🧪 설치 및 실행

```bash
git clone https://github.com/richard-kim-79/markdown-portal-ai-2025.git
cd markdown_portal_ai_2025
pip install -r requirements.txt
python3 -m db.init  # ✅ DB 초기화
streamlit run app/main.py
```

---

## ⏰ 자동 크롤링 설정 (선택)

`hf_restart_trigger.py`를 활용해 [cron-job.org](https://cron-job.org/) 또는 GitHub Actions에서 주기적으로 Hugging Face Space를 재시작 → 자동 수집 트리거!

---

## 📂 프로젝트 구조

```
.
├── app/                # Streamlit 메인 앱
├── db/                 # DB 모델 및 초기화
├── crawler/            # 뉴스/블로그 수집기
├── summarizer/         # 요약기 및 태거
├── docs/               # 생성된 Markdown 파일
├── data/summary.db     # SQLite DB
├── requirements.txt
├── README.md
```

---

## 🚀 Hugging Face Space

👉 https://huggingface.co/spaces/aitree2025/markdown_portal_ai_2025

--- 


from datetime import datetime
from pathlib import Path

def save_markdown(title: str, summary: str, tags: list, content: str) -> Path:
    """
    요약 결과, 원문 텍스트, 태그를 Markdown 파일로 저장합니다.
    """
    safe_title = "".join(c if c.isalnum() else "_" for c in title.strip()) or "untitled"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{safe_title}.md"
    
    save_dir = Path("docs")
    save_dir.mkdir(parents=True, exist_ok=True)
    
    full_path = save_dir / filename
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"⏱️ 저장 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## 📌 요약\n\n{summary}\n\n")
        f.write(f"## 🏷️ 태그\n\n{', '.join(tags)}\n\n")
        f.write(f"## 📄 원문\n\n{content}\n")
    
    return full_path
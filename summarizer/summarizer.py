# summarizer/summarizer.py

from typing import Optional

def summarize_documents(text: str, max_sentences: int = 3) -> str:
    """
    입력된 텍스트를 간단히 요약합니다.
    현재는 단순 문장 분리 후 앞부분 추출 방식입니다.
    향후 Hugging Face 모델로 교체 가능.
    """
    sentences = text.strip().split(".")
    summary = ". ".join(sentences[:max_sentences]).strip()
    return summary + "." if summary and not summary.endswith(".") else summary
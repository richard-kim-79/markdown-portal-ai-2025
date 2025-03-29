# summarizer/tagger.py

from typing import List
import re
from collections import Counter

def generate_tags(text: str, top_k: int = 5) -> List[str]:
    """
    텍스트에서 가장 많이 등장하는 단어를 기반으로 태그를 생성합니다.
    """
    # 단어 정규화
    words = re.findall(r'\b\w{3,}\b', text.lower())  # 길이 3 이상 단어만
    common = Counter(words).most_common(top_k)
    tags = [word for word, _ in common]
    return tags
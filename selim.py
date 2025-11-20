from __future__ import annotations
import re
from collections import Counter
from typing import List, Dict
from crawler import Article

# 공통 불용어 집합
STOPWORDS = {
    "그리고", "그러나", "하지만", "또한",
    "했다", "합니다", "하였다", "있다",
    "이번", "대한", "통해", "오늘",
    "기자", "사진", "제공",
    "관련", "보도", "서울", "한국",
    "에서", "이며", "이다"
}


# 언론사별 기사 개수
def source_counts(articles: List[Article]) -> Dict[str, int]:
    return dict(Counter(a.source for a in articles))

# 전체 단어 빈도 (키워드 TOP N)
def top_keywords(articles: List[Article], topn: int = 7) -> List[tuple[str, int]]:
    text = " ".join(a.content or "" for a in articles)

    # 글자 패턴 (중간점 포함)
    words = re.findall(r"[가-힣A-Za-z0-9·]{2,}", text)

    # 불용어 제거, 숫자 제거
    words = [w for w in words if w not in STOPWORDS and not w.isdigit()]

    counter = Counter(words)
    return counter.most_common(topn)

# 기사 길이 통계
def length_stats(articles: List[Article]) -> Dict[str, float]:
    body_lengths = [len(a.content or "") for a in articles]
    title_lengths = [len(a.title or "") for a in articles]

    return {
        "평균 제목 길이": sum(title_lengths) / len(title_lengths) if title_lengths else 0,
        "평균 본문 길이": sum(body_lengths) / len(body_lengths) if body_lengths else 0,
        "최소 본문 길이": min(body_lengths) if body_lengths else 0,
        "최대 본문 길이": max(body_lengths) if body_lengths else 0,
    }

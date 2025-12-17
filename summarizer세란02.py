import re
import requests
from bs4 import BeautifulSoup


# ===============================
# 공통 문장 분리 유틸
# ===============================
def split_sentences(text: str):
    """
    마침표, 느낌표, 물음표 기준으로 문장을 안전하게 분리
    """
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if s]


# ===============================
# Base Summarizer
# ===============================
class BaseSummarizer:
    def summarize(self, text: str, max_sentences: int = 3) -> str:
        raise NotImplementedError


# ===============================
# Dummy Summarizer
# ===============================
class DummySummarizer(BaseSummarizer):
    def summarize(self, text: str, max_sentences: int = 3) -> str:
        sentences = split_sentences(text)
        return " ".join(sentences[:max_sentences])


# ===============================
# Fake Model
# ===============================
class FakeModel:
    def generate(self, text: str, max_sentences: int = 3):
        sentences = split_sentences(text)
        reversed_sentences = list(reversed(sentences))
        return " ".join(reversed_sentences[:max_sentences])


# ===============================
# Model Summarizer
# ===============================
class ModelSummarizer(BaseSummarizer):
    def __init__(self, model_path: str = "models/news_summary_model.pt"):
        self.model_path = model_path
        self.model = FakeModel()

    def summarize(self, text: str, max_sentences: int = 3) -> str:
        return self.model.generate(text, max_sentences=max_sentences)


# ===============================
# Summarizer Factory
# ===============================
def get_summarizer(model_ready: bool = False):
    if model_ready:
        return ModelSummarizer()
    return DummySummarizer()


# ===============================
# 뉴스 본문 크롤링
# ===============================
def fetch_news_text(url: str) -> str:
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=10
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # 일반적인 뉴스 본문 탐색
    article = (
        soup.find("article")
        or soup.find("div", {"id": "articleBodyContents"})
        or soup.find("div", {"class": "article_body"})
    )

    if not article:
        raise ValueError("뉴스 본문을 찾을 수 없습니다.")

    return article.get_text(separator=" ", strip=True)


# ===============================
# 뉴스 입력창 (콘솔)
# ===============================
def summarize_news_from_input():
    url = input("📰 뉴스 링크를 입력하세요: ").strip()
    summarizer = get_summarizer(model_ready=True)

    try:
        news_text = fetch_news_text(url)
        summary = summarizer.summarize(news_text, max_sentences=3)

        print("\n✅ 뉴스 요약 결과")
        print("-" * 40)
        print(summary)
    except Exception as e:
        print("\n❌ 오류 발생:", e)


# ===============================
# Main
# ===============================
if __name__ == "__main__":
    print("=== 텍스트 요약 테스트 ===")
    text = "첫 문장입니다. 두 번째 문장입니다. 세 번째 문장입니다. 네 번째 문장입니다."

    s1 = get_summarizer(model_ready=False)
    print("Dummy:", s1.summarize(text))

    s2 = get_summarizer(model_ready=True)
    print("Model:", s2.summarize(text))

    print("\n=== 뉴스 요약 ===")
    summarize_news_from_input()

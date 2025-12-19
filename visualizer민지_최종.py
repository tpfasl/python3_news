# visualizer.py
# 역할: 통계 결과 시각화 전용 모듈 (한글 지원)

import os
import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams
from wordcloud import WordCloud

from stats_module import ArticleAnalyzer


# -------------------------
# 한글 폰트 강제 등록
# -------------------------

FONT_PATH = "C:/Windows/Fonts/malgun.ttf"

font_manager.fontManager.addfont(FONT_PATH)
font_name = font_manager.FontProperties(fname=FONT_PATH).get_name()

rcParams["font.family"] = font_name
rcParams["axes.unicode_minus"] = False

os.makedirs("plots", exist_ok=True)


# -------------------------
# 시각화 함수들
# -------------------------

def plot_keyword_freq(keyword_freq: dict):
    """키워드 빈도 막대그래프 (한글 지원)"""
    words = list(keyword_freq.keys())
    counts = list(keyword_freq.values())

    if not words:
        print("시각화할 키워드가 없습니다.")
        return

    plt.figure(figsize=(8, 5))
    plt.bar(words, counts)
    plt.title("키워드 빈도 분석")
    plt.xlabel("키워드")
    plt.ylabel("빈도수")
    plt.tight_layout()
    plt.savefig("plots/keyword_freq.png")
    plt.show()


def plot_wordcloud(keyword_freq: dict):
    """키워드 워드클라우드 (한글 지원)"""
    if not keyword_freq:
        print("워드클라우드용 키워드가 없습니다.")
        return

    font_path = "C:/Windows/Fonts/malgun.ttf"

    wc = WordCloud(
        width=800,
        height=400,
        background_color="white",
        font_path=font_path
    )
    wc.generate_from_frequencies(keyword_freq)

    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("plots/wordcloud.png")
    plt.show()

# -------------------------
# main.py에서 호출하는 진입점
# -------------------------

def run_visualization(articles):
    """
    main.py에서 articles(List[dict])를 받아 시각화 수행
    """
    if not articles:
        print("시각화할 데이터가 없습니다.")
        return

    analyzer = ArticleAnalyzer(articles)
    keyword_list = analyzer.top_keywords()
    keyword_freq = dict(keyword_list)

    plot_keyword_freq(keyword_freq)
    plot_wordcloud(keyword_freq)

# -------------------------
# 단독 실행 방지
# -------------------------

if __name__ == "__main__":
    print("이 모듈은 main.py에서 호출하여 사용합니다.")

import os
from datetime import datetime


def _make_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def save_summary(keyword, summary, folder="results"):
    """
    뉴스 요약 결과를 summary_키워드_날짜.txt 로 저장하는 함수
    summary : 문자열(str) 또는 문자열 리스트(list) 모두 지원
    """
    _make_folder(folder)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"summary_{keyword}_{timestamp}.txt"
    filepath = os.path.join(folder, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"[요약 결과]\n키워드: {keyword}\n")
        f.write(f"파일 생성 시각: {timestamp}\n")
        f.write("=" * 40 + "\n\n")

        # summary가 리스트일 경우 처리
        if isinstance(summary, list):
            for i, s in enumerate(summary, 1):
                f.write(f"{i}. {s}\n")
        else:
            f.write(summary)

    return filepath


def save_stats(keyword, stats, folder="results"):
    """
    단어 빈도 분석 결과를 stats_키워드_날짜.txt 로 저장하는 함수
    stats : dict 형태 (ex: {"경제":5, "시장":3})
    """
    _make_folder(folder)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"stats_{keyword}_{timestamp}.txt"
    filepath = os.path.join(folder, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"[단어 빈도 통계]\n키워드: {keyword}\n")
        f.write(f"파일 생성 시각: {timestamp}\n")
        f.write("=" * 40 + "\n\n")

        for word, count in stats.items():
            f.write(f"{word} : {count}회\n")

    return filepath


if __name__ == "__main__":
    test_sum = ["애플이 신제품을 발표했다.", "금리가 상승하고 있다."]
    test_stat = {"경제": 4, "시장": 2, "물가": 3}

    print(save_summary("경제", test_sum))
    print(save_stats("경제", test_stat))

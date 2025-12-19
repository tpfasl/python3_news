from tkinter import *

# --- 프로젝트 모듈 임포트 ---
from crawler import NewsCollector
from cleaner import clean_title_list
from summarizer import ModelSummarizer
from stats_module import top_keywords, length_stats
from visualizer import run_visualization
from file_manager import save_summary, save_stats  

# 통계/시각화용 전역 변수
last_articles = []

def run_process():
    global last_articles

    listbox.delete(0, END)
    result_label.config(text="")
    key = entry.get().strip()

    if key == "":
        result_label.config(text="키워드를 입력해주세요.", fg="red")
        return

    result_label.config(text="데이터 수집 및 분석 중...", fg="black")
    window.update()

    # 1️⃣ 뉴스 수집
    collector = NewsCollector()
    articles = collector.get_news_list(key, limit=10)

    if not articles:
        result_label.config(text="관련 뉴스를 찾을 수 없습니다.", fg="red")
        return

    # 2️⃣ 제목 정제
    raw_titles = [a["title"] for a in articles]
    cleaned_titles = clean_title_list(raw_titles)

    for a, title in zip(articles, cleaned_titles):
        a["content"] = title

    last_articles = articles

    # 3️⃣ 요약
    summarizer = ModelSummarizer()
    summary = summarizer.summarize(". ".join(cleaned_titles))

    # 4️⃣ 결과 출력
    for i, title in enumerate(cleaned_titles, 1):
        listbox.insert(END, f"{i}. {title}")

    # ✅ [추가] 뉴스 분석이 끝나면 자동으로 요약본 저장
    # file_manager.py의 save_summary 함수를 여기서 호출해야 합니다.
    save_summary(key, summary) 

    result_label.config(
        text="✨ 분석 및 요약 완료 (자동 저장됨):\n" + summary,
        fg="blue"
    )

def run_stats():
    if not last_articles:
        result_label.config(text="먼저 뉴스 분석을 실행하세요.", fg="red")
        return

    keywords = top_keywords(last_articles)
    stats = length_stats(last_articles)

    # 저장용 데이터 준비 (리스트를 딕셔너리로 변환)
    kw_dict = {k: v for k, v in keywords}

    text = "📊 통계 분석 결과\n\n[키워드 빈도]\n"
    for k, v in keywords:
        text += f"- {k}: {v}\n"

    text += "\n[길이 통계]\n"
    for k, v in stats.items():
        text += f"- {k}: {v:.1f}\n"

    # ✅ [추가] 통계 버튼을 누르면 통계 결과 저장
    key = entry.get().strip()
    save_stats(key, kw_dict)

    result_label.config(text=text + "\n(통계 파일 저장 완료)", fg="green")

# --- 이하 run_visual 및 GUI 구성은 기존과 동일 ---
def run_visual():
    if not last_articles:
        result_label.config(text="먼저 뉴스 분석을 실행하세요.", fg="red")
        return
    run_visualization(last_articles)
    result_label.config(text="📈 시각화 완료! plots 폴더 확인", fg="green")

window = Tk()
window.title("키워드 기반 맞춤형 뉴스 요약 시스템")
window.geometry("900x720")
window.option_add("*Font", "맑은고딕 11")

Label(window, text="뉴스 키워드를 입력하세요", font=("맑은고딕", 13, "bold")).pack(pady=10)
entry = Entry(window, width=45)
entry.pack()

Button(window, text="📰 뉴스 분석 시작하기", command=run_process, bg="#4a90e2", fg="white", padx=20).pack(pady=10)
Label(window, text="< 수집 및 정제된 뉴스 목록 >").pack()
listbox = Listbox(window, width=100, height=12)
listbox.pack(pady=5)
Button(window, text="📊 통계 분석", command=run_stats).pack(pady=5)
Button(window, text="📈 시각화 실행", command=run_visual).pack(pady=5)

result_label = Label(window, text="결과가 여기에 표시됩니다.", justify="left", wraplength=850)
result_label.pack(pady=20)
window.mainloop()
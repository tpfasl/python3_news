from tkinter import *

def crawl_news(keyword):
    dummy_titles = [
        f"{keyword}에 대한 전문가 의견 공개",
        f"{keyword} 관련 새로운 연구 발표",
        f"{keyword} 문제가 사회적 이슈로 부상",
        f"{keyword} 시장이 급변하고 있다?",
        f"{keyword} 트렌드 분석 결과는?"
    ]
    return [{"title": t, "content": t + " (내용 생략)"} for t in dummy_titles]

def clean_articles(articles):
    return [a["title"].replace("?", "").replace("!", "") for a in articles]

def summarize_articles(cleaned):
    if not cleaned:
        return "요약할 내용 없음"
    return "핵심: " + cleaned[0] + " ... 등"

def analyze_stats(cleaned, keyword):
    lengths = [len(c) for c in cleaned]
    return {
        "keyword": keyword,
        "count": len(cleaned),
        "avg_length": sum(lengths) / len(lengths) if lengths else 0
    }

def visualize_stats_tk(stats):
    win = Toplevel()
    win.title("통계 결과")
    Label(win, text=f"키워드: {stats['keyword']}").pack()
    Label(win, text=f"기사 개수: {stats['count']}").pack()
    Label(win, text=f"평균 길이: {stats['avg_length']:.2f}").pack()
    Button(win, text="닫기", command=win.destroy).pack(pady=10)

def save_summary(keyword, summary):
    with open(f"{keyword}_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

def save_stats(keyword, stats):
    with open(f"{keyword}_stats.txt", "w", encoding="utf-8") as f:
        for k, v in stats.items():
            f.write(f"{k}: {v}\n")
            
def run_process():
    listbox.delete(0, END)
    key = entry.get()

    if key == "":
        result_label.config(text="키워드 입력해주세요.")
        return

    articles = crawl_news(key)
    if not articles:
        result_label.config(text="관련 뉴스 X")
        return

    for i, a in enumerate(articles, 1):
        listbox.insert(END, str(i) + ". " + a["title"])

    cleaned = clean_articles(articles)
    summary = summarize_articles(cleaned)
    stats = analyze_stats(cleaned, key)

    save_summary(key, summary)
    save_stats(key, stats)

    visualize_stats_tk(stats)

    result_label.config(text="요약:\n" + summary)

window = Tk()
window.title("키워드 기반 뉴스 요약기 (단독 실행)")
window.geometry("800x550+100+100")
window.option_add("*Font", "맑은고딕 12")

Label(window, text="키워드 입력하세요:").pack()
entry = Entry(window, width=40)
entry.pack()

Button(window, text="뉴스 분석 시작하기", command=run_process).pack(pady=10)

Label(window, text="기사 목록").pack()
listbox = Listbox(window, width=80, height=12)
listbox.pack()

result_label = Label(window, text="", fg="blue", justify="left", wraplength=700)
result_label.pack(pady=15)

window.mainloop()

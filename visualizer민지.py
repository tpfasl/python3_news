# visualizer.py
"""
Visualizer.py (English Only Version)
- English labels only
- Pie chart (Sentiment), Bar chart (Keyword Frequency), WordCloud
- TkAgg GUI compatible (Python 3.12, Windows)
- Dummy data fallback if other modules not found
- Plots saved in 'plots' folder
"""

import os
from wordcloud import WordCloud
from matplotlib import rcParams
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # GUI backend

print("Visualizer started")

# -------------------------
# 1. Force English font globally
# -------------------------
rcParams['font.family'] = 'Arial'

# -------------------------
# 2. Try import real modules, else use dummy data
# -------------------------
try:
    from crawler import fetch_news
    from cleaner import clean_text
    from summarizer import summarize_text
    from stat_module import get_sentiment_data, get_keyword_freq
    use_real_data = True
    print("Real modules imported successfully")
except ImportError:
    use_real_data = False
    print("Real modules not found, using dummy data")

# -------------------------
# 3. Ensure 'plots' folder exists
# -------------------------
os.makedirs("plots", exist_ok=True)

# -------------------------
# 4. Sentiment Pie Chart
# -------------------------


def plot_sentiment(sentiment_data):
    labels = list(sentiment_data.keys())
    sizes = list(sentiment_data.values())
    colors = ['#66b3ff', '#ff6666']

    plt.figure(figsize=(6, 6))
    plt.pie(
        sizes, labels=labels, autopct='%1.1f%%',
        colors=colors, startangle=140,
        textprops={'fontsize': 12}
    )
    plt.title("News Article Sentiment")
    plt.savefig("plots/sentiment.png")
    print("Saved: plots/sentiment.png")
    plt.show()

# -------------------------
# 5. Keyword Frequency Bar Chart
# -------------------------


def plot_keyword_freq(keyword_freq):
    words = list(keyword_freq.keys())
    counts = list(keyword_freq.values())

    plt.figure(figsize=(8, 5))
    plt.bar(words, counts, color='#77dd77')
    plt.title("Keyword Frequency")
    plt.xlabel("Keyword")
    plt.ylabel("Frequency")
    plt.savefig("plots/keyword_freq.png")
    print("Saved: plots/keyword_freq.png")
    plt.show()

# -------------------------
# 6. WordCloud
# -------------------------


def plot_wordcloud(keyword_freq):
    font_path = 'C:/Windows/Fonts/arial.ttf'  # English font
    wc = WordCloud(
        width=800, height=400, background_color='white',
        colormap='Set2', font_path=font_path
    )
    wc.generate_from_frequencies(keyword_freq)

    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title("Keyword WordCloud")
    plt.savefig("plots/wordcloud.png")
    print("Saved: plots/wordcloud.png")
    plt.show()

# -------------------------
# 7. Run visualization
# -------------------------


def run_visualization():
    if use_real_data:
        raw_articles = fetch_news()
        cleaned_articles = [clean_text(a) for a in raw_articles]
        summarized_articles = [summarize_text(a) for a in cleaned_articles]

        sentiment_data = get_sentiment_data(summarized_articles)
        keyword_freq = get_keyword_freq(summarized_articles)
    else:
        # Dummy data
        sentiment_data = {"Positive": 20, "Negative": 8}
        keyword_freq = {"AI": 12, "Python": 9, "News": 7, "Data": 5}
        print("Using dummy data")

    plot_sentiment(sentiment_data)
    plot_keyword_freq(keyword_freq)
    plot_wordcloud(keyword_freq)
    print("Visualization complete! Check 'plots' folder.")


# -------------------------
# 8. Standalone execution
# -------------------------
if __name__ == "__main__":
    run_visualization()
    print("Visualizer finished")

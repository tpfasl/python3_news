# stats_module.py
from collections import Counter
import re


class ArticleAnalyzer:
    def __init__(self, articles):
        self.articles = articles

    def _extract_words(self):
        words = []
        for a in self.articles:
            text = a.get("content", "")
            text = re.sub(r"[^가-힣a-zA-Z\s]", "", text)
            words.extend(text.split())
        return words

    def top_keywords(self, top_n=5):
        words = self._extract_words()
        return Counter(words).most_common(top_n)

    def length_stats(self):
        lengths = [len(a.get("content", "")) for a in self.articles]

        if not lengths:
            return {"min": 0, "max": 0, "avg": 0}

        return {
            "min": min(lengths),
            "max": max(lengths),
            "avg": sum(lengths) / len(lengths)
        }

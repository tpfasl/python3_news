#crawler
import requests
from bs4 import BeautifulSoup
import urllib.parse


def get_rss_items(keyword):
    """
    RSS에서 <item> 블록(제목, 링크 등) 가져오기
    """
    q = urllib.parse.quote(keyword)
    url = f"https://news.google.com/rss/search?q={q}&hl=ko&gl=KR&ceid=KR:ko"

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, timeout=3, headers=headers)
        response.raise_for_status()
    except Exception:
        return []

    soup = BeautifulSoup(response.text, "xml")
    items = soup.find_all("item")

    return items


def fetch_article_body(url):
    """
    언론사 홈페이지에서 기사 본문 HTML 텍스트 추출
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, timeout=4, headers=headers)
    except Exception:
        return ""

    soup = BeautifulSoup(r.text, "html.parser")

    # 기사 본문에 자주 쓰이는 selector들
    selectors = [
        "article",
        ".newsct_body",
        "#newsct_body",
        ".article_body",
        ".article-body",
        "#articeBody",
        "#articleBody",
        ".go_trans _article_content",
        ".view"
    ]

    for sel in selectors:
        tag = soup.select_one(sel)
        if tag:
            return tag.get_text(" ", strip=True)

    # 못 찾으면 전체 텍스트라도
    return soup.get_text(" ", strip=True)


def get_articles(keyword):
    """
    입력된 키워드 기반 뉴스 제목 + 본문 크롤링
    return [
        {"title": "...", "link": "...", "body": "..."},
        ...
    ]
    """
    items = get_rss_items(keyword)
    results = []

    items = items[:10]

    for item in items:
        title = item.title.get_text()
        link = item.link.get_text()

        # 본문 가져오기 (출력은 안 하지만, get_articles 함수 정의를 유지하기 위해 실행)
        body = fetch_article_body(link)

        results.append({
            "title": title,
            "link": link,
            "body": body
        })

    return results


# 단독 실행 테스트용
if __name__ == "__main__":
    keyword = input("검색어 입력: ")
    data = get_articles(keyword)

    for art in data:
        print(art["title"])
        print(art["link"])
        print() # 각 기사 사이에 빈 줄 추가
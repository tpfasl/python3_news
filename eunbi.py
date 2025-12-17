import requests
from bs4 import BeautifulSoup
import urllib.parse

class NewsCollector:
    """
    역할: 뉴스 목록 수집 및 사용자 인터페이스 제공
    
    """
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.rss_base_url = "https://news.google.com/rss/search?q={}&hl=ko&gl=KR&ceid=KR:ko"

    def _fetch_rss_data(self, keyword):
        """
        [예외 처리] 네트워크 요청 및 RSS 데이터 수집
        """
        try:
            encoded_keyword = urllib.parse.quote(keyword)
            url = self.rss_base_url.format(encoded_keyword)
            
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status() # HTTP 에러 발생 시 예외 호출
            
            return BeautifulSoup(response.text, "xml")
        except requests.exceptions.RequestException as e:
            print(f"\n[오류] 뉴스 데이터를 가져오는 중 문제가 발생했습니다: {e}")
            return None

    def get_news_list(self, keyword, limit=15):
        """
        키워드에 따른 뉴스 제목과 링크만 리스트로 반환
        """
        soup = self._fetch_rss_data(keyword)
        if not soup:
            return []

        items = soup.find_all("item")
        results = []

        for item in items[:limit]:
            # 제목 정제 (기존 '제목 - 언론사' 형태에서 제목만 추출)
            full_title = item.title.get_text()
            clean_title = full_title.rsplit(" - ", 1)[0] if " - " in full_title else full_title
            
            results.append({
                "title": clean_title,
                "link": item.link.get_text()
            })
        
        return results

    def start_service(self):
        """
        [실행 기능] 사용자에게 키워드를 입력받고 결과를 출력하는 메인 인터페이스
        """
        print("="*50)
        print("맞춤형 뉴스 수집 시스템 실행")
        print("="*50)

        while True:
            keyword = input("\n 검색할 뉴스 키워드를 입력하세요 (종료하려면 'q' 입력): ").strip()
            
            if keyword.lower() == 'q':
                print("시스템을 종료합니다.")
                break
            
            if not keyword:
                print("[알림] 키워드를 한 글자 이상 입력해주세요.")
                continue

            print(f"'{keyword}' 관련 최신 뉴스를 수집 중입니다...")
            news_data = self.get_news_list(keyword)

            if not news_data:
                print("검색 결과가 없거나 수집에 실패했습니다.")
            else:
                print(f"\n✅ '{keyword}' 관련 뉴스 총 {len(news_data)}개를 찾았습니다:")
                print("-" * 50)
                for idx, news in enumerate(news_data, 1):
                    print(f"[{idx}] {news['title']}")
                    print(f"{news['link']}")
                print("-" * 50)

# --- 프로그램 실행 ---
if __name__ == "__main__":
    app = NewsCollector()
    app.start_service()
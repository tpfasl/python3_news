import re

class NewsTitleCleaner:
    def __init__(self):
        
        self.publisher_pattern = re.compile(r"\s*-\s*.+$")
        self.whitespace_pattern = re.compile(r"\s+")
        
        self.quotes = ["“", "”", '"', "'"]

    def clean(self, title):
        
        if not title:
            return ""

       
        title = self.publisher_pattern.sub("", title)

       
        for q in self.quotes:
            title = title.replace(q, "")

       
        title = self.whitespace_pattern.sub(" ", title).strip()

        return title

    def clean_list(self, title_list):
        """리스트 전체를 정제하여 반환"""
        if not title_list:
            return []
            
        cleaned = [self.clean(t) for t in title_list if t is not None]
        
        return [c for c in cleaned if c]


if __name__ == "__main__":
    
    cleaner = NewsTitleCleaner()
    
    test_titles = [
        "“중국도 페이커 열풍”...베이징서 열린 T1 전시 성황 - 문화일보",
        " '손흥민 골' 토트넘 승리 - 스포츠조선 ",
        None,
        "   "
    ]
    
    result = cleaner.clean_list(test_titles)
    
    print("정제 결과:")
    for i, title in enumerate(result, 1):
        print(f"{i}. {title}")

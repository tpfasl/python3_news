import re

def clean_title(title):
    # 1) -(하이픈) 뒤 언론사명 제거
    title = re.sub(r"\s*-\s*.+$", "", title)

    # 2) 따옴표, 특수문자 정리
    title = title.replace("“", "").replace("”", "")
    title = title.replace('"', '').replace("'", "")

    # 3) 공백 정리
    title = re.sub(r"\s+", " ", title).strip()

    return title


def clean_title_list(title_list):
    cleaned = []
    for t in title_list:
        if t is None:
            continue
        ct = clean_title(t)
        if ct:
            cleaned.append(ct)
    return cleaned


if __name__ == "__main__":
    test = "“중국도 페이커 열풍”...베이징서 열린 T1 전시 성황 - 문화일보"
    print(clean_title_list([test]))




import requests
from bs4 import BeautifulSoup
import time
import random

# 네이버 뉴스 페이지 URL
news_urls = [
    "https://n.news.naver.com/article/025/0003417831?ntype=RANKING",
    "https://n.news.naver.com/article/025/0003417847?ntype=RANKING",
    "https://n.news.naver.com/article/052/0002147271?ntype=RANKING"
]

#기사 크롤링 함수
def get_news_details(url):
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML)"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        #제목 가져오기
        title = soup.find("h2", class_="media_end_head_headline").get_text(strip=True)

        #본문 가져오기
        article_body = soup.select_one("#newsct_article, .article_body, .news_end")
        if article_body:
            contents = article_body.get_text(strip=True)
        else:
            contents = "본문 없음"

        #기자명 찾기
        journalist = soup.select_one(".byline_s")
        if journalist:
            journalist = journalist.get_text(strip=True)
        else:
            #본문에서 '기자' 포함된 패턴 찾기
            import re
            match = re.search(r"([가-힣]{2,5}) 기자", contents)
            journalist = match.group(1) if match else "기자명 없음"

        #작성일 가져오기
        date = soup.select_one(".media_end_head_info_datestamp_time")
        date = date.get_text(strip=True) if date else "작성일 없음"

        #결과 출력
        print(f"\n 제목 : {title}")
        print(f"링크 : {url}")
        print(f"기자명 : {journalist}")
        print(f"작성일 : {date}")
        print(f"본문 : {contents[:100]}")
        #본문은 100자까지만 출력

    #예외 처리
    except requests.exceptions.RequestException as e:
        print(f"[오류] {url} 요청 실패 {e}")

#실행 (딜레이 추가)
for url in news_urls:
    get_news_details(url)
    time.sleep(random.uniform(1, 3))
    #1 ~ 3초 랜덤 딜레이

import requests
from bs4 import BeautifulSoup
import time

#네이버 뉴스 '많이 본 뉴스' 페이지 URL
url = "https://news.naver.com/main/ranking/popularDay.naver"

#HTTP 요청 보내기
headers = {"User-Agent":"Mozilla/5.0"}
response = requests.get(url, headers=headers)
response.raise_for_status()

#HTML 파싱
soup = BeautifulSoup(response.text, "html.parser")

#뉴스 제목과 링크 가져오기
news_items = soup.select(".rankingnews_list .list_title")

news_list = []
print("네이버 많이 본 뉴스")

for idx, item in enumerate(news_items[:10], 1):
    #상위 10개 출력
    title = item.get_text().strip()
    link = item.parent['href']
    #뉴스 링크 추출
    full_link = f"https://news.naver.com{link}" if link.startswith("/") else link
    print(f"{idx}. {title} - {full_link}")

    #개별 뉴스 기사 크롤링
    try:
        news_response = requests.get(full_link, headers=headers)
        news_response.raise_for_status()
        news_soup = BeautifulSoup(news_response.text, "html.parser")

        #기사 본문
        article = news_soup.select_one("#newsct_article")
        content = article.get_text().strip() if article else "본문 없음"

        #기자명
        journalist = news_soup.select_one(".byline_s")
        journalist_name = journalist.get_text().strip() if journalist else "기자명 없음"

        #작성일
        date = news_soup.select_one(".media_end_head_info_datestamp_time")
        date_text = date.get_text().strip() if date else "작성일 없음"

        #결과 저장
        news_list.append({"제목":title, "링크":full_link, "기자":journalist_name, "작성일":date_text, "본문":content[:100] + "..."})

        #서버 부하 방지
        time.sleep(1)

    except Exception as e:
        print(f"크롤링 실패: {e}")

#최종 결과 출력
for news in news_list:
    print("\n", "=" * 50)
    print(f"제목: {news['제목']}")
    print(f"링크: {news['링크']}")
    print(f"기자: {news['기자']}")
    print(f"작성일: {news['작성일']}")
    print(f"본문: {news['본문']}")
    
    
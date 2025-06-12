import requests
from bs4 import BeautifulSoup

# 네이버 뉴스 '많이 본 뉴스' 페이지 URL
url = "https://news.naver.com/main/ranking/popularDay.naver"

#HTTP 요청 보내기
#User-Agent  추가
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url)
response.raise_for_status() #오류 발생 시 예외 처리


#HTML 파싱
soup = BeautifulSoup(response.text, "html.parser")

#뉴스 제목 목록 가져오기
news_titles = soup.select(".rankingnews_list .list_title")

#출력
print("네이버 많이 본 뉴스")
for idx, title in enumerate(news_titles[:10], 1): #상위 10개 출력
    print(f"{idx}. {title.get_text().strip()}")

import csv
from bs4 import BeautifulSoup
import requests

#네이버 페이 크롤링
url = f"https://finance.naver.com/news/mainnews.naver"

#HTML 파싱 및 requests 요청, User-Agent 설정(봇으로 인지하지 않도록)
header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

respones = requests.get(url, headers=header)
respones.raise_for_status()

soup = BeautifulSoup(respones.text, "html.parser")

#뉴스 제목 선택
news_title = soup.select("dd.articleSubject a")

#csv 파일로 저장
filename = "pay.csv"

#인코딩을 사용하여 csv 파일을 쓰기 모드로 열어 utf-8-sig를 사용하면 한글이 깨지지 않고, 
#newline=""을 추가해 빈 줄 문제 해결
with open(filename, mode="w", encoding="utf-8-sig", newline="") as file:
    #csv 파일을 작성하는 객체를 생성
    writer = csv.writer(file)
    #csv 파일의 첫 번째 줄에 헤더(열 제목)를 추가
    writer.writerow(["번호", "제목"])

    for idx, news in enumerate(news_title, 1):
        #뉴스 제목 저장
        #크롤링한 뉴스 제목을 csv 파일에 한 줄씩 추가
        writer.writerow([idx, news.get_text().split()])

print(f"뉴스 데이터를 '{filename} 파일로 저장 완료")

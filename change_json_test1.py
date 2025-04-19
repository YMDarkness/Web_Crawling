import csv
import requests
from bs4 import BeautifulSoup

#크롤링할 웹 페이지
url = f"https://finance.naver.com/news/mainnews.naver"

#User-Agent 생성, requests 요청, HTML 파싱
headres = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

respones = requests.get(url, headers=headres)
respones.raise_for_status()

soup = BeautifulSoup(respones.text, "html.parser")

#내용 선택
category = soup.select("dd.articleSubject a")

#csv 파일로 저장
filename = "pay_to.csv"

with open(filename, mode="w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["번호", "제목"])

    for idx, title in enumerate(category, 1):
        #리스트가 아닌 문자열로 저장 ' '.join()
        writer.writerow([idx, ' '.join(title.get_text().split())])

print(f"{filename}이 생성되었습니다")

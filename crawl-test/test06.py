import requests
from bs4 import BeautifulSoup
import time
import csv
import json
import re

#검색할 키워드
search_keyword = "AI"

#User-Agent 설정
headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

#크롤링할 페이지 수
num_page = 3

#뉴스 저장 리스트, 중복 제거를 위해 세트 활용
news_list = []
seen_links = set()

#여러 페이지 크롤링
for page in range(num_page):
    start_num = page * 10 + 1 #1, 11, 21 ...
    search_url = f"https://search.naver.com/search.naver?where=news&query={search_keyword}&start={start_num}"

    response = requests.get(search_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    #네이버 뉴스 제목 class
    for news in soup.select(".news_tit"):
        title = news["title"]
        link = news["href"]

        #중복 제거
        if link not in seen_links:
            news_list.append({"제목" : title, "링크" : link})
            seen_links.add(link)

    #네트워크 부하 방지를 위해 1초 대기
    time.sleep(1)

#결과 출력
for news in news_list:
    print(f"제목 : {news['제목']}")
    print(f"링크 : {news['링크']}")
    print("-" * 50)

#csv 파일로 저장
with open("news_resulte.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["제목", "링크"])
    writer.writeheader()
    writer.writerows(news_list)

#json 파일로 저장
with open("news_resulte.json", "w", encoding="utf-8") as jsonfile:
    json.dump(news_list, jsonfile, ensure_ascii=False, indent=4)

print("크롤링 완료\n")
print("csv와 json 파일로 저장되었습니다")

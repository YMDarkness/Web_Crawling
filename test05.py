import requests
from bs4 import BeautifulSoup
import random
import csv
import json
import re
import time

#검색할 키워드
search_keyword = "AI"

#네이버 뉴스 검색 결과 url
search_url = f"https://search.naver.com/search.naver?where=news&query={search_keyword}"

#User_Agent 설정
headres = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

#요청 보내기
response = requests.get(search_url, headers=headres)
response.raise_for_status() #요청 오류 확인

#HTML 파싱
soup = BeautifulSoup(response.text, "html.parser")

#뉴스 제목과 링크 찾기
news_list = []
for news in soup.select(".news_tit"): #네이버 뉴스 제목 class
    title = news["title"]
    link = news["href"]
    news_list.append({"제목" : title, "링크" : link})

#결과 출력
for news in news_list:
    print(f"제목 : {news['제목']}")
    print(f"링크 : {news['링크']}")
    print("-" * 50)

# 크롤링 확인 및 테스팅

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import time

url = 'https://m.stock.naver.com/worldstock/index/.N225/total'

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)

driver.get(url)
time.sleep(2)

#HTTP 요청 보내기
#User-Agent  추가
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

#HTML 파싱
soup = BeautifulSoup(driver.page_source, "html.parser")

news_titles = soup.select_one('strong.GraphMain_price__H72B2')

#출력
print("크롤링 결과 테스트 : ", news_titles)

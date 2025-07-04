# 크롤링 확인 및 테스팅

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import time

url = 'https://upbit.com/exchange?code=CRIX.UPBIT.KRW-BTC&utm_source=naver&utm_medium=SA&utm_campaign=up_pc&utm_group=%EC%A3%BC%EC%9A%94%EC%A2%85%EB%AA%A9%EB%AA%85&utm_term=%EB%B9%84%ED%8A%B8%EC%BD%94%EC%9D%B8&n_media=27758&n_query=%EB%B9%84%ED%8A%B8%EC%BD%94%EC%9D%B8&n_rank=2&n_ad_group=grp-a001-01-000000051195453&n_ad=nad-a001-01-000000389016399&n_keyword_id=nkw-a001-01-000007235860525&n_keyword=%EB%B9%84%ED%8A%B8%EC%BD%94%EC%9D%B8&n_campaign_type=1&n_ad_group_type=1&n_match=1'

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

news_titles = soup.select_one('span.first > strong')

#출력
print("크롤링 결과 테스트 : ", news_titles)

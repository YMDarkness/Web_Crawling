# 크롤링 확인 및 테스팅

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import time
import re

url = 'https://m.stock.naver.com/marketindex/bond/US10YT=RR'

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

news_titles = soup.select_one('strong.DetailInfo_price__v_j1V')

#출력
print("크롤링 결과 테스트 : ", news_titles)

'''driver.quit()

# 정제된 가격을 저장할 변수 초기화
price_value = 0.0

if news_titles:
    # 1. 요소의 전체 텍스트를 가져옵니다. (결과: "3,516.101트로이온스(Troy ounce)...")
    raw_string = news_titles.text.strip()
    
    # 2. 정규 표현식으로 숫자와 소수점만 추출합니다.
    # r'\d{1,3}(?:,\d{3})*\.\d+' 패턴은 쉼표가 있는 숫자도 안전하게 찾습니다.
    match = re.search(r'(\d{1,3}(?:,\d{3})*\.\d+)', raw_string)
    
    if match:
        # 3. 찾은 문자열에서 쉼표를 제거합니다.
        extracted_price = match.group(1).replace(',', '')
        
        # 4. float 타입으로 변환합니다.
        price_value = float(extracted_price)
        print("정제된 가격:", price_value)
    else:
        print("가격 정보를 찾을 수 없습니다.")
else:
    print("원하는 HTML 요소를 찾을 수 없습니다.")'''

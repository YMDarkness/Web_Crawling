import requests
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# 원-엔화 환율

class Jpy(BaseCrawler):
    def __init__(self):
        super().__init__('jpy')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('https://finance.naver.com/marketindex/').text
        url = 'https://finance.naver.com/marketindex/exchangeDetail.naver?marketindexCd=FX_JPYKRW'
        wait_selector = (By.CLASS_NAME, 'no_today')
        super().fetch_data(url, wait_selector)

    # HTML 파싱 및 엔화 환율 데이터 추출
    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        jpy_price = soup.select_one('p.no_today')
        '''
        self.data = {
            'USD_KRW': float(usd_price.text.replace(",", "")) if usd_price else 0.0,
            'JPY_KRW': float(jpy_price.text.replace(",", "")) if jpy_price else 0.0
        }
        '''

        price = 0.0
        if jpy_price:
            # get_text()를 사용하여 중첩된 텍스트 사이에 공백을 추가
            raw_string = jpy_price.get_text(' ', strip=True)
            
            # 숫자와 소수점을 제외한 모든 문자를 제거
            cleaned_string = re.sub(r'[^0-9.]', '', raw_string)
            
            # 정제된 문자열이 비어있지 않으면 float으로 변환
            if cleaned_string:
                price = float(cleaned_string)
            else:
                print(f"가격 정보를 찾을 수 없습니다: {raw_string}")

        self.data = {'jpy_price': price}
        
        '''price = 0.0
        if jpy_price:
            raw_string = jpy_price.text.strip()

            # 정규 표현식으로 숫자와 소수점만 추출
            match = re.search(r'(\d{1,3}(?:,\d{3})*\.\d+)', raw_string)
            
            if match:
                # 추출된 문자열에서 쉼표 제거 후 float 변환
                extracted_price = match.group(1).replace(',', '').replace('\n', '')
                price = float(extracted_price)
            else:
                # 가격 정보를 찾지 못했을 경우 로그를 남겨 디버깅에 활용
                print(f"가격 정보를 찾을 수 없습니다: {raw_string}")

        self.data = {'jpy_price' : price}'''

    '''
    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric_name = f"market_{key}".replace(".", "_")
            lines.append(f"{metric_name} {value}")
        return '\n'.join(lines) + '\n'
    '''

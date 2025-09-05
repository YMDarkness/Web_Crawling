import requests
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# 미국 10년 국채금리

class US10Y(BaseCrawler):
    def __init__(self):
        super().__init__('us10y')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('').text
        url = 'https://m.stock.naver.com/marketindex/bond/US10YT=RR'
        wait_selector = (By.CLASS_NAME, 'DetailInfo_price__I_VJn')
        super().fetch_data(url, wait_selector)

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        us10y_price = soup.select_one('strong.DetailInfo_price__v_j1V')
        '''
        self.data = {
            'us10y' : float(us10y_price.text.replace(',', '').replace('원', '')) if us10y_price else 0.0
        }
        '''
        
        price = 0.0
        if us10y_price:
            raw_string = us10y_price.text.strip()

            # 정규 표현식으로 숫자와 소수점만 추출
            match = re.search(r'(\d{1,3}(?:,\d{3})*\.\d+)', raw_string)
            
            if match:
                # 추출된 문자열에서 쉼표 제거 후 float 변환
                extracted_price = match.group(1).replace(',', '').replace('\n', '')
                price = float(extracted_price)
            else:
                # 가격 정보를 찾지 못했을 경우 로그를 남겨 디버깅에 활용
                print(f"가격 정보를 찾을 수 없습니다: {raw_string}")

        self.data = {'us10y_price' : price}

    '''
    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'us10y_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'
    '''
    
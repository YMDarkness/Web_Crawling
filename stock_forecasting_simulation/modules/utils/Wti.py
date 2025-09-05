import requests
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# WTI (서부 텍사스 중질유) 시세

class WTI(BaseCrawler):
    def __init__(self):
        super().__init__('wti')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('https://finance.naver.com/marketindex/worldOilDetail.naver?marketindexCd=OIL_CL&fdtc=2').text
        url = 'https://finance.naver.com/marketindex/worldOilDetail.naver?marketindexCd=OIL_CL&fdtc=2'
        wait_selector = (By.CLASS_NAME, 'no_today')
        super().fetch_data(url, wait_selector)

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        wti_price = soup.select_one('p.no_today')
        '''
        self.data = {
            'wti_price': float(wti_price.text.replace(',', '').replace('원', '')) if wti_price else 0.0
        }
        '''
        '''price = float(
            wti_price.text.strip().split('KRW')[0].replace(',', '')
        ) if wti_price else 0.0
        self.data = {'wti_price' : price}'''

        price = 0.0
        if wti_price:
            raw_string = wti_price.text.strip()
            
            # 정규 표현식으로 숫자와 소수점만 추출
            match = re.search(r'(\d{1,3}(?:,\d{3})*\.\d+)', raw_string)
            
            if match:
                # 추출된 문자열에서 쉼표 제거 후 float 변환
                extracted_price = match.group(1).replace(',', '').replace('\n', '')
                price = float(extracted_price)
            else:
                # 가격 정보를 찾지 못했을 경우 로그를 남겨 디버깅에 활용
                print(f"가격 정보를 찾을 수 없습니다: {raw_string}")

        self.data = {'wti_price' : price}

    '''
    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'wti_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'
    '''

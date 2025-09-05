import requests
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# 국제 금 시세

class COMEXgold(BaseCrawler):
    def __init__(self):
        super().__init__('comexgold')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('https://finance.naver.com/marketindex/worldGoldDetail.naver?marketindexCd=CMDT_GC&fdtc=2').text
        url = 'https://finance.naver.com/marketindex/worldGoldDetail.naver?marketindexCd=CMDT_GC&fdtc=2'
        wait_selector = (By.CLASS_NAME, 'no_today')
        super().fetch_data(url, wait_selector)

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        comexgold_price = soup.select_one('p.no_today')
        '''
        self.data = {
            'comexgold_price': float(comexgold_price.text.replace(',', '').replace('달러', '')) if comexgold_price else 0.0
        }
        '''
        
        price = 0.0
        if comexgold_price:
            raw_string = comexgold_price.text.strip()
            
            # 정규 표현식으로 숫자와 소수점만 추출
            match = re.search(r'(\d{1,3}(?:,\d{3})*\.\d+)', raw_string)
            
            if match:
                # 추출된 문자열에서 쉼표 제거 후 float 변환
                extracted_price = match.group(1).replace(',', '')
                price = float(extracted_price)
            else:
                # 가격 정보를 찾지 못했을 경우 로그를 남겨 디버깅에 활용
                print(f"가격 정보를 찾을 수 없습니다: {raw_string}")

        self.data = {'comexgold_price' : price}

    '''
    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'comexgold_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'
    '''
    
    '''
    2번 안
        price = 0.0
        if comexgold_price:
            raw_string = comexgold_price.text.strip()
            
            # 정규 표현식으로 숫자와 소수점만 추출
            match = re.search(r'(\d{1,3}(?:,\d{3})*\.\d+)', raw_string)
            
            if match:
                # 추출된 문자열에서 쉼표 제거 후 float 변환
                extracted_price = match.group(1).replace(',', '')
                price = float(extracted_price)
            else:
                # 가격 정보를 찾지 못했을 경우 로그를 남겨 디버깅에 활용
                print(f"가격 정보를 찾을 수 없습니다: {raw_string}")

        self.data = {'comexgold_price' : price}
    '''

    '''
    1번 안
        price = 0.0
        if comexgold_price:
            # get_text(' ', strip=True)를 사용하여 중첩된 텍스트 사이에 공백을 추가
            price_string = comexgold_price.get_text(' ', strip=True)
            
            # 정규 표현식으로 숫자와 쉼표, 소수점을 포함한 패턴을 모두 찾습니다.
            match = re.findall(r'(\d{1,3}(?:,\d{3})*\.\d+)', price_string)

            if match:
                # 찾은 값 리스트에서 첫 번째 요소를 사용하고 쉼표를 제거 후 float으로 변환
                price = float(match[0].replace(',', ''))
        
        self.data = {'comexgold_price': price}
    '''
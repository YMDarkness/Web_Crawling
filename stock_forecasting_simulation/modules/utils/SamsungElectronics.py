import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# 삼성전자 주가

class SamsungElectronics(BaseCrawler):
    def __init__(self):
        super().__init__('samsungelectronics')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('https://finance.naver.com/item/main.naver?code=005930').text
        url = 'https://finance.naver.com/item/main.naver?code=005930'
        wait_selector = (By.CLASS_NAME, 'no_today')
        super().fetch_data(url, wait_selector)

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        samsungelectronics_price = soup.select_one('p.no_today')
        '''
        self.data = {
            'samsungelectronics_price': 
            float(samsungelectronics_price.text.replace(',', '')
                  .replace('원', '')) if samsungelectronics_price else 0.0
        }
        '''
        price = float(
            samsungelectronics_price.text.strip().split('KRW')[0].replace(',', '')
        ) if samsungelectronics_price else 0.0
        self.data = {'samsungelectronics_price' : price}

    '''
    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'samsungelectronics_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'
    '''
    
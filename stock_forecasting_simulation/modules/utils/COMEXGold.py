import requests
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
        price = float(
            comexgold_price.text.strip().split('USD')[0].replace(',', '')
        ) if comexgold_price else 0.0
        self.data = {'comexgold_price' : price}

    '''
    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'comexgold_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'
    '''

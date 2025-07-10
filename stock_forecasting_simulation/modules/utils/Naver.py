import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# NAVER 주가

class Naver(BaseCrawler):
    def __init__(self):
        super().__init__('naver')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('https://finance.naver.com/item/main.naver?code=035420').text
        url = 'https://finance.naver.com/item/main.naver?code=035420'
        wait_selector = (By.CLASS_NAME, 'no_today')
        super().fetch_data(url, wait_selector)

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        naver_price = soup.select_one('p.no_today')
        '''
        self.data = {
            'naver_price' : float(naver_price.text.replace(',', '').replace('원', '')) if naver_price else 0.0
        }
        '''
        price = float(
            naver_price.text.strip().split('KRW')[0].replace(',', '')
        ) if naver_price else 0.0
        self.data = {'naver_price' : price}

    '''
    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'naver_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'
    '''

import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# LG 에너지솔루션 주가

class LGensol(BaseCrawler):
    def __init__(self):
        super().__init__('lgensol')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('https://finance.naver.com/item/main.naver?code=373220').text
        url = 'https://finance.naver.com/item/main.naver?code=373220'
        wait_selector = (By.CLASS_NAME, 'no_today')
        super().fetch_data(url, wait_selector)

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        lgensol_price = soup.select_one('p.no_today')
        '''
        self.data = {
            'lgensol_price' : float(lgensol_price.text.replace(',', '').replace('원', '')) if lgensol_price else 0.0
        }
        '''
        price = float(
            lgensol_price.text.strip().split('KRW')[0].replace(',', '')
        ) if lgensol_price else 0.0
        self.data = {'lgensol_price' : price}

    '''
    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'lgensol_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'
    '''
    
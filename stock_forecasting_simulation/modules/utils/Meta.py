import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# 메타(구 페이스북) 주가

class Meta(BaseCrawler):
    def __init__(self):
        super().__init__('meta')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('').text
        url = 'https://m.stock.naver.com/worldstock/stock/META.O/total'
        wait_selector = (By.CLASS_NAME, 'GraphMain_price__H72B2')
        super().fetch_data(url, wait_selector)

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        meta_price = soup.select_one('strong.GraphMain_price__H72B2')
        '''
        self.data = {
            'meta_price' : float(meta_price.text.replace(',','').replace('원', '')) if meta_price else 0.0
        }
        '''
        price = float(
            meta_price.text.strip().split('USD')[0].replace(',', '')
        ) if meta_price else 0.0
        self.data = {'meta_price' : price}

    '''
    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'meta_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'
    '''

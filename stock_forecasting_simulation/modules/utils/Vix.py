import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# VIX (공포지수) 지수

class VIX(BaseCrawler):
    def __init__(self):
        super().__init__('vix')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('').text
        url = 'https://m.stock.naver.com/worldstock/index/.VIX/total'
        wait_selector = (By.CLASS_NAME, 'GraphMain_price__H72B2')
        super().fetch_data(url, wait_selector)

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        vix_price = soup.select_one('strong.GraphMain_price__H72B2')
        '''
        self.data = {
            'vix_price' : float(vix_price.text.replace(',', '').replace('원', '')) if vix_price else 0.0
        }
        '''
        price = float(
            vix_price.text.strip().split('USD')[0].replace(',', '')
        ) if vix_price else 0.0
        self.data = {'vix_price' : price}

    '''
    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'vix_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'
    '''
    
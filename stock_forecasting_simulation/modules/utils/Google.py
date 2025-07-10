import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# 알파벳(구글) 주가

class Google(BaseCrawler):
    def __init__(self):
        super().__init__('google')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('').text
        url = 'https://m.stock.naver.com/worldstock/stock/GOOG.O/total'
        wait_selector = (By.CLASS_NAME, 'GraphMain_price__H72B2')
        super().fetch_data(url, wait_selector)

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        google_price = soup.select_one('strong.GraphMain_price__H72B2')
        '''
        self.data = {
            'google_price' : float(google_price.text.replace(',', '').replace('원', '')) if google_price else 0.0
        }
        '''
        price = float(
            google_price.text.strip().split('USD')[0].replace(',', '')
        ) if google_price else 0.0
        self.data = {'google_price' : price}

    '''
    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'google_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'
    '''
    
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# 니케이 225 지수

class N225(BaseCrawler):
    def __init__(self):
        super().__init__('n225')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('').text
        url = 'https://m.stock.naver.com/worldstock/index/.N225/total'
        wait_selector = (By.CLASS_NAME, 'GraphMain_price__H72B2')
        super().fetch_data(url, wait_selector)

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        n225_price = soup.select_one('strong.GraphMain_price__H72B2')
        '''
        self.data = {
            'n225' : float(n225_price.text.replace(',', '').replace('원', '')) if n225_price else 0.0
        }
        '''
        price = float(
            n225_price.text.strip().split('JPY')[0].replace(',', '')
        ) if n225_price else 0.0
        self.data = {'n225_price' : price}

    '''
    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'n225_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'
    '''

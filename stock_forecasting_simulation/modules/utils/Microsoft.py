import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# 마이크로소프트 주가

class Microsoft(BaseCrawler):
    def __init__(self):
        super().__init__('microsoft')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('').text
        url = 'https://m.stock.naver.com/worldstock/stock/MSFT.O/total'
        wait_selector = (By.CLASS_NAME, 'GraphMain_price__H72B2')
        super().fetch_data(url, wait_selector)

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        microsoft_price = soup.select_one('strong.GraphMain_price__H72B2')
        '''
        self.data = {
            'microsoft_price' : 
            float(microsoft_price.text.replace(',', '')
                  .replace('원', '')) if microsoft_price else 0.0
        }
        '''
        price = float(
            microsoft_price.text.strip().split('USD')[0].replace(',', '')
        ) if microsoft_price else 0.0
        self.data = {'microsoft_price' : price}

    '''
    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'microsoft_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'
    '''

import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# AMD 주가

class AMD(BaseCrawler):
    def __init__(self):
        super().__init__('amd')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('').text
        url = 'https://m.stock.naver.com/worldstock/stock/AMD.O/total'
        wait_selector = (By.CLASS_NAME, 'GraphMain_price__H72B2')
        super().fetch_data(url, wait_selector)

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        amd_price = soup.select_one('strong.GraphMain_price__H72B2')
        '''
        self.data = {
            'amd_price' : float(amd_price.text.replace(',', '').replace('원', '')) if amd_price else 0.0
        }
        '''
        price = float(
            amd_price.text.strip().split('USD')[0].replace(',', '')
            ) if amd_price else 0.0
        self.data = {'amd_price' : price}

    '''
    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'amd_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'
    '''
    
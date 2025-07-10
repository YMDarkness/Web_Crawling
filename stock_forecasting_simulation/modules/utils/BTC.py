import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# 비트코인

class BTC(BaseCrawler):
    def __init__(self):
        super().__init__('btc')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('').text
        url = 'https://m.stock.naver.com/crypto/UPBIT/BTC'
        wait_selector = (By.CLASS_NAME, 'DetailInfo_price__yCAl0')
        super().fetch_data(url, wait_selector)

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        btc_price = soup.select_one('div.DetailInfo_price__yCAl0')
        '''
        self.data = {
            'btc' : float(btc_price.text.replace(',', '').replace('원', '')) if btc_price else 0.0
        }
        '''
        price = float(
            btc_price.text.strip().split('USD')[0].replace(',', '')
        ) if btc_price else 0.0
        self.data = {'btc_price' : price}

    '''
    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'btc_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'
    '''
    
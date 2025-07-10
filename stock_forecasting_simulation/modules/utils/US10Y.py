import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# 미국 10년 국채금리

class US10Y(BaseCrawler):
    def __init__(self):
        super().__init__('us10y')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('').text
        url = 'https://m.stock.naver.com/marketindex/bond/US10YT=RR'
        wait_selector = (By.CLASS_NAME, 'DetailInfo_price__I_VJn')
        super().fetch_data(url, wait_selector)

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        us10y_price = soup.select_one('strong.DetailInfo_price__I_VJn')
        '''
        self.data = {
            'us10y' : float(us10y_price.text.replace(',', '').replace('원', '')) if us10y_price else 0.0
        }
        '''
        price = float(
            us10y_price.text.strip().split('USD')[0].replace(',', '')
        ) if us10y_price else 0.0
        self.data = {'us10y_price' : price}

    '''
    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'us10y_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'
    '''
    
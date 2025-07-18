import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# 코스피 지수

class Kospi(BaseCrawler):
    def __init__(self):
        super().__init__('kospi')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('https://finance.naver.com/sise/sise_index.naver?code=KOSPI').text
        url = 'https://finance.naver.com/sise/sise_index.naver?code=KOSPI'
        wait_selector = (By.CLASS_NAME, 'now_value')
        super().fetch_data(url, wait_selector)

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        kospi_price = soup.select_one('#now_value')
        '''
        self.data = {
            'kospi_data' : float(kospi_price.text.replace(',', '').replace('원', '')) if kospi_price else 0.0
        }
        '''
        price = float(
            kospi_price.text.strip().split('KRW')[0].replace(',', '')
        ) if kospi_price else 0.0
        self.data = {'kospi_price' : price}

    '''
    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'kospi_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'
    '''

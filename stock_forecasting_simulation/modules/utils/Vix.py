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
        self.html = requests.get('').text

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        vix_price = soup.select_one('')
        self.data = {
            'vix_price' : float(vix_price.text.replace(',', '').replace('원', '')) if vix_price else 0.0
        }

    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'vix_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'

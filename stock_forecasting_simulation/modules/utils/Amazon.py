import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# 아마존 주가

class Amazon(BaseCrawler):
    def __init__(self):
        super().__init__('amazon')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        self.html = requests.get('').text

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        amazon_price = soup.select_one('')
        self.data = {
            'amazon_price' : float(amazon_price.text.replace(',', '').replace('원', '')) if amazon_price else 0.0
        }

    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'amazon_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'

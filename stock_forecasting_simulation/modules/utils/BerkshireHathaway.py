import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# 버크셔 헤서웨이 주가

class BerkshireHathaway(BaseCrawler):
    def __init__(self):
        super().__init__('berkshire_hathaway')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        self.html = requests.get('').text

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        berkshire_price = soup.select_one('')
        self.data = {
            'berkshire_price': float(berkshire_price.text.replace(',', '').replace('원', '')) if berkshire_price else 0.0
        }

    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'berkshire_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'

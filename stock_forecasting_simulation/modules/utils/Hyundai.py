import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# 현대 자동차 주가

class Hyundai(BaseCrawler):
    def __init__(self):
        super().__init__('hyundai')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        self.html = requests.get('https://finance.naver.com/item/main.naver?code=005380').text

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        hyundai_price = soup.select_one('#rate_info_krx > div.today > p.no_today')
        self.data = {
            'hyundai_price': float(hyundai_price.text.replace(',', '').replace('원', '')) if hyundai_price else 0.0
        }

    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'hyundai_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'

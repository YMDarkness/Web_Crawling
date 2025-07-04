import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# 한화에어로스페이스 주가

class HanwhaAerospace(BaseCrawler):
    def __init__(self):
        super().__init__('hanwhaaerospace')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        self.html = requests.get('https://finance.naver.com/item/main.naver?code=012450').text

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        hanwhaaerospace_price = soup.select_one('#rate_info_krx > div.today > p.no_today')
        self.data = {
            'hanwhaaerospace_price' : 
            float(hanwhaaerospace_price.text.replace(',', '')
                  .replace('원', '')) if hanwhaaerospace_price else 0.0
        }

    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'hanwhaaerospace_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'

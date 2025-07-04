import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# 나스닥 지수

class IXIC(BaseCrawler):
    def __init__(self):
        super().__init__('ixic')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        self.html = requests.get('https://finance.naver.com/world/sise.naver?symbol=NAS@IXIC').text

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        ixic_price = soup.select_one('#content > div.rate_info > div.today > p.no_today')
        self.data = {
            'ixic_price' : float(ixic_price.text.replace(',', '').replace('원', '')) if ixic_price else 0.0
        }

    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'ixic_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'

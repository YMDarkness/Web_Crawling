import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# 달러 인덱스 지수

class DXY(BaseCrawler):
    def __init__(self):
        super().__init__('dxy')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        self.html = requests.get('https://finance.naver.com/marketindex/worldExchangeDetail.naver?marketindexCd=FX_USDX').text

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        dxy_price = soup.select_one('#content > div.spot > div.today > p.no_today')
        self.data = {
            'dxy_price' : float(dxy_price.text.replace(',','').replace('원', '')) if dxy_price else 0.0
        }

    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'dxy_{key}'.replace('.','')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'

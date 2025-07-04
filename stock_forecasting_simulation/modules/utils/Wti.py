import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# WTI (서부 텍사스 중질유) 시세

class WTI(BaseCrawler):
    def __init__(self):
        super().__init__('wti')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        self.html = requests.get('https://finance.naver.com/marketindex/worldOilDetail.naver?marketindexCd=OIL_CL&fdtc=2').text

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        wti_price = soup.select_one('#content > div.spot > div.today > p.no_today')
        self.data = {
            'wti_price': float(wti_price.text.replace(',', '').replace('원', '')) if wti_price else 0.0
        }

    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'wti_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'

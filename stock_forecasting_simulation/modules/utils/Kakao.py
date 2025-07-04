import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# Kakao 주가

class Kakao(BaseCrawler):
    def __init__(self):
        super().__init__('kakao')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        self.html = requests.get('https://finance.naver.com/item/main.naver?code=035720').text

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        kakao_price = soup.select_one('#rate_info_krx > div.today > p.no_today')
        self.data = {
            'kakao_price' : float(kakao_price.text.replace(',', '').replace('원', '')) if kakao_price else 0.0
        }

    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'kakao_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'

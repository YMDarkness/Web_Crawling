import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# 삼성바이오로직스 주가

class SamsungBioLogics(BaseCrawler):
    def __init__(self):
        super().__init__('samsungbiologics')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        self.html = requests.get('https://finance.naver.com/item/main.naver?code=207940').text

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        samsungbiologics_price = soup.select_one('#rate_info_krx > div.today > p.no_today')
        self.data = {
            'samsungbiologics_price' : 
            float(samsungbiologics_price.text.replace(',', '')
                  .replace('원', '')) if samsungbiologics_price else 0.0
        }

    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'samsungbiologics_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'

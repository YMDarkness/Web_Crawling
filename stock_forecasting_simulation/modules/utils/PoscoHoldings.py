import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# POSCO홀딩스 주가

class PoscoHoldings(BaseCrawler):
    def __init__(self):
        super().__init__('poscohodings')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        self.html = requests.get('https://finance.naver.com/item/main.naver?code=005490').text

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        poscoholdings_price = soup.select_one('#rate_info_krx > div.today > p.no_today')
        self.data = {
            'poscoholdings_price' : 
            float(poscoholdings_price.text.replace(',', '')
                  .replace('원', '')) if poscoholdings_price else 0.0
        }

    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'poscoholdings_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'

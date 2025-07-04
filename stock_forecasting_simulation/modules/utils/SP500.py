import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# S&P 500 지수

class GSPC(BaseCrawler):
    def __init__(self):
        super().__init__('sp500')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        self.html = requests.get('https://finance.naver.com/world/sise.naver?symbol=SPI@SPX').text

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        gspc_price = soup.select_one('#content > div.rate_info > div.today > p.no_today')
        self.data = {
            'sp500' : float(gspc_price.text.replace(',', '').replace('원', '')) if gspc_price else 0.0
        }

    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'sp500_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'

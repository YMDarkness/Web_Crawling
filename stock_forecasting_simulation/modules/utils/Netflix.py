import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# 넷플릭스 주가

class Netflix(BaseCrawler):
    def __init__(self):
        super().__init__('netflix')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        self.html = requests.get('').text
    
    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        netflix_price = soup.select_one('')
        self.data = {
            'netflix_price' : float(netflix_price.text.replace(',', '').replace('원', '')) if netflix_price else 0.0
        }

    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'netflix_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'

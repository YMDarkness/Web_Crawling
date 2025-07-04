import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# 엔비디아 주가

class Nvidia(BaseCrawler):
    def __init__(self):
        super().__init__('nvidia')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        self.html = requests.get('').text

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        nvidia_price = soup.select_one('')
        self.data = {
            'nvidia_price' : 
            float(nvidia_price.text.replace(',','')
                  .replace('원', '')) if nvidia_price else 0.0
        }

    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'nvidia_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'

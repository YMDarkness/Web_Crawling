import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# 애플 주가

class Apple(BaseCrawler):
    def __init__(self):
        super().__init__('apple')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        self.html = requests.get('').text
    
    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        apple_price = soup.select_one('')
        self.data = {
            'apple_price' : float(apple_price.text.replace(',', '').replace('원', '')) if apple_price else 0.0
        }

    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'apple_{key}'.replace('.', '') # 지표 이름 생성
            lines.append(f'{metric} {value}') # Prometheus 포맷 생성
        return '\n'.join(lines) + '\n' # 한 줄씩 붙이기
    # 크롤링한 데이터를 Prometheus가 이해할 수 있는 텍스트 포맷으로 변환하는 역할

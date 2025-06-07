import requests
from bs4 import BeautifulSoup
from .base_collector import BaseCollector

# 금 시세 정보 수집기

class GoldCollector(BaseCollector):
    def __init__(self):
        super().__init__('gold')

    # 수집 대상 웹페이지 요청
    def fetch(self):
        self.html = requests.get('https://finance.naver.com/marketindex/goldDetail.naver').text

    # HTML 파싱 및 금 시세 데이터 추출
    def parse(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        gold_elem = soup.select_one('.gold_td td:nth-child(2)')
        self.data = {
            '금_시세 ': float(gold_elem.text.replace(", ", "").replace("원", "")) if gold_elem else 0.0
        }

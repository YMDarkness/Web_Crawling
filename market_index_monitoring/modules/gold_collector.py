import requests
from bs4 import BeautifulSoup
from .base_collector import BaseCollector

# 금 시세 정보 수집기

class GoldCollector(BaseCollector):
    def __init__(self):
        super().__init__('gold')

    # 수집 대상 웹페이지 요청
    def fetch(self):
        self.html = requests.get('https://finance.naver.com/marketindex/').text

    # HTML 파싱 및 금 시세 데이터 추출
    def parse(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        gold_elem = soup.select_one('#oilGoldList > li > a.head.gold_domestic > div > span.value')
        self.data = {
            'gold_price': float(gold_elem.text.replace(",", "").replace("원", "")) if gold_elem else 0.0
        }

    def to_prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric_name = f"gold_{key}".replace(".", "_")
            lines.append(f"{metric_name} {value}")
        return '\n'.join(lines) + '\n'

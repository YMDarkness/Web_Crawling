import requests
from bs4 import BeautifulSoup
from .base_collector import BaseCollector

# 환율 정보 (USD/KRW, JPY/KRW) 수집기

class MarketCollector(BaseCollector):
    def __init__(self):
        self.data = {}

    # 수집 대상 웹페이지 요청
    def fetch(self):
        self.html = requests.get('https://finance.naver.com/marketindex/').text

    # HTML 파싱 및 환율 데이터 추출
    def parse(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        usd_elem = soup.select_one('#exchangeList > li.on > a.head.usd > div > span.value')
        jpy_elem = soup.select_one('#exchangeList > li > a.head.jpy > div > span.value')
        self.data = {
            'USD_KRW': float(usd_elem.text.replace(",", "")) if usd_elem else 0.0,
            'JPY_KRW': float(jpy_elem.text.replace(",", "")) if jpy_elem else 0.0
        }

    def to_prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric_name = f"market_{key}".replace(".", "_")
            lines.append(f"{metric_name} {value}")
        return '\n'.join(lines) + '\n'

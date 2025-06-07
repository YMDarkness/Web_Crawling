import requests
from bs4 import BeautifulSoup
from .base_collector import BaseCollector

# 환율 정보 (USD/KRW, JPY/KRW) 수집기

class MarketCollector(BaseCollector):
    def __init__(self):
        super().__init__('market')

    # 수집 대상 웹페이지 요청
    def fetch(self):
        self.html = requests.get('https://finance.naver.com/marketindex/').text

    # HTML 파싱 및 환율 데이터 추출
    def parse(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        usd_elem = soup.select_one('#exchangeList > li.on > a.head.usd > div > span.value')
        jpy_elem = soup.select_one('#exchangeList > li.on > a.head.jpy > div > span.value')
        self.data = {
            '달러_환율': float(usd_elem.text.replace(",", "")) if usd_elem else 0.0,
            '엔화_환율': float(jpy_elem.text.replace(",", "")) if jpy_elem else 0.0
        }

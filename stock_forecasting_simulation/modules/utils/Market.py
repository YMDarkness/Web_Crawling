import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# 원-달러 환율

class Market(BaseCrawler):
    def __init__(self):
        self.data = {}

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        self.html = requests.get('https://finance.naver.com/marketindex/').text

    # HTML 파싱 및 엔-달러 환율 데이터 추출
    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        usd_price = soup.select_one('#exchangeList > li.on > a.head.usd > div > span.value')
        jpy_price = soup.select_one('#exchangeList > li > a.head.jpy > div > span.value')
        self.data = {
            'USD_KRW': float(usd_price.text.replace(",", "")) if usd_price else 0.0,
            'JPY_KRW': float(jpy_price.text.replace(",", "")) if jpy_price else 0.0
        }


    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric_name = f"market_{key}".replace(".", "_")
            lines.append(f"{metric_name} {value}")
        return '\n'.join(lines) + '\n'

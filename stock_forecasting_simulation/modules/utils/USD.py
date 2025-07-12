import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# 원-달러 환율

class Usd(BaseCrawler):
    def __init__(self):
        self.data = {}

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('https://finance.naver.com/marketindex/').text
        url = 'https://finance.naver.com/marketindex/exchangeDetail.naver?marketindexCd=FX_USDKRW'
        wait_selector = (By.CLASS_NAME, 'no_today')
        super().fetch_data(url, wait_selector)

    # HTML 파싱 및 달러 환율 데이터 추출
    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        usd_price = soup.select_one('p.no_today')
        '''
        self.data = {
            'USD_KRW': float(usd_price.text.replace(",", "")) if usd_price else 0.0,
            'JPY_KRW': float(jpy_price.text.replace(",", "")) if jpy_price else 0.0
        }
        '''
        usd_prices = float(
            usd_price.text.strip().split('KRW')[0].replace(',', '')
        ) if usd_price else 0.0
        self.data = {'usd_price' : usd_prices}

    '''
    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric_name = f"market_{key}".replace(".", "_")
            lines.append(f"{metric_name} {value}")
        return '\n'.join(lines) + '\n'
    '''

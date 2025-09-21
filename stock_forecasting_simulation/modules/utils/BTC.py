import requests
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from .BaseCrawler import BaseCrawler
from .price_parser import extract_price

# 비트코인

class BTC(BaseCrawler):
    def __init__(self):
        super().__init__('btc')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('').text
        url = 'https://m.stock.naver.com/crypto/UPBIT/BTC'
        wait_selector = (By.CLASS_NAME, 'DetailInfo_price__yCAl0')
        super().fetch_data(url, wait_selector)

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        btc_price = soup.select_one('div.DetailInfo_price__yCAl0')
        
        price = 0.0
        if btc_price:
            price = extract_price(btc_price.text)

        self.data = {'btc_price' : price}
